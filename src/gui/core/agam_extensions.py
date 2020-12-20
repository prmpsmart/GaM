from .prmp_gui.extensions import *
from .agam_dialogs import *
from ...backend.core.date_time import MONTHS_NAMES, DAYS_NAMES, DateTime
from ...backend.agam.agam import AGAM
from ...backend.dc.dc_regions import Client


class RegionRadioCombo(RadioCombo):
    
    def __init__(self, master=None, region=None, regionLevel=5, recievers=[], **kwargs):
        super().__init__(master, **kwargs)
        
        self._subRegionDict = {}
        self.subRegionDict = {}
        self.set(region)
        self.choosen = None
        self.region = region
        self._receivers = recievers
        self.regionLevel = regionLevel
    
    def addReceiver(self, receiver):
        if receiver not in self._receivers: self._receivers.append(receiver)
        elif isinstance(receiver, (list, tuple)): 
            for recv in receiver: self.addReceiver(recv)
    
    def clicked(self, e=0):
        val = super().clicked()
        regVal = self.get()
        
        if regVal and self._receivers:
            for recv in self._receivers: recv((self, regVal))
    
    def get(self):
        val = self.B.get()
        regVal = self.subRegionDict.get(val)
        _regval = self._subRegionDict.get(val)
        
        if regVal: return regVal
        elif _regval: return _regval
        else: return self.choosen
    
    def receiver(self, tup):
        wid, region = tup
        self.var.set(self.val)
        wid.unlight()
        self.light()
        self.set(region)
        
    def processRegionSubs(self, region):
        rm = region.subRegions
        
        if rm:
            for region in rm:
                rname = region.name
                self._subRegionDict[rname] = region
                try: number = region.number
                except: number = rm.index(region) + 1
                name = f'{number})  {rname}'
                self.subRegionDict[name] = region
        # else: self.subRegionDict[region.name] = region
    
    def setKeys(self, region=None):
        if region:
            self.processRegionSubs(region)
            keys = self.getSubKeys()
            if keys:
                self.changeValues(keys)
                self.B.set(keys[0])
        
    def set(self, region):
        if region:
            self.subRegionDict = {}
            self._subRegionDict = {}
            regionLevel = len(region.hierachy)
            
            assert regionLevel  == self.regionLevel, f'Incorrect region of level {regionLevel} given, level must be {self.regionLevel}'
            self.setKeys(region)
            self.region = region
    
    def getSubKeys(self):
        keys = list(self.subRegionDict.keys())
        keys.sort()
        
        return keys
RRC = RegionRadioCombo

class Hierachy(PRMP_TreeView):
    __shows = ['tree', 'headings']
    __slots__ = ['tree']
    
    def __init__(self, master=None, columns=[], **kwargs):
        super().__init__(master=master, columns=columns, **kwargs)
        
        from .agam_apps import RegionDetails
        self.RD = RegionDetails
    
    def bindings(self):
        super().bindings()
        self.treeview.bind('<Control-Return>', self.viewRegion)

    def viewRegion(self, e=0):
        current = self.selected()
        if current:
            if current._type == 'reg':
                if current.level == 5: PersonDialog(self, title=current.name, values=current.person.values)
                else: self.RD(self, region=current)
H = Hierachy


class OfficeDetails(LabelFrame):
    def __init__(self, master=None, text='Office Details', office=None, **kwargs):
        super().__init__(master=master, text=text, **kwargs)

        self.office = office
        
        Label(self, text='Office').place(relx=.02, rely=0, relh=.3, relw=.35)

        Label(self, text='Areas', place=dict(relx=.02, rely=.32, relh=.32, relw=.35))

        Label(self, text='Clients', place=dict(relx=.02, rely=.66, relh=.32, relw=.35))

        self.name = Label(self, asEntry=True, font='PRMP_FONT', text='Owode', place=dict(relx=.4, rely=0, relh=.3, relw=.58))

        self.areas = Label(self, asEntry=True, font='PRMP_FONT', text='6', place=dict(relx=.4, rely=.32, relh=.3, relw=.58))

        self.clients = Label(self, asEntry=True, font='PRMP_FONT', text='1280', place=dict(relx=.4, rely=.66, relh=.3, relw=.58))


