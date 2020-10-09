
from tkinter import Toplevel, Label
from .styles import Styles
import sys


class About(Toplevel):
    font = "-family {Times New Roman} -size 9 -weight bold"
    
    ab = '''AGAM ANALYSIS SOFTWARE, made\nfor easy analysing of AGAM accounts.\nIt contains every possible accounts\nof the company and can be easily extensible to cover\nmore accounts to be added in the nearest future \n\n__author__ = PRMP Smart\n__email__ = prmpsmart@gmail.com\n\nAGAM's Contact = 08136795920'''
    
    op = False


    def __init__(self, master=None):
        self._w = "self"
        if About.op == True: pass
        else:
            super().__init__(master)
            self.title("About")
            self["background"] = Styles.background
            self.attributes("-alpha", 1, "-disabled", False, "-toolwindow", True, "-topmost", True)
            self.wm_protocol("WM_DELETE_WINDOW", self.exiting)

            
            Label(self, text="About", bg="blue", relief="solid").pack(fill="x")
            Label(self, text=self.ab, bg="#17806D").pack(fill="both", expand=True)

            self.bind_all("<Return>", sys.exit)
            
            About.op = True
            self.mainloop()

    def exiting(self):
        About.op = False
        self.destroy()