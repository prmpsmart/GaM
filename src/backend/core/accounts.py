from .date_time import DateTime, CompareByDate, Mixins
from .errors import Errors

# Account is the list of Records recieved for a month.
# AccountsManager is the manager of Accounts. It has a property 'accounts' which is a list of Accounts for the life time of the associated region.

# These serve as a container for the accounts for the period of season contained. They are given accounts by after being sorted by the AccountsManager.
# DailyAccounts comprises of the Accounts recieved and accounted for in a Day.
# WeeklyAccounts comprises of the DailyAccounts recieved and accounted for in a Week.
# MonthlyAccounts comprises of the DailyAccounts and WeeklyAccounts (as specified to the constructor) recieved and accounted for in a Month.
# YearlyAccounts comprises of the DailyAccounts,WeeklyAccounts and MonthlyAccounts (as specified to the constructor) recieved and accounted for in a Year.



class DailyAccounts(Mixins):
    # 
    pass

class WeeklyAccounts(Mixins):
    
    def __init__(self, week, days_accounts, oneWeek=False):
        self.week = week
        self.monday = [day for day in days_accounts if day.date.dayName == 'Monday']
        self.tuesday = [day for day in days_accounts if day.date.dayName == 'Tueday']
        self.wednesday = [day for day in days_accounts if day.date.dayName == 'Wednesday']
        self.thurday = [day for day in days_accounts if day.date.dayName == 'Thursday']
        self.friday = [day for day in days_accounts if day.date.dayName == 'Friday']
        self.saturday = [day for day in days_accounts if day.date.dayName == 'Saturday']
        self.sunday = [day for day in days_accounts if day.date.dayName == 'Sunday']
        
        for day in self.__dict__:
            if '_' in day: continue
            if not self.__dict__[day]: continue
            if self.__dict__[day]:
                if oneWeek: self.__dict__[day] = self.__dict__[day][0]
                else: self.__dict__[day] = sum(self.__dict__[day])

class MonthlyAccounts(Mixins):
    def __init__(self, monthName, accounts, day=False):
        self.monthName = monthName
        if day == False:
            self.week1 = [record for record in accounts if record.date.week == 1]
            self.week2 = [record for record in accounts if record.date.week == 2]
            self.week3 = [record for record in accounts if record.date.week == 3]
            self.week4 = [record for record in accounts if record.date.week == 4]
            self.week5 = [record for record in accounts if record.date.week == 5]
            self.others = [record for record in accounts if record not in [week1 + week2 + week3 + week4 + week5]]
        else:
            self.days = accounts.sort()

class YearlyAccounts(Mixins):
    pass

class Account(CompareByDate):
    
    def __init__(self, manager=None, date=None, previous=None, number=0, **kwargs):
        assert manager != None, 'No manager passed.'
        self.__manager = manager
        if date == None: date = DateTime.now()
        DateTime.checkDateTime(date)
        self.__date = date
        self.__nextAccount = None
        self.__previousAccount = previous
        self.__number = number
        
    def __eq__(self, account):
        if account == None: return False
        return ((self.number == account.number) and super().__eq__(account) and self.manager is account.manager)
    
    def __getitem__(self, num): return self.recordsManagers[num]
    def __str__(self): return f'{self.manager} | {self.className}({self.date.dayMonthYear})'
    def __len__(self): return len(self.recordsManagers)
    @property
    def region(self): return self.manager.region
    @property
    def number(self): return self.__number
    @property
    def recordsManagers(self): self.notImp()
    @property
    def date(self): return self.__date
    @property
    def nextAccount(self): return self.__nextAccount
    @nextAccount.setter
    def nextAccount(self, account):
        if self.__nextAccount == None: self.__nextAccount = account
        else: raise Errors.AccountError('A next account is already set.')
    
    @property
    def previousAccount(self): return self.__previousAccount
    
    @property
    def manager(self): return self.__manager
    
    @property
    def recordsManagersAsList(self): return [int(recordsManager) for recordsManager in self]
    @property
    def recordsManagersAsTupleFull(self): return [(recordsManager, int(recordsManager)) for recordsManager in self]
    @property
    def recordsManagersAsTupleShort(self): return [(recordsManager.shortName, int(recordsManager)) for recordsManager in self]
    @property
    def recordsManagersAsTuple(self): return [(recordsManager.className, int(recordsManager)) for recordsManager in self]
    @property
    def recordsManagersAsDict(self): return [{recordsManager.className: int(recordsManager)} for recordsManager in self]
    @property
    def recordsManagersAsDictFull(self): return [{recordsManager: int(recordsManager)} for recordsManager in self]
    @property
    def recordsManagersAsDictShort(self): return [{recordsManager.shortName: int(recordsManager)} for recordsManager in self]

    def _balanceAccount(self):
            pass
    def balanceAccount(self): self.notImp()
    
    
   
   ########## Sorting
    #Date Sorting
    def sortRecordManagersByDate(self, date): pass
    
    #Day Sorting
    def sortRecordManagersByDay(self, day): pass
    
    def sortRecordManagersIntoDaysInWeek(self, week):
        pass
    def sortRecordManagersIntoDaysInMonth(self, month):
        pass
    
    #Week Sorting
    def sortRecordManagersByWeek(self):
        pass
    def sortRecordManagersIntoWeeksInMonth(self):
        pass
    def sortRecordManagersIntoWeeksInYear(self):
        pass
    
    #Month Sorting
    def sortRecordManagersByMonth(self, month): pass
        
    def sortRecordManagersIntoMonthsInYear(self):
        pass
    def sortRecordManagersIntoMonthsInYears(self):
        pass
    
    #Year Sorting
    def sortRecordManagersByYear(self):
        pass
    def sortRecordManagersIntoYears(self):
        pass


