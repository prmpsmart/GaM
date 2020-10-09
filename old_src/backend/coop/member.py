from ..core.records.loans import Loans
from ..core.records.levies import Levies
from ..core.records.loan_bonds import Loan_Bonds
from ..core.records.materials import Materials
from ..core.records.savings import Savings
from ..core.records.shares import Shares
from ..core.sort.date import Date
from ..core.details import Details


class Member:
    
    def __init__(self, unit, name, gender, tel='', photo=''):
        self.unit = unit
        self.details = Details({"unitName": unit.name, "name": name, "gender": gender, "telephone": tel, "photo": photo})
        self.date = Date.getDMYFromDate(Date.date())

        self.shares = Shares()
        self.savings = Savings
        self.loans = Loans()
        self.materials = Materials()
        self.loan_bonds = Loan_Bonds()
        self.levies = Levies
        
        self.current_levy = None
        self.loan_repayed = 0
        self.pending_loan = 0
        self.entry_fee = 0
        
        self.referral = None
        




