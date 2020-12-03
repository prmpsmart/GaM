from .packed import *


class Toplevel:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("1047x646")
        top.title("New Toplevel")
        top.configure(background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")

        self.Label1 = tk.Label(top, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 14 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='''Areas''')
        self.Label1.place(relx=.01, rely=.062, h=33, w=123)

        self.Label2 = tk.Label(top, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 14 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='''006''')
        self.Label2.place(relx=.143, rely=.062, h=33, w=103)

        self.Frame1_11 = DC_Overview(top, relief='groove', borderwidth="2", background="#d9d9d9", highlightbackground="#ff8040", highlightcolor="black")
        self.Frame1_11.place(relx=.35, rely=0, relh=1, relw=.65)


        self.Frame1 = tk.Frame(top, relief='groove', borderwidth="2", background="#d9d9d9", highlightbackground="#ff8040", highlightcolor="black")
        self.Frame1.place(relx=.01, rely=.139, relh=.859, relw=.33)

        self.Labelframe1 = tk.LabelFrame(self.Frame1, relief='groove', font="-family {Times New Roman} -size 11 -weight bold", foreground="black", text='''Month''', background="#d9d9d9", highlightbackground="#ff8040", highlightcolor="black")
        self.Labelframe1.place(relx=.029, rely=.144, relh=.297, relw=.957)

        self.Label1_14 = tk.Label(self.Labelframe1, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 17 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='''December''')
        self.Label1_14.place(relx=.061, rely=.121, h=33, w=183, bordermode='ignore')

        self.Label1_15 = tk.Label(self.Labelframe1, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 17 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='''2020''')
        self.Label1_15.place(relx=.667, rely=.121, h=33, w=93, bordermode='ignore')

        self.Label1_8 = tk.Label(self.Labelframe1, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='''Clients''')
        self.Label1_8.place(relx=.061, rely=.424, h=23, w=113, bordermode='ignore')

        self.Label2_9 = tk.Label(self.Labelframe1, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='''340''')
        self.Label2_9.place(relx=.485, rely=.424, h=23, w=93, bordermode='ignore')

        self.Button1 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000", background="#d9d9d9", disabledforeground="#bf6030", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Prev''')
        self.Button1.place(relx=.061, rely=.788, h=28, w=45, bordermode='ignore')

        self.Button1_9 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000", background="#d9d9d9", disabledforeground="#bf6030", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Current''')
        self.Button1_9.place(relx=.394, rely=.788, h=28, w=65, bordermode='ignore')

        self.Button1_10 = tk.Button(self.Labelframe1, activebackground="#ececec", activeforeground="#000000", background="#d9d9d9", disabledforeground="#bf6030", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='''Next''')
        self.Button1_10.place(relx=.788, rely=.788, h=28, w=45, bordermode='ignore')

        self.Labelframe1_13 = tk.LabelFrame(self.Frame1, relief='groove', font="-family {Times New Roman} -size 11 -weight bold", foreground="black", text='''Sort and Search''', background="#d9d9d9", highlightbackground="#ff8040", highlightcolor="black")
        self.Labelframe1_13.place(relx=.029, rely=.505, relh=.477, relw=.957)

        self.Labelframe1_9 = tk.LabelFrame(self.Frame1, relief='groove', font="-family {Times New Roman} -size 11 -weight bold", foreground="black", text='''Date and Time''', background="#d9d9d9", highlightbackground="#ff8040", highlightcolor="black")
        self.Labelframe1_9.place(relx=.029, rely=.018, relh=.099, relw=.957)

        self.Label3 = tk.Label(self.Labelframe1_9, activebackground="#ffaa7f", activeforeground="black", background="#d9d9d9", disabledforeground="#bf6030", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#ff8040", highlightcolor="black", relief="ridge", text='''03 : 23 AM''')
        self.Label3.place(relx=.03, rely=.364, h=23, w=103, bordermode='ignore')

        self.Label3_11 = tk.Label(self.Labelframe1_9, activebackground="#ffaa7f", activeforeground="black", background="#d9d9d9", disabledforeground="#bf6030", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#ff8040", highlightcolor="black", relief="ridge", text='''Tuesday 1, December 2020''')
        self.Label3_11.place(relx=.394, rely=.364, h=23, w=193, bordermode='ignore')
