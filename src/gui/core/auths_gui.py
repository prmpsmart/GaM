from ...utils.auths import Authorisation

# GUI counterpart

from .gam_dialogs import *
from .gam_images import GAM_PNGS



def show_admin_required(): PRMP_MsgBox(title="ADMIN Required", msg="An ADMIN permission is required, and any changes would not be saved.", _type="error", ask=0)

def make_change(ordfunc=None, *args, silent=0, **kwargs):
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
        if not silent: show_admin_required()
        return False



class Base_Password(PRMP_FillWidgets, Frame):
    
    def __init__(self, master, req=1, **kwargs):
        
        Frame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self)
        
        self.req = req
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
        
        self.password_length = Label(self, relief="sunken", bd=2, font='PRMP_FONT')
        
        self.clr_pwd = Button(self, text="Clear", command=self.password.empty, relief="solid")
        
        self.new = Entry(self, very=1)
        self.clr_new = Button(self, text="Clear", command=self.new.empty, relief="solid")
        
        self.show_pass = Checkbutton(self, command=self.show_password, relief="solid", text="Show")
        
        self.show_old = Checkbutton(self, command=self.show_old_, relief="solid", text="Show")
        
        self.hint = Entry(self, very=0)
        
        self.clr_hint = Button(self, text="Clear", command=self.hint.empty, relief="solid")
        
        self.hx, self.hy, self.hh, self.hw, = .1, .57, .04, .5
        self.forgot_chk = Checkbutton(self, command=self.forgot_check, relief="solid", text="Forgot Password?")
        
        self.hint_lbl = Label(self, relief="flat")
        
        self.action = Button(self, text='Action', relief="solid", command=self.make_change)
       
    def binds(self):
        # self.bind_all('<Return>', self.make_change)
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
            PRMP_MsgBox(title="ADMIN?", msg="Only an ADMIN can add another user", which="error", ask=0)
            
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
        if self.forgot_chk.get():
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
        usr = self.username.get()
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
    
    def make_change(self, e=0):
        if self.req: make_change(self.act)
        else: self.act()
    
    def act(self): pass


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
                PRMP_MsgBox(self, title="User exists!", msg=f"User with username: {new_usr} already exists.", _type="error")
                return
            user = Authorisation.get_user(old_usr, pwd)
            not_exist = Authorisation.not_exist(old_usr)
            if user == Authorisation.wrong_pass: PRMP_MsgBox(self, title="Wrong password", msg=f"Wrong password entered for User with username: {old_usr} ", _type="error")
            elif user == not_exist: PRMP_MsgBox(self, title="User Doesn't Exist", msg=f"User with username: {old_usr} doesn't exist", _type="error")
            else: PRMP_MsgBox(self, title="Change Username Confirmation", msg=f"Are you sure to change the username for this  user with details\nName :{user.name}\nUsername: {old_usr}\nNew Username: {new_usr} ", which=1, callback=self._act)
                    
        else: PRMP_MsgBox(self, title="Incorrect Input", msg="Make sure to enter the required inputs correctly", _type="warn")
    
    def _act(self, w):
        if w:
            self.emptyWidgets()
            Authorisation.change_username(*self.get_inputs())
            PRMP_MsgBox(self, title="Username change Successful", msg="Username change is successful", _type="info")

    def place_widgs(self):
        self.username.place(relx=.1, rely=.1, relh=.15, relw=.6)
        self.clr_usr.place(relx=.72, rely=.1, relh=.14, relw=.09)

        self.new.place(relx=.1, rely=.3, relh=.15, relw=.6)
        self.clr_new.place(relx=.72, rely=.3, relh=.14, relw=.09)
        
        self.password.place(relx=.1, rely=.5, relh=.15, relw=.6)
        self.clr_pwd.place(relx=.72, rely=.5, relh=.14, relw=.09)
        
        self.show_pass.place(relx=.84, rely=.5, relh=.14, relw=.11)

        self.action.place(relx=.1, rely=.8, relh=.14, relw=.8)

