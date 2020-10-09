from tkinter import StringVar, Toplevel, Message
from time import time


class ToolTip(Toplevel):
    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None, delay=1, follow=True):
        self.wdgt = wdgt
        self.parent = self.wdgt.master
        Toplevel.__init__(self, self.parent, background='black', padx=1, pady=1)
        self.withdraw()
        self.overrideredirect(True)
        self.msgVar = StringVar()
        if msg is None: self.msgVar.set('No message provided')
        else: self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        Message(self, textvariable=self.msgVar, background='yellow', font=tooltip_font, aspect=1000).grid()
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        self.visible = 1
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        if self.visible == 1 and time() - self.lastMotion > self.delay: self.visible = 2
        if self.visible == 2: self.deiconify()

    def move(self, event):
        self.lastMotion = time()
        if self.follow is False:
            self.withdraw()
            self.visible = 1
        self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
        
        #To get the present event coordinates
        print(event.x_root,event.y_root)
        
        try: self.msgVar.set(self.msgFunc())
        except: pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        self.visible = 0
        self.withdraw()
#===========================================================
#                   End of Class ToolTip
#===========================================================