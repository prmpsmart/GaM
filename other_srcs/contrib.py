import sys
sys.path.append(r'C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GaM')


from prmp_lib.prmp_miscs.prmp_mixins import PRMP_Mixins
from prmp_lib.prmp_miscs.prmp_exts import PRMP_File, os
from prmp_miscs.prmp_datetime import PRMP_DateTime

from prmp_lib.prmp_gui.dialogs import *
from prmp_gui.two_widgets import *
PTh.setThemeIndex(30)




DEST = r'C:\Users\Administrator\Documents\GaM OFFICE\DC matters\Contributions'

columns = ['number', 'rate', 'amount', 'money']


class Contribution(PRMP_Mixins):

    def __init__(self, number, rate, amount):
        amount = float(amount)
        rate = float(rate)
        number = int(number)
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
    def __repr__(self): return f'<{self.number}>'

    def __lt__(self, other):
        if other == None: return False
        return self.number < other.number
    def __le__(self, other):
        if other == None: return False
        return self.number <= other.number
    def __eq__(self, other):
        if other == None: return False
        return self.number is other.number
    def __ne__(self, other):
        if other == None: return True
        return self.number != other.number
    def __gt__(self, other):
        if other == None: return True
        return self.number > other.number
    def __ge__(self, other):
        if other == None: return True
        return self.number >= other.number

class Contributions(PRMP_Mixins):
    def __init__(self, area, month=None, date=None,commission=False):
        date = self.getDate(date)
        month = self.getDate(month)

        self.get = self.getFromSelf

        self.area, self.month, self.date, self.commission =  int(area), month, date, commission
        self.subs = self.contributions = []

    def __str__(self): return f'{self.className}(Area={self.area}, Month={self.month.monthYear}, Date={self.date.date}, Money={self.money})'

    def add(self, number, rate, amount=0):
        numbers = [cont.number for cont in self]
        if self.commission: amount = 1

        if number in numbers: raise ValueError(f'This number {number} already exists.')

        cont = Contribution(number, rate, amount)
        self.contributions.append(cont)
        self.contributions.sort()

        return cont

    def remove(self, cont):
        if cont in self: self.subs.remove(cont)

    @property
    def _name(self):
        n = f'Area_{self.area} {self.month.monthYear} {self.date.date}'

        n = n.replace('/', '-')
        return n

    @property
    def name(self):
        n = f'{self._name} {"Commission" if self.commission else ""}'

        return n

    @property
    def path(self):
        p = self._name.split(' ')
        p = '/'.join(p[:-1])
        p = os.path.join(p, self._name).replace('/', '\\')
        dest = os.path.join(DEST, p) + f' {"Commission" if self.commission else ""}.cont'
        return dest

    @property
    def money(self): return sum([cont.money for cont in self])

    @property
    def total(self): return len(self)

    def save(self, path=''):
        if not path:
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

