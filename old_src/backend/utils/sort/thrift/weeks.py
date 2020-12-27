from ....thrift.regions.years import Years
from ..date import DAYS_NAMES, MONTHS_NAMES, DAYS_ABBRS, Calendar, Date


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
                        print(next_month, nm)
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
            print(e)
            return list(range(1,6))
