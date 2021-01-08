from .core import *
from .miscs import create_container, bound_to_mousewheel, Columns
from prmp_miscs.prmp_pics import *
from prmp_miscs.prmp_datetime import PRMP_DateTime

picTypes = ['Pictures {.jpg .png .jpeg .gif .xbm}']
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

class PRMP_FillWidgets(PRMP_Mixins):
    
    def __init__(self, values={}):
        self.__resultsWidgets = []
        self.__notEditables = []
        self.values = values
        self.fill = self.set
        self.empty = self.get
        
    def addResultsWidgets(self, child):
        if child not in self.__resultsWidgets:
            if isinstance(child, self.containers):
                for ch in child: self.addResultsWidgets(ch)
            else: self.__resultsWidgets.append(child)
        
    def addNotEditables(self, child):
        if child not in self.__notEditables:
            if isinstance(child, self.containers):
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
                    # try:
                        val = values.get(widgetName, '')
                        if val: widget.set(val)
                    # except Exception as er: print(f'ERROR {er}.')
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
                        PRMP_MsgBox(self, title='Required Input', message=f'{widgetName.title()}* is required to proceed!', _type='error', okText='Understood')
                        return
                else: result[widgetName] = get
        return result
FW = PRMP_FillWidgets

class PRMP_ImageWidget:
    def __init__(self, prmpImage=None, thumb=None, resize=None):
        self.rt = None
        self.prmpImage = prmpImage
        self.thumb = thumb or (200, 170)
        self.resize = resize or (100, 100)
        
        self.frame_counter = 0
        self.frame = None
        self.frames = None
        self.durations = None

        self.default_dp = PRMP_Image('profile_pix', inbuilt=True, thumb=self.thumb)
        self.bindMenu()
        
        self.loadImage(self.prmpImage)
            
    def disabled(self):
        self.unBindMenu()
        super().disabled()
    
    def normal(self):
        self.bindMenu()
        super().normal()
    
    def loadImage(self, prmpImage=None, **kwargs):
        self.delMenu()
        dif = 20
        w = self.width-dif, self.height-dif
        if w[0] < 0 and w[1] < 0: 
            w = (250, 200)
            self.after(50, lambda: self.loadImage(prmpImage, **kwargs))
            return

        if prmpImage:
            if not isinstance(prmpImage, PRMP_Image): prmpImage = PRMP_Image(prmpImage, thumb=self.thumb, resize=w, **kwargs)

            if isinstance(prmpImage, PRMP_Image):
                self.imageFile = prmpImage.imageFile
                self.frame = prmpImage.resizeTk(w)
            else: raise ValueError('prmpImage must be an instance of PRMP_Image')
            
            self.prmpImage =  prmpImage

            if prmpImage.ext == 'xbm': self.frame = prmpImage.resizeTk(self.resize)

            if self.prmpImage.ext == 'gif':
                self.frames = self.prmpImage.animatedTkFrames
                self.frame = self.frames[self.frame_counter]
                self.durations = self.prmpImage.interframe_durations
                self.__renderGif()
                # print(self.prmpImage.animatedFrames)
            
            self.configure(image=self.frame)

        else: self.loadImage(self.default_dp)
    
    def __renderGif(self):
        # Update Frame
        self.frame = self.frames[self.frame_counter]
        self.config(image=self.frames[self.frame_counter])

        # Loop Counter
        self.frame_counter += 1
        if self.frame_counter >= len(self.frames): self.frame_counter = 0
        self.after(self.durations[self.frame_counter], self.__renderGif)
    
    def removeImage(self):
        self.delMenu()
        from .dialogs import PRMP_MsgBox

        PRMP_MsgBox(self, title='Profile Picture Removal', message='Are you sure you wanna remove the picture from this profile? ', callback=self._removeImage)
    
    def _removeImage(self, val):
        if val: self.loadImage()
    
    def set(self, imageFile): self.loadImage(imageFile)
    
    def changeImage(self, e=0):
        self.delMenu()
        file = askopenfilename(filetypes=picTypes)
        if file: self.loadImage(file)
    
    def bindMenu(self):
        self.bind('<1>', self.delMenu, '+')
        self.bind('<3>', self.showMenu, '+')
        self.bind('<Double-1>', self.camera)
    
    def unBindMenu(self):
        self.unbind('<1>')
        self.unbind('<3>')
        self.unbind('<Double-1>')
    
    def get(self): return self.imageFile
    
    def delMenu(self, e=0):
        if self.rt:
            self.rt.destroy()
            del self.rt
            self.rt = None
        
    def camera(self, e=0):
        self.delMenu()
        from .dialogs import PRMP_CameraDialog

        PRMP_CameraDialog(self, title='Profile Photo', tw=1, tm=1, callback=self.set)
    
    def saveImage(self):
        self.delMenu()
        if self.imageFile:
            file = asksaveasfilename(filetypes=picTypes)
            if file: self.imageFile.save(file)
    
    def showMenu(self, e=0):
        self.delMenu()
        x, y = e.x, e.y
        x, y = e.x_root, e.y_root
        self.rt = rt = PRMP_Toplevel(self, geo=(50, 75, x, y), tm=1, asb=0, atb=0)
        PRMP_Button(rt, text='Camera', command=self.camera, overrelief='sunken', font=PTh.DEFAULT_MENU_FONT, place=dict(relx=0, rely=0, relh=.25, relw=1))
        PRMP_Button(rt, text='Change', command=self.changeImage, overrelief='sunken', font=PTh.DEFAULT_MENU_FONT, place=dict(relx=0, rely=.25, relh=.25, relw=1))
        PRMP_Button(rt, config=dict(text='Save', command=self.saveImage, overrelief='sunken'), font=PTh.DEFAULT_MENU_FONT, place=dict(relx=0, rely=.5, relh=.25, relw=1))
        PRMP_Button(rt, config=dict(text='Remove', command=self.removeImage, overrelief='sunken'), font=PTh.DEFAULT_MENU_FONT, place=dict(relx=0, rely=.75, relh=.25, relw=1))
        rt.paint()

