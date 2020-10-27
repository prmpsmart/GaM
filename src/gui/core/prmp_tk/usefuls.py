import platform
import tkinter.messagebox as msgbox

def on_mousewheel(event, widget):
    what = 'units'
    what = 'pages'
    if platform.system() == 'Windows': widget.yview_scroll(-1*int(event.delta/120),what)
    elif platform.system() == 'Darwin': widget.yview_scroll(-1*int(event.delta),what)
    else:
        if event.num == 4:
            widget.yview_scroll(-1, what)
        elif event.num == 5:
            widget.yview_scroll(1, what)

def on_shiftmouse(event, widget):
    what = 'units'
    what = 'pages'
    if platform.system() == 'Windows': widget.xview_scroll(-1*int(event.delta/120), what)
    elif platform.system() == 'Darwin': widget.xview_scroll(-1*int(event.delta), what)
    else:
        if event.num == 4: widget.xview_scroll(-1, what)
        elif event.num == 5: widget.xview_scroll(1, what)

def bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: on_shiftmouse(e, child))

def unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def create_container(func):
    '''Creates a Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = F(master)
        container.bind('<Enter>', lambda e: bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped



def show(title=None, msg=None, which=None):
    if which == 'error': msgbox.showerror(title, msg)
    elif which == 'info': msgbox.showinfo('Information', msg)
    elif which == 'warn': msgbox.showwarning('Warning', msg)

def confirm(title=None, msg=None, num=None):
    if num == 1: return msgbox.askyesno(title, msg)
    if num == 2: return msgbox.askquestion(title, msg)
    if num == 3: return msgbox.askokcancel(title, msg)
    if num == 4: return msgbox.askretrycancel(title, msg)
    if num == 5: return msgbox.askyesnocancel(title, msg)


