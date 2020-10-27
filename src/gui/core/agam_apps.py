from .prmp_tk.two_widgets import *
import tkinter.ttk as ttk
import tkinter as tk



class RegionHierachy(PRMP_Tk):
    
    def __init__(self, region):
        super().__init__()
        self.nodes = {}
        frame = tk.Frame(self)
        self.tree = ttk.Treeview(frame)
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Project tree', anchor='w')

        self.tree.grid(row=0, column=0, rowspan=10, columnspan=10)
        ysb.grid(row=0, column=11, rowspan=10, sticky='ns')
        xsb.grid(row=11, column=0, columnspan=10, sticky='ew')
        frame.grid()

        self.region = region
        self.processRegion(self.region)
    
    def processRegion(self, region):
        regionsManagers = region.regionsManagers
        if regionsManagers[0]:
            for rm in regionsManagers: self.processRegion(rm)

RH = RegionHierachy


class RegionDetails(PRMP_Tk, FillWindow):
    
    def __init__(self, region=None, title='Region Details', geo=(600, 600), values={}, **kwargs):
        PRMP_Tk.__init__(self, title=title, geo=geo, ntb=1, **kwargs)
        
        self.region = region
    
        self.addTitleBar()
        
        hierachy = LF(self, text='Hierachy')
        hierachy.place(x=10, y=30, h=150, w=335)
        
        self.office = CC(hierachy,  text='Office', orient='h', relx=.02, rely=0, relh=.23, relw=.96, longent=.3)
        
        self.department = CC(hierachy,  text='Department', orient='h', relx=.02, rely=.25, relh=.23, relw=.96, longent=.35)
        
        self.sup = CC(hierachy,  text='Superscript', orient='h', relx=.02, rely=.5, relh=.23, relw=.96, longent=.35)
        
        self.sub = CC(hierachy,  text='Subscript', orient='h', relx=.02, rely=.75, relh=.23, relw=.96, longent=.3)
        
        persons = PCb(self, text='Persons')
        persons.place(x=10, y=190, h=24, w=90)
        
        new = PCb(self, text='New Dialog ?')
        new.place(x=225, y=190, h=24, w=120)
        
        self.image = IL(self)
        self.image.place(x=360, y=40, h=170, w=230)
        
        account = LF(self, text='Account')
        account.place(x=10, y=220, h=270, w=280)
        
        self.childWidgets += [persons, new, account, hierachy, self.image]
        self.resultsWidgets = ['office', 'department', 'sup', 'image', 'sub']
        
        FillWindow.__init__(self, values=values)
        
        self.mainloop()
        
    def loadRegion(self, region=None):
        if region:
            self.region = region
            self.titleBar.config(text=f'{self.region} Details Dialog')
        
       





