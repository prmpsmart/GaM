
from .errors import Errors
from .date_time import DateTime, CompareByMonth, CompareByWeek, CompareByYear, DAYS_ABBRS, DAYS_NAMES, MONTHS_ABBRS, MONTHS_NAMES, timedelta
from .bases import ObjectsManager, Mixins
from .records import *

# RecordsManager is the manager of records. It has a property 'records' which is a list of Records

# These serve as a container for the records for the period of season contained. They are given records by after being sorted by the RecordsManager.

# DailyRecords comprises of the Records recieved and accounted for in a Day.
# WeeklyRecords comprises of the DailyRecords recieved and accounted for in a Week.
# MonthlyRecords comprises of the DailyRecords and WeeklyRecords (as specified to the constructor) recieved and accounted for in a Month.
# YearlyRecords comprises of the DailyRecords,WeeklyRecords and MonthlyRecords (as specified to the constructor) recieved and accounted for in a Year.


class SeasonRecord(Mixins):
    maximum = 0
    def __init__(self, records):
        assert records, 'Records cannot be empty.'
        if self.maximum: assert len(records) <= self.maximum, f'Records may not be more than {self.maximum}'
        
        man = records[0].manager
        for rec in records:
            assert rec.manager == man, 'Records of different managers given.'
        
        self.__records = records
        self.__records.sort()
    
    def __int__(self): return sum([int(rec) for rec in self])
    
    def __getitem__(self, num): return self.records[num]
    
    def __len__(self): return len(self.records)
    
    @property
    def manager(self): return self.records[0].manager
    
    @property
    def date(self): return self.records[0].date
    
    @property
    def records(self): return self.__records
    
    def get(self, season, wh):
        if season == 'year':
            for rec in self:
                if wh == rec.year: return rec
        elif season == 'month':
            for rec in self:
                if wh == rec.month: return rec
        elif season == 'day':
            for rec in self:
                if wh == rec.day: return rec

class WeekRecord(SeasonRecord, CompareByWeek):
    maximum = 7
    
    def __init__(self, records):
        super().__init__(records)
        self.recDayNames = [rec.date.dayName for rec in records]
    
    def __str__(self): return f'{self.manager} | {self.className}({self.weekMonthYear}) | {self.moneyWithSign}'

    def __day(self, name):
        if name in self.recDayNames:
            for rec in self:
                if name.title() == rec.date.dayName: return rec
    @property
    def sunday(self): return self.__day('Sunday')
    @property
    def monday(self): return self.__day('Monday')
    @property
    def tuesday(self): return self.__day('Tuesday')
    @property
    def wednesday(self): return self.__day('Wednesday')
    @property
    def thursday(self): return self.__day('Thursday')
    @property
    def friday(self): return self.__day('Friday')
    @property
    def saturday(self): return self.__day('Saturday')

class MonthRecord(SeasonRecord, CompareByMonth):
    maximum = 5
    
    def __init__(self, records, weeks=False):
        super().__init__(records)
        self.__weeks = []
        self.__sorted = False
        if weeks: self.sortRecordsIntoWeeks()
    
    def __str__(self): return f'{self.manager} | {self.className}({self.monthYear}) | {self.moneyWithSign}'
    
    def sortRecordsIntoWeeks(self):
        if self.__sorted: return self
        daysRec = [record for record in self if record.date.isSameMonth(self.date)]
        weeks = DateTime.monthYearOfMonthWeekDays(dateObj=self.date)
        week1 = []
        week2 = []
        week3 = []
        week4 = []
        week5 = []
        for dayRec in daysRec:
            if dayRec.date.monthYear in weeks[0]: week1.append(dayRec)
            elif dayRec.date.monthYear in weeks[1]: week2.append(dayRec)
            elif dayRec.date.monthYear in weeks[2]: week3.append(dayRec)
            elif dayRec.date.monthYear in weeks[3]: week4.append(dayRec)
            elif dayRec.date.monthYear in weeks[4]: week5.append(dayRec)
        
        self.__weeks = [WeekRecord(week1), WeekRecord(week2),  WeekRecord(week3),  WeekRecord(week4),  WeekRecord(week5)]
        self.__sorted = True
        return self
    
    @property
    def __week(self, num):
        try: return self.__weeks[num]
        except: pass
    @property
    def week1(self): return self.__week(0)
    @property
    def week2(self): return self.__week(1)
    @property
    def week3(self): return self.__week(2)
    @property
    def week4(self): return self.__week(3)
    @property
    def week5(self): return self.__week(4)

