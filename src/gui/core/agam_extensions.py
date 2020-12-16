from .prmp_gui.extensions import *
from .agam_dialogs import *

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


class PersonalDetails(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        Label(self, text='Name', place=dict(relx=.02, rely=0, relh=.15, relw=.25))
        self.name = Entry(self, place=dict(relx=.3, rely=0, relh=.15, relw=.68))

        Label(self, text='Number', place=dict(relx=.02, rely=.16, relh=.15, relw=.25))
        self.number = Entry(self, place=dict(relx=.3, rely=.16, relh=.15, relw=.68))

        Label(self, text='Phone', place=dict(relx=.02, rely=.32, relh=.15, relw=.25))
        self.phone = Entry(self, place=dict(relx=.3, rely=.32, relh=.15, relw=.68))

        Label(self, text='ID', place=dict(relx=.02, rely=.48, relh=.15, relw=.25))
        self.id = Entry(self, place=dict(relx=.3, rely=.48, relh=.15, relw=.68))

        Label(self, text='Gender', place=dict(relx=.02, rely=.64, relh=.15, relw=.25))
        self.gender = Combobox(self, type_='gender', place=dict(relx=.3, rely=.64, relh=.15 , relw=.68))

        Label(self, text='Address', place=dict(relx=.02, rely=.8, relh=.15, relw=.25))
        self.address = Entry(self, place=dict(relx=.3, rely=.8, relh=.15, relw=.68))


class RecordDetails(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        Label(self, text='Date', place=dict(relx=.02, rely=0, relh=.25, relw=.2))
        self.date = Button(self, text='06/12/2020', place=dict(relx=.24, rely=0, relh=.25, relw=.25))

        Label(self, text='Range', place=dict(relx=.02, rely=.27, relh=.25, relw=.2))

        self.range1 = Entry(self, place=dict(relx=.24, rely=.27, relh=.25, relw=.25))

        Label(self, text='- to -', relief='flat', place=dict(relx=.51, rely=.27, relh=.25, relw=.2))

        self.range2 = Entry(self, place=dict(relx=.73, rely=.27, relh=.25, relw=.25))

        Label(self, text='Note', place=dict(relx=.02, rely=.54, relh=.25, relw=.2 ))
        self.note = Text(self, wrap='word', place=dict(relx=.24, rely=.54, relh=.42, relw=.74), very=True)


class DateSearch(LabelFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.date = Button(self, text='06/12/2020', place=dict(relx=.02, rely=0, relh=.2, relw=.3))

        self.season = tk.StringVar()
        self.season.set('sub')

        self.year = Radiobutton(self, text='Year', variable=self.season, value='year', place=dict(relx=.02, rely=.22, relh=.25 , relw=.22))

        self.month = Radiobutton(self, text='Month', variable=self.season, value='month', place=dict(relx=.25, rely=.22, relh=.25 , relw=.22))

        self.week = Radiobutton(self, text='Week', variable=self.season, value='week', place=dict(relx=.48, rely=.22, relh=.25 , relw=.24))

        self.day = Radiobutton(self, text='Day', variable=self.season, value='day', place=dict(relx=.73, rely=.22, relh=.25 , relw=.24))

        self.setRadioGroups([self.day, self.week, self.month, self.year])

        
        self.seasonNames = tk.StringVar()
        self.seasonNames.set('sub')

        self.dayName = RadioEntry(self, topKwargs=dict(config=dict(text='Day Name', style='Group.TRadiobutton', variable=self.seasonNames, value='dayName')), orient='h', place=dict(relx=.02, rely=.48, relh=.25 , relw=.45))


        self.monthName = RadioEntry(self, topKwargs=dict(config=dict(text='Month Name', style='Group.TRadiobutton', variable=self.seasonNames, value='monthName')), orient='h', place=dict(relx=.5, rely=.48, relh=.25 , relw=.45))

        self.weekNumber = RadioEntry(self, topKwargs=dict(config=dict(text='Week Number', style='Group.TRadiobutton', variable=self.seasonNames, value='weekNumber')), orient='h', place=dict(relx=.02, rely=.75, relh=.25 , relw=.45))

        self.yearNumber = RadioEntry(self, topKwargs=dict(config=dict(text='Year Number', style='Group.TRadiobutton', variable=self.seasonNames, value='yearNumber')), orient='h', place=dict(relx=.5, rely=.75, relh=.25 , relw=.456))

        self.setRadioGroups([self.dayName, self.weekNumber, self.monthName, self.yearNumber])


class Details(Notebook):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        
        self.personalDetails = PersonalDetails(self, text='Personal Details', place=dict(relx=.022, rely=.032, relh=.328 , relw=.25))
        self.add(self.personalDetails, padding=3)
        self.tab(0, text='Records', compound='left', underline='-1')

        self.recordDetails = RecordDetails(self, text='Record Details', place=dict(relx=.005, rely=.005, relh=.4 , relw=.35))
        self.add(self.recordDetails, padding=3)
        self.tab(1, text='Regions', compound='left', underline='-1')

