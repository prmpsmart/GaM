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
    
    def __eq__(self, other): return (self.manager is other.manager) and (self.date is other.date)

    @property
    def contrib(self): return self.account.contributions

    @property
    def region(self): return self.account.region


class Daily_Contribution(ObjectsManager):
    Manager = 'Daily_Contributions'
    
    def __init__(self, manager, account=None, **kwargs):
        super().__init__(manager, **kwargs)

        self.account = account
    
    @property
    def name(self): return f'{self.manager} | {self.className}({self.date}) '
    
    def __eq__(self, other): return (self.manager is other.manager) and (self.date is other.date)

    @property
    def contrib(self): return self.account.contributions

    @property
    def region(self): return self.account.region




class Daily_Contributions(ObjectsManager):
    ObjectType = Daily_Contribution
    MultipleSubsPerMonth = True

    def __init__(self, area):
        super().__init__(area)
    
    @property
    def name(self): return f'{self.master} {self.className} '

    def createSub(self, number, month=None, date=None, **kwargs):
        
        if date == None: date = PRMP_DateTime.now()
        PRMP_DateTime.checkDateTime(date)
        
        date_validations = [dict(value=True, attr='date', attrMethod='isSameDate', attrMethodParams=[date])]

        prevs = self.objectSort.sort(validations=date_validations)

        if prevs: raise ValueError(f'Daily_Contribution({date}) already exists.')

        account = self.getClientAccount(number, month)
        # print(account)

        return super().createSub(account=account, date=date, **kwargs)
    
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









