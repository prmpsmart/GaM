import sys
sys.path.append(r'C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GaM')
from prmp_miscs.prmp_mixins import PRMP_Mixins
from prmp_miscs.prmp_exts import PRMP_File, os

DEST = r'C:\Users\Administrator\Documents\GaM OFFICE\DC matters\Contributions'

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
    def name(self):
        n = f'Area_{self.area} {self.month.monthYear} {self.date.date}'

        n = n.replace('/', '-')
        return n

    @property
    def path(self):
        p = self.name.split(' ')
        p = '/'.join(p[:-1])
        p = os.path.join(p, self.name).replace('/', '\\')
        dest = os.path.join(DEST, p) + '.cont'
        return dest

    @property
    def total(self): return sum([cont.money for cont in self])
    @property
    def money(self): return self.total

    def save(self):
        path = self.path
        dir_ = os.path.dirname(path)
        try: os.makedirs(dir_)
        except: pass

        file = PRMP_File(filename=path)
        file.saveObj(self)
        file.save(path)

        return file

    @classmethod
    def load(self, file):
        file = PRMP_File(filename=file)
        conts = file.loadObj()
        return conts

# p = r'C:\Users\Administrator\Documents\GaM OFFICE\DC matters\Contributions\Area_3\July-2021\Area_3 July-2021 18-08-2021.cont'

p = r'C:\Users\Administrator\Documents\GaM OFFICE\DC matters\Contributions\Area_1\February-2021\Area_1 February-2021 18-02-2021.cont'

o = Contributions.load(p)

from prmp_gui.dialogs import PRMP_Dialog

class App(PRMP_Dialog):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


wids = [area, month, date]
wids = [number, rate, amount]

Widgets = [labelentry, labellabel(for totalmoney, contribs), hierachy]



App()


