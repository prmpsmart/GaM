import sys
sys.path.append(r'C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GaM')
from prmp_miscs.prmp_mixins import PRMP_Mixins
from pickle import load

class Contribution(PRMP_Mixins):

    def __init__(self, number, rate, amount):
        amount = float(amount)
        rate = float(rate)
        self.number = number
        self.rate = rate

        if amount > 31: money = 1
        else: money = 0

        if money:
            self.money = amount
            self.amount = amount / rate
        else:
            self.amount = amount
            self.money = rate * amount

    @property
    def _subs(self): return self['number', 'rate', 'amount', 'money']

    def __str__(self): return f'{self.className}(Number={self.number}, Rate={self.rate}, Amount={self.amount}, Money={self.money})'


class Contributions(PRMP_Mixins):
    def __init__(self, area, month=None, date=None):
        date = self.getDate(date)
        month = self.getDate(month)

        self.area, self.month, self.date =  area, month, date
        self.subs = self.contributions = []

    def __str__(self): return f'{self.className}(Area={self.area}, Month={self.month.monthYear}, Date={self.date.date}, Money={self.money})'

    def add(self, number, rate, amount):
        cont = Contribution(number, rate, amount)
        self.contributions.append(cont)
        return cont

    @property
    def total(self): return sum([cont.money for cont in self])
    @property
    def money(self): return self.total


conts = Contributions(1)
c = conts.add(1, 400, 80)
print(conts)
