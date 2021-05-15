# from ..core.accounts import Account, AccountsManager
from ..dc.dc_accounts import AreaAccount, AreaAccountsManager
# from ..coop.coop_accounts import UnitAccount


# class CoopOfficeAccount(UnitAccount):
#     Manager = 'CoopOffice'


class DCOfficeAccount(AreaAccount):
    Manager = 'DCOfficeAccountsManager'

    def _balanceAccount(self, date=None):
        areasAccounts = self.manager.sortSubRegionsAccountsByMonth(self.date)
        for a in areasAccounts: a.balanceAccount()
        if areasAccounts:
            self.incomes.updateWithOtherManagers([account.incomes for account in areasAccounts])
            
            self.balances.updateWithOtherManagers([account.balances for account in areasAccounts])
            
            self.broughtForwards.updateWithOtherManagers([account.broughtForwards for account in areasAccounts])
            
            self.commissions.updateWithOtherManagers([account.commissions for account in areasAccounts])
            
            self.debits.updateWithOtherManagers([account.debits for account in areasAccounts])
            
            self.savings.updateWithOtherManagers([account.savings for account in areasAccounts])
            
            self.upfronts.updateWithOtherManagers([account.upfronts for account in areasAccounts])
            
            self.excesses.updateWithOtherManagers([account.excesses for account in areasAccounts])
            
            self.deficits.updateWithOtherManagers([account.deficits for account in areasAccounts])
            
            self.btos.updateWithOtherManagers([account.btos for account in areasAccounts])
        
            self.paidouts.updateWithOtherManagers([account.paidouts for account in areasAccounts])
            
            self.withdrawals.updateWithOtherManagers([account.withdrawals for account in areasAccounts])
            
            self.transfers.updateWithOtherManagers([account.transfers for account in areasAccounts])

            self.normalIncomes.updateWithOtherManagers([account.normalIncomes for account in areasAccounts])


class DCOfficeAccountsManager(AreaAccountsManager):
    ObjectType = DCOfficeAccount
