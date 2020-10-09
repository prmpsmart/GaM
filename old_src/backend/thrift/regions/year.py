from .years import Years
from ...utils.debug.debug import Debug


class Year:
    which = "year"
    def __init__(self, name, sole=0):
        self.name = "Year_" + str(name) if "Year_" not in name else name
        self.number = self.name.split("_")[1]
        self.months = []
        self.months_names = []
        self.commissions = 0
        self.debits = 0
        self.savings = 0
        self.not_paids = 0
        self.brought_forwards = 0
        self.upfronts = 0
        self.r_upfronts = 0
        self.p_upfronts = 0
        self.balances = 0
        self.btos = 0
        self.excesses = 0
        self.deficits = 0
        self.total_months = 0
        self.total_clients = 0
        self.max_areas = 0
        Years.add(self)
        
        if not sole: Years.update()
        
        
    def __trunc__(self): return int(self.number)
    def __repr__(self): return self.name
    def __str__(self): return self.name
    def __bool__(self): return True
    def intstr(self): return str(int(self))
    def __getitem__(self, num): return self.months[num]
    def __len__(self): return self.total_months
    
    def datas(self): return [self.name, self.total_months, self.total_clients, self.brought_forwards, self.commissions, self.savings, self.debits, self.not_paids, self.upfronts, self.p_upfronts, self.r_upfronts, self.balances, self.deficits, self.excesses, self.btos]
    
    def delete(self):
        ln, msg = 32, str(self) + " DELETED"
        Years.delete_year(self)
        for month in self.months: month.delete()
        del self
        Debug.print_bug(ln, msg, file=__file__)
    def add_month(self, month):
        if self.total_months <= 12:
            if month in self.months: return "Already added can\"t add again"
            else:
                self.months.append(month)
                self.total_months = len(self.months)
                self.months_names.append(month.name)
                # self.update()
                return self.total_months
    def delete_month(self, month):
        if month in self.months:
            self.months.remove(month)
            self.months_names.remove(month.name)
        self.update()
    def update(self, sole=0):
        if self.months:
            self.total_months = len(self.months)
            self.commissions = sum([month.commissions for month in self.months])
            self.debits = sum([month.debits for month in self.months])
            self.brought_forwards = sum([month.brought_forwards for month in self.months])
            self.upfronts = sum([month.upfronts for month in self.months])
            self.r_upfronts = sum([month.r_upfronts for month in self.months])
            self.p_upfronts = sum([month.p_upfronts for month in self.months])
            self.balances = sum([month.balances for month in self.months])
            self.savings = sum([month.savings for month in self.months])
            self.not_paids = sum([month.not_paids for month in self.months])
            self.total_clients = sum([month.total_clients for month in self.months])
            self.btos = sum([month.btos for month in self.months])
            self.excesses = sum([month.excesses for month in self.months])
            self.deficits = sum([month.deficits for month in self.months])
            self.max_areas = max([month.total_areas for month in self.months])

            if not sole: Years.update()

    def get(self, name):
        for month in self.months:
                if month.name == name: return month

