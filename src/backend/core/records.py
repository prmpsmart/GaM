from .bases import Object, DateTime, Errors
from datetime import timedelta

# Record is the {money, date} recieved daily a.k.a DayRecord


class Record(Object):
    Manager = 'RecordsManager'
    _type = 'rec'
    
    def __init__(self, manager, money, date=None, note='Note', **kwargs):
        Object.__init__(self, manager, **kwargs)
        self.money = money
        self.note = note
    
    def __int__(self): return self.money
    
    def __str__(self): return f'{self.manager} | {self.name}'

    def __repr__(self): return f'<{self.name}>'

    @property
    def name(self): return f'{self.className}({self.moneyWithSign}, {self.date}, {self.note})'

    @property
    def region(self): return self.manager.region
    
    def set(self, money): self.money = money
    
    def add(self, money): self.money += money
    
    def substract(self, money): self.money -= money

DayRecord = Record


class Repayment(Record):
    dueSeason = ''
    dueTime = 0
    duing =  True
    Manager = 'RepaymentsManager'
    subTypes = ['Repayments']
    
    def __init__(self, manager, money, date=None, **kwargs):
        super().__init__(manager, money, date, **kwargs)
        
        if self.duing: assert self.dueSeason and self.dueTime, 'Due Season and Time must be set.'
        
        if self.dueSeason == 'year': self.__dueDate = self.date + (self.dueTime * 12)
        elif self.dueSeason == 'month': self.__dueDate = self.date + self.dueTime
        elif self.dueSeason == 'day': self.__dueDate = self.date + timedelta(days=self.dueTime)
        
        from .records_managers import RecordsManager
        
        self.__repaymentsManager = RecordsManager(self)
    
    def __getitem__(self, num): return self.repaymentsManager[num]
    
    def __len__(self): return len(self.repaymentsManager)
    
    @property
    def records(self): return self.repaymentsManager.records
    
    @property
    def isDue(self): return DateTime.now() > self.dueDate
    
    @property
    def dueDate(self): return self.__dueDate
    
    @property
    def outstanding(self): return int(self) - self.repaid
    
    @property
    def paid(self): return int(self) == self.repaid
    
    @property
    def repaid(self): return int(self.repaymentsManager)
    
    @property
    def repayment(self): return self.repaid
    
    @property
    def repayments(self): return self.repaymentsManager
    
    @property
    def repaymentsManager(self): return self.__repaymentsManager
    
    def addRepayment(self, repay, **kwargs):
        if self.paid: raise Errors.RepaymentError(f'{self.className} is already repaid.')
        else:
            if self.outstanding < repay: raise Errors.RepaymentError(f'Outstanding repayments ({self.outstanding}) is less than the repayment given ({repay}).')
            else:
                repayment = self.repaymentsManager.createRecord(repay, **kwargs)
                if self.paid: self.completed()
                return repayment
    
    def completed(self): pass

class Salary(Record):
    pass

class Loan(Repayment):
    dueSeason = 'year'
    dueTime = 11
    rate = 2
    Manager = 'LoanBond'
    
    def __init__(self, loanBond, interestRate=.1, dueTime=None, **kwargs):
        if dueTime: self.dueTime = dueTime
        from .records_managers import LoanInterests
        
        super().__init__(loanBond, loanBond.proposedLoan, **kwargs)
        
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
        if self.paid: raise Errors.LoanRepaymentsError('Loan is already repaid.')
        #  pay interest accordingly first
        else: pass
    
    def addDoubleInterest(self, date=None):
        if self.isDue:
            doubleInterest = self.outstanding * .2
            self.loanInterestsManager.addLoanInterest(doubleInterest, date)

class LoanBond(Repayment):
    duing = False
    LoanType = Loan
    Manager = 'LoanBonds'
    
    def __init__(self, manager, money, proposedLoan, **kwargs):
        super().__init__(manager, money, **kwargs)
        
        validLoan = manager.validLoan
        assert validLoan >= proposedLoan, f'Loan {proposedLoan} exceed maximum valid loan of {validLoan}.'
        
        self.grantedDate = None
        self.proposedLoan = proposedLoan
        self.details = None
        self.loan = None
    
    def addLoanRepayment(self, money, **kwargs):
        if self.granted: return self.loan.addRepayment(money, **kwargs)
        else: raise Errors.LoanRepaymentsError("Not yet granted. There's no loan to repay.")
    
    @property
    def outstandingLoan(self): return self.loan.outstanding if self.loan else 0
    
    @property
    def granted(self):
        if self.paid and self.loan: return True
        return False
    
    @property
    def paidLoan(self): return self.loan.paid
    
    @property
    def filledLoanBond(self):
        if self.details: return True
        else: return False
    
    def completed(self):
        pass
    
    def fillLoanBond(self, ):
        pass
    
    def grant(self, interestRate=.1, dueTime=None, date=None): self.loan = self.LoanType(self, date=date, interestRate=interestRate, dueTime=dueTime)

class LoanInterest(Repayment):
    duing = False
    Manager = 'LoanInterests'
    
    def __init__(self, manager, interest, interestRate=None, **kwargs):
        if interestRate: self.__interestRate = interestRate
        
        super().__init__(manager, interest, **kwargs)
    
    @property
    def interestRate(self): return self.__interestRate

    def repayInterest(self, interest, **kwargs): return self.createRecord(interest, **kwargs)





