from ..core.bases import ObjectSort


class DCColumn:
    _clientsRecMs = ['BroughtForwards', 'Rates', 'Contributions', 'Incomes', 'NormalIncomes', 'Transfers', 'Savings', 'Debits', 'Withdrawals', 'Paidouts', 'Upfronts', 'Balances']
    _areasRecMs = ['BroughtToOffices', 'Excesses', 'Deficits']

    weeks = ["Week"]
    days = ["Day", "Date"]
    specday = ['Week', 'Date']
    specdays = ['Day']
    clients = ["Ledger Number", "Name"] # done

    nums = dict(weeks=1, days=2, specday=2, specdays=1, clients=2)
    dateAttrs = dict(Week='weekName', Day='dayName', Date='date')


    subs = ['Name', 'Date', 'Active']
    subsBig = ['Name', 'Date', 'Month', 'Active']

    subsAttrs = dict(Date='date', Month='monthYear', Active='date')

    @classmethod
    def areas(cls, header):
        cl = cls._clientsRecMs.copy()
        del cl[1]
        cl[1] = 'Commissions'
        ar = cl + cls._areasRecMs
        head = cls.__dict__[header]

        return head + ar

    @classmethod
    def getColumns(cls, header, recMs):
        if recMs == '_areasRecMs': return cls.areas(header)
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


    @classmethod
    def designDatas(cls, season, which, datas, w=''):
        pass


class DCSort(ObjectSort):

    def __init__(self, region):
        super().__init__(region)

    def sortSubsMonthBySeasons(self, *args, attr='month', **kwargs): return self.sortSubsBySeasons(*args, attr=attr, **kwargs)

    def sort_Recs_By_Date(self, date, recs=[]):
        recs = recs or self.object[:]

        sortedRecs = self.sortSubsBySeasons(date, subs=recs, seasons=['date'])
        return sortedRecs

    def getObj(self, date=None, season='', which='', account=0, object_=None, subsAttr=''):
        subsAttr = subsAttr or 'accountsManager'
        obj = object_ or self.object
        season, which = self._format_season_which(season, which)

        w = 'obj'
        if 'DCRegion' in obj.mroStr:
            w = 'man'
            obj = obj[subsAttr]

        elif 'DCAccountsManager' in obj.mroStr: w = 'man'
        elif ('DCAccount' in obj.mroStr) or (obj.className == 'ClientsAccounts'):
            if obj.className == 'AreaAccount': w = 'Aacc'
            elif (obj.className == 'ClientsAccounts'): w = 'AaccC'
            else: w = 'acc'
            account = 0

        if season not in ['years', 'year']:
            if self.checkNumber(account):
                if int(account) != 0:
                    account = int(account) - 1
                    accs = obj.sortSubsByMonth(date)
                    obj = accs[account] if accs else None
                    w = 'acc'

        return [obj, w]

    def getObj_w(self, *args, **kwargs): return self.getObj(*args, **kwargs)[1]

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

    def sort_it(self, date=None, season='', which='', account=0, object_=None, subsAttr='', **kwargs):
        season, which = self._format_season_which(season, which)
        date = self.getDate(date)

        obj, w = self.getObj(date, season=season, which=which, account=account, object_=object_, subsAttr=subsAttr)

        results = []

        if (season == 'subs') or (obj.className == 'ClientsAccounts'):
            if 'A' in w:
                if (obj.className == 'ClientsAccounts'):
                    cl_accs = obj
                    which = season
                else: cl_accs = obj.clientsAccounts

                datas = []
                for acc in cl_accs:
                    data = acc.get_RMs_By_Seasons(date, seasons=[which])
                    if data: datas.append(data)
                results =  datas

            elif w == 'man': results = obj.objectSort.sortSubsBySeasons(date, seasons=[which], **kwargs)

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

    def getColumns(self, season='', which='', w=''):
        num = 0
        columns = []

        if 'acc' in w:
            recMs = '_clientsRecMs'
            if ('A' in w):
                if season == 'subs' or 'C' in w: which = 'clients'
                else: recMs = '_areasRecMs'
            # only for weeks, days, specday, specdays, clients
            num = DCColumn.nums[which]
            columns = DCColumn.getColumns(which, recMs)

        elif w == 'obj' and season != 'subs':
            pass

        elif season == 'subs':
            if which in ['date', 'week']: columns = DCColumn.subs
            elif which in ['month', 'year']: columns = DCColumn.subsBig

        return columns, num

    def getDataByColumns(self, datas, columns, datacols):
        columnsNum = []
        if datas and columns: columnsNum = [datacols.index(c) for c in columns]

        refinedDatas = []

        if columnsNum:
            for data in datas:
                _data = [data[cn] for cn in columnsNum]
                refinedDatas.append(_data)

        return refinedDatas or datas

    def fillColumns(self, season='', which='', columns=[], _type=None, **kwargs):
        datas, w = self.sort_it(season=season, which=which, **kwargs)
        cols, num = self.getColumns(season, which, w)
        designcols, datacols = cols[:num], cols[num:]

        refinedDatas = self.getDataByColumns(datas, columns, datacols)
        # print(refinedDatas)

        designedDatas = []

        if season != 'subs' or w in ['Aacc']:
            case = [data[0] for data in refinedDatas]

            if 'Ledger Number' in designcols: attrs = [dict(account=designcols[0]), dict(region=designcols[1])]

            else: attrs = [dict(date=DCColumn.dateAttrs[col]) for col in designcols]

            designedDatas = [d[attrs] for d in case]

            for cd in designedDatas:
                index = designedDatas.index(cd)
                data = refinedDatas[index]
                if _type: data = [_type(d) for d in data]
                cd.extend(data)

        else:
            for data in refinedDatas:
                dataColumns = []
                for col in cols:
                    attr = self.propertize(col)

                    if attr == 'month':
                        if getattr(data, attr, None): attr = dict(month='monthYear')
                        else: attr = dict(date='monthYear')
                    elif attr in ['date', 'active']: attr = {attr: 'date'}

                    dataColumns.append(data[attr])
                designedDatas.append(dataColumns)

        return designedDatas








