from ..core.accounts import AccountsManager
from ..core.regions_managers import RegionsManager, Region, Person, PersonsManager

from ..dc.dc_regions import AreasManager

from ..coop.coop_regions import UnitsManager

from .office_accounts import *

class DCManagerDetail(Person):
    Manager = 'DCManagerDetailsManager'

class CoopManagerDetail(Person):
    Manager = 'CoopManagerDetailsManager'

class OfficeManagerDetail(Person):
    Manager = 'OfficeManagerDetailsManager'


class DCManagerDetailsManager(PersonsManager):
    ObjectType = DCManagerDetail
    
class CoopManagerDetailsManager(PersonsManager):
    ObjectType = CoopManagerDetail
    
class OfficeManagerDetailsManager(PersonsManager):
    ObjectType = OfficeManagerDetail


class Office(Region):
    AccountsManager = AccountsManager
    Manager = 'OfficesManager'
    PersonsManager = OfficeManagerDetailsManager
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.__coopOffice = CoopOffice(manager=self, sup=self, number=1)
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
    
    def setMoneySign(self, sign='$'): Mixins._moneySign = sign
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
        master = self.manager if self.strManager else self.manager
        # return f'{master}'
        return f'{master} | {self.name}'
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
        from ..dc.dc_sorts import DCSort
        self.allSort = DCSort(self)
    
    @property
    def areasManager(self): return self.subRegionsManager


class CoopOffice(SubOffice):
    AccountsManager = CoopOfficeAccount
    SubRegionsManager = UnitsManager
    PersonsManager = CoopManagerDetailsManager
    DEPARTMENT = 'COOP'
    
    def addUnit(self, unit):
        pass
    @property
    def unitsManager(self): return self.subRegionsManager




