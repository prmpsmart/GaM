from .core import tk
from . import *
from .miscs import *

__all__ = ['PRMP_ListBox', 'PRMP_TreeView', 'PRMP_ScrollText', 'ScrollableFrame', 'ScrolledText', 'ScrolledEntry', 'ListBox', 'TreeView', 'ScrollText', 'Hierachy']

class AutoScroll:
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        try:
            self.vsb = tk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        self.hsb = tk.Scrollbar(master, orient='horizontal', command=self.xview)

        try:
            self.configure(yscrollcommand=self._autoscroll(self.vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(self.hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            self.vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        self.hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        # if py2
        # methods = Pack.__dict__.keys() + Grid.__dict__.keys() + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)
AS = AutoScroll


class PRMP_ListBox(PRMP_Frame):

    def __getattr__(self, attr):
        ret = self.getFromSelf(attr, self._unget)
        if ret != self._unget: return ret
        else: return getattr(self.listbox, attr)

    def __init__(self, master, listboxConfig={}, callback=None, **kwargs):
        super().__init__(master, **kwargs)

        self.listbox = PRMP_Listbox(self, callback=callback, **listboxConfig)

        self.clear = self.listbox.clear
        self.set = self.listbox.set
        self.clicked = self.listbox.clicked

        self.xscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="horizontal", command=self.listbox.xview))
        self.yscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="vertical", command=self.listbox.yview))
        self.listbox.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)

        self.xscrollbar.pack(side="bottom", fill="x")
        self.listbox.pack(side='left', fill='both', expand=1)
        self.yscrollbar.pack(side="right", fill="y")

        bound_to_mousewheel(0, self)

    @property
    def selected(self): return self.listbox.selected or []

ListBox = PLB = PRMP_ListBox

class PRMP_TreeView(PRMP_Frame):
    __shows = ['tree', 'headings']
    __slots__ = ['tree']

    # def __getattr__(self, attr):
        # ret = self.getFromSelf(attr, self._unget)
        # if ret != self._unget: return ret
        # else: return getattr(self.treeview, attr)

    def __init__(self, master=None, columns=[], treeviewKwargs={}, **kwargs):
        super().__init__(master=master, **kwargs)

        self.treeview = None
        self.treeviewKwargs = treeviewKwargs
        self.xscrollbar = None
        self.yscrollbar = None
        self.obj = None
        self.firstItem = None

        self.columns = Columns(columns)
        self.setColumns(columns)

    def bindings(self): pass

    def create(self):
        if self.treeview:
            self.treeview.destroy()
            del self.treeview

            self.xscrollbar.destroy()
            del self.xscrollbar

            self.yscrollbar.destroy()
            del self.yscrollbar

        self.t = self.tree = self.treeview = PRMP_Treeview(self, **self.treeviewKwargs)
        self.xscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="horizontal", command=self.treeview.xview))
        self.yscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="vertical", command=self.treeview.yview))
        self.treeview.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)

        self.xscrollbar.pack(side="bottom", fill="x")
        self.treeview.pack(side='left', fill='both', expand=1)
        self.yscrollbar.pack(side="right", fill="y")
        bound_to_mousewheel(0, self)

        self.attributes = []

        self.selected = self.treeview.selected
        self.clear = self.treeview.clear
        self.ivd = self.treeview.ivd
        self.insert = self.treeview.insert
        self.heading = self.treeview.heading
        self.column = self.treeview.column

        self.bindings()

    def tag_config(self, tagName, font=PRMP_Theme.DEFAULT_FONT, **kwargs):
        font = Font(**font)
        # return self.tree.tag_configure(tagName, font=font, **kwargs)
        return self.tree.tag_configure(tagName, **kwargs)

    def treeviewConfig(self, **kwargs): self.treeview.configure(**kwargs)

    tvc = Config = treeviewConfig

    def setColumns(self, columns=[]):
        self.create()

        if isinstance(columns, Columns): self.columns = columns

        else: self.columns.process(columns)

        if len(self.columns) > 1: self.tvc(columns=self.columns[1:])
        self.updateHeading()

    def updateHeading(self):
        for column in self.columns:
            self.heading(column.index, text=column.text, anchor='center')
            self.column(column.index, width=column.width, stretch=1,  anchor="center")#, minwidth=80)
        self.reload()

    def _set(self, obj=None, parent='', subs='subs', op=1):
        name, *columns = self.columns.getFromObj(obj)
        tag = 'prmp'

        # the fourth value of this [text, attr, width, value] can be used in sorting, it wont insert the region and its columns both into self.tree and self.ivd if not equal to value

        item = self.insert(parent, text=name, values=columns, tag=tag, open=op, value=obj)
        self.tag_config(tag)

        if self.firstItem == None:
            self.firstItem = item
            self.treeview.focus(self.firstItem)

        _subs = obj.getFromSelf(subs) if not isinstance(obj, self.containers) else obj
        if _subs:
            for sub in _subs: self._set(obj=sub, parent=item, subs=subs, op=op)

    def set(self, obj, op=1):
        if not obj: return

        self.setColumns()
        self.clear()
        if obj:
            self.obj = obj
            self._set(obj, op=op)

    def reload(self): self.set(self.obj)

