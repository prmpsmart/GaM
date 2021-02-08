from .errors import Errors
from .mixins import Mixins
from prmp_miscs.prmp_datetime import *
from hashlib import sha224
import time

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
    __eq = ('eq', '==')
    __ne = ('ne', '!=')
    __gt = ('gt', '>')
    __ge = ('ge', '>=')
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

    def getCompType(self, _type):
        for c in self.__comparisons:
            ind = self.__comparisons.index(c)
            if _type in c: return c[1]

    def compare(self, a, b, _type='=='):
        comp = self.getCompType(_type)
        if comp:
            equation = f'{a} {comp} {b}'
            # print(equation)
            return eval(equation)
    
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
            equation = f'{a} {r1} {b} {r2} {c}'
            # print(equation)
            return eval(equation)
    
    def getAllObjects(self, object_=None):
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
    
    def getObjects(self, object_=None, subs=[], attrs=[]):
        object_ = object_ or self.object
        
        if subs and object_: raise ValueError('If this ObjectSort instance has an attributed object or an object_ is passed to sort method, subs should not be passed.')

        if attrs and not object_: raise ValueError('This ObjectSort instance has no attributed object.')

        if subs and attrs: raise SyntaxError('Only one of [subs, attrs] is required.')

        objects = subs.copy()
        if object_ and not objects:
            if getattr(object_, 'subRegions', None): objects.extend(object_.subRegions[:])
            objects.extend(object_.subs[:])
        
        if attrs and not subs: objects = [object_[attr] for attr in attrs]

        return objects

    def sort(self, subs=[], attrs=[], _type=None, object_=None, validations=[]):
        '''
        validations = [
            {'value': PRMP_DateTime.getDMYFromDate('20/12/2020'), 'method': 'isSameMonth', 'attr': 'date', 'attrMethod': 'isSameMonth', 'methodParams': [], 'attrMethodParams': [], 'valueType': int, 'comp': __comparisons, 'compType': ['range', 'comp'], 'minValue': 2000, 'range': __ranges, 'className': 'ObjectsMixins', 'mroStr': 'Record'}
        ]
        '''
        objects = self.getObjects(object_=object_, subs=subs, attrs=attrs)
        if not objects: return

        if validations:
            validated = []
            for obj in objects:
                valid = True
                val = obj

                for validation in validations:
                    if not valid: break

                    className = validation.get('className')
                    if className and (obj.className != className):
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
                        if methodParams: val = meth(*methodParams)
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
                            if attrMethodParams: val = attrMeth(*attrMethodParams)
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

    def search(self, _type=None, className='ObjectsMixins', value=None, attr='', searchType='', allSubs=False, object_=None, validations=[], instance=None):
        results = []
        subs = []

        object_ = object_ or self.object

        if not object_: return

        subs = self.getAllObjects(object_)

        if validations: return self.sort(subs=subs, validations=validations, _type=_type, object_=object_)

        if instance: subs = [sub for sub in subs if instance in sub.mroStr]
        # if instance: subs = [sub for sub in subs if isinstance(sub, instance)]

        return subs


class ObjectsMixins(Mixins, CompareByDate):
    subTypes = ['subs']
    
    def __init__(self, date=None, previous=None, idReq=0):
        self.__editableValues = []
        
        self._date = self.getDate(date)
        self.objectSort = ObjectSort(self)
        
        self.previous = previous
        self.next = None
        
        if not idReq: self._uniqueID = sha224(str(self).encode()).hexdigest()
    
    @property
    def uniqueID(self): return self._uniqueID
    
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
        
    
    def update(self,  values={}):
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
    @property
    def day(self): return self.date.day
    @property
    def dayName(self): return self.date.dayName
    @property
    def month(self): return self.date.month
    @property
    def monthName(self): return self.date.monthName
    @property
    def year(self): return self.date.year
    @property
    def monthYearTuple(self): return self.date.monthYearTuple
    @property
    def weekMonthYearTuple(self): return self.date.weekMonthYearTuple
    
    @property
    def monthYear(self): return self.date.monthYear
    
    @property
    def weekMonthYear(self): return self.date.weekMonthYear
   
    @property
    def week(self): return self.date.week
    
    @property
    def date(self): return self._date

    @date.setter
    def date(self, _date): self._date = self.getDate(_date)

    # def __getattr__(self, attr, dontRaise=False):
    #     ret = self.getFromSelf(attr, self._unget)
    #     if ret != self._unget: return ret
    #     elif not dontRaise: self.attrError(attr)
    
    # def __setattr__(self, attr, value): return None
    
    # def __setitem__(self, key, value):
    #     var = self.getFromSelf(self.propertize(key))
    #     var = value
    
    def __getitem__(self, item):
        if isinstance(item, self.containers):
            res = []
            for it in item: res.append(self[it])
            return res

        elif isinstance(item, str): return self.getFromSelf(self.propertize(item))

        elif isinstance(item, dict):
            res = []
            for k, v in item.items():
                head = self[k]
                if isinstance(v, dict):
                    tail = []
                    tail_props = [(g, h) for g, h in v.items()]
                    last = tail_props[-1]
                    count = 0
                    length_of_tail_props = len(tail_props)
                    while count < length_of_tail_props:
                        tail_prop = tail_props[count]
                        try: tail_1 = head[tail_prop[0]]
                        except: tail_1  = getattr(head, tail_prop[0])
                        
                        try: tail_2 = tail_1[tail_prop[1]]
                        except: tail_2  = getattr(tail_1, tail_prop[1])

                        tail.append(tail_2)
                        count += 1
                else:
                    if head:
                        try: tail = head[v]
                        except: tail = getattr(head, v)
                    else: self.attrError(k)
                res.append(tail)
            return res if len(res) > 1 else res[0]

        return self.subs[item]


class Object(CompareByNumber, ObjectsMixins):
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
    
    @subs.setter
    def subs(self, subs): self._subs = subs

    @property
    def first(self):
        if len(self):
            self.subs.sort()
            first_ = self[0]
            assert first_.previous == None, f'{self} is not the first.'
            return first_
        
    @property
    def last(self):
        if len(self):
            self.subs.sort()
            last_ = self[-1]
            assert last_.next == None, f'{self} is not the last.'
            return last_
    
    def addSub(self, sub): self._subs.append(sub)
    
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
















