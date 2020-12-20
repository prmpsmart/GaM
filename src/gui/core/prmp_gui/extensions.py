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
        self.__notEditables = []
        self.values = values
        self.fill = self.set
        self.empty = self.get
        
    def addResultsWidgets(self, child):
        if child not in self.__resultsWidgets:
            if isinstance(child, (list, tuple)):
                for ch in child: self.addResultsWidgets(ch)
            else: self.__resultsWidgets.append(child)
        
    def addNotEditables(self, child):
        if child not in self.__notEditables:
            if isinstance(child, (list, tuple)):
                for ch in child: self.addNotEditables(ch)
            else: self.__notEditables.append(child)
    
    @property
    def notEditables(self): return self.__notEditables
    @property
    def resultsWidgets(self): return self.__resultsWidgets
    
    def set(self, values={}):
        if values:
            for widgetName in self.resultsWidgets:
                widget = self.getFromSelf(widgetName)
                if widget:
                    try:
                        val = values.get(widgetName, '')
                        widget.set(val)
                    except Exception as er: print(f'ERROR {er}.')
                else: print(f'Error [{widgetName}, {widget}]')
            if isinstance(values, dict): self.values.update(values)
            return True
        else:
            if self.values: return self.set(self.values)
    
    def get(self):
        result = {}

        self.resultsWidgets.sort()
        for widgetName in self.resultsWidgets:
            if widgetName in self.__notEditables: continue

            wid = self.__dict__.get(widgetName)
            if wid:
                get = wid.get()
                verify = getattr(wid, 'verify', None)
                if verify:
                    if verify(): result[widgetName] = get
                    else:
                        from .dialogs import PRMP_MsgBox
                        PRMP_MsgBox(self, title='Required Input', message=f'{widgetName.title()} is required to proceed!', _type='error', okText='Understood')
                        return
                else: result[widgetName] = get
        return result
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
    
    def get(self): return self.__image.imageFile
    
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

class ImageLabel(ImageWidget, PRMP_Style_Label):
    def __init__(self, master, imageFile=None, resize=(), thumb=(), **kwargs):
        PRMP_Style_Label.__init__(self, master, **kwargs)
        ImageWidget.__init__(self, imageFile=imageFile, thumb=thumb, resize=resize)
IL = ImageLabel

class PRMP_DateButton(PRMP_Button):
    def __init__(self, master=None, font=PTh.DEFAULT_FONT, asEntry=True, placeholder='', min_=None, max_=None, **kwargs):
        
        self.date = None
        from .dialogs import CalendarDialog, DateTime
        self.CD = CalendarDialog
        self.DT = DateTime
        self.min = min_
        self.max = max_

        super().__init__(master=master, config=dict(command=self.action, anchor='w'), font=font, asEntry=asEntry,  **kwargs)
        self['text'] = placeholder
    
    def verify(self):
        if self.DT.checkDateTime(self.date): return True
        else: return False

    def action(self):
        self.date = self.CD(self, caller=self.toplevel, side=self.topest.side, _return=1, min_=self.min, max_=self.max).result
        self.set(str(self.date))
    
    def get(self): return self.date
    
    def set(self, date):
        if isinstance(date, str):
            if '-' in date: d, m, y = date.split('-')
            elif '/' in date: d, m, y = date.split('/')
            else: return
            self.date = self.DT.createDateTime(int(y), int(m), int(d))
        elif isinstance(date, self.DT): self.date = date
        self['text'] = self.date
PDB = PRMP_DateButton


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

