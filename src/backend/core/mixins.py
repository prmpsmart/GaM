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






