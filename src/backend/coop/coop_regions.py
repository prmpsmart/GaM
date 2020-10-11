from ..core.regions import Region, RegionsManager, Person, PersonsManager
from .coop_accounts import CoopErrors, CoopAccount, MemberAccount, UnitAccount
from .coop_errors import CoopErrors

class MemberDetail(Person):
    
    @property
    def member(self): return self.manager

class CoopCO(Person):
    'Cooperative Cash Officer.'

class CoopCOsManager(PersonsManager):
    regionClass = CoopCO
    def createCoopCo(self, **kwargs): return self.createDetail(**kwargs)

class ThirdPartySurety:
    
    def __init__(self, loanBondDetails='', name='', dob='', maritalStatus='', phone='', address='', officeAddress='', religion='', homeTown='', stateOfOrigin='', occupation='', knowledgeOfMember='', relationshipToMember='', photo='', date=None):
    
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
        self.__relationshipToMember = relationshipToMember
        self.__photo = photo
        
    @property
    def dob(self): return self.__dob
    @property
    def maritalStatus(self): return self.__maritalStatus
    @property
    def photo(self): return self.__photo
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
    def relationshipToMember(self): return self.__relationshipToMember

class LoanBondDetails:

    def __init__(self, loanBond):
    
        self.__loanBond = loanBond
        self.__proposedLoan = loanBond.proposedLoan
        self.__firstSurety = None
        self.__secondSurety = None
        self.__thirdSurety = None
        self.__thirdPartySurety = None
        self.__accountName = None
        self.__accountNumber = None
        self.__bank = None
        self.__photo = None
        
        self.__interest = None
        self.__monthlyRepayment = None
    
    @property
    def photo(self): return self.__photo
    @property
    def interest(self): return self.__interest
    @property
    def monthlyRepayment(self): return self.__monthlyRepayment
    @property
    def accountName(self): return self.__accountName
    @property
    def accountNumber(self): return self.__accountNumber
    @property
    def bank(self): return self.__bank
    @property
    def loanBond(self): return self.__loanBond
    @property
    def firstSurety(self): return self.__firstSurety
    @property
    def secondSurety(self): return self.__secondSurety
    @property
    def proposedLoan(self): return self.__proposedLoan
    @property
    def thirdSurety(self): return self.__thirdSurety
    
    def setThirdPartySurety(self, **kwargs): 
        self.__thirdPartySurety = ThirdPartySurety(self, **kwargs)
        
    @property
    def unit(self): return self.member.unit
    
    def setDetails(self, members, accountName, accountNumber, bank, rate=.1, date=None):
        validLoan = (int(self.loanBond.manager.savings) * 2)
        assert validLoan <= self.proposedLoan, f'Loan exceed maximum valid loan of {validLoan}.'
        
        self.setMemberSureties(members)
    
    def setMemberSureties(self, members):
        assert len(members) == 3, 'Three numbers of society members are expected e.g [1,2,3].'
        for num in members:
            if not self.unit.memberExists(number=num): raise CoopErrors.UnitError(f'Member with number "{num}" does not exist.')
        
        self.__firstSurety = self.unit.getMember(number=members[0])
        self.__secondSurety = self.unit.getMember(number=members[1])
        self.__thirdSurety = self.unit.getMember(number=members[2])

class CoopRegion(Region):
    Errors = CoopErrors
    AccountsManager = CoopAccount
    Manager = 'CoopRegionsManager'

class CoopRegionsManager(RegionsManager):
    regionClass = CoopRegion
    # def __str__(self): return f'{self.master} {self.className}'

class Member(CoopRegion, Person):
    AccountsManager = MemberAccount
    Manager = 'MembersManager'
    Person = MemberDetail
    
    def __init__(self, manager, name, gender, phone, photo=None, email=None, date=None, **kwargs):
        assert name != None, 'Name can not be empty.'
        assert gender, 'Gender is not provided.'
        assert gender.lower() in ['f', 'm', 'male', 'female'], "Name can not be empty and must be among ['f', 'm', 'male', 'female']."
        
        super().__init__(manager=manager, name=name, gender=gender, phone=phone, photo=photo, email=email, date=date, **kwargs)
    
    @property
    def unit(self): return self.manager.unit
    @property
    def expenses(self): return self.accountsManager.expenses
    @property
    def levies(self): return self.accountsManager.levies
    @property
    def loanBonds(self): return self.accountsManager.loanBonds
    @property
    def loans(self): return self.accountsManager.loans
    @property
    def materials(self): return self.accountsManager.materials
    @property
    def savings(self): return self.accountsManager.savings
    
    def newLoanBond(self, money, **kwargs): return self.accountsManager.newLoanBond(money, **kwargs)
    
    def balanceAccount(self): return self.accountsManager.balanceAccount()

class MembersManager(CoopRegionsManager):
    regionClass = Member
   
    @property
    def unit(self): return self.master
    
    @property
    def members(self): return self.regions
    
    def createMember(self, **kwargs): return self.createRegion(**kwargs)
    
    def memberExists(self, **kwargs): return self.regionExists(**kwargs)

class Unit(CoopRegion):
    AccountsManager = UnitAccount
    Manager = 'UnitsManager'
    SubRegionsManager = MembersManager
    PersonsManager = CoopCOsManager
    
    def __init__(self, **kwargs):
        super().__init__(nameFromNumber=True, **kwargs)
        pass
    @property
    def office(self): return self.manager.office
    
    @property
    def membersManager(self): return self.subRegionsManager
    @property
    def members(self): return self.membersManager.members
    
    def memberExists(self, **kwargs): return self.membersManager.memberExists(**kwargs)
    
    def getMember(self, **kwargs): return self.getRegion(**kwargs)

class UnitsManager(CoopRegionsManager):
    regionClass = Unit
    
    @property
    def office(self): return self.master
    @property
    def units(self): return self.regions
    
    def createUnit(self, **kwargs): return self.createRegion(**kwargs)




