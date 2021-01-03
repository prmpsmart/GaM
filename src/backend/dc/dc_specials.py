from ..core.bases import Object, ObjectsManager, PRMP_DateTime, ObjectSort

class ContribContainer(Object):
    Manager = 'Daily_Contribution'
    
    def __init__(self, manager, clientAccount=None, amount=0, money=False, debit=0, paidout=False, transfer=False, **kwargs):
        super().__init__(manager, **kwargs)
        assert clientAccount, 'Account must be given'
        assert amount, 'Amount must be given'

        self.account = clientAccount
        
        self._paidout = paidout
        self._transfer = transfer
        self._money = money
        
        contribs = float(self.contributions)
        max_ = 31.0

        if money:
            contributed = amount/self.rate
            if (contribs + contributed) <= max_:
                remain = max_ - contribs
                'The amount'

        else:
            pass

        self.amount = amount if money else amount * self.rate
        self.contributed = amount/self.rate if money else amount
        self.debit = debit

        del self.objectSort

    @property
    def isUpfrontRepay(self): return

    @property
    def withdraw(self): return

    @property
    def paidout(self): return

    @property
    def transfer(self): return

    @property
    def month(self): return self.account.date
    
    @property
    def subs(self): return self._subs

    @property
    def name(self): return f'{self.className}({self.date.date}, No. {self.number})'
    
    def __eq__(self, other):
        if other == None: return False
        return (self.manager is other.manager) and (self.date is other.date)

    @property
    def contributions(self): return self.account.contributions

    @property
    def regName(self): return self.region.name

    @property
    def region(self): return self.account.region

    @property
    def rate(self): return self.account.rate
    
    def update(self):
        pass


class Daily_Contribution(ObjectsManager):
    Manager = 'Daily_Contributions'
    ObjectType = ContribContainer
    MultipleSubsPerMonth = True
    
    def __init__(self, manager, date=None, previous=None, number=0):
        super().__init__(manager)

        self._date = date
        self._previous = previous
        self.number = number
        self._bto = 0
        self._next = None
    
    @property
    def previous(self): return self._previous
    
    @property
    def next(self): return self._next
    
    @next.setter
    def next(self, next_):
        if self._next == None: self._next = next_
        else: raise self.Errors('A next is already set.')
    
    @property
    def manager(self): return self.master
    
    @property
    def name(self): return f'{self.className}({self.date.date})'
    
    def __eq__(self, other):
        if other == None: return False
        return (self.manager is other.manager) and (self.date is other.date)

    @property
    def region(self): return self.manager.region
    
    def createSub(self, number, month=None, date=None, **kwargs):
        now = PRMP_DateTime.now()
        if month == None: month = now
        if date == None: date = now
        PRMP_DateTime.checkDateTime(month)
        PRMP_DateTime.checkDateTime(date)
        
        validations = [dict(value=number, attr='number'), dict(value=month, attr={'account': 'date'})]

        prevs = self.sort(validations=validations)

        if prevs and len(prevs): raise ValueError(f'{prevs[0].name} already exists.')

        clientAccount = self.getClientAccount(number, month)
        if clientAccount: return super().createSub(clientAccount=clientAccount, date=date, **kwargs)
    
    @property
    def accountsManager(self): return self.manager.accountsManager
    
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
    def region(self): return self.master
    
    @property
    def name(self): return f'{self.master} | {self.className}'

    def createSub(self, date=None, **kwargs):
        
        if date == None: date = PRMP_DateTime.now()
        PRMP_DateTime.checkDateTime(date)
        
        date_validations = [dict(value=True, attr='date', attrMethod='isSameDate', attrMethodParams=[date])]

        prevs = self.sort(validations=date_validations)

        if prevs: raise ValueError(f'{self.objectName}({date.date}) already exists.')

        return super().createSub(date=date, **kwargs)
    
    createDailyContributions = createSub

    @property
    def accountsManager(self): return self.master.accountsManager








