from ..core.prmp_gui.extensions import *
from ..dc.dc_extensions import *
from ..core.agam_extensions import *


class SubsList(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.listbox = ListBox(self, text='Subs', place=dict(relx=0, rely=0, relh=.865, relw=1))

        self.total = LabelLabel(self, place=dict(relx=0, rely=.87, relh=.12, relw=.8), topKwargs=dict(text='Total Subs'), orient='h')




class DCObjectDetails(PRMP_MainWindow):
    def __init__(self, master=None, geo=(1200, 600), title='DC Object Details', **kwargs):
        super().__init__(master, geo=geo, title=title, **kwargs)

        sups = LabelFrame(self.container, place=dict(relx=.005, rely=.02, relh=.965, relw=.3), text='Object Subcripts')
        
        self.region = LabelButton(sups, place=dict(relx=.005, rely=0, relh=.07, relw=.99), topKwargs=dict(text='Region'), orient='h', longent=.2)

        self.subType = LabelCombo(sups, place=dict(relx=.005, rely=.08, relh=.07, relw=.7), topKwargs=dict(text='Sub Type'), bottomKwargs=dict(values=['Regions', 'Accounts', 'Records Managers', 'Records', 'Persons']), orient='h', longent=.4)

        self.dialog = Checkbutton(sups, place=dict(relx=.577, rely=.16, relh=.07, relw=.35), text='Dialog?')
        
        self.subsList = SubsList(sups, place=dict(relx=.038, rely=.24, relh=.73, relw=.9), text='Subs')

        self.subs = TreeView(self.container, place=dict(relx=.307, rely=.039, relh=.97, relw=.68))
        
        self.paint()














