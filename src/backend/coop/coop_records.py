from ..core.records import RecordsManager, DateTime, Repayment, RepaymentsManager, Loan, LoanBonds, LoanInterests, LoanBond

from .coop_errors import CoopErrors

class CoopRecordsManager(RecordsManager):
    Errors = CoopErrors
    'Able to list records in a particular season, able to total it too.'
    
    def getMonthRecords(self, month): return self.sortRecordsIntoDaysInMonth(month)
    def getYearRecords(self, year): return self.sortRecordsByYear(year)

class CoopRepaymentsManager(RepaymentsManager):
    
    @property
    def region(self): return self.account

class Expenses(CoopRecordsManager):
    pass

class Levies(Repayment):
    duing = False
    rate = 200
    
    def __init__(self, manager, money=0, date=None):
        super().__init__(manager, money=money, date=date)
    
    
    @property
    def reignMonths(self): return self.manager.region.reignMonths
    
    @property
    def _dues(self): return self.rate * self.reignMonths
    
    @property
    def outstanding(self):
        out = self._dues - self.repaid
        if out < 0: return 0
        return out
    
    @property
    def dues(self): return self.outstanding
    
    def deductFromSavings(self):
        outLevy = self.outstanding
        if outLevy:
            self.addLevy(outLevy)
            self.manager.savings.addSaving(-(outLevy))

    
    def addLevy(self, repay, **kwargs):
        if self.outstanding == 0: raise CoopErrors.LeviesError('No outstanding levy.')
        return self.repaymentsManager.addRecord(repay, **kwargs)

class LoanInterest(Repayment):
    duing = False
    
    def __init__(self, manager, interest, date, interestRate=None):
        if interestRate: self.__interestRate = interestRate
        
        super().__init__(manager, interest, date)
    
    @property
    def interestRate(self): return self.__interestRate

    def repayInterest(self, interest, **kwargs): return self.addRecord(interest, **kwargs)

class LoanInterests(CoopRepaymentsManager):
    recordClass = LoanInterest
    
    def __init__(self, manager):
        super().__init__(manager)
        self.addLoanInterest(date=manager.date)
    
    def addLoanInterest(self, **kwargs):
        interestRate = self.loan.interestRate
        interest = self.loan.outstanding * interestRate
        self.addRecord(interest, interestRate=interestRate, **kwargs)
        
    @property
    def loan(self): return self.account
    
    @property
    def paid(self):
        for interest in self:
            if not interest.paid: return False
        return True

class CoopLoan(Loan):
    dueSeason = 'year'
    dueTime = 11
    rate = 2
    

class CoopLoanBond(LoanBond):
    duing = False
    
    
    @property
    def unit(self): return self.manager.member.unit


class CoopLoanBonds(LoanBonds):
    recordClass = CoopLoanBond
    
    @property
    def region(self): return self.manager


class Materials(Repayment):
    duing = False

class Savings(CoopRecordsManager):
    
    def addSaving(self, savings, **kwargs): self.addRecord(savings, **kwargs)

class Shares(CoopRecordsManager):
    pass
