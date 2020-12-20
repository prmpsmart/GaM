from .agam_extensions import *


class RegionLookUp(PRMP_MainWindow, FillWidgets):
    
    def __init__(self, master=None, title='Region Details', geo=(650, 270), expandGeo=(800, 600), values={}, region=None, tm=1, gaw=1, **kwargs):
        
        PRMP_MainWindow.__init__(self, master, title=title, geo=geo, gaw=gaw, ntb=1, tm=tm, atb=1, asb=1, **kwargs)
        
        FillWidgets.__init__(self, values=values)
        
        self.region = region
        self.personDialog = None
        self.switchState = None
        self._sub = None
        self.geo_ = geo
        self.expandGeo = expandGeo
        
        self._setupApp()

        self.set()
        self.paint()
        
        if self.region:
            for wid in [self.office, self.department, self.sub, self.sup]:
                if self.region.level == wid.regionLevel: wid.set(self.region)
        
    def regionChanged(self, region):
        region = region[1]
        if not region or (region is self.region): return
    
        self.region = region
        self.addTitleBar(region.idText)
        
        person = region.person
        if person: self.set(dict(image=person.image))

        # self.loadAccounts(region)
    
    def _setupApp(self):
        # hierachy

        self.hierachy = PRMP_LabelFrame(self.container, config=dict(text='Hierachy'))
        self.hierachy.place(x=2, y=2, h=170, relw=.6)
        
        self.hierachyVar = tk.StringVar()
        self.hierachyVar.set('sub')
        
        self.office = RegionRadioCombo(self.hierachy,  topKwargs=dict(config=dict(text='Office', style='Group.TRadiobutton', variable=self.hierachyVar, value='off')), bottomKwargs=dict(placeholder='Enter Office Name'), orient='h', place=dict(relx=.02, rely=0, relh=.25, relw=.96), longent=.3, regionLevel=1, recievers=[self.regionChanged], dot=1, tttk=1)
        
        self.department = RegionRadioCombo(self.hierachy,  topKwargs=dict(config=dict(text='Department', style='Group.TRadiobutton', variable=self.hierachyVar, value='dep')), orient='h', place=dict(relx=.02, rely=.25, relh=.25, relw=.96), longent=.35, regionLevel=2, recievers=[self.regionChanged], dot=1, tttk=1)
        self.office.addReceiver(self.department.receiver)
        
        self.sup = RegionRadioCombo(self.hierachy,  topKwargs=dict(config=dict(text='Superscript', style='Group.TRadiobutton', variable=self.hierachyVar, value='sup')), orient='h', place=dict(relx=.02, rely=.5, relh=.25, relw=.96), longent=.35, regionLevel=3, recievers=[self.regionChanged], dot=1, tttk=1)
        self.department.addReceiver(self.sup.receiver)
        
        self.sub = RegionRadioCombo(self.hierachy,  topKwargs=dict(config=dict(text='Subscript', value='sub', style='Group.TRadiobutton', variable= self.hierachyVar)), orient='h', place=dict(relx=.02, rely=.75, relh=.25, relw=.96), longent=.3, regionLevel=4, recievers=[self.regionChanged], dot=1, tttk=1)
        self.sup.addReceiver(self.sub.receiver)
        
        # workers in the region or the individual 
        persons = PRMP_Button(self.container, config=dict(text='Persons', command=self.showPersons))
        persons.place(x=2, y=175, h=24, w=80)
        
        switch = PRMP_Button(self.container, config=dict(text='Switch?', command=self.switch))
        switch.place(x=100, y=175, h=24, w=90)
        
        new = PRMP_Checkbutton(self.container, config=dict(text='New Dialog ?'))
        new.place(x=208, y=175, h=24, w=140)
       
        
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
            self.accountsHie.set(acc, 1)
    
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
            h -= 205
            self._sub.place(x=2, y=203, h=h, w=w-8)
        
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
        self.accountsHie.place(x=2, y=0, w=hx-8, h=hy-30)
        
    def placeSubRegions(self):
        self.placeSubs(self.subRegions)
        self.subRegions.update()
        
        hx, hy = self.subRegions.tupled_winfo_geometry[:2]
        self.subRegionsHie.place(x=2, y=0, w=hx-8, h=hy-24)
RLU = RegionLookUp


class SortNSearch(PRMP_MainWindow):
    def __init__(self, master=None, title='Sort and Search', geo=(700, 850), longent=.27, sup=None):
        super().__init__(master, title=title, geo=geo)

        self._sup = sup

        self.sup = LabelButton(self.container, place=dict(relx=.005, rely=.005, relh=.04, relw=.99), orient='h', longent=.2, topKwargs=dict(text='Sup'), bottomKwargs=dict(text=sup), command=self.openSup)

        
        self.results = PRMP_TreeView(LabelFrame(self.container, text='Results', place=dict(relx=.005, rely=longent+.05, relh=.99-.04-longent, relw=.99)), place=dict(relx=0, rely=0, relh=1 , relw=1))

        self.details = SearchDetails(self.container, place=dict(relx=.005, rely=.05, relh=longent, relw=.99), results=self.results, sup=sup)

        self.paint()
    
    def openSup(self):
        pass


class ObjectDetails(PRMP_MainWindow):
    
    def __init__(self, master=None, geo=(1200, 600), title='DC Object Details', sup=None, **kwargs):
        super().__init__(master, geo=geo, title=title, **kwargs)

        self._sup = sup

        sups = LabelFrame(self.container, place=dict(relx=.005, rely=.02, relh=.965, relw=.3), text='Object Subcripts')
        
        self.sup = LabelButton(sups, place=dict(relx=.005, rely=0, relh=.07, relw=.99), topKwargs=dict(text='Super'), orient='h', longent=.2, command=self.openSup, bottomKwargs=dict(text=sup.name if sup else 'Name'))

        self.subTypes = ['Regions', 'Accounts', 'Records Managers', 'Records', 'Persons']
        self.subType = LabelCombo(sups, place=dict(relx=.005, rely=.08, relh=.07, relw=.7), topKwargs=dict(text='Sub Type'), bottomKwargs=dict(values=self.subTypes), orient='h', longent=.4, func=self.changeSubs)

        self.month = TwoWidgets(sups, topKwargs=dict(text='Month'), place=dict(relx=.005, rely=.16, relh=.07, relw=.5), orient='h', bottom='datebutton', top='checkbutton', bottomKwargs=dict())

        self.subsList = SubsList(sups, place=dict(relx=.038, rely=.24, relh=.73, relw=.9), text='Subs', listboxConfig=dict(selectmode='single'), callback=self.selected)

        self.subs = Hierachy(self.container, place=dict(relx=.307, rely=.039, relh=.97, relw=.68))
        
        self.paint()
    
    @property
    def selectedSubType(self): return self.subType.get()
    
    def changeSubs(self, e=0):
        if self._sup:
            subs = self._sup[self.selectedSubType] or []
            self.subsList.set([sub.name for sub in self._sup])
    
    def openSup(self):
        pass

    def selected(self, obj):
        print(obj)














