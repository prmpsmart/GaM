from . import *
from .scrollables import *
from .two_widgets import *
from .dialogs import *
from .miscs import *
from prmp_lib.prmp_miscs.prmp_images import PRMP_DB

from .image_widgets import PRMP_ImageSButton
import math, os


class PRMP_FramedCanvas(Frame):
    def __init__(self, master, canvasConfig={}, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = Canvas(self, **canvasConfig, place=dict(relx=.005, rely=.005, relh=.99, relw=.99))


class PRMP_Entry_Label(Label):
    def __init__(self, master, font='DEFAULT_FONT', **kwargs): super().__init__(master, asEntry=True, font=font, **kwargs)
Entry_Label = PRMP_Entry_Label


class Tushed_Entry(Frame):
    imageLoaded = False
    res = (20, 20)
    dic = dict(inbuilt=1, resize=res, for_tk=1)

    def __init__(self, master, font={}, action=None, show='*', entryKwargs={}, reliefs='', positions=(1, 0, 0, 0, 0), _pass=None, **kwargs):
        '''
        a Login widget that features a show button and action button.
        positions: tuple of three floats relating the width of the (entry, pass, show, clear, action) summing up to one.
        '''
        super().__init__(master, **kwargs)
        
        _f = font
        font = font if isinstance(font, (dict, str, tuple)) else self.PRMP_FONT.copy()
        
        if isinstance(_f, (float, int)): font['size'] = _f or 20

        if reliefs: entryKwargs['relief'] = reliefs

        self.entry = Entry(self, show=show, font=font, **entryKwargs)
        # self.entry.focus()

        self.set = self.entry.set
        self.get = self.entry.get
        self._pass = _pass
        
        self.positions = positions
        self.reliefs = reliefs
        self.show = show
        self._action = action

        self.loaded = False
        # self.bind('<Map>', self.load)
        self.bind('<Configure>', lambda e: self.load(self.positions))
    
    def load(self, positions=(), again=False):

        if self.loaded==True and again==False: return

        positions = positions or self.positions
        assert len(positions) == 5 , 'Length of positions must be 5.'
        assert math.fsum(positions) == 1, 'Sum of positions must be 1.0,'

        self.positions = positions

        self.view = self.clear = self.action = self.pass_ = None

        tip = self.toplevel.tipping
        e, p, s, c, a = self.positions
        
        self.entry.place(relx=0, rely=0, relw=e, relh=1)

        if p:
            self._passes = PRMP_Image(filename='button_blank_red', name='red_pass', **self.dic), PRMP_Image(filename='button_blank_yellow', name='yellow_pass', **self.dic), PRMP_Image(filename='button_blank_green', name='green_pass', **self.dic)

            self.pass_ = PRMP_ImageSButton(self, place=dict(relx=e, rely=0, relw=p, relh=1), config=dict(style='buttons.TButton'))
            self.after(100, self.validating)
            self.entry.bind('<KeyRelease>', self.validating)

        if s:
            self.show = PRMP_ImageSButton(self, place=dict(relx=e+p, rely=0, relw=s, relh=1), imageKwargs=dict(**self.dic, prmpImage='highlighter_blue'), config=dict(style='buttons.TButton'))

            self.show.bind('<ButtonPress-1>', lambda e: self.entry.configure(show=''))
            self.show.bind('<ButtonRelease-1>', lambda e: self.entry.configure(show=self.show))
        else: self.entry.config(show='')
        
        if c:
            self.clear = PRMP_ImageSButton(self, place=dict(relx=e+s+p, rely=0, relw=c, relh=1), imageKwargs=dict(**self.dic, prmpImage='gtk_cancel'), config=dict(style='buttons.TButton'))

            self.clear.bind('<1>', self.empty)

        if a:
            self.action = PRMP_ImageSButton(self, place=dict(relx=e+s+p+c, rely=0, relw=a, relh=1), imageKwargs=dict(**self.dic, prmpImage='button_next'), config=dict(style='buttons.TButton'))
            self.entry.bind('<Return>', self.invokeAction)

        self.loaded = True
        Tushed_Entry.imageLoaded = True
    
    def empty(self, event=None):
        self.entry.empty()
        self.validating(event)
    
    def validating(self, event=None):
        if self._pass and self.pass_:
            num = self._pass(self.entry.get())
            if  num == 1: fg = "yellow"
            elif num == 2: fg = "green"
            else: fg = "red"

            self.pass_['image'] = fg+'_pass'
            # self.pass_.config(image=fg+'_pass', bg=self.DEFAULT_BACKGROUND_COLOR, relief='groove')
            # self.pass_.paint()
    
    def invokeAction(self, event=None):
        try: self.action.invoke()
        except: pass

    def __getattr__(self, name):
        try:
            res = self.getFromSelf(name, None)
            if not res: raise AttributeError
            return res
        except Exception as e:
            res = self.entry.getFromSelf(name, None)
            return res

    def setAction(self, action=None, _pass=None):
        if action: self.action.config(command=action)
        if _pass: self._pass = _pass

    def getFromSelf(self, *args): return self.entry.getFromSelf(*args)


class ChoosePath(LabelText):
    def __init__(self, master, text='', callback=None, folder=0, bottomKwargs={}, customFont=0, **kwargs):
        if customFont:
            FONT = self.PRMP_FONT
            FONT['size'] = 20
        else: FONT = 'DEFAULT_FONT'

        tip = self.topest.tipping
        image = None

        if folder:
            self.image = PRMP_Image('folder_add', resize=(25, 25), inbuilt=1, inExt='png', for_tk=1)
            pathType = 'dir'
        else:
            if PRMP_DB:
                image = PRMP_DB.getImage('soft_scraps', 'file_open')[0]
                self.image = PRMP_Image(image, resize=(25, 25), for_tk=1)
            pathType = 'file'
        
        bottomKwargs.update(dict(_type=pathType))

        super().__init__(master, topKwargs=dict(text=text, font=FONT, image=self.image, compound='left'), tipKwargs=dict(text='Double-click to choose folder!') if tip else {}, bottomKwargs=bottomKwargs, **kwargs)


        self.T.bind('<Double-1>', self.load_dir)
        self.T.bind('<1>', self.read_dir)
        self.B.bind('<Double-1>', self.load_dir)

        self._folder = folder
        self.path = ''
        self.callback = callback

    def read_dir(self, event):
        path = self.B.get()
        self._set(path)

    def load_dir(self, event):
        path = dialogFunc(path=1, folder=self._folder)
        self._set(path)

    
    def _set(self, path):
        func = os.path.isdir if self._folder else os.path.isfile
        if path and func(path):
            self.path = path
            self.B.set(path)
            if self.callback: self.callback(path)


class AttributesViewer(LabelFrame):

    def __init__(self, master, attr='', obj=None, dialog=None, **kwargs):
        super().__init__(master, **kwargs)
        from .two_widgets import LabelLabel, LabelEntry, LabelText, TwoWidgets

        self.dialog = dialog
        if not self.dialog:
            from .dialogs import dialogFunc
            self.dialog = dialogFunc

        self.obj = obj
        self.attr = attr

        self._value = self.obj[self.attr]
        self._type = type(self._value)

        self.name = LabelEntry(self, place=dict(relx=0, rely=0, relh=.15, relw=1), topKwargs=dict(text='attr Name'), bottomKwargs=dict(state='readonly'), orient='h', longent=.3)

        self.name.set(self.attr)

        self.value = LabelText(self, place=dict(relx=0, rely=.15, relh=.45, relw=1), topKwargs=dict(text='attr Value'), bottomKwargs=dict(state='disabled'), orient='h', longent=.3)

        self.value.set(self._value)

        self.valueType = LabelEntry(self, place=dict(relx=0, rely=.6, relh=.15, relw=1), topKwargs=dict(text='value Type'), bottomKwargs=dict(state='readonly'), orient='h', longent=.23)

        self.valueType.set(self._type)

        self.mastertype = TwoWidgets(self, place=dict(relx=0, rely=.76, relh=.14, relw=1), topKwargs=dict(text='master Type', command=self.openMaster), bottomKwargs=dict(state='readonly'), orient='h', longent=.22, top=Button, bottom='entry')

        self.mastertype.set(type(self.obj))

        self.details = Button(self, text='Further Details', place=dict(relx=0, rely=.9, relh=.1, relw=1), command=self.open)

    def openMaster(self): self.dialog(obj=self.obj)

    def open(self):
        if isinstance(self._value, (int, str, list, tuple, dict)): AttributesExplorer(values=self._value, dialog=self.dialog, grab=0)
        else: self.dialog(obj=self._value, grab=0, tm=1)


class AttributesExplorer(LabelFrame):
    def __init__(self, master, listboxConfig={}, callback=None, obj=None, values={}, dialog=None, **kwargs):
        super().__init__(master, **kwargs)
        from .two_widgets import LabelLabel, LabelEntry, LabelText, TwoWidgets

        self.dialog = dialog
        self.callback = callback
        self.obj = obj

        frame1 = Frame(self, place=dict(relx=0, rely=0, relw=.44, relh=1))

        Label(frame1, text='Top Attrs', place=dict(relx=0, rely=0, relw=1, relh=.07))

        self.listbox = ListBox(frame1, place=dict(relx=0, rely=.08, relh=.84, relw=1), listboxConfig=dict(config=dict(selectmode='multiple'), values=values), bindings=[('<Return>', self.clicked, '')])

        self.total = LabelLabel(frame1, place=dict(relx=0, rely=.93, relh=.07, relw=.6), orient='h', bottomKwargs=dict(font='DEFAULT_FONT'), longent=.4, topKwargs=dict(text='Total'))

        Button(frame1, text='Open', place=dict(relx=.65, rely=.93, relh=.07, relw=.25), command=self.openAttribute)

        PRMP_Separator(self, place=dict(relx=.445, rely=0, relh=1, relw=.05), config=dict(orient='vertical'))

        frame2 = Frame(self, place=dict(relx=.455, rely=0, relw=.545, relh=1))

        self.treeview = PRMP_Treeview(frame2, place=dict(relx=0, rely=0, relh=.8, relw=1))
        self.treeview.heading('#0', text='Attributes')
        self.ivd = self.treeview.ivd
        self.treeview.bind('<Delete>', self.deleteAttribute, '+')

        self.entry = LabelEntry(frame2, place=dict(relx=0, rely=.81, relw=.65, relh=.085), orient='h', longent=.25, topKwargs=dict(text='New'), bottomKwwargs=dict(placeholder=''))
        self.entry.B.bind('<Return>', self.addAtrribute, '+')

        self.top = Checkbutton(frame2, text='Top?', place=dict(relx=.7, rely=.815, relh=.07, relw=.25))

        Button(frame2, text='Delete', place=dict(relx=.1, rely=.915, relh=.07, relw=.25), command=self.deleteAttribute)
        Button(frame2, text='Get', place=dict(relx=.65, rely=.915, relh=.07, relw=.25), command=self.getAttributes)

        self._foc = None

        if obj and not values:
            keys = list(obj.__dict__.keys())
            values = [key.strip('_') for key in keys if '__' not in key]
            values.sort()

        self.values = values
        self.set(values)

    def openAttribute(self):
        from .tushed_windows import PRMP_MsgBox, AttributesViewerDialog

        if not self.obj: PRMP_MsgBox(self, title='Object Error', message='No object is given!')

        attrs = self.getAttributes()
        if attrs:
            leng = len(attrs)

            if not leng: PRMP_MsgBox(self, title='Attribute Error', message='Choose an attribute from the listbox!')
            elif leng > 1: PRMP_MsgBox(self, title='Attribute Error', message='Choose only one attribute from the listbox!')
            else:
                attr = attrs[0]
                # value = self.obj[attr]
                # openCores(obj=value)
                AttributesViewerDialog(attr=attr, obj=self.obj, dialog=self.dialog, tm=0, grab=0)

    def addAtrribute(self, e=0):
        get = self.entry.get()
        if not get: return
        item = '' if self.top.get() else self.treeview.focus()
        self.treeview.insert(item, text=get)
        # self.treeview.focus('')
        self.setListBox()
        self.entry.B.clear()

    def deleteAttribute(self, e=0):
        self._foc = focus = self.treeview.focus()

        _all = 'all attributes' if not focus else f'this attribute --> {self.ivd[focus]}'

        from .dialogs import PRMP_MsgBox

        PRMP_MsgBox(self, title='Delete Attribute', message=f'Are you sure to delete {_all}', ask=1, callback=self._delete)

    def _delete(self, w):
        if w:
            if not self._foc: self.treeview.deleteAll()
            else: self.treeview.delete(self._foc)
        self.setListBox()

    def setListBox(self):
        self.listbox.clear()
        tops = self.treeview.get_children()
        for top in tops: self.listbox.insert(self.ivd[top])
        self.total.set(self.listbox.last)

    def clicked(self, event=None, selected=None):
        selected = self.listbox.selected
        self.treeview.see

    def set(self, values):
        if not values: return
        self.values = values
        self.setTreeview(values)
        self.setListBox()

    def getAttributes(self):
        tops = self.treeview.getChildren()
        listbox = self.listbox.curselection()
        if not listbox: listbox = range(self.listbox.last)
        result = [tops[num] for num in listbox] if isinstance(tops, (tuple, list)) else [tops]

        if self.callback: self.callback(result)
        else: return result


    def setTreeview(self, values, parent=''):
        if isinstance(values, list):
            for value in values: self.setTreeview(value, parent)

        elif isinstance(values, dict):
            for key, value in values.items():
                item = self.treeview.insert(parent, text=key)
                self.setTreeview(value, item)

        elif isinstance(values, (str, bytes)):
            self.treeview.insert(parent, text=values)
            pass


class ColumnViewer(LabelFrame):

    def __init__(self, master, column=None, **kwargs):
        super().__init__(master, **kwargs)
        from .two_widgets import LabelEntry

        self.text = LabelEntry(self, place=dict(relx=0, rely=0, relh=.2, relw=1), topKwargs=dict(text='text'), orient='h', longent=.3)

        self.attr = LabelEntry(self, place=dict(relx=0, rely=.2, relh=.2, relw=1), topKwargs=dict(text='attr'), orient='h', longent=.3)

        self.value = LabelEntry(self, place=dict(relx=0, rely=.4, relh=.2, relw=1), topKwargs=dict(text='value'), orient='h', longent=.3)

        self._width = LabelEntry(self, place=dict(relx=0, rely=.6, relh=.2, relw=1), topKwargs=dict(text='width'), orient='h', longent=.3)

        if column:
            self.text.set(column.text)
            self.attr.set(column.attr)
            self.value.set(column.value)
            self._width.set(column.width)

    def openMaster(self):
        from .dialogs import dialogFunc
        dialogFunc(master=self, obj=self.obj)

    def open(self):
        from .dialogs import dialogFunc, ColumnsExplorerDialog
        if isinstance(self._value, (int, str, list, tuple, dict)): ColumnsExplorerDialog(self, values=self._value)
        else: dialogFunc(master=self, obj=self._value)


class ColumnsExplorer(PRMP_FillWidgets, LabelFrame):
    def __init__(self, master, listboxConfig={}, callback=None, columns=None, masterWid=None, **kwargs):

        LabelFrame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self)

        self.callback = callback
        self.columns = columns
        self.masterWid = masterWid

        _cols = ['text', 'attr', 'width', 'value']

        frame1 = Frame(self, place=dict(relx=0, rely=0, relw=.3, relh=1))

        Label(frame1, text='Columns', place=dict(relx=0, rely=0, relw=1, relh=.07))

        self.listbox = ListBox(frame1, place=dict(relx=0, rely=.08, relh=.84, relw=1), listboxConfig=dict(config=dict(selectmode='multiple')), bindings=[('<Return>', self.clicked, '')])

        self.total = LabelLabel(frame1, place=dict(relx=0, rely=.93, relh=.07, relw=.6), orient='h', bottomKwargs=dict(font='DEFAULT_FONT'), longent=.4, topKwargs=dict(text='Total'))

        PRMP_Separator(self, place=dict(relx=.305, rely=0, relh=1, relw=.05), config=dict(orient='vertical'))

        frame2 = Frame(self, place=dict(relx=.315, rely=0, relw=.685, relh=1))

        self.treeview = Hierachy(frame2, place=dict(relx=0, rely=0, relh=.7, relw=1), columns=_cols)
        self.treeview.treeview.bind('<Delete>', self.deleteColumn, '+')

        self.text = LabelEntry(frame2, place=dict(relx=.0, rely=.71, relw=.5, relh=.085), orient='h', longent=.23, topKwargs=dict(text='text'), bottomKwargs=dict(_type='text', required=True))
        self.attr = Button(frame2, place=dict(relx=.55, rely=.71, relw=.1, relh=.085), text='attr', command=self.getAttr)
        self._width = LabelEntry(frame2, place=dict(relx=0, rely=.8, relw=.3, relh=.085), orient='h', topKwargs=dict(text='width'), bottomKwargs=dict(_type='number'))
        self.value = LabelEntry(frame2, place=dict(relx=.35, rely=.8, relw=.3, relh=.085), orient='h', longent=.4,  topKwargs=dict(text='value'), bottomKwargs=dict(_type='text'))

        Button(frame2, text='Get', place=dict(relx=.8, rely=.75, relh=.15, relw=.15), command=self.getColumns)

        Button(frame2, text='Delete', place=dict(relx=.1, rely=.915, relh=.07, relw=.25), command=self.deleteColumn)
        Button(frame2, text='Add', place=dict(relx=.45, rely=.915, relh=.07, relw=.25), command=self.addColumn)

        self._foc = None
        self._focObj = None
        self._attr = ''

        self.set(columns)
        self._cols = _cols

        self.addResultsWidgets(_cols)

    def width(self): return self._width

    def addColumn(self, e=0):
        gets = self.get(['text', '_width', 'value'])
        gets['attr'] = self._attr
        width = gets['_width'] or 20
        gets['width'] = int(width)
        try: j = self.columns.addColumn(gets)
        except:
            from .dialogs import PRMP_MsgBox
            PRMP_MsgBox(self, title='Error', _type='error', message='Try to add the "attr" value.')
        self._attr = ''

        self.set(self.columns)

    def getAttr(self):
        from .dialogs import AttributesExplorerDialog
        AttributesExplorerDialog(callback=self.setAttr)

    def setAttr(self, attr):
        if attr: self._attr = attr[0]

    def deleteColumn(self, e=0):
        from .dialogs import PRMP_MsgBox

        self._foc = focus = self.treeview.treeview.focus()
        if not focus: PRMP_MsgBox(self, title='No Selection.n', message='Pick a row to delete.')

        self._focObj = self.treeview.treeview.ivd[focus]

        _all = 'all Columns' if not focus else f'this Column --> {self._focObj.index}'

        PRMP_MsgBox(self, title='Delete Column', message=f'Are you sure to delete {_all}', ask=1, callback=self._delete)

    def _delete(self, w):
        if w:
            if not self._foc: return
            else:
                self.treeview.treeview.delete(self._foc)
                # self.columns.remove(self._focObj)
                self.updateCol()

        self.setListBox()

    def setListBox(self):
        self.listbox.clear()
        tops = self.columns

        if tops:
            for top in tops:
                text = top.text
                self.listbox.insert(text)
            last = self.listbox.last
        else: last = 0

        self.total.set(last)

    def clicked(self, event=None, selected=None):
        selected = self.listbox.selected
        self.treeview.see

    def set(self, columns):
        if not columns: return

        self.columns = columns if isinstance(columns, Columns) else Columns(columns)

        self.treeview.treeview.deleteAll()
        self.treeview.viewSubs(self.columns)

        self.setListBox()

    def updateCol(self, listbox=[]):
        tops = self.treeview.treeview.getChildren()
        listbox = listbox or range(len(tops))

        result = [tops[num] for num in listbox] if isinstance(tops, (tuple, list)) else [tops]

        results = [dict(text=res.text, attr=res.attr, width=res.width, value=res.value) for res in result]

        self.columns.process(results)

    def getColumns(self, e=0):
        listbox = self.listbox.curselection()
        self.updateCol(listbox)

        if self.callback: self.callback(self.columns, e)

    # def setTreeview(self, values, parent=''):
    #     if isinstance(values, list):
    #         for value in values: self.setTreeview(value, parent)

    #     elif isinstance(values, dict):
    #         for key, value in values.items():
    #             item = self.treeview.insert(parent, text=key)
    #             self.setTreeview(value, item)

    #     elif isinstance(values, (str, bytes)):
    #         self.treeview.insert(parent, text=values, value=values)
    #         pass

