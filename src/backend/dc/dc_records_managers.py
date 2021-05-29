from .dc_records import *
from .dc_sorts import DCSort


class DCRecordsManager(RecordsManager):
    ObjectType = DCRecord
    ObjectSortClass = DCSort

    def __init__(self, account, lastRecord=False):
        self._lastRecord = lastRecord
        # super().__init__(account, date=account.date)
        super().__init__(account)

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



