from .packed import *
sys = os.sys


class Toplevel1(LabelFrame):
    def __init__(self, top=None):
        super().__init__(top, place=dict(relx=.014, rely=.014, relh=.861 , relw=.969))

        self.Labelframe2 = DateSearch(self, text='Date Search', place=dict(relx=.5, rely=.032, relh=.344 , relw=.456))

        # self.Frame1 = Frame(self, relief='groove', borderw='2')
        # self.Frame1.place(relx=.5, rely=.384, relh=.312, relw=.457 )

        self.TNotebook1 = ttk.Notebook(self)
        self.TNotebook1.place(relx=.5, rely=.384, relh=.312, relw=.457)
        # self.TNotebook1.place(relx=.0, rely=.026, relh=.974 , relw=.987)
        self.TNotebook1_t0 = tk.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t0, padding=3)
        self.TNotebook1.tab(0, text='Sub-regions', compound='left', underline='-1')
        self.TNotebook1_t1 = tk.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t1, padding=3)
        self.TNotebook1.tab(1, text='Accounts',compound='left',underline='-1')

        self.Scrolledlistbox1_3 = ScrolledListBox(self.TNotebook1_t0, background='white', disabledforeground='#a3a3a3', foreground='black', highlightbackground='#d9d9d9', highlightcolor='#800080', selectbackground='#c4c4c4', selectforeground='black')
        self.Scrolledlistbox1_3.place(relx=.0, rely=.0, relh=1.0 , relw=1.00)

        self.Scrolledtreeview1 = ScrolledTreeView(self.TNotebook1_t1)
        self.Scrolledtreeview1.place(relx=.0, rely=.0, relh=1.0 , relw=1.0)
        self.Scrolledtreeview1.config(columns='Col1')
        self.Scrolledtreeview1.heading('#0',text='Tree')
        self.Scrolledtreeview1.heading('#0',anchor='center')
        self.Scrolledtreeview1.column('#0',w='142')
        self.Scrolledtreeview1.column('#0',minw='20')
        self.Scrolledtreeview1.column('#0',stretch='1')
        self.Scrolledtreeview1.column('#0',anchor='w')
        self.Scrolledtreeview1.heading('Col1',text='Col1')
        self.Scrolledtreeview1.heading('Col1',anchor='center')
        self.Scrolledtreeview1.column('Col1',w='142')
        self.Scrolledtreeview1.column('Col1',minw='20')
        self.Scrolledtreeview1.column('Col1',stretch='1')
        self.Scrolledtreeview1.column('Col1',anchor='w')



        self.details = Notebook(self, place=dict(relx=.005, rely=.005, relh=.4, relw=.44))

        self.recordDetails = RecordDetails(self.details, text='Record Details', place=dict(relx=.005, rely=.005, relh=.8 , relw=.44))
        self.details.add(self.recordDetails, padding=3)
        self.details.tab(0, text='Regions', compound='left', underline='-1')

        self.personalDetails = PersonalDetails(self.details, text='Personal Details', place=dict(relx=.022, rely=.032, relh=.328 , relw=.25))
        self.details.add(self.personalDetails, padding=3)
        self.details.tab(1, text='Records', compound='left', underline='-1')






















