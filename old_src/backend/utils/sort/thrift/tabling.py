
from .weeks import Weeks
from .days import Days
from .regions import Regions

class Tabling:

    @classmethod
    def thrift_table(cls, header=None, region=None, week=None, day=None, month=None):
        columns = []
        if region.which == "years":
            if header == "years":
                years = region.years
                if years:
                    for year in years:
                        columns = year.datas()
                        yield columns
            elif header == "months":
                columns = Regions.sum_months_in_years()
                if columns:
                    for column in columns: yield column
            elif header == "areas":
                columns = Regions.sum_areas_in_years()
                if columns:
                    for column in columns: yield column

        elif region.which == "year":
            if header == "months":
                months = region.months
                if months:
                    for month in months:
                        columns = month.datas()
                        yield columns
            elif header == "areas":
                columns = Regions.sum_areas_in_year(region)
                if columns:
                    for column in columns: yield column


        elif region.which == "month":
            if header == "areas":
                areas = region.areas
                if areas:
                    for area in areas:
                        if day: columns = Days.day_column(area, day)

                        elif week: columns = Weeks.week_column(area, week)

                        else: columns = area.datas()
                        if columns: yield columns
            elif header == "weeks":
                columns = cls.week_yield(region)
                if columns:
                    for column in columns: yield column
            elif header == "days":
                columns = cls.day_yield(region, week=week)
                if columns:
                    for column in columns: yield column

        elif region.which == "area":
            if header == "clients":
                clients = region.clients
                if clients:
                    for client in clients:
                        if day: columns = Days.day_column(client, day)

                        elif week: columns = Weeks.week_column(client, week)

                        else: columns = client.datas()
                        if columns: yield columns
            elif header == "weeks":
                columns = cls.week_yield(region)
                if columns:
                    for column in columns: yield column
            elif header == "days":
                columns = cls.day_yield(region, week=week)
                if columns:
                    for column in columns: yield column

        elif region.which == "client":
            if header == "clnt_weeks":
                columns = cls.week_yield(region)
                if columns:
                    for column in columns: yield column
                    del columns[1]
                    yield columns
            elif header == "clnt_days":
                columns = cls.day_yield(region, week=week)
                if columns:
                    for column in columns: yield column
                    del columns[2]
                    yield columns

    @classmethod
    def week_yield(cls, region): return Weeks.weekly_sort(region)

    @classmethod
    def day_yield(cls,  region, week=None): return Days.daily_sort(region, week=week)


