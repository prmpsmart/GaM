from ....thrift.regions.years import Years
from ....thrift.daily.saving_daily import Saving_Daily
from ...debug.debug import Debug
from .weeks import Weeks, Date, MONTHS_NAMES

class Regions:

    @classmethod
    def same_months_in_years(cls, month_name):
        try: return [[ month for month in year.months if month.name.title() == month_name.title()][0] for year in Years.years]
        except: return []
    @classmethod
    def same_months(cls, month_name):
        months = cls.same_months_in_years(month_name)
        for month in months:
            columns = [month.year, month.total_areas, month.total_clients, month.brought_forwards, month.commissions, month.savings, month.debits, month.not_paids, month.upfronts, month.p_upfronts, month.r_upfronts, month.balances, month.deficits, month.excesses, month.btos]
            yield columns
    @classmethod
    def sum_same_months(cls, months):
        name = months[0].name
        total_areas = 0
        total_clients = 0
        brought_forwards = 0
        commissions = 0
        savings = 0
        debits = 0
        not_paids = 0
        upfronts = 0
        p_upfronts = 0
        r_upfronts = 0
        balances = 0
        btos = 0
        deficits = 0
        excesses = 0
        for month in months:
            total_areas += month.total_areas
            total_clients += month.total_clients
            brought_forwards += month.brought_forwards
            commissions += month.commissions
            savings += month.savings
            debits += month.debits
            not_paids += month.not_paids
            upfronts += month.upfronts
            p_upfronts += month.p_upfronts
            r_upfronts += month.r_upfronts
            balances += month.balances
            btos += month.btos
            deficits += month.deficits
            excesses += month.excesses
        return [name, total_areas, total_clients, brought_forwards, commissions, savings, debits, not_paids, upfronts, p_upfronts, r_upfronts, balances, deficits, excesses, btos]
    @classmethod
    def sum_months_in_years(cls):
        months = MONTHS_NAMES[1:]
        months_datas = []
        for month in months: months_datas.append(cls.sum_same_months(cls.same_months_in_years(month)))
        return months_datas

    @classmethod
    def sum_same_areas(cls, areas):
        try:
            name = areas[0].name
            total_clients = 0
            brought_forwards = 0
            commissions = 0
            savings = 0
            debits = 0
            not_paids = 0
            upfronts = 0
            p_upfronts = 0
            r_upfronts = 0
            balances = 0
            excesses = 0
            deficits = 0
            btos = 0

            for area in areas:
                total_clients += area.total_clients
                brought_forwards += area.brought_forwards
                commissions += area.commissions
                savings += area.savings
                debits += area.debits
                not_paids += area.not_paids
                upfronts += area.upfronts
                p_upfronts += area.p_upfronts
                r_upfronts += area.r_upfronts
                balances += area.balances
                btos += area.btos
                excesses += area.excesses
                deficits += area.deficits
            return [name, total_clients, brought_forwards, commissions, savings, debits, not_paids, upfronts, p_upfronts, r_upfronts, balances, deficits, excesses, btos]

        except: return list(0 for i in range(14))


    @classmethod
    def same_areas_in_year(cls, year, area_number):
        try: int(area_number)
        except: area_number = int(area_number.split("_")[1])
        ars = []
        for month in year:
            for area in month:
                if area.number == area_number: ars.append(area)
        return ars

    @classmethod
    def sum_areas_in_year(cls, year):
        if year.max_areas:
            areas_datas = []
            for num in range(1, year.max_areas + 1): areas_datas.append(cls.sum_same_areas(cls.same_areas_in_year(year, num)))
            return areas_datas

    @classmethod
    def sum_same_areas_in_years(cls, areas_datas):
        name = areas_datas[0][0]
        total_clients = 0
        brought_forwards = 0
        commissions = 0
        savings = 0
        debits = 0
        not_paids = 0
        upfronts = 0
        p_upfronts = 0
        r_upfronts = 0
        balances = 0
        deficits = 0
        excesses = 0
        btos = 0
        for area_data in areas_datas:
            total_clients += area_data[1]
            brought_forwards += area_data[2]
            commissions += area_data[3]
            savings += area_data[4]
            debits += area_data[5]
            not_paids += area_data[6]
            upfronts += area_data[7]
            p_upfronts += area_data[8]
            r_upfronts += area_data[9]
            balances += area_data[10]
            deficits = area_data[11]
            excesses = area_data[12]
            btos = area_data[13]
        return [name, total_clients, brought_forwards, commissions, savings, debits, not_paids, upfronts, p_upfronts, r_upfronts, balances, deficits, excesses, btos]

    @classmethod
    def same_areas_in_years(cls, years_datas, area_number):
        try: int(area_number)
        except: area_number = int(area_number.split("_")[1])
        area_name = "Area_%d"%area_number
        areas_datas = []
        for data in years_datas:
            for area in data:
                if area_name in area: areas_datas.append(area)
        return areas_datas

    @classmethod
    def sum_areas_in_years(cls, years=None):
        try: total_areas = max([max([month.total_areas for month in year.months]) for year in Years.years])
        except: total_areas = 0

        if total_areas:
            years_areas_datas = []
            for year in Years.years: years_areas_datas.append((cls.sum_areas_in_year(year)))

            areas_years_datas = []
            for num in range(1, total_areas + 1):
                sort1 = cls.same_areas_in_years(years_areas_datas, num)
                sort2 = cls.sum_same_areas_in_years(sort1)
                areas_years_datas.append(sort2)

            if years:
                real_datas = []
                for datas in years_areas_datas:
                    index = years_areas_datas.index(datas)
                    real_datas.append([Years.years[index], datas])

                return real_datas

            else: return areas_years_datas

    @classmethod
    def same_areas_year(cls, year, area_name):
        areas = cls.same_areas_in_year(year, area_name)
        for area in areas:
            columns = [area.month_name, area.total_clients, area.brought_forwards, area.commissions, area.savings, area.debits, area.not_paids, area.upfronts, area.p_upfronts, area.r_upfronts, area.balances, area.deficits, area.excesses, area.btos]
            yield columns
    @classmethod
    def same_areas_years(cls, area_name):
        # num = int(area_name.split(" ")[1])
        years_areas_datas = cls.sum_areas_in_years(1)

        areas = []
        if years_areas_datas:
            for datas in years_areas_datas:
                for data in datas[1]:
                    if area_name in data:
                        data[0] = datas[0]
                        areas.append(data)
        return areas

    @classmethod
    def area_name(cls, num): return "Area_{}".format(num)
    @classmethod
    def filter_obj(cls, datas, fil_d):
       def filt_num(g):
           if g[0].number == g[1]: return 1
       def filt_name(g):
           if g[0].name == g[1]: return 1

       try:
           try:
               fil_d + 0
               filterer = filt_num
           except TypeError:
               int(fil_d)
               if len(fil_d) == 4: filterer = filt_name
               else:
                   fil_d = int(fil_d)
                   filterer = filt_num
       except ValueError: filterer = filt_name

       rer = []
       for obj in datas:
           tup = [obj, fil_d]
           rer.append(tup)
       filtered = list(filter(filterer, rer))
       if filtered: return filtered[0][0]

    @classmethod
    def check_number(cls, number):
        test_number = str(number)
        if test_number.isdigit(): return True
        else: return False
    @classmethod
    def number_name(cls, clients_names):
        for index in range(len(clients_names)):
            number = str(index + 1) + ". "
            clients_names[index] = number + clients_names[index]
    @classmethod
    def check_year(cls, year_name):
        year = Years.get(year_name)
        if year: return year
        else:
            message = "{} not found".format(year_name)
            line = 221
            Debug.print_bug(line, message, file=__file__)
    @classmethod
    def check_month(cls, year_name, month_name):
        year = cls.check_year(year_name)
        if year:
            month = cls.filter_obj(year[:], month_name)
            if month: return month
            else:
                message = "Month - {0} is not present in {1}".format(month_name, year_name)
                line = 231
                Debug.print_bug(line, message, file=__file__)
    @classmethod
    def check_area(cls, year_name, month_name, area_number):
        month = cls.check_month(year_name, month_name)
        if month:
            area = cls.filter_obj(month[:], area_number)
            if area: return area
            else:
                message = "There\"s no Area with number ---> {1}".format(area_number)
                line = 241
                Debug.print_bug(line, message, file=__file__)
    @classmethod
    def check_client(cls, year_name, month_name, area_number, number=None, name=None):
        if number:
            if cls.check_number(number):
                area = cls.check_area(year_name, month_name, area_number)
                if area:
                    client = cls.filter_obj(area[:], number)
                    if client: return client
                    else:
                        message = "Client {} not found".format(number)
                        line = 253
                        Debug.print_bug(line, message, file=__file__)
                else:
                    message = "Area_{} not found".format(area_number)
                    line = 257
                    Debug.print_bug(line, message, file=__file__)

        elif name:
            area = cls.check_area(year_name, month_name, area_number)
            if area:
                client = cls.filter_obj(area[:], name)
                if client: return client
                else:
                    message = "Client not found in Area_{}".format(area_number)
                    line = 267
                    Debug.print_bug(line, message, file=__file__)
            else:
                message = "Area_{} not found".format(area_number)
                line = 271
                Debug.print_bug(line, message, file=__file__)

    @classmethod
    def check_area_daily(cls, area_name): return Saving_Daily.get(area_name)
    @classmethod
    def check_daily(cls, area_name, date):
        area = cls.check_area_daily(area_name)
        if area:
            for daily_thrift in area.daily_thrifts:
                if daily_thrift.date == date:
                    return daily_thrift
    @classmethod
    def area_dailies(cls, area):
        area_d = cls.check_area_daily(area.name)
        dates = Weeks.month_dates(area.month)
        if area_d:
            for daily in area_d.dailies:
                if daily.date in dates: yield daily


