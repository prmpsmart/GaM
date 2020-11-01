from src.backend.core.records_managers import Repayment, DateTime, RecordsManager, RepaymentsManager, Record
from .dc_errors import DCErrors

class DCRecord(Record):
    pass

class DCRepayment(Repayment):
    pass

class Contribution(DCRecord):
    
    def __init__(self, manager, contrib, **kwargs):
        rate = manager.manager.rate 
        money = rate * contrib
        self.__contrib = contrib

        super().__init__(manager, money, **kwargs)
    
    @property
    def contributed(self): return self.__contrib


class Upfront(DCRepayment):
    dueSeason = 'month'
    dueTime = 1








