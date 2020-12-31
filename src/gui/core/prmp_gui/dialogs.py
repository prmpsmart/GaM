
from ....backend.core.date_time import DateTime
from .extensions import *
from .pics import PRMP_Image


class PRMP_Dialog(PRMP_MainWindow, FillWidgets):
    
    def __init__(self, master=None, _return=True, values={}, ntb=1, nrz=0, tm=1, gaw=1, tw=1, editable=True,  resultObj=None, **kwargs):

        PRMP_MainWindow.__init__(self, master, ntb=ntb, nrz=nrz, tm=tm, gaw=gaw, tw=tw, **kwargs)
        FillWidgets.__init__(self, values=values)

        self.resultObj = resultObj
        self._return = _return
        self.command = None
        self.submitBtn = None
        self.editBtn = None
        
        self._setupDialog()
        self.set()

        self.default()
        
        if editable:
            if values: self.editInput(0)
            else: self.editInput(1)
        
        self.paint()
        
        if master: self.wait_window()
        else: self.mainloop()
    
    def _setupDialog(self):
        'This is to be overrided in subclasses of PRMPDialog to setup the widgets into the dialog.'

    def default(self): pass
    
    def _setResult(self, result):
        if not isinstance(self.resultObj, PRMP_Result): raise ValueError('No PRMP_Result object is given.')
        self.resultObj.setResult(result)
    
    def addSubmitButton(self, command=None):
        self.submitBtn = PRMP_Button(self.container, config=dict(text='Submit', command=command or self.processInput))
    
    def bindCR(self): self.bind('<Control-Return>', self.command or self.processInput)
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
    
    def addEditButton(self, command=None, submitCommand=None):
        self.command = submitCommand
        if self.submitBtn == None: self.addSubmitButton(submitCommand)
        x, y = self.containerGeo
        self.editBtn = xbtn = PRMP_Style_Checkbutton(self.container, config=dict(text='Edit', command=self.editInput))
        xbtn.place(x=10 , y=y-40, h=30, w=60)
    
    def processInput(self, e=0):
        result = self.get()
        # result = {'address': 'lklk', 'email': 'awa.@asd.asa', 'gender': 'Male', 'name': 'Aderemi Goodness', 'phone': '2121', 'regDate': DateTime(2020, 12, 30, 0, 54, 19)}
        self._setResult(result)
        
        return self.resultObj.result
        
    def editInput(self, e=0):
        if self.editBtn == None: return
        if e: self.editBtn.var.set('1')
        if self.editBtn.var.get() == '1':self.placeSubmitBtn(1)
        else: self.placeSubmitBtn()
        for widgetName in self.resultsWidgets:
            wid = self[widgetName]
            if self.editBtn.var.get() == '1': wid.normal()
            else: wid.disabled()
PD = PRMP_Dialog

class CalendarDialog(PRMP_Dialog):
   
    def __init__(self, master=None, month=None, dest='', title='Calendar Dialog', geo=(300, 300), min_=None, max_=None, **kwargs):
        
        self.min = min_
        self.max = max_
        super().__init__(master, title=title, geo=geo, editable=False, **kwargs)

    def _setupDialog(self): self.calendar = self.addWidget(Calendar, config=dict(hook=self.hook, max_=self.max, min_=self.min), place=dict(relx=0, rely=0, relh=1, relw=1))
    
    def afterPaint(self): self.calendar.afterPaint()

    def hook(self):
        self._setResult(self.calendar.date)
        if self._return:
            Calendar.choosen = None
            self.destroy()
CD = CalendarDialog

class PRMP_MsgBox(PRMP_Dialog):
    _bitmaps = ['info', 'question', 'error', 'warning']
    def __init__(self, master=None, geo=(350, 160), title='Message Dialog', message='Put your message here.', _type='info', cancel=0, ask=1, okText='', msgFont='DEFAULT_FONT', **kwargs):
        self.message = message
        self.msgFont = msgFont
        self._type = _type
        self.okText = okText
        self.ask = ask
        self._cancel = cancel
        
        from .pics import Xbms

        self.XBM = Xbms
        if okText: self.ask = 0
        
        super().__init__(master, title=title, geo=geo, ntb=1, tm=1, asb=0, editable=False, **kwargs)

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
    def _xbms(self): return self.XBM.filesDict()

    def yesCom(self):
        if self.ask: self._setResult(True)
        self.destroy()
    def cancelCom(self):
        self._setResult(None)
        self.destroy()
    def noCom(self):
        self._setResult(False)
        self.destroy()
PMB = PRMP_MsgBox

class CameraDialog(PRMP_Dialog):

    def __init__(self, master=None, source=0, frameUpdateRate=10, title='Camera', **kwargs):
        self.source = source
        self.frameUpdateRate = frameUpdateRate
        super().__init__(master, title=title, **kwargs)
    
    def isMaximized(self): return self.getWid_H_W(self)

    def _setupDialog(self):
        self.camera = Camera(self.container, source=self.source, frameUpdateRate=self.frameUpdateRate, place=dict(relx=.01, rely=.01, relh=.98, relw=.98), hook=self.hook)
    
    def hook(self, imageFile):
        self._setResult(imageFile)
        if self._return: self.destroy()
    
    def __del__(self): del self.camera


