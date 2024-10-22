from .gam_dialogs import *
from ...backend.core.bases import ObjectsManager
from ...backend.dc.dc_specials import *


class GaM_App(PRMP_MainWindow):

    _save = GaM_Settings.saveAll
    _save = GaM_Settings.threadSave
    _load = GaM_Settings.threadLoad

    def __init__(self, master=None, title='Goodness and Mercy', obj=None, **kwargs):
        super().__init__(master, title=title, **kwargs)
        self.obj = obj

        self.root.save = self.save
        self._setupApp()

        self.defaults()
        self.setMenus()

        self.start()

    def saveIt(self):
        from .auths_gui import make_change
        make_change(self._save, silent=1)
        PRMP_MsgBox(self, title='Successful', message='Saving is successful.')

    def save(self, u=0):
        if u: self.saveIt()
        else: self._save()

    def load(self): self._load()

    def _setupApp(self):
        pass

    def defaults(self):
        pass

    def setMenus(self):
        if not self.titleBar: return

        def showSnS(obj):
            if obj: SortNSearch(self, obj=self.obj)

        def showAM(obj):
            if obj: ManagerHome(self, obj=self.obj, title=f'{self.obj.name} Details.')

        def updateObj(obj):
            if isinstance(obj, Account): obj.balanceAccount()

        def editObj(obj): openCores(obj=self.obj, edit=True)

        def security(): from .auths_gui import Security; Security()

        self.viewMenu = None
        self.settingsMenu = None

        self.viewMenu = Menu(self, config=dict(tearoff=0))
        view = [
            dict(label='Search', 
                command=lambda : showSnS(self.obj)
                ), 
            dict(label='As Manager', 
                command=lambda : showAM(self.obj)
                ), 
            dict(label='Update Current Object', 
                command=lambda : updateObj(self.obj)
                ),
            dict(label='Edit Current Object',
                command=lambda : editObj(self.obj)
                )
            ]

        for vie in view: self.viewMenu.add_command(**vie)

        self.settingsMenu = Menu(self, config=dict(tearoff=0))
        settings = [
            dict(label='Load', 
                command=self.load
                ), 
            dict(label='Save', 
                command=self.save
                ), 
            dict(label='Security', 
                command=security
                ), 
            dict(label='Others')
        ]

        for sett in settings: self.settingsMenu.add_command(**sett)

        self.helpMenu = Menu(self, config=dict(tearoff=0))
        help_ = [
            dict(label='Welcome'), 
            dict(label='Documentation'), 
            dict(label='Keyboard Shortcuts Reference'), 
            dict(label='About')
        ]
        
        for hel in help_: self.helpMenu.add_command(**hel)

        Menubutton(self.menuBar, config=dict(menu=self.viewMenu, text="View", style='Window.TMenubutton'), place=dict(relx=.005, rely=.05, relw=.045, relh=.9), font='PRMP_FONT', relief='flat')
        Menubutton(self.menuBar, config=dict(menu=self.settingsMenu, text="Settings", style='Window.TMenubutton'), place=dict(relx=.05, rely=.05, relw=.065, relh=.9), font='PRMP_FONT', relief='flat')
        Menubutton(self.menuBar, config=dict(menu=self.helpMenu, text="Help", style='Window.TMenubutton'), place=dict(relx=.115, rely=.05, relw=.045, relh=.9), font='PRMP_FONT', relief='flat')


