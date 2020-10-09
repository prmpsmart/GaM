from .base_password import Base_Password, Authorisation, show, confirm


class Change_Password(Base_Password):
    
    def __init__(self, master=None, inh=False):
        super().__init__(master=master)
        self.new_is_password = True
        self.ent_new = self.ent_cpwd
        self.inh = inh
        if not self.inh:
            self.action.config(text="Change Password")
            self.old_is_password = True
            self.ent_old = self.ent_pwd
            self.ent_pwd = self.ent_npwd
            self.ent_new = self.ent_cpwd
            self.init()
    
    def get_inputs(self):
        inputs = [self.username.get(), self.old.get(), self.password.get(), self.new.get(), self.hint.get()]
        if self.check_valids(*inputs): return inputs
    
    def act(self):
        inputs = self.get_inputs()
        if inputs:
            username, old, new, conf, hint = inputs
            user = Authorisation.get_user(username, old)
            not_exist = Authorisation.not_exist(username)
            if user == Authorisation.wrong_pass: show("Wrong password", f"Wrong password entered for User with username: {username} ", "error")
            elif user == not_exist: show("User Not Exist", f"User with username: {username} doesn't exist", "error")
            else:
                if confirm("Change Password Confirmation", f"Are you sure to change the password for this  user with details\nName :{user.get_name()}\nUsername: {username}", 1):
                    Authorisation.change_password(username, old, new, hint)
                    self.save_data()
                    show("Change Password Successful", f"The password for User:\nName :{user.get_name()}\nUsername: {username}\n is changed successfully", "info")
        else: show("Incorrect Input", "Make sure to enter the required inputs correctly", "warn")


    def place_widgs(self):
        if not self.inh:
            self.username_ent.place(relx=.1, rely=.05, relh=.09, relw=.6)
            self.clr_usr.place(relx=.72, rely=.05, relh=.09, relw=.1)
            
            self.old_ent.place(relx=.1, rely=.15, relh=.1, relw=.6)
            self.clr_old.place(relx=.72, rely=.15, relh=.09, relw=.1)
            self.show_old.place(relx=.84, rely=.15, relh=.09, relw=.15)
        
        self.password_ent.place(relx=.1, rely=.3, relh=.1, relw=.6)
        
        self.clr_pwd.place(relx=.72, rely=.3, relh=.09, relw=.1)
        
        self.show_pass.place(relx=.84, rely=.3, relh=.09, relw=.15)
        
        self.password_length.place(relx=.1, rely=.405, relh=.05, relw=.6)
        
        self.new_ent.place(relx=.1, rely=.47, relh=.1, relw=.6)
        
        self.password_confirm.place(relx=.72, rely=.48, relh=.08, relw=.23)

        self.hint_ent.place(relx=.1, rely=.6, relh=.09, relw=.7)
        
        self.clr_hint.place(relx=.84, rely=.6, relh=.09, relw=.1)

        self.action.place(relx=.1, rely=.78, relh=.09, relw=.8)
