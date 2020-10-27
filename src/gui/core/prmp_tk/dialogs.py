
from ....backend.core.date_time import DateTime
from .core import *


PRMP_Toplevel = PRMP_Tk

class PRMP_Dialog(PRMP_Toplevel, FillWindow):
    
    def __init__(self, master=None, _return=True, values={}, **kwargs):
        # PRMP_Toplevel.__init__(self, master, **kwargs)
        PRMP_Toplevel.__init__(self, ntb=9, nrz=0, tm=1, **kwargs)
        
        self.__result = None
        
        self.resultsWidgets = []
        self._return = _return
        
        self._setupDialog()
        self.paint()
        self.default()
        
        FillWindow.__init__(self, values=values)
        
        try:
            if values: self.editBtn.var.set('0')
            else: self.editBtn.var.set('1')
            self.editInput()
        except: pass
        
        # self._isDialog()
        self.mainloop()
    
    def _setupDialog(self):
        'This is to be overrided in subclasses of PRMPDialog to setup the widgets into the dialog.'
    
    @property
    def result(self): return self.__result
    
    def default(self): pass
    
    def _setResult(self, result): self.__result = result
    
    def addSubmitButton(self, command=None):
        geo = self.kwargs.get('geo')
        if geo:
            x, y = geo[:2]
            xbtn = B(self, text='Submit', command=command)
            xbtn.place(x=(x/2)-30 , y=y-40, h=30, w=60)
            self.childWidgets.append(xbtn)
    
    def addEditButton(self, command=None):
        geo = self.kwargs.get('geo')
        if geo:
            x, y = geo[:2]
            self.editBtn = xbtn = Cb(self, text='Edit', command=self.editInput)
            xbtn.place(x=10 , y=y-40, h=30, w=60)
            self.childWidgets.append(xbtn)
    
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
        
    def editInput(self):
        if self.editBtn.var.get() == '1':
            for widgetName in self.resultsWidgets:
                wid = self.__dict__.get(widgetName)
                if wid: wid.normal()
        else: 
            for widgetName in self.resultsWidgets:
                wid = self.__dict__.get(widgetName)
                if wid: wid.disabled()

