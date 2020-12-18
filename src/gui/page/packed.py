from ..core.prmp_gui.extensions import *
from ..dc.dc_extensions import *
from ..core.agam_extensions import *




class DCObjectDetails(PRMP_MainWindow):
    def __init__(self, master=None, geo=(1200, 600), title='DC Object Details', **kwargs):
        super().__init__(master, geo=geo, title=title, **kwargs)

        sups = LabelFrame(self.container, place=dict(relx=.005, rely=.02, relh=.965, relw=.3), text='Object Subcripts')
        
        self.region = LabelButton(sups, place=dict(relx=.038, rely=.091, h=26, w=73), text='Region')

        self.Button2 = Button(sups, place=dict(relx=.346, rely=.091, h=25, w=156), text='Apata Miracle Peter')

        self.Scrolledlistbox1 = ListBox(LabelFrame(sups, place=dict(relx=.038, rely=.4, relh=.546, relw=.912), text='Subs'), place=dict(relx=0, rely=0, relh=1, relw=1))

        self.Checkbutton1 = Checkbutton(sups, place=dict(relx=.577, rely=.183, relh=.076, relw=.365), text='Dialog?')

        self.Label1_3 = Label(sups, place=dict(relx=.038, rely=.305, h=23, w=123), text='Total Subs')

        self.Label1_1 = Label(sups, place=dict(relx=.538, rely=.305, h=24, w=63), text='6')

        self.TCombobox1 = Combobox(sups, place=dict(relx=.038, rely=.183, relh=.073, relw=.319))
        
        self.Scrolledtreeview2 = TreeView(self.container, place=dict(relx=.307, rely=.02, relh=.915, relw=.68))
        
        self.paint()














