from ..core.accounts import Account, AccountsManager


class OfficeAccount(Account):
    pass

class OfficeAccountsManager(AccountsManager):
    accountClass = OfficeAccount

class CoopOfficeAccount(OfficeAccount):
    pass

class CoopOfficeAccountsManager(OfficeAccountsManager):
    accountClass = CoopOfficeAccount

class DCOfficeAccount(OfficeAccount):
    pass

class DCOfficeAccountsManager(OfficeAccountsManager):
    accountClass = DCOfficeAccount
