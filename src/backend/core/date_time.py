__author__ = 'PRMPSmart@gmail.com'

from datetime import datetime, timedelta, date
from calendar import day_abbr, day_name, month_abbr, month_name, Calendar
from .errors import Errors

DAYS_ABBRS, DAYS_NAMES, MONTHS_ABBRS, MONTHS_NAMES = day_abbr[:], day_name[:], month_abbr[:], month_name[:]


class CompareByDate:
    def __lt__(self, other):
        if other == None: return False
        return self.date < other.date
    def __le__(self, other):
        if other == None: return False
        return self.date <= other.date
    def __eq__(self, other):
        if other == None: return False
        return self.date == other.date
    def __ne__(self, other):
        if other == None: return True
        return self.date != other.date
    def __gt__(self, other):
        if other == None: return True
        return self.date > other.date
    def __ge__(self, other):
        if other == None: return True
        return self.date >= other.date

class CompareByWeek:
    def __lt__(self, other):
        if other == None: return False
        return self.date.weekMonthYearTuple < other.date.weekMonthYearTuple
    def __le__(self, other):
        if other == None: return False
        return self.date.weekMonthYearTuple <= other.date.weekMonthYearTuple
    def __eq__(self, other):
        if other == None: return False
        return self.date.weekMonthYearTuple == other.date.weekMonthYearTuple
    def __ne__(self, other):
        if other == None: return True
        return self.date.weekMonthYearTuple != other.date.weekMonthYearTuple
    def __gt__(self, other):
        if other == None: return True
        return self.date.weekMonthYearTuple > other.date.weekMonthYearTuple
    def __ge__(self, other):
        if other == None: return True
        return self.date.weekMonthYearTuple >= other.date.weekMonthYearTuple

class CompareByMonth:
    def __lt__(self, other):
        if other == None: return False
        return self.date.monthYearTuple < other.date.monthYearTuple
    def __le__(self, other):
        if other == None: return False
        return self.date.monthYearTuple <= other.date.monthYearTuple
    def __eq__(self, other):
        if other == None: return False
        return self.date.monthYearTuple == other.date.monthYearTuple
    def __ne__(self, other):
        if other == None: return True
        return self.date.monthYearTuple != other.date.monthYearTuple
    def __gt__(self, other):
        if other == None: return True
        return self.date.monthYearTuple > other.date.monthYearTuple
    def __ge__(self, other):
        if other == None: return True
        return self.date.monthYearTuple >= other.date.monthYearTuple

class CompareByYear:
    def __lt__(self, other):
        if other == None: return False
        return self.date.year < other.date.year
    def __le__(self, other):
        if other == None: return False
        return self.date.year <= other.date.year
    def __eq__(self, other):
        if other == None: return False
        return self.date.year == other.date.year
    def __ne__(self, other):
        if other == None: return True
        return self.date.year != other.date.year
    def __gt__(self, other):
        if other == None: return True
        return self.date.year > other.date.year
    def __ge__(self, other):
        if other == None: return True
        return self.date.year >= other.date.year

