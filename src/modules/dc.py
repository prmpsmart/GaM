__author__ = "PRMP Smart"
from core import *



class DCErrors(Errors):
    class UpfrontsError(Exception): pass
    class RatesError(Exception): pass
    class BroughtForwardsError(Exception): pass
    class BalancesError(Exception): pass
    class ContributionsError(Exception): pass
    class AccountsError(Exception): pass










class DCColumn:
    _clientsRecMs = ['BroughtForwards', 'Rates', 'Contributions', 'Incomes', 'NormalIncomes', 'Transfers', 'Savings', 'Debits', 'Withdrawals', 'Paidouts', 'Upfronts', 'Balances']
    _areasRecMs = ['BroughtToOffices', 'Excesses', 'Deficits']

    _shorts_ = dict(BroughtForwards='Br-Fs', Contributions='Contribs', NormalIncomes='Norm-Incs', Transfers='Trans', Withdrawals='Withdraws', BroughtToOffices='B-T-Os', Excesses='Excess', Deficits='Defs', Commissions='Comms', Balances='Bals')
    _shorts_['Ledger Number'] = 'L / N'

    weeks = ["Week"]
    days = ["Day", "Date"]
    specday = ['Week', 'Date']
    specdays = ['Day']
    clients = ["Ledger Number", "Name"] # done

    nums = dict(weeks=1, days=2, specday=2, specdays=1, clients=2)
    dateAttrs = dict(Week='weekName', Day='dayName', Date='date')


    subs = ['Name', 'Date', 'Active']
    subsBig = ['Name', 'Date', 'Month', 'Active']

    subsAttrs = dict(Date='date', Month='monthYear', Active='date')

    @classmethod
    def getShorts(cls, lists):
        shorts = []
        for name in lists:
            if name in cls._shorts_: new = cls._shorts_[name]
            else: new = name
            shorts.append(new)
        return shorts

    @classmethod
    def areas(cls, header):
        cl = cls._clientsRecMs.copy()
        del cl[1]
        cl[1] = 'Commissions'
        ar = cl + cls._areasRecMs
        head = cls.__dict__[header]

        return head + ar

    @classmethod
    def getColumns(cls, header, recMs):
        if recMs == '_areasRecMs': return cls.areas(header)
        head = cls.__dict__[header]
        reg = cls.__dict__[recMs]

        return head + reg

    @classmethod
    def merge(cls, one, two):
        n = cls.getColumns(one) + cls.getColumns(two)
        return n

    @classmethod
    def getObjColumns(cls, obj, season, which):
        if 'DCAccount' in obj.mroStr:
            recMs = '_clientsRecMs' if obj.className == 'ClientAccount' else '_areasRecMs'

            if season in ['month', 'week']:
                normal = 0
                if 'spec' not in which: normal = 1

                if normal: return cls.getColumns(which, recMs)

            elif season == 'subs':
                if which in ['date', 'week']: pass
                elif which in ['month', 'year']: pass


    @classmethod
    def designDatas(cls, season, which, datas, w=''):
        pass


