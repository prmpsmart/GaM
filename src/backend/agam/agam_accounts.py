from ..core.accounts import Account, AccountsManager

class AGAMAccount(Account):
    Manager = 'AGAMAccountsManager'


class AGAMAccountsManager(AccountsManager): ObjectType = AGAMAccount





