from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime, CompareByDate
from .bases import ObjectsMixins, Object, ObjectsManager
from .errors import Errors

# Account is the list of Records recieved for a month.
# AccountsManager is the manager of Accounts. It has a property 'accounts' which is a list of Accounts for the life time of the associated region.

# These serve as a container for the accounts for the period of season contained. They are given accounts by after being sorted by the AccountsManager.
# DailyAccounts comprises of the Accounts recieved and accounted for in a Day.
# WeeklyAccounts comprises of the DailyAccounts recieved and accounted for in a Week.
# MonthlyAccounts comprises of the DailyAccounts and WeeklyAccounts (as specified to the constructor) recieved and accounted for in a Month.
# YearlyAccounts comprises of the DailyAccounts,WeeklyAccounts and MonthlyAccounts (as specified to the constructor) recieved and accounted for in a Year.



class DailyAccounts(ObjectsMixins):
    #
    pass


class WeeklyAccounts(ObjectsMixins):

    def __init__(self, week, days_accounts, oneWeek=False):
        super().__init__()
        '''
        sort accounts into days in week.

        week: name of the week
        days_accounts: a list of accounts to be containing the accounts per day in the passed week.
        oneWeek: bool to parse the 
        '''
        self.week = week
        self.monday = [day for day in days_accounts if day.date.dayName == 'Monday']
        self.tuesday = [day for day in days_accounts if day.date.dayName == 'Tueday']
        self.wednesday = [day for day in days_accounts if day.date.dayName == 'Wednesday']
        self.thurday = [day for day in days_accounts if day.date.dayName == 'Thursday']
        self.friday = [day for day in days_accounts if day.date.dayName == 'Friday']
        self.saturday = [day for day in days_accounts if day.date.dayName == 'Saturday']
        self.sunday = [day for day in days_accounts if day.date.dayName == 'Sunday']

        for day in self.__dict__:
            if ('_' in day) or (not self.__dict__[day]):
                # if _ starts the key in self.__dict__ or key's value == [] or None
                continue

            if self.__dict__[day]:
                if oneWeek: # sums up the value of the day
                    self.__dict__[day] = self.__dict__[day][0]
                else: self.__dict__[day] = sum(self.__dict__[day])


class MonthlyAccounts(ObjectsMixins):
    def __init__(self, monthName, accounts, day=False):
        super().__init__()
        '''
        monthName: name of the month
        accounts: list of accounts to parse
        day: bool, whether to parse the accounts as [days in month, weeks in month]
        '''
        self.monthName = monthName
        self.day = day
        if day == False:
            self.week1 = [record for record in accounts if record.date.week == 1]
            self.week2 = [record for record in accounts if record.date.week == 2]
            self.week3 = [record for record in accounts if record.date.week == 3]
            self.week4 = [record for record in accounts if record.date.week == 4]
            self.week5 = [record for record in accounts if record.date.week == 5]
            self.others = [record for record in accounts if record not in [week1 + week2 + week3 + week4 + week5]]
        else:
            self.days = accounts.sort()


class YearlyAccounts(ObjectsMixins):
    pass

class MonthCompare:
    'compares the instances via their date.month'

    def __lt__(self, other):
        if other == None: return False
        return self.month < other.month
    def __le__(self, other):
        if other == None: return False
        return self.month <= other.month
    def __eq__(self, other):
        if other == None: return False
        return self.month is other.month
    def __ne__(self, other):
        if other == None: return True
        return self.month != other.month
    def __gt__(self, other):
        if other == None: return True
        return self.month > other.month
    def __ge__(self, other):
        if other == None: return True
        return self.month >= other.month