class DCSort(ObjectSort):

    def __init__(self, region):
        super().__init__(region)

    def sortSubsMonthBySeasons(self, *args, attr='month', **kwargs): return self.sortSubsBySeasons(*args, attr=attr, **kwargs)

    def sort_Recs_By_Date(self, date, recs=[]):
        recs = recs or self.object[:]

        sortedRecs = self.sortSubsBySeasons(date, subs=recs, seasons=['date'])
        return sortedRecs

    def getObj(self, date=None, season='', which='', account=0, object_=None, subsAttr=''):
        subsAttr = subsAttr or 'accountsManager'
        obj = object_ or self.object
        season, which = self._format_season_which(season, which)

        w = 'obj'
        if 'DCRegion' in obj.mroStr:
            w = 'man'
            obj = obj[subsAttr]

        elif 'DCAccountsManager' in obj.mroStr: w = 'man'
        elif ('DCAccount' in obj.mroStr) or (obj.className == 'ClientsAccounts'):
            if obj.className == 'AreaAccount': w = 'Aacc'
            elif (obj.className == 'ClientsAccounts'): w = 'AaccC'
            else: w = 'acc'
            account = 0

        if season not in ['years', 'year']:
            if self.checkNumber(account):
                if int(account) != 0:
                    account = int(account) - 1
                    accs = obj.sortSubsByMonth(date)
                    obj = accs[account] if accs else None
                    w = 'acc'

        return [obj, w]

    def getObj_w(self, *args, **kwargs): return self.getObj(*args, **kwargs)[1]

    def _format_season_which(self, season, which):
        # season = season or 'month'
        season = season.lower() or 'month'
        which = which.lower()

        subs = 'subs'
        ret = [season, which]

        if season in ['date', 'day', 'year']: ret[1] = subs
        elif season == 'week':
            if which != 'days': ret[1] = subs
        elif season == 'month':
            if not which: ret[1] = 'days'

        return ret

    def sort_it(self, date=None, season='', which='', account=0, object_=None, subsAttr='', **kwargs):
        season, which = self._format_season_which(season, which)
        date = self.getDate(date)

        obj, w = self.getObj(date, season=season, which=which, account=account, object_=object_, subsAttr=subsAttr)

        results = []

        if (season == 'subs') or (obj.className == 'ClientsAccounts'):
            if 'A' in w:
                if (obj.className == 'ClientsAccounts'):
                    cl_accs = obj
                    which = season
                else: cl_accs = obj.clientsAccounts

                datas = []
                for acc in cl_accs:
                    data = acc.get_RMs_By_Seasons(date, seasons=[which])
                    if data: datas.append(data)
                results =  datas

            elif w == 'man': results = obj.objectSort.sortSubsBySeasons(date, seasons=[which], **kwargs)

        else:

            if w in ['acc', 'Aacc']:

                if season == 'month':
                    if which == 'weeks':
                        weekDates = date.oneDateInWeeks
                        weekDatas = []

                        for week in weekDates:
                            datas = obj.get_RMs_By_Seasons(week, seasons=['year', 'month', 'week'])
                            if datas: weekDatas.append(datas)
                        results =  weekDatas

                    elif which == 'days':
                        days = date.monthOnlyDates
                        daysDatas = []

                        for day in days:
                            datas = obj.get_RMs_By_Date(day)
                            if datas:
                                daysDatas.append(datas)
                        results =  daysDatas

                    elif which == 'specdays':
                        specdays = date.specDaysDates
                        specDatas = []

                        for spec in specdays:
                            datas = obj.get_RMs_By_Seasons(spec, seasons=['month', 'dayName'])
                            if datas: specDatas.append(datas)
                        results =  specDatas

                    elif which == 'specday':
                        specdays = date.allSpecDaysDates[date.weekDay]
                        specDatas = []

                        for spec in specdays:
                            datas = obj.get_RMs_By_Seasons(spec, seasons=['date'])
                            if datas: specDatas.append(datas)
                        results =  specDatas

                elif season == 'week':
                    days = date.weekDates[date.week-1]
                    datas = []

                    for d in days:
                        data = obj.get_RMs_By_Date(d)
                        if data: datas.append(data)
                    results =  datas

        return results, w
        # return obj, results, w

    def getColumns(self, season='', which='', w=''):
        num = 0
        columns = []

        if 'acc' in w:
            recMs = '_clientsRecMs'
            if ('A' in w):
                if season == 'subs' or 'C' in w: which = 'clients'
                else: recMs = '_areasRecMs'
            # only for weeks, days, specday, specdays, clients
            if not which: return
            num = DCColumn.nums[which]
            columns = DCColumn.getColumns(which, recMs)
            # print(columns)

        elif w == 'obj' and season != 'subs':
            pass

        elif season == 'subs':
            if which in ['date', 'week']: columns = DCColumn.subs
            elif which in ['month', 'year']: columns = DCColumn.subsBig

        return columns, num

    def getDataByColumns(self, datas, columns, datacols):
        columnsNum = []
        if datas and columns: columnsNum = [datacols.index(c) for c in columns]

        refinedDatas = []

        if columnsNum:
            # print(columnsNum, columns, datacols)
            for data in datas:
                # print(len(data), [n.className for n in data])
                _data = [data[cn] for cn in columnsNum]
                refinedDatas.append(_data)

        return refinedDatas or datas

    def fillColumns(self, season='', which='', columns=[], _type=None, **kwargs):
        datas, w = self.sort_it(season=season, which=which, **kwargs)
        cols_num = self.getColumns(season, which, w)

        if cols_num: cols, num = cols_num
        else: return
        designcols, datacols = cols[:num], cols[num:]

        # print(columns)
        refinedDatas = self.getDataByColumns(datas, columns, datacols)
        # print(refinedDatas)

        designedDatas = []

        if (season != 'subs') or (w in ['Aacc']):
            case = [data[0] for data in refinedDatas]
            # print(case)

            if 'Ledger Number' in designcols: attrs = [dict(account=designcols[0]), dict(region=designcols[1])]

            else: attrs = [dict(date=DCColumn.dateAttrs[col]) for col in designcols]

            designedDatas = [d[attrs] for d in case]

            for cd in designedDatas:
                index = designedDatas.index(cd)
                data = refinedDatas[index]
                if _type: data = [_type(d) for d in data]
                cd.extend(data)

        else:
            for data in refinedDatas:
                dataColumns = []
                for col in cols:
                    attr = self.propertize(col)

                    if attr == 'month':
                        if getattr(data, attr, None): attr = dict(month='monthYear')
                        else: attr = dict(date='monthYear')
                    elif attr in ['date', 'active']: attr = {attr: 'date'}

                    dataColumns.append(data[attr])
                designedDatas.append(dataColumns)

        return designedDatas

    def getTitle(self, date=None, season='', which='', **kwargs):
        if not date: return
        
        obj, _ = self.getObj(date=date, season=season, which=which, **kwargs)

        if not obj: return
        season, which = self._format_season_which(season, which)

        name = obj.name
        title = ''

        dateAttr = ''
        if season == 'week': dateAttr = 'weekMonthYear'

        elif season == 'month':
            dateAttr = 'monthYear'

            title = f'{which.title()} in {date[dateAttr]} of {name}'

        elif season == 'subs':
            if which == 'date': dateAttr = 'date'
            elif which == 'week': dateAttr = 'weekMonthYear'
            elif which == 'month': dateAttr = 'monthYear'
            elif which == 'year': dateAttr = 'year'

            title = f'Subs in {date[dateAttr]} of {name}'

        return title







