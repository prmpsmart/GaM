__author__ = "PRMP Smart"
from prmp_miscs import *
import time, hashlib, datetime


class Errors(PRMP_Errors):
    class RegionsManagerError(Exception): pass
    class DateTimeError(Exception): pass
    class AccountError(Exception): pass
    class AccountsManagerError(Exception): pass
    class RepaymentError(Exception): pass
    class LoanBondsError(Exception): pass
    class LoanRepaymentsError(Exception): pass


class Mixins(PRMP_AdvMixins, PRMP_StrMixins):

    def moneyWithSign_ListInList(self, listInList):
        try: listInList[0][0]
        except: raise AssertionError('Data must be list in another list')
        newListInList = []
        for list1 in listInList:
            newList = []
            for data in list1:
                try:
                    if isinstance(data, Mixins): raise
                    money = float(data)
                    new = self.addSignToMoney(money)
                    newList.append(new)
                except: newList.append(data)
            newListInList.append(newList)
        return newListInList

    @classmethod
    def setMoneySign(cls, sign): Mixins._moneySign = sign


class CompareByNumber:
    def __lt__(self, other):
        if other == None: return False
        return self.number < other.number
    def __le__(self, other):
        if other == None: return False
        return self.number <= other.number
    def __eq__(self, other):
        if other == None: return False
        return self.number == other.number
    def __ne__(self, other):
        if other == None: return True
        return self.number != other.number
    def __gt__(self, other):
        if other == None: return True
        return self.number > other.number
    def __ge__(self, other):
        if other == None: return True
        return self.number >= other.number


class ObjectSort(Mixins):
   #
    __lt = ('lt', '<')
    __le = ('le', '<=')
    __gt = ('gt', '>')
    __ge = ('ge', '>=')
    __eq = ('eq', '==')
    __ne = ('ne', '!=')
    __comparisons = (__lt, __le, __eq, __ne, __gt, __ge)

    __lt_lt = (__lt, __lt)
    __lt_le = (__lt, __le)
    __lt_gt = (__lt, __gt)
    __lt_ge = (__lt, __ge)

    __le_lt = (__le, __lt)
    __le_le = (__le, __le)
    __le_gt = (__le, __gt)
    __le_ge = (__le, __ge)

    __gt_lt = (__gt, __lt)
    __gt_le = (__gt, __le)
    __gt_gt = (__gt, __gt)
    __gt_ge = (__gt, __ge)

    __ge_lt = (__ge, __lt)
    __ge_le = (__ge, __le)
    __ge_gt = (__ge, __gt)
    __ge_ge = (__ge, __ge)

    __ranges = (__lt_lt, __lt_le, __lt_gt, __lt_ge, __le_lt, __le_le, __le_gt, __le_ge, __gt_lt, __gt_le, __gt_gt, __gt_ge, __ge_lt, __ge_le, __ge_gt, __ge_ge)

    def __init__(self, object_=None): self.object = object_

    def __str__(self):
        if self.object: return f'{self.className}({self.object.name})'
        else: return object.__str__(self)

    def getCompType(self, _type):
        for c in self.__comparisons:
            ind = self.__comparisons.index(c)
            if _type == '=': return '=='
            elif _type in c: return c[1]

    def compare(self, a, b, _type='=='):
        comp = self.getCompType(_type)
        if comp:
            # equation = f'{a} {comp} {b}'
            # # print(equation)
            # return eval(equation)

            if comp == self.__lt[1]: return a < b
            elif comp == self.__le[1]: return a <= b
            elif comp == self.__eq[1]: return a == b
            elif comp == self.__ne[1]: return a != b
            elif comp == self.__gt[1]: return a > b
            elif comp == self.__ge[1]: return a >= b

    def getRangeType(self, _type):
        t1, t2 = _type
        for r in self.__ranges:
            ind = self.__ranges.index(r)
            a, b = r
            if t1 in a and t2 in b: return a[1], b[1]

    def rangeComp(self, a, b, c, _type=('>', '>')):
        rang = self.getRangeType(_type)
        if rang:
            r1, r2 = rang
            # equation = f'{a} {r1} {b} {r2} {c}'
            # # print(equation)
            # return eval(equation)

            if r1 == self.__lt[1] and r2 == self.__lt[1]: return a < b < c
            elif r1 == self.__lt[1] and r2 == self.__le[1]: return a < b <= c
            elif r1 == self.__lt[1] and r2 == self.__gt[1]: return a < b > c
            elif r1 == self.__lt[1] and r2 == self.__ge[1]: return a < b >= c

            elif r1 == self.__le[1] and r2 == self.__lt[1]: return a <= b < c
            elif r1 == self.__le[1] and r2 == self.__le[1]: return a <= b <= c
            elif r1 == self.__le[1] and r2 == self.__gt[1]: return a <= b > c
            elif r1 == self.__le[1] and r2 == self.__ge[1]: return a <= b >= c

            elif r1 == self.__gt[1] and r2 == self.__lt[1]: return a > b < c
            elif r1 == self.__gt[1] and r2 == self.__le[1]: return a > b <= c
            elif r1 == self.__gt[1] and r2 == self.__gt[1]: return a > b > c
            elif r1 == self.__gt[1] and r2 == self.__ge[1]: return a > b >= c

            elif r1 == self.__ge[1] and r2 == self.__lt[1]: return a >= b < c
            elif r1 == self.__ge[1] and r2 == self.__le[1]: return a >= b <= c
            elif r1 == self.__ge[1] and r2 == self.__gt[1]: return a >= b > c
            elif r1 == self.__ge[1] and r2 == self.__ge[1]: return a >= b >= c

    def getAllObjects(self, object_=None):
        '''
        returns every GaM object in this object_ or self.object
        '''
        object_ = object_ or self.object

        subs = []
        __subs = []
        if 'Record' in object_.mroStr: return object_

        if getattr(object_, 'subRegions', None): __subs.append(object_.subRegions)

        if getattr(object_, 'subs', None): __subs.append(object_.subs)

        for s in __subs: subs.extend(s[:])

        allSubs = []
        allSubs.extend(subs)

        for sub in subs:
            new = self.getAllObjects(sub)
            new_  = [b for b in new if b not in allSubs]
            allSubs.extend(new_)

        return allSubs

    def getObjects(self, object_=None, subs=[], attrs=[], manAttrs=[]):
        object_ = object_ or self.object

        if subs: return subs

        if attrs and not object_: raise ValueError('This ObjectSort instance has no attributed object.')

        if subs and attrs: raise SyntaxError('Only one of [subs, attrs] is required.')

        objects = subs.copy()
        if object_ and not objects:
            for addAttr in manAttrs:
                _addObjs = getattr(object_, addAttr, None)
                if _addObjs:
                    addObjs = _addObjs[:]
                    objects.extend(addObjs)

        if attrs and not subs: objects = [object_[attr] for attr in attrs]

        return objects

    def sort(self, subs=[], attrs=[], _type=None, object_=None, validations=[], manAttrs=['subs']):

        '''
        validations = [
            {'value': PRMP_DateTime.getDMYFromDate('20/12/2020'), 'method': 'isSameMonth', 'attr': 'date', 'attrMethod': 'isSameMonth', 'methodParams': {}, 'attrMethodParams': {}, 'valueType': int, 'comp': __comparisons, 'compType': ['range', 'comp'], 'minValue': 2000, 'range': __ranges, 'className': 'ObjectsMixins', 'mroStr': 'Record'}
        ]
        '''

        objects = self.getObjects(object_=object_, subs=subs, attrs=attrs, manAttrs=manAttrs)
        if not objects: return

        if validations:
            validated = []
            for obj in objects:
                valid = True
                val = obj

                for validation in validations:
                    if not valid: break

                    className = validation.get('className')
                    if className and (className not in obj.mroStr):
                        valid = False
                        break
                    mroStr = validation.get('mroStr')
                    if mroStr and (mroStr not in obj.mroStr):
                        valid = False
                        break

                    value = validation.get('value')

                    method = validation.get('method')
                    methodParams = validation.get('methodParams')

                    attr = validation.get('attr')
                    attrMethod = validation.get('attrMethod')
                    attrMethodParams = validation.get('attrMethodParams')

                    valueType = validation.get('valueType')

                    comp = validation.get('comp', 'eq')
                    compType = validation.get('compType', 'comp')
                    minValue = validation.get('minValue')
                    range_ = validation.get('range', self.__lt_lt)

                    if method:
                        # meth = getattr(obj, method, None)
                        meth = obj[method]
                        if not meth:
                            valid = False
                            break
                        if methodParams: val = meth(**methodParams)
                        else: val = meth()
                    elif attr:
                        # attr_ = getattr(obj, attr, None)
                        attr_ = obj[attr]
                        if not attr_:
                            valid = False
                            break
                        if attrMethod:
                            # attrMeth = getattr(attr_, attrMethod, None)
                            attrMeth = attr_[attrMethod]
                            if not attrMeth:
                                valid = False
                                break
                            if attrMethodParams: val = attrMeth(**attrMethodParams)
                            else: val = attrMeth()
                        else: val = attr_
                    if val:
                        if valueType:
                            try: val = valueType(val)
                            except:
                                valid = False
                                break
                        if compType == 'comp':
                            if self.compare(val, value, comp): valid = True
                            else: valid = False
                        elif compType == 'range':
                            assert minValue, f'minValue must be given if compType is range.'
                            assert isinstance(range_, tuple), f'range must be a tuple of two comp'
                            if self.rangeComp(minValue, val, value, range_): valid = True
                            else: valid = False
                        else: raise SyntaxError(f'{compType} is not valid, valid options are [range, comp].')
                    else: valid = False

                if valid: validated.append(obj)

            objects = validated

        # last one
        if _type: objects = [_type(v) for v in objects]

        return objects

    def sortSubsBySeasons(self, date, seasons=['date'], attr='date', validations=[], **kwargs):
        _types = {'year': 'isSameYear', 'month': 'isSameMonth', 'week': 'isSameWeek', 'day': 'isSameDay', 'date': 'isSameDate', 'dayName': 'isSameDayName'}

        validations = validations.copy()

        for season in seasons:
            validation = dict(value=True, attrMethod=_types[season], attr=attr, attrMethodParams=dict(date=date))
            validations.append(validation)

        # print(validations)

        return self.sort(validations=validations, **kwargs)

    def search(self, _type=None, value=None, attr='', searchType='', allSubs=False, object_=None, validations=[], instance=None):
        '''
        search through the object to return GaM objects that is valid based on the validations.
        '''
        results = []
        subs = []

        object_ = object_ or self.object

        if not object_: return

        subs = self.getAllObjects(object_)

        if validations: return self.sort(subs=subs, validations=validations, _type=_type, object_=object_)

        if instance: subs = [sub for sub in subs if instance in sub.mroStr]
        # if instance: subs = [sub for sub in subs if isinstance(sub, instance)]

        return subs


