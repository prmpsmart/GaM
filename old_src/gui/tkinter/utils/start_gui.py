from tkinter import Tk, Menu
from .decorate.settings import Settings, Path, Threads, TData, Styles
from .decorate.splash import Splash
from ....backend.utils.prmp_reloader import Reloader, os, sys
# from tkinter.ttk import Menubutton
from .widgets.debug import confirm, show
from .widgets.admin_req import make_change
from ..thrift_note import Thrift
from .decorate.about import About
from .decorate.images_tk.images_tk import Images_Tk
from .decorate.credits import Credits
from .decorate.passwords.login_status import Login_Status
import sys, time


class Gui(Reloader):
    states = {"n":"normal", "i":"iconic", "w":"withdrawn", "z":"zoomed"}
    
    state = states['n']
    
    def __init__(self, child, reload_=False):
        self.finished = False
        self.full = False
        self.unload_child = child
        if reload_:
            if os.environ.get("PRMP_TK"): self.start()
            else: self.reload(self.start)
        else: self.start()
    
    def __str__(self): return self.title
    
    def start(self):
        TData.load_other_datas()
        self.root = Tk()
        self.bind()

        self._style = Styles(self.root)
        self._style.set_default()

        self.splash = Splash(self, 1)
        
        self.lower_it = 1
        self.finished = False
        self.root.mainloop()
    
    def load_globals(self):
        TData.load_data()
        while TData.loaded != True: pass

    def startup(self):
        self.load_globals()
        self.title = "AGAM ANALYSIS SOFTWARE"
        self.login_status = Login_Status(self.root)
        self.child = self.unload_child(self.root)
        self.settings = None
        self.style()
        
        self.finished = True
    
    def load_gui(self):
        self.root.withdraw()
        self.root.overrideredirect(False)
        self.splash.place_forget()
        try: self.splash.password.place_forget()
        except: pass
        self.root.iconify()
        
        self.root.attributes("-alpha", 1, "-disabled", False, "-toolwindow", False, "-topmost", False)
        self.root.wm_protocol("WM_DELETE_WINDOW", self.exiting)
        
        try:
            self.root.iconbitmap(Images_Tk.get_ico('b'))
            TData.delete_junks()
        except Exception as e: print(e)
        
        self.root.after(2000, self.load_child)
        

    def load_child(self):
        self.root.title(self.title)
        self.set_menu()
        self.login_status.place(relx=0, rely=0, relh=.05, relw=1)
        self.child.draw_charts()
        self.child.place_widgs()
        
        ### Workaround for Thrift before making of Cooperative
        self.child.place(relx=0, rely=.05, relh=.95, relw=1)
        
        self.show_gui()
    
    def show_gui(self):
        self.root.state(self.states['n'])
        self.root.geometry(Styles.geometry)
        self.root.state(self.states['w'])
        # time.sleep(1)
        self.root.after_idle(self.root.deiconify)

    def load(self):
        if TData.loaded:
            if confirm("LOADED", "Data is already loaded.\n Do you want to reload?", 1):
                TData.loaded = False
                Threads.load_data()
        else: Threads.load_data()
    
    def set_menu(self):
        
        themes = sorted(self._style.themes)
        menubar = Menu(self.root, tearoff=0)
        
        self.root["menu"] = menubar
        self.root.option_add("*tearOff", False)
        menu_style = Menu(menubar, tearoff=0)
        for theme in themes: menu_style.add_radiobutton(label=theme.title(), command=lambda theme=theme: self._style.change_style(theme, func=self.style))
        
        menubar.add_command(label="Window", command=self.lower)
        menubar.add_cascade(menu=menu_style, label="Styles")
        menubar.add_command(label="Load Data", command=self.load)
        menubar.add_command(label="Save Data", command=self.save)
        menubar.add_command(label="Settings", command=self.show_settings)
        menubar.add_command(label="Credits", command=lambda: Credits(self.root))
        menubar.add_command(label="About", command=lambda: About(self.root))
    
    def bind(self):
        self.root.bind_all("<Control-q>", self.exiting)
        self.root.bind_all("<Control-Q>", self.exiting)
        self.root.bind_all("<Control-f>", self.fullscreen)
        self.root.bind_all("<Control-F>", self.fullscreen)
        self.root.bind_all("<Control-R>", self.reloader)
        self.root.bind_all("<Control-r>", self.reloader)
        self.root.bind_all("<Control-/>", self.raw_exit)
    
    def fullscreen(self, e):
        if self.full:
            self.root.state(self.states['n'])
            self.full = False
        else:
            self.root.state(self.states['z'])
            self.full = True

    def exiting(self, e=None):
        self.root.withdraw()
        if confirm(title="Exit", msg=f"Are you sure you want to exit\n {self.title}", num=1):
            self.root.quit()# self.root.destroy()
            TData.save_data()
            TData.delete_junks()
            sys.exit(0)
        else: self.root.state(self.state)
    
    def raw_exit(self, *a):
        try:  self.root.tk.call('destroy', self.root._w)
        except Exception as e: print(e)

    def lower(self):
        if self.lower_it:
            self.root.attributes("-topmost", True, "-toolwindow", True,)
            self.lower_it = 0
        else:
            self.root.attributes("-topmost", False, "-toolwindow", False,)
            self.lower_it = 1

    def save(self): make_change(self._save)
    
    def _save(self):
        if TData.going == True: show(title="In Progress", msg="Loading in progress", which="warn")
        else:
            if confirm("SAVING", "Are you sure you want to save your data?", 1): Threads.save_data()
    
    def show_settings(self): make_change(self._show_settings)
        
    def _show_settings(self):
        self.settings = Settings(self.root)
        self.settings.mainloop()

    def style(self):
        self.root.config(background=Styles.background)
        self.child.style()
        self.login_status.style()
        if self.settings: self.settings.style()

        Threads.save_other_datas()


