from .errors import Errors
from .date_time import CompareByDate, DateTime
from .mixins import Mixins
from hashlib import sha224

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


class ObjectsMixins(Mixins, CompareByDate):
    subTypes = ['subs']

    def __init__(self):
        self.__editableValues = []
        self._date = None

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
    
    @property
    def values(self):
        vals = {}
        edit = self.editableValues
        for key in edit:
            if isinstance(key, dict): key = key['value']
            vals[key] = self[key]
        return vals
    
    def __repr__(self): return f'<{self.name}>'
    
    def sumRecords(self, records): return sum(int(rec) for rec in records)
    
    @property
    def withCommas(self): return self.numWithCommas(self.money)

    @property
    def strManager(self): return isinstance(self.manager, str)
    
    def __len__(self):
        try: return len(self[:])
        except: return -1
    
    def get(self, attr, default=None):
        try: return self[attr]
        except: return default
    
    @property
    def moneyWithSign(self): return f'{self._moneySign}{int(self)}'
    
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
    def date(self, _date):
        # assert isinstance(_date, DateTime), f'{_date} an instance of  {_date.__class__}, is not an instance of DateTime'
        if isinstance(_date, str): _date = DateTime.getDMYFromDate(_date)
        self._date = _date

    def __getattr__(self, attr, dontRaise=False):
        ret = self.getFromSelf(attr, self._unget)
        if ret != self._unget: return ret
        elif not dontRaise: self.attrError(attr)
    
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
                        tail_1 = head[tail_prop[0]]
                        tail_2 = tail_1[tail_prop[1]]
                        tail.append(tail_2)
                        count += 1
                else:
                    if head: tail = head[v]
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
    
    def __init__(self, manager=None, number=None, previous=None, date=None, name=None, nameFromNumber=False, sup=None, **kwargs):
        ObjectsMixins.__init__(self)
        from .date_time import DateTime
        if date == None: date = DateTime.now()
        DateTime.checkDateTime(date)

        if not isinstance(manager, str): assert (manager.className == self.Manager) or (manager.className in self.Managers), f'Manager of {self.className} should be {self.Manager} or in {self.Managers} not {manager.className}.'
        
        self._number = number
        self._sup = sup
        
        self._name = name if not nameFromNumber else f'{self.className} {self.number}'
        self._date = date
        self._manager = manager
        self._previous = previous
        self._next = None
        
        self._uniqueID = sha224(self.id.encode()).hexdigest()
    
    @property
    def id(self): return ''.join(self.spacedID.split(' | ')).replace('AGAM', 'A')
    
    @property
    def sup(self): return self._sup
    
    @property
    def spacedID(self):
        'override in subclass'
        return 'id | object'
    
    @property
    def subs(self): return []
    
    @property
    def uniqueID(self): return self._uniqueID
        
    @property
    def name(self): return self._name
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
    
    @property
    def previous(self): return self._previous
    
    @property
    def next(self): return self._next
    
    @next.setter
    def next(self, next_):
        if self._next == None: self._next = next_
        else: raise self.Error('A next is already set.')


