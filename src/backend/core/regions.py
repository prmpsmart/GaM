from .accounts import AccountsManager, DateTime, Mixins, Errors

class Region(Mixins):
    AccountManager = AccountsManager
    Manager = 'RegionsManager'
    SubRegionsManager = None
    DetailsManager = None
    Detail = None
    MultiSubRegionsManager = False
    
    def __init__(self, manager=None, number=None, name=None, date=None, nameFromNumber=False, location=None, phone=None, **kwargs):
        if not isinstance(manager, str): assert manager.className == self.Manager, f'Manager should be {self.Manager} not {manager.className}.'
        
        if date == None: date = DateTime.now()
        DateTime.checkDateTime(date)
        
        self.__manager = manager
        self.__number = number
        self.__name = name if not nameFromNumber else f'{self.className} {number}'
        self.__location = location
        self.__date = date
        
        self.__accountsManager = self.AccountManager(self, **kwargs)
        
        
        if self.SubRegionsManager or self.MultiSubRegionsManager:
            if self.MultiSubRegionsManager: self.__subRegionsManager = None
            else: self.__subRegionsManager = self.SubRegionsManager(self)
            self.__detail = None
            self.__detailsManager = self.DetailsManager(self)
        else:
            self.__subRegionsManager = None
            self.__detail = self.Detail(manager=self, name=name, date=date, phone=phone, **kwargs)
            self.__detailsManager = None
    
    def __getitem__(self, num): return self.accountsManager[num]
    def __len__(self): return len(self.accountsManager)
    def __repr__(self): return f"<{self}>"
    def __str__(self): return f'{self.manager.master} | {self.className}({self.name})'
    
    @property
    def reignMonths(self): return self.date - DateTime.now() + 1
    @property
    def reignMonthsYears(self): return divmod(self.reignMonths, 12)
    @property
    def gender(self):
        if self.detail: return self.detail.gender
        else: return str(self)
    @property
    def phone(self):
        if self.detail: return self.detail.phone
        else: return str(self)
    @property
    def email(self):
        if self.detail: return self.detail.email
        else: return str(self)
    @property
    def address(self):
        if self.detail: return self.detail.address
        else: return str(self)
    @property
    def photo(self):
        if self.detail: return self.detail.photo
        else: return str(self)
    
    def getRegion(self, **kwargs): return self.subRegionsManager.getRegion(**kwargs)
    @property
    def region(self): return self.manager.region
    @property
    def detail(self): return self.__detail
    @property
    def detailsManager(self): return self.__detailsManager
    @property
    def location(self): return self.__location
    @property
    def name(self): return self.__name
    @property
    def number(self): return self.__number
    @property
    def subRegionsManager(self): return self.__subRegionsManager
    @property
    def manager(self): return self.__manager
    @property
    def date(self): return self.__date
    @property
    def lastAccount(self): return self.accountsManager.lastAccount
    @property
    def accountsManager(self): return self.__accountsManager
    def balanceAccounts(self, month=None):
        if month: self.accountsManager.balanceAccount(month)
        else: self.accountsManager.balanceAccounts()
    
    def subRegionsActiveByMonth(self, month):
        subRegions = []
        for subRegion in self.subRegionsManager:
            monthAccount = subRegion.accountsManager.getAccount(month)
            if monthAccount != None: subRegions.append(subRegion)
        return subRegions
    def sortAccountsByMonth(self, month): return self.accountsManager.sortAccountsByMonth(month)


 ########## Sorting
  # SubRegions
   #Date Sorting
    def sortSubRegionsByDate(self, date): return self.subRegionsManager.sortRegionsByDate(date)
   #Day Sorting
    def sortSubRegionsByDay(self): return self.subRegionsManager.sortRegionsByDay(date)
    def sortSubRegionsIntoDaysInWeek(self): return self.subRegionsManager.sortRegionsIntoDaysInWeek(date)
    def sortSubRegionsIntoDaysInMonth(self): return self.subRegionsManager.sortRegionsIntoDaysInMonth(date)
    
   #Week Sorting
    def sortSubRegionsByWeek(self): return self.subRegionsManager.sortRegionsByDate(date)
    def sortSubRegionsIntoWeeksInMonth(self): return self.subRegionsManager.sortRegionsIntoWeeksInMonth(date)
    def sortSubRegionsIntoWeeksInYear(self): return self.subRegionsManager.sortRegionsIntoWeeksInYear(date)
    
   #Month Sorting
    def sortSubRegionsByMonth(self, month): return self.subRegionsManager.sortRegionsByMonth(date)
    def sortSubRegionsIntoMonthsInYear(self): return self.subRegionsManager.sortRegionsIntoMonthsInYear(date)
    def sortSubRegionsIntoMonthsInYears(self): return self.subRegionsManager.sortRegionsIntoMonthsInYears(date)
    
   #Year Sorting
    def sortSubRegionsByYear(self): return self.subRegionsManager.sortRegionsByYear(date)
    def sortSubRegionsIntoYears(self): return self.subRegionsManager.sortRegionsIntoYears(date)

  # SubRegions Accounts
   #Date Sorting
    def sortSubRegionsAccountsByDate(self): return self.subRegionsManager.sortRegionsAccountsByDate(date)

   #Day Sorting
    def sortSubRegionsAccountsByDay(self): return self.subRegionsManager.sortRegionsAccountsByDay(date)
    def sortSubRegionsAccountsIntoDaysInWeek(self): return self.subRegionsManager.sortRegionsAccountsIntoDaysInWeek(date)
    def sortSubRegionsAccountsIntoDaysInMonth(self): return self.subRegionsManager.sortRegionsAccountsIntoDaysInMonth(date)
    
   #Week Sorting
    def sortSubRegionsAccountsByWeek(self): return self.subRegionsManager.sortRegionsAccountsByWeek(date)
    def sortSubRegionsAccountsIntoWeeksInMonth(self): return self.subRegionsManager.sortRegionsAccountsIntoWeeksInMonth(date)
    def sortSubRegionsAccountsIntoWeeksInYear(self): return self.subRegionsManager.sortRegionsAccountsIntoWeeksInYear(date)
    
   #Month Sorting
    def sortSubRegionsAccountsByMonth(self, month): return self.subRegionsManager.sortRegionsAccountsIntoMonthsInYear(date)
        
    def sortSubRegionsAccountsIntoMonthsInYear(self): return self.subRegionsManager.sortRegionsAccountsIntoMonthsInYear(date)
    def sortSubRegionsAccountsIntoMonthsInYears(self): return self.subRegionsManager.sortRegionsAccountsIntoMonthsInYears(date)
    
   #Year Sorting
    def sortSubRegionsAccountsByYear(self): return self.subRegionsManager.sortRegionsAccountsByYear(date)
    def sortSubRegionsAccountsIntoYears(self): return self.subRegionsManager.sortRegionsAccountsIntoYears(date)

