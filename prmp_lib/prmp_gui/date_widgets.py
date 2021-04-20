from . import *
from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime, datetime
# print(dir())


class PRMP_DateWidget:
    attr = 'date'
    def __init__(self, min_=None, max_=None, callback=None):
        '''
        min_: minimum date.
        max_: maximum date.
        callback: function to call with the chossen date as the parameter to the function.
        '''
        self.callback = callback
        self.date = None
        from .dialogs import PRMP_CalendarDialog
        self.CD = PRMP_CalendarDialog
        self.min = min_
        self.max = max_

    def verify(self):
        if PRMP_DateTime.checkDateTime(self.date, 1): return True
        else: return False

    def action(self): self.CD(self, side=self.topest.side, _return=1, min_=self.min, max_=self.max, callback=self.set)

    def get(self):
        if self.date: return self.date
        text = self['text']
        if text: return PRMP_DateTime.getDMYFromString(text)

    def set(self, date):
        '''
        date: a str or instance of datetime.date
        '''
        if isinstance(date, str): date = PRMP_DateTime.getDMYFromString(date)
        elif isinstance(date, datetime.date): ...
        self.date = date
        self.show()

    def show(self):
        if self.date: self.config(text=self.date.getFromSelf(self.attr))
        if self.callback: self.callback(self.date)

class PRMP_DateButton(PRMP_DateWidget, PRMP_Button):
    def __init__(self, master=None, font=PRMP_Theme.DEFAULT_FONT, asEntry=True, placeholder='', min_=None, max_=None, callback=None, anchor='w', **kwargs):

        PRMP_Button.__init__(self, master=master, config=dict(command=self.action, anchor=anchor), font=font, asEntry=asEntry,  **kwargs)

        PRMP_DateWidget.__init__(self, min_=min_, max_=max_, callback=callback)
        self['text'] = placeholder
PDB = PRMP_DateButton

class PRMP_MonthButton(PRMP_DateButton): attr = 'monthName'
PMoB = PRMP_MonthButton

class PRMP_MonthYearButton(PRMP_DateButton): attr = 'monthYear'


class PRMP_DateTimeView(LabelFrame):
    'A widget that shows the time and date in some sub-widgets.'

    def __init__(self, master, text='Date and Time', **kwargs):
        super().__init__(master, config=dict(text=text), **kwargs)
        self.time = Label(self)
        self.time.place(relx=.005, rely=0, relh=.98, relw=.37)

        self.date = Label(self)
        self.date.place(relx=.39, rely=0, relh=.98, relw=.6)

        self.update()

    def update(self):
        now = PRMP_DateTime.now()
        day = now.day
        dayN = now.dayName
        month = now.monthName
        year = now.year

        date = f'{dayN} {day}, {month} {year}'
        self.date['text'] = date

        hour = str(now.hour % 12).zfill(2)
        minute = str(now.minute).zfill(2)
        second = str(now.second).zfill(2)
        m = now.strftime('%p')

        time = f'{hour} : {minute} : {second} {m}'
        self.time['text'] = time

        self.after(10, self.update)