class RegionLookUp(GaM_App, PRMP_FillWidgets):

    def __init__(self, master=None, title='Region Details', geo=(650, 270), expandGeo=(800, 600), values={}, region=None, tm=1, gaw=1, **kwargs):

        self.region = region
        self.personDialog = None
        self.switchState = None
        self._sub = None
        self.geo_ = geo
        self.expandGeo = expandGeo

        GaM_App.__init__(self, master, title=title, geo=geo, gaw=gaw, ntb=1, tm=tm, atb=1, asb=1, **kwargs)

        PRMP_FillWidgets.__init__(self, values=values)


        self._setupApp()

        self.set()
        self.paint()

    def regionChanged(self, region):
        region = region[1]
        if not region or (region is self.region): return

        self.region = region
        self.setTitle(region.idText)

        person = region.person
        if person: self.set(dict(image=person.image))

        self.loadAccounts(region)

    def _setupApp(self):
        # hierachy

        self.hierachy = PRMP_LabelFrame(self.container, config=dict(text='Hierachy'))
        self.hierachy.place(x=2, y=2, h=170, relw=.6)

        self.hierachyVar = tk.StringVar()
        self.hierachyVar.set('sub')

        self.office = RegionRadioCombo(self.hierachy,  topKwargs=dict(config=dict(text='Office', style='Group.TRadiobutton', variable=self.hierachyVar, value='off')), bottomKwargs=dict(placeholder='Enter Office Name'), orient='h', place=dict(relx=.02, rely=0, relh=.25, relw=.96), longent=.3, regionLevel=1, recievers=[self.regionChanged], dot=1, tttk=1)

        self.department = RegionRadioCombo(self.hierachy,  topKwargs=dict(config=dict(text='Department', style='Group.TRadiobutton', variable=self.hierachyVar, value='dep')), orient='h', place=dict(relx=.02, rely=.25, relh=.25, relw=.96), longent=.35, regionLevel=2, recievers=[self.regionChanged], dot=1, tttk=1)
        self.office.addReceiver(self.department.receiver)

        self.sup = RegionRadioCombo(self.hierachy,  topKwargs=dict(config=dict(text='Superscript', style='Group.TRadiobutton', variable=self.hierachyVar, value='sup')), orient='h', place=dict(relx=.02, rely=.5, relh=.25, relw=.96), longent=.35, regionLevel=3, recievers=[self.regionChanged], dot=1, tttk=1)
        self.department.addReceiver(self.sup.receiver)

        self.sub = RegionRadioCombo(self.hierachy,  topKwargs=dict(config=dict(text='Subscript', value='sub', style='Group.TRadiobutton', variable= self.hierachyVar)), orient='h', place=dict(relx=.02, rely=.75, relh=.25, relw=.96), longent=.3, regionLevel=4, recievers=[self.regionChanged], dot=1, tttk=1)
        self.sup.addReceiver(self.sub.receiver)

        # workers in the region or the individual
        persons = PRMP_Button(self.container, config=dict(text='Persons', command=self.showPersons))
        persons.place(x=2, y=175, h=24, w=80)

        switch = PRMP_Button(self.container, config=dict(text='Switch?', command=self.switch))
        switch.place(x=100, y=175, h=24, w=90)

        new = PRMP_Checkbutton(self.container, config=dict(text='New Dialog ?'))
        new.place(x=208, y=175, h=24, w=140)


        self.image = PRMP_ImageLabel(self.container, status='Profile Picture')
        self.image.place(relx=.61, y=10, h=170, relw=.382)



       # accounts
        self.accounts = PRMP_LabelFrame(self.container, config=dict(text='Accounts'))
        self.accountsHie = Hierachy(self.accounts, status='Accounts Details')
        self.accounts.sub = self.placeAccounts

       # subregions
        self.subRegions = PRMP_LabelFrame(self.container, config=dict(text='Sub Regions'))
        self.subRegionsHie = Hierachy(self.subRegions, status='Sub Regions Details')
        self.subRegions.sub = self.placeSubRegions


        self.addResultsWidgets(['office', 'department', 'sup', 'image', 'sub'])

        self.setRadioGroups([self.office, self.department, self.sub, self.sup])


        if self.region:
            for wid in [self.office, self.department, self.sub, self.sup]:
                if self.region.level == wid.regionLevel: wid.set(self.region)


    def showPersons(self, e=0):
        if self.personDialog: self.personDialog.destroy()
        if self.region:
            if self.region.level == 5:
                self.personDialog = PersonDialog(self,  values=self.region.person.values, side=self.side)
            else: print('Level not upto')

    def loadAccounts(self, region):
        if region:
            acc = region.accountsManager
            headers = [{'text': 'Name', 'width': 120}, 'Date', *[{'type': int, 'text': a} for a in acc.headers]]
            self.accountsHie.setColumns(headers)
            self.accountsHie.set(acc, 1)

    def switch(self):
        # to switch between subregions and accounts
        val = self.hierachyVar.get()
        if val == '0':
            PRMP_MsgBox(self, title='Choose First!', message='Choose a region first.', side=self.side)
            return
        if self.switchState == None:
            if val != self.sub.val:
                self.showSubRegionsContainer()
                self.switchState = True
            else:
                self.showAccountsContainer()
                self.switchState = False

        elif self.switchState == True:
            self.showAccountsContainer()
            self.switchState = False

        elif self.switchState == False:
            self.unExpand()
            self.switchState = None

    def loadRegion(self, region=None, account=1):
        if region:
            self.region = region
            self.titleBar.config(text=f'{self.region} Details Dialog')

    def unExpand(self):
        self.accounts.place_forget()
        self.changeGeometry(self.geo_)

    def isMaximized(self):
        self.update()
        if self._sub: self._sub.sub()

    isNormal = isMaximized

    def expand(self):
        self.resize = (1, 1)
        self.changeGeometry(self.expandGeo)
        self.update()

    def placeSubs(self, sub=None):
        if sub: self._sub = sub
        if self._sub:
            self._sub.place_forget()
            w, h = self._sub.master.tupled_winfo_geometry[:2]
            h -= 205
            self._sub.place(x=2, y=203, h=h, w=w-8)

    def showSubRegionsContainer(self):
        self.expand()
        self.placeSubRegions()

    def showAccountsContainer(self):
        self.subRegions.place_forget()
        self.expand()
        self.placeAccounts()

    def placeAccounts(self):
        self.placeSubs(self.accounts)
        self.accounts.update()
        hx, hy = self.accounts.tupled_winfo_geometry[:2]
        self.accountsHie.place(x=2, y=0, w=hx-8, h=hy-30)

    def placeSubRegions(self):
        self.placeSubs(self.subRegions)
        self.subRegions.update()

        hx, hy = self.subRegions.tupled_winfo_geometry[:2]
        self.subRegionsHie.place(x=2, y=0, w=hx-8, h=hy-24)
