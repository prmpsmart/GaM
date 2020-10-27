from .prmp_tk.two_widgets import *

class RegionRadioCombo(RC):
    
    def __init__(self, master=None, region=None, reciever=None, regionLevel=5, **kwargs):
        super().__init__(master, **kwargs)
        
        self.subRegionDict = {}
        self.set(region)
        self.choosen = None
        self._receiver = None
        self.regionLevel = regionLevel
    
    def setReciever(self, reciever): self._receiver = reciever
    
    def clicked(self, e=0):
        val = super().clicked()
        regVal = self.subRegionDict.get(val)
        if self._receiver: self._receiver(self, regVal)
    
    def get(self):
        if self.B.get() in self.subRegionDict:
            pass
        else: return self.choosen
    
    def _set(self, region):
        if region:
            rm = region.regionsManagers
            regs = len(rm)
            if rm[0] == None:
                print('member/client')
            elif regs == 1: self.setKeys(rm[0])
                
            elif regs == 2:
                pass
            self.region = region
    
    def set(self, region):
        if region:
            # print(repr(region))
            regionLevel = len(region.hierachy)
            if regionLevel == self.regionLevel: self.setKeys(region)
            else: raise SyntaxError(f'Incorrect region of level {regionLevel} given, level must be {self.regionLevel} ')
                
            self.region = region
    
    def receiver(self, wid, region):
        self.var.set(self.val)
        wid.unlight()
        self.light()
        self.set(region)
            
    def processRegionSubs(self, region):
        self.subRegionDict = {}
        rm = region.regionsManagers
        regs = len(rm)
        first = rm[0]
        if first != None:
            if regs == 1: sub = first
            else:
                sub = []
                for manager in rm: sub += manager[:]
            for region in sub:
                try: number = region.number
                except: number = sub.index(region) + 1
                name = f'{number})  {region.name} '
                self.subRegionDict[name] = region
        else: self.subRegionDict[region.name] = region
    
    def setKeys(self, region=None):
        if region: self.processRegionSubs(region)
        keys = self.getSubKeys()
        self.B.set(keys)
        
    def getSubKeys(self):
        keys = list(self.subRegionDict.keys())
        keys.sort()
        return keys


RRC = RegionRadioCombo

class RegionDetails(PRMP_Tk, FillWindow):
    
    def __init__(self, region=None, title='Region Details', geo=(600, 250), values={}, **kwargs):
        PRMP_Tk.__init__(self, title=title, geo=geo, gaw=1, ntb=1, **kwargs)
        FillWindow.__init__(self, values=values)
        
        self.region = region
        self.setupApp()
        self.fill()
        
        self.mainloop()
    
    # def fill(self, values={}):
    #     if super().fill(values):
        
    #         if self.region:
    #             sups = self.region.sups
    #             first = sups[0]
                
    
    def setupApp(self):
        self.addTitleBar()
        self.addStatusBar()
        
        self.hierachy = LF(self, text='Hierachy')
        self.hierachy.place(x=10, y=30, h=150, w=335)
        
        self.hierachyVar = tk.StringVar()
        self.hierachyVar.set('0')
        
        self.office = RRC(self.hierachy,  topKwargs={'text': 'Office', 'value': 'off', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=0, relh=.23, relw=.96, longent=.3, regionLevel=1)
        
        self.department = RRC(self.hierachy,  topKwargs={'text': 'Department', 'value': 'dep', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.25, relh=.23, relw=.96, longent=.35, regionLevel=2)
        self.office.setReciever(self.department.receiver)
        
        self.sup = RRC(self.hierachy,  topKwargs={'text': 'Superscript', 'value': 'sup', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.5, relh=.23, relw=.96, longent=.35, regionLevel=3)
        self.department.setReciever(self.sup.receiver)
        
        self.sub = RRC(self.hierachy,  topKwargs={'text': 'Subscript', 'value': 'sub', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.75, relh=.23, relw=.96, longent=.3, regionLevel=4)
        self.sup.setReciever(self.sub.receiver)
        
        # workers in the region or the individual 
        persons = PCb(self, text='Persons', command=self.showPersons)
        persons.place(x=10, y=190, h=24, w=90)
        
        switch = PCb(self, text='Switch?', command=self.switch)
        switch.place(x=120, y=190, h=24, w=90)
        
        new = PCb(self, text='New Dialog ?')
        new.place(x=225, y=190, h=24, w=120)
       
        
        self.image = IL(self)
        self.image.place(x=360, y=40, h=170, w=230)
        
        self.addChildWidgets([persons, switch, new, self.hierachy, self.image])
        
        self.addResultsWidgets(['office', 'department', 'sup', 'image', 'sub'])
        
        self.setRadioGroups([self.office, self.department, self.sub, self.sup])
        
    def showPersons(self):
        pass
    
    def switch(self):
        # to switch between subregions and accounts
        pass
        
    def loadRegion(self, region=None, account=1):
        if region:
            self.region = region
            self.titleBar.config(text=f'{self.region} Details Dialog')
        
       





