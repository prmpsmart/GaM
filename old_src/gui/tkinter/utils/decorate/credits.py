
from tkinter import Toplevel, Label, LabelFrame
from tkinter.ttk import Separator
import random, sys
from .styles import Styles



class Credits(Toplevel):
    brc = {"Sun": "#8F509D", "Mon": "#CD4A4C", "Tue": "#17806D", "Wed": "#EE204D", "Thur": "#FF6E4A", "Fri": "#1FCECB", "Sat": "#FF1DCE"}
    brcs = list(brc.keys())
    font = "-family {Times New Roman} -size 9 -weight bold"
    
    special_credits = {"BAMGBOSE OLALEKAN": "For the enlarging of the charts (Visualisation).", "OLAOYE TRUST": "For his ideas on the THEME/STYLE of the Software.", "UGWUANYI PRECIOUS": "The HOTSPOT Guy, his connections has guaranteed\nme for online solutions.", "ABOKEDE SEGUN": "For his advice on a better GUI of the Software", "OLORUNTOBI BEATRICE": "For her support financially and morally.\nFor her enlightenment on how the company runs its accounts."}
    more_credits = "More Credits goes to all the Authors of the numerous books I read because of the Project\nThanks to you all, your works speaks on."
    technical_credits = {"Guido Van Rossom": "For creating Python", "John Ousterhout": "For creating TCL/Tk", "D. Richard Hip": "For creating SQLite", "Gerhard Haring": "For creating SQLite binding for Python", "Fredrik Lundh": "For creating TCL/Tk binding for Python as tkinter", "Mark Hammond": "For creating WinCOM bindings for Python as PyWin32", "PRMP Smart": "For combining the works of the above great minds\ninto this software AGAM ANALYSIS SOFTWARE"}

    op = False

    def __init__(self, master=None):
        self._w = "self"
        if Credits.op == True: pass
        else:
            super().__init__(master)
            self.title("Credits")
            self.geometry("500x700")
            self["background"] = Styles.background
            self.attributes("-alpha", 1, "-disabled", False, "-toolwindow", True, "-topmost", True)
            self.wm_protocol("WM_DELETE_WINDOW", self.exiting)

            self.na = Label(self, text="Credits")
            
            self.spec_cred = LabelFrame(self, text="Special Credits")
            sp_sep = Separator(self.spec_cred, orient="vertical")
            sp_sep.place(relx=.304, rely=0, relh=.98, relw=.01)
            
            self.tech_cred = LabelFrame(self, text="Technical Credits")
            sp_sep = Separator(self.tech_cred, orient="vertical")
            sp_sep.place(relx=.304, rely=0, relh=.98, relw=.01)
            
            self.spec_func()
            self.tech_func()
            
            self.bind_all("<Return>", sys.exit)
            
            self.style()
            self.place_widgs()
            Credits.op = True
            self.mainloop()
    
    def exiting(self):
        Credits.op = False
        self.destroy()
    
    def spec_func(self):
        self.spec_labels = []
        a = 0
        h = 1/len(self.special_credits)
        g = h - .02
        for key in self.special_credits:
            val = self.special_credits[key]
            l = Label(self.spec_cred, text=key, font=self.font)
            l.place(relx=0, rely=a, relh=g, relw=.3)
            self.spec_labels.append(l)
            
            lb = Label(self.spec_cred, text=val)
            lb.place(relx=.318, rely=a, relh=g, relw=.682)
            self.spec_labels.append(lb)
            
            a += h

    def tech_func(self):
        self.tech_labels = []
        a = 0
        h = 1/len(self.technical_credits)
        g = h - .02
        for key in self.technical_credits:
            val = self.technical_credits[key]
            l = Label(self.tech_cred, text=key, font=self.font)
            l.place(relx=0, rely=a, relh=g, relw=.3)
            self.tech_labels.append(l)
            
            lb = Label(self.tech_cred, text=val)
            lb.place(relx=.318, rely=a, relh=g, relw=.682)
            self.tech_labels.append(lb)
            
            a += h

    def style(self):
        self.na.config(bg="blue", relief="solid")
        for a in [self.spec_cred, self.tech_cred]: a.config(bg=self.brc["Tue"], relief="ridge")
        c = 0
        f = self.spec_labels+self.tech_labels
        random.shuffle(f)
        for a in f:
            col = self.brcs[c%len(self.brc)]
            cl = self.brc[col]
            a.config(bg=cl, relief="groove")
            c += 1


    def place_widgs(self):
        self.na.place(relw=1, relh=.05)
        self.spec_cred.place(rely=.05, relw=1, relh=.45)
        self.tech_cred.place(rely=.5, relw=1, relh=.5)

