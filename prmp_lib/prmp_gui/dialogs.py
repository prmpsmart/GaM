
from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime
from prmp_lib.prmp_miscs.prmp_mixins import PRMP_ClassMixins
from prmp_lib.prmp_miscs.prmp_pics import PRMP_XBMS
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from tkinter.simpledialog import askstring, askfloat, askinteger
from . import *
from .core import PRMP_FillWidgets



class PRMP_Dialog(PRMP_MainWindow, PRMP_FillWidgets, PRMP_ClassMixins):

    def __init__(self, master=None, _return=True, values={}, ntb=1, nrz=0, tm=1, gaw=1, tw=1, editable=True, callback=None, show=1, grab=1, bell=False, delay=0, tt=False, tooltype=False, wait=False, **kwargs):

        self.tooltype = tt or tooltype
        if self.tooltype: grab = 0

        PRMP_MainWindow.__init__(self, master, ntb=ntb, nrz=nrz, tm=tm, gaw=gaw, tw=tw, grab=grab, tooltype=self.tooltype, **kwargs)

        PRMP_FillWidgets.__init__(self, values=values)

        self.__result = None
        self.callback = callback
        self._return = _return

        self.submitBtn = None
        self.editBtn = None

        self._setupDialog()
        self.set()

        if editable:
            if values: self.editInput(0)
            else: self.editInput(1)

        self.defaults()

        self.paint()
        if bell: self.bell()

        self.focus()
        if delay: self.after(delay, self.destroy)

        if self.tooltype: self.withdraw()
        elif wait: self.wait_window()
        elif show: self.mainloop()


    def _setupDialog(self):
        'This is to be overrided in subclasses of PRMPDialog to setup the widgets into the dialog.'

    def defaults(self):
        # self.grab_set()
        # self.wait_window()
        pass

    @property
    def result(self): return self.__result

    def _setResult(self, result): self.__result = result

    def addSubmitButton(self):
        self.submitBtn = PRMP_Button(self.container, config=dict(text='Submit', command=self.processInput))

    def bindCR(self): self.bind('<Control-Return>', self.processInput)
    def unbindCR(self): self.unbind('<Control-Return>')

    def _placeSubmitButton(self):
        x, y = self.containerGeo
        self.submitBtn.place(x=(x/2)-30 , y=y-40, h=30, w=60)

    def placeSubmitBtn(self, wh=0):
        if wh:
            self.bindCR()
            self.container.paint()
            geo = self.kwargs.get('geo')
            self._placeSubmitButton()
        else:
            self.unbindCR()
            self.submitBtn.place_forget()

    def addEditButton(self):
        if self.submitBtn == None: self.addSubmitButton()
        x, y = self.containerGeo
        self.editBtn = PRMP_Style_Checkbutton(self.container, config=dict(text='Edit', command=self.editInput))
        self.editBtn.place(x=10 , y=y-40, h=30, w=60)

    def processInput(self, e=0):
        result = self.get()
        # result = {'address': 'lklk', 'email': 'awa.@asd.asa', 'gender': 'Male', 'name': 'Aderemi Goodness', 'phone': '2121', 'regDate': PRMP_DateTime(2020, 12, 30, 0, 54, 19)}
        if result:
            self._setResult(result)
            self.action()
            self.save()

        else: PRMP_MsgBox(self, title='No Input Error', message='No input whatsoever is given.', _type='error', ask=0)

    def action(self): print('redefine this method for functionality')

    def save(self): print('redefine this method for functionality')

    def editInput(self, e=0):
        if self.editBtn == None: return
        if e: self.editBtn.set('1')
        if self.editBtn.get(): self.placeSubmitBtn(1)
        else: self.placeSubmitBtn()
        for widgetName in self.resultsWidgets:
            wid = self[widgetName]
            if self.editBtn.get(): wid.normal()
            else: wid.disabled()

    def destroyDialog(self):
        if self.tooltype: self.withdraw()
        elif self._return: self.destroy()

        if self.callback: self.callback(self.result)

PD = PRMP_Dialog

class PRMP_CalendarDialog(PRMP_Dialog):

    def __init__(self, master=None, month=None, title='PRMP_Calendar Dialog', geo=(300, 300), min_=None, max_=None, date=None, **kwargs):
        self.min = min_
        self.max = max_
        self.month = date or month

        super().__init__(master, title=title, geo=geo, editable=False, **kwargs)

    def _setupDialog(self): self.calendar = self.addWidget(PRMP_Calendar, config=dict(callback=self.getDate, max_=self.max, min_=self.min, month=self.month), place=dict(relx=0, rely=0, relh=1, relw=1))

    def afterPaint(self): self.calendar.afterPaint()

    def getDate(self, date):
        self._setResult(date)
        if self._return:
            PRMP_Calendar.choosen = None
            self.destroyDialog()

    def validate_cmd(self, date): return PRMP_DateTime.getDMYFromDate(date)

    def set(self, date=None):
        date = super().getDate(date)
        if date:
            self.calendar.month = date
            self.calendar.updateDays()

