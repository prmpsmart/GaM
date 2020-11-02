import platform
import tkinter.messagebox as msgbox
from .core import PRMP_Frame, partial


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
        container = PRMP_Frame(master)
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

def copyClassMethods(obj, copyClass, *args):
    
    for key, val in copyClass.__dict__.items():
        if key.startswith('__'): continue
        if callable(val):
            func = partial(val, *args)
            setattr(obj, key, func)

class Col_Mixins:
    
    @property
    def className(self): return f'{self.__class__.__name__}'
    
    def __str__(self): return f'{self.className}({str(self.columns)})'
    
    def __getitem__(self, num): return self.columns[num]
    
    def __len__(self): return len(self.columns)
    
    def AlphabetsSwitch(self):
        d = {}
        for n in range(65, 91):
            d[chr(n)] = chr(n+32)
            d[chr(n+32)] = chr(n)
        return d
    
    def propertize(self, name):
        if name:
            name = str(name)
            nm = name.replace(' ', '')
            fin = self.AlphabetsSwitch()[nm[0]] + nm[1:]
            return fin

class Column(Col_Mixins):
    
    def __init__(self, index, column):
        self.index = '#%d'%index
        
        value, width = '', 20
        if isinstance(column, (list, tuple)):
            l = len(column)
            self.text = column[0]
            self.attr = column[1] if (l>1) and column[1] else self.propertize(self.text)
            self.value = column[2] if (l>2) and column[2] else value
            self.width = column[3] if (l>3) and column[3] else 20
            
        elif isinstance(column, dict):
            self.text = column.get('text', value)
            self.attr = column.get('attr', self.propertize(self.text))
            self.value = column.get('value', value)
            self.width = column.get('width', width)
        
        else:
            self.text = column
            self.attr = self.propertize(self.text)
            self.value = value
            self.width = width
    
    def __repr__(self): return f'<{self.index}>'
    
    @property
    def columns(self): return [self.index, self.text, self.attr, self.value, self.width]
    
    def get(self, obj): return getattr(obj, self.attr, '') or ''

    def proof(self, obj): return self.get(obj) == self.value

class Columns(Col_Mixins):
    def __init__(self, columns):
        self.columns = []
        self.process(columns)
    
    def process(self, columns):
        del self.columns
        self.columns = []
        index = 0
        for col in columns:
            colObj = Column(index, col)
            self.columns.append(colObj)
            index += 1
        return self.columns
    
    def get(self, obj): return [col.get(obj) for col in self]