class PRMP_Calendar(Frame):

    choosen = None
    _version_ = '3.4.0' # Alpha by PRMPSmart

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
        'buttons on the main calendar frame'
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
        count = 0

        def __init__(self, master=None, returnMethod=None, **kw):
            super().__init__(master=master, background=self.days_bg, foreground=self.days_fg, font=PRMP_Theme.DEFAULT_FONT, highlightable=0, **kw)
            self.day = None
            self.returnMethod = returnMethod

            # name='DAY'+str(PRMP_Calendar.DayLabel.count)
            # PRMP_Calendar.DayLabel.count += 1

            self.bind('<Enter>', self.onButton, '+')
            self.bind('<Leave>', self.offButton)

            self.bind('<ButtonPress-1>', self.choosen, '+')

        def onButton(self, e=0):
            self.statusShow()
            if self.notPart: return

            if self.day:
                if self.now: self.config(background=self.class_.now_highlight_bg, foreground=self.class_.now_highlight_fg)
                else: self.config(background=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, foreground=PRMP_Theme.DEFAULT_FOREGROUND_COLOR)

        @property
        def status(self):
            if self.day: return self.day.date

        def offButton(self, e=0):

            if self.notPart: return

            if self == PRMP_Calendar.choosen: self.config(background=self.class_.choosen_bg, foreground=self.class_.choosen_fg)
            elif self.now: self.config(background=self.class_.now_bg, foreground=self.class_.now_fg)
            else:
                if self.day: self.config(background=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, foreground='red' if self.redDay else PRMP_Theme.DEFAULT_BACKGROUND_COLOR)
                else: self.config(background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])

        paint = offButton

        def config(self, day=None, command=None, **kwargs):
            if day: self.changeDay(day)
            if command:
                self.unbind('<ButtonPress-1>')
                self.bind('<ButtonPress-1>', command, '+')

            background, foreground = kwargs.get('background'), kwargs.get('foreground')
            self.configure(**kwargs)

            if foreground: self['foreground'] = foreground
            if background: self['background'] = background

        @property
        def now(self):
            day = self.day
            nw = PRMP_DateTime.now()
            if self.day: return day.date == nw.date
            return day == nw

        def changeDay(self, day):
            now = PRMP_DateTime.now()
            if day == now: self.config(background=self.class_.now_bg, foreground=self.class_.now_fg)
            self.day = day
            self.redDay = day.dayName in ['Saturday', 'Sunday']
            self.config(text=self.day.dayNum, state='normal', relief='groove')
            self.offButton()

        def empty(self):
            self.day = None
            self.notPart = True

            self.config(text='', state='disabled', relief='flat', background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])

        def clicked(self, e=0):
            b4 = PRMP_Calendar.choosen
            PRMP_Calendar.choosen = self

            if b4: b4.offButton()

            self.config(background=self.class_.choosen_bg, foreground=self.class_.choosen_fg)

        def choosen(self, e=0):
            if self.day:
                if self.notPart: return
                self.clicked()
                self.returnMethod(self.day)

    def __init__(self, master, month=None, callback=None, min_=None, max_=None, **kwargs):
        '''
        month: datetime.date instance to use as the opening month.
        calllback: function to call with the choosen date as a parameter.
        min_: minimum datetime.date instance viewable
        max_: maximum datetime.date instance viewable
        '''
        super().__init__(master, **kwargs)
        month = kwargs.pop('date', month)

        month = PRMP_DateTime.checkDateTime(month, dontRaise=1)
        if not month: month = PRMP_DateTime.now()

        self.min = PRMP_DateTime.getDMYFromString(min_)
        self.max = PRMP_DateTime.getDMYFromString(max_)
        self.__date = None
        self.month = month
        self.callback = callback

        self.daysButtons = []

        self._back = PRMP_Button(self, text=self._backward, command=self.previousYear, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], font=PRMP_Theme.DEFAULT_MINUTE_FONT)
        self._back.place(relx=0, rely=0, relw=.12, relh=.1)

        self._prev = PRMP_Button(self, text=self._previous, command=self.previousMonth, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])
        self._prev.place(relx=.12, rely=0, relw=.12, relh=.1)

        self.monthNameLbl = PRMP_Label(self, text=self.month.monthName, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])
        self.monthNameLbl.place(relx=.24, rely=0, relw=.36, relh=.1)

        self.yearLbl = PRMP_Label(self, text=self.month.year, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])
        self.yearLbl.place(relx=.6, rely=0, relw=.16, relh=.1)

        self._nxt = PRMP_Button(self, text=self._next, command=self.nextMonth, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])
        self._nxt.place(relx=.76, rely=0, relw=.12, relh=.1)

        self._for = PRMP_Button(self, text=self._forward, command=self.nextYear, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], font=PRMP_Theme.DEFAULT_MINUTE_FONT)
        self._for.place(relx=.88, rely=0, relw=.12, relh=.1)

        # setting the needed labels for the calendar
        # this one for the headers [Mon...Sun], [Next, Prev, etc]
        col = 0
        self.headers = []
        daysAbbrs = [PRMP_DateTime.daysAbbr[-1]] + PRMP_DateTime.daysAbbr[:-1]
        w = 1/7
        for dayAbbr in daysAbbrs:
            x = col * w
            d = PRMP_Label(self, text=dayAbbr, relief='groove', background=self.header_bg, foreground=self.header_fg)
            d.place(relx=x, rely=.1, relw=w, relh=.15)
            self.headers.append(d)
            col += 1
        # this one for the date labels
        h = .75 / 6
        y = .25
        for d in range(42):
            m = d % 7
            x = m * w
            if (d != 0) and (m == 0): y += h
            btn = self.DayLabel(self, returnMethod=self.choosenDay, text=d, relief='groove')
            btn.place(relx=x, rely=y, relw=w, relh=h)
            self.daysButtons.append(btn)
        
        # setting the reset configs
        self.reset = self.daysButtons[-4]
        self.reset.empty()
        self.reset.config(command=self.resetDate, text='☂', background='red', foreground='white', relief='ridge')

        self.updateDays()

    def afterPaint(self):
        dic = dict(background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])

        background = PRMP_Theme.DEFAULT_BUTTON_COLOR[1]
        foreground = PRMP_Theme.DEFAULT_BUTTON_COLOR[0]

        for btn in [self._back, self._for, self._prev, self._nxt, *self.headers]: btn.config(background=background, foreground=foreground)

        self.monthNameLbl.config(**dic)
        self.yearLbl.config(**dic)

    def resetDate(self, e=0):
        self.month = PRMP_DateTime.now()
        self.updateDays()

    def nextYear(self):
        new = self.month + 12
        if self.max and (new.ymdToOrd > self.max.ymdToOrd): return
        self.month = new
        self.updateDays()

    def nextMonth(self, e=0):
        new = self.month + 1
        if self.max and (new.ymdToOrd > self.max.ymdToOrd): return
        self.month = new
        self.updateDays()

    def previousYear(self):
        new = self.month - 12
        if self.min and (new.ymdToOrd < self.min.ymdToOrd): return
        self.month = new
        self.updateDays()

    def previousMonth(self):
        new = self.month - 1
        if self.min and (new.ymdToOrd < self.min.ymdToOrd): return
        self.month = new
        self.updateDays()

    def updateDays(self):
        # updates the calendar with the current month (datetime.date instance)
        self.monthNameLbl.config(text=self.month.monthName)
        self.yearLbl.config(text=self.month.year)
        monthDates = self.month.monthDates
        totalDays = len(monthDates)

        remainingBtns = self.daysButtons[totalDays:]
        for day in monthDates:
            index = monthDates.index(day)
            DayLabel = self.daysButtons[index]
            if DayLabel == self.reset: continue

            if self.month.isSameMonthYear(day):
                DayLabel.config(day=day)
                if self.month.isSameDate(day): DayLabel.clicked()
            else: DayLabel.empty()

        for btn in remainingBtns:
            if btn == self.reset: continue
            btn.empty()

    @property
    def date(self): return self.__date

    def choosenDay(self, date):
        self.__date = date
        if self.callback: self.callback(date)
