from ..core.bases import Object, ObjectsManager, PRMP_DateTime, ObjectSort


class Records(Object, list):
    Manager = 'Thrift'


    def __init__(self, thrift):
        list.__init__(self)
        Object.__init__(self, thrift)
        self.thrift = thrift

    @property
    def subs(self): return list(self)


class Common: col_attr = ['number', {'month': 'monthYear'}, 'Region Name', 'Ledger Number', 'Rate', 'Contributed', 'Income', 'Transfer', 'Paidout', 'Upfront Repay', 'Saved']

DEST = r'C:\Users\Administrator\Documents\GaM OFFICE\DC matters\Contributions'

columns = ['number', 'rate', 'amount', 'money']


class Contribution(PRMP_Mixins):

    def __init__(self, number, rate, amount):
        amount = float(amount)
        rate = float(rate)
        number = int(number)
        self.number = number
        self.rate = rate
        self.subs = None

        if amount > 31: money = 1
        else: money = 0

        if money:
            self.money = amount
            self.amount = amount / rate
        else:
            self.amount = amount
            self.money = rate * amount

    @property
    def _subs(self): return self[columns[:]]

    def __str__(self): return f'{self.className}(Number={self.number}, Rate={self.rate}, Amount={self.amount}, Money={self.money})'
    def __repr__(self): return f'<{self.number}>'

    def __lt__(self, other):
        if other == None: return False
        return self.number < other.number
    def __le__(self, other):
        if other == None: return False
        return self.number <= other.number
    def __eq__(self, other):
        if other == None: return False
        return self.number is other.number
    def __ne__(self, other):
        if other == None: return True
        return self.number != other.number
    def __gt__(self, other):
        if other == None: return True
        return self.number > other.number
    def __ge__(self, other):
        if other == None: return True
        return self.number >= other.number

class Contributions(PRMP_Mixins):
    def __init__(self, area, month=None, date=None,commission=False):
        date = self.getDate(date)
        month = self.getDate(month)

        self.get = self.getFromSelf

        self.area, self.month, self.date, self.commission =  int(area), month, date, commission
        self.subs = self.contributions = []

    def __str__(self): return f'{self.className}(Area={self.area}, Month={self.month.monthYear}, Date={self.date.date}, Money={self.money})'

    def add(self, number, rate, amount=0):
        numbers = [cont.number for cont in self]
        if self.commission: amount = 1

        if number in numbers: raise ValueError(f'This number {number} already exists.')

        cont = Contribution(number, rate, amount)
        self.contributions.append(cont)
        self.contributions.sort()

        return cont

    def remove(self, cont):
        if cont in self: self.subs.remove(cont)

    @property
    def _name(self):
        n = f'Area_{self.area} {self.month.monthYear} {self.date.date}'

        n = n.replace('/', '-')
        return n

    @property
    def name(self):
        n = f'{self._name} {"Commission" if self.commission else ""}'

        return n

    @property
    def path(self):
        p = self._name.split(' ')
        p = '/'.join(p[:-1])
        p = os.path.join(p, self._name).replace('/', '\\')
        dest = os.path.join(DEST, p) + f' {"Commission" if self.commission else ""}.cont'
        return dest

    @property
    def money(self): return sum([cont.money for cont in self])

    @property
    def total(self): return len(self)

    def save(self, path=''):
        if not path:
            path = self.path
            dir_ = os.path.dirname(path)
            try: os.makedirs(dir_)
            except: pass

        file = PRMP_File(filename=path)
        file.saveObj(self)
        file.save(path)

        return file

    @classmethod
    def load(self, file):
        file = PRMP_File(filename=file)
        conts = file.loadObj()
        return conts


class Thrift(Object, Common):
    Manager = 'DailyContribution'

    def __init__(self, manager, clientAccount=None, income=0, money=False, paidout=0, transfer=0, **kwargs):
        assert clientAccount, 'Account must be given'

        assert income or paidout, 'Income or Paidout transactions must be made first.'

        self.account = self.clientAccount = clientAccount
        self.ledgerNumber = clientAccount.ledgerNumber

        self.paidoutRecord = None
        self.contRecord = None
        self.tranRecord = None
        self.debRecord = None
        self.conTranRecord = None

        self._subs = None

        super().__init__(manager, month=self.account.month, **kwargs)
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
        self.paidout = float(paidout)

        max_ = 31.0
        contribs = float(self.contributions)

        contributed = income/self.rate if money else income

        new = contribs + contributed
        if new <= max_:
            self.contributed = float(contributed)
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
    def month(self): return self.clientAccount.month

    @property
    def name(self): return f'{self.className}({self.date.date}, No. {self.number}, {self.clientAccount.name})'

    def __eq__(self, other):
        if other == None: return False
        return (self.manager is other.manager) and (self.date == other.date) and (self.number == other.number)

    @property
    def contributions(self): return self.clientAccount.contributions

    @property
    def newContributions(self): return float(self.contributions) + self.contributed

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

    @property
    def datas(self): return self[self.col_attr]