class ObjectsMixins(CompareByDate, Mixins):
    subTypes = ['subs']

    ObjectSortClass = ObjectSort

    def __init__(self, date=None, previous=None, idReq=0):
        self.__editableValues = []

        self._date = self.getDate(date)
        self.objectSort = self.ObjectSortClass(self)

        self.previous = previous
        self.next = None

        if not idReq: self._uniqueID = hashlib.sha224(str(self).encode()).hexdigest()

        self._active = self._date

    @property
    def totalSubs(self):
        if self.subs: return len(self.subs)
        return 0

    @property
    def uniqueID(self): return self._uniqueID

    @property
    def active(self): return self._active

    @active.setter
    def active(self, date):
        if self._active > date: return
        self._active = date
        if not self.strManager: self.manager.active = date

    @property
    def sort(self): return self.objectSort.sort

    @property
    def search(self): return self.objectSort.search

    def __str__(self): return f'{self.manager} | {self.name}'

    def __repr__(self): return f'<{self.name}>'

    @property
    def name(self): return f'{self.className}({self.date.date})'

    @property
    def editableValues(self): return self.__editableValues

    def addEditableValues(self, child):
        if child not in self.__editableValues:
            if isinstance(child, (list, tuple)):
                for ch in child: self.addEditableValues(ch)
            else: self.__editableValues.append(child)


    def update(self, values={}):
        edit = self.editableValues

        for key in edit:
            _type = None
            if isinstance(key, dict): key, _type = key['value'], key['type']
            val = values.get(key, None)
            if _type: val = _type(val)
            if val: setattr(self, key, val)
            # print(key, val)

    @property
    def values(self):
        vals = {}
        edit = self.editableValues
        for key in edit:
            if isinstance(key, dict): key = key['value']
            vals[key] = self[key]
        return vals

    def __repr__(self): return f'<{self.name}>'

    def sumRecords(self, records): return sum(float(rec) for rec in records)

    @property
    def withCommas(self): return self.numWithCommas(self.money)

    @property
    def strManager(self): return isinstance(self.manager, str)

    def __len__(self):
        try: return len(self[:])
        except: return 1

    def get(self, attr, default=None):
        try: return self[attr]
        except: return default

    @property
    def moneyWithSign(self): return f'{self._moneySign}{float(self)}'

    @property
    def regDate(self): return self.date
    # @property
    # def day(self): return self.date.day
    # @property
    # def dayName(self): return self.date.dayName
    # @property
    # def month(self): return self.date.month
    # @property
    # def monthName(self): return self.date.monthName
    # @property
    # def year(self): return self.date.year
    # @property
    # def monthYearTuple(self): return self.date.monthYearTuple
    # @property
    # def weekMonthYearTuple(self): return self.date.weekMonthYearTuple

    # @property
    # def monthYear(self): return self.date.monthYear

    # @property
    # def weekMonthYear(self): return self.date.weekMonthYear

    # @property
    # def week(self): return self.date.week

    @property
    def date(self): return self._date

    @date.setter
    def date(self, _date): self._date = self.getDate(_date)


# class Object(CompareByNumber, ObjectsMixins):
class Object(ObjectsMixins):
    Manager = 'ObjectsManager'
    Managers = ()

    def __eq__(self, other):
        if other == None: return False
        return self is other

    def __init__(self, manager=None, number=None, name=None, nameFromNumber=False, sup=None, date=None, previous=None, **kwargs):

        if not isinstance(manager, str): assert (manager.className == self.Manager) or (manager.className in self.Managers), f'Manager of {self.className} should be {self.Manager} or in {self.Managers} not {manager.className}.'

        self._number = number
        self._sup = sup

        self._name = name if not nameFromNumber else f'{self.className} {self.number}'
        self._manager = manager

        ObjectsMixins.__init__(self, date=date, previous=previous)

    @property
    def id(self): return ''.join(self.spacedID.split(' | ')).replace('GaM', 'A')

    def delete(self, called=0):
        if self.next: self.next.previous = self.previous
        if self.previous: self.previous.next = self.next

        self.manager.removeSub(self)

    @property
    def sup(self): return self._sup

    @property
    def spacedID(self):
        'override in subclass'
        return 'id | object'

    @property
    def subs(self): return []

    @property
    def name(self):
        try:
            if self._name: return self._name
        except: pass
        return super().name
    @name.setter
    def name(self, n): self._name = n

    @property
    def manager(self): return self._manager

    @property
    def master(self):
        if isinstance(self.manager, str): return self.manager
        return self.manager.master

    @property
    def number(self): return self._number