CD = PRMP_CalendarDialog

class PRMP_MessageDialog(PRMP_Dialog):
    _bitmaps = ['info', 'question', 'error', 'warning']
    def __init__(self, master=None, geo=(350, 160), title='Message Dialog', message='Put your message here.', _type='info', cancel=0, ask=0, okText='', msgFont='DEFAULT_FONT', plenty=0, bell=0, msg='', delay=3000, **kwargs):

        message = msg or message

        self.plenty = plenty
        self.message = message
        self.msgFont = msgFont
        self._type = _type
        self.okText = okText
        self._cancel = cancel

        if kwargs.get('callback'): ask = 1
        if okText: ask = 0

        if ask: delay = 0
        # print(ask, delay)
        self.ask = ask

        super().__init__(master, title=title, geo=geo, tm=1, asb=0, editable=False, grab=1, bell=bell, delay=delay, **kwargs)

    def _setupDialog(self):
        self.placeContainer(h=self.geo[1]-50)
        if self.plenty: self.label = PRMP_Text(self.container, state='disabled')
        else: self.label = PRMP_Label(self.container, config=dict(bitmap='', wraplength=250), font='PRMP_FONT')

        self.label.set(self.message)
        self.label.place(x=0, y=0, relh=.75, relw=.85)

        self.bitmap = PRMP_Label(self.container, config=dict(bitmap=self.getType(self._type)))
        self.bitmap.place(relx=.85, y=0, relh=1, relw=.15)

        self.yes = PRMP_Button(self, config=dict(text='Yes' if self.ask else self.okText or 'Ok', command=self.yesCom))

        if not self.ask:
            self.yes.place(relx=.3, rely=.83, relh=.15, relw=.37)
            self.bind('<Return>', lambda e: self.yes.invoke())
        else:
            self.yes.place(relx=.06, rely=.83, relh=.15, relw=.17)
            self.bind('<Y>', lambda e: self.yes.invoke())
            self.bind('<y>', lambda e: self.yes.invoke())

            self.no = PRMP_Button(self, config=dict(text='No', command=self.noCom), place=dict(relx=.63, rely=.83, relh=.15, relw=.17))
            self.bind('<N>', lambda e: self.no.invoke())
            self.bind('<n>', lambda e: self.no.invoke())

        if self._cancel:
            self.cancel = PRMP_Button(self, config=dict(text='Cancel', command=self.cancelCom))
            self.cancel.place(relx=.33, rely=.83, height=28, relw=.2)
        self.yes.focus()

    def getType(self, _type):
        if _type in self._bitmaps: return _type
        elif _type in self._xbms: return f'@{self._xbms[_type]}'

    @property
    def _xbms(self): return PRMP_XBMS

    def yesCom(self):
        if self.ask: self._setResult(True)
        self.destroyDialog()

    def cancelCom(self):
        self._setResult(None)
        self.destroyDialog()

    def noCom(self):
        self._setResult(False)
        self.destroyDialog()

PMB = PRMP_MsgBox = PRMP_MessageDialog

class PRMP_CameraDialog(PRMP_Dialog):

    def __init__(self, master=None, title='PRMP_Camera Dialog', cameraKwargs={}, **kwargs):
        self.cameraKwargs = cameraKwargs
        super().__init__(master, title=title, **kwargs)

    def isMaximized(self): return self.getWid_H_W(self)

    def _setupDialog(self):
        from .imagewidgets import PRMP_Camera
        self.camera = PRMP_Camera(self.container, place=dict(relx=.01, rely=.01, relh=.98, relw=.98), callback=self.getImage, config=dict(relief='flat'), **self.cameraKwargs)
        self.set = self.camera.setImage

    def getImage(self, imageFile):
        self._setResult(imageFile)
        if not self.callback: return PRMP_Camera._saveImage(imageFile)
        self.destroyDialog()

    # def

    def __del__(self): del self.camera
CamD = PRMP_CameraDialog

class PRMP_ImageDialog(PRMP_Dialog):

    def __init__(self, master=None, prmpImage=None, title='Image Dialog', imageKwargs={}, **kwargs):
        self.prmpImage = prmpImage
        self.imageKwargs = imageKwargs
        # print(kwargs)
        super().__init__(master, title=title, **kwargs)

    # def isMaximized(self): return self.getWid_H_W(self)

    def _setupDialog(self):
        self.imageKwargs['bindMenu'] = 1
        self.imageLabel = PRMP_ImageSLabel(self.container, prmpImage=self.prmpImage, place=dict(relx=.01, rely=.01, relh=.98, relw=.98), callback=self.getImage, config=dict(relief='flat'), imageKwargs=self.imageKwargs)
        self.set = self.imageLabel.set
        # self.bind('<Return>', self.imageLabel.saveImage)

    def getImage(self, imageFile):
        self._setResult(imageFile)
        self.destroyDialog()
    
    def setImage(self, image): self.imageLabel.loadImage(image)

