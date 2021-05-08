from .core import tk, PRMP_Theme, PRMP_Widget, _PIL_, PRMP_Image
from .core_tk import *
from .core_ttk import *
import ctypes, subprocess, functools, os
from prmp_lib.prmp_miscs.prmp_mixins import PRMP_ClassMixins
from prmp_lib.prmp_miscs.prmp_images import PRMP_Images

__all__ = ['PRMP_Window', 'PRMP_Tk', 'PRMP_Toplevel', 'PRMP_MainWindow', 'PRMP_ToolTip', 'PRMP_ToolTipsManager', 'Tk', 'Toplevel']


class PRMP_TkReloader:
    '''reload ability of a tk app.
    subclass this class and bind PRMP_TkReloader.reload() to an event, or manually call it.
    '''

    def runner(self):
        '''
        the brain.
        exits the first process, call another process with the environments variables of the current one.
        and sets the PRMP_TK environ variable
        '''
        args, env = [os.sys.executable] + os.sys.argv,  os.environ
        env["PRMP_TK"] = "RUNNING"
        while True:
            exit_code = subprocess.call(args, env=env, close_fds=False)
            if exit_code != 63: return exit_code

    def reloader(self, e=None):
        '''
        e: event
        '''
        try: os.system("cls")
        except:
            try: os.system("clear")
            except: pass

        print("Reloading")
        os.sys.exit(63)
        
    def reload(self, func):
        '''
        This is the entry point
        func: function to execute if reloaded

        if PRMP_TK environment variable is not set, it call PRMP_TKReloader.runner
        '''
        try:
            if os.environ.get("PRMP_TK") == "RUNNING": func()
            else: os.sys.exit(self.runner())
        except Exception as E: pass