RLU = RegionLookUp


class SortNSearch(GaM_App):
    def __init__(self, master=None, title='Sort and Search', geo=(700, 850), longent=.31, **kwargs):
        self.longent = longent
        super().__init__(master, title=title, geo=geo, tw=1, **kwargs)

    def _setupApp(self):
        self.sup = LabelButton(self.container, place=dict(relx=.005, rely=.005, relh=.04, relw=.99), orient='h', longent=.2, topKwargs=dict(text='Sup'), bottomKwargs=dict(text=self.obj.name if self.obj else ''), command=self.openSup)

        self.results = PRMP_TreeView(LabelFrame(self.container, text='Results', place=dict(relx=.005, rely=self.longent+.05, relh=.99-.04-self.longent, relw=.99)), place=dict(relx=0, rely=0, relh=1 , relw=1))

        note = Notebook(self.container, place=dict(relx=.005, rely=.05, relh=self.longent, relw=.99))

        self.search = SearchDetails(note, results=self.results, obj=self.obj)
        note.add(self.search, padding=3)
        note.tab(0, text='Search', compound='left', underline='-1')

        self.sort = SortDetails(note)
        note.add(self.sort, padding=3)
        note.tab(1, text='Sort', compound='left', underline='-1')

        self.paint()

    def openSup(self):
        pass


