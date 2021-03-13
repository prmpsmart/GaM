import platform

from prmp.prmp_miscs.prmp_datetime import PRMP_Mixins, PRMP_DateTime
import functools


def on_mousewheel(event, widget):
    what = 'units'
    what = 'pages'
    try:
        if platform.system() == 'Windows': widget.yview_scroll(-1*int(event.delta/120), what)
        elif platform.system() == 'Darwin': widget.yview_scroll(-1*int(event.delta),what)
        else:
            if event.num == 4:
                widget.yview_scroll(-1, what)
            elif event.num == 5:
                widget.yview_scroll(1, what)
    except: pass

def on_shiftmouse(event, widget):
    what = 'units'
    what = 'pages'
    try:
        if platform.system() == 'Windows': widget.xview_scroll(-1*int(event.delta/120), what)
        elif platform.system() == 'Darwin': widget.xview_scroll(-1*int(event.delta), what)
        else:
            if event.num == 4: widget.xview_scroll(-1, what)
            elif event.num == 5: widget.xview_scroll(1, what)
    except: pass

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
        from .core import PRMP_Frame
        container = PRMP_Frame(master)
        container.bind('<Enter>', lambda e: bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

def copyClassMethods(obj, copyClass, *args):

    for key, val in copyClass.__dict__.items():
        if key.startswith('__'): continue
        if callable(val):
            if obj.class_ == copyClass: func =functools. partial(val, obj)
            else: func = functools.partial(val, *args)

            setattr(obj, key, func)

class Col_Mixins(PRMP_Mixins):

    def __str__(self): return f'{self.className}({str(self.columns)})'

    def __getitem__(self, num): return self.columns[num]

    def __len__(self): return len(self.columns)

class Column(Col_Mixins):

    def __init__(self, index, column):
        self.subs = []
        self.index = '#%d'%index
        self.type = None
        value, width = '', 20
        self._attr = None

        if isinstance(column, (list, tuple)):
            l = len(column)
            self.text = column[0]
            self.attr = column[1] if (l>1) and column[1] else self.propertize(self.text)
            self.value = column[2] if (l>2) and column[2] else value
            self.width = column[3] if (l>3) and column[3] else 20

        elif isinstance(column, dict):
            self.text = column.get('text', value)
            self.attr = column.get('attr', None)
            if not self.attr: self.attr = self.propertize(self.text)
            if isinstance(self.attr, list):
                self._attr = self.attr
                self.attr = self.attr[0]
            self.value = column.get('value', value)
            self.width = column.get('width', None) or width
            self.type = column.get('type')

        else:
            self.text = column
            self.attr = self.propertize(self.text)
            self.value = value
            self.width = width

    def __repr__(self): return f'<{self.index}>'

    @property
    def columns(self): return [self.index, self.text, self.attr, self.value, self.width]

    def getFromObj(self, obj):
        if obj:
            try:
                val = ''
                if self._attr:
                    for attr in self._attr:
                        try:
                            val = obj[attr]
                            if val != None: break
                        except: pass
                else: val = obj[self.attr] or val

                if val:
                    if self.type: val = self.type(val)
                return val or ''

            except Exception as e: return ''

    def proof(self, obj): return self.getFromObj(obj) == self.value

    def __getitem__(self, item): return PRMP_Mixins.__getitem__(self, item)


class Columns(Col_Mixins):
    def __init__(self, columns):
        self.subs = self.columns = []
        self.process(columns)

    def process(self, columns):
        if not columns: return

        self.columns = []
        for col in columns: self.addColumn(col)
        return self.columns

    setColumns = process

    def getFromObj(self, obj): return [col.getFromObj(obj) for col in self]

    def addColumn(self, col):
        colObj = Column(len(self), col) if not isinstance(col, Column) else col
        self.columns.append(colObj)
        return colObj

    def remove(self, col):
        c = dict(text=col.text, attr=col.attr, width=col.width, value=col.value)
        for res in self:
            d = dict(text=res.text, attr=res.attr, width=res.width, value=res.value)
            if d == c: self.sub.remove(res)