class Delete_User(Base_Password):
    
    def __init__(self, master=None, inh=False, **kwargs):
        super().__init__(master=master, **kwargs)
        
        self.action.config(text="Delete User")
        self.addResultsWidgets(['username', 'password'])
        
        if not inh:
            self.init()
    
    def get_inputs(self):
        results = self.get()
        inputs = [results['username'], results['password']]
        if self.check_valids(*inputs): return inputs
        
    def act(self):
        inputs = self.get_inputs()
        if inputs:
            usr, pwd = inputs
            self._user = user = Authorisation.get_user(usr, pwd)
            not_exist = Authorisation.not_exist(usr)
            if user == Authorisation.wrong_pass: PRMP_MsgBox(self, title="Wrong password", msg=f"Wrong password entered for User with username: {usr} ", _type="error")
            elif user == not_exist: PRMP_MsgBox(self, title="User Doesn't Exist", msg=f"User with username: {usr} doesn't exist", _type="error")
            elif user.super_user == True: PRMP_MsgBox(self, title="Super_User", msg=Authorisation.get_cant_super(), _type="error")
            else: PRMP_MsgBox(title="Delete User Confirmation", msg=f"Are you sure to delete User with details\nName :{user.name}\nUsername: {usr}", which=1, callback=self._act)

        else: PRMP_MsgBox(self, title="Incorrect Input", msg="Make sure to enter the required inputs correctly", _type="warn")
    
    def _act(self, w):
        if w:
            user = self._user
            self.emptyWidgets()
            Authorisation.delete_user(*self.get_inputs())
            PRMP_MsgBox(self, title="User Deleted Successful", msg=f"User:\nName: {user.name}\nUsername: {user.username}  is successful", _type="info")


    def place_widgs(self):
        self.username.place(relx=.1, rely=.1, relh=.15, relw=.6)
        self.clr_usr.place(relx=.72, rely=.1, relh=.14, relw=.09)

        self.password.place(relx=.1, rely=.35, relh=.15, relw=.6)
        self.clr_pwd.place(relx=.72, rely=.35, relh=.14, relw=.09)
        self.show_pass.place(relx=.84, rely=.35, relh=.14, relw=.11)

        self.action.place(relx=.1, rely=.8, relh=.14, relw=.8)

class Change_Password(Base_Password):
    
    def __init__(self, master=None, inh=False, **kwargs):
        super().__init__(master=master, **kwargs)
        self.new_is_password = True
        self.new.changePlaceholder(self.ent_cpwd)
        self.password.bind('<KeyRelease>', self.check_pass_length, '+')
        
        self.inh = inh
        if not self.inh:
            self.action.config(text="Change Password")
            self.old_is_password = True

            self.old.changePlaceholder(self.ent_pwd)
            self.password.changePlaceholder(self.ent_npwd)
            # self.new.changePlaceholder(self.ent_cpwd)
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
            self._user = user = Authorisation.get_user(username, old)
            not_exist = Authorisation.not_exist(username)
            if user == Authorisation.wrong_pass: PRMP_MsgBox(self, title="Wrong password", msg="Wrong password entered for User with username: {username} ", _type="error")
            elif user == not_exist: PRMP_MsgBox(self, title="User Not Exist", msg=f"User with username: {username} doesn't exist", _type="error")
            else: PRMP_MsgBox(title="Change Password Confirmation", msg=f"Are you sure to change the password for this  user with details\nName :{user.name}\nUsername: {username}", which=1, callback=self._act)
        else: PRMP_MsgBox(self, title="Incorrect Input", msg="Make sure to enter the required inputs correctly", _type="warn")
    
    def _act(self, w):
        if w:
            username, old, new, conf, hint = self.get_inputs()
            user = self._user
            self.emptyWidgets()
            
            Authorisation.change_password(username, old, new, hint)

            PRMP_MsgBox(self, title="Change Password Successful", msg=f"The password for User:\nName :{user.name}\nUsername: {user.username}\n is changed successfully", _type="info")


    def place_widgs(self):
        if not self.inh:
            self.username.place(relx=.1, rely=.05, relh=.12, relw=.6)
            self.clr_usr.place(relx=.72, rely=.05, relh=.11, relw=.09)
            
            self.old.place(relx=.1, rely=.2, relh=.12, relw=.6)
            self.clr_old.place(relx=.72, rely=.2, relh=.11, relw=.09)
            self.show_old.place(relx=.84, rely=.2, relh=.11, relw=.11)
        
        self.password.place(relx=.1, rely=.35, relh=.12, relw=.6)
        self.clr_pwd.place(relx=.72, rely=.35, relh=.11, relw=.09)
        self.show_pass.place(relx=.84, rely=.35, relh=.11, relw=.11)
        
        self.password_length.place(relx=.1, rely=.485, relh=.1, relw=.6)
        
        self.new.place(relx=.1, rely=.63, relh=.11, relw=.6)
        
        self.password_confirm.place(relx=.72, rely=.632, relh=.1, relw=.23)

        self.hint.place(relx=.1, rely=.76, relh=.09, relw=.6)
        self.clr_hint.place(relx=.72, rely=.76, relh=.09, relw=.09)

        self.action.place(relx=.1, rely=.87, relh=.12, relw=.8)