class YearRecord(SeasonRecord, CompareByYear):
    maximum = 12
    
    def __init__(self, records, months=False):
        super().__init__(records)
        self.__months = []
        if months: self.recMonthNames = [rec.date.monthName for rec in records]
    
    def __str__(self): return f'{self.manager} | {self.className}({self.year}) | {self.moneyWithSign}'
    
    def sortRecordsIntoMonths(self):
        jan = []
        feb = []
        mar = []
        apr = []
        may = []
        jun = []
        jul = []
        aug = []
        sep = []
        octo = []
        nov = []
        dec = []
        
        for rec in self:
            if rec.monthName == MONTHS_NAMES[1]: jan.append(rec)
            elif rec.monthName == MONTHS_NAMES[2]: feb.append(rec)
            elif rec.monthName == MONTHS_NAMES[3]: mar.append(rec)
            elif rec.monthName == MONTHS_NAMES[4]: apr.append(rec)
            elif rec.monthName == MONTHS_NAMES[5]: may.append(rec)
            elif rec.monthName == MONTHS_NAMES[6]: jun.append(rec)
            elif rec.monthName == MONTHS_NAMES[7]: jul.append(rec)
            elif rec.monthName == MONTHS_NAMES[8]: aug.append(rec)
            elif rec.monthName == MONTHS_NAMES[9]: sep.append(rec)
            elif rec.monthName == MONTHS_NAMES[10]: octo.append(rec)
            elif rec.monthName == MONTHS_NAMES[11]: nov.append(rec)
            elif rec.monthName == MONTHS_NAMES[12]: dec.append(rec)
            
        self.__months = [MonthRecord(jan), MonthRecord(mar), MonthRecord(feb), MonthRecord(apr), MonthRecord(may), MonthRecord(jun), MonthRecord(jul), MonthRecord(aug), MonthRecord(sep), MonthRecord(octo), MonthRecord(nov), MonthRecord(dec)]
        self.recMonthNames = [rec.date.monthName for rec in self.__months]
    
    def __year(self, monthName):
        try:
            if monthName in self.recMonthNames:
                for rec in self.__months:
                    if monthName == rec.date.monthName: return rec
        except: pass
        
    @property
    def months(self): return self.__months
    @property
    def january(self): return self.__year(MONTHS_NAMES[1])
    @property
    def february(self): return self.__year(MONTHS_NAMES[2])
    @property
    def march(self): return self.__year(MONTHS_NAMES[3])
    @property
    def april(self): return self.__year(MONTHS_NAMES[4])
    @property
    def may(self): return self.__year(MONTHS_NAMES[5])
    @property
    def june(self): return self.__year(MONTHS_NAMES[6])
    @property
    def july(self): return self.__year(MONTHS_NAMES[7])
    @property
    def august(self): return self.__year(MONTHS_NAMES[8])
    @property
    def september(self): return self.__year(MONTHS_NAMES[9])
    @property
    def october(self): return self.__year(MONTHS_NAMES[10])
    @property
    def november(self): return self.__year(MONTHS_NAMES[11])
    @property
    def december(self): return self.__year(MONTHS_NAMES[12])

class RecordsWithSameSeasons(SeasonRecord):
    
    def __init__(self, records, name):
        super().__init__(records)
        self.__class__.__name__ = name
    
    def __str__(self): return f'{self.manager} | {self.className}s | {self.moneyWithSign}'

