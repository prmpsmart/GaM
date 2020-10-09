
from .base_password import Base_Password, Authorisation, show, confirm


class Change_Username(Base_Password):
    
    def __init__(self, master=None):
        super().__init__(master=master)
    
        self.ent_new = self.ent_nusr
        self.action.config(text="Change Username")
        
        self.init()
    
    def get_inputs(self):
        inputs = [self.username.get(), self.new.get(), self.password.get()]
        if self.check_valids(*inputs): return inputs
        
    def act(self):
        inputs = self.get_inputs()
        if inputs:
            old_usr, new_usr, pwd = inputs
            user = Authorisation.get_user(old_usr, pwd)
            not_exist = Authorisation.not_exist(old_usr)
            if user == Authorisation.wrong_pass: show("Wrong password", f"Wrong password entered for User with username: {old_usr} ", "error")
            elif user == not_exist: show("User Doesn't Exist", f"User with username: {old_usr} doesn't exist", "error")
            else:
                if confirm("Change Username Confirmation", f"Are you sure to change the username for this  user with details\nName :{user.get_name()}\nUsername: {old_usr}\nNew Username: {new_usr} ", 1):
                    Authorisation.change_username(old_usr, pwd, new_usr)
                    self.save_data()
                    show("Username change Successful", "Username change is successful", "info")
        else: show("Incorrect Input", "Make sure to enter the required inputs correctly", "warn")

    def place_widgs(self):
        
        self.username_ent.place(relx=.1, rely=.15, relh=.1, relw=.6)
        self.clr_usr.place(relx=.72, rely=.15, relh=.09, relw=.1)

        self.new_ent.place(relx=.1, rely=.3, relh=.1, relw=.6)
        
        self.clr_new.place(relx=.72, rely=.3, relh=.09, relw=.1)
        
        self.password_ent.place(relx=.1, rely=.45, relh=.1, relw=.6)
        self.clr_pwd.place(relx=.72, rely=.45, relh=.09, relw=.1)
        
        self.show_pass.place(relx=.84, rely=.45, relh=.09, relw=.15)

        self.action.place(relx=.1, rely=.78, relh=.09, relw=.8)







