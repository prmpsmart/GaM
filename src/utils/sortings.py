
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

class Days:

    @classmethod
    def day_sort(cls, dates, date):
        try: return dates[date]
        except KeyError: return 0
    @classmethod
    def day_sorts(cls, details, date):
        for detail in details:
            index = details.index(detail)
            if isinstance(detail, dict): details[index] = cls.day_sort(detail, date)
        return details
    @classmethod
    def day_column(cls, region, date):
        if region.which == "client": columns = [region.number, region.name, region.brought_forwards_dates, region.rate_date, region.thrifts_dates, region.savings_dates, region.debits_dates, region.not_paids_dates, region.upfronts_dates, region.p_upfronts_dates, region.r_upfronts_dates, region.balances_dates]
        elif region.which in ["area", "month"]: columns = [region.name, region.clients_dates, region.brought_forwards_dates, region.commissions_dates, region.savings_dates, region.debits_dates, region.not_paids_dates, region.upfronts_dates, region.p_upfronts_dates, region.r_upfronts_dates, region.balances_dates, region.deficits_dates, region.excesses_dates, region.btos_dates]

        cls.day_sorts(columns, date)
        return columns
    @classmethod
    def daily_sort(cls, region, week=None):
        if region.which == "month": month = region
        else: month = region.month
        if week: dates_days = Weeks.get_week_day(month, week)
        else: dates_days = Weeks.month_dates(month, "date_day")
        for date in dates_days:
            col = cls.day_column(region, date[0])
            col.insert(0, date[0])
            col[1]= date[1]
            yield col
    @classmethod
    def month_day_columns(cls, region=None, day=None):
        if region.which != "month": month = region.month
        else: month = region
        spec_dates = Weeks.a_day_in_weeks(month, day)
        cols = []
        for date in spec_dates:
            col = cls.day_column(region, date)
            col[0] = date
            cols.append(col)
        return cols

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

