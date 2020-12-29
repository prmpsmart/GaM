from ..core.accounts import Account, AccountsManager

class AGAMAccount(Account):
    Manager = 'AGAMAccountsManager'

    @property
    def subs(self): return []

class AGAMAccountsManager(AccountsManager):
    ObjectType = AGAMAccount
    


