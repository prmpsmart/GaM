from ..office.office_regions import OfficesManager, Region
from .gam_accounts import GaMAccountsManager
from ..core.regions_managers import Person, PersonsManager
from ..gam_config import GaM_Settings

class CEO(Person): Manager = 'CEOsManager'

class CEOsManager(PersonsManager):
    ObjectType = CEO

    def createCEO(self, **kwargs): return self.createPerson(**kwargs)


class GaM(Region):

    SubRegionsManager = OfficesManager
    AccountsManager = GaMAccountsManager
    PersonsManager = CEOsManager
    
    def __init__(self, manager='GaM',  name='GaM', date=None):
        super().__init__(manager, name=name, date=date)
        assert not GaM_Settings.GaM, 'An Object of GaM is aready created.'
        GaM_Settings.GaM = self
    
    def __str__(self): return self.name
    
    @property
    def master(self): return self
    
    @property
    def officesManager(self): return self.subRegionsManager
    
    @property
    def managersManager(self): return self.detailsManager
    
    @property
    def spacedID(self): return self.name





