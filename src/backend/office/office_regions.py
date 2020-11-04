from ..core.accounts import AccountsManager
from ..core.regions_managers import RegionsManager, Region, Person, PersonsManager

from ..dc.dc_regions import AreasManager

from ..coop.coop_regions import UnitsManager

from .office_accounts import *

class DCManagerDetail(Person):
    pass

class CoopManagerDetail(Person):
    pass

class OfficeManagerDetail(Person):
    pass


class DCManagerDetailsManager(PersonsManager):
    detailClass = DCManagerDetail
    
class CoopManagerDetailsManager(PersonsManager):
    detailClass = CoopManagerDetail
    
class OfficeManagerDetailsManager(PersonsManager):
    detailClass = OfficeManagerDetail


class Office(Region):
    AccountsManager = OfficeAccountsManager
    Manager = 'OfficesManager'
    PersonsManager = OfficeManagerDetailsManager
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.__coopOffice = CoopOffice(manager=self, sup=self, number=1)
        self.__dcOffice = DCOffice(manager=self, sup=self, number=2)
    
    @property
    def dcOffice(self): return self.__dcOffice
    @property
    def coopOffice(self): return self.__coopOffice
    @property
    def subs(self): return [self.coopOffice, self.dcOffice]
    def setMoneySign(self, sign='$'): Mixins._moneySign = sign
    @property
    def spacedID(self): return f'{self.sup.spacedID} | {self.name}'


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
    def __str__(self): return f'{self.manager.master} | {self.name} '
    @property
    def name(self): return f'{self.office.name} {self.DEPARTMENT}'
    @property
    def office(self): return self.manager
    @property
    def spacedID(self): return f'{self.sup.spacedID} | {self.DEPARTMENT} '

class DCOffice(SubOffice):
    AccountsManager = DCOfficeAccountsManager
    SubRegionsManager = AreasManager
    PersonsManager = DCManagerDetailsManager
    DEPARTMENT = 'DC'
    
    @property
    def areasManager(self): return self.subRegionsManager
    

class CoopOffice(SubOffice):
    AccountsManager = CoopOfficeAccountsManager
    SubRegionsManager = UnitsManager
    PersonsManager = CoopManagerDetailsManager
    DEPARTMENT = 'Coop'
    
    def addUnit(self, unit):
        pass
    @property
    def unitsManager(self): return self.subRegionsManager




