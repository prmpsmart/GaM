from ..core.bases import ObjectSort

class DCSort(ObjectSort):

    def __init__(self, region):
        super().__init__(region)

    def sortSubsMonthBySeasons(self, *args, attr='month', **kwargs): return self.sortSubsBySeasons(*args, attr=attr, **kwargs)

    def sort_Recs_By_Date(self, date, recs=[]):
        recs = recs or self.object[:]

        sortedRecs = self.sortSubsBySeasons(date, subs=recs, seasons=['date'])
        return sortedRecs

    def sort_it(self, date, season='', which='', _account=0, object_=None):
        obj = object_ or self.object
        season = season or 'month'
        which = which or 'subs'

        if which == 'subs':
            'will now go to the subs accounts details'
            pass
        else:

            if 'DCRegion' in obj.mroStr:
                obj = obj.accountsManager

                if season not in ['years', 'year']:
                    accounts = obj.sortSubsBySeasons(date, seasons=['month'], attr='month')

                    if isinstance(accounts, list):
                        if _account:
                            _account = int(_account)
                            obj = obj[_account]

                if which == 'subs':
                    pass

            if 'DCAccount' in obj.mroStr:

                if season == 'month':
                    if which == 'weeks':
                        weekDates = date.oneDateInWeeks
                        weekDatas = []

                        for week in weekDates:
                            datas = obj.get_RMs_By_Seasons(week, seasons=['year', 'month', 'week'])
                            if datas: weekDatas.append(datas)
                        return weekDatas

                    elif which == 'days':
                        days = date.monthOnlyDates
                        daysDatas = []

                        for day in days:
                            datas = obj.getRecs_Of_RM_ByDate(day)
                            if datas:
                                daysDatas.append(datas)
                        return daysDatas

                    elif which == 'specdays':
                        specdays = date.specDaysDates
                        specDatas = []

                        for spec in specdays:
                            datas = obj.get_RMs_By_Seasons(spec, seasons=['month', 'dayName'])
                            if datas: specDatas.append(datas)
                        return specDatas

                elif season == 'week':
                    days = date.weekDates[date.week-1]
                    datas = []

                    for d in days:
                        data = obj.get_RMs_By_Seasons(d, seasons=['date'])
                        if data: datas.append(data)
                    return datas

            elif 'DCAccountsManager' in obj.mroStr:

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








