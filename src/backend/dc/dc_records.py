from src.backend.core.records_managers import Repayment, PRMP_DateTime, RecordsManager, RepaymentsManager, Record
from .dc_errors import DCErrors

class DCRecord(Record):
    Managers = ('Rates', 'CardDues', 'Contributions', 'Savings', 'BroughtForwards', 'Balances', 'Debits', 'Commissions', 'BroughtToOffices', 'Deficits', 'Excesses', 'Incomes', 'Transfers', 'Withdrawals', 'Paidouts', 'NormalIncomes')
    def update(self, values={}, first=1):
        if not first: super().update(values, first)


class DCRepayment(Repayment): pass
    # Managers = ('Upfronts', )



class Rate(DCRecord): pass

class Balance(DCRecord): pass

class BroughtForward(DCRecord): pass

class BroughtToOffice(DCRecord): pass

class CardDue(DCRecord): pass

class Commission(DCRecord): pass

class Contribution(DCRecord):
    
    def update(self, values={}, first=1):
        super().update(values, 0)
        values['money'] = self.money * self.manager.rate
        if first:
            for rec in self: rec.update(values, 0)
        self.manager.update()

class Paidout(DCRecord): pass

class Withdrawal(DCRecord): pass

class Debit(DCRecord):
    def update(self, values={}, first=1): super().update(values, first)

class Deficit(DCRecord): pass

class Excesse(DCRecord): pass

class NormalIncome(DCRecord): pass

class Transfer(DCRecord): pass

class Income(DCRecord): pass

class Saving(DCRecord): pass

class Upfront(DCRepayment):
    dueSeason = 'month'
    dueTime = 1
    Manager = 'Upfronts'

    def update(self, values={}, first=1): super().update(values, first)





