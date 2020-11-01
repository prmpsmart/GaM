
from .dc_records_managers import BroughtForwards, Rates, Contributions, Savings, Upfronts, Balances, BroughtToOffices, Excesses, Deficits, CardDues, DCErrors, Debits
from ..core.accounts import DateTime, Account, AccountsManager


class DCAccount(Account):
    Manager = 'DCAccountsManager'
    
    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs)
        
        self.__broughtForwards = BroughtForwards(self)
        self.__savings = Savings(self)
        self.__debits = Debits(self)
        self.__upfronts = Upfronts(self)
        self.__balances = Balances(self)
        
    def __int__(self): return int(self.balances)
    @property
    def region(self):
        if self.manager: return self.manager.region
        return None
    
    @property
    def recordsManagers(self): return [self.broughtForwards, self.savings, self.debits, self.upfronts, self.balances]
    
    @property
    def broughtForwards(self): return self.__broughtForwards
    @property
    def savings(self): return self.__savings
    @property
    def debits(self): return self.__debits
    @property
    def upfronts(self): return self.__upfronts
    @property
    def pendingUpfronts(self): return self.upfronts.lastRecord.outstanding
    @property
    def repaidUpfronts(self): return self.upfronts.lastRecord.repaid
    @property
    def balances(self): return self.__balances
    def addBroughtForward(self, bf, date=None): return self.broughtForwards.createRecord(bf, date=date)
    
    def balanceAccount(self, date=None):
        self._balanceAccount(date)
        if self.nextAccount: self.nextAccount.addBroughtForward(int(self.balances))

class DCAccountsManager(AccountsManager):
    ObjectType = DCAccount
    
    def __init__(self, region, **kwargs):
        super().__init__(region, **kwargs)
        

class ClientAccount(DCAccount):
    Manager = 'ClientAccountsManager'
    
    def __init__(self, manager, ledgerNumber=0, rate=0, **kwargs):
        super().__init__(manager, **kwargs)
        
        self.__ledgerNumber = ledgerNumber
        self.__contributions = Contributions(self)
        self.__rates = Rates(self, rate)
        
        
    @property
    def recordsManagers(self):
        recordsManagers_ =  super().recordsManagers
        recordsManagers_.insert(1, self.rates)
        recordsManagers_.insert(2, self.contributions)
        return recordsManagers_
    
    @property
    def rate(self): return int(self.rates)
    @property
    def rates(self): return self.__rates
    @property
    def contributions(self): return self.__contributions
    @property
    def ledgerNumber(self): return self.__ledgerNumber
    def _balanceAccount(self, date=None):
        rate = int(self.rates)
        bal = int(self.broughtForwards) + int(self.savings) - self.upfronts.outstanding - int(self.debits) - self.rate
        self.balances.createRecord(bal, notAdd=True, newRecord=False, date=date)

    def addContribution(self, contribution): self.contributions.addContribution(contribution)
    
    def addDebit(self, debit): self.debits.addDebit(debit)
    
    def addUpfront(self, upfront):
        # assert DateTime.now().isSameMonth(month)
        pass

class AreaAccount(DCAccount):
    Manager = 'AreaAccountsManager'
    
    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs)
        self.__broughtToOffices = BroughtToOffices(self)#
        self.__excesses = Excesses(self)
        self.__deficits = Deficits(self)
    
    @property
    def commissions(self): return self.__commissions
    @property
    def recordsManagers(self):
        recordsManagers =  super().recordsManagers + [self.broughtToOffices, self.excesses, self.deficits]
        return recordsManagers
    
    @property
    def broughtToOffices(self): return self.__broughtToOffices
    @property
    def excesses(self): return self.__excesses
    @property
    def deficits(self): return self.__deficits
    def _balanceAccount(self):
        clientsAccounts = self.manager.sortClientsAccountsByMonth(self.date)
        self.balances.updateWithOtherManagers([account.balances for account in clientsAccounts])
        self.broughtForwards.updateWithOtherManagers([account.broughtForwards for account in clientsAccounts])
        self.commissions.updateWithOtherManagers([account.rates for account in clientsAccounts])
        self.debits.updateWithOtherManagers([account.debits for account in clientsAccounts])
        self.savings.updateWithOtherManagers([account.savings for account in clientsAccounts])
        self.upfronts.updateWithOtherManagers([account.upfronts for account in clientsAccounts])
        
        ###############
        
        self.balances
        self.excesses
        self.deficits


class ClientAccountsManager(DCAccountsManager):
    ObjectType = ClientAccount
    
    def __init__(self, region, **kwargs):
        self.__startRate = kwargs.get('rate', 0)
        super().__init__(region, **kwargs)
    
    @property
    def areaAccountsManager(self): return self.master.accountsManager
    
    @property
    def startRate(self): return self.__startRate
    
    def createAccount(self, rate=0, **kwargs):
        # prmp needs proper thinking
        # get total accounts for current month from the area account manager
        lastAccount = self.lastAccount
        lastLedgerNumber = lastAccount.ledgerNumber if lastAccount else 0
        ledgerNumber = lastLedgerNumber + 1
        return super().createAccount(rate=rate, ledgerNumber=ledgerNumber, **kwargs)

    def changeRate(self, rate):
        if self.lastAccount: self.lastAccount.rates.setRate(rate)
    
    def addContribution(self, contribution, month=None):
        if month == None: month = DateTime.now()
        pass
    
    def addDebit(self, debit, month):
        if month == None: month = DateTime.now()
        monthAcc = self.accountManager.getAccount(month)
        if monthAcc: monthAcc.debits.addDebit(debit)
    
    def addUpfront(self, upfront, month):
        assert DateTime.now().isSameMonth(month)
        pass

class AreaAccountsManager(DCAccountsManager):
    ObjectType = AreaAccount
    
    @property
    def clientsManager(self): return self.region.clientsManager
    
    def sortClientsAccountsByMonth(self, month): return self.sortSubRegionsAccountsByMonth(month)