IW = PRMP_ImageWidget

class PRMP_ImageLabel(PRMP_ImageWidget, PRMP_Style_Label):
    def __init__(self, master, prmpImage=None, resize=(), thumb=(), **kwargs):
        PRMP_Style_Label.__init__(self, master, config=dict(anchor='center'), **kwargs)
        PRMP_ImageWidget.__init__(self, prmpImage=prmpImage, thumb=thumb, resize=resize)
IL = PRMP_ImageLabel

class PRMP_DateWidget:
    attr = 'strDate'
    def __init__(self, min_=None, max_=None, callback=None):
        self.callback = callback
        self.date = None
        from .dialogs import PRMP_CalendarDialog, PRMP_DateTime
        self.CD = PRMP_CalendarDialog
        self.DT = PRMP_DateTime
        self.min = min_
        self.max = max_
    
    def verify(self):
        if self.DT.checkDateTime(self.date, 1): return True
        else: return False

    def action(self): self.CD(self, side=self.topest.side, _return=1, min_=self.min, max_=self.max, callback=self.set)
    
    def get(self):
        if self.date: return self.date
        text = self['text']
        if text: return PRMP_DateTime.getDMYFromDate(text)

    def set(self, date):
        if isinstance(date, str):
            try:
                if '-' in date: d, m, y = date.split('-')
                elif '/' in date: d, m, y = date.split('/')
                else: return
                self.date = self.DT.createDateTime(int(y), int(m), int(d))
            except: return
        elif isinstance(date, self.DT): self.date = date
        self.show()
        
    def show(self):
        if self.date: self.config(text=self.date.getFromSelf(self.attr))

class PRMP_DateButton(PRMP_DateWidget, PRMP_Button):
    def __init__(self, master=None, font=PTh.DEFAULT_FONT, asEntry=True, placeholder='', min_=None, max_=None, **kwargs):
        
        PRMP_Button.__init__(self, master=master, config=dict(command=self.action, anchor='w'), font=font, asEntry=asEntry,  **kwargs)
        PRMP_DateWidget.__init__(self, min_=min_, max_=max_)
        self['text'] = placeholder
        
PDB = PRMP_DateButton

class PRMP_MonthButton(PRMP_DateButton): attr = 'monthName'
PMoB = PRMP_MonthButton

class PRMP_MonthYearButton(PRMP_DateButton): attr = 'monthYear'

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

class Test_PRMP_ToolTip:
    def __init__(self, master, msg='', delay=.01, follow=True, root=None):

        self.msg = msg
        self.master = master

        self.msgVar = tk.StringVar()
        self.msgVar.set(msg)

        self.delay = delay
        self.follow = follow

        self.tip = None
        self.hidden = 0

        self.master.bind('<Enter>', self.spawn, '+')
        self.master.bind('<Leave>', self.hide, '+')
        self.master.bind('<Motion>', self.move, '+')

    def deleteTip(self):
        if self.tip:
            if (time.time() - self.hidden > 3):
                self.tip.destroy()
                self.tip = None
            else: self.tip.after(100, self.deleteTip)
    
    def spawn(self, event=0):
        self.visible = 1
        self.lastMotion = 0

        if not self.tip:
            self.tip = PRMP_Toplevel(self.master, geo=(), atb=0, asb=0, tm=1)
            Message(self.tip, config=dict(textvariable=self.msgVar, aspect=1000), asEntry=True).grid()

            self.tip.after(10, self.deleteTip)

            self.placeTip(event)
            
        self.tip.after(int(self.delay * 1000), self.show)
    
    def update(self, msg): self.msgVar.set(msg)

    def show(self):
        if self.tip: 
            if self.visible == 1 and time.time() - self.lastMotion > self.delay: self.visible = 2
            if self.visible == 2: self.tip.deiconify()
    
    def placeTip(self, event=None): self.tip.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))

    def move(self, event):
        if self.tip:
            self.lastMotion = time.time()
            if self.follow is False:
                self.tip.withdraw()
                self.visible = 1
            self.placeTip(event)
            
            self.tip.after(int(self.delay * 1000), self.show)
        else: self.spawn(event)

    def hide(self, event=None):
        self.hidden = time.time()
        self.visible = 0
        if self.tip: self.tip.withdraw()
