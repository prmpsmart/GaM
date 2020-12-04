from ..core.accounts import Account, AccountsManager
from ..dc.dc_accounts import AreaAccount, AreaAccountsManager
from ..coop.coop_accounts import UnitAccount


class CoopOfficeAccount(UnitAccount):
    Manager = 'CoopOffice'


class DCOfficeAccount(AreaAccount):
    Manager = 'DCOfficeAccountsManager'


class DCOfficeAccountsManager(AreaAccountsManager):
    ObjectType = DCOfficeAccount
