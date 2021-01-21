from ..core.accounts import Account, AccountsManager

class GaMAccount(Account):
    Manager = 'GaMAccountsManager'


class GaMAccountsManager(AccountsManager): ObjectType = GaMAccount





