__author__ = 'PRMPSmart@gmail.com'

import datetime
from calendar import day_abbr, day_name, month_abbr, month_name, Calendar
from .prmp_mixins import PRMP_Mixins, PRMP_Errors

DAYS_ABBRS, DAYS_NAMES, MONTHS_ABBRS, MONTHS_NAMES = day_abbr[:], day_name[:], month_abbr[:], month_name[:]
WEEKS = ['Week %d'%a for a in range(1, 6)]


_DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

_DAYS_BEFORE_MONTH = [-1]  # -1 is a placeholder for indexing purposes.
dbm = 0
for dim in _DAYS_IN_MONTH[1:]:
    _DAYS_BEFORE_MONTH.append(dbm)
    dbm += dim
del dbm, dim

def _is_leap(year):
    "year -> 1 if leap year, else 0."
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def _days_before_year(year):
    "year -> number of days before January 1st of year."
    y = year - 1
    return y*365 + y//4 - y//100 + y//400

def _days_in_month(year, month):
    "year, month -> number of days in that month in that year."
    assert 1 <= month <= 12, month
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]

def _days_before_month(year, month):
    "year, month -> number of days in year preceding first day of month."
    assert 1 <= month <= 12, 'month must be in 1..12'
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))

def _ymd2ord(year, month, day):
    "year, month, day -> ordinal, considering 01-Jan-0001 as day 1."
    assert 1 <= month <= 12, 'month must be in 1..12'
    dim = _days_in_month(year, month)
    assert 1 <= day <= dim, ('day must be in 1..%d' % dim)
    return (_days_before_year(year) +
            _days_before_month(year, month) +
            day)

_DI400Y = _days_before_year(401)    # number of days in 400 years
_DI100Y = _days_before_year(101)    #    "    "   "   " 100   "
_DI4Y   = _days_before_year(5)      #    "    "   "   "   4   "

# A 4-year cycle has an extra leap day over what we'd get from pasting
# together 4 single years.
assert _DI4Y == 4 * 365 + 1

# Similarly, a 400-year cycle has an extra leap day over what we'd get from
# pasting together 4 100-year cycles.
assert _DI400Y == 4 * _DI100Y + 1

# OTOH, a 100-year cycle has one fewer leap day than we'd get from
# pasting together 25 4-year cycles.
assert _DI100Y == 25 * _DI4Y - 1

def _ord2ymd(n):
    "ordinal -> (year, month, day), considering 01-Jan-0001 as day 1."

    # n is a 1-based index, starting at 1-Jan-1.  The pattern of leap years
    # repeats exactly every 400 years.  The basic strategy is to find the
    # closest 400-year boundary at or before n, then work with the offset
    # from that boundary to n.  Life is much clearer if we subtract 1 from
    # n first -- then the values of n at 400-year boundaries are exactly
    # those divisible by _DI400Y:
    #
    #     D  M   Y            n              n-1
    #     -- --- ----        ----------     ----------------
    #     31 Dec -400        -_DI400Y       -_DI400Y -1
    #      1 Jan -399         -_DI400Y +1   -_DI400Y      400-year boundary
    #     ...
    #     30 Dec  000        -1             -2
    #     31 Dec  000         0             -1
    #      1 Jan  001         1              0            400-year boundary
    #      2 Jan  001         2              1
    #      3 Jan  001         3              2
    #     ...
    #     31 Dec  400         _DI400Y        _DI400Y -1
    #      1 Jan  401         _DI400Y +1     _DI400Y      400-year boundary
    n -= 1
    n400, n = divmod(n, _DI400Y)
    year = n400 * 400 + 1   # ..., -399, 1, 401, ...

    # Now n is the (non-negative) offset, in days, from January 1 of year, to
    # the desired date.  Now compute how many 100-year cycles precede n.
    # Note that it's possible for n100 to equal 4!  In that case 4 full
    # 100-year cycles precede the desired day, which implies the desired
    # day is December 31 at the end of a 400-year cycle.
    n100, n = divmod(n, _DI100Y)

    # Now compute how many 4-year cycles precede it.
    n4, n = divmod(n, _DI4Y)

    # And now how many single years.  Again n1 can be 4, and again meaning
    # that the desired day is December 31 at the end of the 4-year cycle.
    n1, n = divmod(n, 365)

    year += n100 * 100 + n4 * 4 + n1
    if n1 == 4 or n100 == 4:
        assert n == 0
        return year-1, 12, 31

    # Now the year is correct, and n is the offset from January 1.  We find
    # the month via an estimate that's either exact or one too large.
    leapyear = n1 == 3 and (n4 != 24 or n100 == 3)
    assert leapyear == _is_leap(year)
    month = (n + 50) >> 5
    preceding = _DAYS_BEFORE_MONTH[month] + (month > 2 and leapyear)
    if preceding > n:  # estimate is too large
        month -= 1
        preceding -= _DAYS_IN_MONTH[month] + (month == 2 and leapyear)
    n -= preceding
    assert 0 <= n < _days_in_month(year, month)

    # Now the year and month are correct, and n is the offset from the
    # start of that month:  we're done!
    return year, month, n+1

