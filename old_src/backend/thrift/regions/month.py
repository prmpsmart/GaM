from ...utils.debug.debug import Debug
from ...utils.sort.thrift.weeks import Weeks

class Month:
    which = "month"
    def __init__(self, year, name, sole=0):
        self.month = self
       # Records
        self.total_areas = 0
        self.total_clients = 0
        self.commissions = 0
        self.savings = 0
        self.debits = 0
        self.not_paids = 0
        self.brought_forwards = 0
        self.upfronts = 0
        self.balances = 0
        self.r_upfronts = 0
        self.p_upfronts = 0
        self.btos = 0
        self.excesses = 0
        self.deficits = 0
       # Details
        self.name = name
        self.areas = []
        self.areas_numbers = []
        self.areas_names = []
        self.year = year
        self.year_name = self.year.name
        self. number = self.year.add_month(self)
       # Dates
        self.commissions_days = {}
        self.debits_dates = {}
        self.savings_dates = {}
        self.upfronts_dates = {}
        self.not_paids_dates = {}
        self.balances_dates = {}
        self.client_dates = {}
        self.brought_forwards_dates = {}
        self.r_upfronts_dates = {}
        self.p_upfronts_dates = {}
        self.savings_dates = {}
        self.btos_dates = {}
        self.excesses_dates = {}
        self.deficits_dates = {}
       #
        if not sole: self.year.update()
       
    # Details
    def __repr__(self): return "Month_" + self.name + " | " + repr(self.year)
    def __str__(self): return self.name + " | " + str(self.year)
    def __getitem__(self, num): return self.areas[num]
    def __len__(self): return self.total_areas
    def __bool__(self): return True
    def delete(self, up=False):
        ln, msg = 47
        Debug.print_bug(str(self) + " DELETED", file=__file__)
        if up: self.year.delete_month(self)
        for area in self.areas: area.delete()
        del self
        Debug.print_bug(ln, msg, file=__file__)
    
    def datas(self): return [self.name, self.total_areas, self.total_clients, self.brought_forwards, self.commissions, self.savings, self.debits, self.not_paids, self.upfronts, self.p_upfronts, self.r_upfronts, self.balances, self.deficits, self.excesses, self.btos]
    
    def add(self, area):
        self.areas.append(area)
        self.total_areas = len(self.areas)
        area_name = "Area_%d" % self.total_areas
        self.areas_names.append(area_name)
        return [self.total_areas, area_name]
    
    def delete_area(self, area, sole=0):
        self.areas.remove(area)
        self.update(sole)
    
    def update(self, sole=0):
        if self.areas:
            self.total_areas = len(self.areas)
            self.areas_names = [area.name for area in self.areas]
            self.commissions = sum([area.commissions for area in self.areas])
            self.debits = sum([area.debits for area in self.areas])
            self.brought_forwards = sum([area.brought_forwards for area in self.areas])
            self.upfronts = sum([area.upfronts for area in self.areas])
            self.r_upfronts = sum([area.r_upfronts for area in self.areas])
            self.p_upfronts = sum([area.p_upfronts for area in self.areas])
            self.balances = sum([area.balances for area in self.areas])
            self.total_clients = sum([area.total_clients for area in self.areas])
            self.savings = sum([area.savings for area in self.areas])
            self.not_paids = sum([area.not_paids for area in self.areas])
            self.btos = sum([area.btos for area in self.areas])
            self.excesses = sum([area.excesses for area in self.areas])
            self.deficits = sum([area.deficits for area in self.areas])
            
            Weeks.update_month_dates(self)
        
            if not sole: self.year.update()
    
    def get(self, name):
        for area in self.areas:
                if area.name == name: return area

