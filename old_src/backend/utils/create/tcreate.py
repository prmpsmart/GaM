
from ...thrift.regions.area import Area
from ...thrift.regions.client import Client
from ...thrift.regions.month import Month
from ...thrift.regions.year import Year
from ...thrift.regions.years import Years
from ...thrift.daily.area_daily import Area_Daily

from ...utils.sort.thrift.regions import Regions
from ...utils.sort.date import Date
from ..debug.debug import Debug


class TCreate:
    """Creating new things"""
    @classmethod
    def year(cls, status=None):
        if status == "current":
            year_name = Date.get_year("current")
            if year_name in Years.years_names:
                year = Regions.check_year(year_name)
                Debug.print_bug(53, str(year) + " already  exists", file=__file__)
                return year
            else:
                year =  Year(year_name)
                Debug.print_bug(58, str(year) + " created successfully", file=__file__)
                return year
        elif status == "next":
            year_name = Date.get_year("next")
            if year_name in Years.years_names:
                year = Regions.check_year(year_name)
                Debug.print_bug(64, str(year) + " already  exists", file=__file__)
                return year
            else:
                year =  Year(year_name)
                Debug.print_bug(69, str(year) + " created successfully", file=__file__)
                return year
        else: Debug.print_bug(71, "Set status to \"current\" or \"next\"", file=__file__)
    @classmethod
    def month(cls, status=None):
        if status == "current":
            year = Regions.check_year(Date.get_year(status))
            month_name = Date.get_month(status)
            if month_name in year.months_names:
                month = Regions.check_month(year.name, month_name)
                Debug.print_bug(79, str(month) + " already  exists", file=__file__)
                return month
            else:
                month =  Month(year, month_name)
                Debug.print_bug(84, str(month) + " created successfully", file=__file__)
                return month
        elif status == "next":
            month_y = Date.get_month(status, y_r=True)
            year = Regions.check_year(month_y[1])
            if month_y[0] in year.months_names:
                month = Regions.check_month(year.name, month_y[0])
                Debug.print_bug(91, str(month) + " already  exists", file=__file__)
                return month
            else:
                month =  Month(year, month_y[0])
                Debug.print_bug(1395, str(month) + " created successfully")
                return month
        else: Debug.print_bug(98, "Set status to \"current\" or \"next\"", file=__file__)
    @classmethod
    def area(cls, status=None):
        if status == "current":
            month = Regions.check_month(Date.get_year("current"), Date.get_month("current"))
            if month:
                area = Area(month)
                Debug.print_bug(106, str(area) + " created successfully", file=__file__)
                return area
        elif status == "next":
            if Date.get_month("current") == "December": month = Regions.check_month(Date.get_year("next"), Date.get_month("next"))
            else: month = Regions.check_month(Date.get_year("current"), Date.get_month("next"))
            if month:
                area = Area(month)
                Debug.print_bug(114, str(area) + " created successfully", file=__file__)
                return area
        else: Debug.print_bug(116, "Set status to \"current\" or \"next\"", file=__file__)
    @classmethod
    def client(cls, area_number, client_name, rate, thrift=0, status=None):
        if status == "current":
            area = Regions.check_area(Date.get_year("current"), Date.get_month("current"), area_number)
            if area:
                if Regions.check_number(rate):
                    clnt = Client(area, client_name, rate)
                    if thrift <= 31 and thrift != 0: clnt.add_thrift(thrift)
                    Debug.print_bug(125, str(clnt) + " created successfully", file=__file__)
                    return clnt
                else:
                    message = "Rate must be a number not {}".format(rate)
                    line = 129
                    Debug.print_bug(line, message, file=__file__)
        elif status == "next":
            if Date.get_month("current") == "December": area = Regions.check_area(Date.get_year("next"), Date.get_month("next"), area_number)
            else: area = Regions.check_area(Date.get_year("current"), Date.get_month("next"), area_number)
            if area:
                if Regions.check_number(rate) and Regions.check_number(thrift):
                    clnt = Client(area, client_name, rate)
                    clnt.add_thrift(thrift)
                    Debug.print_bug(138, str(clnt) + " created successfully", file=__file__)
                    return clnt
                else: Debug.print_bug(140, "Rate and Thrift must be a number not {} and {}".format(rate, thrift), file=__file__)
        else: Debug.print_bug(141, "Set status to current or next", file=__file__)

########  Daily
    @classmethod
    def area_daily(cls, area_name):
        ar = Regions.check_area_daily(area_name)
        if ar: return ar
        else: return Area_Daily(area_name)

##### Manual
    @classmethod
    def man_year(cls, year_name):
        year = Regions.check_year(year_name)
        if year: return year
        else: return Year(year_name)

    @classmethod
    def man_month(cls, year_name, month_name):
        year = Regions.check_year(year_name)
        if year:
            if month_name in year.months_names:
                month = Regions.check_month(year.name, month_name)
                return month
            else: return Month(year, month_name)
    @classmethod
    def man_area(cls, year_name, month_name):
        month = Regions.check_month(year_name, month_name)
        if month: return Area(month)
