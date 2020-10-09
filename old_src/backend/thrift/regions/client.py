from ...utils.debug.debug import Debug
from ...utils.sort.date import Date
from ...utils.sort.thrift.weeks import Weeks


class Client:
    """Profiles of the clients saving thrifts"""
    which = "client"
    def __init__(self, area, client_name, rate, sole=0):
       # Dates
        date = Date.date(form=1)
        self.client_date = {date: 1}#1
        self.rate_date = {date: rate}#2
        self.savings_dates = {}#3
        self.not_paids_dates = {}#3
        self.thrifts_days = []#4
        self.thrifts_dates = {}#5
        self.debits_dates = {}#6
        self.upfronts_dates = {}#7
        self.brought_forwards_dates = {}#8
        self.balances_dates = {}#9
        self.r_upfronts_dates = {}#10
        self.p_upfronts_dates = {}#11
        
        # Records
        self.thrifts = 0
        self.debit = 0
        self.brought_forward = 0
        self.upfront = 0
        self.balance = 0
        self.savings = 0
        self.not_paid = 0
        self.rate = rate
        self.r_upfront = 0
        self.p_upfront = 0
        
       # Details
        self.name = client_name
        self.area = area
        self.area_number = self.area.number
        self.number = self.area.add_client(self)
        self.area_name = self.area.name
        self.month = self.area.month
        self.month_name = self.month.name
        self.year = self.month.year
        self.year_name = self.year.name
       
        if not sole: self.area.update()
   # Details
    def __trunc__(self): return int(self.number)
    def __repr__(self): return "Client_" + str(self.number) + " | " + repr(self.area)
    def __str__(self): return self.name + " | " + str(self.area)
    def __bool__(self): return True
    def datas(self): return [self.number, self.name, self.brought_forward, self.rate, self.thrifts, self.savings, self.debit, self.not_paid, self.upfront, self.p_upfront, self.r_upfront, self.balance]
    
    def delete(self, up=False):
        ln, msg = 51, str(self) + " DELETED"
        if up: self.area.delete_client(self)
        del self
        Debug.print_bug(ln, msg, file=__file__)

        # Methods for Updating values
    def add_thrift(self, thrift, sole=0):
        if self.thrifts + thrift < 32:
            self.thrifts += thrift
            dates = Date.thrift_day()
            date = dates[1]
            sav_date = {date: self.rate * thrift}
            thf_date = {date: thrift}
            Weeks.update_client_dates(self.thrifts_dates, thf_date)
            for _ in range(thrift): self.thrifts_days.append(dates[0])
            
            if self.p_upfront > 0: Weeks.update_client_dates(self.r_upfronts_dates, sav_date)
            else: Weeks.update_client_dates(self.savings_dates, sav_date)
            #4
            
            self.update(sole)
            return 1
            
        elif thrift == 0:
            message = "There can\"t be 0 thrift"
            line = 76
            Debug.print_bug(line, message, file=__file__)
        else:
            message = "The previous thrifts are {0} and {1} thrifts are needed not {2} thrifts".format(self.thrifts, 31-self.thrifts, thrift)
            line = 80
            Debug.print_bug(line, message, file=__file__)
    
    def add_debit(self, debit, sole=0):
        if self.p_upfront == 0: 
            if self.balance >= debit:
                self.debit += debit
                date = Date.date(form=1)
                deb_date = {date: debit}
                Weeks.update_client_dates(self.debits_dates, deb_date)
                self.update(sole)
                return 1
            else: Debug.print_bug(96, "{0} can\"t be debitted this amount of {1}, because Balance is {2}".format(self, debit, self.balance), file=__file__)
        else: Debug.print_bug(97, "{0} can\"t be debitted because of P_Upfront of {1}".format(self, self.p_upfront), file=__file__)
        
    def add_upfront(self, upfront, sole=0):
        if upfront % self.rate == 0 and self.p_upfront == 0:
            date = Date.date(form=1)
            upf_date = {date: upfront}
            #6
            Weeks.update_client_dates(self.upfronts_dates, upf_date)
            self.upfront += upfront
            self.p_upfront = self.upfront
            self.update(sole)
            return 1
        else: Debug.print_bug(112, "{0} rate is {1}, the upfront must be a multiple of a the client\"s rate not {2}". format(self, self.rate, upfront), __file__)
            
    def add_brought_forward(self, brought_forward, sole=0):
        date = Date.date(form=1)
        brf_date = {date: brought_forward}
        #7
        Weeks.update_client_dates(self.brought_forwards_dates, brf_date)
        self.brought_forward += brought_forward
        self.update(sole)
    
    def update_rate(self, rate, sole=0):
        self.rate = rate
        self.update(sole)

    def update(self, sole=0):
        date = Date.date(form=1)
        rate = 0
        if self.p_upfront > 0:
            diff = self.thrifts * self.rate
            if diff <= self.upfront:
                self.r_upfront = diff
                self.p_upfront = self.upfront - self.r_upfront
                
            else:
                change = diff - self.upfront
                self.r_upfront = self.upfront
                self.p_upfront = self.upfront - self.r_upfront
                
                self.balance = change
                
            pend_upf_date = {date: self.p_upfront}
            Weeks.update_client_dates(self.p_upfronts_dates, pend_upf_date)

        else:
            self.savings = self.thrifts * self.rate
            rate = self.rate
        
        self.balance = self.brought_forward + self.savings - self.upfront - self.debit - self.rate
        self.balances_dates[date] = self.balance
        
        self.not_paid = self.savings - self.debit - rate
        self.not_paids_dates[date] = self.not_paid

        if not sole: self.area.update()
    
    def addable(self, which="", amount=0):
        if which == "thrift":
            if self.thrifts + amount < 32: return 1
        elif which == "debit":
            if self.balance >= amount: return 1
        elif which == "upfront":
            if amount % self.rate == 0 and self.p_upfront == 0: return 1

