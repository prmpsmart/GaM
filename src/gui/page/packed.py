from ..core.prmp_gui.extensions import *
from ..dc.dc_extensions import *
from ..core.agam_extensions import *



class DCHome(PRMP_MainWindow):
    def __init__(self, master=None, geo=(1000, 700), title='DC Home', **kwargs):
        super().__init__(master, geo=geo, title=title, **kwargs)

        details = LabelFrame(self.container, place=dict(relx=.02, rely=.005, relh=.176, relw=.96), text='Details')

        self.persons = LabelButton(details, topKwargs=dict(config=dict(text='Persons')), place=dict(relx=.02, rely=0, relh=.35, relw=.2), orient='h', longent=.5)

        self.subs = LabelButton(details, topKwargs=dict(config=dict(text='Total Subs', anchor='center')), place=dict(relx=.02, rely=.4, relh=.35, relw=.25), orient='h', longent=.55)

        self.actSubs = LabelButton(details, topKwargs=dict(config=dict(text='Active Subs', anchor='center')), place=dict(relx=.3, rely=0, relh=.35, relw=.3), orient='h')

        self.accounts = LabelButton(details, topKwargs=dict(config=dict(text='Total Accounts', anchor='center')), place=dict(relx=.3, rely=.4, relh=.35, relw=.3), orient='h', longent=.65)
        
        self.actSubsAccs = LabelButton(details, topKwargs=dict(config=dict(text='Active Subs Accounts', anchor='center')), place=dict(relx=.62, rely=0, relh=.35, relw=.32), orient='h', longent=.65)

        self.objdet = Button(details, place=dict(relx=.795, rely=.632, h=28, w=119), text='Object Details')

        self.dc_overview = DC_Overview(self.container, place=dict(relx=.02, rely=.259, relh=.719, relw=.96), orient='h')




