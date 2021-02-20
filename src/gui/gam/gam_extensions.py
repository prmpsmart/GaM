from prmp_gui.extensions import *
from prmp_gui.two_widgets import *
from prmp_gui.dialogs import *
from prmp_miscs.prmp_datetime import MONTHS_NAMES, DAYS_NAMES, PRMP_DateTime
from ...backend.gam.gam import GaM
from ...backend.dc.dc_regions import *


from ...backend.core.records_managers import *
from ...backend.dc.dc_accounts import *
from ...backend.dc.dc_specials import *
from ...backend.office.office_regions import *


def openCores(master=None, obj=None, create=0, edit=0, **kwargs):

    from ..dc.dc_apps import ThriftDialog, ThriftDetailsDialog, DailyContributionDailog, DC_RegionHome, DC_AccountHome, PersonDialog, RecordDialog, AccountDialog, DailyContributionDailog, ClientAccountDialog, ClientAccount

    from .gam_apps import RegionHome, AccountHome, ManagerHome

    _kwargs = kwargs.copy()
    kwargs = _kwargs

    non = 0

    if obj:
        window = ManagerHome
        try:
            if not kwargs.get('title'): kwargs.update(dict(title=obj.name))
        except: pass

        if create: kwargs.update(dict(manager=obj))

        if isinstance(obj, DCRegion): #Office is there for the mean time.
            window = DC_RegionHome
            if not create: kwargs.update(region=obj)

        elif isinstance(obj, DCAccount):
            if edit:
                if isinstance(obj, ClientAccount): window = ClientAccountDialog
                else: window = AccountDialog
            else: window = DC_AccountHome
            if not create: kwargs.update(account=obj)
        elif isinstance(obj, Record):
            window = RecordDialog
            if not create: kwargs.update(title=obj.name, record=obj)
        elif isinstance(obj, Person):
            window = PersonDialog
            if not create: kwargs.update(person=obj)
        elif isinstance(obj, Thrift):
            if not create:
                window = ThriftDetailsDialog if not edit else ThriftDialog
                kwargs.update(title=obj.name, thrift=obj)
            else: window = ThriftDialog
        elif isinstance(obj, DailyContribution):
            # print('true')
            if not create:
                window = DailyContributionDailog
                kwargs.update(title=obj.name, dcContrib=obj)
            else: window = ThriftDialog
        elif isinstance(obj, ObjectsManager):
            if not create: kwargs.update(title=f'{obj.name} Subscripts Details', obj=obj)
        else:
            kwargs.update(obj=obj)
            non = 1

        if non == 0:
            # print(kwargs)
            win = window(master, **kwargs)
            # if not master: win.start()
        else: dialogFunc(master=master, **kwargs)



class TreeColumns:
    @staticmethod
    def columns(sup):
        if isinstance(sup, (RecordsManager, Account)): return [{'text': 'Type', 'attr': 'className', 'width': 150}, {'text': 'Date', 'attr': {'date': 'date'}}, {'text': 'Money', 'type': float}, {'text': 'Note', 'width': 200}]

        elif isinstance(sup, (DailyContributionsManager)): return [{'text': 'Type', 'attr': 'className', 'width': 150}, {'text': 'Date', 'attr': {'date': 'date'}}, {'text': 'Money', 'type': float}, {'text': 'Note', 'width': 200}]

        elif isinstance(sup, (DailyContribution)): return [{'text': 'S/N', 'attr': 'number', 'width': 1}, {'text': 'Month', 'attr': [{'month': 'monthYear'}, 'name'], 'width': 80}, {'text': 'Name', 'attr': 'regionName', 'width': 100}, {'text': 'Ledger No.', 'attr': 'ledgerNumber'}, 'Rate', {'text': 'Thrift', 'attr': 'contributed'}, 'Income', 'Transfer', 'Paidout', {'text': 'Upfront R.', 'attr': 'upfrontRepay'}, 'Saved', {'text': 'Total', 'attr': 'newContributions', 'type': float}]

        return [{'text': 'Name', 'width': 250}, {'text': 'Date', 'attr': {'date': 'date'}}, {'text': 'Last Active', 'attr': {'last': {'date': 'date'}}}]



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


class GaM_Hierachy(Hierachy):


    @property
    def openDialog(self): return openCores

    def getSubs(self, obj, item=''):
        subs = []

        if isinstance(obj, Region): subs = [obj.subRegions, obj.accounts, obj.persons] + [obj['dailyContributions']] or []
        elif isinstance(obj, Record):
            for a in obj:
                item_ = self.insert(item, text=a.name, value=a)
            return
        elif isinstance(obj, ObjectsMixins): subs = obj.subs

        return subs

