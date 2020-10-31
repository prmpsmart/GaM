from ..core.accounts import Account, AccountsManager


class OfficeAccount(Account):
    pass

class OfficeAccountsManager(AccountsManager):
    subClass = OfficeAccount

class CoopOfficeAccount(OfficeAccount):
    pass

class CoopOfficeAccountsManager(OfficeAccountsManager):
    subClass = CoopOfficeAccount

class DCOfficeAccount(OfficeAccount):
    pass

class DCOfficeAccountsManager(OfficeAccountsManager):
    subClass = DCOfficeAccount
