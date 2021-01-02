__author__ = 'PRMPSmart@gmail.com'

import datetime
from calendar import day_abbr, day_name, month_abbr, month_name, Calendar
import re, zlib, pickle, os, zipfile, io
from PIL.ImageTk import Image, PhotoImage, BitmapImage



DAYS_ABBRS, DAYS_NAMES, MONTHS_ABBRS, MONTHS_NAMES = day_abbr[:], day_name[:], month_abbr[:], month_name[:]


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

class PRMP_Errors(Exception):
    class PRMP_DateTimeError(Exception): pass
    class PRMP_ZipError(Exception): pass

class PRMP_Mixins:
    tempFile = 'prmpsmartTempFile'
    _unget = '_prmp_'
    
    containers = list, set, tuple
    naira = chr(8358)
    dollar = chr(36)
    euro = chr(163)
    yen = chr(165)
    _moneySign = naira + chr(32)
    Errors = PRMP_Errors
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
    @property
    def mroStr(self): return [s.__name__ for s in self.mro]
    
    def numWithCommas(self, num=None):
        if num == None: num = int(self)
        
        div = 3
        str_num = str(num)
        num_list = list(str_num)
        num_len = len(str_num)
        num_rem = num_len % div
        num_div = num_len // div
        if not num_rem: num_div -= 1
        co, to = -3, 0
        for _ in range(num_div):
            num_list.insert(co - to, ",")
            co -= 3
            to += 1
        return "".join(num_list)
    
    def numWithSign_Commas(self, num): return self.addSignToNum(self.numWithCommas(num))

    
    def addSignToNum(self, num): return f'{self._moneySign}{num}'

    def stripSignFromNum(self, num):
        num = num.replace(self._moneySign, '')
        num = num.replace(' ', '')
        return num.replace(' ', '').replace(self._moneySign, '')
    
    
    @property
    def mro(self): return self.class_.__mro__

    @property
    def class_(self): return self.__class__

    def attrError(self, attr): raise AttributeError(f'"{attr}" does not exist in {self}')

    def getFromSelf(self, name, unget=None):
        ret = self.__dict__.get(name, unget)
        if ret != unget: return ret
        else:
            for cl in self.mro:
                ret = cl.__dict__.get(name, unget)
                if ret != unget:
                    if isinstance(ret, property): return ret.fget(self)
                    return ret
        return unget
        
    def printError(self, func, error): print(f"Errors from {self}->{func}: ", error)
    
    def checkEmail(self, email): return True if re.search(self.email_regex, email) else False
    
    def checkNumber(self, number): return str(number).isdigit()

    
    @classmethod
    def notImp(cls): raise NotImplementedError(f'A subclass of {cls} should call this method.')

    @property
    def className(self): return f'{self.__class__.__name__}'
    
    @property
    def AlphabetsSwitch(self):
        d = {}
        for n in range(65, 91):
            d[chr(n)] = chr(n+32)
            d[chr(n+32)] = chr(n)
        return d
    
    def propertize(self, name):
        if name.startswith('_'): return name
        if name:
            name = str(name)
            nm = name.replace(' ', '')
            fin = self.AlphabetsSwitch[nm[0].upper()] + nm[1:]
            return fin
    
    def testPrint(self, *args):
        print()
        for a in args: print(a, end='=')
        print()
    
    def __bool__(self): return True

    def getImageData(self, image):
        temp = io.BytesIO()
        image.save(temp, 'png')
        data = temp.getvalue()
        return data

    def decimalPlace(self, num, place=1):
        num = float(num)
        numStr = str(num) + '0'
        endIndex = numStr.index('.') + place + 1
        return numStr[:endIndex]

    def approximate(self, num, size=1):
        assert size > 0
        strNum = str(num)
        listNum = list(strNum)
        if len(listNum) <= 3: return num
        app = listNum[size]
        
        listNum[size:] = ['0' for _ in range(size, len(listNum))]
        add = 0 if int(app) < 5 else 1
        adx = int(listNum[size - 1]) + add
        listNum[size - 1] = str(adx)
        retur = ''.join(listNum)
        return int(retur)
    
    def stripZeros(self, num, app=1):
        num = self.approximate(num, app)
        strNum = str(num)
        listNum = list(strNum)
        return strNum.strip('0')

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
    # the __add__ and __sub__ are implementaions are purely by PRMPSmart@gmail.com
    def __add__(self, add_month):
        if isinstance(add_month, datetime.timedelta): return self.createDateTime(obj=super().__add__(add_month))
        
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
        if isinstance(sub_month, datetime.timedelta): return self.createDateTime(obj=super().__sub__(sub_month))
        
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
    
    def __str__(self): return self.strftime(self.date_fmt)
    
    @property
    def strDate(self): return str(self)
    
    @property
    def totalDays(self): # also equal to _days_in_month
        lis = [1, 3, 5, 7, 8, 10, 12]
        if self.month == 2: return 28 + self.isLeap
        elif self.month in lis: return 31
        else: return 30
    
    @classmethod
    def getDayNum(cls, day):
        error = cls.Errors(f'day must be among {cls.daysAbbrs} or {cls.daysNames}')
        if isinstance(day, str):
            if day in cls.daysAbbrs: dayNum = cls.daysAbbrs.index(day) + 1
            elif day in cls.daysNames: dayNum = cls.daysNames.index(day) + 1
            else: raise error
            return dayNum
        else: raise error
        
    @classmethod
    def getDayName(cls, day, abbr=False):
        range_ = list(range(1, 31))
        error = cls.Errors(f'day must be among {range_}')
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
        error = cls.Errors(f'month must be among {cls.monthsAbbrs} or {cls.monthsNames}')
        if isinstance(month, str):
            if month in cls.monthsAbbrs: monthNum = cls.monthsAbbrs.index(month)
            elif month in cls.monthsNames: monthNum = cls.monthsNames.index(month)
            else: raise error
            return monthNum
        else: raise error
        
    @classmethod
    def getMonthName(cls, month, abbr=False):
        range_ = list(range(1, 12))
        error = cls.Errors(f'month must be among {range_}')
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
    
    def isSameDate(self, date):
        self.checkDateTime(date)
        return str(self) == str(date)
    
    def isSameDay(self, date): return self.day == date.day
    
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
        days = datetime.timedelta(status)
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

