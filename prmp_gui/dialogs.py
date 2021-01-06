
from prmp_miscs.prmp_datetime import PRMP_DateTime
from .extensions import *
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog


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

def askPath(opened=False, folder=False, many=False, save=False):
    if folder == False:
        if opened == False:
            if many == False:
                if save == False: return filedialog.askopenfilename()
                else: return filedialog.asksaveasfilename()
            else: return filedialog.askopenfilenames()
        else:
            if many == False:
                if save == False: return filedialog.askopenfile()
                else: return filedialog.asksaveasfile()
            else: return filedialog.askopenfiles()
    else: return filedialog.askdirectory()

def dialogFunc(ask=0, path=0, **kwargs):
    if path: return askPath(**kwargs)
    elif ask: return confirmDialog(**kwargs)
    else: return showDialog(**kwargs)



class PRMP_Dialog(PRMP_MainWindow, PRMP_FillWidgets):
    
    def __init__(self, master=None, _return=True, values={}, ntb=1, nrz=0, tm=1, gaw=1, tw=1, editable=True, callback=None, show=1, grab=1, **kwargs):

        PRMP_MainWindow.__init__(self, master, ntb=ntb, nrz=nrz, tm=tm, gaw=gaw, tw=tw, **kwargs)
        PRMP_FillWidgets.__init__(self, values=values)

        self.__result = None
        self.callback = callback
        self._return = _return

        self.submitBtn = None
        self.editBtn = None
        
        self._setupDialog()
        self.set()

        self.paint()
        self.default()
        
        if editable:
            if values: self.editInput(0)
            else: self.editInput(1)
        
        if grab: self.grab_set()
        
        self.mainloop()
        # if show: self.mainloop()
        # else: self.wait_window()
        
    
    def _setupDialog(self):
        'This is to be overrided in subclasses of PRMPDialog to setup the widgets into the dialog.'

    def default(self):
        # self.grab_set()
        # self.wait_window()
        pass

    def destroyDialog(self):
        if self.callback: self.callback(self.result)

        if self._return: self.destroy()

    @property
    def result(self): return self.__result
    
    def _setResult(self, result): self.__result = result
    
    def addSubmitButton(self):
        self.submitBtn = PRMP_Button(self.container, config=dict(text='Submit', command=self.processInput))
    
    def bindCR(self): self.bind('<Control-Return>', self.processInput)
    def unbindCR(self): self.unbind('<Control-Return>')
    
    def placeSubmitBtn(self, wh=0):
        if wh:
            self.bindCR()
            self.container.paint()
            geo = self.kwargs.get('geo')
            x, y = self.containerGeo
            self.submitBtn.place(x=(x/2)-30 , y=y-40, h=30, w=60)
        else:
            self.unbindCR()
            self.submitBtn.place_forget()
    
    def addEditButton(self):
        if self.submitBtn == None: self.addSubmitButton()
        x, y = self.containerGeo
        self.editBtn = xbtn = PRMP_Style_Checkbutton(self.container, config=dict(text='Edit', command=self.editInput))
        xbtn.place(x=10 , y=y-40, h=30, w=60)
    
    def processInput(self, e=0):
        result = self.get()
        # result = {'address': 'lklk', 'email': 'awa.@asd.asa', 'gender': 'Male', 'name': 'Aderemi Goodness', 'phone': '2121', 'regDate': PRMP_DateTime(2020, 12, 30, 0, 54, 19), 'image': self.image.get()}
        self._setResult(result)
        self.action()

    def action(self): print('redefine this method for functionality')
        
    def editInput(self, e=0):
        if self.editBtn == None: return
        if e: self.editBtn.set('1')
        if self.editBtn.get():self.placeSubmitBtn(1)
        else: self.placeSubmitBtn()
        for widgetName in self.resultsWidgets:
            wid = self[widgetName]
            if self.editBtn.get(): wid.normal()
            else: wid.disabled()
PD = PRMP_Dialog

