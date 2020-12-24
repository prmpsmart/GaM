from .dc_dialogs import *


class DCHome(PRMP_MainWindow):
    def __init__(self, master=None, geo=(1000, 850), title='DC Home', region=None, **kwargs):
        super().__init__(master, geo=geo, title=title, **kwargs)

        self.region = region
        self.addTitleBar(region)

        self.regionDetails = RegionDetails(self.container, config=dict(text='Region Details'), place=dict(relx=.005, rely=.005, relh=.22, relw=.45), region=region)

        self.furtherDetails = FurtherDetails(self.container, place=dict(relx=.46, rely=.005, relh=.22, relw=.535), region=region)

        self.dc_overview = DC_Overview(self.container, place=dict(relx=.005, rely=.23, relh=.765, relw=.99), orient='h', region=region, relief='groove')

        self.paint()





