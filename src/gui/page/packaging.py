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



class DCObjDetails:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        font11 = "-family {Courier New} -size 10 -weight normal -slant"  \
            " roman -underline 0 -overstrike 0"
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

        top.geometry("912x340")
        top.title("DC Object Details")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.menubar = tk.Menu(top,font=font12,bg='#004000',fg='#ffff00')
        top.configure(menu = self.menubar)

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.011, rely=0.029, relheight=0.965
                , relwidth=0.285)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''Object Subcripts''')
        self.Labelframe1.configure(background="#d9d9d9")
        self.Labelframe1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1.configure(highlightcolor="black")

        self.Label2 = tk.Label(self.Labelframe1)
        self.Label2.place(relx=0.038, rely=0.091, height=26, width=73
                , bordermode='ignore')
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(relief="groove")
        self.Label2.configure(text='''Region''')

        self.Button2 = tk.Button(self.Labelframe1)
        self.Button2.place(relx=0.346, rely=0.091, height=25, width=156
                , bordermode='ignore')
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(relief="sunken")
        self.Button2.configure(text='''Apata Miracle Peter''')

        self.Labelframe1_1 = tk.LabelFrame(self.Labelframe1)
        self.Labelframe1_1.place(relx=0.038, rely=0.366, relheight=0.546
                , relwidth=0.912, bordermode='ignore')
        self.Labelframe1_1.configure(relief='groove')
        self.Labelframe1_1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Labelframe1_1.configure(foreground="black")
        self.Labelframe1_1.configure(text='''Subs''')
        self.Labelframe1_1.configure(background="#d9d9d9")
        self.Labelframe1_1.configure(highlightbackground="#d9d9d9")
        self.Labelframe1_1.configure(highlightcolor="black")

        self.Scrolledlistbox1 = ScrolledListBox(self.Labelframe1_1)
        self.Scrolledlistbox1.place(relx=0.021, rely=0.112, relheight=0.838
                , relwidth=0.92, bordermode='ignore')
        self.Scrolledlistbox1.configure(background="white")
        self.Scrolledlistbox1.configure(disabledforeground="#a3a3a3")
        self.Scrolledlistbox1.configure(font=font11)
        self.Scrolledlistbox1.configure(foreground="black")
        self.Scrolledlistbox1.configure(highlightbackground="#d9d9d9")
        self.Scrolledlistbox1.configure(highlightcolor="#d9d9d9")
        self.Scrolledlistbox1.configure(selectbackground="#c4c4c4")
        self.Scrolledlistbox1.configure(selectforeground="black")

        self.Checkbutton1 = tk.Checkbutton(self.Labelframe1)
        self.Checkbutton1.place(relx=0.577, rely=0.183, relheight=0.076
                , relwidth=0.365, bordermode='ignore')
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

        self.Label1_3 = tk.Label(self.Labelframe1)
        self.Label1_3.place(relx=0.038, rely=0.305, height=23, width=123
                , bordermode='ignore')
        self.Label1_3.configure(activebackground="#f9f9f9")
        self.Label1_3.configure(activeforeground="black")
        self.Label1_3.configure(background="#d9d9d9")
        self.Label1_3.configure(disabledforeground="#a3a3a3")
        self.Label1_3.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_3.configure(foreground="#000000")
        self.Label1_3.configure(highlightbackground="#d9d9d9")
        self.Label1_3.configure(highlightcolor="black")
        self.Label1_3.configure(relief="groove")
        self.Label1_3.configure(text='''Total Subs''')

        self.Label1_1 = tk.Label(self.Labelframe1)
        self.Label1_1.place(relx=0.538, rely=0.305, height=24, width=63
                , bordermode='ignore')
        self.Label1_1.configure(activebackground="#f9f9f9")
        self.Label1_1.configure(activeforeground="black")
        self.Label1_1.configure(background="#d9d9d9")
        self.Label1_1.configure(disabledforeground="#a3a3a3")
        self.Label1_1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Label1_1.configure(foreground="#000000")
        self.Label1_1.configure(highlightbackground="#d9d9d9")
        self.Label1_1.configure(highlightcolor="black")
        self.Label1_1.configure(relief="sunken")
        self.Label1_1.configure(text='''6''')

        self.TCombobox1 = ttk.Combobox(self.Labelframe1)
        self.TCombobox1.place(relx=0.038, rely=0.183, relheight=0.073
                , relwidth=0.319, bordermode='ignore')
        self.TCombobox1.configure(textvariable=object_details_support.combobox)
        self.TCombobox1.configure(takefocus="")

        self.style.configure('Treeview.Heading',  font=font9)
        self.Scrolledtreeview2 = ScrolledTreeView(top)
        self.Scrolledtreeview2.place(relx=0.307, rely=0.059, relheight=0.915
                , relwidth=0.68)
        self.Scrolledtreeview2.configure(columns="Col1")
        # build_treeview_support starting.
        self.Scrolledtreeview2.heading("#0",text="Tree")
        self.Scrolledtreeview2.heading("#0",anchor="center")
        self.Scrolledtreeview2.column("#0",width="300")
        self.Scrolledtreeview2.column("#0",minwidth="20")
        self.Scrolledtreeview2.column("#0",stretch="1")
        self.Scrolledtreeview2.column("#0",anchor="w")
        self.Scrolledtreeview2.heading("Col1",text="Col1")
        self.Scrolledtreeview2.heading("Col1",anchor="center")
        self.Scrolledtreeview2.column("Col1",width="301")
        self.Scrolledtreeview2.column("Col1",minwidth="20")
        self.Scrolledtreeview2.column("Col1",stretch="1")
        self.Scrolledtreeview2.column("Col1",anchor="w")













