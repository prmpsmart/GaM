from .prmp_tk.two_widgets import *

class RegionDetails(PRMP_Tk, FillWindow):
    
    def __init__(self, region=None, title='Region Details', geo=(600, 220), values={}, **kwargs):
        PRMP_Tk.__init__(self, title=title, geo=geo, gaw=1, ntb=1, **kwargs)
        FillWindow.__init__(self, values=values)
        
        self.region = region
        self.setupApp()
        self.fill()
        self.mainloop()
    
    def setupApp(self):
        self.addTitleBar()
        
        self.hierachy = LF(self, text='Hierachy')
        self.hierachy.place(x=10, y=30, h=150, w=335)
        
        self.hierachyVar = tk.StringVar()
        self.hierachyVar.set('0')
        
        self.office = RC(self.hierachy,  topKwargs={'text': 'Office', 'value': 'off', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=0, relh=.23, relw=.96, longent=.3)
        
        self.department = RC(self.hierachy,  topKwargs={'text': 'Department', 'value': 'dep', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.25, relh=.23, relw=.96, longent=.35)
        
        self.sup = RC(self.hierachy,  topKwargs={'text': 'Superscript', 'value': 'sup', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.5, relh=.23, relw=.96, longent=.35)
        
        self.sub = RC(self.hierachy,  topKwargs={'text': 'Subscript', 'value': 'sub', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.75, relh=.23, relw=.96, longent=.3)
        
        # workers in the region or the individual 
        persons = PCb(self, text='Persons', command=self.showPersons)
        persons.place(x=10, y=190, h=24, w=90)
        
        new = PCb(self, text='New Dialog ?')
        new.place(x=225, y=190, h=24, w=120)
        
        self.image = IL(self)
        self.image.place(x=360, y=40, h=170, w=230)
        
        self.childWidgets += [persons, new, self.hierachy, self.image]
        self.resultsWidgets = ['office', 'department', 'sup', 'image', 'sub']
        
        self.setRadioGroups([self.office, self.department, self.sub, self.sup])

    
    def showPersons(self):
        pass
        
    def loadRegion(self, region=None, account=1):
        if region:
            self.region = region
            self.titleBar.config(text=f'{self.region} Details Dialog')
        
       





