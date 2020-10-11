from ..office.office_regions import OfficesManager, Region
from .agam_accounts import AGAMAccountsManager
from .agam_details import CEOsManager

class AGAM(Region):
    SubRegionsManager = OfficesManager
    AccountManager = AGAMAccountsManager
    PersonsManager = CEOsManager
    
    def __init__(self, manager='AGAM',  name='AGAM'):
        super().__init__(manager=manager, name=name)
        
    def __str__(self): return f'{self.name}'
    @property
    def officesManager(self): return self.subRegionsManager
    @property
    def managersManager(self): return self.detailsManager





