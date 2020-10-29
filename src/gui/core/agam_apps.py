from .agam_dialogs import *
from .prmp_tk.usefuls import bound_to_mousewheel

class RegionRadioCombo(RC):
    
    def __init__(self, master=None, region=None, regionLevel=5, recievers=[], **kwargs):
        super().__init__(master, **kwargs)
        
        self.subRegionDict = {}
        self.set(region)
        self.choosen = None
        self._receivers = recievers
        self.regionLevel = regionLevel
    
    def addReceiver(self, receiver):
        if receiver not in self._receivers: self._receivers.append(receiver)
        elif isinstance(receiver, (list, tuple)): 
            for recv in receiver: self.addReceiver(recv)
    
    def clicked(self, e=0):
        val = super().clicked()
        regVal = self.subRegionDict.get(val)
        if self._receivers:
            for recv in self._receivers: recv((self, regVal))
    
    def get(self):
        if self.B.get() in self.subRegionDict:
            pass
        else: return self.choosen
    
    def set(self, region):
        if region:
            # print(repr(region))
            regionLevel = len(region.hierachy)
            if regionLevel == self.regionLevel: self.setKeys(region)
            else: raise SyntaxError(f'Incorrect region of level {regionLevel} given, level must be {self.regionLevel} ')
                
            self.region = region
    
    def receiver(self, tup):
        wid, region = tup
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
                name = f'{number})  {region.name}'
                self.subRegionDict[name] = region
        else: self.subRegionDict[region.name] = region
    
    def setKeys(self, region=None):
        if region: self.processRegionSubs(region)
        keys = self.getSubKeys()
        if keys:
            self.changeValues(keys)
            self.B.set(keys[0])
        
    def getSubKeys(self):
        keys = list(self.subRegionDict.keys())
        keys.sort()
        return keys
RRC = RegionRadioCombo



class Hierachy(PRMP_Frame):
    __shows = ['tree', 'headings']
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        
        self.t = self.tree = self.treeview = PRMP_Treeview(self)
        xscrollbar = PRMP_Scrollbar(self, orient="horizontal", command=self.treeview.xview)
        yscrollbar = PRMP_Scrollbar(self, orient="vertical", command=self.treeview.yview)
        self.treeview.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        
        xscrollbar.pack(side="bottom", fill="x")
        self.treeview.pack(side='left', fill='both', expand=1)
        yscrollbar.pack(side="right", fill="y")
        bound_to_mousewheel(0, self)
        
        self.ivd = self.itemsValuesDict = {}
        
        
    
    def setHeadings(self, headings=[]):
        for head in headings:
            self.heading(head.name, head.name)
    
    def insert(self, item, position='end', **kwargs): return self.treeview.insert(item, position, **kwargs)
    
    def heading(self, item, **kwargs): return self.treeview.heading(item, **kwargs)
    
    def column(self, item, **kwargs): return self.treeview.column(item, **kwargs)
    
    def treeviewConfig(self, **kwargs): self.treeview.configure(**kwargs)
    
    tvc = Config = treeviewConfig
    
    def test1(self, region=None, parent=''):
        rm = region.regionsManagers
        regs = len(rm)
        first = rm[0]
        if first != None:
            if regs == 1: sub = first
            else:
                sub = []
                for manager in rm: sub += manager[:]
            for region in sub:
                item = self.insert(parent, text=region.name)
                self.ivd[item] = region
        else: self.ivd[parent] = region
    
    def test(self, region=None, parent=''):
        rm = region.regionsManagers
        regs = len(rm)
        first = rm[0]
        if first != None:
            if regs == 1:
                parent = self.insert(parent, text=region.name)
                for rg in rm[0]:
                    item = self.insert(parent, text=rg.name)
                    self.ivd[item] = rg
            else:
                for manager in rm:
                    item = self.insert(parent, text=manager.name)
                    self.ivd[item] = region
        else:
            item = self.insert(parent, text=region.name)
            
            self.ivd[item] = region
    
    
    
    
    
    
H = Hierachy




