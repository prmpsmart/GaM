from ..core.accounts import Account, AccountsManager


class OfficeAccount(Account):
    Manager = 'OfficeAccountsManager'

class OfficeAccountsManager(AccountsManager):
    subClass = OfficeAccount

class CoopOfficeAccount(OfficeAccount):
    Manager = 'CoopOfficeAccountsManager'

class CoopOfficeAccountsManager(OfficeAccountsManager):
    subClass = CoopOfficeAccount

class DCOfficeAccount(OfficeAccount):
    Manager = 'DCOfficeAccountsManager'

class DCOfficeAccountsManager(OfficeAccountsManager):
    subClass = DCOfficeAccount
