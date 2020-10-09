from ..core.regions import Region, RegionsManager
from .dc_accounts import ClientAccountsManager, DCAccountsManager, AreaAccountsManager, DateTime, CardDues, DCErrors, Rates
from .dc_details import ClientDetail, DCCOsManager

class DCRegionsManager(RegionsManager):
    pass

class DCRegion(Region):
    Errors = DCErrors
    AccountManager = DCAccountsManager
    Manager = DCRegionsManager
    SubRegionsManager = DCRegionsManager

class Client(DCRegion):
    
    AccountManager = ClientAccountsManager
    Manager = 'ClientsManager'
    SubRegionsManager = None
    Detail = ClientDetail
    
    def __init__(self, manager, name, date, rate=None, cardDue=False, **kwargs):
        super().__init__(manager=manager, name=name, date=date, rate=rate, **kwargs)
        self.__detail = ClientDetail(self, **kwargs)
        self.__cardDues = CardDues(self, cardDue)

    def __str__(self): return f"{self.manager} | {self.className}({self.name})"
    
    @property
    def area(self): return self.manager.area
    @property
    def cardDues(self): return self.__cardDues
    
    def changeRate(self, rate):
        if self.lastAccount: self.lastAccount.rates.setRate(rate)
    
    def addContribution(self, contribution, month=None):
        if month == None: month = DateTime.now()
        pass
    
    def addPaid(self, paid, month):
        if month == None: month = DateTime.now()
        monthAcc = self.accountManager.getAccount(month)
        if monthAcc: monthAcc.paids.addPaid(paid)
    
    def addUpfront(self, upfront, month):
        assert DateTime.now().isSameMonth(month)
        pass

class ClientsManager(DCRegionsManager):
    regionClass = Client
    
    @property
    def area(self): return self.master
    @property
    def clients(self): return self.regions
    
    def createClient(self, name, rate, cardDue=False, **kwargs): return self.createRegion(name=name, rate=rate, cardDue=cardDue, **kwargs)


class Area(DCRegion):
    
    AccountManager = AreaAccountsManager
    Manager = 'AreasManager'
    SubRegionsManager = ClientsManager
    DetailsManager = DCCOsManager
    
    def __init__(self, manager, number, date=None, autoAccount=True, **kwargs):
        super().__init__(manager, number=number, date=date, nameFromNumber=True, **kwargs)
        self.__otherName = f'DC {self.number}'
        
    def __str__(self): return f'{self.manager} | {self.className}({self.name})'
    @property
    def otherName(self): return self.__otherName
    @property
    def clientsManager(self): return self.subRegionsManager
    @property
    def totalClients(self): return len(self)
    def clientsInMonth(self, month): return self.clientsManager.clientsInMonth(month)
    def createClient(self, name, rate, cardDue=False): return self.clientsManager.createClient(name=name, rate=rate, cardDue=cardDue)

class AreasManager(DCRegionsManager):
    regionClass = Area
    
    @property
    def areas(self): return self.regions

    def createArea(self, autoAccount=True, **kwargs): return self.createRegion(autoAccount=autoAccount, **kwargs)
    
    def getArea(self, number): return self.getFromAllRegions(number)
