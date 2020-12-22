from ..core.regions_managers import Region, RegionsManager, Person, PersonsManager, ThirdPartySurety, LoanBondDetails
from .coop_accounts import CoopErrors, CoopAccount, MemberAccount, UnitAccount
from .coop_errors import CoopErrors

class MemberDetail(Person):
    Manager = 'Member'
    # def __init__(self, **kwargs): super().__init__(**kwargs)
    @property
    def member(self): return self.manager


class CoopCO(Person):
    'Cooperative Cash Officer.'


class CoopCOsManager(PersonsManager):
    ObjectType = CoopCO
    def createCoopCo(self, **kwargs): return self.createDetail(**kwargs)


class CoopThirdPartySurety(ThirdPartySurety):
    pass


class CoopLoanBondDetails(LoanBondDetails):
    thirdPartySurety = CoopThirdPartySurety
    def __init__(self, loanBond):
    
        self.__firstSurety = None
        self.__secondSurety = None
        self.__thirdSurety = None
        self.__accountName = None
        self.__accountNumber = None
        self.__bank = None
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
    def firstSurety(self): return self.__firstSurety
    @property
    def secondSurety(self): return self.__secondSurety
    @property
    def proposedLoan(self): return self.__proposedLoan
    @property
    def thirdSurety(self): return self.__thirdSurety
    
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
    ObjectType = CoopRegion
    # def __str__(self): return f'{self.master} {self.className}'


class Member(CoopRegion):
    AccountsManager = MemberAccount
    Manager = 'MembersManager'
    Person = MemberDetail
    
    def __init__(self, manager, name='', gender='', **kwargs):
        assert name != None, 'Name can not be empty.'
        assert gender, 'Gender is not provided.'
        assert gender.lower() in ['f', 'm', 'male', 'female'], "Name can not be empty and must be among ['f', 'm', 'male', 'female']."
        
        super().__init__(manager=manager, name=name, **kwargs)
        
    @property
    def spacedID(self): return f'{super().spacedID} | M{self.number}'
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
    ObjectType = Member
   
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
    
    def __init__(self, manager, **kwargs):
        super().__init__(manager, nameFromNumber=True, **kwargs)
        
    @property
    def spacedID(self): return f'{super().spacedID} | U{self.number}'
    
    @property
    def office(self): return self.manager.office
    
    @property
    def membersManager(self): return self.subRegionsManager
    @property
    def members(self): return self.membersManager.members
    
    def memberExists(self, **kwargs): return self.membersManager.memberExists(**kwargs)
    
    def getMember(self, **kwargs): return self.getRegion(**kwargs)


class UnitsManager(CoopRegionsManager):
    ObjectType = Unit
    
    @property
    def office(self): return self.master
    @property
    def units(self): return self.regions
    
    def createUnit(self, **kwargs): return self.createRegion(**kwargs)




