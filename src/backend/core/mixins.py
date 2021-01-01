from .errors import Errors
import re, io
from prmp_miscs import PRMP_Mixins



class Mixins(PRMP_Mixins):
    
    def addSignToMoney(self, money):
        int(money)
        return self.addSignToNum(money)
    
    numberToMoney = addSignToMoney

    def stripSignFromNum(self, money): return self.stripSignFromNum(money)

    moneyToNumber = stripSignFromMoney
   
    
    def checkMoney(self, money):
        try:
            if self._moneySign in money:
                int(self.stripSignFromMoney(money))
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
                    money = int(data)
                    new = self.addSignToMoney(money)
                    newList.append(new)
                except: newList.append(data)
            newListInList.append(newList)
        return newListInList

    @classmethod
    def setMoneySign(cls, sign): Mixins._moneySign = sign
    