class PRMP_Window(PRMP_Widget, PRMP_TkReloader):
    TOPEST = None
    STYLE = None

    TKICON = ''
    PRMPICON = ''

    TIPSMANAGER = None

    TkClass = None

    @property
    def style(self): return PRMP_Window.STYLE

    def prevTheme(self, event=None):
        theme, index = self._prevTheme()
        self.editStatus(f'Theme({theme}) | Index({index})')
        self._colorize()

    def nextTheme(self, event=None):
        theme, index = self._nextTheme()
        self.editStatus(f'Theme({theme}) | Index({index})')
        self._colorize()

    @property
    def topest(self): return PRMP_Window.TOPEST
    
    @property
    def toplevel(self): return self


    def start(self):
        '''
        paints this window and starts it
        '''
        self.paint()
        self.mainloop()
    
    @property
    def cont(self): return self.container
    
    def change2Imgcolor(self, image, num_colors=10, update=1, button_fg='white', fg='white'):
        '''
        changes the PRMP_Theme defaults colors to the colors in image

        image: path to image or an PIL.Image instance
        num_colors: number of colors to extract from the image
        update: bool, whether to trigger the painting of the widgets
        button_fg: color to set as the foreground of button widgets.
        '''

        bgs = PRMP_Images.get_colors(image, num_colors, inhex=1)
        bg = bgs[0]
        PRMP_Theme.DEFAULT_INPUT_ELEMENTS_COLOR = PRMP_Theme.DEFAULT_BACKGROUND_COLOR = bg
        PRMP_Theme.DEFAULT_INPUT_TEXT_COLOR = PRMP_Theme.DEFAULT_FOREGROUND_COLOR = fg
        PRMP_Theme.DEFAULT_BUTTON_COLOR = (button_fg, bg)

        if update: self.updateTheme()
        return bgs

    change_color = change2Imgcolor

    def __init__(self, master=None, container=True, containerConfig={'relief': 'groove'},  gaw=None, ntb=None, tm=None, tw=None, grabAnyWhere=True, geo=(500, 500), geometry=(), noTitleBar=True, topMost=False, alpha=1, toolWindow=False, side='center', title='Window', bindExit=True, nrz=None, notResizable=False, atb=None, asb=None, be=None, resize=(1, 1), addStatusBar=True, addTitleBar=True, tkIcon='', prmpIcon='', grab=False, b4t=None, bind4Theme=1, toggleMenuBar=False, tbm=None, normTk=False, normStyle=False, tipping=False, tt=None, tooltype=False, noWindowButtons=False, nwb=None, themeIndex=0, theme='', canvas_as_container=False, cac=None, label_as_container=False, lac=None, containerClass=None, cc=None, promptExit=False, **kwargs):
        '''
        PRMP_Window a base class for all window class for common behaviours.

        Resizability is only effective if and only if (tooltype = noTitleBar = toolWindow = False) and resize = (True, True)


        container: 
        containerConfig: 
        alpha: 
        side: 
        title: 

        resize: 
        normTk: 
        normStyle: 
        tipping: 
        themeIndex: 
        theme: 
        promptExit: 

        tkIcon: 
        prmpIcon: 
        grab: 
        
        b4t, bind4Theme: 
        tbm, toggleMenuBar: 
        tw, toolWindow: 
        geo, geometry: 
        ntb, noTitleBar: 
        tm, topMost: 
        gaw, grabAnyWhere: 
        be, bindExit: 
        nrz, notResizable: 
        atb, addTitleBar: 
        asb, addStatusBar: 
        tt, tooltype: 
        nwb, noWindowButtons: 
        cac, canvas_as_container: 
        lac, label_as_container: 
        cc, containerClass: 

        kwargs: other TKClass options to pass to the PRMP_Widget.__init__
        '''

        if themeIndex: PRMP_Theme.setThemeIndex(themeIndex)
        elif theme: PRMP_Theme.setTheme(theme)

        PRMP_Widget.__init__(self, master, geo=geo, nonText=True, **kwargs)

        if PRMP_Window.TOPEST == None:
            from .core_ttk import PRMP_Style
            self.bind(PRMP_Style.PRMP_STYLE_EVENT, self.paint)

            PRMP_Window.TOPEST = self
            self.createDefaultFonts()

            if not normStyle: PRMP_Window.STYLE = PRMP_Style(self)
            
            if tipping: PRMP_Window.TIPSMANAGER = PRMP_ToolTipsManager(self)

        self.container = None
        self.zoomed = False
        self.iconed = False

        # window's additional widgets
        self.titleBar = None
        self.menuBar = None
        self.statusBar = None
        
        self.side = side
        self.tipping = tipping
        self.titleText = title
        
        self.promptExit = promptExit

        self.co = 0
        # normalizing of the parameters, from the abbr to their full meaning.
        if normTk: atb, asb, geo = 0, 0, ()
        if geo != None: geometry = geo
        if gaw != None: grabAnyWhere = gaw
        if ntb != None: noTitleBar = ntb
        if tm != None: topMost = tm
        if nrz != None: notResizable = nrz
        if tw != None: toolWindow = tw
        if be != None: bindExit = be
        if atb != None: addTitleBar = atb
        if asb != None: addStatusBar = asb
        if b4t != None: bind4Theme = b4t
        if tbm != None: toggleMenuBar = tbm
        if tt != None: tooltype = tt
        if nwb != None: noWindowButtons = nwb
        if cac != None: canvas_as_container = cac
        if lac != None: label_as_container = lac
        if cc != None: containerClass = cc

        containerClass = containerClass or PRMP_Style_Frame

        if container:
            if canvas_as_container: containerClass = Canvas
            elif label_as_container: containerClass = PRMP_Style_Label

            self.container = containerClass(self)
            self.container.configure(**containerConfig)

        self.noWindowButtons = noWindowButtons

        self.toggleMenuBar = toggleMenuBar
        if notResizable: resize = (0, 0)

        if bindExit and not normTk: self.bindExit()

        # binding theme changing using Control-Up/Down
        if bind4Theme:
            self.bind('<Control-Up>', self.prevTheme)
            self.bind('<Control-Down>', self.nextTheme)

        # set the window attributes
        self.windowAttributes(topMost=topMost, toolWindow=toolWindow, alpha=alpha, noTitleBar=noTitleBar, addTitleBar=addTitleBar, addStatusBar=addStatusBar, prmpIcon=prmpIcon, tkIcon=tkIcon, resize=resize, tooltype=tooltype)

        # ability to move the whole window using Holding Right Click
        if grabAnyWhere: self._grab_anywhere_on()
        else: self._grab_anywhere_off()

        # binding the necessary functions, to keep track and keep the geometry of the inbounding widgets and features.
        self.bindToWidget(('<Configure>', self.placeContainer), ('<FocusIn>', self.placeContainer), ('<Map>', self.deiconed), ('<Control-M>', self.minimize), ('<Control-m>', self.minimize))

        # window's postion and title
        self.setTitle(title)

        self.placeOnScreen(side, geometry)
        self.bind('<Control-E>', self.destroySelf)
        self.bind('<Control-e>', self.destroySelf)

        # whether to grab all event to this window
        if grab: self.grab_set()
        self.focus()

        # functions to execute after mapping of this window
        self.__afters = []
        self.after(100, self.loadAfters)

    def loadAfters(self):
        for after in self.__afters: after()

    def addAfter(self, child):
        '''
        child: a callable to execute after mapping of this window
        '''
        if child not in self.__afters:
            if isinstance(child, (list, tuple)):
                for ch in child: self.addAfters(ch)
            else: self.__afters.append(child)

    def windowAttributes(self, topMost=0, toolWindow=0, alpha=1, noTitleBar=1,  addTitleBar=1, addStatusBar=1, tkIcon='', prmpIcon='', resize=(1, 1), tooltype=False):
        '''
        parameters are explained in the constructor.
        '''

        self.resize = resize
        self.resizable(*self.resize)

        self.noTitleBar = noTitleBar
        self._addStatusBar = addStatusBar
        self._addTitleBar = addTitleBar
        self.toolWindow = toolWindow
        self.topMost = topMost
        self.alpha = alpha

        if addTitleBar:
            if toolWindow: self.__r = 1
            elif self.resize.count(True) > 1: self.__r = 2
            else: self.__r = 0
            self.addTitleBar()
            self.setPRMPIcon(prmpIcon or PRMP_Window.PRMPICON)

        if addStatusBar: self.addStatusBar()

        if noTitleBar or tooltype:
            self.overrideredirect(True)
            if not tooltype: self.after(10, self.addWindowToTaskBar)

        else: self.setAttributes()

        self.setTkIcon(tkIcon or PRMP_Window.TKICON)
        
        if self.topMost: self.topmost()
    
    def setAttributes(self): self.attributes('-toolwindow', self.toolWindow, '-alpha', self.alpha)
    # def setAttributes(self): self.attributes('-toolwindow', self.toolWindow, '-alpha', self.alpha)

    def topmost(self): self.attributes('-topmost', True)

    def addWindowToTaskBar(self, event=None):
        '''
        A hack for adding this window to OS managed windows
        called if and only if (noTitleBar is True and tooltype is False)
        '''

        self.withdraw()
        winfo_id = self.winfo_id()
        parent = ctypes.windll.user32.GetParent(winfo_id)
        res = ctypes.windll.user32.SetWindowLongW(parent, -20, 0)
        self.deiconify()
        
        if not res:
            # continue until OS windows manager assign an ID for this window.
            self.after(10, self.addWindowToTaskBar)
        # print('-toolwindow', self.toolWindow, '-alpha', self.alpha, '-topmost', self.topMost)

        if res: self.attributes('-alpha', self.alpha)

    # positioning of window

    def placeOnScreen(self, side='', geometry=(500, 500)):
        error_string = f'side must be of {self._sides} or combination of "center-{self._sides[:-1]}" delimited by "-". e.g center-right. but the two must not be the same.'
        if len(geometry) == 4:
            self.lastPoints = geometry
            side = None

        else: self.lastPoints = [0, 0, 0, 0]

        self._geometry = geometry or (500, 500)

        if side and geometry:
            if '-' in side:
                one, two = side.split('-')
                sides = one, two
                assert (one in self._sides) and (two in self._sides), error_string
                assert one != two, error_string
                assert not ((self._top in sides) and (self._bottom in sides)), 'both "top" and "bottom" can not be combined'
                assert not ((self._left in sides) and (self._right in sides)), 'both "left" and "right" can not be combined'

                if self._center in sides:
                    main_side = one if one != self._center else two
                    funcs = {self._top: self.centerOfTopOfScreen, self._left: self.centerOfLeftOfScreen, self._right: self.centerOfRightOfScreen, self._bottom: self.centerOfBottomOfScreen}
                elif self._top in sides:
                    main_side = one if one != self._top else two
                    funcs = {self._right: self.topRightOfScreen, self._left: self.topLeftOfScreen}
                elif self._bottom in sides:
                    main_side = one if one != self._bottom else two
                    funcs = {self._right: self.bottomRightOfScreen, self._left: self.bottomLeftOfScreen}

            else:
                assert side in self._sides, error_string
                main_side = side
                funcs = {self._top: self.topOfScreen, self._left: self.leftOfScreen, self._right: self.rightOfScreen, self._bottom: self.bottomOfScreen, self._center: self.centerOfScreen}
            funcs[main_side]()
        else:
            if geometry: self.setGeometry(geometry)

        self.setGeometry(self.lastPoints)

    @property
    def screenwidth(self): return self.winfo_screenwidth()

    @property
    def screenheight(self): return self.winfo_screenheight()

    @property
    def screen_xy(self): return (self.screenwidth, self.screenheight)

    @property
    def paddedScreen_xy(self): return (self.screenwidth-70, self.screenheight-70)

    @property
    def geo(self): return self.kwargs.get('geo')

    @property
    def containerGeo(self): return (self.x_w[1], self.y_h[1])

    @property
    def x_w(self): return (2, self.geo[0]-4)

    @property
    def y_h(self): return (30, self.geo[1]-60)

    def getWhichSide(self): return random.randint(1, 15) % 3

    @property
    def getXY(self):
        if self._geometry: return self._geometry[:3]
        return (400, 300)

    def _pointsToCenterOfScreen(self, x, y, *a):
        screen_x, screen_y = self.screen_xy
        show_x = (screen_x - x) // 2
        show_y = (screen_y - y) // 2
        return [x, y, show_x, show_y]

    @property
    def pointsToCenterOfScreen(self): return self._pointsToCenterOfScreen(*self.getXY)

    def getSubbedGeo(self, geo):
        assert isinstance(geo, (tuple, list))
        geo = list(geo)

        while len(geo) < 4: geo.append(0)

        if isinstance(geo, list): geo = tuple(geo)
        return '%dx%d+%d+%d'%geo

    def setGeometry(self, points):
        if points[0] and points[1]:
            self.lastPoints = points
            self.geometry(self.getSubbedGeo(points))

    setSize = position = setGeometry

    def centerOfTopOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-1] = 50
        self.setGeometry(points)

    def changeGeometry(self, geo=(400, 300)): self.placeOnScreen(side=self.side, geometry=geo)

    def centerOfScreen(self): self.setGeometry(self.pointsToCenterOfScreen)

    def centerOfBottomOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-1] *= 2
        self.setGeometry(points)

    def centerOfLeftOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2] = 50
        self.setGeometry(points)

    def centerOfRightOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2] *= 2
        points[2] -= 50
        self.setGeometry(points)

    def topLeftOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2:] = 50, 50
        self.setGeometry(points)

    def topRightOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-1] = 50
        points[2] *= 2
        points[2] -= 50
        self.setGeometry(points)

    def bottomLeftOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2] = 50
        points[-1] *= 2
        self.setGeometry(points)

    def bottomRightOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-2] *= 2
        points[-2] -= 50
        points[-1] *= 2
        self.setGeometry(points)
    
    def topOfScreen(self): [self.topLeftOfScreen, self.topRightOfScreen, self.centerOfTopOfScreen][self.getWhichSide()]()
    
    def bottomOfScreen(self): [self.bottomLeftOfScreen, self.bottomRightOfScreen, self.centerOfBottomOfScreen][self.getWhichSide()]()
    
    def rightOfScreen(self): [self.bottomRightOfScreen, self.topRightOfScreen, self.centerOfRightOfScreen][self.getWhichSide()]()
    
    def leftOfScreen(self): [self.bottomLeftOfScreen, self.topLeftOfScreen, self.centerOfLeftOfScreen][self.getWhichSide()]()
    
    def placeContainer(self, event=None, h=0):
        if self._addTitleBar:
            top = 30
            if self._addStatusBar: bottom = 60
            else: bottom = 30
        else:
            top = 0
            if self._addStatusBar: bottom = 30
            else: bottom = 0

        if self.container: self.container.place(x=0, y=top, relw=1, h=h or self.winfo_height()-bottom-3)

        self.placeTitlebar()
        self.placeStatusBar()

    def _isDialog(self, g=1):
        self.attributes('-toolwindow', 1)
        self.resizable(0, 0)
        if g: self.grab_set()
        self.focus()
        self.wait_fwindow()

    def minimize(self, event=None):
        self.withdraw()
        self.overrideredirect(False)
        self.iconify()
        self.iconed = True
        self.isMinimized()

    def deiconed(self, event=None):
        if self.iconed:
            self.co += 1
            self.iconed = False
            v = self.winfo_viewable()
            if v:
                if self.noTitleBar: self.overrideredirect(True)
                self.normal()
                self.addWindowToTaskBar()

    def maximize(self, event=None):
        if self.__r != 2: return

        if self.zoomed:
            self.zoomed = False
            self.TkClass.state(self, 'normal')
            self.isNormal()

        else:
            self.zoomed = True
            self.TkClass.state(self, 'zoomed')
            self.isMaximized()

    # events
    def isMaximized(self): pass

    def isMinimized(self): pass

    def isNormal(self): pass

    def setTitle(self, title):
        self.title(title)
        self.titleText = title
        if self.titleBar: self.titleBar.set(title or self.titleText)

    def setTkIcon(self, icon):
        if icon: self.iconbitmap(icon)

    def setPRMPIcon(self, icon):
        if icon and _PIL_:
            self.imgIcon = PRMP_Image(icon, resize=(20, 20), for_tk=1)
            self._icon['image'] = self.imgIcon

    def addTitleBar(self, title=''):
        if self.titleBar:
            self.placeTitlebar()
            return
        F, L, B = PRMP_Style_Frame, PRMP_Style_Label, PRMP_Style_Button

        w, y = self.geo[:2]
        fr = F(self)
        self._min = self._max = self._exit = None
        rv = (20, 20)

        if not self.noWindowButtons and self.__r != 1:
            self.imgMin = PRMP_Image('button_blank_green', inbuilt=1, resize=rv, for_tk=1)
            self._min = B(fr, config=dict(command=self.minimize, text=self.min_, image=self.imgMin, style='green.TButton'), font='DEFAULT_SMALL_BUTTON_FONT')

            self.imgMax = PRMP_Image('button_blank_yellow', inbuilt=1, resize=rv, for_tk=1)
            self._max = B(fr, config=dict(command=self.maximize, text=self.max_, image=self.imgMax, style='yellow.TButton'), font='DEFAULT_SMALL_BUTTON_FONT')

        if not self.noWindowButtons:
            self.imgExit = PRMP_Image('button_blank_red', inbuilt=1, resize=rv, for_tk=1)
            self._exit = B(fr, config=dict(text=self.x_btn2, command=self.destroySelf, image=self.imgExit, style='exit.TButton'), font='DEFAULT_SMALL_BUTTON_FONT')

            self._icon = L(fr)

        self.titleBar = L(fr, config=dict( text=title or self.titleText), font='DEFAULT_TITLE_FONT', relief='groove')
        self.menuBar = F(fr, config=dict(relief='groove'))

        if PRMP_Window.TIPSMANAGER:
            tipm = PRMP_Window.TIPSMANAGER
            tipm.add_tooltip(self._max, text='Maximize')
            tipm.add_tooltip(self._min, text='Minimize')
            tipm.add_tooltip(self._exit, text='Exit')
            tipm.add_tooltip(self.titleBar, text='Right click for MENU bar')
            tipm.add_tooltip(self.menuBar, text='Right click for TITLE bar')

        for bar in [self.titleBar, self.menuBar]:
            bar.bind('<Double-1>', self.maximize, '+')
            bar._moveroot()
            bar.bind('<3>', self.switchMenu)

        self.placeTitlebar()

    def switchMenu(self, e=None):
        if e.widget == self.titleBar: self.toggleMenuBar = True
        else: self.toggleMenuBar = False

        self.placeTitlebar()

    def addToMenu(self, widget, **kwargs):
        if self.titleBar and self.menuBar: self.menuBar.addWidget(widget, **kwargs)

    def placeTitlebar(self):
        if self.titleBar:
            x = self.titleBar.master.winfo_width()
            xw = self.titleBar.master.master.winfo_width()
            self.titleBar.master.place(x=0, rely=0, h=30, w=xw)


            if x < 0: return
            w = 30
            if not self.noWindowButtons and self.__r != 1:
                self._min.place(x=x-90, rely=0, relh=1, w=30)
                self._max.place(x=x-60, rely=0, relh=1, w=30)
                w = 90

            if self.toggleMenuBar: bar, unbar = self.menuBar, self.titleBar
            else: unbar, bar = self.menuBar, self.titleBar

            w = x - w
            if not self.noWindowButtons:
                w -= 30
                x = 30
                self._icon.place(x=0, rely=0, relh=1, w=30)
            else:
                x = 0
                w += 30

            bar.place(x=x, rely=0, relh=1, w=w)
            unbar.place_forget()

            if not self.noWindowButtons: self._exit.place(x=xw-30, rely=0, relh=1, w=28)

    def editStatus(self, text):
        if self.statusBar: self.statusBar.set(text)

    def addStatusBar(self):
        if self.statusBar:
            self.placeStatusBar()
            return

        F, L, B = PRMP_Style_Frame, PRMP_Style_Label, PRMP_Style_Button
        self.statusBar = self._up = self._down = None

        fr = F(self)
        self.statusBar = L(fr, config=dict(text='Status' or self.statusText, ), font='DEFAULT_STATUS_FONT')
        self.statusBar._moveroot()
        self._up = B(fr, config=dict(text=self.upArrow, command=self.prevTheme), font='DEFAULT_SMALL_BUTTON_FONT')
        self._down = B(fr, config=dict(text=self.downArrow, command=self.nextTheme), font='DEFAULT_SMALL_BUTTON_FONT')

        if PRMP_Window.TIPSMANAGER:
            tipm = PRMP_Window.TIPSMANAGER
            tipm.add_tooltip(self.statusBar, text='Status Bar', follow=1)
            tipm.add_tooltip(self._down, text='Previous Theme')
            tipm.add_tooltip(self._up, text='Next Theme')


        self.placeStatusBar()

    def placeStatusBar(self, event=None):
        if self.statusBar:
            y = self.winfo_height()
            x = self.statusBar.master.winfo_width()
            xw = self.statusBar.master.master.winfo_width()
            if x < 0: return
            if y < 0: return
            h = 30
            self.statusBar.master.place(x=0, y=y-h, h=h, w=xw)
            self.statusBar.place(x=0, y=0, h=27, w=x-60)
            self._up.place(x=x-60, rely=0, h=27, w=30)
            self._down.place(x=x-30, rely=0, h=27, w=28)

    def closing(self): pass

    def save(self):

        pass

    def destroy(self):
        if self == self.topest:
            PRMP_Window.TOPEST = None
            PRMP_Window.STYLE = None
            PRMP_Style.LOADED = False

        super().destroy()

    def destroySelf(self, event=None):
        self.closing()
        # threading.Thread(target=self.save).start()
        self.save()

        def out(u):
            if not u: return
            self.destroy()
            os.sys.exit(self.save())

        if self == self.topest:
            if self.promptExit:
                from .dialogs import PRMP_MsgBox
                PRMP_MsgBox(self, title='Exit', message='Are you sure to exit?', callback=out)
            else: out(1)
        else: self.destroy()

    def _colorize(self):
        topest = self.topest
        if topest:
            topest.style.update()
            topest._paintAll()
        else: return

    def paint(self, event=None):
        self._paintAll()
        self.afterPaint()

    def afterPaint(self): pass

    def bindExit(self):
        def ex(event=None): os.sys.exit()
        self.bind_all('<Control-/>', ex)

