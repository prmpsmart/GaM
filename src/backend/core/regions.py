from .accounts import AccountsManager, DateTime, Mixins, Errors, RA_Mixins, RAM_Mixins, CompareByDate
from .records import Salary, SalariesManager
import os
from hashlib import sha224

class Person(RA_Mixins, Mixins):
    Manager = 'PersonsManager'
    
    __male = 'male', 'm'
    __female = 'female', 'f'
    
    def __init__(self, manager=None, gender='n', phone='', image=None, email='', address='', date=None, name='', **kwargs):
        
        if isinstance(manager, Region): date = manager.date
        
        RA_Mixins.__init__(self, manager, date=date, name=name)

        gender = gender.lower()
        
        if gender in self.__male:  self.__gender = self.__male[0].title()
        elif gender in self.__female:  self.__gender = self.__female[0].title()
        
        else: self.__gender = 'Neutral'
        
        self.__phone = phone
        
        if image:
            from ...gui.core.prmp_tk.pics import ImageFile
            assert os.path.isfile(image) and os.path.splitext(image)[1] in ['.png', 'jpeg', '.jpg', '.gif', '.xbm'], f'{image} file given is not a valid picture file.'
            self.__image = ImageFile(image)
            
        else: self.__image = None
        
        self.__email = email
        self.__address = address
    
    def __str__(self): return f'{self.manager} | {self.className}({self.name})'
    
    @property
    def values(self): return {'name': self.name, 'gender': self.gender, 'address': self.address, 'image': self.image, 'email': self.email, 'manager': self.manager, 'phone': self.phone}
    
    
    @property
    def gender(self): return self.__gender
    @property
    def address(self): return self.__address
    @address.setter
    def address(self, addr):
        assert addr, 'Address must be str and not empty.'
        self.__address = addr
    @property
    def image(self): return self.__image
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


class Region(RA_Mixins, CompareByDate):
    AccountsManager = AccountsManager
    Manager = 'RegionsManager'
    SubRegionsManager = None
    PersonsManager = None
    Person = None
    
    
    def __init__(self, manager, name=None, date=None, nameFromNumber=False, location=None, phone=None, sup=None, previous=None, number=None, **kwargs):
        
        RA_Mixins.__init__(self, manager, number=number, previous=previous, date=date, name=name, nameFromNumber=nameFromNumber)
        
        self.__sup = sup
        self.__person = None
        self.__personsManager = None
        self.__subRegionsManager = None
        
        self.__location = location
        
        self.__uniqueID = sha224(self.id.encode()).hexdigest()
        
        self.__accountsManager = self.AccountsManager(self, **kwargs)
        
        
        if self.SubRegionsManager:
            self.__subRegionsManager = self.SubRegionsManager(self)
            
            if self.PersonsManager: self.__personsManager = self.PersonsManager(self)
            
        else:
            if self.Person: self.__person = self.Person(manager=self, name=name, date=date, phone=phone, **kwargs)
    
    def __getitem__(self, num): return self.accountsManager[num]
    
    def __len__(self): return len(self.accountsManager)
    
    def __str__(self): return f'{self.manager.master} | {self.className}({self.name})'
    
    @property
    def sup(self): return self.__sup
    
    @property
    def sups(self):
        ss = []
        sup = self.sup
        try:
            while True:
                ss.append(sup)
                sup = sup.sup
        except:
            xx = ss[:-1]
            zz = list(reversed(xx))
            return zz
    
    @property
    def nextRegion(self): return self.next
    @property
    def previousRegion(self): return self.previous
    
    @property
    def level(self): return len(self.hierachy)
    
    @property
    def id(self): return ''.join(self.spacedID.split(' | ')).replace('AGAM', 'A')
    
    @property
    def spacedID(self):
        'override in subclass'
        return 'id | region'
    
    @property
    def uniqueID(self): return self.__uniqueID
    
    @property
    def link(self): return self.__link
    
    @property
    def hierachy(self): return self.sups + [self]
    
    @property
    def hie(self): return self.hierachy
    
    @property
    def hierachyNames(self): return [d.name for d in self.hierachy]
    
    @property
    def reignMonths(self): return self.date - DateTime.now() + 1
    @property
    def reignMonthsYears(self): return divmod(self.reignMonths, 12)
    @property
    def gender(self):
        if self.person: return self.person.gender
    
    @property
    def phone(self):
        if self.person: return self.person.phone
    
    @property
    def email(self):
        if self.person: return self.person.email
    
    @property
    def address(self):
        if self.person: return self.person.address
    
    @property
    def image(self):
        if self.person: return self.person.image
    
    def getRegion(self, **kwargs): return self.getSubReg(**kwargs)
    
    @property
    def region(self):
        manager = self.manager
        if isinstance(manager, str): return manager
        return manager.region
    
    @property
    def person(self):
        if self.personsManager: return self.personsManager.lastPerson
        return self.__person
        
    @property
    def personsManager(self): return self.__personsManager
    @property
    def location(self): return self.__location
    @property
    def subRegionsManager(self): return self.__subRegionsManager
    @property
    def subRegions(self): return self.subRegionsManager[:] if self.subRegionsManager else []
    @property
    def subRegionsCount(self): return len(self.subRegions)
        
    @property
    def lastAccount(self): return self.accountsManager.lastAccount
    
    @property
    def accountsManager(self): return self.__accountsManager
    
    def balanceAccounts(self, month=None):
        if month: self.accountsManager.balanceAccount(month)
        else: self.accountsManager.balanceAccounts()
    
    def subRegionsActiveByMonth(self, month):
        subRegions = []
        for subRegion in self:
        # for subRegion in self.subRegionsManager:
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