class DCRecord(Record):
    Managers = ('Rates', 'CardDues', 'Contributions', 'Savings', 'BroughtForwards', 'Balances', 'Debits', 'Commissions', 'BroughtToOffices', 'Deficits', 'Excesses', 'Incomes', 'Transfers', 'Withdrawals', 'Paidouts', 'NormalIncomes')

    def update(self, values={}, first=1):
        if not first: super().update(values, first)

    def delete(self, called=0):
        if called == 0:
            for a in self: a.delete(1)
        super().delete(called)



class DCRepayment(Repayment):

    def delete(self, called=0):
        if called == 0:
            for a in self: a.delete(1)
        self.manager.removeRecord(self, called)




class Rate(DCRecord): pass

class Balance(DCRecord): pass

class BroughtForward(DCRecord): pass

class BroughtToOffice(DCRecord): pass

class CardDue(DCRecord): pass

class Commission(DCRecord): pass

class Contribution(DCRecord):

    def update(self, values={}, first=1):
        mn = 'money'
        money = values.get(mn)
        if money: self.checkNewUpdates(money)
        super().update(values, 0)

        if money: values[mn] = self.money * self.rate

        if first:
            for rec in self: rec.update(values, 0)
        self.manager.update()

    def checkNewUpdates(self, cont):
        total = float(self.manager)
        own = self.money

        minusOwn = total - own

        if (minusOwn + cont) >= 31.0: raise ValueError(f'Updating with {cont} makes the total contributions exceed 31.0 and the current is {total}.')
        else: return True

    @property
    def rate(self): return self.manager.rate

class Paidout(DCRecord): pass

class Withdrawal(DCRecord): pass

class Debit(DCRecord):
    def update(self, values={}, first=1): super().update(values, first)

class Deficit(DCRecord): pass

class Excess(DCRecord): pass

class NormalIncome(DCRecord): pass

class Transfer(DCRecord): pass

class Income(DCRecord): pass

class Saving(DCRecord): pass

class UpfrontRepayment(DCRecord): Manager = 'UpfrontRepaymentsManager'

class UpfrontRepaymentsManager(RecordsManager):
    ObjectType = UpfrontRepayment

    def removeRecord(self, rec, called=0):
        super().removeRecord(rec)
        if called == 0: self.balance()

