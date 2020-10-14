from tkinter import Button, Entry, Label, Toplevel, Widget, Frame
from tkinter.dialog import Dialog
from tkinter.colorchooser import askcolor
from .prmp_tk import PRMP_Toplevel, PRMP_Tk
from ...backend.core.date_time import DateTime

class PRMP_Dialog(PRMP_Toplevel):
    
    def __init__(self, master=None, title=None, **kwargs):
        super().__init__(master)
        self.setupOfWindow(title=title, **kwargs)
        self.__result = None
        self._setupDialog()
        self._isDialog()
        
    def _setupDialog(self):
        'This is to be overrided in subclasses of PRMPDialog to setup the widgets into the dialog.'
    
    def _setResult(self, result): self.__result = result
    
    @property
    def result(self): return self.__result

class CalendarDialog(PRMP_Dialog):
    _both = '◄►'
    _next = '►'
    _previous = '◄'
    _forward = '⏭'
    _backward = '⏮'
    choosen = None
    _version_ = '3.3.0' # Alpha by PRMPSmart
    
    class DayButton(Label):
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
        notPart = False
        
        def __init__(self, master=None, returnMethod=None, cnf={}, **kw):
            super().__init__(master=master, cnf=cnf, bg=self.days_bg, fg=self.days_fg, **kw)
            self.day = None
            
            self.returnMethod = returnMethod
            
            self.bind('<Enter>', self.onButton)
            self.bind('<Leave>', self.offButton)
            self.bind('<ButtonPress-1>', self.choosen)
            
        def onButton(self, e=0):
            if self.notPart: return
            if self.day:
                if self.now: self.config(bg=self.now_highlight_bg, fg=self.now_highlight_fg)
                elif CalendarDialog.choosen == self: self.config(bg=self.highlight_bg, fg=self.highlight_fg)
                else: self.config(bg=self.highlight_bg, fg=self.highlight_fg)
        
        def offButton(self, e=0):
            if self.notPart: return
            if self == CalendarDialog.choosen: self.config(bg=self.choosen_bg, fg=self.choosen_fg)
            elif self.now: self.config(bg=self.now_bg, fg=self.now_fg)
            else:
                if self.day: self.config(bg=self.days_bg, fg=self.days_fg)
                else: self.config(bg=self.empty_bg)
        
        def config(self, day=None, command=None, notPart=False, **kwargs):
            self.notPart = notPart
            if day: self.changeDay(day)
            if command:
                self.unbind('<ButtonPress-1>')
                self.bind('<ButtonPress-1>', command)
            
            bg, fg = kwargs.get('bg'), kwargs.get('fg')
            if fg: self.fg = fg
            if bg: self.bg = bg
            super().config(**kwargs)
        
        @property
        def now(self): return self.day == DateTime.now()
        
        def changeDay(self, day):
            now = DateTime.now()
            if day == now: self.config(bg=self.now_bg, fg=self.now_fg)
            self.day = day
            self.config(text=self.day.dayNum, state='normal', relief='groove')
            self.offButton()
        
        def empty(self):
            self.day = None
            self.config(text='', state='disabled', relief='flat', bg=self.empty_bg)
        
        def choosen(self, e=0):
            if self.day: 
                if self.notPart: return
                b4 = CalendarDialog.choosen
                CalendarDialog.choosen = self
                if b4: b4.offButton()
                self.config(bg=self.choosen_bg, fg=self.choosen_fg)
                self.returnMethod(self.day)
    
    def __init__(self, master=None, month=None, dest='', title='Calendar Dialog', bg='SystemButtonFace', header_fg='black', header_bg='SystemButtonFace',  month_fg='black', month_bg='SystemButtonFace',  year_fg='black', year_bg='SystemButtonFace',  days_fg='black', days_bg='SystemButtonFace', highlight_fg='white', highlight_bg='#2d18e7', surf_fg='black', surf_bg='SystemButtonFace', empty_bg='SystemButtonFace', _return=True, **kwargs):
        if month == None: month = DateTime.now()
        DateTime.checkDateTime(month)
        self.month = month
        self.dest = dest
        self._return = _return
        # colors
        self.bg = bg
        
        self.surf_bg = surf_bg
        self.surf_fg = surf_fg
        
        self.header_bg = header_bg
        self.header_fg = header_fg
        
        self.month_fg = month_fg
        self.month_bg = month_bg
        
        self.year_fg = year_fg
        self.year_bg = year_bg
        
        self.__class__.DayButton.days_fg = days_fg
        self.__class__.DayButton.days_bg = days_bg
        
        self.__class__.DayButton.empty_bg = empty_bg
        self.__class__.DayButton.highlight_bg = highlight_bg
        self.__class__.DayButton.highlight_fg = highlight_fg
        
        # colors

        if self.dest: self.__dict__[self.dest] = None
        
        super().__init__(master, title=title, bg=bg, **kwargs)
    
    def _setupDialog(self):
        self.daysButtons = []
        header_relief = 'groove'
        Button(self, text=self._backward, command=self.previousYear, relief=header_relief, bg=self.surf_bg, fg=self.surf_fg).place(relx=0, rely=0, relw=.12, relh=.1)
        Button(self, text=self._previous, command=self.previousMonth, relief=header_relief, bg=self.surf_bg, fg=self.surf_fg).place(relx=.12, rely=0, relw=.12, relh=.1)
        self.monthNameLbl = Label(self, text=self.month.monthName, relief=header_relief, bg=self.month_bg, fg=self.month_fg)
        self.monthNameLbl.place(relx=.24, rely=0, relw=.36, relh=.1)
        self.yearLbl = Label(self, text=self.month.year, relief=header_relief, bg=self.year_bg, fg=self.year_fg)
        self.yearLbl.place(relx=.6, rely=0, relw=.16, relh=.1)
        Button(self, text=self._next, command=self.nextMonth, relief=header_relief, bg=self.surf_bg, fg=self.surf_fg).place(relx=.76, rely=0, relw=.12, relh=.1)
        Button(self, text=self._forward, command=self.nextYear, relief=header_relief, bg=self.surf_bg, fg=self.surf_fg).place(relx=.88, rely=0, relw=.12, relh=.1)
        
        col = 0
        daysAbbrs = [DateTime.daysAbbr[-1]] + DateTime.daysAbbr[:-1]
        w = 1/7
        for dayAbbr in daysAbbrs:
            x = col * w
            Label(self, text=dayAbbr, relief='groove', bg=self.header_bg, fg=self.header_fg).place(relx=x, rely=.1, relw=w, relh=.15)
            col += 1
        
        h = .75 / 6
        y = .25
        for d in range(42):
            m = d % 7
            x = m * w
            if (d != 0) and (m == 0): y += h
            btn = self.DayButton(self, returnMethod=self.choosenDay, text=d, relief='groove')
            btn.place(relx=x, rely=y, relw=w, relh=h)
            self.daysButtons.append(btn)
        
        self.reset = self.daysButtons[-4]
        self.reset.config(command=self.resetDate, text='☂', bg='red', fg='white', notPart=1)
        
        self.updateDays()
    
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
            dayButton = self.daysButtons[index]
            if dayButton == self.reset: continue
            if day.month == self.month.month: dayButton.config(day=day)
            else: dayButton.empty()
            
        for btn in remainingBtns:
            if btn == self.reset: continue
            btn.empty()
        
        for dayBtn in self.daysButtons: dayBtn.offButton()
    
    def choosenDay(self, day):
        self._setResult(day)
        if self.dest: self.__dict__[self.dest] = day
        if self._return:
            CalendarDialog.choosen = None
            self.destroy()





class TestDialog(PRMP_Tk):
    
    def __init__(self, **kwargs):
        super().__init__()
        self.title('Dialog Test')
        self.attributes('-topmost', 1)
        
        self.lab = Label(self, relief='solid')
        self.lab.place(relx=0, rely=.2, relh=.2, relw=1)
        
        self.but = Button(self, text='test', command=self.set)
        self.bind('<Return>', self.set)
        self.bind('<BackSpace>', exit)
        self.but.place(relx=.3, rely=.7, relh=.2, relw=.4)
        
        self.setupOfWindow(**kwargs)
        
        self.mainloop()
    
    def set(self, r=0):
        date = CalendarDialog(gaw=1, ntb=1, tm=1, tw=0, alp=1, geo=(200, 200), title='Calendar by PRMPSmart', side='center', bg='red', highlight_bg='#004080', highlight_fg='white', header_bg='#004080', header_fg='white', month_bg='#004080', month_fg='white', surf_fg='#004080', year_bg='black', year_fg='white').result
        self.lab['text'] = str(date)






