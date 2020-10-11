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
    AccountManager = OfficeAccountsManager
    Manager = 'OfficesManager'
    MultiSubRegionsManager = True
    PersonsManager = OfficeManagerDetailsManager
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__dcOfficesManager = DCOfficesManager(self)
        self.__coopOfficesManager = CoopOfficesManager(self)
        
    def __str__(self): return f'{self.manager.master} | {self.className}({self.name})'
    
    @property
    def dcOfficesManager(self): return self.__dcOfficesManager
    @property
    def coopOfficesManager(self): return self.__coopOfficesManager
    
    def setMoneySign(self, sign=0): Mixins._moneySign = sign

class OfficesManager(RegionsManager):
    regionClass = Office
    
    @property
    def name(self): return self.master.name
    
    def createOffice(self, date=None, auto=None, **kwargs):
        name = kwargs.get('name')
        if name == None: name = self.name
        else: del kwargs['name']
        return self.createRegion(date=date, auto=auto, name=name, **kwargs)

class DCOffice(Office):
    AccountManager = DCOfficeAccountsManager
    Manager = 'DCOfficesManager'
    SubRegionsManager = AreasManager
    PersonsManager = DCManagerDetailsManager
    MultiSubRegionsManager = False
    
    @property
    def areasManager(self): return self.subRegionsManager

class DCOfficesManager(OfficesManager):
    regionClass = DCOffice
    
    def createDCOffice(self, **kwargs):
        name = f'{self.master.name} DC Office'
        return self.createOffice(name=name, **kwargs)

class CoopOffice(Office):
    AccountManager = CoopOfficeAccountsManager
    Manager = 'CoopOfficesManager'
    SubRegionsManager = UnitsManager
    PersonsManager = CoopManagerDetailsManager
    MultiSubRegionsManager = False
    
    @classmethod
    def addUnit(cls, unit):
        pass
    @property
    def unitsManager(self): return self.subRegionsManager

class CoopOfficesManager(OfficesManager):
    regionClass = CoopOffice
    
    def createCoopOffice(self, **kwargs): return self.createOffice(**kwargs)