class RegionsManager(Mixins):
    regionClass = Region
    
    def __init__(self, master=None):
        assert master != None
        self.__master = master
        self.__regions = []
    
    def __getitem__(self, num): return self.regions[num]
    def __len__(self): return len(self.regions)
    def __repr__(self): return f'<{self}>'
    def __str__(self): return f'{self.master} | {self.className}({self.master.name})'
    
    @property
    def master(self): return self.__master
    @property
    def region(self): return self.master
    @property
    def date(self): return self.__master.date
    @property
    def regions(self): return self.__regions
    def addRegion(self, region): self.__regions.append(region)
    def getRegion(self, number=None, name=None, phone=None, email=None, photo=None):
        ## provide mechanism to scan pictures.
        for region in self.regions():
            if number == region.number: return region
            elif name == region.name: return region
            elif phone == region.phone: return region
            elif email == region.email: return region
            
    @classmethod
    def getFromAllRegions(cls, number):
        for region in cls.allRegions():
            if region.number == number: return region
    
    def createRegion(self, date=None, auto=None, **kwargs):
        if (DateTime.checkDateTime(date, dontRaise=True) == False) and (auto == True): date = DateTime.createDateTime(auto=auto)
        region = self.regionClass(manager=self, date=date, number=len(self)+1, **kwargs)
        
        self.addRegion(region)
        return region
    
    def regionExists(self, **kwargs):
        if self.getRegion(**kwargs): return True
        return False

 ########## Sorting
  # SubRegions
   #Date Sorting
    def sortRegionsByDate(self, date):
        DateTime.checkDateTime(date)
        clientsByDate = [client for client in self.clients if client.regDate == date]
        return clientsByDate
   #Day Sorting
    def sortRegionsByDay(self):
        pass
    def sortRegionsIntoDaysInWeek(self):
        pass
    def sortRegionsIntoDaysInMonth(self):
        pass
    
   #Week Sorting
    def sortRegionsByWeek(self):
        pass
    def sortRegionsIntoWeeksInMonth(self):
        pass
    def sortRegionsIntoWeeksInYear(self):
        pass
    
   #Month Sorting
    def sortRegionsByMonth(self, month):
        pass
    def sortRegionsIntoMonthsInYear(self):
        pass
    def sortRegionsIntoMonthsInYears(self):
        pass
    
   #Year Sorting
    def sortRegionsByYear(self):
        pass
    def sortRegionsIntoYears(self):
        pass

  # Regions Accounts
   #Date Sorting
    def sortRegionsAccountsByDate(self):
        pass

   #Day Sorting
    def sortRegionsAccountsByDay(self):
        pass
    def sortRegionsAccountsIntoDaysInWeek(self):
        pass
    def sortRegionsAccountsIntoDaysInMonth(self):
        pass
    
   #Week Sorting
    def sortRegionsAccountsByWeek(self):
        pass
    def sortRegionsAccountsIntoWeeksInMonth(self):
        pass
    def sortRegionsAccountsIntoWeeksInYear(self):
        pass
    
   #Month Sorting
    def sortRegionsAccountsByMonth(self, month):
        DateTime.checkDateTime(month)
        clients = [client for client in self.clients if client.lastAccount.date.isSameMonth(month)]
        accounts = []
        for client in clients:
            clientAccounts = client.accountsManager.sortAccountsByMonth(month)
            accounts.extend(clientAccounts)
        return accounts
        
    def sortRegionsAccountsIntoMonthsInYear(self):
        pass
    def sortRegionsAccountsIntoMonthsInYears(self):
        pass
    
   #Year Sorting
    def sortRegionsAccountsByYear(self):
        pass
    def sortRegionsAccountsIntoYears(self):
        pass



