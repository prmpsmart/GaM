from ...utils.auths import Authorisation

# GUI counterpart

from .gam_dialogs import *
from .gam_images import GaM_PNGS
from prmp_lib.prmp_gui.tushed_widgets import LoginEntry
from prmp_lib.prmp_gui.imagewidgets import PRMP_ImageSLabel, PRMP_ImageCheckbutton


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
        if len(subs) == 2: return user.username
        # if len(subs) == 2: return user_text%subs
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


class LoginFrame(SLabel):
    colored = 0

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.after(100, self.load)
    
    def load(self):
        res = self.width, self.height
        self.image = PRMP_Image('purple_beau', inbuilt=1, resize=res, for_tk=1, inExt='jpeg')
        # self.create_image(0, 0, image=self.image)
        self['image'] = self.image
        if not LoginFrame.colored:
            self.master.toplevel.change_color(self.image.image)
            LoginFrame.colored = 1



class Base_Password(PRMP_FillWidgets, PRMP_ClassMixins):
    dic = dict(inbuilt=1, resize=(20, 20), for_tk=1)

    def __str__(self): return str(self.frame)

    def __init__(self, master, req=1, container=None, **kwargs):

        PRMP_FillWidgets.__init__(self) 
        self.frame = master if container else LoginFrame(master, **kwargs)

        self.req = req
        
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
    
    def loadWidgets(self):
        widgets = self.resultsWidgets

        if 'name' in widgets: self.name = LoginEntry(self.frame, entryKwargs=dict(placeholder=self.ent_name), required=1, show='', font=15)

        if 'username' in widgets: self.username = LoginEntry(self.frame, entryKwargs=dict(placeholder=self.ent_usr), required=1, show='', font=15, positions=(.8, .1, 0, .1, 0), _pass=self.check_username)

        if 'admin' in widgets: self.admin = PRMP_ImageCheckbutton(self.frame, text="Admin?", command=self.admin_add, highlightable=9, compound='left', imageKwargs=dict(prmpImage='blue_admin', inbuilt=1, resize=(23, 23)))

        if 'password' in widgets: self.password = LoginEntry(self.frame, entryKwargs=dict(placeholder=self.ent_pwd, required=1), font=15, positions=(.7, 0, .1, .1, .1))

        if 'old' in widgets: self.old = LoginEntry(self.frame, entryKwargs=dict(required=1), font=15, positions=(.9, 0, 0, .1, 0))

        if 'new' in widgets: self.new = LoginEntry(self.frame, entryKwargs=dict(required=1), font=15)

        if 'hint' in widgets: self.hint = Entry(self.frame, required=0)

        if 'forgot_chk' in widgets: self.forgot_chk = Checkbutton(self.frame, command=self.forgot_check, relief="solid", text="Forgot Password?")

        if 'hint_lbl' in widgets: self.hint_lbl = Label(self.frame, relief="flat")

        self.first = 0
        self.load()
        self.place_widgs()

    def load(self): pass

    def rx_rw(self, rw):
        rx = (1-rw)/2
        return rx, rw

    def check_username(self, usr): return 2 if Authorisation.check_username(usr) else 0
    
    def check_password(self, pwd):
        usr = self.username.get()
        o = Authorisation.check_user(usr, pwd)
        if o == 1: return 2

    def admin_add(self):
        if Authorisation.is_admin(): return True
        else:
            self.admin.set('0')
            PRMP_MsgBox(title="ADMIN?", msg="Only an ADMIN can add another user", which="error", ask=0)

    def hintplace(self):
        pass
    
    def show_hint(self):
        if self.forgot_chk.get():
            self.hint_lbl.set(self.hint_text)
            self.hintplace()
        else: self.hint_lbl.place_forget()

    def forgot_check(self):
        usr = self.username.get()
        if Authorisation.check_username(usr):
            hint = Authorisation.get_user_hint(usr)
            self.hint_text="Hint is %s"%hint if hint else "EMPTY"
            self.hint_lbl.config(text="Hint is %s"%hint)
            self.show_hint()

        else: self.informate("Incorrect Username", "Enter a correct username to check for hint", "info")

    def check_pass_length(self, text):
        if self.check_valid(text):
            length = len(text)

            if  6 <= length <= 10: return 1
            elif 10 <= length <= 15: return 2
            else: return 0

    def confirm_password_correct(self, text):
        pwd = self.password.get()
        if pwd == text:
            return self.check_pass_length(pwd)
        else: return 0

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

    def make_change(self, e=0):
        if self.req: make_change(self.act)
        else: self.act()

    def act(self): pass