class ObjectsManager(ObjectsMixins):
    ObjectType = Object
    MultipleSubsPerMonth = False

    @property
    def objectName(self): return self.ObjectType.__name__

    def __init__(self, master=None, date=None, previous=None):
        assert master != None, 'Master can not be None.'
        self._master = master
        self._subs = []
        ObjectsMixins.__init__(self, date=date or master.date, previous=previous)

    def __len__(self): return len(self.subs)

    def __str__(self): return f'{self.master} | {self.name}'

    @property
    def master(self): return self._master
    @property
    def manager(self): return self._master

    @property
    def subs(self): return self._subs

    @property
    def subsByNumber(self):
        subs = self.subs
        s_numbers = [a.number for a in subs]
        ordered_numbeers = sorted(s_numbers)
        ordered = []
        for num in ordered_numbeers:
            index = s_numbers.index(num)
            order = self.subs[index]
            ordered.append(order)

        return ordered

    @property
    def subsByDate(self): return sorted(self._subs)

    @subs.setter
    def subs(self, subs): self._subs = subs

    @property
    def first(self):
        if len(self._subs):
            first_ = self.subsByNumber[0]
            assert first_.previous == None, f'{self} is not the first.'
            return first_

    @property
    def last(self):
        if len(self._subs):
            l = len(self._subs)
            last_ = self.subsByNumber[-1]
            assert last_.next == None, f'{self} is not the last.'
            return last_

    def addSub(self, sub):
        self._subs.append(sub)
        self.active = sub.date

    def getSub(self, **attrs_vals):
        if len(self):
            for sub in self:
                count = []
                for attr, val in attrs_vals.items():
                    if val == None: v = True

                    elif attr == 'month': v = getattr(sub, attr).monthYear == val.monthYear

                    elif 'date' in attr:
                        if '-' in attr:
                            w = attr.split('-')[1]
                            if w == 'd': v = sub.date.isSameDay(val)
                            elif w == 'm': v = sub.date.isSameMonth(val)
                            elif w == 'y': v = sub.date.isSameYear(val)
                            elif w == 't': v = sub.date.isSameDate(val)
                        else: v = sub.date == val

                    else: v = getattr(sub, attr) == val

                    count.append(v)

                if count.count(True) == len(count): return sub

    def createSub(self, *args, date=None, month=None, **kwargs):
        last = self.last
        subsByMonth = self.sortSubsByMonth(month or PRMP_DateTime.now())
        subsByMonth.sort()
        if not self.MultipleSubsPerMonth:
            if len(subsByMonth): raise self.Errors(f'Multiple {self.ObjectType.__name__} can\'t be created within a month.')
        else: last = subsByMonth[-1] if len(subsByMonth) else None

        if month: kwargs = dict(month=month, **kwargs)

        sub = self.ObjectType(self, *args, previous=last, number=len(self)+1, date=date, **kwargs)

        if last: last.next = sub

        self.addSub(sub)

        return sub

    def deleteSubs(self): self._subs = []

    def removeSub(self, sub):
        if sub in self: self._subs.remove(sub)

    def removeSubByIndex(self, index):
        if len(self.subs) >= index:
            sub = self.subs[index]
            sub.delete()
            self.removeSub(sub)
        else: raise ValueError(f'Total Subs is not upto {index}.')

 ########## Sorting

    def sortSubsByDate(self, date):
        date = self.getDate(date)

        _rec = [rec for rec in self if str(rec.date) == str(date)]
        return _rec

    #Day Sorting
    def sortSubsByDay(self, date):
        recs = [sub for sub in self if sub.date.dayName == date.dayName]
        return recs

    def sortSubsIntoDaysInWeek(self, week):
        week = self.getDate(week)
        days = [sub for sub in self if sub.date.isSameWeek(week)]
        return days

    def sortSubsIntoDaysInMonth(self, month):
        month = self.getDate(month)
        days = [sub for sub in self if sub.date.isSameMonth(month)]
        return days

    #Week Sorting
    def sortSubsByWeek(self, date):
        date = self.getDate(date)
        subs = []
        for sub in self:
            if sub.date.week == date.week: subs.append(sub)
        return subs

    def sortSubsIntoWeeksInMonth(self, month):
        daysSub = self.sortSubsIntoDaysInMonth(month)
        weeksSub = daysSub.sortSubsIntoWeeks()
        return weeksSub

    def sortSubsIntoWeeksInYear(self): pass

    #Month Sorting
    def sortSubsByMonth(self, month): return self.sortSubsIntoDaysInMonth(month)

    def sortSubsIntoMonthsInYear(self, year):
        year = self.getDate(year)
        yearSubs = [sub for sub in self if sub.date.isSameYear(year)]
        return yearSubs

    #Year Sorting
    def sortSubsByYear(self, year):
        year = self.getDate(year)
        recs = [rec for rec in self if rec.date.isSameYear(year)]
        return recs

    def sortSubsIntoYears(self):
        years = self.subsYears
        yearsSubs = [self.sortSubsByYear(PRMP_DateTime.creatDateTime(year=year)) for year in years]
        return yearsSubs

















# Record is the {money, date} recieved daily a.k.a DayRecord

class CoRecords(list):
    def __bool__(self): return True
    def addCoRecord(self, coRecord): self.append(coRecord)



class Record(Object):
    Manager = 'RecordsManager'
    _type = 'rec'
    subTypes = ['Co Records', 'Linked Records']

    def __init__(self, manager, money, note='Note', coRecord=None, **kwargs):
        self.money = money
        self.note = note
        self.__coRecord = coRecord
        self.__coRecords = None
        self.type = None

        Object.__init__(self, manager, name=note, **kwargs)


        if coRecord != None: coRecord.addCoRecord(self)
        else:
            self.__coRecords = CoRecords()
            self.addCoRecord(self)

        self.addEditableValues([{'value': 'money', 'type': int}, 'note', 'date'])

    def addCoRecord(self, coRecord):
        if coRecord in self.coRecords: return
        self.coRecords.addCoRecord(coRecord)

    def updateOtherCoRecord(self, other):
        for rec in self.__coRecords: rec.addCoRecord(self)

    def classInLinkedRecords(self, className): return className in [rec.className for rec in self]

    cilr = classInLinkedRecords

    def updateCoRecord(self):
        for rec in self.__coRecords: rec.updateOtherCoRecord(self)

    @property
    def subs(self): return self.linkedRecords or []

    @property
    def coRecord(self): return self.__coRecord

    @property
    def coRecords(self):
        if self.__coRecords != None: return self.__coRecords
        elif self.__coRecord != None: return self.__coRecord.coRecords

    @property
    def linkedRecords(self): return [c for c in self.coRecords if c is not self]

    def update(self, values={}, first=1):
        super().update(values)
        if first:
            for rec in self: rec.update(values, 0)
        self.manager.update()

    def __int__(self): return int(self.money)
    def __float__(self): return float(self.money)

    def __str__(self): return f'{self.manager} | {self.name}'

    def __repr__(self): return f'<{self.name}>'

    @property
    def name(self): return f'{self.className}({self.moneyWithSign}, {self.date.date}, {self.note})'

    @property
    def region(self): return self.manager.region

    def set(self, money): self.money = money

    def add(self, money): self.money += money

    def substract(self, money): self.money -= money

DayRecord = Record


class Repayment(Record):
    dueSeason = ''
    dueTime = 0
    duing =  True
    Manager = 'RepaymentsManager'
    subTypes = ['Repayments']
    ObjectType = None

    def __init__(self, manager, money, date=None, **kwargs):
        super().__init__(manager=manager, money=money, date=date, **kwargs)
        if self.duing: assert self.dueSeason and self.dueTime, 'Due Season and Time must be set.'

        if self.dueSeason == 'year': self.__dueDate = self.date + (self.dueTime * 12)
        elif self.dueSeason == 'month': self.__dueDate = self.date + self.dueTime
        elif self.dueSeason == 'day': self.__dueDate = self.date + datetime.timedelta(days=self.dueTime)

        if not self.ObjectType:
            self.ObjectType = RecordsManager

        self.__repaymentsManager = self.ObjectType(self)

    def __getitem__(self, num): return self.repaymentsManager[num]

    def __len__(self): return len(self.repaymentsManager)

    @property
    def records(self): return self.repaymentsManager.records

    @property
    def isDue(self): return PRMP_DateTime.now() > self.dueDate

    @property
    def dueDate(self): return self.__dueDate

    @property
    def outstanding(self): return float(self) - self.repaid

    @property
    def paid(self): return float(self) == self.repaid

    @property
    def repaid(self): return float(self.repaymentsManager)

    @property
    def repayment(self): return self.repaid

    @property
    def repayments(self): return self.repaymentsManager

    @property
    def repaymentsManager(self): return self.__repaymentsManager

    def addRepayment(self, repay, **kwargs):
        if self.paid: raise Errors.RepaymentError(f'{self.className} is already repaid.')
        else:
            if self.outstanding < repay: raise Errors.RepaymentError(f'Outstanding repayments ({self.outstanding}) is less than the repayment given ({repay}).')
            else:
                repayment = self.repaymentsManager.createRecord(repay, **kwargs)
                if self.paid: self.completed()
                return repayment

    @property
    def name(self): return f'{self.className}({self.moneyWithSign}, {self.date.date}, {self.note})'

    def completed(self): pass

