from .....backend.utils.data.path import Path
from .....backend.utils.threads import Threads, TData
from ..widgets.debug import show, confirm
from ..widgets.admin_req import make_change
from .passwords.password_settings import Password_Settings, Authorisation
from ..widgets.twowidgets import TwoWidgets, LabelEntry, Label, Checkbutton, Styles
from tkinter import Toplevel, StringVar, Button, Frame, colorchooser, filedialog, Widget
from tkinter.ttk import Notebook

class Settings(Toplevel):
    go = 0
    op = False
    def __init__(self, master=None):
        self._w = "self"
        if Settings.op == True: pass
        else:
            super().__init__(master)
            x, y = self.winfo_screenwidth(), self.winfo_screenheight()
            wx = int(x/3)
            wy = int(y/7)
            self.geometry("550x500+%d+%d"%(wx, wy))
            self.title("Settings")
            self["background"] = Styles.background
            self.attributes("-alpha", 1, "-disabled", False, "-toolwindow", True, "-topmost", True)
            self.wm_protocol("WM_DELETE_WINDOW", self.exiting)

            self.save_btn = Button(self, command=self.saving_dir, text=Path.get_save_dir())
            self.save_btn.place(relx=0, rely=0, relh=.1, relw=1)
            
            self.tab_count = 0
            self.note = Notebook(self)
            self.note.place(relx=0, rely=.1, relh=.9, relw=1)
            # Charts
            self.chart = Frame(self.note, takefocus="")
            self.add_to_nb(self.chart, "Charts")
            
        # Password
            self.password = Password_Settings(self.note)
            self.add_to_nb(self.password, "Password")
            
            self.chart_set()
            
            self.style()
            Settings.op = True
            
    def add_to_nb(self, wid, name):
        self.note.add(wid, padding=1)
        self.note.tab(self.tab_count, text=name,compound="left",underline="0")
        self.tab_count += 1
    
    def saving_dir(self):
        save_dir = filedialog.askdirectory()
        if Path.confirm_path(save_dir) == "dir":
            if confirm(title="Confirm", msg=f"Are you sure you want to set {save_dir} as the SAVING DIRECTORY", num=1):
                
                if make_change({Path.set_save_dir: save_dir, Threads.save_other_datas: None}): self.save_btn.config(text=Path.save_dir)
        elif save_dir == "": pass
        else: show(title="Invalid", msg="Enter a valid Directory", which="error")
    
    def chart_set(self):
        def theme():
            self.cb_clicked()
            if self.check.get() != "1": self.color["state"] = "normal"
            else:
                self.color["state"] = "disabled"
                Styles.chart = True
                make_change(TData.save_other_datas)
        def choose_color():
            _, color = colorchooser.askcolor("white")
            self.color["bg"] = color
            Styles.chart = color
            make_change(TData.save_other_datas)
        
        self.check = StringVar()
        
        self.checkb = Checkbutton(self.chart, variable=self.check, text="Use theme", command=theme)
        self.checkb.place(relx=0, rely=.03, relh=.15, relw=.3)
        self.color = Button(self.chart, text="Chart Bg", command=choose_color)
        self.color.place(relx=0, rely=.2, relh=.15, relw=.3)
        if Styles.chart == True: self.check.set('1')
        elif isinstance(Styles.chart, str) and not '': self.color["bg"] = Styles.chart
        theme()

    def exiting(self):
        Settings.op = False
        self.destroy()
    
    def style(self):
        ghs = [self.save_btn, self.checkb, self.color]
        for a in ghs: a.config(activebackground=Styles.background, activeforeground=Styles.foreground, background=Styles.background, disabledforeground=Styles.foreground, font=Styles.font, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief="solid")
        self.password.style()
        frames = [self.chart]
        for frame in frames: frame.config(background=Styles.background)
    
    def cb_clicked(self):
        buts = {self.checkb:self.check}
        for but in buts:
            var = buts[but]
            if var.get() == "1": but["fg"] = "blue"
            else: but["fg"] = Styles.foreground
    


