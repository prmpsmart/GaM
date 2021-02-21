from ..core.bases import ObjectSort

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






# class Area








