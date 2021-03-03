from src.backend.core.records_managers import Repayment, PRMP_DateTime, RecordsManager, RepaymentsManager, Record
from .dc_errors import DCErrors

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







