from .coop_records import Expenses, Materials, Savings, Levies, Shares, LoanBonds, CoopErrors
from ..core.accounts import DateTime, Account


class CoopAccount(Account):
    materialCost = 2500
    loanRate = 2
    
    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs,)
    
        self.__levies = Levies(self)
        self.__loanBonds = LoanBonds(self)
        self.__materials = Materials(self, self.materialCost, self.date)
        self.__savings = Savings(self)
        self.__shares = Shares(self)
    @property
    def region(self): return self.manager
    @property
    def levies(self): return self.__levies
    @property
    def loanBonds(self): return self.__loanBonds
    @property
    def loans(self): return [lb.loan for lb in self.loanBonds if lb.loan]
    @property
    def materials(self): return self.__materials
    @property
    def savings(self): return self.__savings
    @property
    def shares(self): return self.__shares
    
    def balanceAccount(self):
        pass

class MemberAccount(CoopAccount):
    Manager = 'Member'
    
    def newLoanBond(self, money, proposedLoan, **kwargs): return self.loanBonds.newLoanBond(money, proposedLoan, **kwargs)
    
    def balanceAccount(self):
        outLevy = self.levies.outstanding
        if outLevy:
            self.levies.addLevy(outLevy)
            self.savings.addSaving(-(outLevy))

    @property
    def validLoan(self):
        self.balanceAccount()
        return int(self.savings) * self.loanRate

class UnitAccount(CoopAccount):
    Manager = 'Unit'
    
    def __init__(self, manager, date=None,  **kwargs):
        super().__init__(manager, date=date,  **kwargs)
        
        
        self.__expenses = Expenses(self)
    
    @property
    def expenses(self): return self.__expenses
