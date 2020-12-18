from ..core.prmp_gui.extensions import *
from ..dc.dc_extensions import *
from ..core.agam_extensions import *

class SupDCDetails(LabelFrame):
    def __init__(self, master, text='Details', region=None, **kwargs):
        super().__init__(master, text=text, **kwargs)

        self.region = region
        
        self.persons = LabelButton(self, topKwargs=dict(config=dict(text='Persons')), place=dict(relx=.02, rely=0, relh=.35, relw=.2), orient='h', longent=.5)

        self.subs = LabelButton(self, topKwargs=dict(config=dict(text='Total Subs', anchor='center')), place=dict(relx=.02, rely=.4, relh=.35, relw=.25), orient='h', longent=.55)

        self.actSubs = LabelButton(self, topKwargs=dict(config=dict(text='Active Subs', anchor='center')), place=dict(relx=.3, rely=0, relh=.35, relw=.3), orient='h')

        self.accounts = LabelButton(self, topKwargs=dict(config=dict(text='Total Accounts', anchor='center')), place=dict(relx=.3, rely=.4, relh=.35, relw=.3), orient='h', longent=.65)
        
        self.actSubsAccs = LabelButton(self, topKwargs=dict(config=dict(text='Active Subs Accounts', anchor='center')), place=dict(relx=.62, rely=0, relh=.35, relw=.32), orient='h', longent=.65)

        Button(self, place=dict(relx=.65, rely=.632, h=28, w=119), text='Object Details')

        Button(self, place=dict(relx=.795, rely=.632, h=28, w=119), text='Search', command=self.openSNS)

        self.sns = None
        self.objdet = None
    
    def openSNS(self):
        if self.sns: self.sns.topmost()
        self.sns = SortNSearch(self, sup=self.region)
        self.sns.mainloop()


class DCHome(PRMP_MainWindow):
    def __init__(self, master=None, geo=(1000, 700), title='DC Home', **kwargs):
        super().__init__(master, geo=geo, title=title, **kwargs)

        details = SupDCDetails(self.container, place=dict(relx=.02, rely=.005, relh=.18, relw=.96))

        self.dc_overview = DC_Overview(self.container, place=dict(relx=.02, rely=.2, relh=.79, relw=.96), orient='h')

        self.paint()




