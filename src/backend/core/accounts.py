from .date_time import DateTime, CompareByDate
from .bases import Mixins, Object, ObjectsManager
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

class Account(Object, CompareByDate):
    
    def __init__(self, manager, **kwargs):
        assert manager != None, 'No manager passed.'
        Object.__init__(self, manager, **kwargs)
    
    def __eq__(self, account):
        if account == None: return False
        return ((self.number == account.number) and super().__eq__(account) and self.manager is account.manager)
    
    def __getitem__(self, num): return self.recordsManagers[num]
    def __str__(self): return f'{self.manager} | {self.className}({self.date.dayMonthYear})'
    def __len__(self): return len(self.recordsManagers)
    
    @property
    def region(self): return self.manager.region
    
    @property
    def recordsManagers(self): self.notImp()
    
    @property
    def nextAccount(self): return self.next
    @property
    def previousAccount(self): return self.previous
    
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


class AccountsManager(ObjectsManager, Mixins):
    ObjectType = Account
    
    def __init__(self, region, autoAccount=True, **kwargs):
        
        ObjectsManager.__init__(self, region)
        self.addAccount = self.addSub
        self.createAccount = self.createSub
        
        if autoAccount == True: self.createAccount()
        
    def __eq__(self, manager):
        if manager == None: return False
        return self.region == manager.region
   
    def __str__(self):
        if self.region != None: return f'{self.region} | {self.className}'
        return f'{self.className}'
    
    @property
    def firstAccount(self): return self.first
    @property
    def lastAccount(self): return self.last
    
    @property
    def accounts(self): return self.subs
    @property
    def region(self): return self.master
   
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
        
    def getAccount(self, month): return self.getSub({'date-m': month})
    
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




