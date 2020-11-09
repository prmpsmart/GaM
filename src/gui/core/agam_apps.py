from .agam_dialogs import *
from .prmp_gui.extensions import bound_to_mousewheel, PRMP_TreeView


class RegionRadioCombo(RadioCombo):
    
    def __init__(self, master=None, region=None, regionLevel=5, recievers=[], **kwargs):
        super().__init__(master, **kwargs)
        
        self._subRegionDict = {}
        self.subRegionDict = {}
        self.set(region)
        self.choosen = None
        self.region = region
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
        if region:
            self.subRegionDict = {}
            self._subRegionDict = {}
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
            if current._type == 'reg':
                if current.level == 5: PersonDialog(self, title=current.name, values=current.person.values)
                else: RegionDetails(self, region=current)
H = Hierachy


class RegionDetails(PRMP_MainWindow, FillWidgets):
    
    def __init__(self, master=None, title='Region Details', geo=(600, 250), expandGeo=(800, 600), values={}, region=None, **kwargs):
        
        PRMP_MainWindow.__init__(self, master, title=title, geo=geo, gaw=1, ntb=1, tm=1, atb=1, asb=1, **kwargs)
        
        FillWidgets.__init__(self, values=values)
        
        self.region = region
        self.personDialog = None
        self.switchState = None
        self._sub = None
        self.geo_ = geo
        self.expandGeo = expandGeo
        
        self._setupApp()

        # self.root.isMaximized = self.isMaximized
        # self.root.isNormal = self.isMaximized

        self.fill()
        self.paint()
        
        if self.region:
            for wid in [self.office, self.department, self.sub, self.sup]:
                if self.region.level == wid.regionLevel: wid.set(self.region)
        
    def regionChanged(self, region):
        region = region[1]
        if not region or (region is self.region): return
    
        self.region = region
        self.titleBar.set(region.idText)
        
        person = region.person
        if person: self.fill(dict(image=person.image))

        self.loadAccounts(region)

    
    def _setupApp(self):
       # hierachy
        self.hierachy = PRMP_LabelFrame(self.container, config=dict(text='Hierachy'))
        self.hierachy.place(x=2, y=0, h=150, relw=.6)
        
        self.hierachyVar = tk.StringVar()
        self.hierachyVar.set('0')
        
        self.office = RegionRadioCombo(self.hierachy,  topKwargs=dict(text= 'Office', value= 'off', variable= self.hierachyVar), bottomKwargs=dict(placeholder='Enter Office Name'), orient='h', relx=.02, rely=0, relh=.25, relw=.96, longent=.3, regionLevel=1, recievers=[self.regionChanged], dot=1)
        
        self.department = RegionRadioCombo(self.hierachy,  topKwargs=dict(text= 'Department', value= 'dep', variable= self.hierachyVar), orient='h', relx=.02, rely=.25, relh=.25, relw=.96, longent=.35, regionLevel=2, recievers=[self.regionChanged], dot=1)
        self.office.addReceiver(self.department.receiver)
        
        self.sup = RegionRadioCombo(self.hierachy,  topKwargs=dict(text= 'Superscript', value= 'sup', variable= self.hierachyVar), orient='h', relx=.02, rely=.5, relh=.25, relw=.96, longent=.35, regionLevel=3, recievers=[self.regionChanged], dot=1)
        self.department.addReceiver(self.sup.receiver)
        
        self.sub = RegionRadioCombo(self.hierachy,  topKwargs=dict(text= 'Subscript', value= 'sub', variable= self.hierachyVar), orient='h', relx=.02, rely=.75, relh=.25, relw=.96, longent=.3, regionLevel=4, recievers=[self.regionChanged], dot=1)
        self.sup.addReceiver(self.sub.receiver)
        
        # workers in the region or the individual 
        persons = PRMP_Button(self.container, config=dict(text='Persons', command=self.showPersons))
        persons.place(x=2, y=155, h=24, w=80)
        
        switch = PRMP_Button(self.container, config=dict(text='Switch?', command=self.switch))
        switch.place(x=100, y=155, h=24, w=90)
        
        new = PRMP_Checkbutton(self.container, config=dict(text='New Dialog ?'))
        new.place(x=208, y=155, h=24, w=120)
       
        
        self.image = ImageLabel(self.container, status='Profile Picture')
        self.image.place(relx=.61, y=10, h=170, relw=.382)
        
        
    
       # accounts
        self.accounts = PRMP_LabelFrame(self.container, config=dict(text='Accounts'))
        self.accountsHie = Hierachy(self.accounts, status='Accounts Details')
        self.accounts.sub = self.placeAccounts
        
       # subregions
        self.subRegions = PRMP_LabelFrame(self.container, config=dict(text='Sub Regions'))
        self.subRegionsHie = Hierachy(self.subRegions, status='Sub Regions Details')
        self.subRegions.sub = self.placeSubRegions
        
        
        self.addResultsWidgets(['office', 'department', 'sup', 'image', 'sub'])
        
        self.setRadioGroups([self.office, self.department, self.sub, self.sup])
        
    def showPersons(self, e=0):
        if self.personDialog: self.personDialog.destroy()
        if self.region:
            if self.region.level == 5:
                self.personDialog = PersonDialog(self,  values=self.region.person.values, side=self.side)
            else: print('Level not upto')
    
    def loadAccounts(self, region):
        if region:
            acc = region.accountsManager
            headers = [{'text': 'Name', 'width': 120}, 'Date', *[{'type': int, 'text': a} for a in acc.headers]]
            self.accountsHie.setColumns(headers)
            self.accountsHie.set(acc)
    
    def switch(self):
        # to switch between subregions and accounts
        val = self.hierachyVar.get()
        if val == '0':
            PRMP_MsgBox(self, title='Choose First!', message='Choose a region first.', side=self.side, ask=0)
            return
        if self.switchState == None:
            if val != self.sub.val:
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
        self.accounts.place_forget()
        self.changeGeometry(self.geo_)
    
    def isMaximized(self):
        self.update()
        if self._sub: self._sub.sub()
    
    isNormal = isMaximized
        
    def expand(self):
        self.resize = (1, 1)
        self.changeGeometry(self.expandGeo)
        self.update()
    
    def placeSubs(self, sub=None):
        if sub: self._sub = sub
        if self._sub:
            self._sub.place_forget()
            w, h = self._sub.master.tupled_winfo_geometry[:2]
            h -= 189
            self._sub.place(x=2, y=183, h=h, w=w-8)
        
    def showSubRegionsContainer(self):
        self.expand()
        self.placeSubRegions()
        
    def showAccountsContainer(self):
        self.subRegions.place_forget()
        self.expand()
        self.placeAccounts()
        
    def placeAccounts(self):
        self.placeSubs(self.accounts)
        self.accounts.update()
        hx, hy = self.accounts.tupled_winfo_geometry[:2]
        self.accountsHie.place(x=2, y=0, w=hx-8, h=hy-24)
        
    def placeSubRegions(self):
        self.placeSubs(self.subRegions)
        self.subRegions.update()
        
        hx, hy = self.subRegions.tupled_winfo_geometry[:2]
        self.subRegionsHie.place(x=2, y=0, w=hx-8, h=hy-24)
    
RD = RegionDetails