class Salary(Record):
    pass

class Loan(Repayment):
    dueSeason = 'year'
    dueTime = 11
    rate = 2
    Manager = 'LoanBond'

    def __init__(self, loanBond, interestRate=.1, dueTime=None, **kwargs):
        if dueTime: self.dueTime = dueTime

        super().__init__(loanBond, loanBond.proposedLoan, **kwargs)

        self.__interestRate = interestRate
        self.__loanInterests = LoanInterests(self)

    def __str__(self):
        st = super().__str__()
        st = st.split('|')
        del st[-3]
        return '|'.join(st)

    @property
    def loanBond(self): return self.manager
    @property
    def interestRate(self): return self.__interestRate
    @property
    def loanInterests(self): return self.__loanInterests
    @property
    def paidInterests(self): return self.loanInterests.paid

    def repayInterest(self, repay):
        assert repay > 0, 'Repay must be more than zero (0).'
        if self.paid: raise Errors.LoanRepaymentsError('Loan is already repaid.')
        #  pay interest accordingly first
        else: pass

    def addDoubleInterest(self, date=None):
        if self.isDue:
            doubleInterest = self.outstanding * .2
            self.loanInterestsManager.addLoanInterest(doubleInterest, date)

class LoanBond(Repayment):
    duing = False
    LoanType = Loan
    Manager = 'LoanBonds'

    def __init__(self, manager, money, proposedLoan, **kwargs):
        super().__init__(manager, money, **kwargs)

        validLoan = manager.validLoan
        assert validLoan >= proposedLoan, f'Loan {proposedLoan} exceed maximum valid loan of {validLoan}.'

        self.grantedDate = None
        self.proposedLoan = proposedLoan
        self.details = None
        self.loan = None

    def addLoanRepayment(self, money, **kwargs):
        if self.granted: return self.loan.addRepayment(money, **kwargs)
        else: raise Errors.LoanRepaymentsError("Not yet granted. There's no loan to repay.")

    @property
    def outstandingLoan(self): return self.loan.outstanding if self.loan else 0

    @property
    def granted(self):
        if self.paid and self.loan: return True
        return False

    @property
    def paidLoan(self): return self.loan.paid

    @property
    def filledLoanBond(self):
        if self.details: return True
        else: return False

    def completed(self):
        pass

    def fillLoanBond(self, ):
        pass

    def grant(self, interestRate=.1, dueTime=None, date=None): self.loan = self.LoanType(self, date=date, interestRate=interestRate, dueTime=dueTime)

class LoanInterest(Repayment):
    duing = False
    Manager = 'LoanInterests'

    def __init__(self, manager, interest, interestRate=None, **kwargs):
        if interestRate: self.__interestRate = interestRate

        super().__init__(manager, interest, **kwargs)

    @property
    def interestRate(self): return self.__interestRate

    def repayInterest(self, interest, **kwargs): return self.createRecord(interest, **kwargs)







# RecordsManager is the manager of records. It has a property 'records' which is a list of Records

# These serve as a container for the records for the period of season contained. They are given records by after being sorted by the RecordsManager.

# DailyRecords comprises of the Records recieved and accounted for in a Day.
# WeeklyRecords comprises of the DailyRecords recieved and accounted for in a Week.
# MonthlyRecords comprises of the DailyRecords and WeeklyRecords (as specified to the constructor) recieved and accounted for in a Month.
# YearlyRecords comprises of the DailyRecords,WeeklyRecords and MonthlyRecords (as specified to the constructor) recieved and accounted for in a Year.


class SeasonRecord(ObjectsMixins):
    maximum = 0
    def __init__(self, records, date=None):
        if self.maximum: assert len(records) <= self.maximum, f'Records may not be more than {self.maximum}'

        super().__init__(date=date, idReq=1)
        self._subs = records
        self._subs.sort()

        man = records[0].manager
        for rec in records: assert rec.manager.className == man.className, 'Records of different manager types given.'



    def __int__(self): return sum([int(rec) for rec in self])
    def __float__(self): return sum([float(rec) for rec in self])

    # def __getitem__(self, num): return self.records[num]

    # def __len__(self): return len(self.records)

    @property
    def manager(self): return self.records[0].manager

    # @property
    # def date(self): return self.records[0].date

    @property
    def subs(self): return self._subs
    @property
    def records(self): return self.subs

    def get(self, season, wh):
        if season == 'year':
            for rec in self:
                if wh == rec.year: return rec
        elif season == 'month':
            for rec in self:
                if wh == rec.month: return rec
        elif season == 'day':
            for rec in self:
                if wh == rec.day: return rec

class WeekRecord(SeasonRecord, CompareByWeek):
    maximum = 7

    def __init__(self, records, date=None):
        SeasonRecord.__init__(self, records, date=date)
        self.recDayNames = [rec.date.dayName for rec in records]

    def __str__(self): return f'{self.manager} | {self.className}({self.weekMonthYear}) | {self.moneyWithSign}'

    def _day(self, name):
        if name in self.recDayNames:
            for rec in self:
                if name.title() == rec.date.dayName: return rec
    @property
    def sunday(self): return self._day('Sunday')
    @property
    def monday(self): return self._day('Monday')
    @property
    def tuesday(self): return self._day('Tuesday')
    @property
    def wednesday(self): return self._day('Wednesday')
    @property
    def thursday(self): return self._day('Thursday')
    @property
    def friday(self): return self._day('Friday')
    @property
    def saturday(self): return self._day('Saturday')

class MonthRecord(SeasonRecord, CompareByMonth):
    maximum = 5

    def __init__(self, records, weeks=False):
        super().__init__(records)
        self.__weeks = []
        self.__sorted = False
        if weeks: self.sortRecordsIntoWeeks()

    def __str__(self): return f'{self.manager} | {self.className}({self.monthYear}) | {self.moneyWithSign}'

    def sortRecordsIntoWeeks(self):
        if self.__sorted: return self
        daysRec = [record for record in self if record.date.isSameMonth(self.date)]
        weeks = PRMP_DateTime.monthYearOfMonthWeekDays(dateObj=self.date)
        week1 = []
        week2 = []
        week3 = []
        week4 = []
        week5 = []
        for dayRec in daysRec:
            if dayRec.date.monthYear in weeks[0]: week1.append(dayRec)
            elif dayRec.date.monthYear in weeks[1]: week2.append(dayRec)
            elif dayRec.date.monthYear in weeks[2]: week3.append(dayRec)
            elif dayRec.date.monthYear in weeks[3]: week4.append(dayRec)
            elif dayRec.date.monthYear in weeks[4]: week5.append(dayRec)

        self.__weeks = [WeekRecord(week1), WeekRecord(week2),  WeekRecord(week3),  WeekRecord(week4),  WeekRecord(week5)]
        self.__sorted = True
        return self

    @property
    def __week(self, num):
        try: return self.__weeks[num]
        except: pass
    @property
    def week1(self): return self.__week(0)
    @property
    def week2(self): return self.__week(1)
    @property
    def week3(self): return self.__week(2)
    @property
    def week4(self): return self.__week(3)
    @property
    def week5(self): return self.__week(4)