TT = PRMP_ToolTip

class PRMP_SolidScreen(PRMP_MainWindow):
    def __init__(self, side='top-center', gaw=1, bd=12, geo=(),**kwargs):
        super().__init__(tm=1, gaw=gaw, geo=geo or (500, 500), side=side, **kwargs)
        
        self.container.configure(borderwidth=12)

        self.paint()
SS = PRMP_SolidScreen

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

class PRMP_FramedCanvas(Frame):
    def __init__(self, master, canvasConfig={}, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = Canvas(self, **canvasConfig, place=dict(relx=.005, rely=.005, relh=.99, relw=.99))

class PRMP_DateTimeView(LabelFrame):

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
            if self == PRMP_Calendar.choosen: self.config(background=self.class_.choosen_bg, foreground=self.class_.choosen_fg)
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
        def now(self): return self.day == PRMP_DateTime.now()
        
        def changeDay(self, day):
            now = PRMP_DateTime.now()
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
                b4 = PRMP_Calendar.choosen
                PRMP_Calendar.choosen = self
                if b4: b4.offButton()
                self.config(background=self.class_.choosen_bg, foreground=self.class_.choosen_fg)
                self.returnMethod(self.day)
    
    def __init__(self, master=None, month=None, dest='', callback=None, min_=None, max_=None, **kwargs):
        super().__init__(master, **kwargs)
        
        if month == None: month = PRMP_DateTime.now()
        PRMP_DateTime.checkDateTime(month)
        
        self.min = PRMP_DateTime.getDMYFromDate(min_)
        self.max = PRMP_DateTime.getDMYFromDate(max_)
        self.__date = None
        self.month = month
        self.callback = callback
        self.dest = dest
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
        daysAbbrs = [PRMP_DateTime.daysAbbr[-1]] + PRMP_DateTime.daysAbbr[:-1]
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
    
    def choosenDay(self, date):
        self.__date = date
        if self.callback: self.callback(date)

class RPMP_Entry_Label(Label):

    def __init__(self, master, font='DEFAULT_FONT', **kwargs): super().__init__(master, asEntry=True, font=font, **kwargs)

class PRMP_Camera(PRMP_Frame):

    def __init__(self, master, source=0, frameUpdateRate=10, callback=None, **kwargs):
        import cv2
        self.cv2 = cv2
        self.cam = None
        self.source = source
        self.image = None
        self._image = None
        self.callback = callback
        self.pause = False

        self.frameUpdateRate = frameUpdateRate

        super().__init__(master, **kwargs)

        self.screen = Label(self, place=dict(relx=.006, rely=.01, relh=.85, relw=.985))
        self.screen.bind('<Double-1>', self.screenPause)

        self.save = Button(self, config=dict(text='Save', command=self.saveImage))

        self.openCam()
    
    def y(self): return 
    
    def placeSave(self): self.save.place(relx=.375, rely=.87, relh=.1, relw=.25)

    def screenPause(self, e=0):
        if self.pause:
            self.pause = False
            self.openCam()
            self.save.place_forget()
        else:
            self.pause = True
            self.closeCam()
            self.placeSave()
    
    def saveImage(self):
        self.imageFile = PRMP_ImageFile(image=self._image)
        if self.callback: return self.callback(self.imageFile)
        
    @staticmethod
    def _saveImage(image):
        file = asksaveasfilename(filetypes=picTypes)
        
        if file: image.save(file)
    
    def get(self): return self.saveImage()

    def openCam(self):
        self.cam = self.cv2.VideoCapture(self.source)
        self.updateScreen()
    
    def closeCam(self):
        if self.cam and self.cam.isOpened(): self.cam.release()

    def snapshot(self):
        # Get a frame from the video source
        success, frame = self.getFrame()
        # if frame: self.cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", self.cv2.cvtColor(frame, self.cv2.COLOR_RGB2BGR))
    
    def updateScreen(self):
        if self.image: self.screen.config(image=self.image)
        # if self.image: self.screen['image'] = self.image
        del self.image
        self.image = None
        self.setImage()
        if not self.pause: self.after(self.frameUpdateRate, self.updateScreen)

    def setImage(self):
        success, frame = self.getFrame()
        if success:
            dif = 20
            w_h = self.width-dif, self.height-dif
            self._image = Image.fromarray(frame)
            image = self._image.copy()
            image.thumbnail(w_h)
            self.image = PhotoImage(image=image)
        
    def getFrame(self):
        if self.cam and self.cam.isOpened():
            success, frame = self.cam.read()
            if success: return (success, self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB))
            else: return (success, None)
        else: return (False, None)

    def __del__(self): self.closeCam()