PWin = PRMP_Window

class PRMP_Tk(PRMP_Window, tk.Tk):
    TkClass = tk.Tk
    def __init__(self, _ttk_=False, **kwargs):
        PRMP_Window.__init__(self, _ttk_=_ttk_, **kwargs)

Tk = PT = PRMP_Tk

class PRMP_Toplevel(PRMP_Window, tk.Toplevel):
    TkClass = tk.Toplevel
    def __init__(self, master=None, _ttk_=False, **kwargs):

        if isinstance(master, PRMP_Widget):
            try: kwargs['side'] = kwargs.get('side') or master.toplevel.side
            except AttributeError as y: print(y)
        PRMP_Window.__init__(self, _ttk_=_ttk_, **kwargs)

Toplevel = PTl = PRMP_Toplevel


class PRMP_MainWindow(PRMP_ClassMixins):

    def __init__(self, master=None, _ttk_=False, **kwargs):

        master = master or PRMP_Window.TOPEST

        if master: self.root = PRMP_Toplevel(master, _ttk_=_ttk_, **kwargs)
        else: self.root = PRMP_Tk(_ttk_=_ttk_, **kwargs)

        for k, v in self.class_.__dict__.items():
            if k.startswith('__') or k == 'root': continue
            if callable(v): self.root.__dict__[k] = functools.partial(v, self)

    def __str__(self): return str(self.root)

    def __getitem__(self, name):
        attr = self.getFromSelf(name, self._unget)
        if attr != self._unget: return attr
        else: return getattr(self.root, name)

    def __getattr__(self, name): return self[name]

