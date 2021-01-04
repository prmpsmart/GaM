from .errors import Errors
import re, io
from prmp_miscs.prmp_datetime import PRMP_Mixins, PRMP_DateTime, CompareByDate



class Mixins(PRMP_Mixins):

    def getDate(self, date=None):
        if date == None: date = PRMP_DateTime.now()
        PRMP_DateTime.checkDateTime(date)
        return date
    
    def addSignToMoney(self, money):
        float(money)
        return self.addSignToNum(money)
    
    numberToMoney = addSignToMoney

    def stripSignFromMoney(self, money): return self.stripSignFromNum(money)

    moneyToNumber = stripSignFromMoney
   
    
    def checkMoney(self, money):
        try:
            if self._moneySign in money:
                float(self.stripSignFromMoney(money))
                return True
            return False
        except: return False

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
    
