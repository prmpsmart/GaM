from ...utils.debug.debug import Debug


class Years:
    which = "years"
    name = "All_Years"
    years = []
    other_years = []
    years_names = []
    max_areas = 0
    commissions = 0
    debits = 0
    savings = 0
    not_paids = 0
    brought_forwards = 0
    upfronts = 0
    r_upfronts = 0
    p_upfronts = 0
    balances = 0
    total_years = 0
    total_clients = 0
    btos = 0
    excesses = 0
    deficits = 0
    
    def __getitem__(self, num): return self.years[num]
    def __len__(self): return self.total_years
    def __bool__(self): return True
    @classmethod
    def datas(cls): return ["ALL YEARS", cls.total_clients, cls.brought_forwards, cls.commissions,  cls.savings, cls.debits, cls.not_paids, cls.upfronts, cls.p_upfronts, cls.r_upfronts, cls.balances, cls.deficits, cls.excesses, cls.btos]
    @classmethod
    def add(cls, year):
        if year.name in cls.years_names:
            cls.other_years.append(year)
            Debug.print_bug(26, "%s already exists"%year.name, file=__file__)
        else:
            cls.years.append(year)
            cls.years_names.append(year.name)
        cls.update()
    @classmethod
    def delete_year(cls, year):
        if year in cls.years: cls.years.remove(year)
        cls.update()
        
    @classmethod
    def get(cls, name):
        if name in cls.years_names:
            for year in cls.years:
                if year.name == name: return year
    @classmethod
    def update(cls):
        if cls.years:
            cls.total_years = len(cls.years)
            cls.years_names = [year.name for year in cls.years]
            cls.commissions = sum([year.commissions for year in cls.years])
            cls.debits = sum([year.debits for year in cls.years])
            cls.brought_forwards = sum([year.brought_forwards for year in cls.years])
            cls.upfronts = sum([year.upfronts for year in cls.years])
            cls.r_upfronts = sum([year.r_upfronts for year in cls.years])
            cls.p_upfronts = sum([year.p_upfronts for year in cls.years])
            cls.balances = sum([year.balances for year in cls.years])
            cls.savings = sum([year.savings for year in cls.years])
            cls.not_paids = sum([year.not_paids for year in cls.years])
            cls.total_clients = sum([year.total_clients for year in cls.years])
            cls.btos = sum([year.btos for year in cls.years])
            cls.excesses = sum([year.excesses for year in cls.years])
            cls.deficits = sum([year.deficits for year in cls.years])
            cls.max_areas = max([year.max_areas for year in cls.years])