class RecordsManager(ObjectsManager):
    _shortName = 'rec'
    lowest = 50
    ObjectType = Record
    _type = 'recm'
    
    def __init__(self, account=None): ObjectsManager.__init__(self, account)
    
    def __int__(self): return self.totalMonies
    
    def __str__(self): return f'{self.account} | {self.name}'
    
    def __len__(self): return len(self.records)

    def name(self): return f'{self.className}({self.moneyWithSign})'

    @property
    def date(self): return self.account.date
    
    @property
    def name(self): return f'{self.className}({self.moneyWithSign})'

    @property
    def account(self): return self.master
    
    @property
    def region(self): return self.account.region
    
    @property
    def records(self): return self.subs
    
    @property
    def lastMoney(self): return int(self.lastRecord) if self.last else 0
    
    @property
    def lastRecord(self): return self.last
    
    @property
    def totalMonies(self): return sum([int(record) for record in self[:]])
    
    @property
    def recordDateTuples(self): return [(str(record.date), int(record)) for record in self]
    
    @property
    def dates(self): return [record.date for record in self]
    
    def _setRecords(self, records): self.__records = records
    
    def getRecordByDate(self, date): return self.sortRecordsByDate(date)
    
    def createRecord(self, money, date=None, newRecord=True,notAdd=False, **kwargs):
        '''
        money: type int; transaction to be in the record.
        date: type DateTime; date of the transaction.
        newRecord: type bool; whether to create a new record or (add/set) to a record already done
        notAdd: type bool; useful when param newRecord=False, it\'s whether to set the money to a transaction already made or not
        kwargs: further params that a ObjectType might need.
        '''
        money = int(money)
        new = False
        record = None
        
        # if money == 0: newRecord, notAdd = False, True
        
        # assert money != 0, 'Money must not be zero.'
        
        if date == None: date = DateTime.now()
        DateTime.checkDateTime(date)
        
        if newRecord: new = True
        else:
            if date in list(self.dates):
                new = False
                record = self.getRecordByDate(date)
                if record:
                    if notAdd: record.set(money)
                    else: record.add(money)
            else: new = True
            
        if new:
            record = self.createSub(money, date=date, **kwargs)
            self.records.sort()
        
        return record
        
    def updateWithOtherManagers(self, managers):
        self.deleteSubs()
        total = sum([int(manager) for manager in managers])
        self.createRecord(total, newRecord=False, notAdd=True)
    
    def removeRecord(self, date):
        for record in self:
            if record.date == date: self.records.remove(record)
            del record
            return
    
    def removeRecordByIndex(self, index):
        if len(self.records) >= index: del self.records[index]
    
    def checkMoney(self, money):
        if (money < self.lowest): raise ValueError(f'Amount of {money} is too small.')
        if (money % 5) != 0: raise ValueError(f'Amount of {money} is not valid.')
        return 1
    
    @property
    def recordsYears(self):
        years = []
        for rec in self:
            if rec.year in years: continue
            else: years.append(rec.year)
        return years
    
    
    @property
    def recordsAsList(self): return [int(record) for record in self]
    @property
    def recordsAsTupleFull(self): return [(record, int(record)) for record in self]
    @property
    def recordsAsTupleShort(self): return [(self.className, str(record.date), int(record)) for record in self]
    @property
    def recordsAsTuple(self): return [(str(record.date), int(record)) for record in self]
    @property
    def recordsAsDict(self): return [{str(record.date): int(record)} for record in self]
    @property
    def recordsAsDictFull(self): return [{record: int(record)} for record in self]
    @property
    def recordsAsDictShort(self): return [{str(record.date): int(record)} for record in self]

    ############ Sorting
    #Date Sorting
    
    def sortRecordsByDate(self, date):
        DateTime.checkDateTime(date)
        for record in self:
            if record.date == date: return record
    
    #Day Sorting
    def sortRecordsByDay(self, dayName):
        recs = [record for record in self if record.date.dayName == dayName]
        return RecordsWithSameSeasons(recs, dayName)
    
    def sortRecordsIntoDaysInWeek(self, week):
        DateTime.checkDateTime(week)
        days = [record for record in self if record.date.isSameWeek(week)]
        return WeekRecord(days)
    
    def sortRecordsIntoDaysInMonth(self, month):
        DateTime.checkDateTime(month)
        days = [record for record in self if record.date.isSameMonth(month)]
        return MonthRecord(days)
    
    #Week Sorting
    def sortRecordsByWeek(self, weekNum):
        DateTime.checkDateTime(date)
        records = []
        for record in self:
            if record.date.weekNum == int(weekNum): records.append(record)
        return WeekRecord(records)

    def sortRecordsIntoWeeksInMonth(self, month):
        daysRec = self.sortRecordsIntoDaysInMonth(month)
        weeksRec = daysRec.sortRecordsIntoWeeks()
        return weeksRec
    
    def sortRecordsIntoWeeksInYear(self): pass
    
    #Month Sorting
    def sortRecordsByMonth(self, month): return self.sortRecordsIntoDaysInMonth(month)
    
    def sortRecordsIntoMonthsInYear(self, year):
        DateTime.checkDateTime(year)
        yearRecs = [record for record in self if record.date.isSameYear(year)]
        year = YearRecord(yearRecs)
        year.sortRecordsIntoMonths()
        return year
    
    def sortRecordsIntoMonthsInYears(self):
        yearsRecs = YearRecord(self.records)
        yearsRecs.sortRecordsIntoMonths()
        return yearsRecs
    
    #Year Sorting
    def sortRecordsByYear(self, year):
        DateTime.checkDateTime(year)
        recs = [rec for rec in self if rec.date.isSameYear(year)]
        return YearRecord(recs)

    def sortRecordsIntoYears(self):
        years = self.recordsYears
        yearsRecs = [self.sortRecordsByYear(DateTime.creatDateTime(year=year)) for year in years]
        
        return SeasonRecord(yearsRecs)

