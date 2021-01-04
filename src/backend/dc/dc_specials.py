from ..core.bases import Object, ObjectsManager, PRMP_DateTime, ObjectSort

class ContribContainer(Object):
    Manager = 'Daily_Contribution'
    
    def __init__(self, manager, clientAccount=None, income=0, money=False, debit=0, paidout=False, transfer=False, **kwargs):
        super().__init__(manager, **kwargs)
        assert clientAccount, 'Account must be given'

        self.account = clientAccount
        self.debRecord = None
        self.contRecord = None
        self.upfrontRepay = 0
        
        self.paidout = True if paidout else False
        self.transfer = True if transfer else False
        
        max_ = 31.0
        contribs = float(self.contributions)

        contributed = income/self.rate if money else income
        new = contribs + contributed
        if new <= max_:
            self.contributed = contributed
            self.income = contributed * self.rate
        else:
            excess = new - max_
            required = max_ - contribs
            print(excess, required, contribs)
            raise ValueError(f'Excess of {excess}, Required [contribution={required}, money={required*self.rate}], current contributions is {contribs}.')

        bal = float(self.account.balances)
        debit = float(debit)
        if debit <= bal or debit == .0: self.debit = debit
        else: raise ValueError(f'Balance is {bal}, but income to be debited is {debit}')

        self.isUpfrontRepay()

        del self.objectSort

    def isUpfrontRepay(self): return

    @property
    def withdraw(self): return

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
        if self.contributed and not self.contRecord: self.contRecord = self.account.addContribution(self.contributed, date=self.date, _type='t' if self.transfer else 'n')

        if self.debit and not self.debRecord: self.debRecord = self.account.addDebit(self.debit, date=self.date, _type='p' if self.paidout else 'w')
        # print(self.contRecord[:])

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
    
    def createSub(self, number, month=None, **kwargs):
        now = PRMP_DateTime.now()
        if month == None: month = now
        PRMP_DateTime.checkDateTime(month)
        
        validations = [dict(value=number, attr='number'), dict(value=month, attr={'account': 'date'})]

        prevs = self.sort(validations=validations)

        if prevs and len(prevs): raise ValueError(f'{prevs[0].name} already exists.')

        clientAccount = self.getClientAccount(number, month)
        if clientAccount: return super().createSub(clientAccount=clientAccount, date=self.date, **kwargs)
    
    def addIncome(self, number, month=None, income=0, money=False, debit=0, paidout=False, transfer=False): return self.createSub(number, month=month, income=income, money=money, debit=debit, paidout=paidout, transfer=transfer)
    
    @property
    def accountsManager(self): return self.manager.accountsManager
    
    def getClientAccount(self, number, month=None):
        account = self.accountsManager.getAccount(month)
        if account: return account.getClientAccount(number)
    

    def deleteSub(self, number, month=None):
        pass

    def setBto(self, bto):
        pass

    def update(self):
        for sub in self: sub.update()


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
    
    addDailyC = createSub

    @property
    def accountsManager(self): return self.master.accountsManager








