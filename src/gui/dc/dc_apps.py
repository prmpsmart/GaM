from .dc_dialogs import *

def addNote(self):
    
    self.overview = DC_Overview(self.note, region=self.obj)
    self.note.add(self.overview, padding=3)
    self.note.tab(0, text='Overview', compound='left', underline='-1')

    self.tree = Hierachy(self.note)
    self.note.add(self.tree, padding=3)
    self.note.tab(1, text='Tree', compound='left', underline='-1')


class DC_RegionHome(TreeColumns, RegionHome):
    def _setupApp(self):
        super()._setupApp()
        
        self.addTitleBar('DC Region Home')

        self.subRegions.callback = self.selectedSubRegion
        self.accounts.callback = self.selectedAccount
        addNote(self)
        self.selected(self.region)

    def selectedSubRegion(self, region):
        self.selected(region)

    def selectedAccount(self, account):
        self.selected(account)
        self.overview.updateDCDigits(account)

    def selected(self, sub):
        self.tree.setColumns(self.columns(sub))
        self.tree.viewAll(sub)



class DC_AccountHome(TreeColumns, AccountHome):
    def _setupApp(self):
        super()._setupApp()
        
        self.addTitleBar('DC Account Home')

        self.recordsManagers.callback = self.selectedRecordsManager
        addNote(self)
        self.selected(self.account)

    def selectedRecordsManager(self, rm):
        self.selected(rm)

    def selected(self, sub):
        self.tree.setColumns(self.columns(sub))
        self.tree.viewAll(sub)




# 