GH = GaM_Hierachy

class HierachyNColumnsExplorer(Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        binds = [('<Control-C>', self.openColumnExplorer, ''), ('<Control-c>', self.openColumnExplorer, '')]
        self.tree = GaM_Hierachy(self, place=dict(relx=0, rely=0, relw=1, relh=.93), binds=binds)

        self.columns = self.tree.columns
        self.setColumns = self.tree.setColumns
        self.viewObjs = self.tree.viewObjs
        # self.tw = self.tree.tw
        # self.tw = self.tree.tw
        # self.tw = self.tree.tw

        Button(self, text='Columns Explorer', place=dict(relx=.1, rely=.935, relw=.2, relh=.06), command=self.openColumnExplorer)

    def openColumnExplorer(self, e=0): ColumnsExplorerDialog(self, columns=self.columns, callback=self.setColumns)



class UniqueID(Button):
    def __init__(self, master=None, text='Unique ID', obj=None, **kwargs):
        super().__init__(master=master, text=text, command=self.popUp, **kwargs)

        self.obj = obj
        self.view = None

    def popUp(self):
        if self.view: self.view.destroy()


        self.view = PRMP_Toplevel(self, geo=(450, 80), tm=1, tw=1, grab=1, atb=0, asb=0, ntb=1, gaw=1)
        date = uniqueID = ''
        if self.obj:
            date = self.obj.date.date
            uniqueID = self.obj.uniqueID
            self.view.setTitle(self.obj.name)

        LabelEntry(self.view.container, topKwargs=dict(text='Unique ID'), place=dict(relx=.02, rely=.02, relh=.96, relw=.96), bottomKwargs=dict(state='readonly')).set(uniqueID)

        self.view.paint()

    def set(self, obj): self.obj = obj


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
        self.note = Text(self, wrap='word', place=dict(relx=.24, rely=.54, relh=.42, relw=.74), required=True)


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

        self.yearNumber = RadioCombo(self, topKwargs=dict(config=dict(text='Year Number', style='Group.TRadiobutton', variable=self.seasonNames, value='yearNumber')), orient='h', place=dict(relx=.49, rely=.75, relh=.25 , relw=.48), bottomKwargs=dict(values=list(range(2017, PRMP_DateTime.now().year + 1)), _type='number'), tttk=1)

        self.setRadioGroups([self.dayName, self.weekNumber, self.monthName, self.yearNumber])


class SearchDetails(Notebook):
    def __init__(self, master, obj=None, results=None, **kwargs):
        super().__init__(master, **kwargs)

        self.obj = obj
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


class SortDetails(Notebook):
    def __init__(self, master, sup=None, results=None, **kwargs):
        super().__init__(master, **kwargs)

        self._sup = sup
        self.results = results


class SubsList(LabelFrame):
    def __init__(self, master, listboxConfig={}, callback=None, totalConfig=dict(text='Total'), values=[], valuesKwargs={}, **kwargs):
        super().__init__(master, **kwargs)

        self.callback = callback

        self.total = LabelLabel(self, place=dict(relx=0, rely=0, relh=.13, relw=.35), topKwargs=totalConfig, orient='h', bottomKwargs=dict(font='DEFAULT_FONT'), longent=.6)

        Button(self, place=dict(relx=.4, rely=0, relh=.1, relw=.25), text='Reload', command=self.reload)

        self.dialog = Checkbutton(self, place=dict(relx=.68, rely=0, relh=.1, relw=.3), text='Dialog?')

        self.listbox = ListBox(self, text='Subs', place=dict(relx=0, rely=.135, relh=.865, relw=1), callback=self.clicked, listboxConfig=listboxConfig)

        self.listbox.bind('<Double-1>', self.clicked)

        self.values = values
        self.valuesKwargs = valuesKwargs
        if values: self.set(values, **valuesKwargs)

    def reload(self): self.set(self.values, **self.valuesKwargs)

    def set(self, values, **kwargs):
        if not values: return

        self.values = values
        self.valuesKwargs = kwargs

        self.listbox.set(values, **kwargs)
        self.total.set(self.listbox.last)

    def clicked(self, selected=None, event=None):
        selected = selected[0]
        if self.dialog.get(): openCores(self, selected)
        elif self.callback: self.callback(selected)


class RegionDetails(PRMP_FillWidgets, LabelFrame):
    def __init__(self, master, region=None, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self)

        self.region = region

        self.office = LabelLabel(self, topKwargs=dict(text='Office'), place=dict(relx=.02, rely=0, relh=.23, relw=.96), orient='h', longent=.3, bottomKwargs=dict(font='DEFAULT_FONT'))
        self.department = LabelLabel(self, topKwargs=dict(text='Department'), place=dict(relx=.02, rely=.24, relh=.23, relw=.96), orient='h', longent=.3)
        self.sup = LabelLabel(self, topKwargs=dict(text='Superscript'), place=dict(relx=.02, rely=.48, relh=.23, relw=.96), orient='h', longent=.3)
        self.sub = LabelLabel(self, topKwargs=dict(text='Subscript'), place=dict(relx=.02, rely=.72, relh=.23, relw=.96), orient='h', longent=.3)

        self.addResultsWidgets(['office', 'department', 'sup', 'sub'])

        self.set(region)

    def set(self, region):
        if not region: return
        vs = ['office', 'department', 'sup', 'sub']
        values = {}

        hie = region.hie
        ln = len(hie)
        co = 0

        for h in hie:
            if isinstance(h, GaM):
                co += 1
                continue
            ind = hie.index(h)
            key = vs[ind-co]
            values[key] = h.name
        # print(values)
        super().set(values)


class FurtherDetails(PRMP_FillWidgets, LabelFrame):
    def __init__(self, master, text='Details', region=None, **kwargs):
        LabelFrame.__init__(self, master, text=text, **kwargs)

        self.region = region
        PRMP_FillWidgets.__init__(self)

        self.persons = LabelLabel(self, topKwargs=dict(config=dict(text='Persons')), place=dict(relx=.02, rely=0, relh=.22, relw=.4), orient='h', longent=.5)

        self.subs = LabelLabel(self, topKwargs=dict(config=dict(text='Total Subs', anchor='center')), place=dict(relx=.02, rely=.24, relh=.22, relw=.4), orient='h', longent=.55)

        self.accounts = LabelLabel(self, topKwargs=dict(config=dict(text='Total Accounts', anchor='center')), place=dict(relx=.02, rely=.46, relh=.22, relw=.4), orient='h', longent=.65)

        self.actSubs = LabelLabel(self, topKwargs=dict(config=dict(text='Active Subs', anchor='center')), place=dict(relx=.02, rely=.68, relh=.22, relw=.4), orient='h')

        self.actSubsAccs = LabelLabel(self, topKwargs=dict(config=dict(text='Active Subs Accounts', anchor='center')), place=dict(relx=.48, rely=0, relh=.22, relw=.5), orient='h', longent=.7)

        Button(self, place=dict(relx=.7, rely=.44, relh=.22, relw=.28), text='Object Details', command=self.openObjDet)

        Button(self, place=dict(relx=.7, rely=.68, relh=.22, relw=.28), text='Sort and Search', command=self.openSNS)

        self.sns = None
        self.objdet = None

        from .gam_apps import SortNSearch, ManagerHome

        self.SNS = SortNSearch
        self.MAN = ManagerHome

        self.addResultsWidgets(['persons', 'subs', 'actSubs', 'accounts', 'actSubsAccs'])

        self.set()

    def set(self):
        if self.region:
            values = dict(
                    persons=len(self.region.persons or []),
                    subs=len(self.region.subRegions or []),
                    accounts=len(self.region.accounts or [])
                    )
            if not isinstance(self.region, Client):
                self.actSubsAccs.T.config(text='Active Subs Accounts')
                values.update(dict(
                    actSubs=len(self.region.subRegionsManager.sortSubsByMonth(PRMP_DateTime.now())),
                    actSubsAccs=self.region.lastAccount.get('ledgerNumbers', 0)
                    ))
            else:
                self.actSubsAccs.T.config(text='Active Accounts')
                values.update(dict(
                    actSubsAccs=len(self.region.accounts.sortSubsByDate(PRMP_DateTime.now()))
                ))

            if values: super().set(values)

    def openSNS(self):
        if self.sns: self.sns.destroy()
        self.sns = self.SNS(self, sup=self.region)
        self.sns.mainloop()

    def openObjDet(self):
        if self.objdet:
            self.objdet.destroy()
        self.objdet = self.MAN(self, sup=self.region)
        self.objdet.mainloop()