class OldCompareByDate:
    def __lt__(self, other):
        if other == None: return False
        return self.date < other.date
    def __le__(self, other):
        if other == None: return False
        return self.date <= other.date
    def __eq__(self, other):
        if other == None: return False
        return self.date is other.date
    def __ne__(self, other):
        if other == None: return True
        return self.date != other.date
    def __gt__(self, other):
        if other == None: return True
        return self.date > other.date
    def __ge__(self, other):
        if other == None: return True
        return self.date >= other.date

class CompareByDate:
    def __lt__(self, other):
        if other == None: return False
        return self.date.ymdToOrd < other.date.ymdToOrd
    def __le__(self, other):
        if other == None: return False
        return self.date.ymdToOrd <= other.date.ymdToOrd
    def __eq__(self, other):
        if other == None: return False
        return self.date.ymdToOrd is other.date.ymdToOrd
    def __ne__(self, other):
        if other == None: return True
        return self.date.ymdToOrd != other.date.ymdToOrd
    def __gt__(self, other):
        if other == None: return True
        return self.date.ymdToOrd > other.date.ymdToOrd
    def __ge__(self, other):
        if other == None: return True
        return self.date.ymdToOrd >= other.date.ymdToOrd

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

class PRMP_DateTime(datetime.datetime, PRMP_Mixins):
    date_fmt = "%d/%m/%Y"
    daysAbbr, daysNames, monthsAbbrs, monthsNames = day_abbr[:], day_name[:], month_abbr[:], month_name[:]
    Errors = PRMP_Errors.PRMP_DateTimeError

    timedelta = datetime.timedelta


    # the __add__ and __sub__ are implementaions are purely by PRMPSmart@gmail.com

    def __getitem__(self, item):
        # print(item)
        if item == slice(None, None, None): return self
        return PRMP_Mixins.__getitem__(self, item)

    def __add__(self, add_month):
        if isinstance(add_month, self.timedelta): return self.createDateTime(obj=super().__add__(add_month))

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
        if isinstance(sub_month, self.timedelta): return self.createDateTime(obj=super().__sub__(sub_month))

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
                    # therefore, subtract the recent years from the current year, creating a new PRMP_DateTime with everything else in place except the year
                    # the sub_month is more than 12
                    year = self.createDateTime(self.year - div, self.month, self.day)
                    # the remaining months will now fall into the categories of (sub_month < self.month) and ( sub_month == self.month).
                    # it will now look as if it's a loop, the remaining months will now be subtracted from the new year-PRMP_DateTime, the process will now fall into the first two conditions in the new year-PRMP_DateTime
                    return year - mod

    def __str__(self): return repr(self)
    # def __str__(self): return self.strftime(self.date_fmt)

    @property
    def date(self): return self.strftime(self.date_fmt)

    @property
    def strDate(self): return self.date

    @property
    def totalDays(self): # also equal to _days_in_month
        lis = [1, 3, 5, 7, 8, 10, 12]
        if self.month == 2: return 28 + self.isLeap
        elif self.month in lis: return 31
        else: return 30

    @classmethod
    def getDayNum(cls, day):
        error = cls.Errors('day must be among {} or {}'.format(cls.daysAbbrs, cls.daysNames))
        if isinstance(day, str):
            if day in cls.daysAbbrs: dayNum = cls.daysAbbrs.index(day) + 1
            elif day in cls.daysNames: dayNum = cls.daysNames.index(day) + 1
            else: raise error
            return dayNum
        else: raise error

    @classmethod
    def getDayName(cls, day, abbr=False):
        range_ = list(range(1, 31))
        error = cls.Errors('day must be among {}'.format(range_))
        if isinstance(day, int):
            if day in range_:
                if abbr: dayName = cls.daysAbbrs[day - 1]
                else: dayName = cls.daysNames[day - 1]
            else: raise error
            return dayName
        else: raise error

    @classmethod
    def checkDateTime(cls, date, dontRaise=False):
        if not isinstance(date, PRMP_DateTime):
            if dontRaise: return False
            raise cls.Errors('Date must be an instance of PRMP_DateTime')
        return True

    @classmethod
    def now(cls): return cls.createDateTime(obj=super().now())

    @classmethod
    def getMonthNum(cls, month):
        error = cls.Errors('month must be among {} or {}'.format(cls.monthsAbbrs), cls.monthsNames)
        if isinstance(month, str):
            if month in cls.monthsAbbrs: monthNum = cls.monthsAbbrs.index(month)
            elif month in cls.monthsNames: monthNum = cls.monthsNames.index(month)
            else: raise error
            return monthNum
        else: raise error

    @classmethod
    def getMonthName(cls, month, abbr=False):
        range_ = list(range(1, 12))
        error = cls.Errors('month must be among {}'.format(range_))
        if isinstance(month, int):
            if month in range_:
                if abbr: monthName = cls.monthsAbbrs[month - 1]
                else: monthName = cls.monthsNames[month - 1]
            else: raise error
            return monthName
        else: raise error

    @classmethod
    def createDateTime(cls, year=None, month=1, day=1, auto=False, obj=None, week=None, hour=0, minute=0, second=0):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            year = obj.year
            month = obj.month
            day = obj.day
            try:
                hour = obj.hour
                minute = obj.minute
                second = obj.second
            except: pass

        elif auto: return cls.now()

        elif week:
            assert month and year, 'Month and Year are also required.'
            weeks = cls.monthWeekDays(year, month)
            return weeks[week-1][0]

        if isinstance(month, str): month = cls.getMonthNum(month)

        if isinstance(day, str): day = cls.getDayNum(month)

        dummy = cls(year, month, 1).totalDays
        if dummy < day: day = dummy

        return cls(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

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
    def monthYear(self): return '{}-{}'.format(self.monthName, self.year)
    @property
    def weekMonthYear(self): return 'Week {}, {}-{}'.format(self.week, self.monthName, self.year)
    @property
    def monthYearTuple(self): return (self.year, self.month)
    @property
    def weekMonthYearTuple(self): return (self.year, self.month, self.week)
    @property
    def dayMonthYear(self): return '{}-{}'.format(self.day, self.monthYear)

    @property
    def isoWeekDay(self):
        d = (int(self.isoweekday()) + 1) % 7
        if d == 0: return 7
        return d
    @property
    def weekDay(self): return (int(self.weekday()) + 1) % 7
    @property
    def weekInYear(self): return int(self.isocalendar()[1])

    def isSameDate(self, date):
        self.checkDateTime(date)
        return self.date == date.date

    def isSameDay(self, date): return self.day == date.day

    def isSameDayName(self, date): return self.dayName == date.dayName

    def isSameYear(self, date): return self.year == date.year

    def isSameMonth(self, date): return self.month == date.month

    def isSameWeek(self, date): return self.week == date.week

    def isSameMonthYear(self, date): return self.monthYearTuple == date.monthYearTuple

    def isSameWeekMonthYear(self, date): return self.weekMonthYearTuple == date.weekMonthYearTuple


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
            _wk = [w.date for w in wk]
            if self.date in _wk: return weeks.index(wk) + 1
        return 0

    @property
    def weekName(self): return 'Week {}'.format(self.week)

    @classmethod
    def getDate(cls, status=0, form=1, day_=0):

        now = cls.now()
        days = cls.timedelta(status)
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
        if status == "current": return PRMP_DateTime.now()
        elif status == "next": return PRMP_DateTime.now() + 1
        elif status == "previous": return PRMP_DateTime.now() - 1

    @classmethod
    def getYear(cls, status="current"):
        if status == "current": return "Year_" + cls.curr_year()
        elif status == "next": return "Year_" + str(int(cls.curr_year()) + 1)
        elif status == "previous": return "Year_" + str(int(cls.curr_year()) - 1)

    @classmethod
    def verifyDateFormat(cls, date): return len(date.split('/')) == 3

    @classmethod
    def getDMYFromDate(cls, date):
        if date:
            if isinstance(date, str) and cls.verifyDateFormat(date):
                day, month, year = date.split('/')
                day, month, year = int(day), int(month), int(year)
                dt = cls(year, month, day)
                return dt
            elif isinstance(date, cls): return date

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

    @classmethod
    def is_leap(cls, year): return _is_leap(year)

    @property
    def isLeap(self): return self.is_leap(self.year)

    @classmethod
    def days_before_year(cls, year): return _days_before_year(year)

    @property
    def daysBeforeYear(self): return self.days_before_year(self.year)

    @classmethod
    def days_in_month(cls, year, month): return _days_in_month(year, month)

    @property
    def daysInMonth(self): return self.days_in_month(self.year, self.month)

    @classmethod
    def days_before_month(cls, year, month): return _days_before_month(year, month)

    def daysBeforeMonth(self): return self.days_before_month(self.year, self.month)

    @classmethod
    def ymd2ord(cls, year, month, day): return _ymd2ord(year, month, day)

    @property
    def ymdToOrd(self): return self.ymd2ord(self.year, self.month, self.day)

    @classmethod
    def ord2ymd(cls, ord_): return _ord2ymd(ord_)
