from ..core.records import RecordsManager, DateTime, Repayment, RepaymentsManager
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

    
    def addLevy(self, repay, date=None):
        if self.outstanding == 0: raise CoopErrors.LeviesError('No outstanding levy.')
        return self.repaymentsManager.addRecord(repay, date=date)

class LoanInterest(Repayment):
    duing = False
    
    def __init__(self, manager, interest, date, interestRate=None):
        if interestRate: self.__interestRate = interestRate
        
        super().__init__(manager, interest, date)
    
    @property
    def interestRate(self): return self.__interestRate

    def repayInterest(self, interest):
        self.addRecord

class LoanInterests(CoopRepaymentsManager):
    recordClass = LoanInterest
    
    def __init__(self, manager):
        super().__init__(manager)
        
        self.addLoanInterest(manager.date)
    
    def addLoanInterest(self, date=None):
        interestRate = self.loan.interestRate
        interest = self.loan.outstanding * interestRate
        self.addRecord(interest, date=date, interestRate=interestRate)
        
    @property
    def loan(self): return self.account
    @property
    def paid(self):
        for interest in self:
            if not interest.paid: return False
        return True

class Loan(Repayment):
    dueSeason = 'month'
    dueTime = 11
    rate = 2
    
    def __init__(self, loanBond, date, interestRate=.1, dueTime=None):
        if dueTime: self.dueTime = dueTime
        
        super().__init__(loanBond, loanBond.proposedLoan, date)
        
        self.__interestRate = interestRate
        self.__loanInterests = LoanInterests(self)
    
    def __str__(self):
        st = super().__str__()
        st = st.split('|')
        del st[-3]
        return '|'.join(st)
        

    @property
    def loanBond(self): return self.manager
    @property
    def interestRate(self): return self.__interestRate
    @property
    def loanInterests(self): return self.__loanInterests
    @property
    def paidInterests(self): return self.loanInterests.paid
    
    def repayInterest(self, repay):
        assert repay > 0, 'Repay must be more than zero (0).'
        if self.paid: raise CoopErrors.LoanRepaymentsError('Loan is already repaid.')
        #  pay interest accordingly first
        else: pass
    
    def addDoubleInterest(self, date=None):
        if self.isDue:
            doubleInterest = self.outstanding / 10 * 2
            self.loanInterestsManager.addLoanInterest(doubleInterest, date)

class LoanBond(Repayment):
    duing = False
    
    def __init__(self, manager, money, proposedLoan, date=None):
        super().__init__(manager, money, date)
        
        validLoan = manager.validLoan
        assert validLoan >= proposedLoan, f'Loan {proposedLoan} exceed maximum valid loan of {validLoan}.'
        
        self.__grantedDate = None
        self.__proposedLoan = proposedLoan
        self.__details = None
        self.__loan = None
    
    @property
    def unit(self): return self.manager.member.unit
    
    @property
    def proposedLoan(self): return self.__proposedLoan
    
    @property
    def loan(self): return self.__loan
    
    def addLoanRepayment(self, money, date=None):
        if self.loan: return self.loan.addRepayment(money, date)
    
    @property
    def outstandingLoan(self): return self.loan.outstanding if self.loan else 0
    
    @property
    def grantedDate(self): return self.__grantedDate
    
    @property
    def granted(self):
        if self.paid and self.loan: return True
        return False
    
    @property
    def paidLoan(self): return self.loan.paid
    
    @property
    def details(self): return self.__details
    
    @property
    def filledLoanBond(self):
        if self.details: return True
        else: return False
    
    def completed(self):
        pass
    
    def fillLoanBond(self, ):
        pass
    
    def grant(self, interestRate=.1, dueTime=None, date=None):
        if date == None: date = DateTime.now()
        DateTime.checkDateTime(date)
        self.__loan = Loan(self, date, interestRate=interestRate, dueTime=dueTime)

class LoanBonds(CoopRepaymentsManager):
    recordClass = LoanBond
    
    @property
    def validLoan(self): return self.region.validLoan
    
    def newLoanBond(self, money, proposedLoan, date=None):
        last = self.lastRecord
        go = 1
        if last:
            outstandingLoan = last.outstandingLoan
            
            if last.granted:
                if last.paidLoan: pass
                elif outstandingLoan: raise CoopErrors.LoanBondsError(f'There is a paid loan bond with an outstanding loan ({outstandingLoan}).')
            elif last.paid: raise CoopErrors.LoanBondsError('There is a paid loan bond with an pending loan.')
            else: raise CoopErrors.LoanBondsError('There is an outstanding loan bond.')
            
        loanBond = self.addRecord(money, date, proposedLoan=proposedLoan)
        return loanBond

class Materials(Repayment):
    duing = False

class Savings(CoopRecordsManager):
    
    def addSaving(self, savings, date=None): self.addRecord(savings, date)

class Shares(CoopRecordsManager):
    pass
