
from .dc_records_managers import *
from ..core.accounts import PRMP_DateTime, Account, AccountsManager
from ..core.bases import ObjectsManager

class DCAccount(Account):
    Manager = 'DCAccountsManager'
    ObjectSortClass = DCSort

    def __init__(self, manager, month=None, **kwargs):
        assert month, 'Month that this account belongs to must be given.'

        self._month = month

        super().__init__(manager, **kwargs)

        self.incomes = Incomes(self)
        self.broughtForwards = BroughtForwards(self)
        self.savings = Savings(self)
        self.debits = Debits(self)
        self.upfronts = Upfronts(self)
        self.balances = Balances(self)

        self.transfers = Transfers(self)
        self.normalIncomes = NormalIncomes(self)
        self.paidouts = Paidouts(self)
        self.withdrawals = Withdrawals(self)

    def __int__(self): return int(self.balances)
    def __float__(self): return float(self.balances)

    @property
    def name(self): return f'{self.className}({self.region.name} | {self._month.monthYear})'

    @property
    def month(self): return self._month
    @property
    def region(self):
        if self.manager: return self.manager.region
        return None

    @property
    def recordsManagers(self): return [self.broughtForwards, self.incomes, self.normalIncomes, self.transfers, self.savings, self.debits, self.withdrawals, self.paidouts, self.upfronts, self.balances]

    @property
    def pendingUpfronts(self): return self.upfronts.lastRecord.outstanding

    @property
    def repaidUpfront(self):
        if len(self.upfronts): return self.upfronts.lastRecord.repaid

    def addBroughtForward(self, bf, date=None, **kwargs): return self.broughtForwards.createRecord(bf, date=date, **kwargs)

    def balanceAccount(self, date=None):
        self._balanceAccount(date)
        self.updateBroughtForwards(date)

    def updateBroughtForwards(self, date=None):
        if self.nextAccount: self.nextAccount.addBroughtForward(float(self.balances), date=date)

    def get_RMs_By_Seasons(self, date=None, **kwargs):
        leng = len(self)
        date = self.getDate(date)

        recs = []
        for ind in range(leng):
            recM = self[ind]
            _recs = recM.objectSort.sortSubsBySeasons(date, **kwargs)

            newRecM = recM.recordsAsRecordsManager(_recs, date)
            recs.append(newRecM)

        return recs

    def get_RMs_By_Date(self, date=None, **kwargs): return self.get_RMs_By_Seasons(date=date, seasons=['date'], **kwargs)

    def get_RMs_By_Day(self, date=None, **kwargs): return self.get_RMs_By_Seasons(date=date, seasons=['day'], **kwargs)

    def get_RMs_By_DayName(self, date=None, **kwargs): return self.get_RMs_By_Seasons(date=date, seasons=['dayName'], **kwargs)

    def get_RMs_By_Week(self, date=None, **kwargs): return self.get_RMs_By_Seasons(date=date, seasons=['week'], **kwargs)


class DCAccountsManager(AccountsManager):
    ObjectType = DCAccount
    ObjectSortClass = DCSort

    def __init__(self, region, **kwargs):
        super().__init__(region, **kwargs)

    @property
    def overAllAccounts(self):
        # total accounts in this manager
        containerDict = {}
        for recordManager in self.lastAccount:
            name = recordManager.className
            if name not in containerDict: containerDict[name] = 0
            containerDict[name] += float(recordManager)
        return containerDict

    def createAccount(self, month=None, **kwargs):
        month = self.getDate(month)
        return super().createAccount(month=month, **kwargs)

    @property
    def recordsManagers(self): return self.last if len(self) else []

    def sortAccountsIntoMonths(self, date=None, **kwargs):
        date = self.getDate(date)
        monthsDates = date.monthsInYear

        accs = []
        for monthDate in monthsDates:
            _accs = self.sortSubsByMonth(monthDate)
            leng = len(_accs)
            if not leng:
                acc = self.ObjectType(self, month=monthDate, date=monthDate)
                accs.append(acc)
            elif leng: accs.append(_accs[-1])

        return accs


