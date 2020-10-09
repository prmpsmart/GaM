
from .weeks import Weeks
from .days import Days


class Smalling:

    @classmethod
    def thrift_small(cls, region=None, week=None, day=None, month=None):
        columns = []
        if region.which == "client":
            
            if day:
                columns = Days.day_column(region, day)
                columns[0] = (day)
                columns[1] = ("Name", columns[1])
                columns[2] = ("Brought-Fs", columns[2])
                columns[3] = ("Rate", columns[3])
                columns[4] = ("Thrifts", columns[4])
            elif week:
                columns = Weeks.week_column(region, week)
                columns[0] = (week)
                columns[1] = ("Name", columns[1])
                columns[2] = ("Brought-Fs", columns[2])
                columns[3] = ("Rate", columns[3])
                columns[4] = ("Thrifts", columns[4])
            
            else: columns = "Month", ("Client", region.name), ("Brought-Fs", region.brought_forward), ("Rate", region.rate), ("Thrift", region.thrifts), region.savings, region.debit, region.not_paid,region.upfront, region.p_upfront, region.r_upfront, region.balance
        
        elif region.which == "area":
            
            if day:
                columns = Days.day_column(region, day)
                columns[0] = ("Area", columns[0])
                columns[1] = ("Clients", columns[1])
                columns[2] = ("Brought-Fs", columns[2])
                columns[3] = ("Commissions", columns[3])
                columns.insert(0, day)
            elif week:
                columns = Weeks.week_column(region, week)
                
                columns[0] = ("Area", columns[0])
                columns[1] = ("Clients", columns[1])
                columns[2] = ("Brought-Fs", columns[2])
                columns[3] = ("Commissions", columns[3])
                columns.insert(0, week)
            
            else: columns = "Month", ("Area", region.name), ("Clients", region.total_clients), ("Brought-Fs", region.brought_forwards), ("Commissions", region.commissions), region.savings, region.debits, region.not_paids, region.upfronts, region.p_upfronts, region.r_upfronts, region.balances, region.deficits, region.excesses, region.btos

        elif region.which == "month":
            
            if day:
                columns = Days.day_column(region, day)
                columns[0] = "Month", columns[0]
                columns[1] = ("Clients", columns[1])
                columns[2] = ("Brought-Fs", columns[2])
                columns[3] = ("Commissions", columns[3])
                columns.insert(0, day)
            elif week:
                columns = Weeks.week_column(region, week)
                columns[0] = "Month", columns[0]
                columns[1] = ("Clients", columns[1])
                columns[2] = ("Brought-Fs", columns[2])
                columns[3] = ("Commissions", columns[3])
                columns.insert(0, week)
            else: columns = "Month", ("Month", region.name), ("Areas/Clients", f"{region.total_areas}  </>  {region.total_clients}"), ("Brought-Fs", region.brought_forwards), ("Commissions", region.commissions), region.savings, region.debits, region.not_paids, region.upfronts, region.p_upfronts, region.r_upfronts, region.balances, region.deficits, region.excesses, region.btos

        elif region.which == "year": columns = "Year", ("Year", region.name), ("Months/Clients", f"{region.total_months}  </>  {region.total_clients}"), ("Brought-Fs", region.brought_forwards), ("Commissions", region.commissions), region.savings, region.debits, region.not_paids, region.upfronts, region.p_upfronts, region.r_upfronts, region.balances, region.deficits, region.excesses, region.btos
        
        elif region.which == "years": columns = "Years", ("Years", "All YEARS"), ("Years/Clients", f"{region.total_years}  </>  {region.total_clients}"), ("Brought-Fs", region.brought_forwards), ("Commissions", region.commissions), region.savings, region.debits, region.not_paids, region.upfronts, region.p_upfronts, region.r_upfronts, region.balances, region.deficits, region.excesses, region.btos

        return columns




