from ..core.records_managers import RecordsManager, DateTime, Repayment, RepaymentsManager, Loan, LoanBonds, LoanInterests, LoanBond, Record

from .coop_errors import CoopErrors

class CoopRecord(Record):
    Managers = ('Savings', )

class CoopRecordsManager(RecordsManager):
    Errors = CoopErrors
    Managers = ('UnitAccount', 'MemberAccount')
    ObjectType = CoopRecord
    
    
    def getMonthRecords(self, month): return self.sortRecordsIntoDaysInMonth(month)
    def getYearRecords(self, year): return self.sortRecordsByYear(year)

class CoopRepayment(Repayment):
    Managers = ('UnitAccount', 'MemberAccount')

class CoopRepaymentsManager(RepaymentsManager):
    Managers = ('UnitAccount', 'MemberAccount')
    
    @property
    def region(self): return self.account

class Expenses(CoopRecordsManager):
    pass

class Levies(CoopRepayment):
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
        return self.repaymentsManager.createRecord(repay, **kwargs)

class LoanInterest(CoopRepayment):
    duing = False
    
    def __init__(self, manager, interest, date, interestRate=None):
        if interestRate: self.__interestRate = interestRate
        
        super().__init__(manager, interest, date)
    
    @property
    def interestRate(self): return self.__interestRate

    def repayInterest(self, interest, **kwargs): return self.createRecord(interest, **kwargs)

class LoanInterests(CoopRepaymentsManager):
    ObjectType = LoanInterest
    
    def __init__(self, manager):
        super().__init__(manager)
        self.addLoanInterest(date=manager.date)
    
    def addLoanInterest(self, **kwargs):
        interestRate = self.loan.interestRate
        interest = self.loan.outstanding * interestRate
        self.createRecord(interest, interestRate=interestRate, **kwargs)
        
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
    LoanType = CoopLoan
    
    @property
    def unit(self): return self.manager.member.unit


class CoopLoanBonds(LoanBonds):
    ObjectType = CoopLoanBond
    
    @property
    def region(self): return self.manager


class Materials(CoopRepayment):
    duing = False

class Savings(CoopRecordsManager):
    
    def addSaving(self, savings, **kwargs): self.createRecord(savings, **kwargs)

class Shares(CoopRecordsManager):
    pass
