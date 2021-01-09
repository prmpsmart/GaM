from .dc_dialogs import *


class DC_RegionHome(TreeColumns, RegionHome):
    def _setupApp(self):
        super()._setupApp()
        
        self.addTitleBar('DC Region Home')

        self.subRegions.callback = self.selectedSubRegion
        self.accounts.callback = self.selectedAccount

        self.overview = DC_Overview(self.note, region=self.region)
        self.note.add(self.overview, padding=3)
        self.note.tab(0, text='Overview', compound='left', underline='-1')

        self.tree = Hierachy(self.note)
        self.note.add(self.tree, padding=3)
        self.note.tab(1, text='Tree', compound='left', underline='-1')
        self.selected(self.region)

    def selectedSubRegion(self, region):
        self.selected(region)

    def selectedAccount(self, account):
        self.selected(account)
        self.overview.updateDCDigits(account)

    def selected(self, sub):
        self.tree.setColumns(self.columns(sub))
        self.tree.viewAll(sub)








