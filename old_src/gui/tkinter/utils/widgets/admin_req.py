
from .....backend.utils.data.passwords.authorisation import Authorisation

from tkinter import messagebox, Message

def show(title=None, msg=None, which=None):
    if which == 'error': messagebox.showerror(title, msg)
    elif which == 'info': messagebox.showinfo('Information', msg)
    elif which == 'warn': messagebox.showwarning('Warning', msg)

def show_admin_required(): show("ADMIN Required", "An ADMIN permission is required.", "error")

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