class Account(MonthCompare, Object):
    Manager = 'AccountsManager'
    subTypes = ['Records Managers']
    Error = Errors

    def __init__(self, manager, **kwargs):
        '''
        manager: an object to act as the manager
        kwargs: options to pass to the constructor of class Object
        '''
        assert manager != None, 'No manager passed.'
        Object.__init__(self, manager, **kwargs)

    def __eq__(self, account):
        if account == None: return False
        try: res = ((self.number == account.number) and super().__eq__(account) and self.manager is account.manager)
        except AttributeError: return False

    def __str__(self): return f'{self.manager} | {self.name}'
    def __len__(self): return len(self.recordsManagers)
    def __int__(self): return self.balances

    @property
    def name(self): return f'{self.className}({self.date.dayMonthYear})'

    @property
    def money(self): return float(self)

    @property
    def region(self): return self.manager.region

    @property
    def subs(self): return self.recordsManagers or []

    @property
    def recordsManagers(self): return []

    @property
    def headers(self): return [rec.className for rec in self.recordsManagers]

    @property
    def nextAccount(self): return self.next
    @property
    def previousAccount(self): return self.previous

    @property
    def recordsManagersAsList(self): return [float(recordsManager) for recordsManager in self]
    @property
    def recordsManagersAsTupleFull(self): return [(recordsManager, float(recordsManager)) for recordsManager in self]
    @property
    def recordsManagersAsTupleShort(self): return [(recordsManager.shortName, float(recordsManager)) for recordsManager in self]
    @property
    def recordsManagersAsTuple(self): return [(recordsManager.className, float(recordsManager)) for recordsManager in self]
    @property
    def recordsManagersAsDict(self): return [{recordsManager.className: float(recordsManager)} for recordsManager in self]
    @property
    def recordsManagersAsDictFull(self): return [{recordsManager: float(recordsManager)} for recordsManager in self]
    @property
    def recordsManagersAsDictShort(self): return [{recordsManager.shortName: float(recordsManager)} for recordsManager in self]

    def _balanceAccount(self):
            pass
    def balanceAccount(self): self.notImp()


class AccountsManager(ObjectsManager):
    ObjectType = Account
    subTypes = ['Accounts']

    def __init__(self, region, autoAccount=True, **kwargs):
        'region: same as [manager, master]'
        ObjectsManager.__init__(self, region)

        self.addAccount = self.addSub
        self.getAccount = self.getSub
        if autoAccount == True: self.createAccount(**kwargs)

    def __eq__(self, manager):
        if manager == None: return False
        return self.region == manager.region
    def __float__(self): return sum([float(acc.balances) for acc in self])
    def __int__(self): return sum([int(acc.balances) for acc in self])
    def __str__(self):
        if self.region != None: return f'{self.region} | {self.className}'
        return f'{self.className}'

    def createAccount(self, **kwargs):
        account =  self.createSub(**kwargs)
        return account

    @property
    def firstAccount(self): return self.first
    @property
    def lastAccount(self): return self.last

    @property
    def accounts(self): return self.subs

    @property
    def region(self): return self.master
    @property
    def name(self): return f'{self.region.name} | {self.className}'

    @property
    def headers(self): return self.lastAccount.headers

    @property
    def overAllAccounts(self):
        # total accounts in this manager
        lengthOfAccounts = len(self)
        if lengthOfAccounts:
            # total recordsManager in an account
            lengthOfRecordManagers = len(self[0])
            containerDict = {}
            for account in self:
                for recordManager in account:
                    name = recordManager.className
                    if name not in containerDict: containerDict[name] = 0
                    containerDict[name] += float(recordManager)
            return containerDict

    def balanceAccount(self, month=None):
        if month:
            account = self.getAccount(month=self.getDate(month))
            if account: account.balanceAccount()
        else:
            account = self.getLastAccount()
            if account: account.balanceAccount()
        return account

    def balanceAccounts(self):
        for accounts in self: accounts.balanceAccount()
        return self.accounts

    def currentMonthAccounts(self): return self.sortAccountsByMonth(PRMP_DateTime.now())

    def sortSubRegionsAccountsByMonth(self, month):
        PRMP_DateTime.checkDateTime(month)
        subRegionsActiveByMonth = self.region.subRegionsActiveByMonth(month)

        accounts = []
        for subRegion in subRegionsActiveByMonth:
            subRegionsAccounts = subRegion.sortAccountsByMonth(month) or []
            accounts.extend(subRegionsAccounts)
        return accounts

    def subRegionsActiveByMonth(self, month):
        subRegions = []
        for subRegion in self.region.subRegionsManager:
            monthAccount = subRegion.accountsManager.getAccount(month=month)
            if monthAccount != None: subRegions.append(subRegion)
        # or Subs = [Sub for Sub in self.Subs if Sub.lastAccount.date.isSameMonth(month)]

        return subRegions

    def sortSubsByMonth(self, month): return [sub for sub in self if sub.month.isSameMonthYear(month)]


   #Month Sorting
    def sortSubsAccountsByMonth(self, month):
        PRMP_DateTime.checkDateTime(month)
        Subs = self.subRegionsActiveByMonth(month)
        accounts = []
        for Sub in Subs:
            SubAccounts = Sub.accountsManager.sortSubsByMonth(month)
            accounts.extend(SubAccounts)
        return accounts


class SameTimesAccounts(ObjectsMixins):

    def __init__(self, obj):
        self.obj = obj
        self.subs = []

    def setStage(self):
        pass










