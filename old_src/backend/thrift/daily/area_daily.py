from .saving_daily import Saving_Daily
from .daily import Daily
from ...utils.sort.date import Date

class Area_Daily:
    def __repr__(self): return f"{self.name} Daily"
    def __str__(self): return f"{self.name} Daily"
    def __init__(self, name):
        self.name = name
        self.dailies = []
        self.dailies_dates = []
        Saving_Daily.add(self)
        
    def add(self, daily):
        if daily.date in self.dailies_dates: pass
        else:
            self.dailies.append(daily)
            self.dailies_dates.append(daily.date)

    def today_daily(self, area):
        date = Date.date(form=1)
        if date in self.dailies_dates:
            for daily in self.dailies:
                if daily.date == date: return daily
        else:
            new_daily = Daily(self, area, date)
            self.dailies.append(new_daily)
            self.dailies_dates.append(date)
            return new_daily
    
    def get(self, date):
        if date in self.dailies_dates:
            for daily in self.dailies:
                if daily.date == date: return daily