class AccountsManager(Mixins):
    accountClass = Account
    
    def __init__(self, region, autoAccount=True, **kwargs):
        self.__region = region
        self.__accounts = []
        
        if autoAccount == True: self.createAccount(auto=True, **kwargs)
    def __eq__(self, manager):
        if manager == None: return False
        return self.region == manager.region
    
    def __getitem__(self, num): return self.accounts[num]
    def __len__(self): return len(self.accounts)
    def __str__(self):
        if self.region != None: return f'{self.region} | {self.className}'
        return f'{self.className}'
    
    @property
    def accounts(self): return self.__accounts
    @property
    def region(self): return self.__region
   
    @property
    def firstAccount(self):
        if len(self):
            self.accounts.sort()
            firstAccount_ = self[-1]
            assert firstAccount_.previousAccount == None, f'This account {self} is not the first account'
            return firstAccount_
        
    @property
    def lastAccount(self):
        if len(self):
            self.accounts.sort()
            lastAccount_ = self[-1]
            assert lastAccount_.nextAccount == None, f'This account {self} is not the last account'
            return lastAccount_
    
    @property
    def overAllAccounts(self):
        listOfTuple = []
        lengthOfAccounts = len(self)
        if len(self):
            gone = False
            lengthOfRecordManagers = len(self[0])
            listOfTuple = [['', 0] for _ in (range(lengthOfRecordManagers))]
            for account in self:
                for recordManager in account:
                    index = account[:].index(recordManager)
                    if gone: assert listOfTuple[index][0] == recordManager.className
                    else: listOfTuple[index][0] = recordManager.className
                    listOfTuple[index][1] += int(recordManager)
                gone = True
                
            return listOfTuple

    def addAccount(self, account):
        self.__accounts.append(account)
        self.__lastAccount = account
        
    def createAccount(self, date=None, auto=True, **kwargs):
        if (DateTime.checkDateTime(date, dontRaise=True) == False) and (auto == True): date = DateTime.createDateTime(auto=auto)
        lastAccount = self.lastAccount
        account = self.accountClass(manager=self, date=date, previous=lastAccount, number=len(self), **kwargs)
        if lastAccount: lastAccount.nextAccount = account
        self.addAccount(account)
        return account
    
    def getAccount(self, month):
        if len(self):
            for account in self:
                if account.date.isSameMonth(month): return account
    
    def balanceAccount(self, month=None):
        if month:
            DateTime.checkDateTime(month)
            account = self.getAccount(month)
            if account: account.balanceAccount()
        else:
            account = self.getLastAccount()
            if account: account.balanceAccount()
        return account
    
    def balanceAccounts(self):
        for accounts in self: accounts.balanceAccount()
        return self.accounts
    
    def currentMonthAccounts(self): return self.sortAccountsByMonth(DateTime.now())
    
    def sortSubRegionsAccountsByMonth(self, month):
        DateTime.checkDateTime(month)
        subRegionsActiveByMonth = self.region.subRegionsActiveByMonth(month)
        accounts = []
        for subRegion in subRegionsActiveByMonth:
            subRegionsAccounts = subRegion.sortAccountsByMonth(month)
            accounts.extend(subRegionsAccounts)
        return accounts
    
    
 ########## Sorting
  # SubRegions
   #Date Sorting
    def sortAccountsByDate(self, date):
        DateTime.checkDateTime(date)
        clientsByDate = [client for client in self.clients if client.regDate == date]
        return clientsByDate
   #Day Sorting
    def sortAccountsByDay(self):
        pass
    def sortAccountsIntoDaysInWeek(self):
        pass
    def sortAccountsIntoDaysInMonth(self):
        pass
    
   #Week Sorting
    def sortAccountsByWeek(self):
        pass
    def sortAccountsIntoWeeksInMonth(self):
        pass
    def sortAccountsIntoWeeksInYear(self):
        pass
    
   #Month Sorting
    def sortAccountsByMonth(self, month):
        accounts = [account for account in self.accounts if account.date.isSameMonth(month)]
        return accounts
    def sortAccountsIntoMonthsInYear(self):
        pass
    def sortAccountsIntoMonthsInYears(self):
        pass
    
   #Year Sorting
    def sortAccountsByYear(self):
        pass
    def sortAccountsIntoYears(self):
        pass

  # Accounts Accounts
   #Date Sorting
    def sortAccountsAccountsByDate(self):
        pass

   #Day Sorting
    def sortAccountsAccountsByDay(self):
        pass
    def sortAccountsAccountsIntoDaysInWeek(self):
        pass
    def sortAccountsAccountsIntoDaysInMonth(self):
        pass
    
   #Week Sorting
    def sortAccountsAccountsByWeek(self):
        pass
    def sortAccountsAccountsIntoWeeksInMonth(self):
        pass
    def sortAccountsAccountsIntoWeeksInYear(self):
        pass
    
   #Month Sorting
    def sortAccountsAccountsByMonth(self, month):
        DateTime.checkDateTime(month)
        clients = [client for client in self.clients if client.lastAccount.date.isSameMonth(month)]
        accounts = []
        for client in clients:
            clientAccounts = client.accountsManager.sortAccountsByMonth(month)
            accounts.extend(clientAccounts)
        return accounts
        
    def sortAccountsAccountsIntoMonthsInYear(self):
        pass
    def sortAccountsAccountsIntoMonthsInYears(self):
        pass
    
   #Year Sorting
    def sortAccountsAccountsByYear(self):
        pass
    def sortAccountsAccountsIntoYears(self):
        pass




