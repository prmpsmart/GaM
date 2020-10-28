
# Extentions widgets
import tkinter as tk, tkinter.ttk as ttk, platform, time
from .usefuls import create_container, bound_to_mousewheel
from .core import PRMP_Frame, PRMP_Scrollbar, PRMP_Canvas


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
        super().__init__(master)
        
        self.canvas = canvas = PRMP_Canvas(self)
        
        xscrollbar = PRMP_Scrollbar(self, orient="horizontal", command=canvas.xview)
        yscrollbar = PRMP_Scrollbar(self, orient="vertical", command=canvas.yview)
        
        self.scrollable_frame = PRMP_Frame(canvas)

        self.scrollable_frame.bind("<Configure>", self.changeFrameBox)

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)

        xscrollbar.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)
        yscrollbar.pack(side="right", fill="y")
        
        # bound_to_mousewheel(0, self.canvas)
        bound_to_mousewheel(0, self)
        # bound_to_mousewheel(0, self.scrollable_frame)
        # self.scrollable_frame.bind('<MouseWheel>', yscrollbar.set)
        # self.canvas.bind('<MouseWheel>', yscrollbar.set)
        
        # self = self.scrollable_frame
    
    def changeFrameBox(self, e=0): self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def addWidget(self, widget, **kwargs): return widget(self.scrollable_frame, **kwargs)

SF = ScrollableFrame