class YearRecord(SeasonRecord, CompareByYear):
    maximum = 12

    def __init__(self, records, months=False):
        super().__init__(records)
        self.__months = []
        if months: self.recMonthNames = [rec.date.monthName for rec in records]

    def __str__(self): return f'{self.manager} | {self.className}({self.year}) | {self.moneyWithSign}'

    def sortRecordsIntoMonths(self):
        jan = []
        feb = []
        mar = []
        apr = []
        may = []
        jun = []
        jul = []
        aug = []
        sep = []
        octo = []
        nov = []
        dec = []

        for rec in self:
            if rec.monthName == MONTHS_NAMES[1]: jan.append(rec)
            elif rec.monthName == MONTHS_NAMES[2]: feb.append(rec)
            elif rec.monthName == MONTHS_NAMES[3]: mar.append(rec)
            elif rec.monthName == MONTHS_NAMES[4]: apr.append(rec)
            elif rec.monthName == MONTHS_NAMES[5]: may.append(rec)
            elif rec.monthName == MONTHS_NAMES[6]: jun.append(rec)
            elif rec.monthName == MONTHS_NAMES[7]: jul.append(rec)
            elif rec.monthName == MONTHS_NAMES[8]: aug.append(rec)
            elif rec.monthName == MONTHS_NAMES[9]: sep.append(rec)
            elif rec.monthName == MONTHS_NAMES[10]: octo.append(rec)
            elif rec.monthName == MONTHS_NAMES[11]: nov.append(rec)
            elif rec.monthName == MONTHS_NAMES[12]: dec.append(rec)

        self.__months = [MonthRecord(jan), MonthRecord(mar), MonthRecord(feb), MonthRecord(apr), MonthRecord(may), MonthRecord(jun), MonthRecord(jul), MonthRecord(aug), MonthRecord(sep), MonthRecord(octo), MonthRecord(nov), MonthRecord(dec)]
        self.recMonthNames = [rec.date.monthName for rec in self.__months]

    def __year(self, monthName):
        try:
            if monthName in self.recMonthNames:
                for rec in self.__months:
                    if monthName == rec.date.monthName: return rec
        except: pass

    @property
    def months(self): return self.__months
    @property
    def january(self): return self.__year(MONTHS_NAMES[1])
    @property
    def february(self): return self.__year(MONTHS_NAMES[2])
    @property
    def march(self): return self.__year(MONTHS_NAMES[3])
    @property
    def april(self): return self.__year(MONTHS_NAMES[4])
    @property
    def may(self): return self.__year(MONTHS_NAMES[5])
    @property
    def june(self): return self.__year(MONTHS_NAMES[6])
    @property
    def july(self): return self.__year(MONTHS_NAMES[7])
    @property
    def august(self): return self.__year(MONTHS_NAMES[8])
    @property
    def september(self): return self.__year(MONTHS_NAMES[9])
    @property
    def october(self): return self.__year(MONTHS_NAMES[10])
    @property
    def november(self): return self.__year(MONTHS_NAMES[11])
    @property
    def december(self): return self.__year(MONTHS_NAMES[12])

class RecordsWithSameSeasons(SeasonRecord):

    def __init__(self, records, name):
        super().__init__(records)
        self.__class__.__name__ = name

    def __str__(self): return f'{self.manager} | {self.className}s | {self.moneyWithSign}'

class RecordsManager(ObjectsManager):
    lowest = 50
    ObjectType = Record
    MultipleSubsPerMonth = True
    subTypes = ['Records']

    def __init__(self, account=None): ObjectsManager.__init__(self, account)

    def __float__(self): return float(self.totalMonies)
    def __int__(self): return int(self.totalMonies)

    def __str__(self): return f'{self.account} | {self.name}'

    def __len__(self): return len(self.records)

    def __repr__(self): return f'<{self.name}>'

    @property
    def date(self):
        if self.master: return self.master.date
        return self._date

    @property
    def money(self): return float(self)

    @property
    def name(self): return f'{self.className}({self.moneyWithSign}, {self.date.date})'

    @property
    def account(self): return self.master

    @property
    def region(self): return self.account.region

    @property
    def records(self): return self.subs

    @property
    def lastMoney(self): return float(self._subs[-1]) if self._subs else 0

    @property
    def lastRecord(self): return self.last

    @property
    def totalMonies(self): return sum([float(record) for record in self[:]])

    @property
    def recordDateTuples(self): return [(str(record.date), float(record)) for record in self]

    @property
    def dates(self): return [record.date for record in self]

    def _setRecords(self, records): self._subs = records

    def createRecord(self, money, date=None, newRecord=True, notAdd=False, **kwargs):
        '''
        money: type float; transaction to be in the record.
        date: type PRMP_DateTime; date of the transaction.
        newRecord: type bool; whether to create a new record or (add/set) to a record already done
        notAdd: type bool; useful when param newRecord=False, it\'s whether to set the money to a transaction already made or not
        kwargs: further params that a ObjectType might need.
        '''
        money = float(money)
        if not money: return

        new = False
        record = None

        date = self.getDate(date)

        # if self.className == 'BroughtForwards': print(date.date, newRecord, money)

        if newRecord: new = True
        else:
            if date in list(self.dates):
                new = False
                record = self.sortRecordsByDate(date)
                if isinstance(record, list): record = record[0]
                if record:
                    if notAdd: record.set(money)
                    else: record.add(money)
            else: new = True

        if new:
            record = self.createSub(money, date=date, **kwargs)
            # self.records.sort()

        return record

    def updateWithOtherManagers(self, managers):
        self.deleteSubs()
        total = sum([float(manager) for manager in managers])
        self.createRecord(total, newRecord=False, notAdd=True)

    def removeRecord(self, rec): self.removeSub(rec)

    def removeRecordByIndex(self, index): self.removeSubByIndex(index)

    def checkMoney(self, money):
        if (money < self.lowest): raise ValueError(f'Amount of {money} is too small.')
        if (money % 5) != 0: raise ValueError(f'Amount of {money} is not valid.')
        return 1

    @property
    def recordsYears(self):
        years = []
        for rec in self:
            if rec.year in years: continue
            else: years.append(rec.year)
        return years

    @property
    def recordsAsList(self): return [float(record) for record in self]
    @property
    def recordsAsTupleFull(self): return [(record, float(record)) for record in self]
    @property
    def recordsAsTupleShort(self): return [(self.className, str(record.date), float(record)) for record in self]
    @property
    def recordsAsTuple(self): return [(str(record.date), float(record)) for record in self]
    @property
    def recordsAsDict(self): return [{str(record.date): float(record)} for record in self]
    @property
    def recordsAsDictFull(self): return [{record: float(record)} for record in self]
    @property
    def recordsAsDictShort(self): return [{str(record.date): float(record)} for record in self]

    def recordsAsRecord(self, records, date):
        if records:
            money = .0
            for _rec in records: money += float(_rec)
            rec = self.ObjectType(self, money, date=date)
            return rec

    def recordsAsRecordsManager(self, records, date):
        newRecM = self.class_(self.manager)
        newRecM.date = date
        if records:
            rec = self.recordsAsRecord(records, date)
            newRecM.addSub(rec)
        return newRecM


    ############ Sorting
    #Date Sorting

    def sortRecordsByDate(self, date):
        _rec = self.sortSubsByDate(date)
        return _rec

    #Day Sorting
    def sortRecordsByDay(self, date):
        recs = self.sortSubsByDay(date)
        if recs: return RecordsWithSameSeasons(recs, date.dayName)

    def sortRecordsIntoDaysInWeek(self, week):
        days = self.sortSubsIntoDaysInWeek(week)
        if days: return WeekRecord(days)

    def sortRecordsIntoDaysInMonth(self, month):
        days = self.sortSubsIntoDaysInMonth(month)
        return MonthRecord(days)

    #Week Sorting
    def sortRecordsByWeek(self, week):
        records = self.sortSubsByWeek(week)
        if records: return WeekRecord(records)

    def sortRecordsIntoWeeksInMonth(self, month):
        weeksRec = self.sortSubsIntoWeeksInMonth(month)
        return weeksRec

    def sortRecordsIntoWeeksInYear(self): pass

    #Month Sorting
    def sortRecordsByMonth(self, month): return self.sortSubsByMonth(month)

    def sortRecordsIntoMonthsInYear(self, year):
        yearRecs = self.sortSubsIntoMonthsInYear(year)
        year = YearRecord(yearRecs)
        year.sortRecordsIntoMonths()
        return year

    def sortRecordsIntoMonthsInYears(self):
        yearsRecs = YearRecord(self.records)
        yearsRecs.sortRecordsIntoMonths()
        return yearsRecs

    #Year Sorting
    def sortRecordsByYear(self, year):
        recs = self.sortSubsByYear(year)
        return YearRecord(recs)

    def sortRecordsIntoYears(self):
        yearsRecs = self.sortSubsIntoYears()
        return SeasonRecord(yearsRecs)

