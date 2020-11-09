
from ....backend.core.date_time import DateTime
from .extensions import *
from .pics import Xbms


class PRMP_Dialog(PRMP_Toplevel, FillWidgets):
    
    def __init__(self, master=None, _return=True, values={}, ntb=1, nrz=0, tm=1, gaw=1, editable=True, **kwargs):
        PRMP_Toplevel.__init__(self, master, ntb=ntb, nrz=nrz, tm=tm, gaw=gaw, tw=1, **kwargs)
        FillWidgets.__init__(self, values=values)
        
        self.__result = None
        
        self._return = _return
        
        self.submitBtn = None
        self.editBtn = None
        
        self._setupDialog()
        self.fill()

        self.paint()
        self.default()
        
        if editable:
            if values: self.editInput(0)
            else: self.editInput(1)
        
        self._isDialog()
        # self.mainloop()
    
    def _setupDialog(self):
        'This is to be overrided in subclasses of PRMPDialog to setup the widgets into the dialog.'
    
    @property
    def result(self): return self.__result
    
    def default(self): pass
    
    def _setResult(self, result): self.__result = result
    
    def addSubmitButton(self, command=None):
        self.submitBtn = PRMP_Button(self.container, config=dict(text='Submit', command=command or self.processInput))            
    
    def placeSubmitBtn(self, wh=0):
        if wh:
            self.container.paint()
            geo = self.kwargs.get('geo')
            x, y = self.containerGeo
            self.submitBtn.place(x=(x/2)-30 , y=y-40, h=30, w=60)
        else: self.submitBtn.place_forget()
    
    def addEditButton(self, command=None, submitCommand=None):
        if self.submitBtn == None: self.addSubmitButton(submitCommand)
        x, y = self.containerGeo
        self.editBtn = xbtn = PRMP_Checkbutton(self.container, text='Edit', command=self.editInput)
        xbtn.place(x=10 , y=y-40, h=30, w=60)
    
    def processInput(self):
        result = {}
        self.resultsWidgets.sort()
        for widgetName in self.resultsWidgets:
            wid = self.__dict__.get(widgetName)
            if wid:
                result[widgetName] = wid.get()
        self._setResult(result)
        
        self.destroy()
        print(self.result)
        
    def editInput(self, e=0):
        if e: self.editBtn.var.set('1')
        if self.editBtn.var.get() == '1':
            self.placeSubmitBtn(1)
            for widgetName in self.resultsWidgets:
                wid = self.__dict__.get(widgetName)
                if wid: wid.normal()
        else:
            self.placeSubmitBtn()
            for widgetName in self.resultsWidgets:
                wid = self.__dict__.get(widgetName)
                if wid: wid.disabled()
PD = PRMP_Dialog