class ClientAccount(DCAccount):
    Manager = 'ClientAccountsManager'

    def __init__(self, manager, ledgerNumber=0, rate=0, areaAccount=None, month=None, **kwargs):
        self.areaAccount = areaAccount
        if month and ledgerNumber: assert month.monthYear == areaAccount.month.monthYear, 'ClientAccount month must be same as AreaAccount month.'

        rate = float(rate)
        self.ledgerNumber = ledgerNumber

        super().__init__(manager, month=month or areaAccount.month, **kwargs)

        self.contributions = Contributions(self)
        self.rates = Rates(self, rate, ledgerNumber)
        self.addUpfront = self.upfronts.addUpfront
        self.addContribution = self.contributions.addContribution


    @property
    def name(self): return f'{self.className}({self.region.name} | {self._month.monthYear} | Ledger-Number No. {self.ledgerNumber})'

    def income(self, date=None):
        date = self.getDate(date)
        return sum([rec.savings for rec in self.contributions if rec.date.month == date.month])

    @property
    def recordsManagers(self):
        recordsManagers_ =  super().recordsManagers
        recordsManagers_.insert(1, self.rates)
        recordsManagers_.insert(2, self.contributions)
        return recordsManagers_

    @property
    def rate(self): return float(self.rates)

    def _balanceAccount(self, date=None):
        rate = float(self.rates)
        bal = float(self.broughtForwards) + float(self.savings) - float(self.upfronts.outstanding) - float(self.debits) - rate

        self.balances.createRecord(bal, notAdd=True, newRecord=False, date=date)


    def addDebit(self, debit, **kwargs):
        self._balanceAccount()
        rec = self.debits.addDebit(debit, _type=_type, **kwargs)
        self.balanceAccount()
        return rec



class ClientsAccounts(ObjectsManager):
    ObjectSortClass = DCSort
    subTypes = ['Clients Accounts']

    def __init__(self, account):
        assert account.className == 'AreaAccount' and account.region.className == 'Area', 'This account must be an instance of AreaAccount and its region an instance of Area.'

        self.account = account
        self._subs = []
        super().__init__(account, date=account.date)

    @property
    def name(self): return f'{self.className}({self.account.name})'

    def __str__(self): return self.name
    def __repr__(self): return f'<{self}>'

    def add(self, clientAccount):
        if clientAccount not in self._subs:
            # print(clientAccount)
            self._subs.append(clientAccount)

    @property
    def subs(self): return self._subs
    @property
    def clientsAccounts(self): return self.subs

    @property
    def regions(self): return [acc.region for acc in self._subs]

    def getRecs_Of_RM_Of_AccByDate(self, account, date=None): return account.get_RMs_By_Date(date)

    def getRecs_Of_RM_Of_AccsByDate(self, date=None):
        accs = self[:]
        accsRecs = []
        for acc in accs:
            recs = self.getRecs_Of_RM_Of_AccByDate(acc, date)
            accsRecs.append(recs)
        return accsRecs

    def getRecs_Of_RM_Of_AccByWeek(self, account, week=None): return account.getRecs_Of_RM_ByWeek(week)

    def getRecs_Of_RM_Of_AccsByWeek(self, week=None):
        accs = self[:]
        accsRecs = []
        for acc in accs:
            recs = self.getRecs_Of_RM_Of_AccByWeek(acc, week)
            accsRecs.append(recs)
        return accsRecs


