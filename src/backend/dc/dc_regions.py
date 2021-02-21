from ..core.regions_managers import Region, RegionsManager, Person, PersonsManager
from .dc_accounts import ClientAccountsManager, DCAccountsManager, AreaAccountsManager, PRMP_DateTime, CardDues, DCErrors, Rates
from .dc_specials import DailyContributionsManager
from .dc_sorts import DCSort

class ClientDetail(Person):
    Manager = 'ClientDetailsManager'
    @property
    def client(self): return self.manager.master

class ClientDetailsManager(PersonsManager):
    ObjectType = ClientDetail
    MultipleSubsPerMonth = False




class DC_CO(Person):
    'Daily Contribution Cash Officer.'
    Manager = 'DC_COsManager'


class DC_COsManager(PersonsManager):
    ObjectType = DC_CO
    def createDC_CO(self, **kwargs): return self.createPerson(**kwargs)


class DCRegionsManager(RegionsManager):
    pass


class DCRegion(Region):
    Errors = DCErrors
    AccountsManager = DCAccountsManager
    Manager = 'DCRegionsManager'
    SubRegionsManager = DCRegionsManager
    subTypes = ['Regions', 'Accounts', 'Records Managers', 'Persons']
    ObjectSortClass = DCSort


    @property
    def subs(self): return self.accountsManager or []


class Client(DCRegion):

    AccountsManager = ClientAccountsManager
    Manager = 'ClientsManager'
    SubRegionsManager = None
    PersonsManager = ClientDetailsManager

    subTypes = ['Accounts', 'Records Managers', 'Persons']

    def __init__(self, manager, name, date=None, rate=None, cardDue=False, **kwargs):
        super().__init__(manager=manager, name=name, date=date, rate=rate, **kwargs)
        self.cardDues = CardDues(self, cardDue)

    def __str__(self): return f'{self.manager.master} | {self.className}({self.name})'
    @property
    def spacedID(self): return f'{super().spacedID} | C{self.number}'
    @property
    def area(self): return self.manager.area

    @property
    def cardDue(self): return self.cardDues

    @cardDue.setter
    def cardDue(self, c):
        # a decoy to bypass the gui update dialog
        pass

    @property
    def rate(self): return float(self.accountsManager.last.rate)

    def changeRate(self, r):
        if r and (r != self.rate): rat = self.accountsManager.last.rates.addRecord(r)

    def changeRate(self, rate):
        if self.lastAccount: self.lastAccount.rates.setRate(rate)

    def addContribution(self, contribution, month=None, **kwargs):
        month = self.getDate(month)
        return self.accountsManager.addContribution(contribution, **kwargs)

    def addPaid(self, paid, month):
        month = self.getDate(month)
        monthAcc = self.accountManager.getAccount(month=month)
        if monthAcc: monthAcc.paids.addPaid(paid)

    def addUpfront(self, upfront, month):
        assert PRMP_DateTime.now().isSameMonth(month)
        pass


class ClientsManager(DCRegionsManager):
    ObjectType = Client
    subsName = 'Clients'
    subTypes = [subsName]


    @property
    def area(self): return self.master
    @property
    def clients(self): return self.regions

    def createClient(self, name, rate=0, cardDue=False, **kwargs): return self.createRegion(name=name, rate=rate, cardDue=cardDue, **kwargs)


class Area(DCRegion):

    AccountsManager = AreaAccountsManager
    Manager = 'AreasManager'
    SubRegionsManager = ClientsManager
    PersonsManager = DC_COsManager

    subTypes = ['Accounts', 'Records Managers', 'Persons', 'Daily Contributions']

    def __init__(self, manager, number, date=None, autoAccount=True, **kwargs):
        super().__init__(manager, number=number, date=date, nameFromNumber=True, **kwargs)
        self.__otherName = f'DC {self.number}'

        self.dailyContributionsManager = self.dailyContributions = self.dailys = DailyContributionsManager(self)
        self.subRegionsActiveByMonth = self.accountsManager.subRegionsActiveByMonth

    def __str__(self): return f'{self.manager.master} | {self.name}'

    @property
    def spacedID(self): return f'{super().spacedID} | A{self.number}'
    @property
    def otherName(self): return self.__otherName
    @property
    def clients(self): return self.clientsManager.clients
    @property
    def clientsManager(self): return self.subRegionsManager
    @property
    def totalClients(self): return len(self)
    def clientsInMonth(self, month): return self.clientsManager.clientsInMonth(month)
    def createClient(self, name, rate, cardDue=False, **kwargs): return self.clientsManager.createClient(name=name, rate=rate, cardDue=cardDue, **kwargs)


class AreasManager(DCRegionsManager):
    ObjectType = Area
    subsName = 'Areas'

    @property
    def areas(self): return self.regions

    def createArea(self, autoAccount=True, **kwargs): return self.createRegion(autoAccount=autoAccount, **kwargs)

    def getArea(self, number): return self.getFromAllRegions(number)