class Weeks:
    weeks = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Unknown"]
    @classmethod
    def new_month(cls, month, which):
        month_name = month.name
        index = MONTHS_NAMES[:].index(month_name)
        if which == "previous":
            num = index-1
            if num == 0: return MONTHS_NAMES[-1]
            return MONTHS_NAMES[num]
        elif which == "next":
            num = index+1
            if num == 13: return MONTHS_NAMES[1]
            return MONTHS_NAMES[num]


    @classmethod
    def new_week_month(cls, month, status):
        weeks = cls.get_week(month, 5)
        date = Date.date(form=1)
        num = 0
        if status == "current": num = 1
        elif status == "next": num = 2
        else: num = 0
        if weeks:
            for week in weeks:
                if date in week:
                    wk_num = weeks.index(week) + num
                    if wk_num > 0 and wk_num < 6: return [month, "Week %d" % (wk_num)]
                    elif wk_num == 0:
                        nm = cls.new_month(month, "previous")
                        pre_month = month.year.get(nm)
                        if pre_month: return [pre_month, "Week 5"]
                    elif wk_num == 6:
                        nm = cls.new_month(month, "next")
                        next_month = month.year.get(nm)
                        if next_month: return [next_month, "Week 1"]
        return ["", ""]
    @classmethod
    def get_week_tuple(cls, month, num):
        try: int(num)
        except: num = cls.weeks.index(num.title())
        "get month weeks as list of tuples of (date, day_num)"
        weeks_tuples = cls.month_weekdays(month.year.intstr(), month.name, "weeks_tuples")
        if num <= 4:return weeks_tuples[num]
        else: return weeks_tuples
    @classmethod
    def get_week_day(cls, month, num):
        try: int(num)
        except: num = cls.weeks.index(num.title())
        "get month weeks as list of tuples of (date, day_name)"
        weeks_days = cls.month_weekdays(month.year.intstr(), month.name, "weeks_days")
        if num <= 4:return weeks_days[num]
        else: return weeks_days
    @classmethod
    def get_week(cls, month, num):
        try: int(num)
        except: num = cls.weeks.index(num.title())
        "get month weeks dates"
        if month:
            weeks = cls.month_weekdays(month.year.intstr(), month.name, "weeks")
            if num <= 4: return weeks[num]
            else: return weeks
    @classmethod
    def month_dates(cls, month, which="date"):
        weeks = []
        if which == "date": which = "weeks"
        elif which == "date_day": which = "weeks_days"
        for week in cls.month_weekdays(month.year.intstr(), month.name, which): weeks += week
        return weeks
    @classmethod
    def sort_dates_to_weeks(cls, month, dates):
        "to sort amount dates into weeks"
        weeks_dicts = cls.month_weekdays(month.year.intstr(), month.name, "weeks_dicts")
        week1_dict = weeks_dicts[0]
        week2_dict = weeks_dicts[1]
        week3_dict = weeks_dicts[2]
        week4_dict = weeks_dicts[3]
        try: week5_dict = weeks_dicts[4]
        except: week5_dict = dict(n=6, m=8)
        unknown = {}
        for date in dates:
            if date in week1_dict: week1_dict[date] += dates[date]
            elif date in week2_dict: week2_dict[date] += dates[date]
            elif date in week3_dict: week3_dict[date] += dates[date]
            elif date in week4_dict: week4_dict[date] += dates[date]
            elif date in week5_dict: week5_dict[date] += dates[date]
            else:
                if date in unknown: unknown[date] += dates[date]
                else: unknown[date] = dates[date]
        return [week1_dict, week2_dict, week3_dict, week4_dict, week5_dict, unknown]
    @classmethod
    def sum_month_dates(cls, month, dates):
        "to sum and sort the return of {sort_dates_to_weeks}"
        weeks_dicts = cls.sort_dates_to_weeks(month, dates)
        sum_week1_dict = cls.sum_week_dict(weeks_dicts[0])
        sum_week2_dict = cls.sum_week_dict(weeks_dicts[1])
        sum_week3_dict = cls.sum_week_dict(weeks_dicts[2])
        sum_week4_dict = cls.sum_week_dict(weeks_dicts[3])
        sum_week5_dict = cls.sum_week_dict(weeks_dicts[4])
        unknown = cls.sum_week_dict(weeks_dicts[5])
        return [sum_week1_dict, sum_week2_dict, sum_week3_dict, sum_week4_dict, sum_week5_dict, unknown]
    @classmethod
    def sum_week_dict(cls, week_dict): return sum(list(week_dict.values()))
    @classmethod
    def month_weekdays(cls, year, month, which):
        "getting the weeks in a month as according to (which)"
        year = int(year)
        month = MONTHS_NAMES[:].index(month) + 1
        ca = Calendar()
        date_fmt = "%d/%m/%Y"
        month_wks = ca.monthdatescalendar(year, month)
        month_wks2 = ca.monthdays2calendar(year, month)

        weeks_tuples = []
        weeks = []
        weeks_dicts = []
        weeks_days = []
        for week in month_wks:
            week_index = month_wks.index(week)
            w_d_days = []
            weeks_dates = []
            week_dict = {}
            week_days = []
            for day in week:
                day_index = week.index(day)
                day_name = DAYS_NAMES[day_index]
                date = day.strftime(date_fmt)
                weeks_dates.append(date)
                week_day = month_wks2[week_index][day_index][1]
                d_d_w = (date, week_day)
                w_d_days.append(d_d_w)
                week_dict.update({date:0})
                week_days.append((date,day_name))

            weeks.append(weeks_dates)
            weeks_tuples.append(w_d_days)
            weeks_dicts.append(week_dict)
            weeks_days.append(week_days)

        if which == "weeks": return weeks
        elif which == "weeks_tuples": return weeks_tuples
        elif which == "weeks_dicts": return weeks_dicts
        elif which == "weeks_days":  return weeks_days
    @classmethod
    def update_area_dates(cls, area):
        "updating the records dates of an Area_class from the respective Client_class amount dates"
        area.clients_dates = cls.add_clients_dates([client.client_date for client in area.clients])
        area.savings_dates = cls.add_clients_dates([client.savings_dates for client in area.clients])
        area.debits_dates = cls.add_clients_dates([client.debits_dates for client in area.clients])
        area.not_paids_dates = cls.add_clients_dates([client.not_paids_dates for client in area.clients])
        area.upfronts_dates = cls.add_clients_dates([client.upfronts_dates for client in area.clients])
        area.brought_forwards_dates = cls.add_clients_dates([client.brought_forwards_dates for client in area.clients])
        area.balances_dates = cls.add_clients_dates([client.balances_dates for client in area.clients])
        area.commissions_dates = cls.add_clients_dates([client.rate_date for client in area.clients])
        area.r_upfronts_dates = cls.add_clients_dates([client.r_upfronts_dates for client in area.clients])
        area.p_upfronts_dates = cls.add_clients_dates([client.p_upfronts_dates for client in area.clients])
    @classmethod
    def update_month_dates(cls, month):
        "updating the records dates of an Month_class from the respective Area_class amount dates"
        month.clients_dates = cls.add_clients_dates([area.clients_dates for area in month.areas])
        month.savings_dates = cls.add_clients_dates([area.savings_dates for area in month.areas])
        month.debits_dates = cls.add_clients_dates([area.debits_dates for area in month.areas])
        month.not_paids_dates = cls.add_clients_dates([area.not_paids_dates for area in month.areas])
        month.upfronts_dates = cls.add_clients_dates([area.upfronts_dates for area in month.areas])
        month.brought_forwards_dates = cls.add_clients_dates([area.brought_forwards_dates for area in month.areas])
        month.balances_dates = cls.add_clients_dates([area.balances_dates for area in month.areas])
        month.commissions_dates = cls.add_clients_dates([area.commissions_dates for area in month.areas])
        month.p_upfronts_dates = cls.add_clients_dates([area.p_upfronts_dates for area in month.areas])
        month.r_upfronts_dates = cls.add_clients_dates([area.r_upfronts_dates for area in month.areas])
        month.btos_dates = cls.add_clients_dates([area.btos_dates for area in month.areas])
        month.excesses_dates = cls.add_clients_dates([area.excesses_dates for area in month.areas])
        month.deficits_dates = cls.add_clients_dates([area.deficits_dates for area in month.areas])
    @classmethod
    def update_client_dates(cls, root, child):
        "updating the records dates of a Client_class"
        for date in child:
            if date in root:  root[date] += child[date]
            else: root[date] = child[date]
        # return root
    @classmethod
    def add_clients_dates(cls, children):
        "updating the records dates of a Client_class from the daily input"
        added = {}
        for child in children:
            for date in child:
                if date in added:  added[date] += child[date]
                else: added[date] = child[date]
        return added
    @classmethod
    def a_day_in_weeks(cls, month, day_name):
        "a specific day in weeks of a Month_class"
        month_weeks = cls.get_week(month, 5)
        day_num = DAYS_NAMES[:].index(day_name.title())
        spec_day_dates = [week[day_num] for week in month_weeks]
        return spec_day_dates
    @classmethod
    def a_week_in_months(cls, year, week_num, which):
        "sort a specific week in months in Year_class"
        months = year.months_names
        months_weeks = [cls.month_weekdays(year.intstr(), month, which) for month in months]
        spec_week = [weeks[week_num-1] for weeks in months_weeks]
        return spec_week
    @classmethod
    def sort_day_amount_in_weeks_dict(cls, month, day_name, dates_dict):
        "the amount of a specific day in a group of weeks"
        spec_day_dates = cls.a_day_in_weeks(month, day_name)
        spec_day_dict = {}
        for date in dates_dict:
            if date in spec_day_dates: spec_day_dict[date] = dates_dict[date]
        return spec_day_dict

    @classmethod
    def week_sort(cls, month, dates, week):
        try: num = cls.weeks.index(week.title())
        except Exception as e: num = -1
        return cls.sum_month_dates(month, dates)[num]
    @classmethod
    def week_sorts(cls, month, details, week):
        for detail in details:
            index = details.index(detail)
            if isinstance(detail, dict): details[index] = cls.week_sort(month, detail, week)
        return details

    @classmethod
    def week_column(cls, region, week):
        month = region.month
        if region.which == "client": column = [region.number, region.name, region.brought_forwards_dates, region.rate_date, region.thrifts_dates, region.savings_dates, region.debits_dates,  region.upfronts_dates, region.p_upfronts_dates, region.r_upfronts_dates, region.balances_dates]
        elif region.which in ["area", "month"]: column = [region.name, region.clients_dates, region.brought_forwards_dates, region.commissions_dates, region.savings_dates, region.debits_dates, region.not_paids_dates, region.upfronts_dates, region.p_upfronts_dates, region.r_upfronts_dates, region.balances_dates, region.deficits_dates, region.excesses_dates, region.btos_dates]

        cls.week_sorts(month, column, week)
        return column

    @classmethod
    def year_week_columns(cls, year, week):
        week_columns = []
        for month in year: week_columns.append(cls.week_column(month, week))
        return week_columns
    @classmethod
    def weekly_sort(cls, region):
        try:  month = region.month
        except: month = region
        for week in cls.weeks:
            col = cls.week_column(region, week)
            col[0] = week
            yield col
    @classmethod
    def date_short(cls, date):
        date_list = list(date)
        del date_list[-4:-2]
        return "".join(date_list)
    @classmethod
    def name_short(cls, name): return DAYS_ABBRS[DAYS_NAMES.index(name)]
    @classmethod
    def date_name_string(cls, month, week):
        num = cls.weeks.index(week.title())
        dates_names = cls.get_week_day(month, num)
        strs_date_name = []
        try:
            for date_name in dates_names:
                date, name = date_name

                str_date_name = date + " | " + cls.name_short(name)
                strs_date_name.append(str_date_name)
            return strs_date_name
        except Exception as e:
            return list(range(1,6))
