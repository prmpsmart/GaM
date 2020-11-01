from src.backend.core.records_managers import Repayment, DateTime, RecordsManager, RepaymentsManager, Record
from .dc_errors import DCErrors

class DCRecord(Record):
    Managers = ('Rates', 'CardDues', 'Contributions', 'Savings', 'BroughtForwards', 'Balances', 'Debits', '', '', '')

class DCRepayment(Repayment):
    Managers = ('Upfronts', )

class Contribution(DCRecord):
    
    def __init__(self, manager, contrib, **kwargs):
        rate = manager.master.rate
        money = rate * contrib
        self.__contrib = contrib

        super().__init__(manager, money, **kwargs)
    
    def __int__(self): return self.contributed
    
    @property
    def contributed(self): return self.__contrib


class Upfront(DCRepayment):
    dueSeason = 'month'
    dueTime = 1
    Manager = 'Upfronts'








