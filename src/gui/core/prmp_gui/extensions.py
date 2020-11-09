from .core import *
from .miscs import create_container, bound_to_mousewheel, Columns

# Extensions

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
AS = AutoScroll

class FillWidgets:
    
    def __init__(self, values={}):
        self.__resultsWidgets = []
        self.values = values
        
    def addResultsWidgets(self, child):
        if child not in self.__resultsWidgets:
            if isinstance(child, (list, tuple)):
                for ch in child: self.addResultsWidgets(ch)
            else: self.__resultsWidgets.append(child)
    
    @property
    def resultsWidgets(self): return self.__resultsWidgets
    
    def fill(self, values={}):
        if values:
            for widgetName in self.resultsWidgets:
                widget = self.getFromSelf(widgetName)
                if widget:
                    try: widget.set(values.get(widgetName, ''))
                    except Exception as er: print(f'ERROR {er}.')
                else: print(f'Error [{widgetName}, {widget}]')
            self.values = values
            return True
        else:
            if self.values: return self.fill(self.values)
FW = FillWidgets

class ImageWidget:
    def __init__(self, imageFile=None, thumb=None, resize=None):
        self.rt = None
        self.__image = None
        self.thumb = thumb or (200, 170)
        self.resize = resize or (100, 100)
        from .dialogs import PMB
        self.PMB = PMB
        
        self.default_dp = PRMP_Image('profile_pix', thumb=self.thumb)
        
        self.bindMenu()
        self.loadImage(imageFile=imageFile or self.default_dp)
        self.bindEntryHighlight()
        
        # self.set = partial(ImageWidget.set, self)
    
    
    def disabled(self):
        self.unBindMenu()
        super().disabled()
    
    def normal(self):
        self.bindMenu()
        super().normal()
    
    def loadImage(self, imageFile=None):
        if imageFile:
            if isinstance(imageFile, PRMP_Image): pass
            else: imageFile = PRMP_Image(imageFile, thumb=self.thumb)
            
            self.image = self.__image = imageFile

            if imageFile.ext == 'xbm': self.image = imageFile.resizeTk(self.resize)
            # else: self.image = imageFile.thumbnailTk(self.thumb)
            
            self.configure(image=self.image)
    
    def removeImage(self):
        if self.rt: self.rt.destroy()
        if not self.PMB(title='Profile Picture Removal', message='Are you sure you wanna remove the picture from this profile? ').result: return
        else: self.loadImage(imageFile=self.default_dp)
    
    def set(self, imageFile):
        if imageFile: self.loadImage(imageFile=imageFile)
    
    def changeImage(self, e=0):
        file = askopenfilename(filetypes=['Pictures {.jpg .png .jpeg .gif .xbm}'])
        if file: self.loadImage(imageFile=file)
    
    def bindMenu(self):
        self.bind('<1>', self.delMenu, '+')
        self.bind('<3>', self.showMenu, '+')
        # self.bind('<Double-1>', self.showMenu)
    
    def unBindMenu(self):
        self.unbind('<1>')
        self.unbind('<3>')
        # self.unbind('<Double-1>')
    
    def get(self): return self.__image
    
    def delMenu(self, e=0):
        if self.rt:
            self.rt.destroy()
            del self.rt
            self.rt = None
    
    def showMenu(self, e=0):
        self.delMenu()
        x, y = e.x, e.y
        x, y = e.x_root, e.y_root
        self.rt = rt = PRMP_Toplevel(self, geo=(50, 50, x, y))
        rt.overrideredirect(1)
        btn1 = PRMP_Button(rt, text='Change', command=self.changeImage, overrelief='sunken', font=PTh.DEFAULT_MENU_FONT)
        btn1.place(relx=0, rely=0, relh=.5, relw=1)
        
        btn2 = PRMP_Button(rt, config=dict(text='Remove', command=self.removeImage, overrelief='sunken'), font=PTh.DEFAULT_MENU_FONT)
        btn2.place(relx=0, rely=.5, relh=.5, relw=1)
        rt.attributes('-topmost', 1)
        rt.paint()
IW = ImageWidget

class ImageLabel(ImageWidget, PRMP_Label):
    def __init__(self, master, imageFile=None, resize=(), thumb=(), **kwargs):
        PRMP_Label.__init__(self, master, **kwargs)
        ImageWidget.__init__(self, imageFile=imageFile, thumb=thumb, resize=resize)
IL = ImageLabel

