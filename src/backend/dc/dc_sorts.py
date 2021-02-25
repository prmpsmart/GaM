from ..core.bases import ObjectSort


class DCColumn:
    _clientsRecMs = ['BroughtForwards', 'Rates', 'Contributions', 'Incomes', 'NormalIncomes', 'Transfers', 'Savings', 'Debits', 'Withdrawals', 'Paidouts', 'Upfronts', 'Balances']
    _areasRecMs = ['BroughtToOffices', 'Excesses', 'Deficits']

    weeks = ["Week"]
    days = ["Day", "Date"]
    specday = ['Week', 'Date']
    specdays = ['Day']

    clients = ["Ledger Number", "Name"]

    subs = ['Name', 'Date', 'Active']
    subsBig = ['Name', 'Date', 'Month', 'Active']



    @classmethod
    def areas(cls):
        cl = cls._clients.copy()
        del cl[1]
        cl[1] = 'Commissions'
        ar = cl + cls._areas
        return ar

    @classmethod
    def getColumns(cls, header, recMs):
        head = cls.__dict__[header]
        reg = cls.__dict__[recMs]

        return head + reg

    @classmethod
    def merge(cls, one, two):
        n = cls.getColumns(one) + cls.getColumns(two)
        return n

    @classmethod
    def getObjColumns(cls, obj, season, which):
        if 'DCAccount' in obj.mroStr:
            recMs = '_clientsRecMs' if obj.className == 'ClientAccount' else '_areasRecMs'

            if season in ['month', 'week']:
                normal = 0
                if 'spec' not in which: normal = 1

                if normal: return cls.getColumns(which, recMs)
                
            elif season == 'subs':
                if which in ['date', 'week']: pass
                elif which in ['month', 'year']: pass



class DCSort(ObjectSort):

    def __init__(self, region):
        super().__init__(region)

    def sortSubsMonthBySeasons(self, *args, attr='month', **kwargs): return self.sortSubsBySeasons(*args, attr=attr, **kwargs)

    def sort_Recs_By_Date(self, date, recs=[]):
        recs = recs or self.object[:]

        sortedRecs = self.sortSubsBySeasons(date, subs=recs, seasons=['date'])
        return sortedRecs

    def getObj(self, date, season='', which='', account=0, object_=None):
        obj = object_ or self.object
        season, which = self._format_season_which(season, which)


        w = 'obj'
        if 'DCRegion' in obj.mroStr:
            if season != 'subs':
                obj = obj.accountsManager
                w = 'acm'
        elif 'DCAccountsManager' in obj.mroStr: w = 'acm'
        elif 'DCAccount' in obj.mroStr:
            if obj.className == 'AreaAccount': w = 'Aacc'
            else: w = 'acc'
            account = 0

        # else: print(obj)

        if season not in ['years', 'year']:
            if self.checkNumber(account):
                if int(account) != 0:
                    account = int(account) - 1
                    accs = obj.sortSubsByMonth(date)
                    obj = accs[account] if accs else None
                    w = 'acc'

        return [obj, w]

    def _format_season_which(self, season, which):
        # season = season or 'month'
        season = season.lower() or 'month'
        which = which.lower()

        subs = 'subs'
        ret = [season, which]

        if season in ['date', 'day', 'year']: ret[1] = subs
        elif season == 'week':
            if which != 'days': ret[1] = subs
        elif season == 'month':
            if not which: ret[1] = 'days'

        return ret

    def sort_it(self, date, season='', which='', account=0, object_=None, **kwargs):
        season, which = self._format_season_which(season, which)

        obj, w = self.getObj(date, season=season, which=which, account=account, object_=object_)

        # print(season, which, obj.name, w)

        results = []

        if season == 'subs':
            if w == 'Aacc':
                cl_accs = obj.clientsAccounts

                datas = []
                for acc in cl_accs:
                    data = acc.get_RMs_By_Seasons(date, seasons=[which])
                    if data: datas.append(data)
                results =  datas

            else: results =  obj.objectSort.sortSubsBySeasons(date, seasons=[which], **kwargs)

        else:

            if w == 'acc':
                which = which or 'days'

                if season == 'month':
                    if which == 'weeks':
                        weekDates = date.oneDateInWeeks
                        weekDatas = []

                        for week in weekDates:
                            datas = obj.get_RMs_By_Seasons(week, seasons=['year', 'month', 'week'])
                            if datas: weekDatas.append(datas)
                        results =  weekDatas

                    elif which == 'days':
                        days = date.monthOnlyDates
                        daysDatas = []

                        for day in days:
                            datas = obj.get_RMs_By_Date(day)
                            if datas:
                                daysDatas.append(datas)
                        results =  daysDatas

                    elif which == 'specdays':
                        specdays = date.specDaysDates
                        specDatas = []

                        for spec in specdays:
                            datas = obj.get_RMs_By_Seasons(spec, seasons=['month', 'dayName'])
                            if datas: specDatas.append(datas)
                        results =  specDatas

                    elif which == 'specday':
                        specdays = date.allSpecDaysDates[date.weekDay]
                        specDatas = []

                        for spec in specdays:
                            datas = obj.get_RMs_By_Seasons(spec, seasons=['date'])
                            if datas: specDatas.append(datas)
                        results =  specDatas

                elif season == 'week':
                    days = date.weekDates[date.week-1]
                    datas = []

                    for d in days:
                        data = obj.get_RMs_By_Date(d)
                        if data: datas.append(data)
                    results =  datas

        return results, w
        # return obj, results, w

    def getColumns(self, season, which, w):
        if w == 'acc':
            pass
        elif w == 'Aacc': return DCColumn.getColumns('clients', '_clientsRecMs')
        elif w == 'obj' and season == 'subs':
            if which in ['date', 'week']: pass
            elif which in ['month', 'year']: pass

    def designDatas(self, datas, season, which, w):
        pass







