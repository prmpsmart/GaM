from ..core.prmp_gui.extensions import *
from ..dc.dc_extensions import *
from ..core.agam_extensions import *



class DCHome(PRMP_MainWindow):
    def __init__(self, master=None, geo=(1000, 700), title='DC Home', **kwargs):
        super().__init__(master, geo=geo, title=title, **kwargs)

        details = LabelFrame(self.container, place=dict(relx=.02, rely=.005, relh=.176, relw=.696), text='Details')

        self.persons = LabelButton(details, topKwargs=dict(config=dict(text='Persons')), place=dict(relx=.02, rely=0, relh=.35, relw=.3), orient='h', longent=.4)

        self.subs = LabelButton(details, topKwargs=dict(config=dict(text='Total Subs', anchor='center')), place=dict(relx=.02, rely=.4, relh=.35, relw=.3), orient='h')

        self.actSubs = LabelButton(details, topKwargs=dict(config=dict(text='Active Subs', anchor='center')), place=dict(relx=.57, rely=0, relh=.18, relw=.35), orient='h', longent=.4)
        
        self.actSubsAccs = LabelButton(details, topKwargs=dict(config=dict(text='Active Subs Accounts', anchor='center')), place=dict(relx=.346, rely=.632, h=23, w=123), orient='h', longent=.4)

        self.accounts = LabelButton(details, topKwargs=dict(config=dict(text='Total Accounts', anchor='center')), place=dict(relx=.677, rely=.316, h=23, w=123), orient='h', longent=.4)

        self.objdet = Button(details, place=dict(relx=.795, rely=.632, h=28, w=119), text='Object Details')

        self.dc_overview = DC_Overview(self.container, place=dict(relx=.02, rely=.259, relh=.719, relw=.976), orient='h')




