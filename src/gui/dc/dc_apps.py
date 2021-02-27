from .dc_dialogs import *
# from ..gam.gam_dialogs import Notebook

def addNote(self, **kwargs):
    self.overview = DC_Overview(self.note, region=self.obj)
    self.note.add(self.overview, padding=3)
    self.note.tab(0, text='Overview', compound='left', underline='-1')

    self.table = GaM_Table(self.note)
    self.note.add(self.table, padding=3)
    self.note.tab(1, text='Hierachy', compound='left', underline='-1')

    ae = Frame(self.note)
    self.note.add(ae, padding=3)
    self.note.tab(2, text='Attributes', compound='left', underline='-1')

    self.attributes = AttributesExplorer(ae, place=dict(relx=0, rely=0, relw=1, relh=1), dialog=openCores, **kwargs)


class FillTable:

    def fillTable(self, columns=[], **kwargs):

        datas = self.obj.objectSort.fillColumns(_type=int, columns=columns, **kwargs)

        title = self.obj.objectSort.getTitle(**kwargs)

        self.table.setTitle(title)

        self.tree = self.table.hnce.tree
        self.tree.setColumns(columns)
        self.tree.clear()

        self.treeview = self.tree.treeview

        print('datas = ', datas)

        for data in datas:
            print(data)
            # self.treeview.insert('', values=data)



class DC_RegionHome(FillTable, TreeColumns, RegionHome):

    def __init__(self, master=None, title='Region Home', region=None, **kwargs):
        if region:
            if region.className == 'Office': region = region.dcOffice
        RegionHome.__init__(self, master, title=title, region=region, **kwargs)

    def _defs(self):
        self.subRegions.callback = self.selectedRegion
        self.accounts.callback = self.selectedAccount
        addNote(self, obj=self.obj)

        self.details.bind('<1>', lambda e: self.defaults(1))

    def defaults(self, i=0):
        if not i: self._defs()
        if self.region:
            self.selected(self.region)
            self.overview.updateDCDigits(self.region.lastAccount)

    def selectedRegion(self, sub):
        self.selectedAccount(sub[-1])
        self.selected(sub)

    def selectedAccount(self, account):
        self.selected(account)
        self.overview.updateDCDigits(account)

    def selected(self, sub):
        self.table.setColumns(self.columns(sub))
        self.table.viewObjs(sub)

    def _setupApp(self):
        super()._setupApp()

        self.frame2 = ProperDetails(self.detailsNote, callback=self.fillTable, obj=self.obj)
        self.detailsNote.add(self.frame2, padding=3)
        self.detailsNote.tab(1, text='Proper Details', compound='left', underline='-1')



class DC_AccountHome(FillTable, TreeColumns, AccountHome):

    def _setupApp(self):
        super()._setupApp()


        self.frame2 = ProperDetails(self.detailsNote, callback=self.fillTable, obj=self.obj)
        self.detailsNote.add(self.frame2, padding=3)
        self.detailsNote.tab(1, text='Proper Details', compound='left', underline='-1')

        self.recordsManagers.callback = self.selectedRecordsManager

        addNote(self)

        if isinstance(self.account, AreaAccount):
            self.recordsManagers.place(relx=.005, rely=.16, relh=.42, relw=.99)

            self.subAccounts = SubsList(self.frame1, text='Clients Accounts', place=dict(relx=.005, rely=.58, relh=.42, relw=.99), callback=self.selected)

            if self.account: self.subAccounts.set(self.account.getClientsAccounts(), showAttr={'region': 'name'})

        self.selected(self.account)

    def selectedRecordsManager(self, rm): self.selected(rm, 1)

    def openManager(self):
        self.selected(self.account)

    def selected(self, sub, rm=0):
        # return
        if not rm: self.overview.updateDCDigits(sub)
        self.table.setColumns(self.columns(sub))
        self.table.viewObjs(sub)


