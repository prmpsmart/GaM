from .auths import Authorisation

# GUI counterpart

from prmp_gui.dialogs import *


def show_admin_required(): dialogFunc(title="ADMIN Required", msg="An ADMIN permission is required.", which="error")

def make_change(ordfunc=None, *args, **kwargs):
    if Authorisation.is_admin():
        if ordfunc: ordfunc()
        elif args:
            for func in args: func()
        elif kwargs:
            for func in kwargs:
                vals = kwargs[func]
                if vals == None: func()
                elif isinstance(vals, list): func(*vals)
                elif isinstance(vals, dict): func(**vals)
                else: func(vals)
        return True
    else:
        show_admin_required()
        return False



class Base_Password(PRMP_FillWidgets, Frame):
    
    def __init__(self, master, **kwargs):
        
        Frame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self)
        
        self.new_is_password = False
        self.old_is_password = False
        
        self.ent_usr = "Enter Your Username"
        self.ent_nusr = "Enter New Username"
        self.ent_pwd = "Enter Your Password"
        self.ent_npwd = "Enter New Password"
        self.ent_cpwd = "Confirm Your Password"
        self.ent_hint = "Your Password Hint"
        self.ent_name = "Enter Your Name"
        
        self.ent_new = ''
        self.ent_old = ''
        self.hint_text=''
        
        self.name = Entry(self, placeholder=self.ent_name, very=1)
        self.clr_name = Button(self, text="Clear", command=self.name.empty, relief="solid")
        
        self.username = Entry(self, placeholder=self.ent_usr, very=1)
        self.clr_usr = Button(self, text="Clear", command=self.username.empty, relief="solid")
        
        self.admin = Checkbutton(self, relief="solid", text="Admin?", command=self.admin_add)
        
        self.password = Entry(self, placeholder=self.ent_pwd, very=1)
        self.first = 0
        self.password.bind('<KeyPress>', self.show_star)
        
        self.old = Entry(self, very=1)
        self.clr_old = Button(self, text="Clear", command=self.old.empty, relief="solid")
        
        self.password_confirm = Label(self)
        
        self.password_length = Label(self, relief="sunken", bd=3)
        
        self.clr_pwd = Button(self, text="Clear", command=self.password.empty, relief="solid")
        
        self.new = Entry(self, very=1)
        self.clr_new = Button(self, text="Clear", command=self.new.empty, relief="solid")
        
        self.show_pass = Checkbutton(self, command=self.show_password, relief="solid", text="Show")
        
        self.show_old = Checkbutton(self, command=self.show_old_, relief="solid", text="Show")
        
        self.hint = Entry(self, very=0)
        
        self.clr_hint = Button(self, text="Clear", command=self.hint.empty, relief="solid")
        
        self.hx, self.hy, self.hh, self.hw, = .1, .43, .04, .5
        self.forgot_chk = Checkbutton(self, command=self.forgot_check, relief="solid", text="Forgot Password?")
        
        self.hint_lbl = Label(self, relief="groove")
        
        self.action = Button(self, text='Action', relief="solid", command=self.make_change)

        
        # self.init()
       
    def binds(self):
        # return
        if self.old_is_password: self.old.bind("<KeyRelease>", self.old_show_star)
        
        if self.new_is_password: self.new.bind("<KeyRelease>", self.new_show_star)


    def clear_password(self, *e):
        self.password.empty()
        self.pass_leave()
        self.show_norm()
        self.clear_new()
        if self.new_is_password:
            self.new_leave()
            self.new_show_norm()

    def admin_add(self):
        if Authorisation.is_admin(): return True
        else:
            self.admin.set('0')
            dialogFunc(title="ADMIN?", msg="Only an ADMIN can add another user", which="error")
            
    def clear_new(self, *e):
        self.new.set(self.ent_new)
        if self.new_is_password:
            self.new_leave()
            self.new_show_norm()
            
    def clear_old(self, *e):
        self.old.set(self.ent_old)
        if self.old_is_password:
            self.old_leave()
            self.old_show_norm()

    def show_hint(self):
        if self.forgot.get():
            self.hint_lbl.config(text=self.hint_text)
            self.hint_lbl.place(relx=self.hx, rely=self.hy, relh=self.hh, relw=self.hw)
        else: self.hint_lbl.place_forget()
    
    def show_password(self, *e):
        if self.show_pass.get():
            self.show_norm()
            if self.new_is_password: self.new_show_norm()
        else:
            self.show_star()
            if self.new_is_password: self.new_show_star()
    
    def show_old_(self, *e):
        if self.show_old.get():
            self.old_show_norm()
            if self.old_is_password: self.old_show_norm()
        else:
            self.old_show_star()
            if self.old_is_password: self.old_show_star()

    def confirm_password_correct(self):
        pwd, cpwd = self.password.get(), self.new.get()
        if pwd == cpwd: self.password_confirm.config(bg="green", text="CORRECT")
        else: self.password_confirm.config(bg="red", text="NOT CORRECT")
    
    def forgot_check(self):
        usr = self.get_username()
        if Authorisation.check_username(usr):
            hint = Authorisation.get_user_hint(usr)
            self.hint_text="Hint is %s"%hint if hint else "EMPTY"
            self.hint_lbl.config(text="Hint is %s"%hint)
            self.show_hint()
        
        else: self.informate("Incorrect Username", "Enter a correct username to check for hint", "info")

    def check_pass_length(self, e=0):
        pwd = self.password.get()
        if self.check_valid(pwd):
            text = ''
            length = len(pwd)
            bg = 'white'
            fg = None
            if length < 10:
                text = "Password too small in length"
                fg = "red"
            elif  10 <= length <= 15:
                text = "Mild Password"
                fg = "orange"
            elif 15 <= length <= 20:
                text = "Strong Password"
                fg = "green"
            else:
                text = "Password too long"
                fg = "red"
            
            self.password_length.config(text=text, fg=fg, bg=bg)

    def new_show_star(self, *e):
        if self.show_pass.get(): pass
        else: self.new.config(show='*')
        self.confirm_password_correct()
    def new_show_norm(self, *e): self.new.config(show='')

    def old_show_star(self, *e):
        if self.show_pass.get(): pass
        else: self.old.config(show='*')
    
    def old_show_norm(self, *e): self.old.config(show='')

    def show_star(self, *e):
        if e:
            if not self.first: self.first = 1
            else: return
        if self.show_pass.get(): pass
        else: self.password.config(show='*')
        self.check_pass_length()
        
    def show_norm(self, *e): self.password.config(show='')
    
    def check_valid(self, text):
        tests = [self.ent_usr, self.ent_nusr, self.ent_pwd, self.ent_cpwd, self.ent_hint, self.ent_name]
        for test in tests:
            if text == test: return False
        return True
    
    def check_valids(self, *txts):
        for txt in txts:
            if self.check_valid(txt) == False: return False
        return True
    
    def place_widgs(self): pass
    
    def get_inputs(self): pass
    
    def init(self):
        self.binds()
        self.place_widgs()
    
    def make_change(self):
        if Authorisation.is_admin(): self.act()
        else: show_admin_required()
    
    def act(self): pass
    
    # def load_data(self): Threads.load_passwords()
    
    # def save_data(self): Threads.save_passwords()