class CalendarDialog(PRMP_Dialog):
    _both = '◄►'
    _next = '►'
    _previous = '◄'
    _forward = '⏭'
    _backward = '⏮'
    choosen = None
    _version_ = '3.3.0' # Alpha by PRMPSmart

    background=PRMP_Theme.DEFAULT_BACKGROUND_COLOR
    header_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0]
    header_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1]
    month_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1]
    month_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0]
    year_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1]
    year_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0]
    
    surf_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0]
    surf_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1]
        
    
    class DayLabel(PRMP_Label):
        highlight_bg = PRMP_Theme.DEFAULT_BACKGROUND_COLOR
        highlight_fg = PRMP_Theme.DEFAULT_FOREGROUND_COLOR
        now_fg = 'white'
        now_bg = 'green'
        now_highlight_fg = 'green'
        now_highlight_bg = 'white'
        empty_bg = PRMP_Theme.DEFAULT_BUTTON_COLOR[0]
        choosen_fg = 'white'
        choosen_bg = 'black'
        days_fg = PRMP_Theme.DEFAULT_BACKGROUND_COLOR
        days_bg = PRMP_Theme.DEFAULT_FOREGROUND_COLOR
        notPart = False # for buttons not part of the days button
        
        def __init__(self, master=None, returnMethod=None,  **kw):
            super().__init__(master=master, background=self.days_bg, foreground=self.days_fg, font=PRMP_Theme.DEFAULT_FONT, **kw)
            self.day = None
            
            self.returnMethod = returnMethod
            
            self.bind('<Enter>', self.onButton)
            self.bind('<Leave>', self.offButton)
            self.bind('<ButtonPress-1>', self.choosen)

        def onButton(self, e=0):
            self.statusShow()
            if self.notPart: return
            if self.day:
                if self.now: self.config(background=self.class_.now_highlight_bg, foreground=self.class_.now_highlight_fg)
                else: self.config(background=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, foreground=PRMP_Theme.DEFAULT_FOREGROUND_COLOR)
        
        @property
        def status(self): return self.day
        
        def offButton(self, e=0):
            if self.notPart: return
            if self == CalendarDialog.choosen: self.config(background=self.class_.choosen_bg, foreground=self.class_.choosen_fg)
            elif self.now: self.config(background=self.class_.now_bg, foreground=self.class_.now_fg)
            else:
                if self.day: self.config(background=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, foreground='red' if self.redDay else PRMP_Theme.DEFAULT_BACKGROUND_COLOR)
                else: self.config(background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])
        
        paint = offButton

        def config(self, day=None, command=None, notPart=False, **kwargs):
            self.notPart = notPart
            if day: self.changeDay(day)
            if command:
                self.unbind('<ButtonPress-1>')
                self.bind('<ButtonPress-1>', command)
            
            background, foreground = kwargs.get('background'), kwargs.get('foreground')
            self.configure(**kwargs)
            
            if foreground:
                self['foreground'] = foreground
            if background:
                self['bg'] = background
        
        @property
        def now(self): return self.day == DateTime.now()
        
        def changeDay(self, day):
            now = DateTime.now()
            if day == now: self.config(background=self.class_.now_bg, foreground=self.class_.now_fg)
            self.day = day
            self.redDay = day.dayName in ['Saturday', 'Sunday']
            self.config(text=self.day.dayNum, state='normal', relief='groove')
            self.offButton()
        
        def empty(self):
            self.day = None
            self.config(text='', state='disabled', relief='flat', background=self.class_.empty_bg)
        
        def choosen(self, e=0):
            if self.day: 
                if self.notPart: return
                b4 = CalendarDialog.choosen
                CalendarDialog.choosen = self
                if b4: b4.offButton()
                self.config(background=self.class_.choosen_bg, foreground=self.class_.choosen_fg)
                self.returnMethod(self.day)
    
    def __init__(self, master=None, month=None, dest='', title='Calendar Dialog', background='SystemButtonFace', header_fg='black', header_bg='SystemButtonFace',  month_fg='black', month_bg='SystemButtonFace',  year_fg='black', year_bg='SystemButtonFace',  days_fg='black', days_bg='SystemButtonFace', highlight_fg='white', highlight_bg='#2d18e7', surf_fg='black', surf_bg='SystemButtonFace', empty_bg='SystemButtonFace', geo=(300, 300), **kwargs):
        
        if month == None: month = DateTime.now()
        DateTime.checkDateTime(month)
        
        self.month = month
        self.dest = dest

        # # colors
        # self.class_.background = background
        
        # self.class_.surf_bg = surf_bg
        # self.class_.surf_fg = surf_fg
            
        # self.class_.header_bg = header_bg
        # self.class_.header_fg = header_fg
            
        # self.class_.month_fg = month_fg
        # self.class_.month_bg = month_bg
            
        # self.class_.year_fg = year_fg
        # self.class_.year_bg = year_bg
        
        # self.class_.DayLabel.days_fg = days_fg
        # self.class_.DayLabel.days_bg = days_bg
        
        # self.class_.DayLabel.empty_bg = empty_bg
        # self.class_.DayLabel.highlight_bg = highlight_bg
        # self.class_.DayLabel.highlight_fg = highlight_fg
        
        # # colors

        if self.dest: self.__dict__[self.dest] = None
        
        super().__init__(master, title=title, geo=geo, editable=False, **kwargs)

    def paint(self):
        super().paint()
        for btn in [self._back, self._for, self._prev, self._nxt]: btn.configure(background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])
        
        self.monthNameLbl.configure(background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])
        self.yearLbl.configure(background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])

        for btn in self.headers: btn.configure(foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])
    
    def _setupDialog(self):
        self.daysButtons = []
        
        fr = self.container
        self._back = PRMP_Button(fr, text=self._backward, command=self.previousYear, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], font=PRMP_Theme.DEFAULT_MINUTE_FONT)
        self._back.place(relx=0, rely=0, relw=.12, relh=.1)

        self._prev = PRMP_Button(fr, text=self._previous, command=self.previousMonth, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])
        self._prev.place(relx=.12, rely=0, relw=.12, relh=.1)

        self.monthNameLbl = PRMP_Label(fr, text=self.month.monthName, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])
        self.monthNameLbl.place(relx=.24, rely=0, relw=.36, relh=.1)

        self.yearLbl = PRMP_Label(fr, text=self.month.year, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])
        self.yearLbl.place(relx=.6, rely=0, relw=.16, relh=.1)

        self._nxt = PRMP_Button(fr, text=self._next, command=self.nextMonth, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])
        self._nxt.place(relx=.76, rely=0, relw=.12, relh=.1)

        self._for = PRMP_Button(fr, text=self._forward, command=self.nextYear, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], font=PRMP_Theme.DEFAULT_MINUTE_FONT)
        self._for.place(relx=.88, rely=0, relw=.12, relh=.1)
        
        col = 0
        self.headers = []
        daysAbbrs = [DateTime.daysAbbr[-1]] + DateTime.daysAbbr[:-1]
        w = 1/7
        for dayAbbr in daysAbbrs:
            x = col * w
            d = PRMP_Label(fr, text=dayAbbr, relief='groove', background=self.header_bg, foreground=self.header_fg)
            d.place(relx=x, rely=.1, relw=w, relh=.15)
            self.headers.append(d)
            col += 1
        
        h = .75 / 6
        y = .25
        for d in range(42):
            m = d % 7
            x = m * w
            if (d != 0) and (m == 0): y += h
            btn = self.DayLabel(fr, returnMethod=self.choosenDay, text=d, relief='groove')
            btn.place(relx=x, rely=y, relw=w, relh=h)
            self.daysButtons.append(btn)
            
        
        self.reset = self.daysButtons[-4]
        self.reset.config(command=self.resetDate, text='☂', background='red', foreground='white', notPart=1, relief='ridge')
    
    def default(self): self.updateDays()
    
    def resetDate(self, e=0):
        self.month = DateTime.now()
        self.updateDays()
    
    def nextYear(self):
        self.month += 12
        self.updateDays()
    
    def nextMonth(self, e=0):
        self.month += 1
        self.updateDays()
    
    def previousYear(self):
        self.month -= 12
        self.updateDays()
    
    def previousMonth(self):
        self.month -= 1
        self.updateDays()
    
    def updateDays(self):
        self.monthNameLbl.config(text=self.month.monthName)
        self.yearLbl.config(text=self.month.year)
        monthDates = self.month.monthDates
        totalDays = len(monthDates)
        
        remainingBtns = self.daysButtons[totalDays:]
        for day in monthDates:
            index = monthDates.index(day)
            DayLabel = self.daysButtons[index]
            if DayLabel == self.reset: continue
            
            if day.month == self.month.month: DayLabel.config(day=day)
            else: DayLabel.empty()

        for btn in remainingBtns:
            if btn == self.reset: continue
            btn.empty()
        
        # for dayBtn in self.daysButtons: dayBtn.offButton()
    
    def choosenDay(self, day):
        self._setResult(day)
        if self.dest: self.__dict__[self.dest] = day
        if self._return:
            CalendarDialog.choosen = None
            self.destroy()

    @classmethod
    def generate(cls, master=None, month=None, dest='', title='Calendar Dialog', **kwargs): return cls(background=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, header_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], header_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1],  month_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], month_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], year_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], year_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0],  days_fg=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, days_bg=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, highlight_fg=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, highlight_bg=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, surf_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], surf_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], empty_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], **kwargs)