class RepaymentsManager(RecordsManager):
    ObjectType = Repayment
    
    @property
    def paid(self):
        for repay in self[:]:
            if repay and (not repay.paid): return False
        return True
    
    @property
    def outstanding(self):
        out = 0
        for record in self:
            if record: out += record.outstanding
        return out
    
    @property
    def repaid(self):
        rep = 0
        for record in self: rep += record.repaid
        return rep
    
    def updateWithOtherManagers(self, managers):
        self.subs = managers
        
    def addRepayment(self, repay, **kwargs):
        outs = self.outstanding
        if repay > outs: raise Errors.RepaymentError(f'Repay of {repay} is > Outstanding of {outs} ')
        rem_outs = repay
        for rep in self:
            if rem_outs:
                if not rep.paid:
                    if repay > rep.outstanding:
                        rem_outs = repay - rep.outstanding
                        rep.addRepayment(rep.outstanding, **kwargs)
                    else:
                        rep.addRepayment(rem_outs, **kwargs)
                    rem_outs = 0

class SalariesManager(RecordsManager):
    ObjectType = Salary
    def person(self): return self.account
    def addSalary(self, salary, date=None): return self.createRecord(salary, date=date)

class LoanInterests(RepaymentsManager):
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

class LoanBonds(RepaymentsManager):
    ObjectType = LoanBond
    
    @property
    def validLoan(self): return self.account.validLoan

    def newLoanBond(self, money, proposedLoan, **kwargs):
        last = self.lastRecord
        go = 1
        if last:
            outstandingLoan = last.outstandingLoan
            
            if last.paid and last.granted:
                if last.paidLoan: pass
                elif outstandingLoan: raise Errors.LoanBondsError(f'There is a paid loan bond with an outstanding loan ({outstandingLoan}).')
            elif not last.granted: raise Errors.LoanBondsError('There is a paid loan bond with a pending loan.')
            else: raise Errors.LoanBondsError('There is an outstanding loan bond not yet paid.')
            
        loanBond = self.createRecord(money,  proposedLoan=proposedLoan, **kwargs)
        return loanBond