class Change_Username(Base_Password):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
    
        self.username.changePlaceholder(self.ent_usr)
        self.new.changePlaceholder(self.ent_nusr)

        self.action.config(text="Change Username")
        
        self.init()
        self.addResultsWidgets(['username', 'new', 'password'])
    
    def get_inputs(self):
        results = self.get()
        inputs = [results['username'], results['new'], results['password']]
        if self.check_valids(*inputs): return inputs
        
    def act(self):
        inputs = self.get_inputs()
        if inputs:
            old_usr, new_usr, pwd = inputs
            if Authorisation.check_username(new_usr):
                dialogFunc(title="User exists!", msg=f"User with username: {new_usr} already exists.", which="error")
                return
            user = Authorisation.get_user(old_usr, pwd)
            not_exist = Authorisation.not_exist(old_usr)
            if user == Authorisation.wrong_pass: dialogFunc(title="Wrong password", msg=f"Wrong password entered for User with username: {old_usr} ", which="error")
            elif user == not_exist: dialogFunc(title="User Doesn't Exist", msg=f"User with username: {old_usr} doesn't exist", which="error")
            else:
                if dialogFunc(title="Change Username Confirmation", msg=f"Are you sure to change the username for this  user with details\nName :{user.name}\nUsername: {old_usr}\nNew Username: {new_usr} ", which=1, ask=1):
                    Authorisation.change_username(old_usr, pwd, new_usr)
                    # self.save_data()
                    dialogFunc(title="Username change Successful", msg="Username change is successful", which="info")
        else: dialogFunc(title="Incorrect Input", msg="Make sure to enter the required inputs correctly", which="warn")

    def place_widgs(self):
        
        self.username.place(relx=.1, rely=.15, relh=.1, relw=.6)
        self.clr_usr.place(relx=.72, rely=.15, relh=.09, relw=.1)

        self.new.place(relx=.1, rely=.3, relh=.1, relw=.6)
        
        self.clr_new.place(relx=.72, rely=.3, relh=.09, relw=.1)
        
        self.password.place(relx=.1, rely=.45, relh=.1, relw=.6)
        self.clr_pwd.place(relx=.72, rely=.45, relh=.09, relw=.1)
        
        self.show_pass.place(relx=.84, rely=.45, relh=.09, relw=.15)

        self.action.place(relx=.1, rely=.78, relh=.09, relw=.8)