class MonthBox(LabelFrame):
    def __init__(self, master=None, text='Month', account=None, **kwargs):
        super().__init__(master=master, text=text, **kwargs)

        self.account = account
        
        self.month = Label(self, text='December 2020', place=dict(relx=.02, rely=0, relh=.35, relw=.96))

        Label(self, text='Active Clients', place=dict(relx=.02, rely=.4, relh=.25, relw=.5))

        self.activeClients = Label(self, asEntry=True, font='PRMP_FONT', text='360', place=dict(relx=.55, rely=.4, relh=.25, relw=.43))

        self.previous = Button(self, text='Previous', place=dict(relx=.02, rely=.73, relh=.2, relw=.3))

        self.current = Button(self, text='Current', place=dict(relx=.35, rely=.73, relh=.2, relw=.3))

        self.next = Button(self, text='Next', place=dict(relx=.68, rely=.73, relh=.2, relw=.3))


class AccountHighlight(LabelFrame):
    def __init__(self, master=None, text='Account Highlight', subOffice=None, **kwargs):
        super().__init__(master=master, text=text, **kwargs)

        self.subOffice = subOffice
        
        Label(self, text='Areas', place=dict(relx=.02, rely=.01, relh=.1, relw=.17))

        Label(self, text='Clients', place=dict(relx=.02, rely=.13, relh=.1, relw=.17))

        self.sups = Combobox(self, place=dict(relx=.2, rely=.01, relh=.1, relw=.3))

        self.subs = Combobox(self, place=dict(relx=.2, rely=.13, relh=.1, relw=.3))

        
        accounts = LabelFrame(self, text='Accounts', place=dict(relx=.02, rely=.23, relh=.692, relw=.965))

        # self.style.configure('Treeview.Heading',  font=font9)
        self.Scrolledtreeview1 = ScrolledTreeView(accounts)
        self.Scrolledtreeview1.place(relx=.01, rely=.005, relh=.99, relw=.98)
        self.Scrolledtreeview1.configure(columns="Col1")
        # build_treeview_support starting.
        self.Scrolledtreeview1.heading("#0",text="Tree")
        self.Scrolledtreeview1.heading("#0",anchor="center")
        self.Scrolledtreeview1.column("#0",w="257")
        self.Scrolledtreeview1.column("#0",minw="20")
        self.Scrolledtreeview1.column("#0",stretch="1")
        self.Scrolledtreeview1.column("#0",anchor="w")
        self.Scrolledtreeview1.heading("Col1",text="Col1")
        self.Scrolledtreeview1.heading("Col1",anchor="center")
        self.Scrolledtreeview1.column("Col1",w="258")
        self.Scrolledtreeview1.column("Col1",minw="20")
        self.Scrolledtreeview1.column("Col1",stretch="1")
        self.Scrolledtreeview1.column("Col1",anchor="w")


