from .errors import Errors
from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime, CompareByDate
from prmp_lib.prmp_miscs.prmp_mixins import *



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

