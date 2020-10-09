from ..core.errors import Errors

class CoopErrors(Errors):
    class LeviesError(Exception): pass
    class LoanBondsError(Exception): pass
    class LoanRepaymentsError(Exception): pass
    class BalancesError(Exception): pass
    class LoansError(Exception): pass
    class MaterialsError(Exception): pass
    class SharesError(Exception): pass
    class SavingsError(Exception): pass
    class UnitError(Exception): pass
