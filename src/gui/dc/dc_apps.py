from .dc_dialogs import *


class DC_Home(PRMP_MainWindow):
    def __init__(self, master=None, geo=(1000, 850), title='DC Home', region=None, resize=(1, 1), **kwargs):
        super().__init__(master, geo=geo, title=title, resize=resize, **kwargs)

        self.region = region
        self.addTitleBar(region)

        self.regionDetails = RegionDetails(self.container, config=dict(text='Region Details'), place=dict(relx=.005, rely=.005, relh=.22, relw=.45), region=region)

        self.furtherDetails = FurtherDetails(self.container, place=dict(relx=.46, rely=.005, relh=.22, relw=.535), region=region)

        self.dc_overview = DC_Overview(self.container, place=dict(relx=.005, rely=.23, relh=.765, relw=.99), orient='v', region=region, relief='groove')

        self.paint()


class DC_Home1(TreeColumns, Home1):
    def _setupApp(self):
        super()._setupApp()
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




