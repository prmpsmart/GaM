from ..core.bases import ObjectSort

class DCColumn:
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



class DCSort(ObjectSort):

    def __init__(self, region):
        super().__init__(region)

    def sortSubsMonthBySeasons(self, *args, attr='month', **kwargs): return self.sortSubsBySeasons(*args, attr=attr, **kwargs)

    def sort_Recs_By_Date(self, date, recs=[]):
        recs = recs or self.object[:]

        sortedRecs = self.sortSubsBySeasons(date, subs=recs, seasons=['date'])
        return sortedRecs

    def sort_it(self, date, season='', which='', account=0, object_=None):
        obj = object_ or self.object
        season = season or 'month'

        if which == 'subs':
            'will now go to the subs accounts details'
            pass

        else:
            if 'DCRegion' in obj.mroStr: acm = obj.accountsManager
            elif 'DCAccountsManager' in obj.mroStr: acm = obj
            acc = None

            if season not in ['years', 'year']:
                if self.checkNumber(account):
                    if int(account) != 0:
                        account = int(account) - 1
                        accs = acm.sortSubsByMonth(date)
                        acc = accs[account] if accs else None

            if which == 'subs':
                pass

            if acc:
                which = which or 'days'

                if season == 'month':
                    if which == 'weeks':
                        weekDates = date.oneDateInWeeks
                        weekDatas = []

                        for week in weekDates:
                            datas = acc.get_RMs_By_Seasons(week, seasons=['year', 'month', 'week'])
                            if datas: weekDatas.append(datas)
                        return weekDatas

                    elif which == 'days':
                        days = date.monthOnlyDates
                        daysDatas = []

                        for day in days:
                            datas = acc.getRecs_Of_RM_ByDate(day)
                            if datas:
                                daysDatas.append(datas)
                        return daysDatas

                    elif which == 'specdays':
                        specdays = date.specDaysDates
                        specDatas = []

                        for spec in specdays:
                            datas = acc.get_RMs_By_Seasons(spec, seasons=['month', 'dayName'])
                            if datas: specDatas.append(datas)
                        return specDatas

                elif season == 'week':
                    days = date.weekDates[date.week-1]
                    datas = []

                    for d in days:
                        data = acc.get_RMs_By_Seasons(d, seasons=['date'])
                        if data: datas.append(data)
                    return datas

            else:

                if season == 'year':
                    datas = obj.sortAccountsIntoMonths(date)
                    return datas

                elif season == 'years':
                    if which == 'years':
                        # datas = obj.sortAccountsIntoYears()
                        pass
                    elif which == 'months':
                        pass

                    self.notImp()