class Upfront(DCRepayment):
    dueSeason = 'month'
    dueTime = 1
    Manager = 'Upfronts'
    ObjectType = UpfrontRepaymentsManager

    def update(self, values={}, first=1): super().update(values, first)

    @property
    def subs(self): return self[:]









class DCRecordsManager(RecordsManager):
    ObjectType = DCRecord
    ObjectSortClass = DCSort

    def __init__(self, account, lastRecord=False):
        self._lastRecord = lastRecord
        super().__init__(account, date=account.date)

    def __int__(self):
        if self._lastRecord: return int(self.lastMoney)
        else: return super().__int__()

    def __float__(self):
        if self._lastRecord: return float(self.lastMoney)
        else: return super().__float__()

    @property
    def money(self): return float(self)

    def recordsAsRecord(self, records, date):
        if not self._lastRecord: return super().recordsAsRecord(records, date)

        else:
            # print(records[0].date.date, records[0].date.dayName)
            if records:
                numbers = [r.number for r in records]
                mx = max(numbers)
                index = numbers.index(mx)
                rec = records[index]
                return rec

    def balance(self): return self.account.balanceAccount()

    def removeRecord(self, rec, called=0):
        super().removeRecord(rec)
        if called == 0: self.balance()

class Rates(DCRecordsManager):
    ObjectType = Rate
    lowest = 50

    def __init__(self, accounts, rate=0, raw=0):
        super().__init__(accounts, True)
        self.setRate(rate, raw)

    def __int__(self):
        try: return int(self[-1])
        except: return 0

    def __float__(self):
        try: return float(self[-1])
        except: return 0.0

    def payUpBal(self, rate):
        contributions = float(self.account.contributions)
        if rate > self.rate:
            payUpBal = (rate - self.rate) * contributions
            return payUpBal
        return -1

    @classmethod
    def checkRate(cls, rate):
        if rate < cls.lowest: raise DCErrors.RatesError(f'Rate ({rate}) must not be less than {cls.lowest}')
        return True

    def setRate(self, rate, raw=0):
        if not raw: return
        if self.checkRate(rate): self.createRecord(rate)

class Balances(DCRecordsManager):
    ObjectType = Balance

    def __init__(self, account):
        super().__init__(account, True)

class BroughtForwards(DCRecordsManager):
    ObjectType = BroughtForward
    
    def __init__(self, account):
        super().__init__(account, True)

    def createRecord(self, money, **kwargs):
        if money > 0: super().createRecord(money, notAdd=True, newRecord=False, **kwargs)

class BroughtToOffices(DCRecordsManager):
    ObjectType = BroughtToOffice

class CardDues(DCRecordsManager):
    ObjectType = CardDue
    def __init__(self, client, cardDue=True):
        super().__init__(client)
        self.client = client
        if cardDue == True: self.createRecord(100, client.date)

    @property
    def cardDues(self): return self.totalMonies

    @property
    def cardDue(self):
        accs = self.client.accountsManager[:]
        paids = self.cardDues
        d, m = divmod(accs, 12)
        if m: d += 1
        return paids == d * 100

class Commissions(DCRecordsManager):
    ObjectType = Commission

class Contributions(DCRecordsManager):
    ObjectType = Contribution

    def payUp(self, rate, payup):
        payUpBal = self.account.rates.payUpBal(rate)
        if payUpBal != -1:
            if payup == payUpBal: self.account.rates.changeRate(rate)

    def addContribution(self, contribution, note='Note', _type='n',  **kwargs):
        # print(kwargs)
        assert contribution != 0, 'Contributions can not be zero.'
        newContributions = float(self) + contribution
        if newContributions < 32:
            conRec = self.createRecord(contribution, note=note, **kwargs)

            contr = contribution * self.rate
            incRec = self.account.incomes.addIncome(contr, note=note, _type=_type, coRecord=conRec,**kwargs)
            # print('ereq')
            if not self.upfronts.paid:

                repay, remain = self._toUpfrontRepay(contr)
                # print('here')

                # repRec = self.upfrontsrepayUpfront(repay, note=note, coRecord=incRec, **kwargs)
                repRec = self.upfronts.last.addRepayment(repay, note=note, coRecord=incRec, **kwargs)
                # print(repRec)

                note = f'Repay of Upfront Loan. {note}'

                if remain > 0: savRec = self.savings.addSaving(remain, note=note, coRecord=repRec, **kwargs)

            else: savRec = self.savings.addSaving(contr, coRecord=incRec, note=note, **kwargs)
            self.account.balanceAccount(date=conRec.date)
            # print(conRec.date)
            return conRec

        else: raise DCErrors.ContributionsError(f'Contributions will be {newContributions} which is more than 31')

    def _toUpfrontRepay(self, contr):
        out = self.upfronts.outstanding
        money = contr if out > contr else out
        repay, remain = money, contr - money
        return (repay, remain)

    @property
    def rate(self): return self.account.rate
    @property
    def savings(self): return self.account.savings
    @property
    def upfronts(self): return self.account.upfronts

    @property
    def contributed(self): return sum(cont.savings for cont in self)

