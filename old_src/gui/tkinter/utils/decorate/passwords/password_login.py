
from .delete_user import Delete_User, Authorisation
from . import Out_Message, show
import sys

class Password_Login(Delete_User):
    def __init__(self, master=None, okay=None):
        super().__init__(master=master, inh=True)
        self.okay = okay
        self.hx, self.hy, self.hh, self.hw, = .1, .43, .09, .6
        self.hint_text = "Love You"
        self.action.config(text="Login", command=self.login_check)
        
        self.pass_count = 0
        
        self.message = Out_Message(self, head="Love", relx=.008, rely=.7, relh=.3, relw=.968)
        
        self.init()
    
    def style(self):
        super().style()
        self.message.style()
        
    
    def login_check(self):
        self.pass_count += 1
        if self.pass_count >= 3:
            self.informate("Incorrect Credentials and EXITING", "Too much unsuccessful logins exiting in 5 seconds", "info")
            self.root.after(5000, sys.exit)
        
        
        usr = self.get_username()
        pwd = self.get_password()
        if self.check_valids(usr, pwd):
            log = Authorisation.login(usr, pwd)
            if log == 1:
                self.informate("Correct Credentials", "Correct Password\nLogin Successful.", "info")
                self.pass_count = 0
                self.defaults()
                if self.okay: self.okay()
            elif log == 2: self.informate("Incorrect Credentials", "Wrong Password", "warn")
            else: self.informate("Incorrect Credentials", Authorisation.not_exist(usr), "error")
        else:  self.informate("Incorrect Credentials", "Enter valid credentials", "error")

    def defaults(self):
        super().defaults()
        self.forgot.set('0')
        self.show_hint()
        self.clear_username()
        self.clear_password()

    def informate(self, title='', msg='', which=''):
        self.message.set_message(msg)
        if which: show(title=title, msg=msg, which=which)

    
    def place_widgs(self):
        super().place_widgs()
        
        self.forgot_chk.place(relx=.72, rely=.43, relh=.09, relw=.27)
        
        self.action.place(relx=.1, rely=.6, relh=.08, relw=.8)
        
        self.message.place_widgs()


