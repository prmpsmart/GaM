from ..core.regions import Region, RegionsManager
from .coop_accounts import CoopErrors, CoopAccount, MemberAccount, UnitAccount
from .coop_details import MemberDetail, CoopCOsManager

class CoopRegion(Region):
    Errors = CoopErrors
    AccountManager = CoopAccount
    Manager = 'CoopRegionsManager'

class CoopRegionsManager(RegionsManager):
    regionClass = CoopRegion
    # def __str__(self): return f'{self.master} {self.className}'

class Member(CoopRegion):
    AccountManager = MemberAccount
    Manager = 'MembersManager'
    Detail = MemberDetail
    
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
    AccountManager = UnitAccount
    Manager = 'UnitsManager'
    SubRegionsManager = MembersManager
    DetailsManager = CoopCOsManager
    
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




