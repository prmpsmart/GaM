from .errors import Errors
from .date_time import CompareByDate, DateTime
from hashlib import sha224
import re

class Mixins:
    naira = chr(8358)
    dollar = chr(36)
    euro = chr(163)
    yen = chr(165)
    _moneySign = naira + chr(32)
    Error = Errors
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
    def getFromSelf(self, name): return self.__dict__.get(name)
    
    def printError(self, func, error): print(f"Error from {self}->{func}: ", error)
    
    def checkEmail(self, email): return True if re.search(self.email_regex, email) else False

    def testPrint(self, *args):
        print()
        for a in args: print(a, end='=')
        print()
    
    @property
    def withCommas(self): return self.numWithCommas(self.money)

    @classmethod
    def setMoneySign(cls, sign): Mixins._moneySign = sign
    
    @classmethod
    def notImp(cls): raise NotImplementedError(f'A subclass of {cls} should call this method.')
    @property
    def className(self): return f'{self.__class__.__name__}'
    
    def __repr__(self): return f'<{self}>'
    
    @property
    def shortName(self): return self._shortName
    
    
    def containerToDict(self, cont):
        lcont = len(cont)
        assert lcont % 2 == 0, f'Length of container items must be divisible by 2 not {lcont} .'
    
    
    def AlphabetsSwitch(self):
        d = {}
        for n in range(65, 91):
            d[chr(n)] = chr(n+32)
            d[chr(n+32)] = chr(n)
        return d
    
    def propertize(self, name):
        if name:
            name = str(name)
            nm = name.replace(' ', '')
            fin = self.AlphabetsSwitch()[nm[0]] + nm[1:]
            return fin
    


class ObjectsMixins(Mixins, CompareByDate):
    
    
    def __len__(self):
        try: return len(self[:])
        except: return 1
    
    
    @property
    def moneyWithSign(self, hashtag=0): return f'{self._moneySign}{int(self)}'
    
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
    
    
    
    def __bool__(self): return True
    
    def addMoneySign(self, money): return f'{self._moneySign}{money}'
    
    def moneyWithSign_ListInList(self, listInList):
        try: listInList[0][0]
        except: raise AssertionError('Data must be list in another list')
        newListInList = []
        for list1 in listInList:
            newList = []
            for data in list1:
                try:
                    if isinstance(data, Mixins): raise
                    money = int(data)
                    new = self.addMoneySign(money)
                    newList.append(new)
                except: newList.append(data)
            newListInList.append(newList)
        return newListInList
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
    
    
    
    def __getattr__(self, attr): return None
    
    def __setitem__(self, key, value): pass
    
    def __getitem__(self, item):
        
        if isinstance(item, (int, slice)):
            subs = self.subs
            if subs: return subs[item]
            print(item, 'num')
        elif isinstance(item, (list, tuple, set)):
            dicts = self.containerToDict(item)
            print('container')
        if isinstance(item, slice):
            pass
        if isinstance(item, slice):
            pass
        if isinstance(item, slice):
            pass
    

class Object(ObjectsMixins):
    Manager = 'ObjectsManager'
    Managers = ()
    
    def __eq__(self, other):
        if other == None: return False
        return self is other
    
    def __init__(self, manager=None, number=None, previous=None, date=None, name=None, nameFromNumber=False, sup=None, **kwargs):
        from .date_time import DateTime
        if date == None: date = DateTime.now()
        DateTime.checkDateTime(date)
        
        if not isinstance(manager, str): assert (manager.className == self.Manager) or (manager.className in self.Managers), f'Manager of {self.className} should be {self.Manager} or in {self.Managers} not {manager.className}.'
        
        self.__number = number
        self.__sup = sup
        
        self.__name = name if not nameFromNumber else f'{self.className} {self.number}'
        self.__date = date
        self.__manager = manager
        self.__previous = previous
        self.__next = None
        
        self.__uniqueID = sha224(self.id.encode()).hexdigest()
    
    
    @property
    def id(self): return ''.join(self.spacedID.split(' | ')).replace('AGAM', 'A')
    
    @property
    def sup(self): return self.__sup
    
    @property
    def spacedID(self):
        'override in subclass'
        return 'id | object'
    
    @property
    def subs(self): return []
    
    @property
    def uniqueID(self): return self.__uniqueID
        
    @property
    def name(self): return self.__name
    
    @property
    def manager(self): return self.__manager
    
    @property
    def master(self):
        if isinstance(self.manager, str): return self.manager
        return self.manager.master
    
    @property
    def number(self): return self.__number
    
    @property
    def date(self): return self.__date
    
    @property
    def previous(self): return self.__previous
    
    @property
    def next(self): return self.__next
    
    @next.setter
    def next(self, next_):
        if self.__next == None: self.__next = next_
        else: raise self.Error('A next is already set.')



class ObjectsManager(ObjectsMixins):
    ObjectType = Object
    
    def __init__(self, master=None):
        assert master != None, 'Master can not be None.'
        
        self.__master = master
        self.__subs = []
    
    def __getitem__(self, num): return self.subs[num]
    
    def __len__(self): return len(self.subs)
    
    @property
    def master(self): return self.__master
    
    @property
    def subs(self): return self.__subs
    
    @property
    def first(self):
        if len(self):
            self.subs.sort()
            first_ = self[-1]
            assert first_.previous == None, f'{self} is not the first.'
            return first_
        
    @property
    def last(self):
        if len(self):
            self.subs.sort()
            last_ = self[-1]
            assert last_.next == None, f'{self} is not the last.'
            return last_
    
    
    def addSub(self, sub): self.__subs.append(sub)
    
    def getSub(self, attrs_vals={}):
        if len(self):
            for sub in self:
                count = []
                for attr, val in attrs_vals.item():
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
    
    def createSub(self, *args, **kwargs):
        last = self.last
        
        sub = self.ObjectType(self, *args, previous=last, number=len(self)+1, **kwargs)
        if last: last.next = sub
        
        self.addSub(sub)
        
        return sub

    def deleteSubs(self):
        del self.__subs
        self._subs = []