MainWindow = PMW = PRMP_MainWindow

# ToolTips

class PRMP_ToolTip(Toplevel):
    'Create a tooltip'
    _initialized = False

    def __setitem__(self, key, value): self.configure(**{key: value})

    def __getitem__(self, key): return self.cget(key)

    def cget(self, key):
        if key == self.key: return self.keyval() if callable(self.keyval) else self.keyval
        else: return self.cgetsub(key) if self.cgetsub else self.cgetsub

    def __init__(self, master, alpha=.8, bg='', background='', fg='', font='', foreground='', pos=None, position=(), relief='flat', text='', _ttk_=0, **kwargs):
        '''
        Construct a Tooltip with parent master.
        alpha: float. Tooltip opacity between 0 and 1.
        bg, background: for the tip
        fg, foreground: for the tip
        pos, position: position to place the tip
        relief: for the tip
        _ttk_: whether to use tkinter.ttk Entry or not
        kwargs: ttk.Label options,
        '''

        foreground = fg or foreground
        background = bg or background
        position = pos or position or ()

        k = {}
        if Toplevel != tk.Toplevel: k.update(normTk=1)

        super().__init__(master, background=background, padx=0, pady=0, tooltype=True, **k)
        self.transient(master)
        # self.overrideredirect(True)
        self.update_idletasks()
        self.attributes('-alpha', alpha or 0.8, '-topmost', 1)

        if 'linux' in os.sys.platform: self.attributes('-type', 'tooltip')

        style_dict = {}

        self.updateFg = not bool(foreground)
        self.updateBg = not bool(background)
        self.updateFont = not bool(font)

        if not self.updateFg: style_dict['foreground'] = foreground
        if not self.updateBg: style_dict['background'] = background
        if not self.updateFont: style_dict['font'] = font

        if _ttk_ and not ToolTip._initialized:
            # default tooltip style
            style = ttk.Style(self)
            style.configure('tooltip.TLabel',  relief=relief, **style_dict)
            ToolTip._initialized = True

        # default options
        kw = dict(compound='left', style='tooltip.TLabel', padding=4, text=text, justify=tk.LEFT, relief=tk.SOLID, borderwidth=1)
        # update with given options
        kw.update(kwargs)

        if not _ttk_:
            # do some editting for the tk.Label widget
            del kw['style'], kw['padding']
            kw.update(style_dict)
            Label = tk.Label
        else: Label = ttk.Label

        self.label = Label(self, **kw)
        self.label.pack(fill='both')

        self.key = 'alpha'
        self.keyval = lambda : self.attributes('-alpha')
        self.cgetsub = self.label.cget

        if position: self.position(pos)

    def configure(self, **kwargs):
        if 'alpha' in kwargs: self.attributes('-alpha', kwargs.pop('alpha'))
        self.label.configure(**kwargs)

    config = configure

    def update_style(self):
        style_dict = {}
        if self.updateFg: style_dict['foreground'] = PRMP_Theme.DEFAULT_INPUT_TEXT_COLOR
        if self.updateBg: style_dict['background'] = PRMP_Theme.DEFAULT_INPUT_ELEMENTS_COLOR
        if self.updateFont: style_dict['font'] = 'DEFAULT_FONT'

        self.configure(**style_dict)

    def deiconify(self):
        self.update_style()
        super().deiconify()

    def keys(self):
        keys = list(self.label.keys())
        keys.insert(0, 'alpha')
        return keys

    def position(self, pos):
        if len(pos) == 2:
            x, y = pos
            geo = f'+{x}+{y}'
            self.geometry(geo)

