from ..sort.date import Date


class Record:
    def __init__(self, money, date, freq=1):
        self.__money = money
        self.__freq = freq
        self.dateStr = date
        if Date.verifyDateFormat(date): self.date = Date.getDMYFromDate(date)
    @property
    def money(self): return self.__money
    @property
    def freq(self): return self.__freq
    def add(self, money=0): self.__money += money
    def substract(self, money=0): self.__money -= money

class Records:
    name = "Records"
    
    def __init__(self, obj):
       self.obj = obj
       self.records = []
       
    @property
    def dates(self):
        for record in self.records: yield record.date.dateStr
    
    def getRecordByDate(self, date):
        for record in self.records:
            if record.date == date: return record
    
    def addRecord(self, money, date, freq=1):
        if date in list(self.dates):
            record = self.getRecordByDate(date)
            record.add(money)
        else:
            record = Record(money, date, freq)
            self.records.append(record)
        
    def removeRecord(self, date):
        for record in self.records:
            if record.date == date: self.records.remove(record)
            del record
    
    def removeRecordByDate(self, date):
        if date in list(self.dates): self.removeRecord(date)
    
    def removeRecordByIndex(self, index):
        if len(self.records) >= index: del self.records[index]
    
    @property
    def total_records(self): return len(self.records)
    
    #sorting
    def sortByDayName(self, dayName):
        for record in self.records:
            if record.date.dayName == dayName: yield record
    
    def sortByDayNum(self, dayNum):
        for record in self.records:
            if record.date.dayNum == int(dayNum): yield record
    
    def sortByWeek(self, weekNum):
        for record in self.records:
            if record.date.weekNum == int(weekNum): yield record
    
    def sortByMonth(self, monthName):
        for record in self.records:
            if record.date.monthName == monthName: yield record
    
    def sortByYear(self, year):
        for record in self.records:
            if record.date.yearNum == int(year): yield record