class Paidouts(DCRecordsManager):
    ObjectType = Paidout

class Withdrawals(DCRecordsManager):
    ObjectType = Withdrawal

class Debits(DCRecordsManager):
    ObjectType = Debit
    lowest = Rates.lowest

    def addDebit(self, toDebit, _type='w', **kwargs):
        if self.checkMoney(toDebit):
            balance = float(self.account.balances)
            if toDebit <= balance:
                debRec = self.createRecord(toDebit, **kwargs)

                if _type == 'w': debRec.type = self.account.withdrawals.createRecord(toDebit, coRecord=debRec, **kwargs)
                else: debRec.type = self.account.paidouts.createRecord(toDebit, coRecord=debRec, **kwargs)
                return debRec

            else: raise DCErrors.BalancesError(f'Amount {toDebit} to debit is more than balance of {balance}')

class Deficits(DCRecordsManager):
    ObjectType = Deficit

class Excesses(DCRecordsManager):
    ObjectType = Excess

class NormalIncomes(DCRecordsManager):
    ObjectType = NormalIncome

class Transfers(DCRecordsManager):
    ObjectType = Transfer

class Incomes(DCRecordsManager):
    ObjectType = Income

    def addIncome(self, income, _type='n', coRecord=None, **kwargs):
        incRec = self.createRecord(income, coRecord=coRecord, **kwargs)

        if _type == 'n': incRec.type = self.account.normalIncomes.createRecord(income, coRecord=incRec, **kwargs)
        else: incRec.type = self.account.transfers.createRecord(income, coRecord=incRec, **kwargs)

        return incRec

class Savings(DCRecordsManager):
    ObjectType = Saving

    def addSaving(self, saving, **kwargs): return self.createRecord(saving, **kwargs)

class Upfronts(RepaymentsManager):
    ObjectType = Upfront

    def addUpfront(self, upfront, **kwargs):
        rate = self.account.rate
        # savings = self.account.savings
        maxDebit = rate * 30

        if (float(self.account.debits) + float(self) + upfront) > maxDebit: raise DCErrors.UpfrontsError(f'Client\'s debit can\'t be more than {maxDebit}')
        else: return self.createRecord(upfront, **kwargs)

    @property
    def repaidUpfront(self): return self.repaid

    @property
    def overdue(self): return self.outstanding

    @property
    def pendingdUpfronts(self): return self.outstanding

    def repayUpfront(self, upfront, **kwargs): return self.addRepayment(upfront, **kwargs)





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




class Records(list, Object):
    Manager = 'Thrift'

    def __init__(self, thrift):
        Object.__init__(self, thrift)
        list.__init__(self)
        self.thrift = thrift


class Common(PRMP_ClassMixins): col_attr = ['number', {'month': 'monthYear'}, 'Region Name', 'Ledger Number', 'Rate', 'Contributed', 'Income', 'Transfer', 'Paidout', 'Upfront Repay', 'Saved']

DEST = r'C:\Users\Administrator\Documents\GaM OFFICE\DC matters\Contributions'

columns = ['number', 'rate', 'amount', 'money']


