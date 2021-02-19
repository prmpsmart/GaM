import sys
sys.path.append(r'C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GaM')
from prmp_miscs.prmp_mixins import PRMP_Mixins
from prmp_miscs.prmp_exts import PRMP_File, os
from prmp_miscs.prmp_datetime import PRMP_DateTime

DEST = r'C:\Users\Administrator\Documents\GaM OFFICE\DC matters\Contributions'

columns = ['number', 'rate', 'amount', 'money']

class Contribution(PRMP_Mixins):

    def __init__(self, number, rate, amount):
        amount = float(amount)
        rate = float(rate)
        self.number = number
        self.rate = rate
        self.subs = None

        if amount > 31: money = 1
        else: money = 0

        if money:
            self.money = amount
            self.amount = amount / rate
        else:
            self.amount = amount
            self.money = rate * amount

    @property
    def _subs(self): return self[columns[:]]

    def __str__(self): return f'{self.className}(Number={self.number}, Rate={self.rate}, Amount={self.amount}, Money={self.money})'


class Contributions(PRMP_Mixins):
    def __init__(self, area, month=None, date=None):
        date = self.getDate(date)
        month = self.getDate(month)

        self.get = self.getFromSelf

        print(self.get)

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
    def money(self): return sum([cont.money for cont in self])

    @property
    def total(self): return len(self)

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

cs = Contributions.load(p)
# cs = Contributions(1, date=PRMP_DateTime.now().addTimes(days=-1))
import random
for a in range(20):
    n = a + 1
    r = random.randrange(100, 1000, 100)
    m = r * random.randint(1, 6)

    cs.add(number=n, rate=r, amount=m)




# exit()

from prmp_gui.dialogs import *
from prmp_gui.two_widgets import *
PTh.setThemeIndex(38)

class App(PRMP_Dialog):

    def __init__(self, contributions=None, **kwargs):
        self.contributions = contributions

        super().__init__(tw=0, **kwargs)

    def _setupDialog(self):
        cont = self.container

        fr1 = Frame(cont, place=dict(relx=0, rely=0, relw=.4, relh=1), relief='groove')

        area1 = LabelFrame(fr1, place=dict(relx=0, rely=0, relw=1, relh=.3), relief='groove', text='Area Details')
        self.areaDatas = ['area', 'month', 'date']

        self.area = LabelEntry(area1, topKwargs=dict(text='Area'), place=dict(relx=0, rely=0, relw=1, relh=.3), orient='h', bottomKwargs=dict(_type='number'))

        self.month = LabelMonthYearButton(area1, topKwargs=dict(text='Month'), place=dict(relx=0, rely=.31, relw=1, relh=.3), orient='h', longent=.35)

        self.date = LabelDateButton(area1, topKwargs=dict(text='Date'), place=dict(relx=0, rely=.62, relw=1, relh=.3), orient='h', longent=.35)

        cont1 = LabelFrame(fr1, place=dict(relx=0, rely=.3, relw=1, relh=.4), relief='groove', text='Contribution Details')
        self.contDatas = ['number', 'rate', 'amount', 'commission']

        self.number = LabelEntry(cont1, topKwargs=dict(text='Number'), place=dict(relx=0, rely=0, relw=1, relh=.24), orient='h', bottomKwargs=dict(_type='number'))

        self.rate = LabelEntry(cont1, topKwargs=dict(text='Rate'), place=dict(relx=0, rely=.25, relw=1, relh=.24), orient='h', bottomKwargs=dict(_type='number'))

        self.amount = LabelEntry(cont1, topKwargs=dict(text='Amount'), place=dict(relx=0, rely=.5, relw=1, relh=.24), orient='h', bottomKwargs=dict(_type='number'))

        self.commission = Checkbutton(cont1, text='Commission', place=dict(relx=0, rely=.75, relw=.4, relh=.2))

        settings = LabelFrame(fr1, place=dict(relx=0, rely=.86, relw=1, relh=.12), text='Settings')
        Button(settings, text='New', place=dict(relx=0, rely=0, relw=.3, relh=.9), command=self.new)
        Button(settings, text='Load', place=dict(relx=.35, rely=0, relw=.3, relh=.9), command=self.save)
        Button(settings, text='Save', place=dict(relx=.7, rely=0, relw=.3, relh=.9), command=self.save)

        Button(cont1, text='Add', place=dict(relx=.77, rely=.77, relw=.2, relh=.17))

        fr2 = Frame(cont, place=dict(relx=.4, rely=0, relw=.6, relh=1), relief='groove')

        self.tree = Hierachy(fr2, place=dict(relx=0, rely=0, relw=1, relh=.8), columns=columns)

        totals = LabelFrame(fr2, text='Totals', place=dict(relx=0, rely=.8, relw=1, relh=.2))
        self.totalsDatas = ['money', 'total']

        self.money = LabelLabel(totals, place=dict(relx=0, rely=0, relw=.5, relh=.4), topKwargs=dict(text='Money'), orient='h')
        self.total = LabelLabel(totals, place=dict(relx=0, rely=.5, relw=.5, relh=.5), topKwargs=dict(text='Contributions'), orient='h', longent=.6)



    def update(self):
        if self.contributions:
            self.set(self.contributions, widgets=[*self.totalsDatas, *self.areaDatas])

            self.tree.viewSubs(self.contributions)







    def defaults(self):
        if not self.titleBar: return

        Button(self.menuBar, text='New', place=dict(relx=0, rely=0, relw=.1, relh=1), command=self.new)
        Button(self.menuBar, text='Load', place=dict(relx=.1, rely=0, relw=.1, relh=1), command=self.save)
        Button(self.menuBar, text='Save', place=dict(relx=.2, rely=0, relw=.1, relh=1), command=self.save)
        self.update()

    def new(self):
        pass
    def load(self):
        pass

    def save(self):
        pass


# wids = [area, month, date]
# wids = [number, rate, amount, commission]

# Widgets = [labelentry, labellabel(for totalmoney, contribs), hierachy]


geo = (700, 600)
App(geo=geo, side='top-center', contributions=cs)


