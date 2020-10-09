

class Column:
    clnt_days = ["Dates", "Days", "Brought-F", "Rate", "Thrifts", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances"]
    clnt_weeks = ["Weeks", "Brought-F", "Rate", "Thrifts", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances"]
    clients = ["S/N", "Clients", "Brought-F", "Rates", "Thrifts", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances"]
    
    areas = ["Areas", "Clients", "Brought-F", "Commissions", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances", "Deficits", "Excesses", "B-T-Os"]
    days = ["Dates", "Days", "Clients", "Brought-F", "Commissions", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances", "Deficits", "Excesses", "B-T-Os"]
    spec_day = ["Dates", "Clients", "Brought-F", "Commissions", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances", "Deficits", "Excesses", "B-T-Os"]
    spec_area_yr = ["Months",  "Clients", "Brought-F", "Commissions", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances", "Deficits", "Excesses", "B-T-Os"]
    spec_area_yrs = ["Years", "Clients", "Brought-F", "Commissions", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances", "Deficits", "Excesses", "B-T-Os"]
    weeks = ["Weeks", "Clients", "Brought-F", "Commissions", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances", "Deficits", "Excesses", "B-T-Os"]
    spec_week = ["Months", "Clients", "Brought-F", "Commissions", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances", "Deficits", "Excesses", "B-T-Os"]
    months = ["Months", "Areas", "Clients", "Brought-F", "Commissions", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances", "Deficits", "Excesses", "B-T-Os"]
    spec_month = ["Years", "Clients", "Brought-F", "Commissions", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances", "Deficits", "Excesses", "B-T-Os"]
    years = ["Years", "Months", "Clients", "Brought-F", "Commissions", "Savings", "Debits", "Not-Paid", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances", "Deficits", "Excesses", "B-T-Os"]
    
    daily = ["S/N", "Clients", "Rate", "Old Thrifts", "Today Thrifts",  "New Savings", "Debits", "R-Upfronts", "Total Savings", "Total Debits", "Total Upfronts"]
    
    @classmethod
    def get_columns(cls, header):
        if header == "clients": return cls.clients
        elif header == "areas": return cls.areas
        elif header == "days": return cls.days
        elif header == "spec_day": return cls.spec_day
        elif header == "weeks": return cls.weeks
        elif header == "spec_week": return cls.spec_week
        elif header == "months": return cls.months
        elif header == "spec_month": return cls.spec_month
        elif header == "years": return cls.years
        elif header == "daily": return cls.daily
        elif header == "clnt_days": return cls.clnt_days
        elif header == "clnt_weeks": return cls.clnt_weeks
        elif header == "spec_area_yr": return cls.spec_area_yr
        elif header == "spec_area_yrs": return cls.spec_area_yrs






