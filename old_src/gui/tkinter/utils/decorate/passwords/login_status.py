

from . import LabelFrame, Label, Authorisation, Styles, Fonts, Button, confirm

class Login_Status(LabelFrame):
    font = Fonts.font15b
    logout_font = font
    
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


