
from .base_password import Base_Password, Authorisation, show, confirm

class Delete_User(Base_Password):
    
    def __init__(self, master=None, inh=False):
        super().__init__(master=master)
        
        self.action.config(text="Delete User")
        
        if not inh: self.init()
    
    def get_inputs(self):
        inputs = [self.username.get(), self.password.get()]
        if self.check_valids(*inputs): return inputs
        
    def act(self):
        inputs = self.get_inputs()
        if inputs:
            usr, pwd = inputs
            user = Authorisation.get_user(usr, pwd)
            not_exist = Authorisation.not_exist(usr)
            if user == Authorisation.wrong_pass: show("Wrong password", f"Wrong password entered for User with username: {usr} ", "error")
            elif user == not_exist: show("User Doesn't Exist", f"User with username: {usr} doesn't exist", "error")
            elif user.super_user == True: show("Super_User", Authorisation.get_cant_super(), "error")
            else:
                if confirm("Delete User Confirmation", f"Are you sure to delete User with details\nName :{user.get_name()}\nUsername: {usr}", 1):
                    Authorisation.delete_user(usr, pwd)
                    self.save_data()
                    show("User Deleted Successful", f"User:\nName: {user.get_name()}\nUsername: {user.get_username()}  is successful", "info")
        else: show("Incorrect Input", "Make sure to enter the required inputs correctly", "warn")

    
    def place_widgs(self):
        
        self.username_ent.place(relx=.1, rely=.15, relh=.1, relw=.6)
        self.clr_usr.place(relx=.72, rely=.15, relh=.09, relw=.1)

        self.password_ent.place(relx=.1, rely=.3, relh=.1, relw=.6)
        
        self.clr_pwd.place(relx=.72, rely=.3, relh=.09, relw=.1)
        
        self.show_pass.place(relx=.84, rely=.3, relh=.09, relw=.15)

        self.action.place(relx=.1, rely=.5, relh=.08, relw=.8)
 