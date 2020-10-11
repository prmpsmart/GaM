from .accounts import AccountsManager, DateTime, Mixins, Errors
from .records import Salary, SalariesManager

class Region(Mixins):
    AccountsManager = AccountsManager
    Manager = 'RegionsManager'
    SubRegionsManager = None
    PersonsManager = None
    Person = None
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
        
        self.__accountsManager = self.AccountsManager(self, **kwargs)
        
        
        if self.SubRegionsManager or self.MultiSubRegionsManager:
            if self.MultiSubRegionsManager: self.__subRegionsManager = None
            else: self.__subRegionsManager = self.SubRegionsManager(self)
            self.__person = None
            self.__personsManager = self.PersonsManager(self)
        else:
            self.__subRegionsManager = None
            self.__person = self.Person(manager=self, name=name, date=date, phone=phone, **kwargs)
            self.__personsManager = None
    
    def __getitem__(self, num): return self.accountsManager[num]
    def __len__(self): return len(self.accountsManager)
    # def __repr__(self): return f"<{self}>"
    def __str__(self): return f'{self.manager.master} | {self.className}({self.name})'
    
    @property
    def reignMonths(self): return self.date - DateTime.now() + 1
    @property
    def reignMonthsYears(self): return divmod(self.reignMonths, 12)
    @property
    def gender(self):
        if self.person: return self.person.gender
        else: return str(self)
    @property
    def phone(self):
        if self.person: return self.person.phone
        else: return str(self)
    @property
    def email(self):
        if self.person: return self.person.email
        else: return str(self)
    @property
    def address(self):
        if self.person: return self.person.address
        else: return str(self)
    @property
    def photo(self):
        if self.person: return self.person.photo
        else: return str(self)
    
    def getRegion(self, **kwargs): return self.subRegionsManager.getRegion(**kwargs)
    @property
    def region(self): return self.manager.region
    @property
    def person(self): return self.__person
    @property
    def personsManager(self): return self.__personsManager
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
        for region in self.regions:
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

class Person(Mixins):
    Manager = 'PersonsManager'
    
    __male = 'male', 'm'
    __female = 'female', 'f'
    
    def __init__(self, manager=None, gender='n', phone='', photo='', email='', address='', date=None, name=None, **kwargs):
        
        if isinstance(manager, str): pass
        elif isinstance(manager, Region): self.__date = manager.date
        else: assert manager.className == self.Manager, f'Manager should be {self.Manager} not {manager.className}'
        gender = gender.lower()
        
        if gender in self.__male:  self.__gender = self.__male[0].title()
        elif gender in self.__female:  self.__gender = self.__female[0].title()
        
        else: self.__gender = 'Neutral'
        
        self.__name = name
        self.__phone = phone
        self.__photo = photo
        self.__email = email
        self.__address = address
        self.__manager = manager
    
    def __str__(self): return f'{self.manager} | {self.className}({self.name}) '
    
    @property
    def name(self): 
        if not self.__name: return self.manager.name
        return self.__name
    @property
    def manager(self): return self.__manager
    @property
    def gender(self): return self.__gender
    @property
    def address(self): return self.__address
    @address.setter
    def address(self, addr):
        assert addr, 'Address must be str and not empty.'
        self.__address = addr
    @property
    def image(self):
        pass
    @property
    def email(self): return self.__email
    @email.setter
    def email(self, em): 
        # confirm if email is valid
        self.__email = em
    @property
    def phone(self): return self.__phone
    @phone.setter
    def phone(self, number):
        assert number, 'Number must be valid.'
        # confirm if number is valid
        self.__phone = number
    
    def show(self):
        pass

class PersonsManager(RegionsManager):
    regionClass = Person
    
    def createPerson(self, **kwargs): return self.createRegion(**kwargs)

class Staff(Region):
    AccountsManager = SalariesManager
    Manager = 'StaffsManager'
    Person = None
    def salariesManager(self): return self.accountsManager
    def paySalary(self, salary, date=None): self.salariesManager.addSalary(salary, date=date)
    