class PRMP_Pics:
    _dir = 'prmp_pics'
    subDir = ''
    
    @classmethod
    def picsExt(cls):
        ext = cls.subDir[:-1]
        return ext.replace('prmp_', '')
    
    @classmethod
    def picsHome(cls): return os.path.join (os.path.dirname(__file__), cls._dir)
    
    @classmethod
    def picName(cls, pic): return os.path.splitext (os.path.basename(pic))[0]
    
    @classmethod
    def files(cls):
        _dir = os.path.join(cls.picsHome(), cls.subDir)
        _files = []
        
        for r, d, ff in os.walk(_dir):
            for f in ff:
                if f.endswith(cls.picsExt()):
                    _files.append (os.path.join(r, f))
        
        return _files
    
    @classmethod
    def filesDict(cls):
        files = cls.files()
        _filesDict = {cls.picName(file): file for file in files}
        return _filesDict
    
    @classmethod
    def get(cls, bitmap):
        filesL = cls.files()
        
        if isinstance(bitmap, int):
            try: return filesL[bitmap]
            except: filesL[0]
        elif isinstance(bitmap, str):
            files = cls.filesDict()
            try: return files[bitmap]
            except: filesL[0]

class PRMP_Xbms(PRMP_Pics): subDir = 'prmp_xbms'
    
class PRMP_Pngs(PRMP_Pics): subDir = 'prmp_pngs'
    
class PRMP_Gifs(PRMP_Pics): subDir = 'prmp_gifs'

