
from tkinter import Label
from tkinter.ttk import Progressbar
from .images_tk.images_tk import Images_Tk, Images
from .passwords.login import Login, Authorisation
import time, sys

# Path.splash = "prmpsmart"

class Splash(Label):
    
    def __init__(self, gui, no=0):
        self.gui = gui
        self.root = gui.root
        self.image = Images_Tk.app()
        self.img = self.image.img
        
        self.geo = self.image.calc_geo(self.root) #splash logo
        
        self.bar_relx=.1
        self.bar_rely=.965
        self.bar_relh=.03
        self.bar_relw=.8

        self.root.overrideredirect(True)
        self.root.attributes("-alpha", 1, "-disabled", False, "-toolwindow", False, "-topmost", True)
        
        self.root.geometry(self.geo)

        super().__init__(self.root, image=self.img)
        self.place(relx=0, rely=0, relh=1, relw=1)
        
        self.bar = Progressbar(self, orient='horizontal', length=self.image.size[0]-20, mode='determinate')
        self.bar["maximum"] = 100
        self.bar.place(relx=self.bar_relx, rely=self.bar_rely, relh=self.bar_relh, relw=self.bar_relw)
        
        self.start_gui()
        
        self.after(10, self.run_bar)
        
        self.gone = 0
        self.count = 0
        self.time = 35
        
        # self.root.mainloop()
        
    def run_bar(self):
        self.bar["value"] = self.count%100
        self.count += 1
        self.bar.update()

        if self.gui.finished:
            self.bar.stop()
            self.bar = Label(self, text="Finished Loading")
            self.bar.place(relx=.1, rely=.83, relh=.1, relw=.8)
            
            self.root.withdraw()
            if not Authorisation.logged_in(): self.password = Login(self.gui)
            else: self.gui.load_gui()
            
        else: self.after(self.time, self.run_bar)
    
    def stop(self, *a): sys.exit()
    
    def start_gui(self):
        from threading import Thread
        self.thread = Thread(target=self.gui.startup)
        self.thread.start()
        # self.thread.join()





