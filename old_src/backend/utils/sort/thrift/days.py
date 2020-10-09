from .weeks import Weeks


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





