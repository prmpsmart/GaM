from itertools import zip_longest

from .agam_dialogs import *
from .prmp_tk.scrollables import bound_to_mousewheel, PRMP_TreeView


class RegionRadioCombo(RC):
    
    def __init__(self, master=None, region=None, regionLevel=5, recievers=[], **kwargs):
        super().__init__(master, **kwargs)
        
        self._subRegionDict = {}
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
        regVal = self.get()
        
        if regVal and self._receivers:
            for recv in self._receivers: recv((self, regVal))
    
    def get(self):
        val = self.B.get()
        regVal = self.subRegionDict.get(val)
        _regval = self._subRegionDict.get(val)
        
        if regVal: return regVal
        elif _regval: return _regval
        else: return self.choosen
    
    def receiver(self, tup):
        wid, region = tup
        self.var.set(self.val)
        wid.unlight()
        self.light()
        self.set(region)
        
    def processRegionSubs(self, region):
        rm = region.subRegions
        
        if rm:
            for region in rm:
                rname = region.name
                self._subRegionDict[rname] = region
                try: number = region.number
                except: number = rm.index(region) + 1
                name = f'{number})  {rname}'
                self.subRegionDict[name] = region
        # else: self.subRegionDict[region.name] = region
    
    def setKeys(self, region=None):
        if region:
            self.processRegionSubs(region)
            keys = self.getSubKeys()
            if keys:
                self.changeValues(keys)
                self.B.set(keys[0])
        
    def set(self, region):
        self._subRegionDict = {}
        self.subRegionDict = {}
        if region:
            regionLevel = len(region.hierachy)
            
            assert regionLevel  == self.regionLevel, f'Incorrect region of level {regionLevel} given, level must be {self.regionLevel}'
            self.setKeys(region)
            self.region = region
    
    def getSubKeys(self):
        keys = list(self.subRegionDict.keys())
        keys.sort()
        
        return keys
RRC = RegionRadioCombo

class Hierachy(PRMP_TreeView):
    __shows = ['tree', 'headings']
    __slots__ = ['tree']
    
    def __init__(self, master=None, columns=[], **kwargs):
        super().__init__(master=master, columns=columns, **kwargs)
        
    
    def bindings(self):
        super().bindings()
        self.tree.bind('<Control-Return>', self.viewRegion)

    def viewRegion(self, e=0):
        current = self.selected()
        if current:
            if current.level == 5: PersonDialog(self, title=current.name, values=current.person.values)
            else: RegionDetails(self, region=current)
H = Hierachy


class RegionDetails(PRMP_Window, FillWindow):
    
    def __init__(self, master=None, title='Region Details', geo=(600, 250), values={}, region=None, **kwargs):
        
        PRMP_Window.__init__(self, master, title=title, geo=geo, gaw=1, ntb=1, tm=1, atb=1, asb=1, **kwargs)
        FillWindow.__init__(self, values=values)
        
        self.region = region
        self.personDialog = None
        self.switchState = None
        self.setupApp()
        
        self.fill()
        self.paint()
        
        
        if self.region:
            for wid in [self.office, self.department, self.sub, self.sup]:
                if self.region.level == wid.regionLevel: wid.set(self.region)
        
    def regionChanged(self, region):
        region = region[1]
        if not region: return
        text = ''
        hie = region.hierachy
        
        for reg in hie[1:]:
            if len(hie) > 2 and reg is hie[2]: name = reg.DEPARTMENT
            else: name = reg.name
            text += name + ' | '

        te = text.split('|')[:-1]
        text = ' | '.join(te)
        
        self.region = region
        self.titleBar.set(text)
        
        person = region.person
        if person: self.fill(person.values)
    
    def setupApp(self):
        # self.addTitleBar()
        # self.addStatusBar()
        
        self.frame = F(self, relief='groove')
        y, h = self.y_h
        x, w = self.x_w
        self.frame.place(x=2, y=y, relw=w, h=h)
        self.w = w
        
       # hierachy
        self.hierachy = LF(self.frame, text='Hierachy')
        self.hierachy.place(relx=0, y=0, h=150, w=335)
        
        self.hierachyVar = tk.StringVar()
        self.hierachyVar.set('0')
        
        self.office = RRC(self.hierachy,  topKwargs={'text': 'Office', 'value': 'off', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=0, relh=.25, relw=.96, longent=.3, regionLevel=1, recievers=[self.regionChanged])
        
        self.department = RRC(self.hierachy,  topKwargs={'text': 'Department', 'value': 'dep', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.25, relh=.25, relw=.96, longent=.35, regionLevel=2, recievers=[self.regionChanged])
        self.office.addReceiver(self.department.receiver)
        
        self.sup = RRC(self.hierachy,  topKwargs={'text': 'Superscript', 'value': 'sup', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.5, relh=.25, relw=.96, longent=.35, regionLevel=3, recievers=[self.regionChanged])
        self.department.addReceiver(self.sup.receiver)
        
        self.sub = RRC(self.hierachy,  topKwargs={'text': 'Subscript', 'value': 'sub', 'variable': self.hierachyVar}, orient='h', relx=.02, rely=.75, relh=.25, relw=.96, longent=.3, regionLevel=4, recievers=[self.regionChanged])
        self.sup.addReceiver(self.sub.receiver)
        
        # workers in the region or the individual 
        persons = B(self.frame, text='Persons', command=self.showPersons)
        persons.place(x=0, y=155, h=24, w=90)
        
        switch = B(self.frame, text='Switch?', command=self.switch)
        switch.place(x=110, y=155, h=24, w=90)
        
        new = PCb(self.frame, text='New Dialog ?')
        new.place(x=215, y=155, h=24, w=120)
       
        
        self.image = IL(self)
        self.image.place(x=360, y=40, h=170, w=230)
    
       # accounts
        self.accounts = LF(self, text='Accounts')
       # subregions
        self.subRegions = LF(self, text='Sub Regions')
        
        self.addResultsWidgets(['office', 'department', 'sup', 'image', 'sub'])
        
        self.setRadioGroups([self.office, self.department, self.sub, self.sup])
        
    def showPersons(self, e=0):
        if self.personDialog: self.personDialog.destroy()
        if self.region:
            if self.region.level == 5:
                self.personDialog = PersonDialog(values=self.region.person.values, side='center')
            else: print('Level not upto')
    
    def switch(self):
        # to switch between subregions and accounts
        if self.switchState == None:
            if self.hierachyVar.get() != self.sub.val:
                self.showSubRegionsContainer()
                self.switchState = True
            else:
                self.showAccountsContainer()
                self.switchState = False
            
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
        self.subRegions.place(x=2, y=220, h=350, relw=self.w)
        self.expand()
        
    def showAccountsContainer(self):
        self.subRegions.place_forget()
        self.accounts.place(x=2, y=220, h=350, relw=self.w)
        self.expand()
RD = RegionDetails

