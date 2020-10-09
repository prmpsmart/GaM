
from tkinter import Frame, Button, StringVar, LabelFrame
from tkinter.ttk import Notebook
from ...widgets.twowidgets import Styles, Label, Checkbutton, Entry, Fonts

from ...widgets.debug import show, Out_Message, confirm
from .change_username import Change_Username, Authorisation
from .add_user import Change_Password, Add_User
from .password_login import Delete_User, Password_Login
from .login_status import Login_Status


class Password_Settings(Frame):
    
    def __init__(self, master):
        try: master = master.root
        except: pass
        super().__init__(master, bg=Styles.background, relief="solid")

        self.container = Notebook(self)
        
        Login_Status.font = Fonts.font9
        Login_Status.logout_font = Fonts.font8
        self.login_status = Login_Status(self)
        
        self.tab_count = 0
        
        self.password_login = Password_Login(self.container)
        
        self.add_user = Add_User(self.container)
        
        self.change_username = Change_Username(self.container)
        
        self.change_password = Change_Password(self.container)
        
        self.delete_user = Delete_User(self.container)
        

        self.add_wids_to_nb()
        self.place_widgs()
        
        
        
    def add_wids_to_nb(self):
        self.add_to_nb(self.password_login, "Password Login")
        self.add_to_nb(self.add_user, "Add User")
        self.add_to_nb(self.change_username, "Change Username")
        self.add_to_nb(self.change_password, "Change Password")
        self.add_to_nb(self.delete_user, "Delete User")
    
    def style(self):
        self.config(bg=Styles.background)
        widgs = [self.change_username, self.change_password, self.add_user, self.delete_user, self.password_login, self.login_status]
        for widg in widgs: widg.style()
        
    

    def add_to_nb(self, wid, name):
        self.container.add(wid, padding=1)
        self.container.tab(self.tab_count, text=name,compound="left",underline="0")
        self.tab_count += 1
        
    def place_widgs(self):
        self.place(relx=0, rely=0, relh=1, relw=1)
        
        self.login_status.place(relx=0, rely=0, relh=.1, relw=1)
        self.container.place(relx=0, rely=.1, relh=.9, relw=1)
