from ..decorate.styles import Styles, Fonts
from tkinter import LabelFrame
from tkinter import messagebox, Message

def show(title=None, msg=None, which=None):
    if which == 'error': messagebox.showerror(title, msg)
    elif which == 'info': messagebox.showinfo('Information', msg)
    elif which == 'warn': messagebox.showwarning('Warning', msg)
    
def confirm(title=None, msg=None, num=None):
    if num == 1: return messagebox.askyesno(title, msg)
    if num == 2: return messagebox.askquestion(title, msg)
    if num == 3: return messagebox.askokcancel(title, msg)
    if num == 4: return messagebox.askretrycancel(title, msg)
    if num == 5: return messagebox.askyesnocancel(title, msg)


class Out_Message(LabelFrame):
    def __init__(self, master, relx=0, rely=0.753, relh=0.2475, relw=0.19, hide=0, var=None, head=''):
        
        if hide: head=''
        else:
            if head: pass
            else: head = 'Output Message'
        super().__init__(master, text=head)
        self.relx, self.rely, self.relh, self.relw = relx, rely, relh, relw

        self.message = Message(self, anchor='nw', relief="sunken", width=296, text='You get ya OUTPUT MESSAGE here', textvariable=var)

        self.style()
        
    def set_message(self, msg): self.message.config(text=msg)
    def style(self):
        self.config(relief='groove', font=Fonts.font11b, foreground=Styles.foreground, background=Styles.background, highlightbackground=Styles.background, highlightcolor=Styles.foreground)
        self.message.config(borderwidth="3", font=Fonts.font11b, foreground=Styles.higfg, highlightbackground=Styles.background, highlightcolor=Styles.foreground, background=Styles.higbg)
    
    def place_widgs(self):
        self.message.place(relx=0.016, rely=0.167, relh=0.708, relw=0.955, bordermode='ignore')
        self.place(relx=self.relx, rely=self.rely, relh=self.relh, relw=self.relw)