class ToolTip(PRMP_Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """
    def __init__(self, wdgt, msg=None, msgFunc=None, delay=1, follow=True):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          font: Font to be used
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        # self.parent = self.wdgt.master
        # Initalise the Toplevel
        super().__init__(self.wdgt.topest, padx=1, pady=1, asb=0, atb=0, geo=(), ntb=1)
        # Hide initially
        self.withdraw()
        # The ToolTip Toplevel should have no frame or title bar
        # self.overrideredirect(True)

        # The msgVar will contain the text displayed by the ToolTip
        self.msgVar = tk.StringVar()
        if msg is None: self.msgVar.set('No message provided')
        else: self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        # The text of the ToolTip is displayed in a Message widget
        self.msgwid = PRMP_Message(self, config=dict(textvariable=self.msgVar, aspect=1000), font=PRMP_Theme.DEFAULT_MINUTE_FONT, background=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, foreground=PRMP_Theme.DEFAULT_BACKGROUND_COLOR)
        self.msgwid.grid()

        # Add bindings to the widget.  This will NOT override
        # bindings that the widget already has
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

        self.withdraw()

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        # The after function takes a time argument in miliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time.time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.msgwid.configure(background=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, foreground=PRMP_Theme.DEFAULT_BACKGROUND_COLOR)
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.
        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time.time()
        # If the follow flag is not set, motion within the
        # widget will make the ToolTip disappear
        #
        if self.follow is False:
            self.withdraw()
            self.visible = 1

        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
        try:
            # Try to call the message function.  Will not change
            # the message if the message function is None or
            # the message function fails
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()
TT = ToolTip

class SolidScreen(PRMP_MainWindow):
    def __init__(self, side='top-center', gaw=1, bd=12, geo=(),**kwargs):
        super().__init__(tm=1, gaw=gaw, geo=geo or (500, 500), side=side, **kwargs)
        
        self.container.configure(borderwidth=12)

        self.paint()
SS = SolidScreen

class ScrolledText(AutoScroll, tk.Text):

    @create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class ScrolledEntry(AutoScroll, tk.Entry):

    @create_container
    def __init__(self, master, **kw):
        tk.Entry.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class FramedCanvas(Frame):
    def __init__(self, master, canvasConfig={}, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = Canvas(self, **canvasConfig)
        self.canvas.place(relx=.005, rely=.005, relh=.99, relw=.99)

class DateTimeView(LabelFrame):

    def __init__(self, master, text='Date and Time', **kwargs):
        super().__init__(master, config=dict(text=text), **kwargs)
        self.time = Label(self)
        self.time.place(relx=.005, rely=0, relh=.98, relw=.37)

        self.date = Label(self)
        self.date.place(relx=.39, rely=0, relh=.98, relw=.6)

        self.update()
    
    def update(self):
        now = DateTime.now()
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

class Calendar(Frame):
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
            if self == Calendar.choosen: self.config(background=self.class_.choosen_bg, foreground=self.class_.choosen_fg)
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
            self.config(text='', state='disabled', relief='flat', background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])
        
        def choosen(self, e=0):
            if self.day: 
                if self.notPart: return
                b4 = Calendar.choosen
                Calendar.choosen = self
                if b4: b4.offButton()
                self.config(background=self.class_.choosen_bg, foreground=self.class_.choosen_fg)
                self.returnMethod(self.day)
    
    def __init__(self, master=None, month=None, dest='', hook=None, min_=None, max_=None, **kwargs):
        super().__init__(master, **kwargs)
        
        if month == None: month = DateTime.now()
        DateTime.checkDateTime(month)
        
        self.min = DateTime.getDMYFromDate(min_)
        self.max = DateTime.getDMYFromDate(max_)
        self.__date = None
        self.month = month
        self.hook = hook
        self.dest = dest
        if self.dest: self.__dict__[self.dest] = None
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
        
        col = 0
        self.headers = []
        daysAbbrs = [DateTime.daysAbbr[-1]] + DateTime.daysAbbr[:-1]
        w = 1/7
        for dayAbbr in daysAbbrs:
            x = col * w
            d = PRMP_Label(self, text=dayAbbr, relief='groove', background=self.header_bg, foreground=self.header_fg)
            d.place(relx=x, rely=.1, relw=w, relh=.15)
            self.headers.append(d)
            col += 1
        
        h = .75 / 6
        y = .25
        for d in range(42):
            m = d % 7
            x = m * w
            if (d != 0) and (m == 0): y += h
            btn = self.DayLabel(self, returnMethod=self.choosenDay, text=d, relief='groove')
            btn.place(relx=x, rely=y, relw=w, relh=h)
            self.daysButtons.append(btn)
            
        
        self.reset = self.daysButtons[-4]
        self.reset.config(command=self.resetDate, text='☂', background='red', foreground='white', notPart=1, relief='ridge')

        self.updateDays()
    
    def afterPaint(self):
        dic = dict(background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])
        
        background = PRMP_Theme.DEFAULT_BUTTON_COLOR[1]
        foreground = PRMP_Theme.DEFAULT_BUTTON_COLOR[0]

        for btn in [self._back, self._for, self._prev, self._nxt, *self.headers]: btn.config(background=background, foreground=foreground)
        
        self.monthNameLbl.config(**dic)
        self.yearLbl.config(**dic)
    
    def resetDate(self, e=0):
        self.month = DateTime.now()
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
        # print(new, self.month, self.min)
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
    
    @property
    def date(self): return self.__date
    
    def choosenDay(self, day):
        self.__date = day
        if self.dest: self.__dict__[self.dest] = day
        if self.hook: self.hook()

class Entry_Label(Label):

    def __init__(self, master, font='DEFAULT_FONT', **kwargs): super().__init__(master, asEntry=True, font=font, **kwargs)






