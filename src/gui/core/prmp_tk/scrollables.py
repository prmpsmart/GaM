
# Extentions widgets
import tkinter as tk, tkinter.ttk as ttk, platform, time
from .usefuls import create_container, bound_to_mousewheel, Columns
from .core import PRMP_Frame, PRMP_Scrollbar, PRMP_Canvas, PRMP_Treeview, Font, PRMP_Theme


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
        '''Hide and show scrollbar as needed.'''
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


class ScrolledTreeView(AutoScroll, ttk.Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''
    @create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class ScrollableFrame(PRMP_Frame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.canvas = canvas = PRMP_Canvas(self, bg='blue')
        canvas.place(x=0, rely=0, relh=.96, relw=.99)
        
        # self.canvas.grid_rowconfigure(0, weight=1)
        
        xscrollbar = PRMP_Scrollbar(self, orient="horizontal", command=canvas.xview)
        yscrollbar = PRMP_Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        xscrollbar.pack(side="bottom", fill="x")

        yscrollbar.pack(side="right", fill="y")
        
        bound_to_mousewheel(0, self)
        
        self.scrollable_frame = PRMP_Frame(canvas)
        self.scrollable_frame.pack(side='left', fill='both', expand=1)

        self.scrollable_frame.bind("<Configure>", self.changeFrameBox)

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')


        
        
    def changeFrameBox(self, e=0):
        p = self.canvas.bbox("all")
        self.canvas.configure(scrollregion=p)
        

SF = ScrollableFrame


class PRMP_TreeView(PRMP_Frame):
    __shows = ['tree', 'headings']
    __slots__ = ['tree']
    
    def __init__(self, master=None, columns=[], **kwargs):
        super().__init__(master=master, **kwargs)
        
        self.t = self.tree = self.treeview = PRMP_Treeview(self)
        xscrollbar = PRMP_Scrollbar(self, orient="horizontal", command=self.treeview.xview)
        yscrollbar = PRMP_Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        
        xscrollbar.pack(side="bottom", fill="x")
        self.treeview.pack(side='left', fill='both', expand=1)
        yscrollbar.pack(side="right", fill="y")
        bound_to_mousewheel(0, self)
        
        self.ivd = self.itemsValuesDict = {}
        self.firstItem = None
        self.current = None
        self.attributes = []
        
        self.columns = Columns(columns)
        self.setColumns()
        self.bindings()
    
    def bindings(self):
        self.tree.bind('<<TreeviewSelect>>', self.selected)

    def selected(self, e=0):
        item = self.tree.focus()
        self.current = self.ivd.get(item)
        return self.current

    def insert(self, item, position='end',  **kwargs): return self.treeview.insert(item, position, **kwargs)
    
    def tag_config(self, tagName, font=PRMP_Theme.DEFAULT_FONT, **kwargs):
        font = Font(**font)
        return self.tree.tag_configure(tagName, font=font, **kwargs)
    
    def heading(self, item, **kwargs): return self.treeview.heading(item, **kwargs)
    
    def column(self, item, **kwargs): return self.treeview.column(item, **kwargs)
    
    def treeviewConfig(self, **kwargs): self.treeview.configure(**kwargs)
    
    tvc = Config = treeviewConfig

    def setColumns(self, columns=[]):
        if columns: self.columns.process(columns)
            
        if len(self.columns) > 1: self.tvc(columns=self.columns[1:])

        for column in self.columns:
            self.heading(column.index, text=column.text, anchor='center')
            self.column(column.index, width=column.width, minwidth=10, stretch=1,  anchor="w")
    
    def set(self, obj=None, parent='', op=False):

        cols = self.columns.get(obj)
        
        name, *columns = self.columns.get(obj)
        tag = 'prmp'
        
        # the fourth value of this [text, attr, width, value] can be used in sorting, it wont insert the region and its columns both into self.tree and self.ivd if not equal to value
        
        item = self.insert(parent, text=name, values=columns, tag=tag, open=op)
        self.tag_config(tag)

        self.ivd[item] = obj
        
        if self.firstItem == None:
            self.firstItem = item
            self.treeview.focus(self.firstItem)
        
        subs = obj.subs
        if subs:
            for sub in subs: self.set(sub, item, op)






