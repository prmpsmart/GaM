from .....backend.utils.colours import Colours
from .....backend.utils.fonts import Fonts
from tkinter import Tk, Label, Button

class Test(Tk):
    def __init__(self):
        super().__init__()
        self.cn = 0
        self.cp = 0
        self.cm = 0
        self.title("Color Test Proudly PRMPSmart made")
        self.geometry("500x500+495+63")
        # self.iconify()
        # self.deiconify()
        self.resizable(0, 0)
        self.configure(background="pink", highlightbackground=Colours.colors_values[5], highlightcolor=Colours.colors_values[25])

        self.btn1 = Button(self, text="Color Plus", font="-family {Times New Roman} -size 10 -weight bold ", relief="flat", overrelief="ridge")
        self.btn1.place(x=1, y=1, height=100, width=100)
        self.btn1.bind("<1>", self.chpl)

        self.btn2 = Button(self, text="Center", font="-family {Times New Roman} -size 10 -weight bold ", relief="flat", overrelief="ridge")
        self.btn2.place(x=201, y=1, height=100, width=100)
        self.btn2.bind("<1>", self.cen)

        self.btn3 = Button(self, text="Color Minus", font="-family {Times New Roman} -size 10 -weight bold ", relief="flat", overrelief="ridge")
        self.btn3.place(x=399, y=1, height=100, width=100)
        self.btn3.bind("<1>", self.chmn)

        self.lbl1 = Label(self, text="Color Test", font="-family {Times New Roman} -size 24 -weight bold ", relief="flat")
        self.lbl1.place(x=10, y=140, height=200, width=200)

        self.lbl2 = Label(self, text="Color Test", font="-family {Times New Roman} -size 24 -weight bold ", relief="flat")
        self.lbl2.place(x=150, y=380, height=100, width=200)

        self.lbl3 = Label(self, text="Color Test", font="-family {Times New Roman} -size 24 -weight bold ", relief="flat")
        self.lbl3.place(x=290, y=150, height=200, width=200)
        
        self.mainloop()
        
    def chpl(self,a):
        oss = Colours.getti(self.cp%120)
        ss = oss[1]
        self.btn1.config(background=ss, activebackground=ss)
        self.lbl1.config(text="%s\n\n%s"%(oss[0],ss), background=ss)
        self.cp += 1
    def cen(self,a):
        oss = Colours.getti(self.cn%120)
        ss = oss[1]
        self.config(background=ss)
        self.btn2.config(background=ss, activebackground=ss)
        self.lbl2.config(text="%s\n\n%s"%(oss[0],ss), background=ss)
        self.cn += 1
    def chmn(self,a):
        oss = Colours.getti(self.cm%120)
        ss = oss[1]
        self.btn3.config(background=ss, activebackground=ss)
        self.lbl3.config(text="%s\n\n%s"%(oss[0],ss), background=ss)
        self.cm -= 1
    
    def start(self): self.mainloop()