class RepaymentsManager(RecordsManager):
    ObjectType = Repayment

    @property
    def paid(self):
        for repay in self[:]:
            if repay and (not repay.paid): return False
        return True

    @property
    def outstanding(self):
        out = 0
        for record in self:
            if record: out += record.outstanding
        return out

    @property
    def repaid(self):
        rep = 0
        for record in self: rep += record.repaid
        return rep

    def updateWithOtherManagers(self, managers):
        self.subs = managers

    def addRepayment(self, repay, **kwargs):
        outs = self.outstanding
        if repay > outs: raise Errors.RepaymentError(f'Repay of {repay} is > Outstanding of {outs} ')
        rem_outs = repay
        for rep in self:
            if rem_outs:
                if not rep.paid:
                    if repay > rep.outstanding:
                        rem_outs = repay - rep.outstanding
                        rep.addRepayment(rep.outstanding, **kwargs)
                    else:
                        rep.addRepayment(rem_outs, **kwargs)
                    rem_outs = 0

class SalariesManager(RecordsManager):
    ObjectType = Salary
    def person(self): return self.account
    def addSalary(self, salary, date=None): return self.createRecord(salary, date=date)

class LoanInterests(RepaymentsManager):
    ObjectType = LoanInterest

    def __init__(self, manager):
        super().__init__(manager)
        self.addLoanInterest(date=manager.date)

    def addLoanInterest(self, **kwargs):
        interestRate = self.loan.interestRate
        interest = self.loan.outstanding * interestRate
        self.createRecord(interest, interestRate=interestRate, **kwargs)

    @property
    def loan(self): return self.account

    @property
    def paid(self):
        for interest in self:
            if not interest.paid: return False
        return True

class LoanBonds(RepaymentsManager):
    ObjectType = LoanBond

    @property
    def validLoan(self): return self.account.validLoan

    def newLoanBond(self, money, proposedLoan, **kwargs):
        last = self.lastRecord
        go = 1
        if last:
            outstandingLoan = last.outstandingLoan

            if last.paid and last.granted:
                if last.paidLoan: pass
                elif outstandingLoan: raise Errors.LoanBondsError(f'There is a paid loan bond with an outstanding loan ({outstandingLoan}).')
            elif not last.granted: raise Errors.LoanBondsError('There is a paid loan bond with a pending loan.')
            else: raise Errors.LoanBondsError('There is an outstanding loan bond not yet paid.')

        loanBond = self.createRecord(money,  proposedLoan=proposedLoan, **kwargs)
        return loanBond







# Account is the list of Records recieved for a month.
# AccountsManager is the manager of Accounts. It has a property 'accounts' which is a list of Accounts for the life time of the associated region.

# These serve as a container for the accounts for the period of season contained. They are given accounts by after being sorted by the AccountsManager.
# DailyAccounts comprises of the Accounts recieved and accounted for in a Day.
# WeeklyAccounts comprises of the DailyAccounts recieved and accounted for in a Week.
# MonthlyAccounts comprises of the DailyAccounts and WeeklyAccounts (as specified to the constructor) recieved and accounted for in a Month.
# YearlyAccounts comprises of the DailyAccounts,WeeklyAccounts and MonthlyAccounts (as specified to the constructor) recieved and accounted for in a Year.



class DailyAccounts(ObjectsMixins):
    #
    pass


class WeeklyAccounts(ObjectsMixins):

    def __init__(self, week, days_accounts, oneWeek=False):
        super().__init__()
        '''
        sort accounts into days in week.

        week: name of the week
        days_accounts: a list of accounts to be containing the accounts per day in the passed week.
        oneWeek: bool to parse the 
        '''
        self.week = week
        self.monday = [day for day in days_accounts if day.date.dayName == 'Monday']
        self.tuesday = [day for day in days_accounts if day.date.dayName == 'Tueday']
        self.wednesday = [day for day in days_accounts if day.date.dayName == 'Wednesday']
        self.thurday = [day for day in days_accounts if day.date.dayName == 'Thursday']
        self.friday = [day for day in days_accounts if day.date.dayName == 'Friday']
        self.saturday = [day for day in days_accounts if day.date.dayName == 'Saturday']
        self.sunday = [day for day in days_accounts if day.date.dayName == 'Sunday']

        for day in self.__dict__:
            if ('_' in day) or (not self.__dict__[day]):
                # if _ starts the key in self.__dict__ or key's value == [] or None
                continue

            if self.__dict__[day]:
                if oneWeek: # sums up the value of the day
                    self.__dict__[day] = self.__dict__[day][0]
                else: self.__dict__[day] = sum(self.__dict__[day])


class MonthlyAccounts(ObjectsMixins):
    def __init__(self, monthName, accounts, day=False):
        super().__init__()
        '''
        monthName: name of the month
        accounts: list of accounts to parse
        day: bool, whether to parse the accounts as [days in month, weeks in month]
        '''
        self.monthName = monthName
        self.day = day
        if day == False:
            self.week1 = [record for record in accounts if record.date.week == 1]
            self.week2 = [record for record in accounts if record.date.week == 2]
            self.week3 = [record for record in accounts if record.date.week == 3]
            self.week4 = [record for record in accounts if record.date.week == 4]
            self.week5 = [record for record in accounts if record.date.week == 5]
            self.others = [record for record in accounts if record not in [week1 + week2 + week3 + week4 + week5]]
        else:
            self.days = accounts.sort()


class YearlyAccounts(ObjectsMixins):
    pass

class MonthCompare:
    'compares the instances via their date.month'

    def __lt__(self, other):
        if other == None: return False
        return self.month < other.month
    def __le__(self, other):
        if other == None: return False
        return self.month <= other.month
    def __eq__(self, other):
        if other == None: return False
        return self.month is other.month
    def __ne__(self, other):
        if other == None: return True
        return self.month != other.month
    def __gt__(self, other):
        if other == None: return True
        return self.month > other.month
    def __ge__(self, other):
        if other == None: return True
        return self.month >= other.month

class Account(MonthCompare, Object):
    Manager = 'AccountsManager'
    subTypes = ['Records Managers']
    Error = Errors

    def __init__(self, manager, **kwargs):
        '''
        manager: an object to act as the manager
        kwargs: options to pass to the constructor of class Object
        '''
        assert manager != None, 'No manager passed.'
        Object.__init__(self, manager, **kwargs)

    def __eq__(self, account):
        if account == None: return False
        try: res = ((self.number == account.number) and super().__eq__(account) and self.manager is account.manager)
        except AttributeError: return False

    def __str__(self): return f'{self.manager} | {self.name}'
    def __len__(self): return len(self.recordsManagers)
    def __int__(self): return self.balances

    @property
    def name(self): return f'{self.className}({self.date.dayMonthYear})'

    @property
    def money(self): return float(self)

    @property
    def region(self): return self.manager.region

    @property
    def subs(self): return self.recordsManagers or []

    @property
    def recordsManagers(self): return []

    @property
    def headers(self): return [rec.className for rec in self.recordsManagers]

    @property
    def nextAccount(self): return self.next
    @property
    def previousAccount(self): return self.previous

    @property
    def recordsManagersAsList(self): return [float(recordsManager) for recordsManager in self]
    @property
    def recordsManagersAsTupleFull(self): return [(recordsManager, float(recordsManager)) for recordsManager in self]
    @property
    def recordsManagersAsTupleShort(self): return [(recordsManager.shortName, float(recordsManager)) for recordsManager in self]
    @property
    def recordsManagersAsTuple(self): return [(recordsManager.className, float(recordsManager)) for recordsManager in self]
    @property
    def recordsManagersAsDict(self): return [{recordsManager.className: float(recordsManager)} for recordsManager in self]
    @property
    def recordsManagersAsDictFull(self): return [{recordsManager: float(recordsManager)} for recordsManager in self]
    @property
    def recordsManagersAsDictShort(self): return [{recordsManager.shortName: float(recordsManager)} for recordsManager in self]

    def _balanceAccount(self):
            pass
    def balanceAccount(self): self.notImp()