class PRMP_ImageFile(io.BytesIO):
    count = 0

    def getImageFile(self, pix, ext='.png', db=0):
        if isinstance(pix, str):
            e = os.path.splitext(pix)[-1]

            if e in ['.png', '.xbm', '.gif', '.jpg', '.jpeg']: self.ext = e[1:]
            else: self.ext = ext

            if db:
                if self.ext == 'png': pic = PRMP_Pngs.get(pix)
                elif self.ext == 'gif': pic = PRMP_Gifs.get(pix)
                elif self.ext == 'xbm': pic = PRMP_Xbms.get(pix)
            else: pic = pix
            self.name = pix
            self.basename = os.path.basename(pic)
            return pic

    def __init__(self, fp=None, ext='.png', db=0, image=None):
        self.name = None
        self.basename = None
        self.ext = ext
        self._data = b''

        if isinstance(fp, str):
            file = self.getImageFile(fp, ext=ext, db=db)
            self._data = open(file, 'rb').read()
        elif isinstance(fp, bytes): self._data = fp

        super().__init__(self._data)

        if image: image.save(self, 'png')

        PRMP_ImageFile.count += 1

    def __str__(self):
        if self.name:return f'PRMP_ImageFile({self.name})'
        else: return f'PRMP_ImageFile({PRMP_ImageFile.count})'

    def __len__(self): return self.size

    @property
    def data(self): return self.getvalue()
    @property
    def compressedData(self): return zlib.compress(self.data)
    @property
    def cdata(self): return self.compressedData
    @property
    def size(self): return len(self.data)

    def get(self): return self.data

    def setCompressedData(self, compressedData):
        decomData = zlib.decompress(compressedData)
        self.write(decomData)
    
    def pickle(self, file):
        try: f = open(file, 'wb')
        except: f = file
        pickle.dump(self, f)

    def save(self, file):
        try: f = open(file, 'wb')
        except: f = file

        f.write(self.data)

class PRMP_Image:
    count = 0
    def __init__(self, imageFile=None, ext='png', resize=(), thumb=(), db=0, image=None):
        
        pic = None
        self.ext = 'jpg'
        self.imageFile = imageFile
        self.imgClass = PhotoImage
        self.resizedImage = None
        self.image = None
        self.tkImage = None
        self.name = ''

        if imageFile or image:
            if isinstance(imageFile, (str, bytes)): self.imageFile = PRMP_ImageFile(imageFile, ext=ext, db=db)
            elif image: self.imageFile = PRMP_ImageFile(image=image)
            
            self.name = self.imageFile.name
            self.ext = self.imageFile.ext
            
            if self.ext in ['xbm', '.xbm']: self.imgClass = BitmapImage

            img = self.image = Image.open(self.imageFile)

            if resize and len(resize) == 2:
                self.resizedImage = self.image.resize(resize)
                img = self.resizedImage
            
            if thumb and len(thumb) == 2: img.thumbnail(thumb)
            
            self.tkImage = self.imgClass(img, name=self.basename)

            PRMP_Image.count += 1
            
        else: raise ValueError('imageFile is None')

    def __str__(self): return str(self.tkImage)

    @property
    def basename(self):
        if self.imageFile and self.imageFile.basename: return self.imageFile.basename
        return f'PRMP_Image({PRMP_Image.count})'

    def resize(self, rz): return self.image.resize(rz)

    def get(self): return self.imageFile

    def resizeTk(self, rz): return self.imgClass(self.resize(rz))

    def thumbnail(self, rz): self.image.thumbnail(rz)
    
    def thumbnailTk(self, rz): 
        self.thumbnail(rz)
        return self.imgClass(self.image)

def zipPath(resource, destination='', latest=False):
    # Create name of new zip file, based on original folder or file name
    resource = resource.rstrip('\\').rstrip('/')
    # if resource in destination: TranxFerLogger.warning('Loop: Save somewhere else!')
    
    if not os.path.exists(resource): return
    
    if destination:
        if os.path.isdir(destination):
            baseFileName = os.path.basename(resource) + '.zip'
            zipFileName = os.path.join(destination, baseFileName)
        else: zipFileName = destination

    else: zipFileName = resource + '.zip'
    
    if os.path.isdir(resource): zipRootDir = os.path.basename(resource)
    
    if (os.path.isfile(zipFileName) == True) and (latest == False): return zipFileName
    
    # Create zip file
    with zipfile.ZipFile(zipFileName, "w", compression=zipfile.ZIP_DEFLATED) as zipFile:
        if os.path.isdir(resource):
            for root, dirs, files in os.walk(resource):
               for file in files:
                   filename = os.path.join(root, file)
                   arc = root.replace(resource, zipRootDir)
                   arcname = os.path.join(arc, file)
                   zipFile.write(filename, arcname, zipfile.ZIP_DEFLATED)
        else: zipFile.write(resource, zipFileName, zipfile.ZIP_DEFLATED)
    return zipFileName