TreeView = PTV = PRMP_TreeView

class PRMP_ScrollText(PRMP_Frame):

    def __init__(self, master=None, columns=[], **kwargs):
        super().__init__(master=master, **kwargs)

        self.text = PRMP_Text(self)
        self.xscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="horizontal", command=self.text.xview))
        self.yscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="vertical", command=self.text.yview))
        self.text.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)

        self.xscrollbar.pack(side="bottom", fill="x")
        self.text.pack(side='left', fill='both', expand=1)
        self.yscrollbar.pack(side="right", fill="y")
        bound_to_mousewheel(0, self)

ScrollText = PSTx = PRMP_ScrollText

# under testing
class ScrollableFrame(PRMP_Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.canvas = PRMP_Canvas(self, config=dict(bg='blue'))
        self.canvas.place(x=0, rely=0, relh=.96, relw=.99)

        # self.canvas.grid_rowconfigure(0, weight=1)

        xscrollbar = PRMP_Scrollbar(self, config=dict(orient="horizontal", command=self.canvas.xview))
        yscrollbar = PRMP_Scrollbar(self, config=dict(orient="vertical", command=self.canvas.yview))
        self.canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        xscrollbar.pack(side="bottom", fill="x")

        yscrollbar.pack(side="right", fill="y")

        bound_to_mousewheel(0, self)

        self.scrollable_frame = PRMP_Frame(self.canvas)
        self.scrollable_frame.pack(side='left', fill='both', expand=1)

        self.scrollable_frame.bind("<Configure>", self.changeFrameBox)

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.changeFrameBox()

    def changeFrameBox(self, e=0):
        p = self.canvas.bbox("all")
        self.canvas.configure(scrollregion=p)

SF = ScrollableFrame


class ScrolledText(AutoScroll, tk.Text):

    @create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


class ScrolledEntry(AutoScroll, tk.Entry):

    @create_container
    def __init__(self, master, **kw):
        tk.Entry.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)