class AccountsManager(ObjectsManager):
    ObjectType = Account
    subTypes = ['Accounts']

    def __init__(self, region, autoAccount=True, **kwargs):
        'region: same as [manager, master]'
        ObjectsManager.__init__(self, region)

        self.addAccount = self.addSub
        self.getAccount = self.getSub
        if autoAccount == True: self.createAccount(**kwargs)

    def __eq__(self, manager):
        if manager == None: return False
        return self.region == manager.region
    def __float__(self): return sum([float(acc.balances) for acc in self])
    def __int__(self): return sum([int(acc.balances) for acc in self])
    def __str__(self):
        if self.region != None: return f'{self.region} | {self.className}'
        return f'{self.className}'

    def createAccount(self, **kwargs):
        account =  self.createSub(**kwargs)
        return account

    @property
    def firstAccount(self): return self.first
    @property
    def lastAccount(self): return self.last

    @property
    def accounts(self): return self.subs

    @property
    def region(self): return self.master
    @property
    def name(self): return f'{self.region.name} | {self.className}'

    @property
    def headers(self): return self.lastAccount.headers

    @property
    def overAllAccounts(self):
        # total accounts in this manager
        lengthOfAccounts = len(self)
        if lengthOfAccounts:
            # total recordsManager in an account
            lengthOfRecordManagers = len(self[0])
            containerDict = {}
            for account in self:
                for recordManager in account:
                    name = recordManager.className
                    if name not in containerDict: containerDict[name] = 0
                    containerDict[name] += float(recordManager)
            return containerDict

    def balanceAccount(self, month=None):
        if month:
            account = self.getAccount(month=self.getDate(month))
            if account: account.balanceAccount()
        else:
            account = self.getLastAccount()
            if account: account.balanceAccount()
        return account

    def balanceAccounts(self):
        for accounts in self: accounts.balanceAccount()
        return self.accounts

    def currentMonthAccounts(self): return self.sortAccountsByMonth(PRMP_DateTime.now())

    def sortSubRegionsAccountsByMonth(self, month):
        PRMP_DateTime.checkDateTime(month)
        subRegionsActiveByMonth = self.region.subRegionsActiveByMonth(month)

        accounts = []
        for subRegion in subRegionsActiveByMonth:
            subRegionsAccounts = subRegion.sortAccountsByMonth(month) or []
            accounts.extend(subRegionsAccounts)
        return accounts

    def subRegionsActiveByMonth(self, month):
        subRegions = []
        for subRegion in self.region.subRegionsManager:
            monthAccount = subRegion.accountsManager.getAccount(month=month)
            if monthAccount != None: subRegions.append(subRegion)
        # or Subs = [Sub for Sub in self.Subs if Sub.lastAccount.date.isSameMonth(month)]

        return subRegions

    def sortSubsByMonth(self, month): return [sub for sub in self if sub.month.isSameMonthYear(month)]


   #Month Sorting
    def sortSubsAccountsByMonth(self, month):
        PRMP_DateTime.checkDateTime(month)
        Subs = self.subRegionsActiveByMonth(month)
        accounts = []
        for Sub in Subs:
            SubAccounts = Sub.accountsManager.sortSubsByMonth(month)
            accounts.extend(SubAccounts)
        return accounts


class SameTimesAccounts(ObjectsMixins):

    def __init__(self, obj):
        self.obj = obj
        self.subs = []

    def setStage(self):
        pass











'''
DC Objects = Region, Person, Account, Records, Client, Area
and Managers

'''


class Person(Object):
    Manager = 'PersonsManager'
    
    _male = 'male', 'm'
    _female = 'female', 'f'
    
    def __init__(self, manager=None, gender='n', phone='', image=None, email='', address='', date=None, name='', **kwargs):
        
        if isinstance(manager, Region): date = manager.date
        
        names = name.split(' ')
        names = [name.title() for name in names]
        name = ' '.join(names)

        super().__init__(manager, date=date, name=name)

        gender = gender.lower()
        
        if gender in self._male:  self.gender = self._male[0].title()
        elif gender in self._female:  self.gender = self._female[0].title()
        
        else: self.gender = 'Neutral'
        
        self.phone = phone
        
        self.image = image

        self.__email = None
        self.email = email
        
        self.address = address

        self.addEditableValues(['gender', 'phone', 'image', 'email', 'address', 'name', 'date'])
    
    def __str__(self): return f'{self.manager} | {self.className}({self.name})'
    
    @property
    def values(self):
        vals = super().values
        vals.update({'manager': self.manager})
        return vals

    @property
    def email(self): return self.__email

    @email.setter
    def email(self, email):
        if email:
            if self.checkEmail(email): self.__email = email
            # else: raise ValueError(f'{email} is not a valid email.')

class Region(Object):
    AccountsManager = AccountsManager
    Manager = 'RegionsManager'
    SubRegionsManager = None
    PersonsManager = None
    _type = 'reg'
    
    subTypes = ['Regions', 'Accounts', 'Persons']

    
    def __init__(self, manager, name=None, date=None, location=None, phone=None, previous=None, number=None, **kwargs):
        
        self._personsManager = None
        self._subRegionsManager = None
        self._location = location
        
        Object.__init__(self, manager, previous=previous, date=date, name=name, number=number, **kwargs)
        
        self._accountsManager = self.AccountsManager(self, **kwargs)
        
        if self.SubRegionsManager:
            self._subRegionsManager = self.SubRegionsManager(self)
            
        if self.PersonsManager:
            self._personsManager = self.PersonsManager(self, name=name, date=date, phone=phone, **kwargs)
    
    def __str__(self): return f'{self.manager.master} | {self.className}({self.name})'
    
    @property
    def totalSubs(self): return len(self.subs)

    @property
    def spacedID(self):
        sup = self.manager if self.strManager else self.sup.spacedID
        return f'{str(sup).replace(" ", "")}'
        
    @property
    def sups(self):
        ss = []
        sup = self.sup
        try:
            while True:
                ss.append(sup)
                sup = sup.sup
        except:
            xx = ss[:-1]
            zz = list(reversed(xx))
            return zz
    
    @property
    def nextRegion(self): return self.next
    
    @property
    def previousRegion(self): return self.previous
    
    @property
    def level(self): return len(self.hierachy)
    
    @property
    def idText(self):
        text = ''
        hie = self.hierachy
        
        for reg in hie[1:]:
            if len(hie) > 2 and reg is hie[2]: name = reg.DEPARTMENT
            else: name = reg.name
            text += name + ' | '

        te = text.split('|')[:-1]
        text = ' | '.join(te)
        return text
    
    @property
    def hierachy(self): return self.sups + [self]
    
    @property
    def hie(self): return self.hierachy
    
    @property
    def hierachyNames(self): return [d.name for d in self.hierachy]
    
    @property
    def reignMonths(self): return self.date - PRMP_DateTime.now() + 1
    @property
    def reignMonthsYears(self): return divmod(self.reignMonths, 12)
    @property
    def gender(self): return self.person.gender if self.person else ''
    
    # @property
    # def name(self):
    #     if self.className == 'Clients': return self.person.name
    #     else: return self._name

    @property
    def phone(self): return self.person.phone if self.person else ''
    
    @property
    def email(self): return self.person.email if self.person else ''
    
    @property
    def address(self): return self.person.address if self.person else ''
    
    @property
    def image(self): return self.person.image if self.person else ''
    
    def getRegion(self, **kwargs): return self.getSubReg(**kwargs)
    
    @property
    def region(self):
        manager = self.manager
        if isinstance(manager, str): return manager
        return manager.region
    
    @property
    def person(self): return self.personsManager.lastPerson if self.personsManager else None
    
    @property
    def personsManager(self): return self._personsManager
    
    @property
    def persons(self): return self.personsManager

    @property
    def location(self): return self._location

    @property
    def subRegionsManager(self): return self._subRegionsManager
    
    @property
    def subs(self): return self.accountsManager or []
    
    @property
    def subRegions(self): return self.subRegionsManager

    @property
    def regions(self): return self.subRegions
    
    @property
    def subRegionsCount(self): return len(self.subRegions)
        
    @property
    def lastAccount(self): return self.accountsManager.lastAccount
    
    @property
    def accountsManager(self): return self._accountsManager
    
    @property
    def accounts(self): return self.accountsManager
    
    @property
    def recordsManagers(self): return self.accountsManager.recordsManagers
    
    def balanceAccounts(self, month=None):
        if month: self.accountsManager.balanceAccount(month)
        else: self.accountsManager.balanceAccounts()
    
    def sortAccountsByMonth(self, month): return self.accountsManager.sortSubsByMonth(month)

 ########## Sorting
  # SubRegions
   #Date Sorting
    def sortSubRegionsByDate(self, date): return self.subRegionsManager.sortRegionsByDate(date)
   #Day Sorting
    def sortSubRegionsByDay(self): return self.subRegionsManager.sortRegionsByDay(date)
    def sortSubRegionsIntoDaysInWeek(self): return self.subRegionsManager.sortRegionsIntoDaysInWeek(date)
    def sortSubRegionsIntoDaysInMonth(self): return self.subRegionsManager.sortRegionsIntoDaysInMonth(date)
    
   #Week Sorting
    def sortSubRegionsByWeek(self): return self.subRegionsManager.sortRegionsByDate(date)
    def sortSubRegionsIntoWeeksInMonth(self): return self.subRegionsManager.sortRegionsIntoWeeksInMonth(date)
    def sortSubRegionsIntoWeeksInYear(self): return self.subRegionsManager.sortRegionsIntoWeeksInYear(date)
    
   #Month Sorting
    def sortSubRegionsByMonth(self, month): return self.subRegionsManager.sortRegionsByMonth(date)
    def sortSubRegionsIntoMonthsInYear(self): return self.subRegionsManager.sortRegionsIntoMonthsInYear(date)
    def sortSubRegionsIntoMonthsInYears(self): return self.subRegionsManager.sortRegionsIntoMonthsInYears(date)
    
   #Year Sorting
    def sortSubRegionsByYear(self): return self.subRegionsManager.sortRegionsByYear(date)
    def sortSubRegionsIntoYears(self): return self.subRegionsManager.sortRegionsIntoYears(date)

  # SubRegions Accounts
   #Date Sorting
    def sortSubRegionsAccountsByDate(self): return self.subRegionsManager.sortRegionsAccountsByDate(date)

   #Day Sorting
    def sortSubRegionsAccountsByDay(self): return self.subRegionsManager.sortRegionsAccountsByDay(date)
    def sortSubRegionsAccountsIntoDaysInWeek(self): return self.subRegionsManager.sortRegionsAccountsIntoDaysInWeek(date)
    def sortSubRegionsAccountsIntoDaysInMonth(self): return self.subRegionsManager.sortRegionsAccountsIntoDaysInMonth(date)
    
   #Week Sorting
    def sortSubRegionsAccountsByWeek(self): return self.subRegionsManager.sortRegionsAccountsByWeek(date)
    def sortSubRegionsAccountsIntoWeeksInMonth(self): return self.subRegionsManager.sortRegionsAccountsIntoWeeksInMonth(date)
    def sortSubRegionsAccountsIntoWeeksInYear(self): return self.subRegionsManager.sortRegionsAccountsIntoWeeksInYear(date)
    
   #Month Sorting
    def sortSubRegionsAccountsByMonth(self, month): return self.subRegionsManager.sortRegionsAccountsIntoMonthsInYear(month)
        
    def sortSubRegionsAccountsIntoMonthsInYear(self): return self.subRegionsManager.sortRegionsAccountsIntoMonthsInYear(date)
    def sortSubRegionsAccountsIntoMonthsInYears(self): return self.subRegionsManager.sortRegionsAccountsIntoMonthsInYears(date)
    
   #Year Sorting
    def sortSubRegionsAccountsByYear(self): return self.subRegionsManager.sortRegionsAccountsByYear(date)
    def sortSubRegionsAccountsIntoYears(self): return self.subRegionsManager.sortRegionsAccountsIntoYears(date)