class Thrift(Object, Common):
    Manager = 'DailyContribution'

    def __init__(self, manager, clientAccount=None, income=0, money=False, paidout=0, transfer=0, **kwargs):
        assert clientAccount, 'Account must be given'

        assert income or paidout, 'Income or Paidout transactions must be made first.'

        self.account = self.clientAccount = clientAccount
        self.ledgerNumber = clientAccount.ledgerNumber
        
        self._subs = []

        Object.__init__(self, manager, month=self.account.month, **kwargs)
        del self.objectSort

        self.update(transfer=transfer, income=income, money=money, paidout=paidout, reload_=0)

    @property
    def fullSubs(self): return [self.contRecord, self.conTranRecord, self.tranRecord, self.debRecord, self.paidoutRecord]

    @property
    def subs(self):
        self._subs = Records(self)
        for r in self.fullSubs:
            if r: self._subs.append(r)
        return self._subs

    def update(self, transfer=0, income=0, money=False, paidout=0, reload_=1):
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
            self.income = contributed * self.rate
            self.cash = self.income if not transfer else self.income - transfer

        else:
            excess = new - max_
            required = max_ - contribs
            raise ValueError(f'Excess of {excess}, Required [contribution={required}, money={required*self.rate}], current contributions is {contribs}.')

        self.isUpfrontRepay()

        bal = float(self.clientAccount.balances) + self.income
        paidout = float(paidout)
        if paidout <= bal or paidout == 0.0: self.paidout = paidout
        else: raise ValueError(f'Balance is {bal}, but amount to be paidout is {paidout}')

        if reload_: self.updateRecords()

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
    def updated(self): return self.fullSubs.count(None) != len(self.fullSubs)

    @property
    def totals(self):
        less_than = 0.0
        for cont in self.contributions:
            if cont.date <= self.date: less_than += float(cont)
        if not self.contRecord: less_than += self.contributed
        return less_than

    @property
    def saved(self):
        less_than = 0.0
        for cont in self.account.savings:
            if cont.date <= self.date: less_than += float(cont)
        if not self.contRecord: less_than += self.contributed
        return less_than

    @property
    def regionName(self): return self.region.name

    @property
    def region(self): return self.clientAccount.region

    @property
    def rate(self): return self.clientAccount.rate

    def deleteRecords(self):
        for rec in self.subs:
            if rec: rec.delete()

        self.paidoutRecord = None
        self.contRecord = None
        self.tranRecord = None
        self.debRecord = None
        self.conTranRecord = None
        self.account.balanceAccount()

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
        self.records_dict = {}

    @property
    def lastMonths(self):
        thrifts = [thf for thf in self if thf.account.month.monthYearTuple < self.date.monthYearTuple]
        return thrifts
    @property
    def currentMonths(self):
        thrifts = [thf for thf in self if thf.account.month.monthYearTuple == self.date.monthYearTuple]
        return thrifts
    @property
    def nextMonths(self):
        thrifts = [thf for thf in self if thf.account.month.monthYearTuple > self.date.monthYearTuple]
        return thrifts

    @property
    def lastMonthIncome(self): return sum([dc.income for dc in self.lastMonths])
    @property
    def currentMonthIncome(self): return sum([dc.income for dc in self.currentMonths])
    @property
    def nextMonthIncome(self): return sum([dc.income for dc in self.nextMonths])

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

        rec_key = f'{int(ledgerNumber)}, {month.monthYear}'

        if rec_key in self.records_dict: raise ValueError(f'Client with ledger number: {ledgerNumber} and month: {month.monthYear} already exists.')

        clientAccount = clientAccount or self.getClientAccount(ledgerNumber, account, month)

        if clientAccount:
            clA = super().createSub(clientAccount=clientAccount, date=self.date, **kwargs)
            self.records_dict[rec_key] = clA
            return clA
        else: raise ValueError(f'ClientAccount({month.monthYear}, No. {ledgerNumber}) does not exists.')

    def createThrift(self, ledgerNumber=None, month=None, income=0, money=False, paidout=0, transfer=0, account=None, clientAccount=None): return self.createSub(ledgerNumber, month=month, income=income, money=money, paidout=paidout, transfer=transfer, account=account, clientAccount=clientAccount)

    def getClientAccount(self, ledgerNumber, account=None, month=None):
        month = self.getDate(month)
        account = account or self.accountsManager.getAccount(month=month)

        if account: return account.getClientAccount(ledgerNumber, month=month)

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

        date_validations = [dict(value=True, attr='date', attrMethod='isSameDate', attrMethodParams={'date': date})]

        prevs = self.sort(validations=date_validations)

        if prevs: raise ValueError(f'{self.objectName}({date.date}) already exists.')

        return super().createSub(date=date, **kwargs)

    addDailyC = createSub

    @property
    def accountsManager(self): return self.master.accountsManager


class Contribution(PRMP_ClassMixins):

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


class Contributions(PRMP_ClassMixins):
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

