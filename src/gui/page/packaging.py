from .packed import *
sys = os.sys

class t: pass
ttk = tk = t()
gg = globals().copy()
for a in gg: setattr(t, a, gg[a])




class DCSubs:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font12 = "-family {Segoe UI} -size 9 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
        font9 = "-family {Times New Roman} -size 11 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font=font9)
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("760x541")
        top.title("DC Subs")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.013, rely=0.176, relheight=0.811
                , relwidth=0.974)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''DC Subs Details''')
        self.Labelframe1.configure(background="#d9d9d9")
        self.Labelframe1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1.configure(highlightcolor="black")

        self.style.configure('Treeview.Heading',  font=font9)
        self.Scrolledtreeview1 = ScrolledTreeView(self.Labelframe1)
        self.Scrolledtreeview1.place(relx=0.014, rely=0.046, relheight=0.932
                , relwidth=0.973, bordermode='ignore')
        self.Scrolledtreeview1.configure(columns="Col1")
        # build_treeview_support starting.
        self.Scrolledtreeview1.heading("#0",text="Tree")
        self.Scrolledtreeview1.heading("#0",anchor="center")
        self.Scrolledtreeview1.column("#0",width="350")
        self.Scrolledtreeview1.column("#0",minwidth="20")
        self.Scrolledtreeview1.column("#0",stretch="1")
        self.Scrolledtreeview1.column("#0",anchor="w")
        self.Scrolledtreeview1.heading("Col1",text="Col1")
        self.Scrolledtreeview1.heading("Col1",anchor="center")
        self.Scrolledtreeview1.column("Col1",width="351")
        self.Scrolledtreeview1.column("Col1",minwidth="20")
        self.Scrolledtreeview1.column("Col1",stretch="1")
        self.Scrolledtreeview1.column("Col1",anchor="w")

        self.Labelframe1_1 = tk.LabelFrame(top)
        self.Labelframe1_1.place(relx=0.013, rely=0.0, relheight=0.176
                , relwidth=0.375)
        self.Labelframe1_1.configure(relief='groove')
        self.Labelframe1_1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Labelframe1_1.configure(foreground="black")
        self.Labelframe1_1.configure(text='''Details''')
        self.Labelframe1_1.configure(background="#d9d9d9")
        self.Labelframe1_1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1_1.configure(highlightcolor="black")

        self.Button1 = tk.Button(self.Labelframe1_1)
        self.Button1.place(relx=0.035, rely=0.632, height=28, width=121
                , bordermode='ignore')
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''New Sub''')

        self.Label1 = tk.Label(self.Labelframe1_1)
        self.Label1.place(relx=0.035, rely=0.211, height=33, width=103
                , bordermode='ignore')
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#d9d9d9")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1.configure(foreground="#000000")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(relief="groove")
        self.Label1.configure(text='''Total Subs''')

        self.Label1_5 = tk.Label(self.Labelframe1_1)
        self.Label1_5.place(relx=0.421, rely=0.211, height=33, width=83
                , bordermode='ignore')
        self.Label1_5.configure(activebackground="#f9f9f9")
        self.Label1_5.configure(activeforeground="black")
        self.Label1_5.configure(background="#d9d9d9")
        self.Label1_5.configure(disabledforeground="#a3a3a3")
        self.Label1_5.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_5.configure(foreground="#000000")
        self.Label1_5.configure(highlightbackground="#d9d9d9")
        self.Label1_5.configure(highlightcolor="black")
        self.Label1_5.configure(relief="sunken")
        self.Label1_5.configure(text='''76''')

        self.Button1_4 = tk.Button(self.Labelframe1_1)
        self.Button1_4.place(relx=0.526, rely=0.632, height=28, width=121
                , bordermode='ignore')
        self.Button1_4.configure(activebackground="#ececec")
        self.Button1_4.configure(activeforeground="#000000")
        self.Button1_4.configure(background="#d9d9d9")
        self.Button1_4.configure(disabledforeground="#a3a3a3")
        self.Button1_4.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Button1_4.configure(foreground="#000000")
        self.Button1_4.configure(highlightbackground="#d9d9d9")
        self.Button1_4.configure(highlightcolor="black")
        self.Button1_4.configure(pady="0")
        self.Button1_4.configure(text='''Search and Sort''')

        self.menubar = tk.Menu(top,font=font12,bg='#004000',fg='#ffff00')
        top.configure(menu = self.menubar)