class Add_User(Change_Password):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, inh=True, **kwargs)
        
        self.action.config(text="Add User")
        self.addResultsWidgets(['username', 'password', 'name', 'hint', 'new', 'admin'])
        
        self.init()
    
    def get_inputs(self):
        results = self.get()
        inputs = [results['name'], results['username'], results['password'], results['new'], results['hint'], results['admin']]
        if self.check_valids(*inputs): return inputs
        
    def act(self):
        if not self.admin_add(): return
        inputs = self.get_inputs()
        if inputs:
            name, username, password, confirm_password, hint, admin = inputs
            admin = Authorisation.get_permission(admin)[1]
            if password != confirm_password:
                PRMP_MsgBox(self, title="Unmatch Passwords!", msg="The passwords are not matching", _type="warn")
                return
            
            PRMP_MsgBox(title="Add User Confirmation", msg=f"Are you sure to add user with details\nName :{name}\nUsername: {username}\nHint for Password: {hint}\nPermission: {admin} ", which=1, callback=self._act)

        else: PRMP_MsgBox(self, title="Incorrect Input", msg="Make sure to enter the required inputs correctly", _type="warn")
    
    def _act(self, w):
        if w:
            name, username, password, confirm_password, hint, admin = self.get_inputs()

            add = Authorisation.add_user(name, username, password, hint, admin)
            if add[0] == Authorisation.added:
                add = Authorisation.decify(add[0])
                self.emptyWidgets()
                
                self.password_confirm.config(text='')
                self.password_length.config(text='')

                PRMP_MsgBox(self, title="Add Successful", msg=f"User: {name}\nUsername: {username}\nis added SUCCESSFULLY ")
                self.emptyWidgets()
            else: PRMP_MsgBox(self, title="Add ERROR", msg=add, _type="error")

    def place_widgs(self):
        super().place_widgs()

        self.name.place(relx=.1, rely=.05, relh=.12, relw=.6)
        self.clr_name.place(relx=.72, rely=.05, relh=.11, relw=.09)

        self.username.place(relx=.1, rely=.2, relh=.12, relw=.6)
        self.clr_usr.place(relx=.72, rely=.2, relh=.11, relw=.09)
        self.admin.place(relx=.84, rely=.2, relh=.11, relw=.14)

class User_Login(Delete_User):
    def __init__(self, master=None, callback=None, **kwargs):
        super().__init__(master=master, inh=True, req=0, **kwargs)

        self.callback = callback

        self.hx, self.hy, self.hh, self.hw, = .1, .6, .12, .6
        self.hint_text = "Love You"

        self.action.config(text="Login")
        
        self.pass_count = 0
        
        self.init()
    
    def make_change(self, e=0):
        print(e)
        if e:
            children = list(self.children.keys())
            child = str(e.widget).split('.')[-1]
            if child not in children: return

            if not isinstance(e.widget, str) and (e.widget.toplevel == self.toplevel): super().make_change()
        else: super().make_change()
    
    def act(self):
        self.pass_count += 1
        
        if self.pass_count >= 3:
            self.after(2000, os.sys.exit)
            self.informate("Incorrect Credentials and EXITING", "Too much unsuccessful logins exiting in 5 seconds", "info", delay=5000)
        
        res = self.get(['username', 'password'])
        usr = res['username']
        pwd = res['password']

        if self.check_valids(usr, pwd):
            log = Authorisation.login(usr, pwd)
            if log == 1:
                self.emptyWidgets(['username', 'password'])
                self.pass_count = 0

                if self.callback: self.after(1000, self.callback)
                
                PRMP_MsgBox(title="Correct Credentials", msg="Correct Password\nLogin Successful.", which="info")

            elif log == 2: self.informate("Incorrect Credentials", "Wrong Password", "warn")
            else: self.informate("Incorrect Credentials", Authorisation.not_exist(usr), "error")
        else:  self.informate("Incorrect Credentials", "Enter valid credentials", "error")

    def informate(self, title='', msg='', which='', **kwargs):
        PRMP_MsgBox(title=title, msg=msg,_type=which, ask=0, **kwargs)
    
    def place_widgs(self):
        super().place_widgs()
        self.forgot_chk.place(relx=.72, rely=.6, relh=.12, relw=.27)


