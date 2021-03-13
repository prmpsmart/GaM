from prmp.prmp_miscs.prmp_errors import PRMP_Errors

class Errors(PRMP_Errors):
    class RegionsManagerError(Exception): pass
    class DateTimeError(Exception): pass
    class AccountError(Exception): pass
    class AccountsManagerError(Exception): pass
    class RepaymentError(Exception): pass
    class LoanBondsError(Exception): pass
    class LoanRepaymentsError(Exception): pass