class PRMP_DateButton(PRMP_Button):
    def __init__(self, master=None, font=PTh.DEFAULT_FONT, asEntry=True, **kwargs):
        self.date = None
        from .dialogs import CalendarDialog, DateTime
        self.CD = CalendarDialog
        self.DT = DateTime
        super().__init__(master=master, command=self.action, font=font, asEntry=asEntry, anchor='nw', **kwargs)
    
    def action(self):
        self.date = self.CD(self).result
        self.set(str(self.date))
    
    def get(self): return self.date
    
    def set(self, date):
        if '-' in date: d, m, y = date.split('-')
        elif '/' in date: d, m, y = date.split('/')
        else: return
        self.date = self.DT.createDateTime(int(y), int(m), int(d))
        self['text'] = self.date
PDB = PRMP_DateButton

class ScrolledTreeView(AutoScroll, PRMP_Treeview):
    '''A standard ttk Treeview widget with scrollbars that will
    automatically show/hide as needed.'''
    @create_container
    def __init__(self, master, **kw):
        ttk.Treeview.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
STV = ScrolledTreeView

class ScrollableFrame(PRMP_Frame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.canvas = canvas = PRMP_Canvas(self, config=dict(bg='blue'))
        canvas.place(x=0, rely=0, relh=.96, relw=.99)
        
        # self.canvas.grid_rowconfigure(0, weight=1)
        
        xscrollbar = PRMP_Scrollbar(self, config=dict(orient="horizontal", command=canvas.xview))
        yscrollbar = PRMP_Scrollbar(self, config=dict(orient="vertical", command=canvas.yview))
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
        xscrollbar = PRMP_Scrollbar(self, config=dict(orient="horizontal", command=self.treeview.xview))
        yscrollbar = PRMP_Scrollbar(self, config=dict(orient="vertical", command=self.treeview.yview))
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
        self.setColumns(columns)
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
        if columns:
            self.columns.process(columns)
            
            if len(self.columns) > 1: self.tvc(columns=self.columns[1:])
            self.updateHeading()
            
    def updateHeading(self):
        for column in self.columns:
            self.heading(column.index, text=column.text, anchor='center')
            print(column.width, time.time())
            self.column(column.index, width=column.width, minwidth=80, stretch=1,  anchor="center")
    
    def _set(self, obj=None, parent='', op=False):
        
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
            for sub in subs: self._set(sub, item, op)
    
    def set(self, obj, op=0):
        self.updateHeading()
        if self.firstItem:
            self.tree.delete(self.firstItem)
            self.firstItem = None
        if obj:
            self.obj = obj
            self._set(obj, op=op)
    
    def reload(self): self.set(self.obj)
PTV = PRMP_TreeView

class ToolTip:
    def __init__(self, wdgt, msg=None, font=None, delay=1, follow=True, tipGeo=(100, 40), **kwargs):
        self.wdgt = wdgt
        self.parent = self.wdgt.master
        
        self.msg = msg

        self.tipGeo = tipGeo
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        self.top = None
        self.font = font
        self.kwargs = kwargs
        
        
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')
        

    def spawn(self, event=None):
        self.visible = 1
        self.wdgt.after(int(self.delay * 1000), self.show)

    def show(self):
        spl = self.msg.split('\n')
        c = 0
        for v in spl:
            i = len(v)
            if i > c: c = i
        
        r = len(spl)
        r = r or 1
        self.tipGeo = c * 7, r * 20

        self.top = PTp(self.parent, geo=self.tipGeo, ntb=1, tm=1, **self.kwargs)
        
        L(self.top, text=self.msg or 'No message provided', background=PTh.DEFAULT_BACKGROUND_COLOR, font=self.font, relief='groove').place(relx=0, rely=0, relh=1, relw=1)
        # self.withdraw()
        
        if self.visible == 1 and time.time() - self.lastMotion > self.delay: self.visible = 2
        if self.visible == 2: self.top.deiconify()
        
        self.top.mainloop()

    def move(self, event):
        if self.top:
            self.lastMotion = time.time()
            if self.follow is False:
                self.withdraw()
                self.visible = 1
            self.top.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
            
            #To get the present event coordinates
            # print(event.x_root,event.y_root)
            
            # self.top.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        if self.top:
            self.visible = 0
            # self.top.withdraw()
            self.top.destroy()
        # self.parent.state('normal')
TT = ToolTip

class SolidScreen(PRMP_MainWindow):
    def __init__(self, side='top-center', gaw=1, bd=12, geo=(),**kwargs):
        super().__init__(tm=1, gaw=gaw, geo=geo or (500, 500), side=side, **kwargs)
        
        self.container['bd'] = 12
        
        
        self.paint()
SS = SolidScreen