class ObjectHome(GaM_App):

    def __init__(self, master=None, geo=(1500, 800), title='Home', obj=None, **kwargs):
        self.sns = None
        self.objdet = None

        super().__init__(master, geo=geo, title=title, obj=obj, **kwargs)

    def _setupApp(self):
        obj = self.obj


        self.detailsNote = Notebook(self.container, place=dict(relx=.005, rely=.005, relh=.932, relw=.24))

        self.frame1 = Frame(self.detailsNote)
        self.detailsNote.add(self.frame1, padding=3)
        self.detailsNote.tab(0, text='Details', compound='left', underline='-1')

        self.date = LabelLabel(self.container, place=dict(relx=.005, rely=.94, relh=.05, relw=.15), orient='h', topKwargs=dict(text='Date'), bottomKwargs=dict(text=obj.date.date if obj else ''))

        UniqueID(self.container, place=dict(relx=.17, rely=.94, relh=.045, relw=.07), obj=obj)

        self.note = Notebook(self.container, place=dict(relx=.25, rely=.005, relh=.99, relw=.745))

    def openSNS(self):
        if self.sns: self.sns.destroy()
        self.sns = SortNSearch(self, sup=self.obj)
        self.sns.mainloop()

    def openObjDet(self):
        if self.objdet:
            self.objdet.destroy()
        self.objdet = ManagerHome(self, obj=self.obj)
        self.objdet.mainloop()


class RegionHome(ObjectHome):

    def __init__(self, master=None, title='Region Home', region=None, **kwargs):

        super().__init__(master, title=title, obj=region, **kwargs)

    def _setupApp(self):
        super()._setupApp()

        region = self.region = self.obj
        if region: self.setTitle(region.name)

        self.details = RegionDetails(self.frame1, text='Details', place=dict(relx=.005, rely=.005, relh=.27, relw=.99), region=region)

        subs = region.subRegions.subsName if region and region.subRegions else 'Subs'

        self.subRegions = SubsList(self.frame1, text=subs, place=dict(relx=.005, rely=.28, relh=.36, relw=.99))

        self.accounts = SubsList(self.frame1, text='Accounts', place=dict(relx=.005, rely=.65, relh=.34, relw=.99))

        if region:
            self.subRegions.set(region.subRegions, showAttr='name')
            self.accounts.set(region.accounts, showAttr='name')


class AccountHome(ObjectHome):

    def __init__(self, master=None, title='Account Home', account=None, **kwargs):

        super().__init__(master, title=title, obj=account, **kwargs)

    def _setupApp(self):
        super()._setupApp()

        account = self.account = self.obj
        name, self._manager = (account.manager.name, account.manager) if account != None else ('', None)

        self.manager = LabelButton(self.frame1, topKwargs=dict(text='Manager'), place=dict(relx=.005, rely=.005, relh=.14, relw=.99), bottomKwargs=dict(command=self._openManager, text=name))

        self.recordsManagers = SubsList(self.frame1, text='Records Managers', place=dict(relx=.005, rely=.16, relh=.63, relw=.99))

        if account:
            account.balanceAccount()
            self.recordsManagers.set(account, showAttr='name')

    def _openManager(self, event=None):
        if self._manager: openCores(master=self, obj=self._manager, edit=0)


