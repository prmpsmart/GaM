
from .dc_records_managers import *
from ..core.accounts import PRMP_DateTime, Account, AccountsManager


class DCAccount(Account):
    Manager = 'DCAccountsManager'
    
    def __init__(self, manager, month=None, **kwargs):
        super().__init__(manager, **kwargs)
        assert month, 'Month that this account belongs to must be given.'

        self._month = month

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
    def __float__(self): return float(self.balances)
    @property
    def name(self): return f'{self.className}({self._month.dayMonthYear})'
    @property
    def month(self): return self._month
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
        if self.nextAccount: self.nextAccount.addBroughtForward(float(self.balances))


class DCAccountsManager(AccountsManager):
    ObjectType = DCAccount
    
    def __init__(self, region, **kwargs):
        super().__init__(region, **kwargs)
    
    @property
    def overAllAccounts(self):
        # total accounts in this manager
        containerDict = {}
        for recordManager in self.lastAccount:
            name = recordManager.className
            if name not in containerDict: containerDict[name] = 0
            containerDict[name] += float(recordManager)
        return containerDict
    
    
    def createAccount(self, month=None, **kwargs):
        month = self.getDate(month)
        return super().createAccount(month=month, **kwargs)
    
    @property
    def recordsManagers(self): return self.last if len(self) else []





class ClientAccount(DCAccount):
    Manager = 'ClientAccountsManager'
    
    def __init__(self, manager, ledgerNumber=0, rate=0, areaAccount=None, month=None, **kwargs):
        self.areaAccount = areaAccount
        if month: assert month.monthYear == areaAccount.month.monthYear, 'ClientAccount month must be same as AreaAccount month.'

        super().__init__(manager, month=month or areaAccount.month, **kwargs)

        rate = float(rate)
        self.ledgerNumber = ledgerNumber
        self.contributions = Contributions(self)
        self.rates = Rates(self, rate)
    
    @property
    def name(self): return f'{self.className}({self._month.monthYear} | No. {self.ledgerNumber})'
    
    def income(self, date=None):
        date = self.getDate(date)
        return sum([rec.savings for rec in self.contributions if rec.date.month == date.month])
    
    @property
    def recordsManagers(self):
        recordsManagers_ =  super().recordsManagers
        recordsManagers_.insert(1, self.rates)
        recordsManagers_.insert(2, self.contributions)
        return recordsManagers_
    
    @property
    def rate(self): return float(self.rates)

    def _balanceAccount(self, date=None):
        rate = float(self.rates)
        bal = float(self.broughtForwards) + float(self.savings) - float(self.upfronts.outstanding) - float(self.debits) - rate
        
        self.balances.createRecord(bal, notAdd=True, newRecord=False, date=date)

    def addContribution(self, contribution, **kwargs):
        rec = self.contributions.addContribution(contribution, **kwargs)
        self.balanceAccount()
        return rec
    
    def addDebit(self, debit, _type='w', **kwargs):
        self._balanceAccount()
        rec = self.debits.addDebit(debit, _type=_type, **kwargs)
        self.balanceAccount()
        return rec
    
    def addUpfront(self, upfront):
        # assert PRMP_DateTime.now().isSameMonth(month)
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

        incomes = [self.sumRecords(acc.incomes.sortSubsByDate(date)) for acc in clientsAccounts()]

        contributed = sum(incomes)

        transfers = self.sumRecords(self.transfers.sortRecordsByDate(date))
        
        btoRec = self.btos.createRecord(bto, date)
        bto += transfers

        if bto > contributed: self.excesses.createRecord(bto - contributed, date, coRecord=btoRec)
        elif contributed > bto: self.deficits.createRecord(contributed - bto, date, coRecord=btoRec)

    def clientsAccounts(self, month=None): return sorted(self.manager.sortClientsAccountsByMonth(month or self.month))

    def getClientAccount(self, number, month=None):
        clientsAccounts = self.clientsAccounts(month)
        
        for clientsAccount in clientsAccounts:
            if clientsAccount.ledgerNumber == number: return clientsAccount


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
        areaAcc = area.accountsManager.getAccount(month=month)
        if areaAcc:
            ledgerNumber = areaAcc.ledgerNumbers + 1

            acc = super().createAccount(rate=rate, ledgerNumber=ledgerNumber, areaAccount=areaAcc, month=month, **kwargs)

            areaAcc.addClientAccount(acc)
            return acc

        else: raise DCErrors.AccountsError(f'{area} does not have an account in {month.monthYear} ')

    def changeRate(self, rate):
        if self.lastAccount: self.lastAccount.rates.setRate(rate)
    
    def addContribution(self, contribution, month=None, **kwargs):
        if month == None: month = PRMP_DateTime.now()
        account = self.sortSubsByMonth(month)[0]
        return account.addContribution(contribution, **kwargs)
    
    def addDebit(self, debit, month):
        if month == None: month = PRMP_DateTime.now()
        monthAcc = self.accountManager.getAccount(month=month)
        if monthAcc: monthAcc.debits.addDebit(debit)
    
    def addUpfront(self, upfront, month):
        assert PRMP_DateTime.now().isSameMonth(month)
        pass


class AreaAccountsManager(DCAccountsManager):
    ObjectType = AreaAccount
    
    @property
    def clientsManager(self): return self.region.clientsManager
    
    def sortClientsAccountsByMonth(self, month): return self.sortSubRegionsAccountsByMonth(month)