class Delete_User(Base_Password):
    
    def __init__(self, master=None, inh=False, **kwargs):
        super().__init__(master=master, **kwargs)
        
        self.action.config(text="Delete User")
        
        if not inh:
            self.init()
            self.addResultsWidgets(['username', 'password'])

    
    def get_inputs(self):
        results = self.get()
        inputs = [results['username'], results['password']]
        if self.check_valids(*inputs): return inputs
        
    def act(self):
        inputs = self.get_inputs()
        if inputs:
            usr, pwd = inputs
            user = Authorisation.get_user(usr, pwd)
            not_exist = Authorisation.not_exist(usr)
            if user == Authorisation.wrong_pass: dialogFunc(title="Wrong password", msg=f"Wrong password entered for User with username: {usr} ", which="error")
            elif user == not_exist: dialogFunc(title="User Doesn't Exist", msg=f"User with username: {usr} doesn't exist", which="error")
            elif user.super_user == True: dialogFunc(title="Super_User", msg=Authorisation.get_cant_super(), which="error")
            else:
                if dialogFunc(title="Delete User Confirmation", msg=f"Are you sure to delete User with details\nName :{user.name}\nUsername: {usr}", which=1, ask=1):
                    Authorisation.delete_user(usr, pwd)
                    # self.save_data()
                    dialogFunc(title="User Deleted Successful", msg=f"User:\nName: {user.name}\nUsername: {user.username}  is successful", which="info")
        else: dialogFunc(title="Incorrect Input", msg="Make sure to enter the required inputs correctly", which="warn")

    
    def place_widgs(self):
        
        self.username.place(relx=.1, rely=.15, relh=.1, relw=.6)
        self.clr_usr.place(relx=.72, rely=.15, relh=.09, relw=.1)

        self.password.place(relx=.1, rely=.3, relh=.1, relw=.6)
        
        self.clr_pwd.place(relx=.72, rely=.3, relh=.09, relw=.1)
        
        self.show_pass.place(relx=.84, rely=.3, relh=.09, relw=.15)

        self.action.place(relx=.1, rely=.5, relh=.08, relw=.8)