class RegionDetails(PRMP_Tk, FillWindow):
    
    def __init__(self, title='Region Details', geo=(600, 250), values={}, **kwargs):
        PRMP_Tk.__init__(self, title=title, geo=geo, gaw=1, ntb=1, tm=1, **kwargs)
        FillWindow.__init__(self, values=values)
        
        self.region = None
        self.personDialog = None
        self.switchState = None
        self.setupApp()
        self.fill()
        self.paint()
        self.mainloop()
        
    def regionChanged(self, region):
        region = region[1]
        if not region: return
        text = ''
        hie = region.hierachy
        for reg in hie[1:]:
            if len(hie) > 2 and reg == hie[2]: name = reg.name.split(hie[1].name)[1]
            else: name = reg.name
            text += name + ' | '
        te = text.split('|')[:-1]
        text = ' | '.join(te)# + 'details.'
        self.region = region
        self.titleBar.set(text)
    
    def setupApp(self):
        self.addTitleBar()
        self.addStatusBar()
       
       # hierachy
        self.hierachy = LF(self, text='Hierachy')
        self.hierachy.place(relx=0, y=30, h=150, w=335)
        
        self.hierachyVar = tk.StringVar()
        self.hierachyVar.set('0')
        
        self.office = RRC(self.hierachy,  topKwargs={'text': 'Office', 'value': 'off', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=0, relh=.23, relw=.96, longent=.3, regionLevel=1, recievers=[self.regionChanged])
        
        self.department = RRC(self.hierachy,  topKwargs={'text': 'Department', 'value': 'dep', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.25, relh=.23, relw=.96, longent=.35, regionLevel=2, recievers=[self.regionChanged])
        self.office.addReceiver(self.department.receiver)
        
        self.sup = RRC(self.hierachy,  topKwargs={'text': 'Superscript', 'value': 'sup', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.5, relh=.23, relw=.96, longent=.35, regionLevel=3, recievers=[self.regionChanged])
        self.department.addReceiver(self.sup.receiver)
        
        self.sub = RRC(self.hierachy,  topKwargs={'text': 'Subscript', 'value': 'sub', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.75, relh=.23, relw=.96, longent=.3, regionLevel=4, recievers=[self.regionChanged])
        self.sup.addReceiver(self.sub.receiver)
        
        # workers in the region or the individual 
        persons = B(self, text='Persons', command=self.showPersons)
        persons.place(x=0, y=190, h=24, w=90)
        
        switch = B(self, text='Switch?', command=self.switch)
        switch.place(x=110, y=190, h=24, w=90)
        
        new = PCb(self, text='New Dialog ?')
        new.place(x=215, y=190, h=24, w=120)
       
        
        self.image = IL(self)
        self.image.place(x=360, y=40, h=170, w=230)
    
       # accounts
        self.accounts = LF(self, text='Accounts')
       # subregions
        self.subRegions = LF(self, text='Sub Regions')
        
        self.addResultsWidgets(['office', 'department', 'sup', 'image', 'sub'])
        
        self.setRadioGroups([self.office, self.department, self.sub, self.sup])
        
    def showPersons(self):
        if self.personDialog: self.personDialog.destroy()
        if self.region:
            if self.region.level == 5:
                self.personDialog = PersonDialog(values=self.region.person.values, side='center')
    
    def switch(self):
        # to switch between subregions and accounts
        if self.switchState == None:
            self.showSubRegionsContainer()
            self.switchState = True
            
        elif self.switchState == True:
            self.showAccountsContainer()
            self.switchState = False
            
        elif self.switchState == False:
            self.unExpand()
            self.switchState = None
        
    def loadRegion(self, region=None, account=1):
        if region:
            self.region = region
            self.titleBar.config(text=f'{self.region} Details Dialog')
        
    def unExpand(self):
        self.changeGeometry((600, 250))
        self.accounts.place_forget()
        self.placeStatusBar()
        
    def expand(self):
        self.changeGeometry((800, 600))
        self.placeStatusBar()
        
    def showSubRegionsContainer(self):
        self.subRegions.place(relx=0, y=220, h=350, relw=1)
        self.expand()
        
    def showAccountsContainer(self):
        self.subRegions.place_forget()
        self.accounts.place(relx=0, y=220, h=350, relw=1)
        self.expand()





