from .packed import *
sys = os.sys


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#800080'  # Closest X11 color: 'magenta4'
        _fgcolor = '#ffffff'  # X11 color: 'white'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font9 = "-family {Times New Roman} -size 11 -weight bold -slant roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font=font9)
        self.style.map('.',background=[('selected', _compcolor), ('active',_ana2color)])

        top.geometry("577x554")
        top.title("New Toplevel")
        top.configure(background="#800080")

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.0, rely=0.0, relheight=0.226
                , relwidth=0.468)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''DC Office Details''')
        self.Labelframe1.configure(background="#800080")

        self.Label1 = tk.Label(self.Labelframe1)
        self.Label1.place(relx=0.037, rely=0.24, height=23, width=100
                , bordermode='ignore')
        self.Label1.configure(background="#800080")
        self.Label1.configure(disabledforeground="#bf6030")
        self.Label1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1.configure(foreground="#ffffff")
        self.Label1.configure(relief="groove")
        self.Label1.configure(text='''Office''')

        self.Label1_1 = tk.Label(self.Labelframe1)
        self.Label1_1.place(relx=0.037, rely=0.48, height=23, width=100
                , bordermode='ignore')
        self.Label1_1.configure(activebackground="#ffaa7f")
        self.Label1_1.configure(activeforeground="black")
        self.Label1_1.configure(background="#800080")
        self.Label1_1.configure(disabledforeground="#bf6030")
        self.Label1_1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_1.configure(foreground="#ffffff")
        self.Label1_1.configure(highlightbackground="#ff8040")
        self.Label1_1.configure(highlightcolor="black")
        self.Label1_1.configure(relief="groove")
        self.Label1_1.configure(text='''Areas''')

        self.Label1_4 = tk.Label(self.Labelframe1)
        self.Label1_4.place(relx=0.463, rely=0.24, height=23, width=130
                , bordermode='ignore')
        self.Label1_4.configure(activebackground="#ffaa7f")
        self.Label1_4.configure(activeforeground="black")
        self.Label1_4.configure(background="#0000ff")
        self.Label1_4.configure(disabledforeground="#bf6030")
        self.Label1_4.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_4.configure(foreground="#ffffff")
        self.Label1_4.configure(highlightbackground="#ff8040")
        self.Label1_4.configure(highlightcolor="black")
        self.Label1_4.configure(relief="sunken")
        self.Label1_4.configure(text='''Owode''')

        self.Label1_5 = tk.Label(self.Labelframe1)
        self.Label1_5.place(relx=0.463, rely=0.48, height=23, width=130
                , bordermode='ignore')
        self.Label1_5.configure(activebackground="#ffaa7f")
        self.Label1_5.configure(activeforeground="black")
        self.Label1_5.configure(background="#0000ff")
        self.Label1_5.configure(disabledforeground="#bf6030")
        self.Label1_5.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_5.configure(foreground="#ffffff")
        self.Label1_5.configure(highlightbackground="#ff8040")
        self.Label1_5.configure(highlightcolor="black")
        self.Label1_5.configure(relief="sunken")
        self.Label1_5.configure(text='''6''')

        self.Label1_5 = tk.Label(self.Labelframe1)
        self.Label1_5.place(relx=0.463, rely=0.72, height=23, width=130
                , bordermode='ignore')
        self.Label1_5.configure(activebackground="#ffaa7f")
        self.Label1_5.configure(activeforeground="black")
        self.Label1_5.configure(background="#0000ff")
        self.Label1_5.configure(disabledforeground="#bf6030")
        self.Label1_5.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_5.configure(foreground="#ffffff")
        self.Label1_5.configure(highlightbackground="#ff8040")
        self.Label1_5.configure(highlightcolor="black")
        self.Label1_5.configure(relief="sunken")
        self.Label1_5.configure(text='''1280''')

        self.Label1_2 = tk.Label(self.Labelframe1)
        self.Label1_2.place(relx=0.037, rely=0.72, height=23, width=100
                , bordermode='ignore')
        self.Label1_2.configure(activebackground="#ffaa7f")
        self.Label1_2.configure(activeforeground="black")
        self.Label1_2.configure(background="#800080")
        self.Label1_2.configure(disabledforeground="#bf6030")
        self.Label1_2.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_2.configure(foreground="#ffffff")
        self.Label1_2.configure(highlightbackground="#ff8040")
        self.Label1_2.configure(highlightcolor="black")
        self.Label1_2.configure(relief="groove")
        self.Label1_2.configure(text='''Clients''')

        self.Labelframe2 = tk.LabelFrame(top)
        self.Labelframe2.place(relx=0.503, rely=0.0, relheight=0.28
                , relwidth=0.47)
        self.Labelframe2.configure(relief='groove')
        self.Labelframe2.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Labelframe2.configure(foreground="black")
        self.Labelframe2.configure(text='''Month''')
        self.Labelframe2.configure(background="#800080")

        self.Label1_3 = tk.Label(self.Labelframe2)
        self.Label1_3.place(relx=0.037, rely=0.452, height=23, width=100
                , bordermode='ignore')
        self.Label1_3.configure(activebackground="#ffaa7f")
        self.Label1_3.configure(activeforeground="black")
        self.Label1_3.configure(background="#800080")
        self.Label1_3.configure(disabledforeground="#bf6030")
        self.Label1_3.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_3.configure(foreground="#ffffff")
        self.Label1_3.configure(highlightbackground="#ff8040")
        self.Label1_3.configure(highlightcolor="black")
        self.Label1_3.configure(relief="groove")
        self.Label1_3.configure(text='''Active Clients''')

        self.Label1_5 = tk.Label(self.Labelframe2)
        self.Label1_5.place(relx=0.48, rely=0.452, height=23, width=130
                , bordermode='ignore')
        self.Label1_5.configure(activebackground="#ffaa7f")
        self.Label1_5.configure(activeforeground="black")
        self.Label1_5.configure(background="#0000ff")
        self.Label1_5.configure(disabledforeground="#bf6030")
        self.Label1_5.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_5.configure(foreground="#ffffff")
        self.Label1_5.configure(highlightbackground="#ff8040")
        self.Label1_5.configure(highlightcolor="black")
        self.Label1_5.configure(relief="sunken")
        self.Label1_5.configure(text='''360''')

        self.Label1_4 = tk.Label(self.Labelframe2)
        self.Label1_4.place(relx=0.037, rely=0.194, height=32, width=249
                , bordermode='ignore')
        self.Label1_4.configure(activebackground="#ffaa7f")
        self.Label1_4.configure(activeforeground="black")
        self.Label1_4.configure(background="#800080")
        self.Label1_4.configure(disabledforeground="#bf6030")
        self.Label1_4.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_4.configure(foreground="#ffffff")
        self.Label1_4.configure(highlightbackground="#ff8040")
        self.Label1_4.configure(highlightcolor="black")
        self.Label1_4.configure(relief="groove")
        self.Label1_4.configure(text='''December 2020''')

        self.Button1 = tk.Button(self.Labelframe2)
        self.Button1.place(relx=0.037, rely=0.774, height=28, width=72
                , bordermode='ignore')
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#ffffff")
        self.Button1.configure(background="#800080")
        self.Button1.configure(disabledforeground="#bf6030")
        self.Button1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Button1.configure(foreground="#ffffff")
        self.Button1.configure(highlightbackground="#800080")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''Previous''')

        self.Button1_5 = tk.Button(self.Labelframe2)
        self.Button1_5.place(relx=0.738, rely=0.774, height=28, width=59
                , bordermode='ignore')
        self.Button1_5.configure(activebackground="#ececec")
        self.Button1_5.configure(activeforeground="#ffffff")
        self.Button1_5.configure(background="#800080")
        self.Button1_5.configure(disabledforeground="#bf6030")
        self.Button1_5.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Button1_5.configure(foreground="#ffffff")
        self.Button1_5.configure(highlightbackground="#800080")
        self.Button1_5.configure(highlightcolor="black")
        self.Button1_5.configure(pady="0")
        self.Button1_5.configure(text='''Next''')

        self.Button1_6 = tk.Button(self.Labelframe2)
        self.Button1_6.place(relx=0.406, rely=0.774, height=28, width=59
                , bordermode='ignore')
        self.Button1_6.configure(activebackground="#ececec")
        self.Button1_6.configure(activeforeground="#ffffff")
        self.Button1_6.configure(background="#800080")
        self.Button1_6.configure(disabledforeground="#bf6030")
        self.Button1_6.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Button1_6.configure(foreground="#ffffff")
        self.Button1_6.configure(highlightbackground="#800080")
        self.Button1_6.configure(highlightcolor="black")
        self.Button1_6.configure(pady="0")
        self.Button1_6.configure(text='''Current''')

        self.Labelframe3 = tk.LabelFrame(top)
        self.Labelframe3.place(relx=0.0, rely=0.397, relheight=0.587
                , relwidth=0.997)
        self.Labelframe3.configure(relief='groove')
        self.Labelframe3.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Labelframe3.configure(foreground="black")
        self.Labelframe3.configure(text='''Account Highlight''')
        self.Labelframe3.configure(background="#800080")

        self.Labelframe4 = tk.LabelFrame(self.Labelframe3)
        self.Labelframe4.place(relx=0.017, rely=0.277, relheight=0.692
                , relwidth=0.965, bordermode='ignore')
        self.Labelframe4.configure(relief='groove')
        self.Labelframe4.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Labelframe4.configure(foreground="black")
        self.Labelframe4.configure(text='''Accounts''')
        self.Labelframe4.configure(background="#800080")

        self.style.configure('Treeview.Heading',  font=font9)
        self.Scrolledtreeview1 = ScrolledTreeView(self.Labelframe4)
        self.Scrolledtreeview1.place(relx=0.018, rely=0.133, relheight=0.831
                , relwidth=0.962, bordermode='ignore')
        self.Scrolledtreeview1.configure(columns="Col1")
        # build_treeview_support starting.
        self.Scrolledtreeview1.heading("#0",text="Tree")
        self.Scrolledtreeview1.heading("#0",anchor="center")
        self.Scrolledtreeview1.column("#0",width="257")
        self.Scrolledtreeview1.column("#0",minwidth="20")
        self.Scrolledtreeview1.column("#0",stretch="1")
        self.Scrolledtreeview1.column("#0",anchor="w")
        self.Scrolledtreeview1.heading("Col1",text="Col1")
        self.Scrolledtreeview1.heading("Col1",anchor="center")
        self.Scrolledtreeview1.column("Col1",width="258")
        self.Scrolledtreeview1.column("Col1",minwidth="20")
        self.Scrolledtreeview1.column("Col1",stretch="1")
        self.Scrolledtreeview1.column("Col1",anchor="w")

        self.Label1_3 = tk.Label(self.Labelframe3)
        self.Label1_3.place(relx=0.017, rely=0.092, height=23, width=100
                , bordermode='ignore')
        self.Label1_3.configure(activebackground="#ffaa7f")
        self.Label1_3.configure(activeforeground="black")
        self.Label1_3.configure(background="#800080")
        self.Label1_3.configure(disabledforeground="#bf6030")
        self.Label1_3.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_3.configure(foreground="#ffffff")
        self.Label1_3.configure(highlightbackground="#ff8040")
        self.Label1_3.configure(highlightcolor="black")
        self.Label1_3.configure(relief="groove")
        self.Label1_3.configure(text='''Areas''')

        self.Label1_3 = tk.Label(self.Labelframe3)
        self.Label1_3.place(relx=0.017, rely=0.185, height=23, width=100
                , bordermode='ignore')
        self.Label1_3.configure(activebackground="#ffaa7f")
        self.Label1_3.configure(activeforeground="black")
        self.Label1_3.configure(background="#800080")
        self.Label1_3.configure(disabledforeground="#bf6030")
        self.Label1_3.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_3.configure(foreground="#ffffff")
        self.Label1_3.configure(highlightbackground="#ff8040")
        self.Label1_3.configure(highlightcolor="black")
        self.Label1_3.configure(relief="groove")
        self.Label1_3.configure(text='''Clients''')

        self.TCombobox1 = ttk.Combobox(self.Labelframe3)
        self.TCombobox1.place(relx=0.209, rely=0.092, relheight=0.074
                , relwidth=0.249, bordermode='ignore')
        self.TCombobox1.configure(textvariable=dcofficedetails_support.combobox)
        self.TCombobox1.configure(takefocus="")

        self.TCombobox1_4 = ttk.Combobox(self.Labelframe3)
        self.TCombobox1_4.place(relx=0.209, rely=0.169, relheight=0.074
                , relwidth=0.249, bordermode='ignore')
        self.TCombobox1_4.configure(textvariable=dcofficedetails_support.combobox)
        self.TCombobox1_4.configure(takefocus="")





