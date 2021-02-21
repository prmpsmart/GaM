

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
    def get_columns(cls, header): return cls.__dict__[header]






