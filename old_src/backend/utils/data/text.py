from ..details.tdetails import TDetails
from ..path import Path


class Text:
    @classmethod
    def write_area_txt(cls, area):
        area_file_path = Path.area_file(area, ext="txt")
        text = str(TDetails.get_area_pd(area))
        with open(area_file_path, "w") as file: file.write(cls)
    @classmethod
    def write_month_txt(cls, month):
        month_file_path = Path.month_file(month, ext="txt")
        text = str(TDetails.get_month_pd(month))
        with open(month_file_path, "w") as file: file.write(cls)
    @classmethod
    def write_year_txt(cls, year):
        year_file_path = Path.year_file(year, ext="txt")
        text = str(TDetails.get_year_pd(year))
        with open(year_file_path, "w") as file: file.write(cls)
    @classmethod
    def write_years_txt(cls):
        years_file_path = Path.years_file(ext="txt")
        text = str(TDetails.get_years_pd())
        with open(years_file_path, "w") as file: file.write(cls)