class PRMP_CalendarDialog(PRMP_Dialog):
   
    def __init__(self, master=None, month=None, dest='', title='PRMP_Calendar Dialog', geo=(300, 300), min_=None, max_=None, **kwargs):
        
        self.min = min_
        self.max = max_
        super().__init__(master, title=title, geo=geo, editable=False, show=0, **kwargs)

    def _setupDialog(self): self.calendar = self.addWidget(PRMP_Calendar, config=dict(callback=self.getDate, max_=self.max, min_=self.min), place=dict(relx=0, rely=0, relh=1, relw=1))
    
    def afterPaint(self): self.calendar.afterPaint()

    def getDate(self, date):
        self._setResult(date)
        if self._return:
            PRMP_Calendar.choosen = None
            self.destroy()
CD = PRMP_CalendarDialog

class PRMP_MsgBox(PRMP_Dialog):
    _bitmaps = ['info', 'question', 'error', 'warning']
    def __init__(self, master=None, geo=(350, 160), title='Message Dialog', message='Put your message here.', _type='info', cancel=0, ask=1, okText='', msgFont='DEFAULT_FONT', **kwargs):
        self.message = message
        self.msgFont = msgFont
        self._type = _type
        self.okText = okText
        self.ask = ask
        self._cancel = cancel
        
        if okText: self.ask = 0
        
        super().__init__(master, title=title, geo=geo, tm=1, asb=0, editable=False, **kwargs)

    def _setupDialog(self):
        self.placeContainer(h=self.geo[1]-50)
        self.label = PRMP_Label(self.container, config=dict(text=self.message, bitmap='', wraplength=250), font=self.msgFont)
        
        self.label.place(x=0, y=0, relh=1, relw=.85)
        
        self.bitmap = PRMP_Label(self.container, config=dict(bitmap=self.getType(self._type)))
        self.bitmap.place(relx=.85, y=0, relh=1, relw=.15)

        self.yes = PRMP_Button(self, config=dict(text='Yes' if self.ask else self.okText or 'Ok', command=self.yesCom))
        
        if not self.ask:
            self.yes.place(relx=.3, rely=.83, relh=.15, relw=.37)
            self.bind('<Return>', lambda e: self.yes.invoke())
        else:
            self.yes.place(relx=.06, rely=.83, relh=.15, relw=.17)
            self.no = PRMP_Button(self, config=dict(text='No', command=self.noCom))
            self.no.place(relx=.63, rely=.83, relh=.15, relw=.17)

        if self._cancel:
            self.cancel = PRMP_Button(self, config=dict(text='Cancel', command=self.cancelCom))
            self.cancel.place(relx=.33, rely=.83, height=28, relw=.2)
        
    def getType(self, _type):
        if _type in self._bitmaps: return _type
        elif _type in self._xbms: return f'@{self._xbms[_type]}'
    
    @property
    def _xbms(self): return Xbms.filesDict()

    def yesCom(self):
        if self.ask: self._setResult(True)
        self.destroyDialog()

    def cancelCom(self):
        self._setResult(None)
        self.destroyDialog()

    def noCom(self):
        self._setResult(False)
        self.destroyDialog()
PMB = PRMP_MsgBox

class PRMP_CameraDialog(PRMP_Dialog):

    def __init__(self, master=None, source=0, frameUpdateRate=10, title='PRMP_Camera Dialog', **kwargs):
        self.source = source
        self.frameUpdateRate = frameUpdateRate
        super().__init__(master, title=title, **kwargs)
    
    def isMaximized(self): return self.getWid_H_W(self)

    def _setupDialog(self): PRMP_Camera(self.container, source=self.source, frameUpdateRate=self.frameUpdateRate, place=dict(relx=.01, rely=.01, relh=.98, relw=.98), callback=self.getImage)

    def getImage(self, imageFile):
        self._setResult(imageFile)
        if not self.callback: PRMP_Camera._saveImage(imageFile)
        if self._return: self.destroy()
    
    def __del__(self): del self.camera
CamD = PRMP_CameraDialog

class PRMP_ImageDialog(PRMP_Dialog):
    
    def __init__(self, master=None, image=0, title='Image Dialog', **kwargs):
        self.image = image
        super().__init__(master, title=title, **kwargs)
    
    def isMaximized(self): return self.getWid_H_W(self)

    def _setupDialog(self): PRMP_ImageLabel(self.container, prmpImage=self.image, place=dict(relx=.01, rely=.01, relh=.98, relw=.98), callback=self.getImage)

    def getImage(self, imageFile):
        self._setResult(imageFile)
        self.destroyDialog()

