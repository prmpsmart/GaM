__author__ = "PRMP Smart"
from core import RegionsManager, Region, Person, PersonsManager, AccountsManager
from dc import AreasManager, AreaAccount, AreaAccountsManager
from prmp_miscs import PRMP_StrMixins



# class CoopOfficeAccount(UnitAccount):
#     Manager = 'CoopOffice'


class DCOfficeAccount(AreaAccount):
    Manager = 'DCOfficeAccountsManager'

    def _balanceAccount(self, date=None):
        areasAccounts = self.manager.sortSubRegionsAccountsByMonth(self.date)
        for a in areasAccounts: a.balanceAccount()
        if areasAccounts:
            self.incomes.updateWithOtherManagers([account.incomes for account in areasAccounts])
            
            self.balances.updateWithOtherManagers([account.balances for account in areasAccounts])
            
            self.broughtForwards.updateWithOtherManagers([account.broughtForwards for account in areasAccounts])
            
            self.commissions.updateWithOtherManagers([account.commissions for account in areasAccounts])
            
            self.debits.updateWithOtherManagers([account.debits for account in areasAccounts])
            
            self.savings.updateWithOtherManagers([account.savings for account in areasAccounts])
            
            self.upfronts.updateWithOtherManagers([account.upfronts for account in areasAccounts])
            
            self.excesses.updateWithOtherManagers([account.excesses for account in areasAccounts])
            
            self.deficits.updateWithOtherManagers([account.deficits for account in areasAccounts])
            
            self.btos.updateWithOtherManagers([account.btos for account in areasAccounts])
        
            self.paidouts.updateWithOtherManagers([account.paidouts for account in areasAccounts])
            
            self.withdrawals.updateWithOtherManagers([account.withdrawals for account in areasAccounts])
            
            self.transfers.updateWithOtherManagers([account.transfers for account in areasAccounts])

            self.normalIncomes.updateWithOtherManagers([account.normalIncomes for account in areasAccounts])


class DCOfficeAccountsManager(AreaAccountsManager):
    ObjectType = DCOfficeAccount



class DCManagerDetail(Person):
    Manager = 'DCManagerDetailsManager'

class CoopManagerDetail(Person):
    Manager = 'CoopManagerDetailsManager'

class OfficeManagerDetail(Person):
    Manager = 'OfficeManagerDetailsManager'


class DCManagerDetailsManager(PersonsManager):
    ObjectType = DCManagerDetail
    
# class CoopManagerDetailsManager(PersonsManager):
#     ObjectType = CoopManagerDetail
    
class OfficeManagerDetailsManager(PersonsManager):
    ObjectType = OfficeManagerDetail


class Office(Region):
    AccountsManager = AccountsManager
    Manager = 'OfficesManager'
    PersonsManager = OfficeManagerDetailsManager
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # self.__coopOffice = CoopOffice(manager=self, sup=self, number=1)
        self.__dcOffice = DCOffice(manager=self, sup=self, number=2)
    
    def __str__(self):
        if self.strManager: return self.manager
        else: return f'{self.manager.name} | {self.name}'
    
    # @property
    # def name(self):
    #     _name = self.manager if self.strManager else self.manager.name
    #     return _name

    @property
    def dcOffice(self): return self.__dcOffice
    @property
    def coopOffice(self): return self.__coopOffice
    
    @property
    def subs(self): return self.subRegions
    
    @property
    def subRegions(self): return [self.coopOffice, self.dcOffice]
    
    def setMoneySign(self, sign='$'): PRMP_StrMixins._moneySign = sign

    @property
    def spacedID(self): return f'{super().spacedID} | {self.name}'


class OfficesManager(RegionsManager):
    ObjectType = Office
    
    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs)
    
    @property
    def name(self): return self.master.name
    
    def createOffice(self, name=None, **kwargs):
        if name == None: name = self.name 
        return self.createRegion(name=name, **kwargs)


class SubOffice(Region):
    DEPARTMENT = 'SO'
    Manager = 'Office'

    def __str__(self):
        if self.strManager: return f'{self.manager} | {self.location} {self.DEPARTMENT}'
        else: return f'{self.manager} | {self.name}'

    @property
    def name(self):
        _name = self.manager if self.strManager else self.manager.name
        return f'{_name} {self.DEPARTMENT}'
    @property
    def office(self): return self.manager
    @property
    def spacedID(self): return f'{super().spacedID} | {self.DEPARTMENT} '


class DCOffice(SubOffice):
    AccountsManager = DCOfficeAccountsManager
    SubRegionsManager = AreasManager
    PersonsManager = DCManagerDetailsManager
    DEPARTMENT = 'DC'

    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs)
        self.subRegionsActiveByMonth = self.accountsManager.subRegionsActiveByMonth
        from dc import DCSort
        self.allSort = DCSort(self)
    
    @property
    def areasManager(self): return self.subRegionsManager


# class CoopOffice(SubOffice):
#     AccountsManager = CoopOfficeAccount
#     SubRegionsManager = UnitsManager
#     PersonsManager = CoopManagerDetailsManager
#     DEPARTMENT = 'COOP'
    
#     def addUnit(self, unit):
#         pass
#     @property
#     def unitsManager(self): return self.subRegionsManager




