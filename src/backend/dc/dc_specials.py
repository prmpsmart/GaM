from ..core.bases import Object, ObjectsManager, PRMP_DateTime, ObjectSort

class Records(Object, list):
    Manager = 'Thrift'


    def __init__(self, thrift):
        list.__init__(self)
        Object.__init__(self, thrift)
        self.thrift = thrift

    @property
    def subs(self): return list(self)


class Thrift(Object):
    Manager = 'DailyContribution'
    
    def __init__(self, manager, clientAccount=None, income=0, money=False, paidout=0, transfer=0, **kwargs):
        assert clientAccount, 'Account must be given'

        self.account = self.clientAccount = clientAccount
        self.ledgerNumber = clientAccount.ledgerNumber
        
        self.paidoutRecord = None
        self.contRecord = None
        self.tranRecord = None
        self.debRecord = None
        self.conTranRecord = None
        
        self._subs = None
        
        super().__init__(manager, **kwargs)
        del self.objectSort

        self.update(transfer=transfer, income=income, money=money, paidout=paidout, reload_=0)
    
    @property
    def subs(self):
        self._subs = Records(self)
        for r in [self.contRecord, self.conTranRecord, self.tranRecord, self.debRecord, self.paidoutRecord]:
            if r: self._subs.append(r)

        return self._subs
    
    def update(self, transfer=0, income=0, money=False, paidout=0, reload_=1):
        # self.deleteRecords()

        self.updated = False
        self.upfrontRepay = 0.

        self.money = money
        self.transfer = float(transfer)
        self._income = float(income)
        
        max_ = 31.0
        contribs = float(self.contributions)

        contributed = income/self.rate if money else income

        new = contribs + contributed
        if new <= max_:
            self.contributed = contributed
            self.saved = self.income = contributed * self.rate
            self.cash = self.saved if not transfer else self.saved - transfer

        else:
            excess = new - max_
            required = max_ - contribs
            raise ValueError(f'Excess of {excess}, Required [contribution={required}, money={required*self.rate}], current contributions is {contribs}.')

        self.isUpfrontRepay()

        bal = float(self.clientAccount.balances) + self.saved
        paidout = float(paidout)
        if paidout <= bal or paidout == 0.0: self.paidout = paidout
        else: raise ValueError(f'Balance is {bal}, but amount to be paidout is {paidout}')


        if reload_: self.updateRecords()

    def deleteRecords(self):
        for rec in self.subs:
            if rec: rec.delete()

        self.paidoutRecord = None
        self.contRecord = None
        self.tranRecord = None
        self.debRecord = None
        self.conTranRecord = None
        self.account.balanceAccount()

    def isUpfrontRepay(self):
        if not self.clientAccount.upfronts.paid:
            repay, remain = self.contributions._toUpfrontRepay(self.income)
            self.saved = remain
            self.upfrontRepay = repay

    @property
    def withdraw(self): return

    @property
    def month(self): return self.clientAccount.month

    @property
    def name(self): return f'{self.className}({self.date.date}, No. {self.number}, {self.clientAccount.name})'
    
    def __eq__(self, other):
        if other == None: return False
        return (self.manager is other.manager) and (self.date == other.date) and (self.number == other.number)

    @property
    def contributions(self): return self.clientAccount.contributions

    @property
    def regionName(self): return self.region.name

    @property
    def region(self): return self.clientAccount.region

    @property
    def rate(self): return self.clientAccount.rate
    
    def updateRecords(self):
        
        if self.updated: return
        self.deleteRecords()

        if self.contributed:
            if self.cash:
                self.contRecord = self.clientAccount.addContribution(self.cash/self.rate, date=self.date)
                self.account.balanceAccount()

            if self.transfer:
                self.conTranRecord = self.clientAccount.addContribution(self.transfer/self.rate, date=self.date, _type='t')
                for rec in self.conTranRecord:
                    if rec.className == 'Transfer': self.tranRecord = rec

                self.account.balanceAccount()
                    
        if self.paidout:
            self.debRecord = self.clientAccount.addDebit(self.paidout, date=self.date, _type='p')
            self.paidoutRecord = self.debRecord.type
            self.account.balanceAccount()
        self.updated = True
    
    def delete(self):
        self.deleteRecords()
        self.manager.removeSub(self)


class DailyContribution(ObjectsManager):
    Manager = 'DailyContributionsManager'
    ObjectType = Thrift
    MultipleSubsPerMonth = True
    subTypes = ['Thrifts']
    
    col_attr = [{'month': 'monthYear'}, 'Region Name', 'Ledger Number', 'Rate', 'Contributed', 'Income', 'Transfer', 'Paidout', 'Upfront Repay', 'Saved']
    
    def __init__(self, manager, date=None, previous=None, number=0):
        super().__init__(manager, date=date, previous=previous)

        self.number = number
        self._bto = 0

    @property
    def thrifts(self): return self.subs
    
    @property
    def manager(self): return self.master
    
    @property
    def accountsManager(self): return self.manager.accountsManager
    
    @property
    def name(self): return f'{self.className}({self.region.name} | {self.date.date})'
    
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
    
    def createThrift(self, number, month=None, income=0, money=False, paidout=0, transfer=0): return self.createSub(number, month=month, income=income, money=money, paidout=paidout, transfer=transfer)
    
    def getClientAccount(self, number, month=None):
        month = self.getDate(month)
        account = self.accountsManager.getAccount(month=month)
        
        if account: return account.getClientAccount(number)
    
    def deleteSub(self, number, month=None):
        pass

    def setBto(self, bto):
        pass

    def update(self):
        for sub in self: sub.updateRecords()
    
    @property
    def subsDatas(self): return [sub[self.col_attr] for sub in self]


class DailyContributionsManager(ObjectsManager):
    ObjectType = DailyContribution
    MultipleSubsPerMonth = True
    subTypes = ['Daily Contributions']

    @property
    def region(self): return self.master
    
    @property
    def name(self): return f'{self.className}({self.master.name})'

    def createSub(self, date=None, **kwargs):
        
        date = self.getDate(date)
        
        date_validations = [dict(value=True, attr='date', attrMethod='isSameDate', attrMethodParams=[date])]

        prevs = self.sort(validations=date_validations)

        if prevs: raise ValueError(f'{self.objectName}({date.date}) already exists.')

        return super().createSub(date=date, **kwargs)
    
    addDailyC = createSub

    @property
    def accountsManager(self): return self.master.accountsManager








