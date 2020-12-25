
from .dc_records_managers import *
from ..core.accounts import DateTime, Account, AccountsManager


class DCAccount(Account):
    Manager = 'DCAccountsManager'
    
    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs)
        self.incomes = Incomes(self)
        self.broughtForwards = BroughtForwards(self)
        self.savings = Savings(self)
        self.debits = Debits(self)
        self.upfronts = Upfronts(self)
        self.balances = Balances(self)

        self.transfers = Transfers(self)
        self.normalIncomes = NormalIncomes(self)
        self.paidouts = Paidouts(self)
        self.withdrawals = Withdrawals(self)

        
    def __int__(self): return int(self.balances)
    
    @property
    def region(self):
        if self.manager: return self.manager.region
        return None
    
    @property
    def recordsManagers(self): return [self.broughtForwards, self.incomes, self.normalIncomes, self.transfers, self.savings, self.debits, self.withdrawals, self.paidouts, self.upfronts, self.balances]

    @property
    def pendingUpfronts(self): return self.upfronts.lastRecord.outstanding
    
    @property
    def repaidUpfront(self):
        if len(self.upfronts): return self.upfronts.lastRecord.repaid

    def addBroughtForward(self, bf, date=None, **kwargs): return self.broughtForwards.createRecord(bf, date=date, **kwargs)
    
    def balanceAccount(self, date=None):
        self._balanceAccount(date)
        self.updateBroughtForwards()
    
    def updateBroughtForwards(self):
        if self.nextAccount: self.nextAccount.addBroughtForward(int(self.balances))


class DCAccountsManager(AccountsManager):
    ObjectType = DCAccount
    
    def __init__(self, region, **kwargs):
        super().__init__(region, **kwargs)


class ClientAccount(DCAccount):
    Manager = 'ClientAccountsManager'
    
    def __init__(self, manager, ledgerNumber=0, rate=0, areaAccount=None, **kwargs):
        super().__init__(manager, **kwargs)
        rate = int(rate)
        self.areaAccount = areaAccount
        self.ledgerNumber = ledgerNumber
        self.contributions = Contributions(self)
        self.rates = Rates(self, rate)
    
    def income(self, date=None):
        if date == None: date = DateTime.now()
        DateTime.checkDateTime(date)
        return sum([rec.savings for rec in self.contributions if rec.date.month == date.month])
    
    @property
    def recordsManagers(self):
        recordsManagers_ =  super().recordsManagers
        recordsManagers_.insert(1, self.rates)
        recordsManagers_.insert(2, self.contributions)
        return recordsManagers_
    
    @property
    def rate(self): return int(self.rates)

    def _balanceAccount(self, date=None):
        rate = int(self.rates)
        bal = int(self.broughtForwards) + int(self.savings) - int(self.upfronts.outstanding) - int(self.debits) - rate
        
        if bal: self.balances.createRecord(bal, notAdd=True, newRecord=False, date=date)

    def addContribution(self, contribution, **kwargs): return self.contributions.addContribution(contribution, **kwargs)
    
    def addDebit(self, debit, up=1, _type='w'):
        if up: self._balanceAccount()
        self.debits.addDebit(debit, _type=_type)
    
    def addUpfront(self, upfront):
        # assert DateTime.now().isSameMonth(month)
        pass


class AreaAccount(DCAccount):
    Manager = 'AreaAccountsManager'

    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs)
        self.commissions = Commissions(self)
        self.broughtToOffices = BroughtToOffices(self)
        self.excesses = Excesses(self)
        self.deficits = Deficits(self)
        self.ledgerNumbers = 0
        self._clientsAccounts = []
    
    def addClientAccount(self, account):
        self._clientsAccounts.append(account)
        self.ledgerNumbers = len(self._clientsAccounts)

    
    @property
    def recordsManagers(self):
        recordsManagers =  super().recordsManagers + [self.broughtToOffices, self.excesses, self.deficits]
        return recordsManagers
    
    @property
    def btos(self): return self.broughtToOffices
    
    def _balanceAccount(self, date=None):
        clientsAccounts = self._clientsAccounts
        for a in self._clientsAccounts: a.balanceAccount()
        if clientsAccounts:

            self.incomes.updateWithOtherManagers([account.incomes for account in clientsAccounts])
            
            self.balances.updateWithOtherManagers([account.balances for account in clientsAccounts])
            
            self.commissions.updateWithOtherManagers([account.rates for account in clientsAccounts])
            
            self.debits.updateWithOtherManagers([account.debits for account in clientsAccounts])
            
            self.savings.updateWithOtherManagers([account.savings for account in clientsAccounts])
            
            self.upfronts.updateWithOtherManagers([account.upfronts for account in clientsAccounts])
            
            self.paidouts.updateWithOtherManagers([account.paidouts for account in clientsAccounts])
            
            self.withdrawals.updateWithOtherManagers([account.withdrawals for account in clientsAccounts])
            
            self.transfers.updateWithOtherManagers([account.transfers for account in clientsAccounts])

            self.normalIncomes.updateWithOtherManagers([account.normalIncomes for account in clientsAccounts])
        
    
    def addBto(self, bto, date=None):
        clientsAccounts = self.clientsAccounts

        incomes = [self.sumRecords(acc.incomes.sortSubsByDate(date)) for acc in clientsAccounts]

        contributed = sum(incomes)

        transfers = self.sumRecords(self.transfers.sortRecordsByDate(date))
        
        btoRec = self.btos.createRecord(bto, date)
        bto += transfers

        if bto > contributed: self.excesses.createRecord(bto - contributed, date, coRecord=btoRec)
        elif contributed > bto: self.deficits.createRecord(contributed - bto, date, coRecord=btoRec)

    @property
    def clientsAccounts(self, month=None): return sorted(self.manager.sortClientsAccountsByMonth(month or self.date))


class ClientAccountsManager(DCAccountsManager):
    ObjectType = ClientAccount
    MultipleSubsPerMonth = True
    
    def __init__(self, region, **kwargs):
        self.startRate = kwargs.get('rate', 0)
        super().__init__(region, **kwargs)
    
    @property
    def areaAccountsManager(self): return self.master.accountsManager
    
    def createAccount(self, rate=0, month=None, **kwargs):
        area = self.region.sup
        areaAcc = area.accountsManager.getAccount(month)
        if areaAcc:
            ledgerNumber = areaAcc.ledgerNumbers + 1 if areaAcc else 1

            acc = super().createAccount(rate=rate, ledgerNumber=ledgerNumber, areaAccount=areaAcc, **kwargs)

            areaAcc.addClientAccount(acc)
            return acc

        else: raise self.Error.AccountError(f'{area} does not have an account in {month.monthYear} ')

    def changeRate(self, rate):
        if self.lastAccount: self.lastAccount.rates.setRate(rate)
    
    def addContribution(self, contribution, month=None, **kwargs):
        if month == None: month = DateTime.now()
        account = self.sortSubsByMonth(month)[0]
        return account.addContribution(contribution, **kwargs)
    
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