class User_Login(Base_Password):
    def __init__(self, master=None, callback=None, **kwargs):
        self.callback = callback
        self.hint_text = "Love You"
        self.pass_count = 0
        super().__init__(master=master, req=0, **kwargs)
        self.addResultsWidgets(['hint_lbl', 'password', 'username', 'forgot_chk'])
        self.loadWidgets()

    def load(self):
        self.password.load((.6, .1, .1, .1, .1), 1)
        self.password.setAction(self.act, self.check_password)
    
    def hintplace(self):
        rw = .75
        rx = (1-rw)/2
        rrw = .6*rw
        self.hint_lbl.place(relx=rx, rely=.65, relh=.09, relw=rrw-.05)

    def place_widgs(self):
        rx, rw = self.rx_rw(.75)
        self.username.place(relx=rx, rely=.3, relh=.09, relw=rw)
        self.password.place(relx=rx, rely=.5, relh=.09, relw=rw)

        rrx = rx+(.6*rw)
        rrw = .4*rw
        self.forgot_chk.place(relx=rrx, rely=.65, relh=.09, relw=rrw)

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
            self.username.after(2000, os.sys.exit)
            self.informate("Incorrect Credentials and EXITING", "Too much unsuccessful logins exiting in 5 seconds", "info", delay=5000)

        res = self.get(['username', 'password'])
        usr = res['username']
        pwd = res['password']

        if self.check_valids(usr, pwd):
            log = Authorisation.login(usr, pwd)
            if log == 1:
                self.emptyWidgets(['username', 'password'])
                self.pass_count = 0

                if self.callback: self.frame.after(1000, self.callback)

                PRMP_MsgBox(title="Correct Credentials", msg="Correct Password\nLogin Successful.", which="info")

            elif log == 2: self.informate("Incorrect Credentials", "Wrong Password", "warn")
            else: self.informate("Incorrect Credentials", Authorisation.not_exist(usr), "error")
        else:  self.informate("Incorrect Credentials", "Enter valid credentials", "error")

    def informate(self, title='', msg='', which='', **kwargs):
        PRMP_MsgBox(title=title, msg=msg,_type=which, ask=0, **kwargs)


class Add_User(Base_Password):

    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.addResultsWidgets(['username', 'password', 'name', 'hint', 'new', 'admin'])
        self.loadWidgets()
    
    def load(self):
        self.name.load((.9, 0, 0, .1, 0), 1)
        self.username.load((.9, 0, 0, .1, 0), 1)
        self.password.load((.7, .1, .1, .1, 0), 1)
        self.password._pass = self.check_pass_length
        self.new.load((.6, .1, .1, .1, .1), 1)
        self.new.changePlaceholder(self.ent_cpwd)
        self.new.setAction(self.act, self.confirm_password_correct)
        self.hint.changePlaceholder(self.ent_hint)

    def place_widgs(self):
        rx, rw = self.rx_rw(.75)
        rrw = .6*rw
        self.name.place(relx=rx, rely=.05, relh=.12, relw=rw)

        self.username.place(relx=rx, rely=.22, relh=.12, relw=rw)
        self.admin.place(relx=rx+rw-.2, rely=.35, relh=.08, relw=.2)

        self.password.place(relx=rx, rely=.47, relh=.12, relw=rw)
        self.hint.place(relx=rx, rely=.6, relh=.09, relw=rw)

        self.new.place(relx=rx, rely=.76, relh=.09, relw=rw)

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


class Change_Username(Base_Password):

    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.addResultsWidgets(['password', 'username', 'new'])
        self.loadWidgets()
    
    def load(self):
        self.new.changePlaceholder(self.ent_nusr)
        self.new.load((.9, 0 , 0, .1, 0), 1)
        self.password.load((.6, .1, .1, .1, .1), 1)
        self.password.setAction(self.act, self.check_password)

    def place_widgs(self):
        rx, rw = self.rx_rw(.75)
        self.username.place(relx=rx, rely=.15, relh=.1, relw=rw)
        self.new.place(relx=rx, rely=.3, relh=.1, relw=rw)
        self.password.place(relx=rx, rely=.7, relh=.1, relw=rw)

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


