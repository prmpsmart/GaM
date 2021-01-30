from .dc_dialogs import *
# from ..core.gam_dialogs import Notebook

def addNote(self):
    self.overview = DC_Overview(self.note, region=self.obj)
    self.note.add(self.overview, padding=3)
    self.note.tab(0, text='Overview', compound='left', underline='-1')

    self.tree = Hierachy(self.note)
    self.note.add(self.tree, padding=3)
    self.note.tab(1, text='Tree', compound='left', underline='-1')


class DC_RegionHome(TreeColumns, RegionHome):
    
    def __init__(self, master=None, title='Region Home', region=None, **kwargs):
        if region:
            if region.className == 'Office': region = region.dcOffice
        RegionHome.__init__(self, master, title=title, region=region, **kwargs)
    
    def _defs(self):
        self.subRegions.callback = self.selectedRegion
        self.accounts.callback = self.selectedAccount
        addNote(self)
        
        self.details.bind('<1>', lambda e: self.defaults(1))
    
    def defaults(self, i=0):
        if not i: self._defs()
        if self.region:
            self.selected(self.region)
            self.overview.updateDCDigits(self.region.lastAccount)
    
    def selectedRegion(self, sub):
        self.selected(sub)
        self.selectedAccount(sub[-1])

    def selectedAccount(self, account):
        self.selected(account)
        self.overview.updateDCDigits(account)

    def selected(self, sub):
        self.tree.setColumns(self.columns(sub))
        self.tree.viewAll(sub)


class DC_AccountHome(TreeColumns, AccountHome):
    def _setupApp(self):
        super()._setupApp()

        self.recordsManagers.callback = self.selectedRecordsManager

        addNote(self)

        if isinstance(self.account, AreaAccount):
            self.recordsManagers.place(relx=.005, rely=.13, relh=.36, relw=.24)
            self.subAccounts = SubsList(self.container, text='Clients Accounts', place=dict(relx=.005, rely=.5, relh=.36, relw=.24), callback=self.selected)
            
            if self.account: self.subAccounts.set(self.account.clientsAccounts, showAttr={'region': 'name'})

        self.selected(self.account)

    def selectedRecordsManager(self, rm): self.selected(rm, 1)

    def openManager(self):
        self.selected(self.account)

    def selected(self, sub, rm=0):
        # return
        if not rm: self.overview.updateDCDigits(sub)
        self.tree.setColumns(self.columns(sub))
        self.tree.viewAll(sub)


class DC_Office(DC_RegionHome):
    def __init__(self, master=None, region=None, **kwargs):
        if region: assert isinstance(region, DCOffice)
        super().__init__(master, region=region, **kwargs)

    @property
    def dcOffice(self): return self.region
    
    def _setupApp(self):
        cont = self.container
        note = Notebook(cont, place=dict(relx=.005, rely=.005, relh=.87, relw=.24))
        
        frame = Frame(note)
        note.add(frame, padding=3)
        note.tab(0, text='Details', compound='left', underline='-1')

        super()._setupApp(frame)

        self.details.place(relx=.005, rely=.005, relh=.27, relw=.99)
        self.subRegions.place(relx=.005, rely=.28, relh=.36, relw=.99)
        self.accounts.place(relx=.005, rely=.65, relh=.34, relw=.99)

        self.frame2 = Frame(note)
        note.add(self.frame2, padding=3)
        note.tab(1, text='Proper Details', compound='left', underline='-1')

        self.properDetails()
    
    def properDetails(self):
        ''
        pass








