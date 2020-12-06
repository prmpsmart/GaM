from .prmp_gui.extensions import *


class OfficeDetails(LabelFrame):
    def __init__(self, master=None, text='Office Details', office=None, **kwargs):
        super().__init__(master=master, text=text, **kwargs)

        self.office = office
        
        Label(self, text='Office').place(relx=.02, rely=0, relh=.3, relw=.35)

        Label(self, text='Areas', place=dict(relx=.02, rely=.32, relh=.32, relw=.35))

        Label(self, text='Clients', place=dict(relx=.02, rely=.64, relh=.32, relw=.35))

        self.name = Label(self, asEntry=True, font='PRMP_FONT', text='Owode', place=dict(relx=.4, rely=0, relh=.3, relw=.58))

        self.areas = Label(self, asEntry=True, font='PRMP_FONT', text='6', place=dict(relx=.4, rely=.32, relh=.3, relw=.58))

        self.clients = Label(self, asEntry=True, font='PRMP_FONT', text='1280', place=dict(relx=.4, rely=.64, relh=.3, relw=.58))


class MonthBox(LabelFrame):
    def __init__(self, master=None, text='Month', account=None, **kwargs):
        super().__init__(master=master, text=text, **kwargs)

        self.account = account
        
        self.month = Label(self, text='December 2020', place=dict(relx=.02, rely=0, relh=.35, relw=.96))

        Label(self, text='Active Clients', place=dict(relx=.02, rely=.4, relh=.25, relw=.5))

        self.activeClients = Label(self, asEntry=True, font='PRMP_FONT', text='360', place=dict(relx=.55, rely=.4, relh=.25, relw=.43))

        self.previous = Button(self, text='Previous', place=dict(relx=.02, rely=.73, relh=.2, relw=.3))

        self.current = Button(self, text='Current', place=dict(relx=.35, rely=.73, relh=.2, relw=.3))

        self.next = Button(self, text='Next', place=dict(relx=.68, rely=.73, relh=.2, relw=.3))


class AccountHighlight(LabelFrame):
    def __init__(self, master=None, text='Account Highlight', subOffice=None, **kwargs):
        super().__init__(master=master, text=text, **kwargs)

        self.subOffice = subOffice
        
        Label(self, text='Areas', place=dict(relx=.02, rely=.01, relh=.1, relw=.17))

        Label(self, text='Clients', place=dict(relx=.02, rely=.13, relh=.1, relw=.17))

        self.sups = Combobox(self, place=dict(relx=.2, rely=.01, relh=.1, relw=.3))

        self.subs = Combobox(self, place=dict(relx=.2, rely=.13, relh=.1, relw=.3))

        
        accounts = LabelFrame(self, text='Accounts', place=dict(relx=.02, rely=.23, relh=.692, relw=.965))

        # self.style.configure('Treeview.Heading',  font=font9)
        self.Scrolledtreeview1 = ScrolledTreeView(accounts)
        self.Scrolledtreeview1.place(relx=.01, rely=.005, relh=.99, relw=.98)
        self.Scrolledtreeview1.configure(columns="Col1")
        # build_treeview_support starting.
        self.Scrolledtreeview1.heading("#0",text="Tree")
        self.Scrolledtreeview1.heading("#0",anchor="center")
        self.Scrolledtreeview1.column("#0",w="257")
        self.Scrolledtreeview1.column("#0",minw="20")
        self.Scrolledtreeview1.column("#0",stretch="1")
        self.Scrolledtreeview1.column("#0",anchor="w")
        self.Scrolledtreeview1.heading("Col1",text="Col1")
        self.Scrolledtreeview1.heading("Col1",anchor="center")
        self.Scrolledtreeview1.column("Col1",w="258")
        self.Scrolledtreeview1.column("Col1",minw="20")
        self.Scrolledtreeview1.column("Col1",stretch="1")
        self.Scrolledtreeview1.column("Col1",anchor="w")
