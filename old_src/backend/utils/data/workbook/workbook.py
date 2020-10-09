from xlsxwriter import Workbook as WORKBOOK
from .area_workbook import Area_Workbook
from .month_workbook import Month_Workbook
from .year_workbook import Year_Workbook
from .years_workbook import Years_Workbook, Years
from .daily_workbook import Daily_Workbook
import threading
from ...sort.date import Date
from win32com.client import Dispatch


class Workbook:
    @classmethod
    def run(cls, func, *args):
        thread = threading.Thread(target=func, args=args) if args else threading.Thread(target=func)
        thread.start()
    @classmethod
    def open_wb(cls, region, daily=None):
        file = ""
        if region.which == "years": file = Years_Workbook().path
        elif region.which == "year": file = Year_Workbook(region).path
        elif region.which == "month": file = Month_Workbook(region).path
        elif region.which == "area":
            if daily: file = Daily_Workbook(region).path
            else: file = Area_Workbook(region).path
        if file:
            xl = Dispatch("Excel.Application")
            xl.Visible = True
            wb = xl.Workbooks.Open(file)
    @classmethod
    def all_workbooks(cls):
        years = Years.years
        if years:
            cls.run(Years_Workbook)
            for year in years:
                cls.run(Year_Workbook, year)
                for month in year.months:
                    cls.run(Month_Workbook, month)
                    for area in month.areas:
                        cls.run(Area_Workbook, area)
                        cls.run(Daily_Workbook, area)
    @classmethod
    def cur_year_wb(cls):
        year = Years.get(Date.get_year())
        if year:
            cls.run(Year_Workbook, year)
            for month in year.months:
                cls.run(Month_Workbook, month)
                for area in month.areas:
                    cls.run(Area_Workbook, area)
                    cls.run(Daily_Workbook, area)
    @classmethod
    def cur_month_wb(cls):
       year = Years.get(Date.get_year())
       if year:
           month = year.get(Date.get_month())
           if month:
               cls.run(Month_Workbook, month)
               for area in month.areas:
                   cls.run(Area_Workbook, area)
                   cls.run(Daily_Workbook, area)

        
    