class ObjectsManager(ObjectsMixins):
    ObjectType = Object
    MultipleSubsPerMonth = False
    
    def __init__(self, master=None):
        assert master != None, 'Master can not be None.'
        super().__init__()
        self._master = master
        self._subs = []
        self._date = master.date
    
    def __len__(self): return len(self.subs)

    def __getattr__(self, attr):
        ret = self.getFromSelf(attr, self._unget)
        if ret != self._unget: return ret
        else: return getattr(self.last, attr)
    
    @property
    def master(self): return self._master
    
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
    
    def getSub(self, attrs_vals={}):
        if len(self):
            for sub in self:
                count = []
                for attr, val in attrs_vals.items():
                    if val == None: v = True
                    
                    elif 'date' in attr:
                        w = attr.split('-')[1]
                        if w == 'd': v = sub.date.isSameDay(val)
                        elif w == 'm': v = sub.date.isSameMonth(val)
                        elif w == 'y': v = sub.date.isSameYear(val)
                        elif w == 't': v = sub.date.isSameDate(val)
                        
                    else: v = getattr(sub, attr) == val
                        
                    count.append(v)

                if count.count(True) == len(count): return sub
    
    def createSub(self, *args, date=None, **kwargs):
        last = self.last
        exist = self.sortSubsByMonth(date or DateTime.now())
        if len(exist) and not self.MultipleSubsPerMonth: raise self.Error(f'Multiple {self.ObjectType.__name__} can\'t be created within a month.')
        
        sub = self.ObjectType(self, *args, previous=last, number=len(self)+1, date=date, **kwargs)
        if last: last.next = sub
        
        self.addSub(sub)
        
        return sub

    def deleteSubs(self):
        del self._subs
        self._subs = []
    
    
 ########## Sorting

    def sortSubsByDate(self, date):
        if date == None: date = DateTime.now()
        DateTime.checkDateTime(date)

        _rec = [rec for rec in self if str(rec.date) == str(date)]
        return _rec
    
    #Day Sorting
    def sortSubsByDay(self, date):
        recs = [sub for sub in self if sub.date.dayName == date.dayName]
        return recs
    
    def sortSubsIntoDaysInWeek(self, week):
        DateTime.checkDateTime(week)
        days = [sub for sub in self if sub.date.isSameWeek(week)]
        return days
    
    def sortSubsIntoDaysInMonth(self, month):
        DateTime.checkDateTime(month)
        days = [sub for sub in self if sub.date.isSameMonth(month)]
        return days
    
    #Week Sorting
    def sortSubsByWeek(self, date):
        DateTime.checkDateTime(date)
        subs = []
        for sub in self:
            if sub.date.weekNum == int(date.weekNum): subs.append(sub)
        return subs

    def sortSubsIntoWeeksInMonth(self, month):
        daysSub = self.sortSubsIntoDaysInMonth(month)
        weeksSub = daysSub.sortSubsIntoWeeks()
        return weeksSub
    
    def sortSubsIntoWeeksInYear(self): pass
    
    #Month Sorting
    def sortSubsByMonth(self, month): return self.sortSubsIntoDaysInMonth(month)
    
    def sortSubsIntoMonthsInYear(self, year):
        DateTime.checkDateTime(year)
        yearSubs = [sub for sub in self if sub.date.isSameYear(year)]
        return yearSubs
    
    #Year Sorting
    def sortSubsByYear(self, year):
        DateTime.checkDateTime(year)
        recs = [rec for rec in self if rec.date.isSameYear(year)]
        return recs

    def sortSubsIntoYears(self):
        years = self.subsYears
        yearsSubs = [self.sortSubsByYear(DateTime.creatDateTime(year=year)) for year in years]
        return yearsSubs


class ObjectSort:

    __lt = ('lt', '<')
    __le = ('le', '<=')
    __eq = ('eq', '==')
    __ne = ('ne', '!=')
    __gt = ('gt', '>')
    __ge = ('ge', '>=')
    

    def __init__(self, _object):
        self.object = _object
    
    def compare(self, a, b, _type='=='):
        if _type in self.__lt: return a < b
        elif _type in self.__le: return a <= b
        elif _type in self.__eq: return a == b
        elif _type in self.__ne: return a != b
        elif _type in self.__gt: return a > b
        elif _type in self.__ge: return a >= b
    
    def sort(self, attrs=[], _type=None, validations=[]):
        '''
        validations = [
            {'value': DateTime.getDMYFromDate('20/12/2020'), 'method': 'isSameMonth', 'attr': 'date', 'attrMethod': 'isSameMonth', 'methodParams': [], 'attrMethodParams': [], 'valueType': int, 'valueComp': [('lt', '<'), ('le', '<='), ('eq', '=='), ('eq', '!='), ('gt', '>'), ('ge', '>=')]}
        ]
        '''
        objects = []
        if attrs: objects = [self.object[attr] for attr in attrs]
        # print(objects)
        
        if validations:
            validated = []
            for obj in objects:
                valid = True
                val = obj

                for validation in validations:
                    if not valid: break
                    value = validation.get('value')

                    method = validation.get('method')
                    methodParams = validation.get('methodParams')

                    attr = validation.get('attr')
                    attrMethod = validation.get('attrMethod')
                    attrMethodParams = validation.get('attrMethodParams')
                    valueType = validation.get('valueType')
                    valueComp = validation.get('valueComp', 'eq')

                    if method:
                        meth = getattr(self.object, method, None)
                        if not meth:
                            valid = False
                            break
                        if methodParams: val = meth(*methodParams)
                        else: val = meth()
                    elif attr:
                        attr_ = getattr(self.object, attr, None)
                        if not attr_:
                            valid = False
                            break
                        if attrMethod:
                            attrMeth = getattr(attr_, attrMethod, None)
                            if not attrMeth:
                                valid = False
                                break
                            if attrMethodParams: val = attrMeth(*attrMethodParams)
                            else: val = attrMeth()
                        else: val = attr_
                    if val:
                        
                        if valueType: val = valueType(val)
                        if self.compare(val, value, valueComp):
                            valid = True
                            print(56, obj.className)
                
                if valid: validated.append(obj)
            
            objects = validated

        # last one
        
        if _type: objects = [_type(v) for v in objects]

        print(objects)

    def search(self, _type=None, className='ObjectsMixins', value=None, attr='', ):
        pass