CD = CalendarDialog

class PRMP_MsgBox(PRMP_Toplevel):
    _bitmaps = ['info', 'question', 'error', 'warning']
    def __init__(self, master=None, geo=(338, 169), title='Message Dialog', message='Put your message here.', _type='info', cancel=0, ask=1, okText='', **kwargs):
        super().__init__(title=title, geo=geo, ntb=1, tm=1, asb=0, tw=1, **kwargs)
        
        self.__result = None
        self.addTitleBar()
        self.placeContainer(h=geo[1]-50)
        self.label = PRMP_Label(self.container, config=dict(text=message, bitmap='', wraplength=250, relief='flat'))
        
        self.label.place(x=0, y=0, relh=1, relw=.85)
        
        self.bitmap = PRMP_Label(self.container, config=dict(bitmap=self.getType(_type)), relief='flat')
        self.bitmap.place(relx=.85, y=0, relh=1, relw=.15)

        self.yes = PRMP_Button(self, config=dict(text='Yes' if ask else okText or 'Ok', command=self.yesCom))
        
        if not ask:
            self.yes.place(relx=.425, rely=.83, relh=.15, relw=.17)
            self.bind('<Return>', lambda e: self.yes.invoke())
        else:
            self.yes.place(relx=.06, rely=.83, relh=.15, relw=.17)
            self.no = PRMP_Button(self, config=dict(text='No', command=self.noCom))
            self.no.place(relx=.77, rely=.83, relh=.15, relw=.17)

        if cancel:
            self.cancel = PRMP_Button(self, config=dict(text='Cancel', command=self.cancelCom))
            self.cancel.place(relx=.769, rely=.769, height=28, relw=.3)

        self.paint()
        
        self._isDialog()
        
        
    def getType(self, _type):
        if _type in self._bitmaps: return _type
        elif _type in self._xbms: return f'@{self._xbms[_type]}'
    
    @property
    def _xbms(self): return Xbms.filesDict()
    
    @property
    def result(self): return self.__result
    def _setResult(self, result): self.__result = result
    def yesCom(self):
        self._setResult(True)
        self.destroy()
    def cancelCom(self):
        self._setResult(None)
        self.destroy()
    def noCom(self):
        self._setResult(False)
        self.destroy()
PMB = PRMP_MsgBox



