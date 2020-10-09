from ..debug.debug import Debug
from datetime import datetime, timedelta, date
from calendar import day_abbr, day_name, month_abbr, month_name, Calendar
DAYS_ABBRS, DAYS_NAMES, MONTHS_ABBRS, MONTHS_NAMES = day_abbr[:], day_name[:], month_abbr[:], month_name[:]
import random

MONTHS_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

MONTHS_ABBRS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

DAYS_BEFORE_MONTH = [-1]

DAYS_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

DAYS_ABBRS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

WEEKS_NAMES = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Unknown"]


dbm = 0
for i in range(12):
    dim = DAYS_IN_MONTH[i]
    DAYS_BEFORE_MONTH.append(dbm)
    dbm += dim
del dim, dbm

def is_leap(year):
    div_by_4 = (year % 4 == 0)
    not_div_by_100 = (year % 100 != 0)
    div_by_400 = (year % 400 == 0)
    return div_by_4 and (not_div_by_100 or div_by_400)


def days_before_year(year): 
    y = year - 1
    return y*365 + y//4 - y//100 + y//400

def days_before_month(year, month):
    assert 1 <= month and month <= 12
    return DAYS_BEFORE_MONTH[month] + (month > 2 and  is_leap(year))


def days_in_month(year, month):
    assert 1 <= month  and month <= 12
    return DAYS_IN_MONTH[month] + (month == 2 and is_leap(year))

def ymd2ord(year, month, day):
    assert (1 <= month and month <= 12)

    dim = days_in_month(year, month)
    assert(1 <= day and day <= dim)
    
    return (days_before_year(year) + days_before_month(year, month) + day)


DI400Y = days_before_year(401)
DI100Y = days_before_year(101)
DI4Y = days_before_year(5)

assert DI4Y == 4 * 365 + 1
assert DI400Y == 4 * DI100Y + 1
assert DI100Y == 25 * DI4Y - 1


def weekday(year, month, day): return (ymd2ord(year, month, day) + 6) % 7



def ord2ymd(n):
    n -= 1;
    n400, n = divmod(n, DI400Y)

    year = n400 * 400 + 1

    n100, n = divmod(n, DI100Y)

    n4, n = divmod(n, DI4Y)

    n1, n = divmod(n, 365)

    year += n100 * 100 + n4 * 4 + n1;
    if (n1 == 4 or n100 == 4):
        assert (n == 0)
        return year-1, 12, 31

    leapyear = n1 == 3 and (n4 != 24 or n100 == 3)
    assert leapyear == is_leap(year)
    
    month = (n + 50) >> 5;
    preceding = DAYS_BEFORE_MONTH[month] + (month > 2 and leapyear);

    if (preceding > n):
        month -= 1;
        preceding -= DAYS_IN_MONTH[month] + (month == 2 and leapyear);

    n -= preceding;
    assert(0 <= n < days_in_month(year, month));

    return year, month, n+1




class DateTime(date):

    def __init__(self, year, month, day): super().__init__()
    @property
    def dayName(self): return self.strftime('%A')
    @property
    def dayNameAbbr(self): return self.strftime('%a')
    @property
    def monthName(self): return self.strftime('%B')
    @property
    def monthNameAbbr(self): return self.strftime('%b')
    @property
    def yearNum(self): return int(self.year)
    @property
    def monthNum(self): return int(self.month)
    @property
    def dayNum(self): return int(self.day)
    @property
    def weekNum(self): return int(weekday(self.year, self.month, self.day))
    @property
    def isoWeekDay(self): return int(self.isoweekday())
    @property
    def weekDay(self): return int(self.weekday())
    @property
    def weekInYear(self): return int(self.isocalendar()[1])


class Date:
    month_year = None
    creator = 0
    "Anything day and month"

    @classmethod
    def current_day(cls):
        now = datetime.now()
        day = now.strftime("%a %d")
        add = day.split()
        return tuple(add)
    @classmethod
    def thrift_day(cls): return cls.date(form=1, day_=1)
    @classmethod
    def current_time(cls, form=None):
        now = datetime.now()
        if form == "24": return now.strftime("%H:%M:%S %p")
        elif form == "12": return now.strftime("%I:%M:%S %p")
    @classmethod
    def curr_year(cls):
        now = datetime.now()
        return now.strftime("%Y")
    @classmethod
    def date(cls, status=0, form=1, day_=0):
        # testing
        if cls.creator: status = random.randrange(0, 31)
        # testing

        now = datetime.now()
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
    def get_month(cls, status="current", y_r=False):
        if status == "current":
            now = datetime.now()
            month = now.strftime("%B")
            if y_r: return [month, Date.get_year(status)]
            else: return month
        if status == "next":
            month = MONTHS_NAMES[(MONTHS_NAMES.index(Date.get_month("current")) + 1) % 12]
            if y_r:
                if Date.get_month("current") == "December": return [month, Date.get_year(status)]
                else: return [month, Date.get_year("current")]
            else: return month
        if status == "previous":
            month = MONTHS_NAMES[(MONTHS_NAMES.index(Date.get_month("current")) - 1) % 12]
            if y_r:
                if Date.get_month("current") == "January": return [month, Date.get_year(status)]
                else: return [month, Date.get_year("current")]
            else: return month
    @classmethod
    def get_year(cls, status="current"):
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
            dt = DateTime(year, month, day)
            return dt