class DailyContribution(ObjectsManager, Common):
    Manager = 'DailyContributionsManager'
    ObjectType = Thrift
    MultipleSubsPerMonth = True
    subTypes = ['Thrifts']

    def __init__(self, manager, date=None, previous=None, number=0):
        super().__init__(manager, date=date, previous=previous)

        self.number = number
        self.__bto = 0

    @property
    def lastMonths(self):
        thrifts = [thf for thf in self if thf.account.date.monthYearTuple < self.date.monthYearTuple]
        return thrifts
    @property
    def currentMonths(self):
        thrifts = [thf for thf in self if thf.account.date.monthYearTuple == self.date.monthYearTuple]
        return thrifts
    @property
    def nextMonths(self):
        thrifts = [thf for thf in self if thf.account.date.monthYearTuple > self.date.monthYearTuple]
        return thrifts

    @property
    def lastMonthIncome(self): return sum(self.lastMonths)
    @property
    def currentMonthIncome(self): return sum(self.currentMonths)
    @property
    def nextMonthIncome(self): return sum(self.nextMonths)

    @property
    def accounts(self): return len(self)

    @property
    def contributed(self): return sum([thrift.contributed for thrift in self.thrifts])

    @property
    def cash(self): return sum([thrift.cash for thrift in self.thrifts])

    @property
    def transfer(self): return sum([thrift.transfer for thrift in self.thrifts])

    @property
    def paidout(self): return sum([thrift.paidout for thrift in self.thrifts])

    @property
    def income(self): return sum([thrift.income for thrift in self.thrifts])

    @property
    def saved(self): return sum([thrift.saved for thrift in self.thrifts])

    @property
    def upfrontRepay(self): return sum([thrift.upfrontRepay for thrift in self.thrifts])

    @property
    def bto(self): return self.__bto

    @property
    def excess(self):
        if self.bto > self.income: return self.bto - self.income
        return 0

    @property
    def deficit(self):
        if self.bto < self.income: return self.income - self.bto
        return 0

    @property
    def thrifts(self): return self.subs

    @property
    def accountsManager(self): return self.manager.accountsManager

    @property
    def name(self): return f'{self.className}({self.region.name} | {self.date.date})'

    def __eq__(self, other):
        if other == None: return False
        return (self.manager is other.manager) and (self.date is other.date)

    @property
    def region(self): return self.manager.region

    def createSub(self, ledgerNumber, month=None, account=None, clientAccount=None, **kwargs):
        if account: month = account.month
        else: month = self.getDate(month)
        ledgerNumber = int(ledgerNumber)

        prevs = self.getSub(number=ledgerNumber, month=month) or []

        if prevs: raise ValueError(f'{prevs.name} already exists.')

        # clientAccount = self.getClientAccount(ledgerNumber, account, month)
        clientAccount = clientAccount or self.getClientAccount(ledgerNumber, account, month)

        if clientAccount: return super().createSub(clientAccount=clientAccount, date=self.date, **kwargs)
        else: raise ValueError(f'ClientAccount({month.monthYear}, No. {ledgerNumber}) does not exists.')

    def createThrift(self, ledgerNumber=None, month=None, income=0, money=False, paidout=0, transfer=0, account=None, clientAccount=None): return self.createSub(ledgerNumber, month=month, income=income, money=money, paidout=paidout, transfer=transfer, account=account, clientAccount=clientAccount)

    def getClientAccount(self, ledgerNumber, account=None, month=None):
        month = self.getDate(month)
        account = account or self.accountsManager.getAccount(month=month)

        if account: return account.getClientAccount(ledgerNumber)

    def deleteSub(self, number, month=None):
        pass

    def addBTO(self, bto): self.__bto = bto
    addBto = addBTO

    def updateThrifts(self):
        for sub in self: sub.updateRecords()

    @property
    def subsDatas(self): return [sub.datas for sub in self]


class DailyContributionsManager(ObjectsManager):
    ObjectType = DailyContribution
    MultipleSubsPerMonth = True
    subTypes = ['Daily Contributions']

    @property
    def region(self): return self.master

    @property
    def dailyContributions(self): return self.subs

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








