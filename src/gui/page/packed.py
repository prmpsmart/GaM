from ..core.prmp_gui.extensions import *
from ..dc.dc_extensions import *
from ..core.agam_extensions import *




class DCObjDetails(PRMP_MainWindow):
    def __init__(self, master=None, geo=(900, 350), title='DC Object Details', **kwargs):
        super().__init__(master, geo=geo, title=title, **kwargs)


        self.Labelframe1 = LabelFrame(top, place=dict(relx=0.011, rely=0.029, relh=0.965, relw=0.285), text='''Object Subcripts''')

        self.Label2 = Label(self.Labelframe1, place=dict(relx=0.038, rely=0.091, h=26, w=73, text='''Region''')

        self.Button2 = Button(self.Labelframe1, place=dict(relx=0.346, rely=0.091, h=25, w=156, text='''Apata Miracle Peter''')

        self.Labelframe1_1 = LabelFrame(self.Labelframe1, place=dict(relx=0.038, rely=0.366, relh=0.546, relw=0.912, text='''Subs''')

        self.Scrolledlistbox1 = ScrolledListBox(self.Labelframe1_1, place=dict(relx=0.021, rely=0.112, relh=0.838, relw=0.92)

        self.Checkbutton1 = Checkbutton(self.Labelframe1, place=dict(relx=0.577, rely=0.183, relh=0.076, relw=0.365)
        self.Checkbutton1.configure(activebackground="#ececec")
        self.Checkbutton1.configure(activeforeground="#000000")
        self.Checkbutton1.configure(background="#d9d9d9")
        self.Checkbutton1.configure(disabledforeground="#a3a3a3")
        self.Checkbutton1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Checkbutton1.configure(foreground="#000000")
        self.Checkbutton1.configure(highlightbackground="#d9d9d9")
        self.Checkbutton1.configure(highlightcolor="black")
        self.Checkbutton1.configure(justify='left')
        self.Checkbutton1.configure(relief="groove")
        self.Checkbutton1.configure(text='''Dialog?''')
        self.Checkbutton1.configure(variable=object_details_support.che76)

        self.Label1_3 = Label(self.Labelframe1, place(relx=0.038, rely=0.305, h=23, w=123), text='''Total Subs''')

        self.Label1_1 = Label(self.Labelframe1), place(relx=0.538, rely=0.305, h=24, w=63), text='''6''')

        self.TCombobox1 = Combobox(self.Labelframe1, place=dict(relx=0.038, rely=0.183, relh=0.073, relw=0.319)
        
        self.Scrolledtreeview2 = ScrolledTreeView(top, place=dict(relx=0.307, rely=0.059, relh=0.915, relw=0.68)
        self.Scrolledtreeview2.configure(columns="Col1")
        # build_treeview_support starting.
        self.Scrolledtreeview2.heading("#0",text="Tree")
        self.Scrolledtreeview2.heading("#0",anchor="center")
        self.Scrolledtreeview2.column("#0",w="300")
        self.Scrolledtreeview2.column("#0",minw="20")
        self.Scrolledtreeview2.column("#0",stretch="1")
        self.Scrolledtreeview2.column("#0",anchor="w")
        self.Scrolledtreeview2.heading("Col1",text="Col1")
        self.Scrolledtreeview2.heading("Col1",anchor="center")
        self.Scrolledtreeview2.column("Col1",w="301")
        self.Scrolledtreeview2.column("Col1",minw="20")
        self.Scrolledtreeview2.column("Col1",stretch="1")
        self.Scrolledtreeview2.column("Col1",anchor="w")