ImgD = PRMP_ImageDialog

class Splash(PRMP_Dialog):
    def __init__(self, master=None, prmpImage='', ntb=1, atb=0, asb=0, geo=(800, 500), callback=None, title='Goodness and Mercy', imageKwargs={}, delay=2000, **kwargs):

        self.prmpImage = prmpImage
        self.delay = delay
        self.imageKwargs = imageKwargs

        super().__init__(master, atb=atb, asb=asb, ntb=ntb, geo=geo, title=title, editable=0, callback=callback, **kwargs)

    def _setupDialog(self):
        asb = self.addStatusBar
        if asb: cont = self.container
        else:
            cont = self
            self.container.place_forget()

        self.imageKwargs['bindMenu'] = 0
        self.imageKwargs['imgDelay'] = 0

        self.image = PRMP_ImageLabel(cont, prmpImage=self.prmpImage, place=dict(relx=0, rely=0, relw=1, relh=.9), resize=self.geo, imageKwargs=self.imageKwargs)

        self.load = PRMP_ImageLabel(cont, prmpImage='line_boxes', place=dict(relx=0, rely=.9, relw=1, relh=.1), imageKwargs=dict(inbuilt=1, inExt='gif'), resize=(280, 50))

        # self.after(self.delay, self.destroy)
        self.after(self.delay, self.processCallback)

    def processCallback(self):
        if self.callback: self.callback(self.destroy)
        else: self.after(10, self.processCallback)

    def set(self): pass






class AttributesExplorerDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Attributes Explorer Dialog', geo=(600, 500), obj=None, dialog=None, **kwargs):
        self.obj = obj
        self.dialog = dialog
        super().__init__(master, title=title, geo=geo, **kwargs)

    def _setupDialog(self): AttributesExplorer(self.container, place=dict(relx=.02, rely=.02, relh=.96, relw=.96), values=self.values, obj=self.obj,  dialog=self.dialog, callback=self._callback)

    def _callback(self, w):
        if self.callback:
            self.callback(w)
            self.destroy()



class AttributesViewerDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Attributes Viewer Dialog', geo=(700, 300), obj=None, attr=None, dialog=None, **kwargs):
        self.attr = attr
        self.obj = obj
        self.dialog = dialog
        super().__init__(master, title=title, geo=geo, **kwargs)

    def _setupDialog(self): AttributesViewer(self.container, place=dict(relx=.02, rely=.02, relh=.96, relw=.96), attr=self.attr, obj=self.obj, dialog=self.dialog)











def showDialog(title=None, msg=None, which=None):
    if which == 'error': messagebox.showerror(title, msg)
    elif which == 'info': messagebox.showinfo('Information', msg)
    elif which == 'warn': messagebox.showwarning('Warning', msg)

def confirmDialog(title=None, msg=None, which=None):
    if which == 1: return messagebox.askyesno(title, msg)
    if which == 2: return messagebox.askquestion(title, msg)
    if which == 3: return messagebox.askokcancel(title, msg)
    if which == 4: return messagebox.askretrycancel(title, msg)
    if which == 5: return messagebox.askyesnocancel(title, msg)

def askPath(opened=False, folder=False, many=False, save=False, **kwargs):
    if folder == False:
        if opened == False:
            if many == False:
                if save == False: return filedialog.askopenfilename(**kwargs)
                else: return filedialog.asksaveasfilename(**kwargs)
            else: return filedialog.askopenfilenames(**kwargs)
        else:
            if many == False:
                if save == False: return filedialog.askopenfile(**kwargs)
                else: return filedialog.asksaveasfile(**kwargs)
            else: return filedialog.askopenfiles(**kwargs)
    else: return filedialog.askdirectory(**kwargs)

def dialogFunc(*args, ask=0, path=0, obj=None, int_=0, float_=0, string=0, **kwargs):
    if obj:
        if isinstance(obj, PRMP_DateTime): PRMP_CalendarDialog(month=obj, **kwargs)
        elif isinstance(obj, (PRMP_Image, PRMP_ImageFile)): PRMP_ImageDialog(image=obj, **kwargs)
        elif isinstance(obj, Columns): ColumnsExplorerDialog(columns=obj, **kwargs)
        elif isinstance(obj, Column): ColumnViewerDialog(column=obj, **kwargs)
    elif path: return askPath(**kwargs)
    elif ask: return confirmDialog(**kwargs)
    elif string: return askstring(*args, **kwargs)
    elif float_: return askfloat(*args, **kwargs)
    elif int_: return askinteger(*args, **kwargs)
    else: return showDialog(**kwargs)
