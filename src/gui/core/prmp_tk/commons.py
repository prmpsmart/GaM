
import time
from .core import PTp, L, PTh, Tk, F

class ToolTip:
    def __init__(self, wdgt, msg=None, font=None, delay=1, follow=True, tipGeo=(100, 40), **kwargs):
        self.wdgt = wdgt
        self.parent = self.wdgt.master
        
        self.msg = msg

        self.tipGeo = tipGeo
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        self.top = None
        self.font = font
        self.kwargs = kwargs
        
        
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')
        

    def spawn(self, event=None):
        self.visible = 1
        self.wdgt.after(int(self.delay * 1000), self.show)

    def show(self):
        spl = self.msg.split('\n')
        c = 0
        for v in spl:
            i = len(v)
            if i > c: c = i
        
        r = len(spl)
        r = r or 1
        self.tipGeo = c * 7, r * 20

        self.top = PTp(self.parent, geo=self.tipGeo, ntb=1, tm=1, **self.kwargs)
        
        L(self.top, text=self.msg or 'No message provided', background=PTh.DEFAULT_BACKGROUND_COLOR, font=self.font, relief='groove').place(relx=0, rely=0, relh=1, relw=1)
        # self.withdraw()
        
        if self.visible == 1 and time.time() - self.lastMotion > self.delay: self.visible = 2
        if self.visible == 2: self.top.deiconify()
        
        self.top.mainloop()

    def move(self, event):
        if self.top:
            self.lastMotion = time.time()
            if self.follow is False:
                self.withdraw()
                self.visible = 1
            self.top.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
            
            #To get the present event coordinates
            # print(event.x_root,event.y_root)
            
            # self.top.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        if self.top:
            self.visible = 0
            # self.top.withdraw()
            self.top.destroy()
        # self.parent.state('normal')

class SolidScreen(Tk):
    def __init__(self, side='top-center', gaw=1, bd=12, geo=(),**kwargs):
        super().__init__(tm=1, gaw=gaw, geo=geo or (500, 500), side=side, atb=1, asb=1, **kwargs)
        
        self.frame = F(self, relief='solid')
        self.frame['bd'] = 12
        y, h = self.y_h
        self.frame.place(x=0, y=y, relw=1, h=h)
        
        self.paint()
        # self.mainloop()
    

SS = SolidScreen