ToolTip = PRMP_ToolTip

class PRMP_ToolTipsManager:

    def __init__(self, widget=None, delay=200, text='', **kwargs):
        '''
        widget: tkinter widget
        delay: delay to pop-up tip
        text: the text on the tip
        kwargs: options for the tooltip window e.g bg, font etc
        '''

        self.widget = widget
        self.istree = isinstance(widget, ttk.Treeview)

        self.tooltip_text = {}
        self.tooltip_follows = {}
        self.tooltip_delays = {}

        # time delay before displaying the tooltip
        self.delay = delay
        self.kwargs = kwargs
        self.timer_id = None

        self.tooltip = None

        self.key = 'delay'
        self.keyval = self.delay
        self.current_widget = None

        self.text = text

        # self.configure(**kwargs)
        if self.text:
            self.tooltip_follows[str(self.widget)] = kwargs.pop('follow', False)
            self.widget.bind('<Enter>', self.enter, add=1)
            self.widget.bind('<Motion>', self.motion, add=1)
            self.widget.bind('<Leave>', self.leave, add=1)
            self.widget.bind('<ButtonPress>', self.leave, add=1)
        elif not self.istree:
            # keep track of binding ids to cleanly remove them
            self.bind_enter_ids = {}  # {widget name: bind id, ...}
            self.bind_leave_ids = {}  # {widget name: bind id, ...}
            # widget currently under the mouse if among wrapped widgets:
        else:
            self.current_widget = self.widget
            self.widget.bind('<Motion>', self._on_motion_tree, add=1)
            self.widget.bind('<Leave>', self._on_leave, add=1)

 # for a single widget
    def motion(self, event=None):
        if self.tooltip and self.tooltip_follows[str(self.widget)]: self.tooltip.position((event.x_root+20, event.y_root-10))

    def enter(self, event=None):
        '''
        Called by tkinter when mouse enters a widget
        :param event:  from tkinter.  Has x,y coordinates of mouse

        '''
        if str(event.widget) != str(self.widget): return

        self.x, self.y = event.x, event.y

        # Schedule a timer to time how long mouse is hovering
        self.id = self.widget.after(self.delay, self.showtip)

    def leave(self, event=None):
        '''
        Called by tkinter when mouse exits a widget
        :param event:  from tkinter.  Event info that's not used by function.

        '''
        # Cancel timer used to time mouse hover
        if self.id: self.widget.after_cancel(self.id)
        self.id = None

        # Destroy the tooltip window
        if self.tooltip: self.tooltip.destroy()
        self.tooltip = None

    def showtip(self, event=None):
        '''
        Creates a tooltip window with the tooltip text inside of it
        '''
        if self.tooltip: return
        self.lastMotion = 0

        x = self.widget.winfo_rootx() + self.x
        y = self.widget.winfo_rooty() + self.y - 20

        self.tooltip = PRMP_ToolTip(self.widget, pos=(x, y), text=self.text, **self.kwargs)
 # for a single widget

    def create_tooltip(self):
        self.tooltip = ToolTip(self.widget, **self.kwargs)

        if not self.istree: self.tooltip.bind('<Leave>', self._on_leave_tooltip)

    @property
    def cgetsub(self): return self.tooltip.cget if self.tooltip else self.tooltip

    def configure(self, **kwargs):
        try:
            self.delay = int(kwargs.pop('delay', self.delay))
        except ValueError:
            raise ValueError('expected integer for the delay option.')
        if self.tooltip: self.tooltip.configure(**kwargs)

    config = configure

    def add_tooltip(self, item, follow=False, delay=300, **kwargs):
        '''Add a tooltip with given text to the item.'''
        if not item: return

        name = str(item)
        self.tooltip_text[name] = kwargs
        self.tooltip_follows[name] = follow
        self.tooltip_delays[name] = delay or 200

        if not isinstance(item, str):
            self.bind_enter_ids[name] = item.bind('<Enter>', self._on_enter_widget)
            self.bind_leave_ids[name] = item.bind('<Leave>', self._on_leave)
            self.bind_leave_ids[name] = item.bind('<Motion>', self._on_motion_widget)

    def set_tooltip_text(self, item, follow=False, delay=100, **kwargs):
        '''Change tooltip text for given item.'''
        name = str(item)
        if name in self.tooltip_text:
            self.tooltip_text[name] = kwargs
            self.tooltip_follows[name] = follow
            self.tooltip_delays[name] = delay or 100

    def remove_tooltip(self, item):
        '''Remove widget from manager.'''
        try:
            name = str(item)
            del self.tooltip_text[name]
            if not self.istree:
                item.unbind('<Enter>', self.bind_enter_ids[name])
                item.unbind('<Leave>', self.bind_leave_ids[name])
                del self.bind_enter_ids[name]
                del self.bind_leave_ids[name]
                del self.tooltip_delays[name]
                del self.tooltip_follows[name]
        except KeyError: pass

    def remove_all(self):
        '''Remove all tooltips.'''
        self.tooltip_text.clear()
        if not self.istree:
            for name in self.tooltip_text:
                widget = self.tooltip.nametowidget(name)
                widget.unbind('<Enter>', self.bind_enter_ids[name])
                widget.unbind('<Leave>', self.bind_leave_ids[name])
            self.bind_enter_ids.clear()
            self.bind_leave_ids.clear()
            self.tooltip_follows.clear()
            self.tooltip_delays.clear()

    def _on_enter_widget(self, event):
        '''Change current widget and launch timer to display tooltip.'''
        if self.tooltip == None or not self.tooltip.winfo_ismapped():
            self.timer_id = event.widget.after(self.tooltip_delays[str(event.widget)], self.display_tooltip)
            self.current_widget = event.widget

    def _on_motion_tree(self, event):
        '''Withdraw tooltip on mouse motion and cancel its appearance.'''
        if not self.tooltip: self.create_tooltip()

        if self.tooltip.winfo_ismapped():
            x, y = self.widget.winfo_pointerxy()
            if self.widget.winfo_containing(x, y) != self.tooltip:
                if self.widget.identify_row(y - self.widget.winfo_rooty()):
                    self.tooltip.withdraw()
        else:
            try: self.widget.after_cancel(self.timer_id)
            except ValueError:
                # nothing to cancel
                pass
            self.timer_id = self.widget.after(self.delay, self.display_tooltip)

    def _on_motion_widget(self, event):
        'Tooltip will moves in a widget if the *follow==True*'

        if (self.current_widget == event.widget) and self.tooltip_follows[str(self.current_widget)] and self.tooltip: self.tooltip.position((event.x_root+20, event.y_root-10))

    def _on_leave(self, event):
        '''Hide tooltip if visible or cancel tooltip display.'''

        if self.istree:
            try: self.widget.after_cancel(self.timer_id)
            except ValueError:
                # nothing to cancel
                pass
        else:
            if self.tooltip == None: return

            if self.tooltip.winfo_ismapped():
                x, y = event.widget.winfo_pointerxy()
                if not event.widget.winfo_containing(x, y) in [event.widget, self.tooltip]:
                    self.tooltip.withdraw()
            else:
                try:
                    event.widget.after_cancel(self.timer_id)
                except ValueError:
                    pass
            self.current_widget = None

    def _on_leave_tooltip(self, event):
        '''Hide tooltip.'''
        if self.tooltip == None: return
        x, y = event.widget.winfo_pointerxy()
        if not event.widget.winfo_containing(x, y) in [self.current_widget, self.tooltip]: self.tooltip.withdraw()

    def display_tooltip(self):
        'Display tooltip'

        if self.current_widget is None:
            return

        if not self.tooltip: self.create_tooltip()

        disabled = False
        try: disabled = 'disabled' == self.current_widget['state']
        except AttributeError:
            try: disabled = self.current_widget.cget('state') == 'disabled'
            except: pass

        if self.istree:
            item = self.widget.identify_row(self.widget.winfo_pointery() - self.widget.winfo_rooty())
            x = self.widget.winfo_pointerx() + 14
            bbox = self.widget.bbox(item)
            if len(bbox) < 4:
                # it signifies that the mouse/pointer just moved outside the inside of the treeview widget
                return
            y = self.widget.winfo_rooty() + bbox[1] + bbox[3] - 14
            item = item if item in self.tooltip_text else ''

        else:
            item = str(self.current_widget)
            x = self.current_widget.winfo_pointerx() + 14
            y = self.current_widget.winfo_rooty() + self.current_widget.winfo_height() + 2
            item = item if item in self.tooltip_text else ''

        # print(disabled, '<>', item, '<>')
        if item and not disabled:
            kwargs = self.tooltip_text.get(item, {})
            self.tooltip.configure(**kwargs)
            self.tooltip.deiconify()
            self.tooltip.position((x, y))

ToolTipsManager = PRMP_ToolTipsManager