class Staff(Region):
    AccountsManager = SalariesManager
    Manager = 'StaffsManager'
    Person = None
    def salariesManager(self): return self.accountsManager
    def paySalary(self, salary, date=None): self.salariesManager.addSalary(salary, date=date)

class ThirdPartySurety(ObjectsMixins):
    
    def __init__(self, loanBondDetails=None, name='', dob='', maritalStatus='', phone='', address='', officeAddress='', religion='', homeTown='', stateOfOrigin='', occupation='', knowledgeOfMember='', email='', relationshipWithMember='', image='', date=None):
        super().__init__()
        self.loanBondDetails = loanBondDetails
        self.name = None
        
        self.dob = dob
        self.maritalStatus = maritalStatus
        self.phone = phone
        self.address = address
        self.officeAddress = officeAddress
        self.religion = religion
        self.homeTown = homeTown
        self.stateOfOrigin = stateOfOrigin
        self.occupation = occupation
        self.knowledgeOfMember = knowledgeOfMember
        self.relationshipWithMember = relationshipWithMember
        self.image = image
        
        self.email = None
        if self.checkEmail(email): self.email = email

class LoanBondDetails:
    _thirdPartySurety = ThirdPartySurety

    def __init__(self, loanBond):
    
        self.loanBond = loanBond
        self.proposedLoan = loanBond.proposedLoan
        self.thirdPartySurety = None
        self.image = None
        
        self.interest = None
    
    @property
    def image(self): return self.__image
    @property
    def interest(self): return self.__interest
    @property
    def loanBond(self): return self.__loanBond
    def proposedLoan(self): return self.__proposedLoan
    
    def setThirdPartySurety(self, **kwargs): 
        self.thirdPartySurety = self._thirdPartySurety(self, **kwargs)












class RegionsManager(ObjectsManager):
    ObjectType = Region
    subTypes = ['Regions']
    MultipleSubsPerMonth = True
    subsName = 'Regions'
    
    def __init__(self, master):
        ObjectsManager.__init__(self, master)
        self.__master = master
        self.addRegion = self.addSub
        
    def __str__(self): return f'{self.master} | {self.name}'
    
    @property
    def name(self): return f'{self.className}({self.master.name})'

    @property
    def firstRegion(self): return self.first
    @property
    def lastRegion(self): return self.last
    
    @property
    def region(self): return self.master
    
    @property
    def date(self): return self.master.date
    
    @property
    def regions(self): return self.subs
    
    def getRegion(self, number=None, name=None, phone=None, email=None, image=None):
        ## provide mechanism to scan pictures.
        self.getSub(dict(number=number, name=name, phone=phone, email=email, image=image))
            
    @classmethod
    def getFromAllRegions(cls, number):
        for region in cls.allRegions():
            if region.number == number: return region
    
    def regionExists(self, **kwargs):
        if self.getRegion(**kwargs): return True
        return False
    
    def createRegion(self, **kwargs): return self.createSub(sup=self.master, **kwargs)
    

 ########## Sorting
  
  # Regions Accounts
   #Date Sorting
    def sortRegionsAccountsByDate(self):
        pass

   #Day Sorting
    def sortRegionsAccountsByDay(self):
        pass
    def sortRegionsAccountsIntoDaysInWeek(self):
        pass
    def sortRegionsAccountsIntoDaysInMonth(self):
        pass
    
   #Week Sorting
    def sortRegionsAccountsByWeek(self):
        pass
    def sortRegionsAccountsIntoWeeksInMonth(self):
        pass
    def sortRegionsAccountsIntoWeeksInYear(self):
        pass
    
   #Month Sorting
    def sortRegionsAccountsByMonth(self, month):
        PRMP_DateTime.checkDateTime(month)
        clients = [client for client in self.clients if client.lastAccount.date.isSameMonth(month)]
        accounts = []
        for client in clients:
            clientAccounts = client.accountsManager.sortAccountsByMonth(month)
            accounts.extend(clientAccounts)
        return accounts
        
    def sortRegionsAccountsIntoMonthsInYear(self):
        pass
    def sortRegionsAccountsIntoMonthsInYears(self):
        pass
    
   #Year Sorting
    def sortRegionsAccountsByYear(self):
        pass
    def sortRegionsAccountsIntoYears(self):
        pass


class PersonsManager(ObjectsManager):
    ObjectType = Person
    subTypes = ['Persons']
    MultipleSubsPerMonth = True

    
    def __init__(self, master, date=None, **kwargs):
        super().__init__(master, date=date)
        self.createPerson(**kwargs)

    @property
    def firstPerson(self): return self.first
    
    @property
    def lastPerson(self): return self.last

    def createPerson(self, **kwargs): return self.createSub(**kwargs)

    @property
    def name(self): return f'{self.className}({self.master.name})'

    @property
    def region(self): return self.master
    
    @property
    def date(self): return self.master.date
    
    @property
    def persons(self): return self.subs