class AreaAccount(DCAccount):
    Manager = 'AreaAccountsManager'

    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs)
        self.commissions = Commissions(self)
        self.broughtToOffices = BroughtToOffices(self)
        self.excesses = Excesses(self)
        self.deficits = Deficits(self)
        self.ledgerNumbers = 0
        self.ledgerNumber = self.number


        if self.className == 'AreaAccount': self.clientsAccounts = ClientsAccounts(self)

    def addClientAccount(self, account):
        if account in self.clientsAccounts: return
        self.clientsAccounts.add(account)
        self.ledgerNumbers = len(self.clientsAccounts)


    @property
    def recordsManagers(self):
        recordsManagers =  super().recordsManagers + [self.broughtToOffices, self.excesses, self.deficits]
        recordsManagers.insert(1, self.commissions)
        return recordsManagers

    @property
    def btos(self): return self.broughtToOffices

    def _balanceAccount(self, date=None):
        clientsAccounts = self.clientsAccounts.subs

        for a in clientsAccounts: a.balanceAccount()

        if clientsAccounts:

            self.incomes.updateWithOtherManagers([account.incomes for account in clientsAccounts])

            self.balances.updateWithOtherManagers([account.balances for account in clientsAccounts])

            self.commissions.updateWithOtherManagers([account.rates for account in clientsAccounts])

            self.debits.updateWithOtherManagers([account.debits for account in clientsAccounts])

            self.savings.updateWithOtherManagers([account.savings for account in clientsAccounts])

            self.upfronts.updateWithOtherManagers([account.upfronts for account in clientsAccounts])

            self.paidouts.updateWithOtherManagers([account.paidouts for account in clientsAccounts])

            self.withdrawals.updateWithOtherManagers([account.withdrawals for account in clientsAccounts])

            self.transfers.updateWithOtherManagers([account.transfers for account in clientsAccounts])

            self.normalIncomes.updateWithOtherManagers([account.normalIncomes for account in clientsAccounts])


    def addBto(self, bto, date=None):
        clientsAccounts = self.getClientsAccounts()

        incomes = [self.sumRecords(acc.incomes.sortSubsByDate(date)) for acc in clientsAccounts]

        contributed = sum(incomes)

        transfers = self.sumRecords(self.transfers.sortRecordsByDate(date))

        btoRec = self.btos.createRecord(bto, date)
        bto += transfers

        if bto > contributed: self.excesses.createRecord(bto - contributed, date, coRecord=btoRec)
        elif contributed > bto: self.deficits.createRecord(contributed - bto, date, coRecord=btoRec)

    def updateClientsAccounts(self):
        accs = self.getClientsAccounts()
        for acc in accs: self.addClientAccount(acc)

    def getClientsAccounts(self, month=None):
        acs = self.manager.sortClientsAccountsByMonth(month or self.month)
        return sorted(acs)

    def getClientAccount(self, ledgerNumber, month=None):
        clientsAccounts = self.getClientsAccounts(month)
        for clientsAccount in clientsAccounts:
            if clientsAccount.ledgerNumber == int(ledgerNumber): return clientsAccount


class ClientAccountsManager(DCAccountsManager):
    ObjectType = ClientAccount
    MultipleSubsPerMonth = True

    def __init__(self, region, **kwargs):
        self.startRate = kwargs.get('rate', 0)
        super().__init__(region, **kwargs)

    @property
    def areaAccountsManager(self): return self.master.accountsManager

    def createAccount(self, rate=0, month=None, **kwargs):
        area = self.region.sup
        areaAcc = area.accountsManager.getAccount(month=month)
        if areaAcc:
            ledgerNumber = areaAcc.ledgerNumbers + 1

            acc = super().createAccount(rate=rate, ledgerNumber=ledgerNumber, areaAccount=areaAcc, month=month, **kwargs)

            areaAcc.addClientAccount(acc)
            return acc

        else: raise DCErrors.AccountsError(f'{area} does not have an account in {month.monthYear} ')

    def changeRate(self, rate):
        if self.lastAccount: self.lastAccount.rates.setRate(rate)

    def addContribution(self, contribution, month=None, **kwargs):
        if month == None: month = PRMP_DateTime.now()
        account = self.sortSubsByMonth(month)[0]
        return account.addContribution(contribution, **kwargs)

    def addDebit(self, debit, month):
        if month == None: month = PRMP_DateTime.now()
        monthAcc = self.accountManager.getAccount(month=month)
        if monthAcc: monthAcc.debits.addDebit(debit)

    def addUpfront(self, upfront, month):
        assert PRMP_DateTime.now().isSameMonth(month)
        pass


class AreaAccountsManager(DCAccountsManager):
    ObjectType = AreaAccount

    @property
    def clientsManager(self): return self.region.clientsManager

    def sortClientsAccountsByMonth(self, month): return self.sortSubRegionsAccountsByMonth(month)



