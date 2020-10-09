

from .change_password import Change_Password, Authorisation, show, confirm

class Add_User(Change_Password):
    
    def __init__(self, master=None):
        super().__init__(master=master, inh=True)
        
        self.action.config(text="Add User")
        
        self.init()
    
    def get_inputs(self):
        inputs = [self.name.get(), self.username.get(), self.password.get(), self.new.get(), self.hint.get()]
        admin = True if self.admin.get() == '1' else False
        if self.check_valids(*inputs): return [*inputs, admin]
        
    def act(self):
        if not self.admin_add(): return
        inputs = self.get_inputs()
        if inputs:
            name, username, password, confirm_password, hint, admin = inputs
            admin = Authorisation.get_permission(admin)[1]
            if password != confirm_password:
                show("Unmatch", "The passwords are not matching", "warn")
                return
            if confirm("Add User Confirmation", f"Are you sure to add user with details\nName :{name}\nUsername: {username}\nHint for Password: {hint}\nPermission: {admin} ", 1):
                del inputs[3]
                add = Authorisation.add_user(*inputs)
                if add == Authorisation.added:
                    self.save_data()
                    show("Add Successful", f"User: {name}\nUsername: {username}\nis added SUCCESSFULLY ", "info")
                    self.defaults()
                else: show("Add ERROR", add, "error")
        else: show("Incorrect Input", "Make sure to enter the required inputs correctly", "warn")

    def place_widgs(self):
        super().place_widgs()
        self.admin_chk.place(relx=.84, rely=.15, relh=.09, relw=.15)
        self.name_ent.place(relx=.1, rely=.05, relh=.09, relw=.6)
        self.clr_name.place(relx=.72, rely=.05, relh=.09, relw=.1)

        self.username_ent.place(relx=.1, rely=.15, relh=.1, relw=.6)
        self.clr_usr.place(relx=.72, rely=.15, relh=.09, relw=.1)
        