class RegionsManager(RAM_Mixins, Mixins):
    subClass = Region
    
    def __init__(self, master):
        RAM_Mixins.__init__(self, master)
        self.__master = master
        self.addRegion = self.addSub
        
    
    
    def __getitem__(self, num): return self.regions[num]
    def __len__(self): return len(self.regions)
    def __repr__(self): return f'<{self}>'
    def __str__(self): return f'{self.master} | {self.className}({self.master.name})'
    
    @property
    def firstRegion(self): return self.first
    @property
    def lastRegion(self): return self.last
    
    @property
    def region(self): return self.master
    
    @property
    def date(self): return self.master.date
    
    @property
    def regions(self): return self.subs
    
    def getRegion(self, number=None, name=None, phone=None, email=None, image=None):
        ## provide mechanism to scan pictures.
        self.getSub(dict(number=number, name=name, phone=phone, email=email, image=image))
        # for region in self.regions:
        #     if number == region.number: return region
        #     elif name == region.name: return region
        #     elif phone == region.phone: return region
        #     elif email == region.email: return region
            
    @classmethod
    def getFromAllRegions(cls, number):
        for region in cls.allRegions():
            if region.number == number: return region
    
    def regionExists(self, **kwargs):
        if self.getRegion(**kwargs): return True
        return False
    
    def createRegion(self, **kwargs): return self.createSub(sup=self.master, **kwargs)
    

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




class PersonsManager(RegionsManager):
    subClass = Person
    @property
    def lastPerson(self): return self.lastRegion
    def createPerson(self, **kwargs): return self.createRegion(**kwargs)

class Staff(Region):
    AccountsManager = SalariesManager
    Manager = 'StaffsManager'
    Person = None
    def salariesManager(self): return self.accountsManager
    def paySalary(self, salary, date=None): self.salariesManager.addSalary(salary, date=date)


class ThirdPartySurety:
    
    def __init__(self, loanBondDetails='', name='', dob='', maritalStatus='', phone='', address='', officeAddress='', religion='', homeTown='', stateOfOrigin='', occupation='', knowledgeOfMember='', relationshipWithMember='', image='', date=None):
    
        self.__loanBondDetails = loanBondDetails
        self.__name = None
        
        self.__dob = dob
        self.__maritalStatus = maritalStatus
        self.__phone = phone
        self.__address = address
        self.__officeAddress = officeAddress
        self.__religion = religion
        self.__homeTown = homeTown
        self.__stateOfOrigin = stateOfOrigin
        self.__occupation = occupation
        self.__knowledgeOfMember = knowledgeOfMember
        self.__relationshipWithMember = relationshipWithMember
        self.__image = image
        
    @property
    def dob(self): return self.__dob
    @property
    def maritalStatus(self): return self.__maritalStatus
    @property
    def image(self): return self.__image
    @property
    def phone(self): return self.__phone
    @property
    def address(self): return self.__address
    @property
    def officeAddress(self): return self.__officeAddress
    @property
    def religion(self): return self.__religion
    @property
    def homeTown(self): return self.__homeTown
    @property
    def stateOfOrigin(self): return self.__stateOfOrigin
    @property
    def occupation(self): return self.__occupation
    @property
    def knowledgeOfMember(self): return self.__knowledgeOfMember
    @property
    def relationshipWithMember(self): return self.__relationshipWithMember


class LoanBondDetails:
    thirdPartySurety = ThirdPartySurety

    def __init__(self, loanBond):
    
        self.__loanBond = loanBond
        self.__proposedLoan = loanBond.proposedLoan
        self.__thirdPartySurety = None
        self.__image = None
        
        self.__interest = None
    
    @property
    def image(self): return self.__image
    @property
    def interest(self): return self.__interest
    @property
    def loanBond(self): return self.__loanBond
    def proposedLoan(self): return self.__proposedLoan
    
    def setThirdPartySurety(self, **kwargs): 
        self.__thirdPartySurety = self.thirdPartySurety(self, **kwargs)