class Change_Password(Base_Password):
    
    def __init__(self, master=None, inh=False, **kwargs):
        super().__init__(master=master, **kwargs)
        self.new_is_password = True
        self.new.changePlaceholder(self.ent_cpwd)
        
        self.inh = inh
        if not self.inh:
            self.action.config(text="Change Password")
            self.old_is_password = True

            self.old.changePlaceholder(self.ent_pwd)
            self.password.changePlaceholder(self.ent_npwd)
            # self.new.changePlaceholder(self.ent_cpwd)
            self.password.bind('<KeyRelease>', self.check_pass_length, '+')
            self.hint.changePlaceholder(self.ent_hint)

            self.addResultsWidgets(['username', 'password', 'old', 'hint', 'new'])

            self.init()
    
    def get_inputs(self):
        results = self.get()
        inputs = [results['username'], results['old'], results['password'], results['new'], results['hint']]
        if self.check_valids(*inputs): return inputs
    
    def act(self):
        inputs = self.get_inputs()
        if inputs:
            username, old, new, conf, hint = inputs
            user = Authorisation.get_user(username, old)
            not_exist = Authorisation.not_exist(username)
            if user == Authorisation.wrong_pass: dialogFunc(title="Wrong password", msg="Wrong password entered for User with username: {username} ", which="error")
            elif user == not_exist: dialogFunc(title="User Not Exist", msg=f"User with username: {username} doesn't exist", which="error")
            else:
                if dialogFunc(title="Change Password Confirmation", msg=f"Are you sure to change the password for this  user with details\nName :{user.get_name()}\nUsername: {username}", which=1, ask=1):
                    Authorisation.change_password(username, old, new, hint)
                    self.save_data()
                    dialogFunc(title="Change Password Successful", msg=f"The password for User:\nName :{user.get_name()}\nUsername: {username}\n is changed successfully", which="info")
        else: dialogFunc(title="Incorrect Input", msg="Make sure to enter the required inputs correctly", which="warn")

    def place_widgs(self):
        if not self.inh:
            self.username.place(relx=.1, rely=.05, relh=.09, relw=.6)
            self.clr_usr.place(relx=.72, rely=.05, relh=.09, relw=.1)
            
            self.old.place(relx=.1, rely=.15, relh=.1, relw=.6)
            self.clr_old.place(relx=.72, rely=.15, relh=.09, relw=.1)
            self.show_old.place(relx=.84, rely=.15, relh=.09, relw=.15)
        
        self.password.place(relx=.1, rely=.3, relh=.1, relw=.6)
        
        self.clr_pwd.place(relx=.72, rely=.3, relh=.09, relw=.1)
        
        self.show_pass.place(relx=.84, rely=.3, relh=.09, relw=.15)
        
        self.password_length.place(relx=.1, rely=.405, relh=.05, relw=.6)
        
        self.new.place(relx=.1, rely=.47, relh=.1, relw=.6)
        
        self.password_confirm.place(relx=.72, rely=.48, relh=.08, relw=.23)

        self.hint.place(relx=.1, rely=.6, relh=.09, relw=.7)
        
        self.clr_hint.place(relx=.84, rely=.6, relh=.09, relw=.1)

        self.action.place(relx=.1, rely=.78, relh=.09, relw=.8)



class Add_User(Change_Password):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, inh=True, **kwargs)
        
        self.action.config(text="Add User")
        
        self.init()
    
    def get_inputs(self):
        inputs = [self.name.get(), self.username.get(), self.password.get(), self.new.get(), self.hint.get()]
        admin = True if self.admin.get() else False
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
        self.admin.place(relx=.84, rely=.15, relh=.09, relw=.15)
        self.name.place(relx=.1, rely=.05, relh=.09, relw=.6)
        self.clr_name.place(relx=.72, rely=.05, relh=.09, relw=.1)

        self.username.place(relx=.1, rely=.15, relh=.1, relw=.6)
        self.clr_usr.place(relx=.72, rely=.15, relh=.09, relw=.1)

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





class Login_Status(LabelFrame):
    # font = Fonts.font15b
    # logout_font = font
    
    def __init__(self, master=None):
        super().__init__(master=master, relief="solid")
        
        self.login_dets = Label(self, relief="solid", text=self.current_user())
        self.logout = Button(self, relief="solid", text="LOGOUT", command=self.logout_confirm)
        self.admin_dets = Label(self, relief="solid", text=Authorisation.get_current_user_permission())
        
        self.update_status()
        self.style()
        self.place_widgs()
    def current_user(self):
        user_text = "Current User : %s (%s) "
        user = Authorisation.get_current_user()
        subs = ()
        if not isinstance(user, str): subs = user.get_status()
        if len(subs) == 2: return user_text%subs
        else: return user
    
    def logout_confirm(self):
        if confirm("Logout Confirm", "Are you sure to LOGOUT?", 1): Authorisation.logout()
    
    def update_status(self):
        self.login_dets.config(text=self.current_user())
        self.admin_dets.config(text=Authorisation.get_current_user_permission())
        # print(Authorisation.get_current_user_permission())
        self.after(1000, self.update_status)
    
    def place_widgs(self):
        self.login_dets.place(relx=0, rely=0, relh=1, relw=.7)
        self.logout.place(relx=.7, rely=0, relh=1, relw=.1)
        self.admin_dets.place(relx=.8, rely=0, relh=1, relw=.2)
    def style(self):
        widgs = [self.login_dets, self.admin_dets, self]
        for widg in widgs: widg.config(bg=Styles.background, fg=Styles.foreground, font=self.font)
        self.logout.config(activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=self.logout_font, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor="white", justify="left", overrelief="ridge", relief="solid")

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