class Hierachy(PRMP_TreeView):

    def __init__(self, master=None, columns=[], toggleOpen=True, binds=[], **kwargs):
        self._toggleOpen = False
        self.toop = toggleOpen
        self.last = []
        self.binds = binds
        super().__init__(master=master, columns=columns, **kwargs)

        self.bindings()

    @property
    def openDialog(self):
        from .dialogs import dialogFunc
        return dialogFunc

    def toggleOpen(self, e=0):
        if self._toggleOpen: self._toggleOpen = False
        else: self._toggleOpen = True

        if self.last: self.viewObjs(*self.last)

    def bindings(self):
        self.treeview.bind('<Control-Return>', self.viewSelected, '+')
        if self.toop:
            self.treeview.bind('<Control-o>', self.toggleOpen, '+')
            self.treeview.bind('<Control-O>', self.toggleOpen, '+')

        self.treeview.bind('<Control-r>', self.reload, '+')
        self.treeview.bind('<Control-R>', self.reload, '+')

        for event, func, sign in self.binds: self.treeview.bind(event, func, sign)

    def reload(self, e=0):
        if self.last: self.viewObjs(*self.last)

    def viewSelected(self, e=0):
        current = self.selected()

        if current: self.openDialog(master=self, obj=current)

    def getSubs(self, obj, item=''):
        return obj.subs

    def _viewObjs(self, obj, parent=''):
        if not obj: return

        if isinstance(obj, list):
            subs = obj
            item = parent
        else:
            raw = self.columns.getFromObj(obj)
            first, *columns = raw

            item = self.insert(parent, text=first, values=columns, open=self._toggleOpen, value=obj)

            subs = self.getSubs(obj, item)

        if isinstance(subs, list):
            for sub in subs:
                # print(subs)
                if sub: self._viewObjs(sub, item)

    def viewObjs(self, obj, parent=''):
        if not parent: self.clear()
        self._viewObjs(obj, parent)
        self.last = obj, parent

    def viewSubs(self, obj): self.viewObjs(obj[:])


class Table(Frame):
    
    def toNum(self, value):
        numbers = [str(num) for num in range(10)] + ['.']
        value = str(value)
        for val in value:
            if val not in numbers: value = value.replace(val, '')
        return float(value or 0)

    def __init__(self, master, title='', treeKwargs={}, reserve=0, output=float, converter=None, offset=3, treeWidget=(), **kwargs):
        '''
        master: parent of this widget.
        title: title of this table.
        treeKwargs: parameters of the Treeview.
        reserve: number of columns to not process in each row.
        output: function to format the processed values.
        converter: function to process the raw values, default is Table.toNum.
        offset: number of empty rows to leave before writing the totals.
        treeWidget: A subclass of Treeview, or any widget to use as the holder of the contents of the table
        kwargs: parameters for Frame.__init__() 
        '''



        super().__init__(master, **kwargs)
        
        self.reserve = reserve
        self.output = output
        self.offset = offset
        self.converter = converter or self.toNum

        font = self.PRMP_FONT.copy()
        font['size'] = 20
        self.title = Label(self, text=title, place=dict(x=0, y=0, h=40, relw=1), font=font)

        treeWidget = treeWidget or Hierachy
        self.tree = treeWidget(self, place=dict(x=0, y=42, relw=1, relh=1), **treeKwargs)

        self.bind('<Map>', self.resize)
    
    def resize(self, event=None):
        width, height = self.width, self.height
        self.title.place(x=0, y=0, h=40, relw=1)
        self.tree.place(x=0, y=40, relw=1, relh=((height-40)/height))
    
    def setTitle(self, title): self.title.set(title)

    @property
    def columns(self): return self.tree.columns

    def getTotals(self, values):
        processed_values = []
        for value in values:
            proc_val = self.columns.getFromObj(value)[self.reserve:]
            proc_val = [self.converter(val) for val in proc_val]
            processed_values.append(proc_val)

        totalInner = len(processed_values[0])

        combined = [0 for _ in range(totalInner)]
        
        for p_v in processed_values:
            for index, inner in enumerate(p_v): combined[index] += float(inner or 0)
        

        outputs = []
        for val in combined:
            if val: out = self.output(val)
            else: out = ''
            outputs.append(out)
        
        return outputs
    
    def updateTable(self, title, values):
        self.setTitle(title)
        self.viewObjs(values)

    def viewObjs(self, values):
        self.tree.viewObjs(values)
        
        if not values: return
        totals = self.getTotals(values)
        
        offset_rows = ['' for _ in self.columns[1:]]
        text = totals[0]
        if self.reserve:
            totals = offset_rows[:self.reserve-1] + totals
            text = 'Totals'
        
        for _ in range(self.offset): self.tree.insert('', text='', values=offset_rows)

        self.tree.insert('', text=text, values=totals)
    
    def clear(self):
        self.title.clear()
        self.tree.clear()










