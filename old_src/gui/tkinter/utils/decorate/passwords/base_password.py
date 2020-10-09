
from . import Frame, Button, StringVar, Checkbutton, Styles, Entry, Fonts, Label, Authorisation, show, confirm, Threads
from ...widgets.admin_req import show_admin_required

class Base_Password(Frame):
    
    def __init__(self, master=None):
        
        super().__init__(master=master, bg=Styles.background)
        
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

        self.name = StringVar()
        self.username = StringVar()
        self.admin = StringVar()
        self.password = StringVar()
        self.old = StringVar()
        self.new = StringVar()
        self.pass_show = StringVar()
        self.old_show = StringVar()
        self.hint = StringVar()
        self.forgot = StringVar()
        
        self.name_ent = Entry(self, textvariable=self.name, bd=2, font=Fonts.font10)
        
        self.clr_name = Button(self, text="Clear", command=self.clear_name, relief="solid")
        
        self.username_ent = Entry(self, textvariable=self.username, font=Fonts.font10, bd=2)
        self.clr_usr = Button(self, text="Clear", command=self.clear_username, relief="solid")
        
        self.admin_chk = Checkbutton(self, variable=self.admin, relief="solid", text="Admin?", command=self.admin_add)
        
        self.password_ent = Entry(self, textvariable=self.password, font=Fonts.font10, bd=2)
        
        self.old_ent = Entry(self, textvariable=self.old, font=Fonts.font10, bd=2)
        self.clr_old = Button(self, text="Clear", command=self.clear_old, relief="solid")
        
        self.password_confirm = Label(self)
        
        self.password_length = Label(self, relief="sunken", bd=3)
        
        self.clr_pwd = Button(self, text="Clear", command=self.clear_password, relief="solid")
        
        self.new_ent = Entry(self, textvariable=self.new, font=Fonts.font10, bd=2)
        self.clr_new = Button(self, text="Clear", command=self.clear_new, relief="solid")
        
        self.show_pass = Checkbutton(self, variable=self.pass_show, command=self.show_password, relief="solid", text="Show")
        
        self.show_old = Checkbutton(self, variable=self.old_show, command=self.show_old_, relief="solid", text="Show")
        
        self.hint_ent = Entry(self, textvariable=self.hint, font=Fonts.font10, bd=2)
        
        self.clr_hint = Button(self, text="Clear", command=self.clear_hint, relief="solid")
        
        self.hx, self.hy, self.hh, self.hw, = .1, .43, .04, .5
        self.forgot_chk = Checkbutton(self, variable=self.forgot, command=self.forgot_check, relief="solid", text="Forgot Password?")
        
        self.hint_lbl = Label(self, relief="groove")
        
        self.action = Button(self, text='Action', relief="solid", command=self.make_change)
        
        # self.init()
        
    def get_name(self): return self.name.get()
    def get_username(self): return self.username.get()
    def get_password(self): return self.password.get()
    def get_new(self): return self.new.get()
    def get_hint(self): return self.hint.get()
        
    def defaults(self):
        self.username.set(self.ent_usr)
        self.name.set(self.ent_name)
        self.admin.set('0')
        self.password.set(self.ent_pwd)
        self.old.set(self.ent_old)
        self.new.set(self.ent_new)
        self.hint.set(self.ent_hint)
        self.pass_show.set('0')
        self.old_show.set('0')
        self.password_length.config(text='')

    def binds(self):
        self.username_ent.bind("<Enter>", self.usr_enter)
        self.username_ent.bind("<Leave>", self.usr_leave)
        
        self.name_ent.bind("<Enter>", self.name_enter)
        self.name_ent.bind("<Leave>", self.name_leave)
        
        self.hint_ent.bind("<Enter>", self.hint_enter)
        self.hint_ent.bind("<Leave>", self.hint_leave)
        
        self.password_ent.bind("<Enter>", self.pass_enter)
        self.password_ent.bind("<Leave>", self.pass_leave)
        self.password_ent.bind("<KeyRelease>", self.show_star)
        
        self.old_ent.bind("<Enter>", self.old_enter)
        self.old_ent.bind("<Leave>", self.old_leave)
        if self.old_is_password: self.old_ent.bind("<KeyRelease>", self.old_show_star)
        
        self.new_ent.bind("<Enter>", self.new_enter)
        self.new_ent.bind("<Leave>", self.new_leave)
        if self.new_is_password: self.new_ent.bind("<KeyRelease>", self.new_show_star)

    def clear_username(self, *e): self.username.set(self.ent_usr)
    def clear_name(self, *e): self.name.set(self.ent_name)
    def clear_hint(self, *e): self.hint.set(self.ent_hint)
    def clear_password(self, *e):
        self.password.set(self.ent_pwd)
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
            show("ADMIN?", "Only an ADMIN can add another user", "error")
            
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
        self.cb_clicked()
        if self.forgot.get() == '1':
            self.hint_lbl.config(text=self.hint_text)
            self.hint_lbl.place(relx=self.hx, rely=self.hy, relh=self.hh, relw=self.hw)
        else: self.hint_lbl.place_forget()
    
    def show_password(self, *e):
        self.cb_clicked()
        if self.pass_show.get() == '1':
            self.show_norm()
            if self.new_is_password: self.new_show_norm()
        else:
            self.show_star()
            if self.new_is_password: self.new_show_star()
    
    def show_old_(self, *e):
        self.cb_clicked()
        if self.old_show.get() == '1':
            self.old_show_norm()
            if self.old_is_password: self.old_show_norm()
        else:
            self.old_show_star()
            if self.old_is_password: self.old_show_star()

    def usr_enter(self, *e):
        username = self.username.get()
        if username == self.ent_usr: self.username_ent.delete("0", "end")

    def usr_leave(self, *e):
        username = self.username.get()
        if username == '': self.username_ent.insert("0", self.ent_usr)
        
    def name_enter(self, *e):
        name = self.name.get()
        if name == self.ent_name: self.name_ent.delete("0", "end")

    def name_leave(self, *e):
        name = self.name.get()
        if name == '': self.name_ent.insert("0", self.ent_name)

    def hint_enter(self, *e):
        hint = self.hint.get()
        if hint == self.ent_hint: self.hint_ent.delete("0", "end")

    def hint_leave(self, *e):
        hint = self.hint.get()
        if hint == '': self.hint_ent.insert("0", self.ent_hint)

    def pass_enter(self, *e):
        password = self.password.get()
        if password == self.ent_pwd: self.password_ent.delete("0", "end")

    def pass_leave(self, *e):
        password = self.password.get()
        if password == '':
            self.show_norm()
            self.password_ent.insert("0", self.ent_pwd)
    
    def new_enter(self, *e):
        new = self.new.get()
        if new == self.ent_new: self.new_ent.delete("0", "end")
    
    def new_leave(self, *e):
        new = self.new.get()
        if new == '':
            if self.new_is_password: self.new_show_norm()
            self.new_ent.insert("0", self.ent_new)
    
    def old_enter(self, *e):
        old = self.old.get()
        if old == self.ent_old: self.old_ent.delete("0", "end")
    
    def old_leave(self, *e):
        old = self.old.get()
        if old == '':
            if self.old_is_password: self.old_show_norm()
            self.old_ent.insert("0", self.ent_old)
    
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

    
    def check_pass_length(self):
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
        if self.pass_show.get() == '1': pass
        else: self.new_ent.config(show='*')
        self.confirm_password_correct()
    def new_show_norm(self, *e): self.new_ent.config(show='')

    def old_show_star(self, *e):
        if self.pass_show.get() == '1': pass
        else: self.old_ent.config(show='*')
    def old_show_norm(self, *e): self.old_ent.config(show='')

    def show_star(self, *e):
        if self.pass_show.get() == '1': pass
        else: self.password_ent.config(show='*')
        self.check_pass_length()
        
    def show_norm(self, *e): self.password_ent.config(show='')
    
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
    
    def cb_clicked(self):
        buts = {self.forgot_chk:self.forgot, self.show_pass:self.pass_show, self.show_old:self.old_show}
        for but in buts:
            var = buts[but]
            if var.get() == "1": but["fg"] = "blue"
            else: but["fg"] = Styles.foreground
    
    def style(self):
        self.config(bg=Styles.background)
        ents = [self.name_ent, self.username_ent,  self.password_ent, self.new_ent, self.old_ent, self.hint_ent]
        widgs = [self.show_pass, self.hint_lbl, self.password_confirm, self.show_old] #+ ents
        for widg in widgs: widg.config(bg=Styles.background, fg=Styles.foreground, font=Fonts.font11b)
        
        buttons = [self.clr_name, self.clr_usr, self.admin_chk, self.clr_pwd, self.clr_new, self.clr_old, self.clr_hint, self.forgot_chk, self.action, self.forgot_chk, self.show_pass]
        for button in buttons: button.config(activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor="white", justify="left", overrelief="ridge", relief="solid")


    def init(self):
        self.binds()
        self.defaults()
        self.place_widgs()
        self.style()
    def make_change(self):
        if Authorisation.is_admin(): self.act()
        else: show_admin_required()
    def act(self): pass
    
    def load_data(self): Threads.load_passwords()
    
    def save_data(self): Threads.save_passwords()

