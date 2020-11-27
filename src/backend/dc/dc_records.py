from src.backend.core.records_managers import Repayment, DateTime, RecordsManager, RepaymentsManager, Record
from .dc_errors import DCErrors

class DCRecord(Record):
    Managers = ('Rates', 'CardDues', 'Contributions', 'Savings', 'BroughtForwards', 'Balances', 'Debits', 'Commissions', '', '')

class DCRepayment(Repayment):
    Managers = ('Upfronts', )

class Contribution(DCRecord):
    
    def __init__(self, manager, contrib, **kwargs):
        self.__contrib = contrib
        
        rate = manager.master.rate
        money = rate * contrib

        super().__init__(manager, money, **kwargs)
    
    def __int__(self): return self.contributed
    
    @property
    def contributed(self): return self.__contrib
    
    @property
    def savings(self): return super().__int__()

class Upfront(DCRepayment):
    dueSeason = 'month'
    dueTime = 1
    Manager = 'Upfronts'








