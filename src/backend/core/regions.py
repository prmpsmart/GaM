from .accounts import AccountsManager, DateTime, ObjectsMixins, Errors, Object, ObjectsManager, CompareByDate
from .records_managers import *
import os

'''
DC Objects = Region, Person, Account, Records, Client, Area
and Managers


'''


class Person(Object):
    Manager = 'PersonsManager'
    
    _male = 'male', 'm'
    _female = 'female', 'f'
    
    def __init__(self, manager=None, gender='n', phone='', image=None, email='', address='', date=None, name='', **kwargs):
        
        if isinstance(manager, Region): date = manager.date
        
        Object.__init__(self, manager, date=date, name=name)

        gender = gender.lower()
        
        if gender in self._male:  self.gender = self._male[0].title()
        elif gender in self._female:  self.gender = self._female[0].title()
        
        else: self.gender = 'Neutral'
        
        self.phone = phone
        
        self.image = image

        self.email = None
        if self.checkEmail(email): self.email = email
        
        self.address = address
    
    def __str__(self): return f'{self.manager} | {self.className}({self.name})'
    
    @property
    def values(self): return {'name': self.name, 'gender': self.gender, 'address': self.address, 'image': self.image, 'email': self.email, 'manager': self.manager, 'phone': self.phone}

class Region(Object):
    AccountsManager = AccountsManager
    Manager = 'RegionsManager'
    SubRegionsManager = None
    PersonsManager = None
    Person = None
    _type = 'reg'
    
    subTypes = ['Regions', 'Accounts', 'Records Managers', 'Persons']

    
    def __init__(self, manager, name=None, date=None, location=None, phone=None, previous=None, number=None, **kwargs):
        
        Object.__init__(self, manager, previous=previous, date=date, name=name, number=number, **kwargs)
        
        
        self._person = None
        self._personsManager = None
        self._subRegionsManager = None
        
        self._location = location
        
        
        self._accountsManager = self.AccountsManager(self, **kwargs)
        
        if self.SubRegionsManager:
            self._subRegionsManager = self.SubRegionsManager(self)
            
            if self.PersonsManager: self._personsManager = self.PersonsManager(self)

        else:
            if self.Person: self._person = self.Person(manager=self, name=name, date=date, phone=phone, **kwargs)
    
    def __getattr__(self, name):
        ret = self.getFromSelf(name, self._unget)
        if str(ret) != self._unget: return ret

        aret = getattr(self.accountsManager, name, self._unget)
        if str(aret) != self._unget: return aret

        sret = getattr(self.accountsManager, name, self._unget)
        if str(sret) != self._unget: return sret

        self.attrError(name)
    
    def __len__(self): return len(self.accountsManager)
    
    def __str__(self): return f'{self.manager.master} | {self.className}({self.name})'
    
    @property
    def subs(self): return self.subRegionsManager[:] if self.subRegionsManager else []
    
    @property
    def totalSubs(self): return len(self.subs)

    @property
    def spacedID(self):
        sup = self.manager if self.strManager else self.sup.spacedID
        return f'{str(sup).replace(" ", "")}'
        
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
    def idText(self):
        text = ''
        hie = self.hierachy
        
        for reg in hie[1:]:
            if len(hie) > 2 and reg is hie[2]: name = reg.DEPARTMENT
            else: name = reg.name
            text += name + ' | '

        te = text.split('|')[:-1]
        text = ' | '.join(te)
        return text
    
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
    def gender(self): return self.person.gender if self.person else ''
    
    @property
    def phone(self): return self.person.phone if self.person else ''
    
    @property
    def email(self): return self.person.email if self.person else ''
    
    @property
    def address(self): return self.person.address if self.person else ''
    
    @property
    def image(self): return self.person.image if self.person else ''
    
    def getRegion(self, **kwargs): return self.getSubReg(**kwargs)
    
    @property
    def region(self):
        manager = self.manager
        if isinstance(manager, str): return manager
        return manager.region
    
    @property
    def person(self):
        if self.personsManager: return self.personsManager.lastPerson
        return self._person
        
    @property
    def personsManager(self): return self._personsManager
    
    @property
    def persons(self): return self.personsManager or [self.person]

    @property
    def location(self): return self._location

    @property
    def subRegionsManager(self): return self._subRegionsManager
    
    @property
    def subs(self): return self.accountsManager if self.accountsManager else []
    
    @property
    def subRegions(self): return self.subRegionsManager

    @property
    def regions(self): return self.subRegions
    
    @property
    def regions(self): return self.subRegions
    
    @property
    def subRegionsCount(self): return len(self.subRegions)
        
    @property
    def lastAccount(self): return self.accountsManager.lastAccount
    
    @property
    def accountsManager(self): return self._accountsManager
    
    @property
    def accounts(self): return self.accountsManager
    
    @property
    def recordsManagers(self): return self.accountsManager.recordsManagers
    
    
    def balanceAccounts(self, month=None):
        if month: self.accountsManager.balanceAccount(month)
        else: self.accountsManager.balanceAccounts()
    
    
    def sortAccountsByMonth(self, month): return self.accountsManager.sortSubsByMonth(month)


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

class Staff(Region):
    AccountsManager = SalariesManager
    Manager = 'StaffsManager'
    Person = None
    def salariesManager(self): return self.accountsManager
    def paySalary(self, salary, date=None): self.salariesManager.addSalary(salary, date=date)

class ThirdPartySurety(ObjectsMixins):
    
    def __init__(self, loanBondDetails=None, name='', dob='', maritalStatus='', phone='', address='', officeAddress='', religion='', homeTown='', stateOfOrigin='', occupation='', knowledgeOfMember='', email='', relationshipWithMember='', image='', date=None):
        super().__init__()
        self.loanBondDetails = loanBondDetails
        self.name = None
        
        self.dob = dob
        self.maritalStatus = maritalStatus
        self.phone = phone
        self.address = address
        self.officeAddress = officeAddress
        self.religion = religion
        self.homeTown = homeTown
        self.stateOfOrigin = stateOfOrigin
        self.occupation = occupation
        self.knowledgeOfMember = knowledgeOfMember
        self.relationshipWithMember = relationshipWithMember
        self.image = image
        
        self.email = None
        if self.checkEmail(email): self.email = email

class LoanBondDetails:
    _thirdPartySurety = ThirdPartySurety

    def __init__(self, loanBond):
    
        self.loanBond = loanBond
        self.proposedLoan = loanBond.proposedLoan
        self.thirdPartySurety = None
        self.image = None
        
        self.interest = None
    
    @property
    def image(self): return self.__image
    @property
    def interest(self): return self.__interest
    @property
    def loanBond(self): return self.__loanBond
    def proposedLoan(self): return self.__proposedLoan
    
    def setThirdPartySurety(self, **kwargs): 
        self.thirdPartySurety = self._thirdPartySurety(self, **kwargs)


