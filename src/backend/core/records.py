from .bases import Object, PRMP_DateTime, Errors
import datetime

# Record is the {money, date} recieved daily a.k.a DayRecord

class CoRecords(list):
    def __bool__(self): return True
    def addCoRecord(self, coRecord): self.append(coRecord)



class Record(Object):
    Manager = 'RecordsManager'
    _type = 'rec'
    subTypes = ['Co Records', 'Linked Records']

    def __init__(self, manager, money, note='Note', coRecord=None, **kwargs):
        self.money = money
        self.note = note
        self.__coRecord = coRecord
        self.__coRecords = None
        self.type = None

        Object.__init__(self, manager, name=note, **kwargs)


        if coRecord != None: coRecord.addCoRecord(self)
        else:
            self.__coRecords = CoRecords()
            self.addCoRecord(self)

        self.addEditableValues([{'value': 'money', 'type': int}, 'note', 'date'])

    def addCoRecord(self, coRecord):
        if coRecord in self.coRecords: return
        self.coRecords.addCoRecord(coRecord)

    def updateOtherCoRecord(self, other):
        for rec in self.__coRecords: rec.addCoRecord(self)

    def classInLinkedRecords(self, className): return className in [rec.className for rec in self]

    cilr = classInLinkedRecords

    def updateCoRecord(self):
        for rec in self.__coRecords: rec.updateOtherCoRecord(self)

    @property
    def subs(self): return self.linkedRecords or []

    @property
    def coRecord(self): return self.__coRecord

    @property
    def coRecords(self):
        if self.__coRecords != None: return self.__coRecords
        elif self.__coRecord != None: return self.__coRecord.coRecords

    @property
    def linkedRecords(self): return [c for c in self.coRecords if c is not self]

    def update(self, values={}, first=1):
        super().update(values)
        if first:
            for rec in self: rec.update(values, 0)
        self.manager.update()

    def __int__(self): return int(self.money)
    def __float__(self): return float(self.money)

    def __str__(self): return f'{self.manager} | {self.name}'

    def __repr__(self): return f'<{self.name}>'

    @property
    def name(self): return f'{self.className}({self.moneyWithSign}, {self.date.date}, {self.note})'

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
    ObjectType = None

    def __init__(self, manager, money, date=None, **kwargs):
        super().__init__(manager=manager, money=money, date=date, **kwargs)
        if self.duing: assert self.dueSeason and self.dueTime, 'Due Season and Time must be set.'

        if self.dueSeason == 'year': self.__dueDate = self.date + (self.dueTime * 12)
        elif self.dueSeason == 'month': self.__dueDate = self.date + self.dueTime
        elif self.dueSeason == 'day': self.__dueDate = self.date + datetime.timedelta(days=self.dueTime)

        if not self.ObjectType:
            from .records_managers import RecordsManager
            self.ObjectType = RecordsManager

        self.__repaymentsManager = self.ObjectType(self)

    def __getitem__(self, num): return self.repaymentsManager[num]

    def __len__(self): return len(self.repaymentsManager)

    @property
    def records(self): return self.repaymentsManager.records

    @property
    def isDue(self): return PRMP_DateTime.now() > self.dueDate

    @property
    def dueDate(self): return self.__dueDate

    @property
    def outstanding(self): return float(self) - self.repaid

    @property
    def paid(self): return float(self) == self.repaid

    @property
    def repaid(self): return float(self.repaymentsManager)

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

    @property
    def name(self): return f'{self.className}({self.moneyWithSign}, {self.date.date}, {self.note})'

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





