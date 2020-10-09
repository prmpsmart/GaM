
from . import Styles, LabelFrame, Label, Entry, Button, Fonts, Path
from .password_login import Password_Login, Authorisation
from ..images_tk.images_tk import Images_Tk

class Login(LabelFrame):
    def __init__(self, gui=None):
        self.gui = gui
        self.root = gui.root
        self.root.geometry(Styles.geometry)
        super().__init__(self.root, bg=Styles.background, relief="solid")
        
        self.container = Label(self, bg=Styles.background, relief="solid")
        
        self.login_img = Images_Tk.login()
        self.lo_img = self.login_img.img
        self.header = Label(self.container, background="yellow", image=self.lo_img)

        self.pass_login = Password_Login(self.container, self.okay)

        self.place_widgs()
        self.gui.show_gui()

    def okay(self): self.gui.load_gui()


    def place_widgs(self):
        self.place(relx=0, rely=0, relh=1, relw=1)
        self.container.place(relx=.3, rely=0, relh=1, relw=.4)
        self.header.place(relx=0, rely=0, relh=.26, relw=1)
        
        self.pass_login.place(relx=.05, rely=.35, relh=.63, relw=.9)




