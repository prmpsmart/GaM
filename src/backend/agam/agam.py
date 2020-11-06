from ..office.office_regions import OfficesManager, Region
from .agam_accounts import AGAMAccountsManager
from ..core.regions_managers import Person, PersonsManager

class CEO(Person):
    pass

class CEOsManager(PersonsManager):
    ObjectType = CEO

    def createCEO(self, **kwargs): return self.createPerson(**kwargs)
    

class AGAM(Region):
    SubRegionsManager = OfficesManager
    AccountsManager = AGAMAccountsManager
    PersonsManager = CEOsManager
    
    def __init__(self, manager='AGAM',  name='AGAM'):
        super().__init__(manager, name=name)
        
    def __str__(self): return f'{self.name}'
    
    @property
    def master(self): return self
    
    @property
    def officesManager(self): return self.subRegionsManager
    
    @property
    def managersManager(self): return self.detailsManager
    
    @property
    def spacedID(self): return self.name





