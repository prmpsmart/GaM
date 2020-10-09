from tkinter import LabelFrame, Button
from .gui.tkinter.thrift_note import Thrift, Notebook, Frame, Styles


class AGAM(LabelFrame):
    go = 0
    def __init__(self, master):
        super().__init__(master)
        self.place(relx=0, rely=0, relh=1, relw=1)
        
        self.master = master

        self.WINDOWS = Notebook(self)
        self.WINDOWS.place(relx=.0, rely=0, relh=.998, relw=1)
        self.WINDOWS.config(takefocus="")
        self.WINDOWS.enable_traversal()
        
        self.home_page = Frame(self.WINDOWS)
        self.WINDOWS.add(self.home_page, padding=1)
        self.WINDOWS.tab(0, text="Home",compound="left",underline="0")

        self.thrift_page = Frame(self.WINDOWS)
        self.WINDOWS.add(self.thrift_page, padding=1)
        self.WINDOWS.tab(1, text="Thrift",compound="none",underline="0",)
        
        self.coop_page = Frame(self.WINDOWS)
        self.WINDOWS.add(self.coop_page, padding=1)
        self.WINDOWS.tab(2, text="Cooperative", compound="none", underline="0")
        # self.settings_page = Frame(self.WINDOWS,)
        # self.WINDOWS.add(self.settings_page, padding=1)
        # self.WINDOWS.tab(3, text="Settings", compound="none", underline="0")
        

        self.thrift = Thrift(self.thrift_page)
        self.style()
        

    def style(self):
        frames = [self.home_page, self.thrift_page, self.coop_page]
        for frame in frames: frame.config(highlightbackground=Styles.background, background=Styles.background, highlightcolor=Styles.foreground)
        self.thrift.style()
        
    def draw_charts(self):
        self.thrift.draw_charts()