class Login_Status(LabelFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, relief="solid", **kwargs)
        
        self.login_dets = Label(self, relief="solid", text=self.current_user(), place=dict(relx=0, rely=0, relh=1, relw=.6))
        self.logout = Button(self, relief="solid", text="LOGOUT", command=self.logout_confirm, place=dict(relx=.6, rely=0, relh=1, relw=.2))
        self.admin_dets = Label(self, relief="solid", text=Authorisation.get_current_user_permission(), place=dict(relx=.8, rely=0, relh=1, relw=.2))
        
        self.update_status()

    def current_user(self):
        user_text = "%s (%s) "
        user = Authorisation.get_current_user()
        subs = ()
        if not isinstance(user, str): subs = user.status
        if len(subs) == 2: return user_text%subs
        else: return user
    
    def logout_confirm(self):
        PRMP_MsgBox(self, title="Logout Confirm", msg="Are you sure to LOGOUT?", ask=1, callback=self._logout_confirm)

    def _logout_confirm(self, w):
        if w: Authorisation.logout()
    
    def update_status(self):
        self.login_dets.config(text=self.current_user())
        self.admin_dets.config(text=Authorisation.get_current_user_permission())
        # print(Authorisation.get_current_user_permission())
        self.after(1000, self.update_status)

class Security_Settings(Frame): 
    
    def __init__(self, master, **kwargs):
        super().__init__(master, relief="solid", **kwargs)
        self.container = Notebook(self)
        self.login_status = Login_Status(self)
        self.tab_count = 0
        self.user_login = User_Login(self.container)
        self.add_user = Add_User(self.container)
        self.change_username = Change_Username(self.container)
        self.change_password = Change_Password(self.container)
        self.delete_user = Delete_User(self.container)
        
        self.add_wids_to_nb()
        self.place_widgs()
        # self.bell()
    
    def add_wids_to_nb(self):
        self.add_to_nb(self.user_login, "User Login")
        self.add_to_nb(self.add_user, "Add User")
        self.add_to_nb(self.change_username, "Change Username")
        self.add_to_nb(self.change_password, "Change Password")
        self.add_to_nb(self.delete_user, "Delete User")

    def add_to_nb(self, wid, name):
        self.container.add(wid, padding=1)
        self.container.tab(self.tab_count, text=name,compound="left",underline="0")
        self.tab_count += 1
        
    def place_widgs(self):
        self.place(relx=0, rely=0, relh=1, relw=1)
        self.login_status.place(relx=0, rely=0, relh=.1, relw=1)
        self.container.place(relx=0, rely=.1, relh=.9, relw=1)


class Security(GaM_Dialog):
    def __init__(self, master=None, geo=(600, 500), title='GaM Security', **kwargs): super().__init__(master, geo=geo, title=title, **kwargs)
    
    def _setupDialog(self): Security_Settings(self.container, place=dict(relx=.005, rely=.005, relh=.99, relw=.99))

class Login(GaM_Dialog):
    def __init__(self, master=None, title='GaM Login.', **kwargs): super().__init__(master, title=title, **kwargs)
        
    def _setupDialog(self):
        self.header = PRMP_ImageLabel(self.container, imageKwargs=dict(base64=GAM_PNGS['gam']), background="yellow", normal=1, config=dict(relief='solid'), resize=(500, 110), place=dict(relx=.005, rely=.005, relh=.26, relw=.99))

        self.pass_login = User_Login(self.container, callback=self._callback, place=dict(relx=.05, rely=.35, relh=.63, relw=.9))

    def _callback(self):
        if self.callback: self.callback(self.destroy)



