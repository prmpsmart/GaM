from src.backend.core.records_managers import Repayment, DateTime, RecordsManager, RepaymentsManager, Record
from .dc_errors import DCErrors

class DCRecord(Record):
    Managers = ('Rates', 'CardDues', 'Contributions', 'Savings', 'BroughtForwards', 'Balances', 'Debits', 'Commissions', 'BroughtToOffices', 'Deficits', 'Excesses', 'Incomes', 'Transfers', 'Withdrawals', 'Paidouts', 'NormalIncomes')

class DCRepayment(Repayment): pass
    # Managers = ('Upfronts', )



class Rate(DCRecord): pass

class Balance(DCRecord): pass

class BroughtForward(DCRecord): pass

class BroughtToOffice(DCRecord): pass

class CardDue(DCRecord): pass

class Commission(DCRecord): pass

class Contribution(DCRecord): pass

class Paidout(DCRecord): pass

class Withdrawal(DCRecord): pass

class Debit(DCRecord): pass

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




