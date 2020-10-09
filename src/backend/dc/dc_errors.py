from ..core.errors import Errors


class DCErrors(Errors):
    class UpfrontsError(Exception): pass
    class RatesError(Exception): pass
    class BroughtForwardsError(Exception): pass
    class BalancesError(Exception): pass
    class ContributionsError(Exception): pass
    class AccountsError(Exception): pass