class Change_Password(Base_Password):

    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.addResultsWidgets(['username', 'password', 'old', 'hint', 'new'])
        self.loadWidgets()
    
    def load(self):
        self.password.load((.7, .1, .1, .1, 0), 1)
        self.password.changePlaceholder(self.ent_npwd)
        self.password.setAction(_pass=self.check_pass_length)
        
        self.new.changePlaceholder(self.ent_cpwd)
        self.new.setAction(_pass=self.confirm_password_correct)
        self.new.load((.7, .1, .1, .1, 0), 1)
        self.hint.changePlaceholder(self.ent_hint)

        self.old.load((.6, .1, .1, .1, .1), 1)
        self.old.changePlaceholder(self.ent_pwd)
        self.old.setAction(self.act, self.check_password)


    def place_widgs(self):
        rx, rw = self.rx_rw(.75)
        self.username.place(relx=rx, rely=.05, relh=.12, relw=rw)
        self.password.place(relx=rx, rely=.25, relh=.12, relw=rw)
        self.new.place(relx=rx, rely=.4, relh=.12, relw=rw)
        rrw = rw*.7
        self.hint.place(relx=rx, rely=.55, relh=.09, relw=rrw)
        self.old.place(relx=rx, rely=.76, relh=.12, relw=rw)

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


class Delete_User(Base_Password):

    def __init__(self, master=None, inh=False, **kwargs):
        super().__init__(master=master, **kwargs)
        self.addResultsWidgets(['username', 'password'])
        self.loadWidgets()
    
    def load(self):
        self.password.load((.6, .1, .1, .1, .1), 1)
        self.password.setAction(self.act, self.check_password)

    def place_widgs(self):
        rx, rw = self.rx_rw(.75)
        self.username.place(relx=rx, rely=.15, relh=.15, relw=rw)
        self.password.place(relx=rx, rely=.5, relh=.15, relw=rw)

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




class Security_Settings(Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, relief="solid", **kwargs)
        self.container = Notebook(self, place=dict(relx=0, rely=.1, relh=.9, relw=1))
        self.login_status = Login_Status(self, place=dict(relx=0, rely=0, relh=.1, relw=1))
        self.tab_count = 0

        self.add_to_nb(User_Login(self.container), "User Login")
        self.add_to_nb(Add_User(self.container), "Add User")
        self.add_to_nb(Change_Username(self.container), "Change Username")
        self.add_to_nb(Change_Password(self.container), "Change Password")
        self.add_to_nb(Delete_User(self.container), "Delete User")
        # self.bell()

    def add_to_nb(self, wid, name):
        self.container.add(wid, padding=1)
        self.container.tab(self.tab_count, text=name,compound="left",underline="0")
        self.tab_count += 1




class Security(GaM_Dialog):
    def __init__(self, master=None, geo=(600, 500), title='GaM Security', **kwargs): super().__init__(master, geo=geo, title=title, **kwargs)

    def _setupDialog(self): Security_Settings(self.container, place=dict(relx=.005, rely=.005, relh=.99, relw=.99))


class Login(GaM_Dialog):
    def __init__(self, master=None, title='GaM Login.', **kwargs): super().__init__(master, title=title, cac=1, tipping=1, **kwargs)

    def _setupDialog(self):
        self.loaded = False

        self.pass_login = User_Login(self.container, container=1, callback=self._callback, place=dict(relx=.05, rely=.35, relh=.63, relw=.9), offset=.3)
        
        self.username_font = self.PRMP_FONT.copy()
        self.username_font['size'] = 30
        self.username_font = self.parseFont(self.username_font)

        self.anime = PRMP_ImageSLabel(self.container, bindMenu=0,  imageKwargs=dict(name='llovee', inExt='gif', inbuilt=1, prmpImage='line_bubbles'), config=dict(relief='flat'), place=dict(relx=(1-.6)/2, rely=.9, relw=.6, relh=.05))


        self.place_widgs()
        self.bind('<Map>',  self.afterload)
        self.loads = 0

    def afterload(self, event=None):
        '''
        updates the container objects
        '''
        if self.loaded: return

        x, y = geo = self.width, self.height
        
        self.img = PRMP_Image('purple_beau', resize=geo, for_tk=1, inbuilt=1, inExt='jpeg', name='purple_beau%s'%self.loads)

        self.container.create_image(0, 0, image=self.img, anchor='nw')

        self.gam_img = PRMP_Image(b64=GaM_PNGS['gam'], resize=(x, 180), for_tk=1)
        self.container.create_image(0, 5, image=self.gam_img, anchor='nw')

        self.change_color(self.img.image)

        user = 'Rocky Miracy Peter'
        # self.container.create_text(x/2, 360, text=user, fill='white', font=self.username_font)

        self.loads += 1
        self.loaded = 1

    def _callback(self):
        if self.callback: self.callback(self.destroy)

    def place_widgs(self):
        rw = .6
        rx = (1-rw)/2

        self.pass_login.username.place(relx=rx, rely=.45, relh=.065, relw=rw)
        self.pass_login.password.place(relx=rx, rely=.6, relh=.065, relw=rw)
        self.anime.place(relx=rx, rely=.9, relw=rw, relh=.05)





