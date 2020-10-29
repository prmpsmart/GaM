from ..core.accounts import AccountsManager, Mixins
from ..core.regions import RegionsManager, Region, Person, PersonsManager

from ..dc.dc_regions import AreasManager

from ..coop.coop_regions import UnitsManager

from .office_accounts import CoopOfficeAccount, DCOfficeAccount, CoopOfficeAccountsManager, DCOfficeAccountsManager, OfficeAccountsManager, OfficeAccount

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
    MultiSubRegionsManager = True
    PersonsManager = OfficeManagerDetailsManager
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__dcOffice = DCOffice(self)
        self.__coopOffice = CoopOffice(self)
        
    def __str__(self): return f'{self.manager.master} | {self.className}({self.name})'
    
    @property
    def dcOffice(self): return self.__dcOffice
    @property
    def coopOffice(self): return self.__coopOffice
    @property
    def regions(self): return [self.dcOffice, self.coopOffice]
    
    def setMoneySign(self, sign='$'): Mixins._moneySign = sign
    
    @property
    def spacedID(self): return f'{self.sup.spacedID} | {self.name}'


class OfficesManager(RegionsManager):
    regionClass = Office
    
    @property
    def name(self): return self.master.name
    
    def createOffice(self, date=None, auto=None, **kwargs):
        name = kwargs.get('name')
        if name == None: name = self.name
        else: del kwargs['name']
        return self.createRegion(date=date, auto=auto, name=name, **kwargs)

class SubOffice(Region):
    DEPARTMENT = 'SO'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
    @property
    def office(self): return self.manager
    @property
    def spacedID(self): return f'{self.sup.spacedID} | {self.DEPARTMENT} '

class DCOffice(SubOffice):
    AccountsManager = DCOfficeAccountsManager
    Manager = 'DCOfficesManager'
    SubRegionsManager = AreasManager
    PersonsManager = DCManagerDetailsManager
    DEPARTMENT = 'DC'
    
    @property
    def areasManager(self): return self.subRegionsManager
    
    


# class DCOfficesManager(OfficesManager):
#     regionClass = DCOffice
    
#     def createDCOffice(self, **kwargs):
#         name = f'{self.master.name} DC Office'
#         return self.createOffice(name=name, **kwargs)

class CoopOffice(Office):
    AccountsManager = CoopOfficeAccountsManager
    Manager = 'CoopOfficesManager'
    SubRegionsManager = UnitsManager
    MultiSubRegionsManager = False
    PersonsManager = CoopManagerDetailsManager
    DEPARTMENT = 'COOP'
    
    def addUnit(self, unit):
        pass
    @property
    def unitsManager(self): return self.subRegionsManager

# class CoopOfficesManager(OfficesManager):
#     regionClass = CoopOffice
    
#     def createCoopOffice(self, **kwargs):
#         name = f'{self.master.name} COOP Office'
#         office = self.createOffice(name=name, **kwargs)
#         return office