class App(PRMP_Dialog):

    def __init__(self, contributions=None, geo=(900, 600), **kwargs):
        self.contributions = contributions

        super().__init__(tw=0, geo=geo, **kwargs)

    def _setupDialog(self):
        cont = self.container

        fr1 = Frame(cont, place=dict(relx=0, rely=0, relw=.4, relh=1), relief='groove')

        area1 = LabelFrame(fr1, place=dict(relx=0, rely=0, relw=1, relh=.4), relief='groove', text='Area Details')
        self.areaDatas = ['area', 'month', 'date', 'commission']

        self.area = LabelEntry(area1, topKwargs=dict(text='Area'), place=dict(relx=0, rely=0, relw=1, relh=.24), orient='h', bottomKwargs=dict(_type='number'))

        self.month = LabelMonthYearButton(area1, topKwargs=dict(text='Month'), place=dict(relx=0, rely=.25, relw=1, relh=.24), orient='h', longent=.35)

        self.date = LabelDateButton(area1, topKwargs=dict(text='Date'), place=dict(relx=0, rely=.5, relw=1, relh=.24), orient='h', longent=.35)

        self.commission = Checkbutton(area1, text='Commission', place=dict(relx=0, rely=.79, relw=.4, relh=.15))


        Button(area1, text='Create', place=dict(relx=.5, rely=.79, relw=.4, relh=.15), command=lambda: PRMP_MsgBox(self, title='Create a Contribution?', message='Are you sure to create contribution?', ask=1, callback=self.create, _type='question'))



        cont1 = LabelFrame(fr1, place=dict(relx=0, rely=.45, relw=1, relh=.4), relief='groove', text='Contribution Details')
        self.contDatas = ['number', 'rate', 'amount']

        self.number = LabelEntry(cont1, topKwargs=dict(text='Number'), place=dict(relx=0, rely=0, relw=1, relh=.24), orient='h', bottomKwargs=dict(_type='number'))

        self.rate = LabelEntry(cont1, topKwargs=dict(text='Rate'), place=dict(relx=0, rely=.25, relw=1, relh=.24), orient='h', bottomKwargs=dict(_type='number'))

        self.amount = LabelEntry(cont1, topKwargs=dict(text='Amount'), place=dict(relx=0, rely=.5, relw=1, relh=.24), orient='h', bottomKwargs=dict(_type='number'))

        Button(cont1, text='Add', place=dict(relx=.77, rely=.77, relw=.2, relh=.17), command=self.add)


        settings = LabelFrame(fr1, place=dict(relx=0, rely=.86, relw=1, relh=.12), text='Settings')
        Button(settings, text='Clear', place=dict(relx=0, rely=0, relw=.24, relh=.9), command=self.clearIt)
        Button(settings, text='Load', place=dict(relx=.25, rely=0, relw=.24, relh=.9), command=self.load)
        Button(settings, text='Save', place=dict(relx=.5, rely=0, relw=.24, relh=.9), command=lambda: PRMP_MsgBox(self, title='Save?', message=f'Are you sure to save to {self.contributions.path if self.contributions else ""}', callback=self.save_, geo=(400, 300)))

        Button(settings, text='Update', place=dict(relx=.75, rely=0, relw=.24, relh=.9), command=self.updateCont)

        fr2 = Frame(cont, place=dict(relx=.4, rely=0, relw=.6, relh=1), relief='groove')

        self.tree = Hierachy(fr2, place=dict(relx=0, rely=0, relw=1, relh=.8), columns=columns)
        self.tree.tree.bind('<Delete>', self.delete)

        totals = LabelFrame(fr2, text='Totals', place=dict(relx=0, rely=.8, relw=1, relh=.2))
        self.totalsDatas = ['money', 'total']

        self.money = LabelLabel(totals, place=dict(relx=0, rely=0, relw=.5, relh=.4), topKwargs=dict(text='Money'), orient='h')
        self.total = LabelLabel(totals, place=dict(relx=0, rely=.5, relw=.5, relh=.5), topKwargs=dict(text='Contributions'), orient='h', longent=.6)

    def update(self):
        self.clear()
        if self.contributions:
            self.setTitle(self.contributions.name)
            self.set(self.contributions, widgets=[*self.totalsDatas, *self.areaDatas])

            self.tree.viewSubs(self.contributions)

    def clear(self, w=1):
        if not w: return
        self.setTitle('Contribution App')

        self.tree.clear()
        self.emptyWidgets([*self.areaDatas, *self.contDatas])

        for wid in [*self.areaDatas, *self.totalsDatas]: self[wid].set('')

    def clearIt(self):
        PRMP_MsgBox(self, title='Clear?', message='Are you sure to clear this current contribution?', ask=1, callback=self.clear, _type='question')


    def defaults(self):

        self.bind('<Control-L>', self.load)
        self.bind('<Control-l>', self.load)
        self.bind('<Control-O>', self.load)
        self.bind('<Control-o>', self.load)
        self.bind('<Control-S>', self.save_)
        self.bind('<Control-s>', self.save_)
        self.bind('<Control-N>', self.create)
        self.bind('<Control-n>', self.create)
        self.bind('<Control-u>', self.updateCont)
        self.bind('<Control-U>', self.updateCont)

        self.update()


    def add(self, e=0):
        if not self.contributions: return

        datas = self.get(self.contDatas)

        try:
            self.contributions.add(**datas)
            self.emptyWidgets(self.contDatas)
        except Exception as e: PRMP_MsgBox(self, title=e.__class__.__name__, message=e, _type='error')

        self.update()

    def delete(self, e=0):
        if not self.contributions: return
        sel = self.tree.selected()
        self.contributions.remove(sel)
        self.update()

    def getAreaData(self):
        contData = self.get(self.areaDatas)
        contData['area'] = int(contData['area'])
        return contData

    def updateCont(self, e=0):
        if not self.contributions: return

        contData = self.getAreaData()
        self.contributions.__dict__.update(contData)
        self.update()

    def create(self, w=0):
        if not w: return
        if self.contributions:
            PRMP_MsgBox(self, title='A Contribution in progress!', message='Are you sure to clear contribution to start a new?', ask=1, callback=self.clear, _type='question')
            return

        contData = self.getAreaData()
        self.contributions = Contributions(**contData)
        self.update()


    def load(self, e=0):
        file = dialogFunc(path=1, filetypes=['Contributions {.cont}'])
        if not file: return

        conts = Contributions.load(file)
        self.contributions = conts
        self.update()

    def save_(self, e=0):
        if not self.contributions: return
        self.updateCont()

        path = self.contributions.path
        if os.path.exists(path): PRMP_MsgBox(self, title='Already Exists', message=f'The path {path} for this contribution already exists, do you wish to overwrite?', ask=1, callback=self._save, geo=(400, 300), _type='error')
        else: self._save(e)

    def _save(self, w=0):
        if w: self.contributions.save()




# rates = [200, 200, 1000, 200, 200, 50, 200, 200, 300, 500, 200, 1000, 200, 100, 1000, 500, 1000, 100, 400, 1000, 500, 200, 200, 200, 400, 50, 200, 500, 300, 500, 500, 200, 200, 200, 200, 200, 200, 500, 100, 300, 1000, 500, 200, 200, 100, 300, 200, 400, 200, 200, 200, 200, 100, 200, 200, 300, 100, 100, 200, 300, 50, 200, 200, 500, 200, 100, 200, 200, 200, 100, 200, 500, 1000, 200, 300, 100, 600, 200, 100, 200, 500, 500, 500, 500, 200, 200, 50, 100, 300, 200, 200, 300, 200, 100, 200, 250, 2000, 300, 200, 100]

# cs = Contributions(2, )
# rts = len(rates)
# for number in range(rts):
#     rate = rates[number]
#     number += 1
#     cs.add(number, rate, 1)

# print(len(rates), sum(rates))
cs = None
App(contributions=cs)














# App(geo=(700, 600), side='top-center', contributions=cs)