class SearchPersonalDetails(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.name = LabelEntry(self, topKwargs=dict(config=dict(text='Name', anchor='center')), place=dict(relx=.02, rely=0, relh=.18, relw=.5), orient='h', longent=.25)

        self.number = LabelEntry(self, topKwargs=dict(config=dict(text='Number', anchor='center')), place=dict(relx=.57, rely=0, relh=.18, relw=.35), orient='h', longent=.4)

        self.phone = LabelEntry(self, topKwargs=dict(config=dict(text='Phone', anchor='center')), place=dict(relx=.02, rely=.22, relh=.18, relw=.35), orient='h', longent=.3)

        self.email = LabelEntry(self, topKwargs=dict(config=dict(text='Email', anchor='center')), bottomKwargs=dict(_type='email'), place=dict(relx=.4, rely=.22, relh=.18, relw=.5), orient='h', longent=.3)

        self.id = LabelEntry(self, topKwargs=dict(config=dict(text='ID', anchor='center')), place=dict(relx=.02, rely=.42, relh=.18, relw=.4), orient='h', longent=.2)

        self.gender = LabelEntry(self, topKwargs=dict(config=dict(text='Gender', anchor='center')), place=dict(relx=.46, rely=.42, relh=.18, relw=.5), orient='h', longent=.3)

        self.address = LabelText(self, topKwargs=dict(config=dict(text='Address', anchor='center')), place=dict(relx=.02, rely=.62, relh=.36, relw=.7), orient='h', longent=.23, widthent=.43)


class SearchRecordDetails(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        Label(self, text='Date', place=dict(relx=.02, rely=0, relh=.25, relw=.2))
        self.date = PRMP_DateButton(self, text='06/12/2020', place=dict(relx=.24, rely=0, relh=.25, relw=.2))

        Label(self, text='Range', place=dict(relx=.02, rely=.27, relh=.25, relw=.2))

        self.range1 = Entry(self, place=dict(relx=.24, rely=.27, relh=.25, relw=.25), _type='number')

        SLabel(self, config=dict(text='- to -', relief='flat', anchor='center'), place=dict(relx=.51, rely=.27, relh=.25, relw=.2))

        self.range2 = Entry(self, place=dict(relx=.73, rely=.27, relh=.25, relw=.25), _type='number')

        Label(self, text='Note', place=dict(relx=.02, rely=.54, relh=.25, relw=.2 ))
        self.note = Text(self, wrap='word', place=dict(relx=.24, rely=.54, relh=.42, relw=.74), very=True)


class DateSearch(LabelFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.date = PRMP_DateButton(self, text='06/12/2020', place=dict(relx=.02, rely=0, relh=.2, relw=.22))

        self.season = tk.StringVar()
        self.season.set('sub')

        self.year = Radiobutton(self, text='Year', variable=self.season, value='year', place=dict(relx=.02, rely=.22, relh=.25 , relw=.22))

        self.month = Radiobutton(self, text='Month', variable=self.season, value='month', place=dict(relx=.25, rely=.22, relh=.25 , relw=.22))

        self.week = Radiobutton(self, text='Week', variable=self.season, value='week', place=dict(relx=.48, rely=.22, relh=.25 , relw=.24))

        self.day = Radiobutton(self, text='Day', variable=self.season, value='day', place=dict(relx=.73, rely=.22, relh=.25 , relw=.24))

        self.setRadioGroups([self.day, self.week, self.month, self.year])

        
        self.seasonNames = tk.StringVar()
        self.seasonNames.set('sub')

        self.dayName = RadioCombo(self, topKwargs=dict(config=dict(text='Day Name', style='Group.TRadiobutton', variable=self.seasonNames, value='dayName')), orient='h', place=dict(relx=.02, rely=.48, relh=.25 , relw=.45), bottomKwargs=dict(values=DAYS_NAMES), tttk=1)

        self.weekNumber = RadioCombo(self, topKwargs=dict(config=dict(text='Week Number', style='Group.TRadiobutton', variable=self.seasonNames, value='weekNumber')), orient='h', place=dict(relx=.02, rely=.75, relh=.25 , relw=.45), longent=.65, bottomKwargs=dict(values=list(range(1, 6)), _type='number'), tttk=1)


        self.monthName = RadioCombo(self, topKwargs=dict(config=dict(text='Month Name', style='Group.TRadiobutton', variable=self.seasonNames, value='monthName')), orient='h', place=dict(relx=.49, rely=.48, relh=.25 , relw=.48), bottomKwargs=dict(values=MONTHS_NAMES[1:]), tttk=1)

        self.yearNumber = RadioCombo(self, topKwargs=dict(config=dict(text='Year Number', style='Group.TRadiobutton', variable=self.seasonNames, value='yearNumber')), orient='h', place=dict(relx=.49, rely=.75, relh=.25 , relw=.48), bottomKwargs=dict(values=list(range(2017, DateTime.now().year + 1)), _type='number'), tttk=1)

        self.setRadioGroups([self.dayName, self.weekNumber, self.monthName, self.yearNumber])


class SearchDetails(Notebook):
    def __init__(self, master, sup=None, results=None, **kwargs):
        super().__init__(master, **kwargs)

        self._sup = sup
        self.results = results
        
        self.personalDetails = SearchPersonalDetails(self, text='Personal Details')
        self.add(self.personalDetails, padding=3)
        self.tab(0, text='Regions', compound='left', underline='-1')
        self.recordDetails = SearchRecordDetails(self, text='Record Details')
        self.add(self.recordDetails, padding=3)
        self.tab(1, text='Records', compound='left', underline='-1')

        self.dateSearch = DateSearch(self, text='Record Details')
        
        self.add(self.dateSearch, padding=3)
        self.tab(2, text='Date', compound='left', underline='-1')


class SubsList(LabelFrame):
    def __init__(self, master, listboxConfig={}, callback=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.callback = callback
        self.listbox = ListBox(self, text='Subs', place=dict(relx=0, rely=0, relh=.865, relw=1), callback=self.clicked, listboxConfig=listboxConfig)

        self.total = LabelLabel(self, place=dict(relx=0, rely=.87, relh=.12, relw=.5), topKwargs=dict(text='Total Subs'), orient='h', bottomKwargs=dict(font='DEFAULT_FONT'), longent=.6)

        self.dialog = Checkbutton(self, place=dict(relx=.74, rely=.88, relh=.1, relw=.25), text='Dialog?')

        self.listbox.bind('<Double-1>', self.clicked)

    def set(self, values):
        self.listbox.set(values)
        self.total.set(self.listbox.last)
    
    def clicked(self, selected=None, event=None):
        selected = selected[0]
        if self.dialog.get(): print(self.dialog.get())
        elif self.callback: self.callback(selected)



class RegionDetails(FillWidgets, LabelFrame):
    def __init__(self, master, region=None, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)
        FillWidgets.__init__(self)

        self.region = region

        self.office = LabelLabel(self, topKwargs=dict(text='Office'), place=dict(relx=.02, rely=0, relh=.23, relw=.96), orient='h', longent=.3, bottomKwargs=dict(font='DEFAULT_FONT'))
        self.department = LabelLabel(self, topKwargs=dict(text='Department'), place=dict(relx=.02, rely=.24, relh=.23, relw=.96), orient='h', longent=.3)
        self.sup = LabelLabel(self, topKwargs=dict(text='Superscript'), place=dict(relx=.02, rely=.48, relh=.23, relw=.96), orient='h', longent=.3)
        self.sub = LabelLabel(self, topKwargs=dict(text='Subscript'), place=dict(relx=.02, rely=.72, relh=.23, relw=.96), orient='h', longent=.3)

        self.addResultsWidgets(['office', 'department', 'sup', 'sub'])

        self.set(region)
    
    def set(self, region):
        vs = ['office', 'department', 'sup', 'sub']
        values = {}

        hie = region.hie[1:]
        ln = len(hie)
        co = 0

        for h in hie:
            if isinstance(h, AGAM):
                co += 1
                continue
            ind = hie.index(h)
            key = vs[ind-co]
            values[key] = h.name
        
        super().set(values)


class FurtherDetails(FillWidgets, LabelFrame):
    def __init__(self, master, text='Details', region=None, **kwargs):
        LabelFrame.__init__(self, master, text=text, **kwargs)

        self.region = region
        FillWidgets.__init__(self)
        
        self.persons = LabelLabel(self, topKwargs=dict(config=dict(text='Persons')), place=dict(relx=.02, rely=0, relh=.22, relw=.4), orient='h', longent=.5)

        self.subs = LabelLabel(self, topKwargs=dict(config=dict(text='Total Subs', anchor='center')), place=dict(relx=.02, rely=.24, relh=.22, relw=.4), orient='h', longent=.55)

        self.accounts = LabelLabel(self, topKwargs=dict(config=dict(text='Total Accounts', anchor='center')), place=dict(relx=.02, rely=.46, relh=.22, relw=.4), orient='h', longent=.65)

        self.actSubs = LabelLabel(self, topKwargs=dict(config=dict(text='Active Subs', anchor='center')), place=dict(relx=.02, rely=.68, relh=.22, relw=.4), orient='h')

        self.actSubsAccs = LabelLabel(self, topKwargs=dict(config=dict(text='Active Subs Accounts', anchor='center')), place=dict(relx=.48, rely=0, relh=.22, relw=.5), orient='h', longent=.7)

        Button(self, place=dict(relx=.73, rely=.44, relh=.22, relw=.25), text='Object Details', command=self.openObjDet)

        Button(self, place=dict(relx=.73, rely=.68, relh=.22, relw=.25), text='Sort and Search', command=self.openSNS)

        self.sns = None
        self.objdet = None

        from .agam_apps import SortNSearch, ObjectDetails

        self.SNS = SortNSearch
        self.OBJDET = ObjectDetails

        self.addResultsWidgets(['persons', 'subs', 'actSubs', 'accounts', 'actSubsAccs'])

        self.set()
    
    def set(self):
        if self.region and not isinstance(self.region, Client):
            values = dict(
                persons=len(self.region.personsManager or []),
                subs=len(self.region.subRegionsManager),
                actSubs=len(self.region.subRegionsManager.sortSubsByMonth(DateTime.now())),
                accounts=len(self.region.accountsManager),
                actSubsAccs=self.region.lastAccount.ledgerNumbers
            )

            super().set(values)
    
    def openSNS(self):
        if self.sns: self.sns.destroy()
        self.sns = self.SNS(self, sup=self.region)
        self.sns.mainloop()
    
    def openObjDet(self):
        if self.objdet:
            self.objdet.destroy()
        self.objdet = self.OBJDET(self, sup=self.region)
        self.objdet.mainloop()














