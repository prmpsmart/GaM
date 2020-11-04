from .accounts import AccountsManager, DateTime, Mixins, Errors, Object, ObjectsManager, CompareByDate
from .records_managers import *
import os


class Person(Object):
    Manager = 'PersonsManager'
    
    __male = 'male', 'm'
    __female = 'female', 'f'
    
    def __init__(self, manager=None, gender='n', phone='', image=None, email='', address='', date=None, name='', **kwargs):
        
        if isinstance(manager, Region): date = manager.date
        
        Object.__init__(self, manager, date=date, name=name)

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
        self.__email = None
        if self.checkEmail(email): self.__email = email
        
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

class Region(Object):
    AccountsManager = AccountsManager
    Manager = 'RegionsManager'
    SubRegionsManager = None
    PersonsManager = None
    Person = None
    
    
    def __init__(self, manager, name=None, date=None, location=None, phone=None, previous=None, number=None, **kwargs):
        
        Object.__init__(self, manager, previous=previous, date=date, name=name, number=number, **kwargs)
        
        
        self.__person = None
        self.__personsManager = None
        self.__subRegionsManager = None
        
        self.__location = location
        
        
        self.__accountsManager = self.AccountsManager(self, **kwargs)
        
        if self.SubRegionsManager:
            self.__subRegionsManager = self.SubRegionsManager(self)
            
            if self.PersonsManager: self.__personsManager = self.PersonsManager(self)

        else:
            if self.Person: self.__person = self.Person(manager=self, name=name, date=date, phone=phone, **kwargs)
    
    # def __getitem__(self, num):
    #     print(num)
    #     if isinstance(num, int):
    #         acc = self.accountsManager
    #         if num <= len(acc): return acc[num]
    
    def __len__(self): return len(self.accountsManager)
    
    def __str__(self): return f'{self.manager.master} | {self.className}({self.name})'
    
    @property
    def subs(self): return self.subRegionsManager[:] if self.subRegionsManager else []
    
    @property
    def totalSubs(self): return len(self.subs)
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
        return self.__person
        
    @property
    def personsManager(self): return self.__personsManager
    @property
    def location(self): return self.__location
    @property
    def subRegionsManager(self): return self.__subRegionsManager
    @property
    def subRegions(self): return self.subs
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

class Staff(Region):
    AccountsManager = SalariesManager
    Manager = 'StaffsManager'
    Person = None
    def salariesManager(self): return self.accountsManager
    def paySalary(self, salary, date=None): self.salariesManager.addSalary(salary, date=date)


class ThirdPartySurety(Mixins):
    
    def __init__(self, loanBondDetails='', name='', dob='', maritalStatus='', phone='', address='', officeAddress='', religion='', homeTown='', stateOfOrigin='', occupation='', knowledgeOfMember='', email='', relationshipWithMember='', image='', date=None):
    
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
        
        self.__email = None
        if self.checkEmail(email): self.__email = email
        
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


