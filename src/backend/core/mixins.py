from .errors import Errors


class Mixins:
    naira = chr(8358)
    dollar = chr(36)
    euro = chr(163)
    yen = chr(165)
    _moneySign = naira + chr(32)
    
    def __len__(self):
        try: return len(self[:])
        except: return 1
    
    @classmethod
    def setMoneySign(cls, sign): Mixins._moneySign = sign
    
    @classmethod
    def notImp(cls): raise NotImplementedError(f'A subclass of {cls} should call this method.')
    @property
    def className(self): return f'{self.__class__.__name__}'
    
    def __repr__(self): return f'<{self}>'
    
    @property
    def shortName(self): return self._shortName
    @property
    def moneyWithSign(self, hashtag=0): return f'{self._moneySign}{int(self)}'
    
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


class RA_Mixins:
    
    def __init__(self, manager=None, number=None, previous=None, date=None, name=None, nameFromNumber=False):
        from .date_time import DateTime
        if date == None: date = DateTime.now()
        DateTime.checkDateTime(date)
        
        self.__number = number
        
        self.__name = name if not nameFromNumber else f'{self.className} {self.number}'
        self.__date = date
        self.__manager = manager
        self.__previous = previous
        self.__next = None
        
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
        else: raise Errors('A next is already set.')


class RAM_Mixins:
    subClass = RA_Mixins
    
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
                        if w == d: v = sub.date.isSameDay(val)
                        elif w == m: v = sub.date.isSameMonth(val)
                        elif w == y: v = sub.date.isSameYear(val)
                        elif w == t: v = sub.date.isSameDate(val)
                        
                    else: v = getattr(sub, attr) == val
                        
                    count.append(v)

                if count.count(True) == len(count): return sub
    
    def createSub(self, **kwargs):
        last = self.last
        # print(self.className)
        sub = self.subClass(self, previous=last, number=len(self)+1, **kwargs)
        if last: last.next = sub
        
        self.addSub(sub)
        
        return sub





