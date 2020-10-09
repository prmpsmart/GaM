from ..core.accounts import AccountsManager, Mixins
from ..core.regions import RegionsManager, Region

from ..dc.dc_regions import AreasManager

from ..coop.coop_regions import UnitsManager

from .office_accounts import CoopOfficeAccount, DCOfficeAccount, CoopOfficeAccountsManager, DCOfficeAccountsManager, OfficeAccountsManager, OfficeAccount
from .office_details import DCManagerDetailsManager, CoopManagerDetailsManager, OfficeManagerDetailsManager


class Office(Region):
    AccountManager = OfficeAccountsManager
    Manager = 'OfficesManager'
    MultiSubRegionsManager = True
    DetailsManager = OfficeManagerDetailsManager
    
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
    DetailsManager = DCManagerDetailsManager
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
    DetailsManager = CoopManagerDetailsManager
    MultiSubRegionsManager = False
    
    @classmethod
    def addUnit(cls, unit):
        pass
    @property
    def unitsManager(self): return self.subRegionsManager

class CoopOfficesManager(OfficesManager):
    regionClass = CoopOffice
    
    def createCoopOffice(self, **kwargs): return self.createOffice(**kwargs)