class CalendarDialog(PRMP_Dialog):
    _both = '◄►'
    _next = '►'
    _previous = '◄'
    _forward = '⏭'
    _backward = '⏮'
    choosen = None
    _version_ = '3.3.0' # Alpha by PRMPSmart
    
    class DayLabel(L):
        highlight_bg = '#2d18e7'
        highlight_fg = 'white'
        now_fg = 'white'
        now_bg = 'green'
        now_highlight_fg = 'green'
        now_highlight_bg = 'white'
        empty_bg = 'white'
        choosen_fg = 'white'
        choosen_bg = 'black'
        days_fg = 'white'
        days_bg = 'black'
        notPart = False # for buttons not part of the days button
        
        def __init__(self, master=None, returnMethod=None,  **kw):
            super().__init__(master=master, background=self.days_bg, foreground=self.days_fg, font=PTh.DEFAULT_FONT, **kw)
            self.day = None
            
            self.returnMethod = returnMethod
            
            self.bind('<Enter>', self.onButton)
            self.bind('<Leave>', self.offButton)
            self.bind('<ButtonPress-1>', self.choosen)
            
        def onButton(self, e=0):
            if self.notPart: return
            if self.day:
                if self.now: self.config(background=self.now_highlight_bg, foreground=self.now_highlight_fg)
                elif CalendarDialog.choosen == self: self.config(background=self.highlight_bg, foreground=self.highlight_fg)
                else: self.config(background=self.highlight_bg, foreground=self.highlight_fg)
        
        def offButton(self, e=0):
            if self.notPart: return
            if self == CalendarDialog.choosen: self.config(background=self.choosen_bg, foreground=self.choosen_fg)
            elif self.now: self.config(background=self.now_bg, foreground=self.now_fg)
            else:
                if self.day: self.config(background=self.days_bg, foreground='red' if self.redDay else self.days_fg)
                else: self.config(background=self.empty_bg)
        
        def config(self, day=None, command=None, notPart=False, **kwargs):
            self.notPart = notPart
            if day: self.changeDay(day)
            if command:
                self.unbind('<ButtonPress-1>')
                self.bind('<ButtonPress-1>', command)
            
            background, foreground = kwargs.get('background'), kwargs.get('foreground')
            super().config(**kwargs)
            
            if foreground:
                self['foreground'] = foreground
            if background:
                self['bg'] = background
        
        @property
        def now(self): return self.day == DateTime.now()
        
        def changeDay(self, day):
            now = DateTime.now()
            if day == now: self.config(background=self.now_bg, foreground=self.now_fg)
            self.day = day
            self.redDay = day.dayName in ['Saturday', 'Sunday']
            self.config(text=self.day.dayNum, state='normal', relief='groove')
            self.offButton()
        
        def empty(self):
            self.day = None
            self.config(text='', state='disabled', relief='flat', background=self.empty_bg)
        
        def choosen(self, e=0):
            if self.day: 
                if self.notPart: return
                b4 = CalendarDialog.choosen
                CalendarDialog.choosen = self
                if b4: b4.offButton()
                self.config(background=self.choosen_bg, foreground=self.choosen_fg)
                self.returnMethod(self.day)
    
    def __init__(self, master=None, month=None, dest='', title='Calendar Dialog', background='SystemButtonFace', header_fg='black', header_bg='SystemButtonFace',  month_fg='black', month_bg='SystemButtonFace',  year_fg='black', year_bg='SystemButtonFace',  days_fg='black', days_bg='SystemButtonFace', highlight_fg='white', highlight_bg='#2d18e7', surf_fg='black', surf_bg='SystemButtonFace', empty_bg='SystemButtonFace', **kwargs):
        
        if month == None: month = DateTime.now()
        DateTime.checkDateTime(month)
        
        self.month = month
        self.dest = dest
        # colors
        self.background = background
        
        self.surf_bg = surf_bg
        self.surf_fg = surf_fg
        
        self.header_bg = header_bg
        self.header_fg = header_fg
        
        self.month_fg = month_fg
        self.month_bg = month_bg
        
        self.year_fg = year_fg
        self.year_bg = year_bg
        
        self.__class__.DayLabel.days_fg = days_fg
        self.__class__.DayLabel.days_bg = days_bg
        
        self.__class__.DayLabel.empty_bg = empty_bg
        self.__class__.DayLabel.highlight_bg = highlight_bg
        self.__class__.DayLabel.highlight_fg = highlight_fg
        
        # colors

        if self.dest: self.__dict__[self.dest] = None
        
        super().__init__(master, title=title, **kwargs)
        
    
    def _setupDialog(self):
        self.addTitleBar(self.titleText)
        h = self.remainFromTitleBar
        
        self.daysButtons = []
        fr = F(self)
        fr.place(x=0, y=25, relh=h, relw=1)
        header_relief = 'groove'
        Button(fr, text=self._backward, command=self.previousYear, relief=header_relief, background=self.surf_bg, foreground=self.surf_fg).place(relx=0, rely=0, relw=.12, relh=.1)
        Button(fr, text=self._previous, command=self.previousMonth, relief=header_relief, background=self.surf_bg, foreground=self.surf_fg).place(relx=.12, rely=0, relw=.12, relh=.1)
        self.monthNameLbl = Label(fr, text=self.month.monthName, relief=header_relief, background=self.month_bg, foreground=self.month_fg)
        self.monthNameLbl.place(relx=.24, rely=0, relw=.36, relh=.1)
        self.yearLbl = Label(fr, text=self.month.year, relief=header_relief, background=self.year_bg, foreground=self.year_fg)
        self.yearLbl.place(relx=.6, rely=0, relw=.16, relh=.1)
        Button(fr, text=self._next, command=self.nextMonth, relief=header_relief, background=self.surf_bg, foreground=self.surf_fg).place(relx=.76, rely=0, relw=.12, relh=.1)
        Button(fr, text=self._forward, command=self.nextYear, relief=header_relief, background=self.surf_bg, foreground=self.surf_fg).place(relx=.88, rely=0, relw=.12, relh=.1)
        
        col = 0
        daysAbbrs = [DateTime.daysAbbr[-1]] + DateTime.daysAbbr[:-1]
        w = 1/7
        for dayAbbr in daysAbbrs:
            x = col * w
            d = L(fr, text=dayAbbr, relief='groove', background=self.header_bg, foreground=self.header_fg)
            d.place(relx=x, rely=.1, relw=w, relh=.15)
            self.childWidgets.append(d)
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
            
        self.childWidgets += self.daysButtons
        self.childWidgets += [fr]
        
        self.reset = self.daysButtons[-4]
        self.reset.config(command=self.resetDate, text='☂', background='red', foreground='white', notPart=1)
    
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
    def generate(cls, master=None, month=None, dest='', title='Calendar Dialog', **kwargs): return cls(background=PTh.DEFAULT_BACKGROUND_COLOR, header_fg=PTh.DEFAULT_BUTTON_COLOR[0], header_bg=PTh.DEFAULT_BUTTON_COLOR[1],  month_fg=PTh.DEFAULT_BUTTON_COLOR[1], month_bg=PTh.DEFAULT_BUTTON_COLOR[0],  year_fg=PTh.DEFAULT_BUTTON_COLOR[1], year_bg=PTh.DEFAULT_BUTTON_COLOR[0],  days_fg=PTh.DEFAULT_BACKGROUND_COLOR, days_bg=PTh.DEFAULT_FOREGROUND_COLOR, highlight_fg=PTh.DEFAULT_FOREGROUND_COLOR, highlight_bg=PTh.DEFAULT_BACKGROUND_COLOR, surf_fg=PTh.DEFAULT_BUTTON_COLOR[0], surf_bg=PTh.DEFAULT_BUTTON_COLOR[1], empty_bg=PTh.DEFAULT_BUTTON_COLOR[0], **kwargs)

class PRMP_MsgBox(PRMP_Toplevel):
    _bitmaps = ['info', 'question', 'error', 'warning']
    def __init__(self, master=None, geo=(338, 169), title='Message Dialog', message='Put your message here.', _type='info', cancel=0, **kwargs):
        super().__init__(title=title, geo=geo, ntb=1, tm=1, **kwargs)
        
        self.__result = None
        self.addTitleBar()
        
        self.label = L(self, text=message, bitmap='')
        self.label.place(relx=0, rely=.15, relh=.6, relw=1)
        self.bitmap = L(self.label, bitmap=_type, relief='flat')
        self.bitmap.place(relx=.84, rely=.2, relh=.6, relw=.15)

        self.yes = PRMP_Button(self, text='Yes', command=self.yesCom)
        self.yes.place(relx=.06, rely=.8, relh=.15, relw=.17)

        if cancel:
            self.cancel = B(self, text='Cancel', command=self.cancelCom)
            self.cancel.place(relx=.769, rely=.769, height=28, relw=.3)

        self.no = B(self, text='No', command=self.noCom)
        self.no.place(relx=.77, rely=.8, relh=.15, relw=.17)
        
        
        self._isDialog()
        # self.mainloop()
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



