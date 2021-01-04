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
        self.saved = 0
        
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

    def isUpfrontRepay(self):
        if not self.account.upfronts.paid:
            repay, remain = self.contributions._toUpfrontRepay(self.income)
            self.saved = remain
            self.upfrontRepay = repay

    @property
    def withdraw(self): return

    @property
    def month(self): return self.account.month
    
    @property
    def subs(self): return self._subs

    @property
    def name(self): return f'{self.className}({self.date.date}, No. {self.number}, [{self.account.region.name}, {self.account.name}])'
    
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
        if self.contributed:
            if self.contRecord: pass
            else: self.contRecord = self.account.addContribution(self.contributed, date=self.date, _type='t' if self.transfer else 'n')

        if self.debit:
            if self.debRecord: pass
            else: self.debRecord = self.account.addDebit(self.debit, date=self.date, _type='p' if self.paidout else 'w')
        # print(self.contRecord[:])
    
    def __del__(self):
        del self.contRecord, self.debRecord
        self.account.balanceAccount()
        del self


class Daily_Contribution(ObjectsManager):
    Manager = 'Daily_Contributions'
    ObjectType = ContribContainer
    MultipleSubsPerMonth = True
    
    columns = ['Month', 'Name', 'Ledger Number', 'Rate', 'Contributed', 'Income', 'Transfer', 'Debit', 'Paidout', 'Upfront Repay', 'Saved']
    col_attr = [{'month': 'monthYear'}, 'regName', {'account': 'ledgerNumber'}, 'rate', 'contributed', 'income', 'transfer', 'debit', 'paidout', 'upfrontRepay', 'saved']
    
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
    def accountsManager(self): return self.manager.accountsManager
    
    @property
    def name(self): return f'{self.className}({self.date.date})'
    
    def __eq__(self, other):
        if other == None: return False
        return (self.manager is other.manager) and (self.date is other.date)

    @property
    def region(self): return self.manager.region
    
    def createSub(self, number, month=None, **kwargs):
        month = self.getDate(month)

        prevs = self.getSub(number=number, month=month) or []

        if prevs and len(prevs): raise ValueError(f'{prevs.name} already exists.')

        clientAccount = self.getClientAccount(number, month)
        
        if clientAccount: return super().createSub(clientAccount=clientAccount, date=self.date, month=month, **kwargs)
        else: raise ValueError(f'ClientAccount({month.monthYear}, No. {number}) does not exists.')
    
    def addIncome(self, number, month=None, income=0, money=False, debit=0, paidout=False, transfer=False): return self.createSub(number, month=month, income=income, money=money, debit=debit, paidout=paidout, transfer=transfer)
    
    def getClientAccount(self, number, month=None):
        month = self.getDate(month)
        account = self.accountsManager.getAccount(month=month)
        
        if account: return account.getClientAccount(number)
    
    def deleteSub(self, number, month=None):
        pass

    def setBto(self, bto):
        pass

    def update(self):
        for sub in self: sub.update()
    
    @property
    def subsDatas(self): return [sub[self.col_attr] for sub in self]


class Daily_Contributions(ObjectsManager):
    ObjectType = Daily_Contribution
    MultipleSubsPerMonth = True

    @property
    def region(self): return self.master
    
    @property
    def name(self): return f'{self.master} | {self.className}'

    def createSub(self, date=None, **kwargs):
        
        date = self.getDate(date)
        
        date_validations = [dict(value=True, attr='date', attrMethod='isSameDate', attrMethodParams=[date])]

        prevs = self.sort(validations=date_validations)

        if prevs: raise ValueError(f'{self.objectName}({date.date}) already exists.')

        return super().createSub(date=date, **kwargs)
    
    addDailyC = createSub

    @property
    def accountsManager(self): return self.master.accountsManager