class DateTime(datetime):
    date_fmt = "%d/%m/%Y"
    daysAbbr, daysNames, monthsAbbrs, monthsNames = day_abbr[:], day_name[:], month_abbr[:], month_name[:]
    Error = Errors.DateTimeError
    # the __add__ and __sub__ are implementaions are purely by PRMPSmart@gmail.com
    def __add__(self, add_month):
        if isinstance(add_month, timedelta): return self.createDateTime(obj=super().__add__(add_month))
        
        elif isinstance(add_month, int):
            months = self.month + add_month
            div, mod = divmod(months, 12)
            if (div == 0) or (months == 12):
                # it means that the months falls within the current self.year
                return self.createDateTime(self.year, months, self.day)
            elif div > 0:
                # it means that the new_month falls within the upcoming years
                if not mod:
                    # it means self.month = 12 and sub_month *12
                    mod = 12
                    # the resulting month is 12
                    div -= 1
                    # since self.month = 12 and sub_month *12 therefore div is having an additional self.month 12 in it
                return self.createDateTime(self.year + div, mod, self.day)
        
    def __sub__(self, sub_month):
        if isinstance(sub_month, timedelta): return self.createDateTime(obj=super().__sub__(sub_month))
        
        elif isinstance(sub_month, self.__class__): return self.diffInMonth(sub_month)
        elif isinstance(sub_month, int):
            
            if sub_month < self.month:
                # since sub_month is lower than self.month, the new month is within that same year
                return self.createDateTime(self.year, self.month - sub_month, self.day)
            
            elif sub_month == self.month:
                # since sub_month is equal to self.month, the new month is automatically last month of last year
                return self.createDateTime(self.year - 1, 12, self.day)
            
            # since the above conditions are not met, it means that the sub_month is actually more than self.month which means that the new month is actually in the recent years if not the last one.
            else:
                # since 12 months == 1 year; recent years in the sub_month = sub_month // 12, and the remaining months is sub_month % 12.
                div, mod =  divmod(sub_month, 12)
                
                if div == 0:
                    # the sub_month > self.month but < 12
                    rem = sub_month - self.month
                    #  first minus its exact month from itself, then minus the remaining months
                    first = self - self.month
                    second = first - rem
                    return second
                
                else:
                    # therefore, subtract the recent years from the current year, creating a new DateTime with everything else in place except the year
                    # the sub_month is more than 12
                    year = self.createDateTime(self.year - div, self.month, self.day)
                    # the remaining months will now fall into the categories of (sub_month < self.month) and ( sub_month == self.month).
                    # it will now look as if it's a loop, the remaining months will now be subtracted from the new year-DateTime, the process will now fall into the first two conditions in the new year-DateTime
                    return year - mod
    
    def __str__(self): return self.strftime(self.date_fmt)
    
    @property
    def isLeap(self): return self.year % 4 == 0 and (self.year % 100 != 0 or self.year % 400 == 0)
    
    @property
    def totalDays(self):
        lis = [1, 3, 5, 7, 8, 10, 12]
        if self.month == 2: return 28 + self.isLeap
        elif self.month in lis: return 31
        else: return 30
    
    @classmethod
    def getDayNum(cls, day):
        error = cls.Error(f'day must be among {cls.daysAbbrs} or {cls.daysNames}')
        if isinstance(day, str):
            if day in cls.daysAbbrs: dayNum = cls.daysAbbrs.index(day) + 1
            elif day in cls.daysNames: dayNum = cls.daysNames.index(day) + 1
            else: raise error
            return dayNum
        else: raise error
        
    @classmethod
    def getDayName(cls, day, abbr=False):
        range_ = list(range(1, 31))
        error = cls.Error(f'day must be among {range_}')
        if isinstance(day, int):
            if day in range_:
                if abbr: dayName = cls.daysAbbrs[day - 1]
                else: dayName = cls.daysNames[day - 1]
            else: raise error
            return dayName
        else: raise error
    
    @classmethod
    def checkDateTime(cls, date, dontRaise=False):
        if not isinstance(date, DateTime):
            if dontRaise: return False
            raise cls.Error('Date must be an instance of DateTime')
        return True
    
    @classmethod
    def now(cls): return cls.createDateTime(obj=super().now())
    
    @classmethod
    def getMonthNum(cls, month):
        error = cls.Error(f'month must be among {cls.monthsAbbrs} or {cls.monthsNames}')
        if isinstance(month, str):
            if month in cls.monthsAbbrs: monthNum = cls.monthsAbbrs.index(month)
            elif month in cls.monthsNames: monthNum = cls.monthsNames.index(month)
            else: raise error
            return monthNum
        else: raise error
        
    @classmethod
    def getMonthName(cls, month, abbr=False):
        range_ = list(range(1, 12))
        error = cls.Error(f'month must be among {range_}')
        if isinstance(month, int):
            if month in range_:
                if abbr: monthName = cls.monthsAbbrs[month - 1]
                else: monthName = cls.monthsNames[month - 1]
            else: raise error
            return monthName
        else: raise error
    
    @classmethod
    def createDateTime(cls, year=None, month=1, day=1, auto=False, obj=None, week=None):
        if isinstance(obj, (date, datetime)): return cls(obj.year, obj.month, obj.day)
        
        if auto: return cls.now()
        
        if week:
            assert month and year, 'Month and Year are also required.'
            weeks = cls.monthWeekDays(year, month)
            return weeks[week-1][0]
        
        if isinstance(month, str): monthNum = cls.getMonthNum(month) 
        else: monthNum = month
        
        if isinstance(day, str): dayNum = cls.getDayNum(month)
        else: dayNum = day
        
        year, month, day = int(year), int(monthNum), int(dayNum)
        
        dummy = cls(year, month, 1).totalDays
        if dummy < day: return cls(year, month, dummy)
        else: return cls(year, month, day)

    @property
    def dayNum(self): return self.day
    @property
    def dayName(self): return self.strftime('%A')
    @property
    def dayNameAbbr(self): return self.strftime('%a')
    @property
    def monthName(self): return self.strftime('%B')
    @property
    def monthNameAbbr(self): return self.strftime('%b')
   
    @property
    def monthYear(self): return f'{self.monthName}-{self.year}'
    @property
    def weekMonthYear(self): return f'Week {self.week}, {self.monthName}-{self.year}'
    @property
    def monthYearTuple(self): return (self.year, self.month)
    @property
    def weekMonthYearTuple(self): return (self.year, self.month, self.week)
    @property
    def dayMonthYear(self): return f'{self.day}-{self.monthYear}'
    
    @property
    def isoWeekDay(self):
        d = (int(self.isoweekday()) + 1) % 7
        if d == 0: return 7
        return d
    @property
    def weekDay(self): return (int(self.weekday()) + 1) % 7
    @property
    def weekInYear(self): return int(self.isocalendar()[1])
    
    def isSameYear(self, date): return self.year == date.year
    
    def isSameMonth(self, date): return self.monthYearTuple == date.monthYearTuple
    
    def isSameWeek(self, date): return self.weekMonthYearTuple == date.weekMonthYearTuple
    
    @classmethod
    def monthWeekDays(cls, year=None, month=None, monday=False, dateObj=None):
        'getting the weeks in a month'
        if dateObj: year, month = dateObj.year, dateObj.month
        
        year = int(year)
        if isinstance(month, str): month = MONTHS_NAMES[:].index(month)
        
        ca = Calendar(0 if monday else 6)
        
        month_wks = ca.monthdatescalendar(year, month)
        month_wks2 = ca.monthdays2calendar(year, month)
        
        weeks = []
        
        for week in month_wks:
            weeks_days = []
            
            for day in week:
                
                Day = cls.createDateTime(obj=day)
                weeks_days.append(Day)
            
            weeks.append(weeks_days)
            
        return weeks
   
    @classmethod
    def getMonthYearOfDateTimes(cls, dts): return [dt.monthYear for dt in dts]
    
    @classmethod
    def monthYearOfMonthWeekDays(cls, **kwargs):
        weeks = cls.monthWeekDays(**kwargs)
        weeks_monthYear = [cls.getMonthYearOfDateTimes(week) for week in weeks]
        return weeks_monthYear
    
    @property
    def weekDates(self): return self.monthWeekDays(self.year, self.month)
    
    @property
    def monthDates(self):
        days = []
        for week in self.weekDates:
            for day in week: days.append(day)
        return days
    
    @property
    def week(self):
        weeks = self.weekDates
        for wk in weeks:
            if self in wk: return weeks.index(wk) + 1
    
    @classmethod
    def date(cls, status=0, form=1, day_=0):

        now = cls.now()
        days = timedelta(status)
        day = now + days

        if form == 0: fmt = "%D"
        elif form == 1:  fmt = "%d/%m/%Y"
        elif form == 2: fmt = "%a %d %B %Y"
        elif form == 3: fmt = "%d %B %Y"
        elif form == 4: fmt = "%d %b %Y"
        elif form == 5: fmt = "%d %a %b %Y"
        if day_:
            add = tuple(day.strftime("%a %d").split()), day.strftime(fmt)
            return tuple(add)
        elif cls.month_year: return day.strftime("%d/") + cls.month_year # testing
        else: return day.strftime(fmt)

    @classmethod
    def getMonth(cls, status="current", y_r=False):
        if status == "current": return DateTime.now()
        elif status == "next": return DateTime.now() + 1
        elif status == "previous": return DateTime.now() - 1
    
    @classmethod
    def getYear(cls, status="current"):
        if status == "current": return "Year_" + cls.curr_year()
        elif status == "next": return "Year_" + str(int(cls.curr_year()) + 1)
        elif status == "previous": return "Year_" + str(int(cls.curr_year()) - 1)

    @classmethod
    def verifyDateFormat(cls, date): return len(date.split('/')) == 3

    @classmethod
    def getDMYFromDate(cls, date):
        if cls.verifyDateFormat(date):
            day, month, year = date.split('/')
            day, month, year = int(day), int(month), int(year)
            dt = cls(year, month, day)
            return dt
    
    def isSameDate(self, date):
        self.checkDateTime(date)
        return str(self) == str(date)
    
    def diffInMonth(self, date):
        self.checkDateTime(date)
        if self.monthYearTuple == date.monthYearTuple: return 0
        elif self > date: maxDate, minDate = self, date
        elif self < date: maxDate, minDate = date, self
        
        yearDiff = maxDate.year - minDate.year
        monthFromYearDiff = yearDiff * 12
        monthDiff = maxDate.month - minDate.month
        monthsDiff = monthFromYearDiff + monthDiff
            
        return monthsDiff
