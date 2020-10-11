from src.backend.core.records import Repayment, DateTime, RecordsManager, RepaymentsManager
from .dc_errors import DCErrors


class DCRecordsManager(RecordsManager):
    _shortName = 'dcrec'
    def __init__(self, account, lastRecord=False):
        super().__init__(account)
        self._lastRecord = lastRecord
    
    def __int__(self):
        if self._lastRecord: return self.lastMoney
        else: return super().__int__()

class Rates(DCRecordsManager):
    _shortName = 'rts'
    lowest = 50
    
    def __init__(self, accounts, rate):
        super().__init__(accounts, True)
        self.setRate(rate)
    def __int__(self): return int(self[-1])
    
    def payUpBal(self, rate):
        contributions = int(self.account.contributions)
        if rate > self.rate:
            payUpBal = (rate - self.rate) * contributions
            return payUpBal
        return -1
    
    @classmethod
    def checkRate(cls, rate):
        if rate < cls.lowest: raise DCErrors.RatesError(f'Rate must not be less than {cls.lowest}')
        return True
    
    def setRate(self, rate):
        if self.checkRate(rate): self.addRecord(rate)

class Balances(DCRecordsManager):
    _shortName = 'bal'
    
    def __init__(self, account):
        super().__init__(account, True)
    
    @property
    def balance(self): return self.recordAccount

class BroughtForwards(DCRecordsManager):
    _shortName = 'btf'
    def __init__(self, account):
        super().__init__(account, True)

class BroughtToOffices(DCRecordsManager):
    _shortName = 'bto'
    
    @property
    def broughtToOffice(self): return self.recordAccount

class CardDues(DCRecordsManager):
    def __init__(self, account, cardDue=True):
        super().__init__(account)
        if cardDue == True: self.addRecord(100, account.date)
    
    @property
    def cardDues(self): return self.totalMonies

class Commissions(DCRecordsManager):
    _shortName = 'com'

class Contributions(DCRecordsManager):
    _shortName = 'dcs'
    
    def payUp(self, rate, payup):
        payUpBal = self.account.rates.payUpBal(rate)
        if payUpBal != -1:
            if payup == payUpBal: self.account.rates.changeRate(rate)

    def addContribution(self, contribution, **kwargs):
        if (int(self) + contribution) < 32: self.addRecord(contribution, **kwargs)
        else: raise DCErrors.ContributionsError(f'Contributions will be {int(self) + contribution} which is more than 31')

class Debits(DCRecordsManager):
    _shortName = 'deb'
    lowest = Rates.lowest
    
    def addDebit(self, toDebit, **kwargs):
        if self.checkMoney(toDebit):
            balance = int(self.account.balances)
            if toDebit <= balance: self.addRecord(toDebit, **kwargs)
            else: raise DCErrors.BalancesError(f'Amount to debit is more than balance of {balance}')

class Deficits(DCRecordsManager):
    _shortName = 'def'
    
    @property
    def deficit(self): return self.recordAccount

class Excesses(DCRecordsManager):
    _shortName = 'exc'
    
    @property
    def excess(self): return self.recordAccount

class Savings(DCRecordsManager):
    _shortName = 'sav'
    
    def __init__(self, account):
        super().__init__(account, True)

class Upfront(Repayment):
    dueSeason = 'month'
    dueTime = 1

class Upfronts(RepaymentsManager):
    _shortName = 'upf'
    recordClass = Upfront
    
    def __init__(self, accounts):
        super().__init__(accounts)
        
    def addUpfront(self, upfront):
        rate = self.account.rate
        maxDebit = rate * 30
        
        if (int(self.account.debits) + int(self) + upfront) > maxDebit: raise DCErrors.UpfrontsError(f'Client\'s debit can\'t be more than {maxDebit}')
        else:
            self.addRecord(upfront)
    @property
    def repaidUpfronts(self): return self.repaid
    @property
    def pendingdUpfronts(self): return self.outstanding
    