class ManagerHome(TreeColumns, GaM_App):

    def __init__(self, master=None, geo=(1300, 600), title='Object Details', obj=None, **kwargs):
        super().__init__(master, geo=geo, title=title, obj=obj, **kwargs)


    def _setupApp(self):
        subTypes = []
        name = 'Name'
        if self.obj:
            name = self.obj.name
            subTypes = self.obj.subTypes
            self.setTitle(name)

        sups = LabelFrame(self.container, place=dict(relx=.005, rely=.02, relh=.965, relw=.3), text='Object Subcripts')

        self.sup = LabelButton(sups, place=dict(relx=.005, rely=0, relh=.07, relw=.99), topKwargs=dict(text='Super'), orient='h', longent=.2, command=self.openSup, bottomKwargs=dict(text=name))

        self.subType = LabelCombo(sups, place=dict(relx=.005, rely=.08, relh=.07, relw=.7), topKwargs=dict(text='Sub Type'), bottomKwargs=dict(values=subTypes), orient='h', longent=.4, func=self.changeSubs)

        self.new = Checkbutton(sups, text='New?', place=dict(relx=.77, rely=.09, relh=.05, relw=.22))

        Button(sups, text='Superscript', place=dict(relx=.009, rely=.16, relh=.07, relw=.9), font='PRMP_FONT')

        self.subsList = SubsList(sups, place=dict(relx=.038, rely=.24, relh=.73, relw=.9), text='Subs', listboxConfig=dict(selectmode='single'), callback=self.selected)

        self.subs = HierachyNColumnsExplorer(self.container, place=dict(relx=.307, rely=.039, relh=.97, relw=.68))

        self.paint()

    def getNewObjectDialog(self, st, obj=None):

        className = self.obj.className
        obj = obj or self.obj

        if isinstance(obj, ObjectsManager):
            subName = obj.objectName
            if (subName == 'Client'):
                from ..dc.dc_dialogs import ClientDialog
                return ClientDialog
            elif (subName == 'Area'):
                from ..dc.dc_dialogs import AreaDialog
                return AreaDialog
            elif (subName == 'ClientAccount'):
                from ..dc.dc_dialogs import ClientAccountDialog
                return ClientAccountDialog
            elif (subName == 'Thrift') and (st == 'Thrifts'):
                from ..dc.dc_dialogs import ThriftDialog
                return ThriftDialog
            elif (subName == 'Thrift') and (st == 'Thrifts'):
                from ..dc.dc_dialogs import ThriftDialog
                return ThriftDialog
            elif (subName == 'DailyContribution') and (st == 'Daily Contributions'):
                from ..dc.dc_dialogs import DailyContributionDailog
                return DailyContributionDailog
            elif (st == 'Records'): return RecordDialog
            elif (st == 'Persons'): return PersonDialog
            elif (st == 'Accounts'): return AccountDialog

        elif isinstance(obj, Object):
            _manager = obj[st]
            if _manager and not isinstance(_manager, list): return self.getNewObjectDialog(st, _manager)

    @property
    def selectedSubType(self): return self.subType.get()

    def getSubs(self):
        subType = self.selectedSubType
        subs = self.obj[subType] or []
        return subs

    # @property
    def c_or_m(self):
        k = ('Client', 'Member')
        g = self.obj.className in k
        h = False
        if not self.obj.strManager and not self.obj.manager.strManager: h = self.obj.region.className in k
        return g or h

    def changeSubs(self, e=0):
        st = self.selectedSubType
        if self.new.get():

            if self.c_or_m() and (st == 'Persons'): PRMP_MsgBox(self, title='Creation Error ', message=f'Only one person is valid for {self.obj.className}.', _type='error')

            else:
                try:
                    dialog = self.getNewObjectDialog(st)
                    if dialog:
                        manager = self.obj if isinstance(self.obj, ObjectsManager) else self.obj[st]
                        dialog(self, manager=manager)
                except Exception as er: PRMP_MsgBox(self, title=er.__class__.__name__, message=er, _type='error')
        else:
            try: subs = self.getSubs()
            except: return
            if subs: self.subsList.set(subs, showAttr='name')
            columns = self.columns(self.obj)
            # print(columns)
            self.subs.setColumns(columns)
            self.subs.viewObjs(self.obj)

    def openSup(self):
        pass

    def selected(self, sub):
        self.subs.setColumns(self.columns(sub))
        self.subs.viewObjs(obj=sub)


class GaM_Home(GaM_App):

    def __init__(self, title='Goodness and Mercy.', geo=(1000, 700), **kwargs):
        super().__init__(title=title, geo=geo, **kwargs)

        # self.setMenus()
        self.mainloop()


    def _setupApp(self):
        offices

        incomes
        savings
        balances
        debits
        transfers
        excesses
        deficits
        loans
        loanrepays
        interests


        dcaccounts
        coopaccounts




        pass


