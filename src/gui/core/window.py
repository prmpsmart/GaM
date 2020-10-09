from random import randint
from tkinter import Tk, Toplevel


class Window:
    _top = 'top'
    _left = 'left'
    _right = 'right'
    _bottom = 'bottom'
    _center = 'center'
    _sides = [_top, _left, _right, _bottom, _center]
        
    def bind_exit(self): self.bind('<Control-u>', exit)
    
    def setupOfWindow(self, gaw=False, ntb=False, tm=False, tw=False, alp=1, grabAnyWhere=False, geo=(), geometry=(), noTitleBar=False, topMost=False, alpha=1, toolWindow=False, side='center', title='Window', bg='SystemButtonFace'):
        
        if geo: geometry = geo
        if gaw: grabAnyWhere = gaw
        if ntb: noTitleBar = ntb
        if tm: topMost = tm
        if alp: alpha = alp
        if tw: toolWindow = tw
        
        self.title(title)
        self.config(bg=bg)
        self.side = side
        
        self.attributes('-topmost', topMost, '-toolwindow', toolWindow, '-alpha', alpha)
        
        if grabAnyWhere: self._grab_anywhere_on()
        else: self._grab_anywhere_off()
        
        if noTitleBar:
            self.state('withdrawn')
            self.overrideredirect(1)
            self.state('normal')
        
        self.lastPoints = [0, 0, 0, 0]
        self._geometry = geometry
        
        error_string = f'side must be of {self._sides} or combination of "center-{self._sides[:-1]}" delimited by "-". e.g center-right. but the two must not be the same.'
        
        if side:
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
        

    def _move(self, event):
        try: self.x, self.y = event.x, event.y
        except: pass
    
    def _grab_anywhere_on(self):
        self.bind("<ButtonPress-1>", self._move)
        self.bind("<ButtonRelease-1>", self._move)
        self.bind("<B1-Motion>", self._onMotion)
    def _grab_anywhere_off(self):
        self.unbind("<ButtonPress-1>")
        self.unbind("<ButtonRelease-1>")
        self.unbind("<B1-Motion>")
    def _onMotion(self, event):
        try:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.winfo_x() + deltax
            y = self.winfo_y() + deltay
            self.geometry("+%s+%s" % (x, y))
        except Exception as e:
            print('on motion error', e)
    def screenwidth(self): return self.winfo_screenwidth() - 70
    def screenheight(self): return self.winfo_screenheight() - 70
    def getWhichSide(self): return randint(1, 15) % 3
    @property
    def getXY(self):
        if self._geometry: return self._geometry[:3]
        return (0, 0)
    
    def _pointsToCenterOfScreen(self, x, y):
        screen_x, screen_y = self.screenwidth(), self.screenheight()
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
    
    def centerOfTopOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-1] = 50
        self.setGeometry(points)
        
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
        self.setGeometry(points)
        
    def topLeftOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2:] = 50, 50
        self.setGeometry(points)
        
    def topRightOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-1] = 50
        points[2] *= 2
        self.setGeometry(points)
        
    def bottomLeftOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2] = 50
        points[-1] *= 2
        self.setGeometry(points)
        
    def bottomRightOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-2] *= 2
        points[-1] *= 2
        self.setGeometry(points)
    
    def topOfScreen(self): [self.topLeftOfScreen, self.topRightOfScreen, self.centerOfTopOfScreen][self.getWhichSide()]()
    def bottomOfScreen(self): [self.bottomLeftOfScreen, self.bottomRightOfScreen, self.centerOfBotomOfScreen][self.getWhichSide()]()
    def rightOfScreen(self): [self.bottomRightOfScreen, self.topRightOfScreen, self.centerOfRightOfScreen][self.getWhichSide()]()
    def leftOfScreen(self): [self.bottomLeftOfScreen, self.topLeftOfScreen, self.centerOfLeftOfScreen][self.getWhichSide()]()
    
    def _isDialog(self):
        self.grab_set()
        self.wait_window()

class PRMPTk(Tk, Window):
    def __init__(self): super().__init__()

class PRMPToplevel(Toplevel, Window):
    def __init__(self, master=None): super().__init__(master)








