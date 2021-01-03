from ..core.bases import Object, ObjectsManager, PRMP_DateTime, ObjectSort

class ContribContainer(Object):
    Manager = 'Daily_Contribution'
    
    def __init__(self, manager, account=None, **kwargs):
        super().__init__(manager, **kwargs)

        self.account = account
        self._subs = []
    
    @property
    def subs(self): return self._subs
    
    @property
    def name(self): return f'{self.manager} | {self.className}({self.date}) '
    
    def __eq__(self, other):
        if other == None: return False
        return (self.manager is other.manager) and (self.date is other.date)

    @property
    def contrib(self): return self.account.contributions

    @property
    def region(self): return self.manager.region


class Daily_Contribution(ObjectsManager):
    Manager = 'Daily_Contributions'
    ObjectType = ContribContainer
    MultipleSubsPerMonth = True
    
    def __init__(self, manager, date=None, previous=None, number=0):
        super().__init__(manager)

        self._date = date
        self.previous = previous
        self.number = number
        self.next = None
    
    @property
    def manager(self): return self.master
    
    @property
    def name(self): return f'{self.manager} | {self.className}({self.date.date})'
    
    def __eq__(self, other):
        if other == None: return False
        return (self.manager is other.manager) and (self.date is other.date)

    @property
    def region(self): return self.manager.region

    
    def creatfeSub(self, number, month=None, date=None):
        
        if date == None: date = PRMP_DateTime.now()
        PRMP_DateTime.checkDateTime(date)
        
        date_validations = [dict(value=True, attr='date', attrMethod='isSameDate', attrMethodParams=[date])]

        prevs = self.objectSort.sort(validations=date_validations)

        if len(prevs): raise ValueError(f'Daily_Contribution({date.date}) already exists.')

        account = self.getClientAccount(number, month)
        # print(account)

        return super().createSub(account=account, date=date)
    
    @property
    def accountsManager(self): return self.master.accountsManager
    
    def getClientAccount(self, number, month=None):
        account = self.accountsManager.getAccount(month)
        if account: return account.getClientAccount(number)
    
    def addAmount(self, number, month=None, money=False, date=None):
        pass

    def deleteSub(self, number, month=None):
        pass

    def setBto(self, bto):
        pass

    def updateSubs(self):
        pass




class Daily_Contributions(ObjectsManager):
    ObjectType = Daily_Contribution
    MultipleSubsPerMonth = True
    
    @property
    def name(self): return f'{self.master} | {self.className}'

    def createSub(self, date=None, **kwargs):
        
        if date == None: date = PRMP_DateTime.now()
        PRMP_DateTime.checkDateTime(date)
        
        date_validations = [dict(value=True, attr='date', attrMethod='isSameDate', attrMethodParams=[date])]

        prevs = self.objectSort.sort(validations=date_validations)
        # prevs = []

        if prevs:
            # print(prevs)
            raise ValueError(f'Daily_Contribution({date.date}) already exists.')

        return super().createSub(date=date, **kwargs)
    
    createDailyContributions = createSub

    @property
    def accountsManager(self): return self.master.accountsManager








