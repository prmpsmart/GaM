from .dc_records import *


class DCRecordsManager(RecordsManager):
    ObjectType = DCRecord
    
    def __init__(self, account, lastRecord=False):
        super().__init__(account)
        self._lastRecord = lastRecord
    
    def __int__(self):
        if self._lastRecord: return self.lastMoney
        else: return super().__int__()
    
    def balance(self): return self.account.balanceAccount()

class Rates(DCRecordsManager):
    lowest = 50
    
    def __init__(self, accounts, rate):
        super().__init__(accounts, True)
        self.setRate(rate)
        
    def __int__(self): return int(self[-1])
    
    def payUpBal(self, rate):
        contributions = int(self.account.contributions)
        if rate > self.rate:
            payUpBal = (rate - self.rate) * contributions
            return payUpBal
        return -1
    
    @classmethod
    def checkRate(cls, rate):
        if rate < cls.lowest: raise DCErrors.RatesError(f'Rate ({rate}) must not be less than {cls.lowest}')
        return True
    
    def setRate(self, rate):
        if self.checkRate(rate): self.createRecord(rate)

class Balances(DCRecordsManager):
    
    def __init__(self, account):
        super().__init__(account, True)
    

class BroughtForwards(DCRecordsManager):
    def __init__(self, account):
        super().__init__(account, True)

class BroughtToOffices(DCRecordsManager): pass
    

class CardDues(DCRecordsManager):
    def __init__(self, account, cardDue=True):
        super().__init__(account)
        if cardDue == True: self.createRecord(100, account.date)
    
    @property
    def cardDues(self): return self.totalMonies

class Commissions(DCRecordsManager): pass

class Contributions(DCRecordsManager):
    ObjectType = Contribution
    
    def __init__(self, account):
        super().__init__(account)
        
        self.__savings = 0
    
    def payUp(self, rate, payup):
        payUpBal = self.account.rates.payUpBal(rate)
        if payUpBal != -1:
            if payup == payUpBal: self.account.rates.changeRate(rate)

    def addContribution(self, contribution, note=None, **kwargs):
        newContributions = int(self) + contribution
        if newContributions < 32:
            self.savings.addSaving(contribution * self.account.rate, **kwargs)
            self.createRecord(contribution, **kwargs)
            
            if not self.upfronts.paid:
                
                out = self.upfronts.outstanding
                
                sav = int(self.savings)
                
                money = sav if out > sav else out
                repay, remain = money, 0 - money
                
                self.upfronts.repayUpfront(repay, note=note, **kwargs)
                self.savings.addSaving(remain, note=f'Repay of Upfront Loan. {note}', **kwargs)
                
            # self.balance()
        else: raise DCErrors.ContributionsError(f'Contributions will be {newContributions} which is more than 31')
    
    # def addContribution(self, contribution, **kwargs):
    #     newContributions = int(self) + contribution
    #     assert contribution != 0, 'Contributions can not be zero.'
    #     if newContributions < 32:
            
    #         self.__savings += contribution * self.account.rate
            
    #         self.createRecord(contribution, **kwargs)
            
            
    #         if not self.upfronts.paid:
    #             out = self.upfronts.outstanding
                
    #             if out > self.__savings:
    #                 self.upfronts.repayUpfront(self.__savings, **kwargs)
    #                 self.__savings = 0
                
    #             else:
    #                 self.upfronts.repayUpfront(out, **kwargs)
    #                 self.__savings = self.__savings - out
                    
    #     else: raise DCErrors.ContributionsError(f'Contributions will be {newContributions} which is more than 31')
    
    # @property
    # def savings(self): return sum([rec.savings for rec in self])
    
    @property
    def upfronts(self): return self.account.upfronts
    
    @property
    def savings(self): return self.account.savings


class Debits(DCRecordsManager):
    lowest = Rates.lowest
    
    def addDebit(self, toDebit, **kwargs):
        if self.checkMoney(toDebit):
            balance = int(self.account.balances)
            if toDebit <= balance: self.createRecord(toDebit, **kwargs)
            else: raise DCErrors.BalancesError(f'Amount {toDebit} to debit is more than balance of {balance}')


class Deficits(DCRecordsManager): pass
    


class Excesses(DCRecordsManager): pass
    


class Savings(DCRecordsManager):
    
    def __init__(self, account):
        super().__init__(account)
    
    def addSaving(self, saving, **kwargs): self.createRecord(saving, **kwargs)



class Upfronts(RepaymentsManager):
    _shortName = 'upf'
    ObjectType = Upfront
    
    def __init__(self, accounts):
        super().__init__(accounts)
    
    def addUpfront(self, upfront):
        rate = self.account.rate
        savings = self.account.savings
        maxDebit = rate * 30
        
        if (int(self.account.debits) + int(self) + upfront) > maxDebit: raise DCErrors.UpfrontsError(f'Client\'s debit can\'t be more than {maxDebit}')
        else: self.createRecord(upfront)
    
    @property
    def repaidUpfronts(self): return self.repaid
    
    @property
    def pendingdUpfronts(self): return self.outstanding
    
    def repayUpfront(self, upfront, **kwargs): return self.addRepayment(upfront, **kwargs)



