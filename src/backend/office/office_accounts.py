from ..core.accounts import Account, AccountsManager


class OfficeAccount(Account):
    Manager = 'OfficeAccountsManager'

class OfficeAccountsManager(AccountsManager):
    ObjectType = OfficeAccount

class CoopOfficeAccount(OfficeAccount):
    Manager = 'CoopOfficeAccountsManager'

class CoopOfficeAccountsManager(OfficeAccountsManager):
    ObjectType = CoopOfficeAccount

class DCOfficeAccount(OfficeAccount):
    Manager = 'DCOfficeAccountsManager'

class DCOfficeAccountsManager(OfficeAccountsManager):
    ObjectType = DCOfficeAccount
