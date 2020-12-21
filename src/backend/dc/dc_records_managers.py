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
    ObjectType = Rate
    lowest = 50
    
    def __init__(self, accounts, rate):
        super().__init__(accounts, True)
        self.setRate(rate)
        
    def __int__(self):
        try: return int(self[-1])
        except: return 0
    
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
    ObjectType = Balance
    
    def __init__(self, account):
        super().__init__(account, True)

class BroughtForwards(DCRecordsManager):
    ObjectType = BroughtForward
    def __init__(self, account):
        super().__init__(account, True)

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

    def addContribution(self, contribution, note=None, _type='n', **kwargs):
        assert contribution != 0, 'Contributions can not be zero.'
        newContributions = int(self) + contribution
        if newContributions < 32:
            _note = ''
            if not self.upfronts.paid:
                
                out = self.upfronts.outstanding
                
                sav = int(self.savings)
                
                money = sav if out > sav else out
                repay, remain = money, 0 - money
                
                self.upfronts.repayUpfront(repay, note=note, **kwargs)
                _note = f'Repay of Upfront Loan. {note}'
                self.savings.addSaving(remain, note=_note, **kwargs)
            
            else: self.savings.addSaving(contribution * self.account.rate, **kwargs)

            self.createRecord(contribution, note=_note, **kwargs)
            self.account.incomes.addIncome(contribution*self.account.rate, note=_note, _type=_type, **kwargs)
                
            # self.balance()
        else: raise DCErrors.ContributionsError(f'Contributions will be {newContributions} which is more than 31')
    
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
            balance = int(self.account.balances)
            if toDebit <= balance:
                if _type == 'w': self.account.withdrawals.createRecord(toDebit, **kwargs)
                else: self._type = self.account.paidouts.createRecord(toDebit, **kwargs)

                self.createRecord(toDebit, **kwargs)
            else: raise DCErrors.BalancesError(f'Amount {toDebit} to debit is more than balance of {balance}')
   
class Deficits(DCRecordsManager):
    ObjectType = Deficit

class Excesses(DCRecordsManager):
    ObjectType = Excesse

class NormalIncomes(DCRecordsManager):
    ObjectType = NormalIncome

class Transfers(DCRecordsManager):
    ObjectType = Transfer

class Incomes(DCRecordsManager):
    ObjectType = Income

    def addIncome(self, income, _type='n', **kwargs):
        if _type == 'n': self.account.normalIncomes.createRecord(income, **kwargs)
        else: self._type = self.account.transfers.createRecord(income, **kwargs)

        self.createRecord(income, **kwargs)

class Savings(DCRecordsManager):
    ObjectType = Saving

    def __init__(self, account):
        super().__init__(account)
    
    def addSaving(self, saving, **kwargs): self.createRecord(saving, **kwargs)

class Upfronts(RepaymentsManager):
    ObjectType = Upfront
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
    def repaidUpfront(self): return self.repaid
    
    @property
    def overdue(self): return self.outstanding
    
    @property
    def pendingdUpfronts(self): return self.outstanding
    
    def repayUpfront(self, upfront, **kwargs): return self.addRepayment(upfront, **kwargs)



