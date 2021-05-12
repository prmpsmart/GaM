# Daily Analysis Book for the Daily Contribution department


from prmp_lib.prmp_miscs.prmp_mixins import PRMP_AdvMixins, PRMP_StrMixins, PRMP_TkMixins
from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime
from prmp_lib.prmp_miscs.prmp_exts import PRMP_File
import threading, os, sqlite3


class Area(PRMP_AdvMixins, PRMP_StrMixins):
    columns = ['current', 'last', 'next', 'upfrontLoan', 'upfrontRepay', 'paidout', 'transfer', 'bto', 'withdraw']

    def __str__(self): return f'{self.className}({self.number}, {self.date.date}, sort="{self.sort}")'

    def __repr__(self): return f'<{self}>'
    
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

    def __init__(self, number, date, sort='date', **datas):
        assert number

        self.subs = []
        self.number = number
        self.sort = sort
        self.date = self.getDate(date)
        assert self.date, f'Date must be provided, not {date}.'
        for key in self.columns:
            val = datas.get(key) or 0
            setattr(self, key, val)
        # self.excess = self.balance if self.balance > 0 else 0

    def get(self, attr, default=None): return self.getFromSelf(attr, default)
    
    @property
    def balance(self): return self.bto + self.paidout - self.total

    @property
    def total(self): return sum([self.current, self.last, self.next])
    
    @property
    def excess(self):
        if self.balance > 0: return self.balance
        return 0
    
    @property
    def deficit(self):
        if self.balance < 0: return abs(self.balance)
        return 0


class Areas:
    join = lambda file: os.path.join(os.path.dirname(__file__), file)
    DAB_FILE1 = join('dab.db1')
    DAB_FILE2 = join('dab.db2')

    areas = []
    sorts = ['date', 'week', 'month', 'year', 'years']
    meths = dict(date='isSameDate', week='isSameWeekMonthYear', month='isSameMonthYear', year='isSameYear')

    @classmethod
    def createArea(cls, number, date, **datas):
        areas = cls.sort(date, 'date')
        if areas:
            for area in areas:
                if area.number  == number and area.date.date == date.date: raise ValueError('An Area with same number and date already exists.')

        area = Area(number, date, **datas)
        cls.areas.append(area)
        return area
    
    @classmethod
    def sort(cls, date, type):
        assert type in cls.sorts[:-1], f'Valid sort types are {cls.sorts[:-1]}.'
        if not cls.areas: return
        
        _areas = []
        date = PRMP_DateTime.getDate(None, date)

        if type == 'date': return [area for area in cls.areas if area.date.date == date.date]

        if type != 'years':
            meth = getattr(date, cls.meths[type])
            for area in cls.areas:
                if meth(area.date): _areas.append(area)
        else: _areas = cls.areas
        
        areas_d = {}
        for area in _areas:
            num = area.number
            if num not in areas_d: areas_d[num] = Area(num, date, type)
            
            area_d = areas_d[num]

            for col in Area.columns:
                old = area_d[col]
                o_new = area[col]
                new = old + o_new
                setattr(area_d, col, new)

        areas = list(areas_d.values())
        return areas
    
    @classmethod
    def sortYears(cls, number, year1, year2):
        areas_d = {}

        for area in cls.areas:
            year = area.date.year
            if year1 <= year <= year2:
                
                if year not in areas_d:
                    year_date = PRMP_DateTime(year, 1, 1)
                    areas_d[year] = Area(area.number, year_date, 'years')
                            
                area_d = areas_d[year]

                for col in Area.columns:
                    old = area_d[col]
                    o_new = area[col]
                    new = old + o_new
                    setattr(area_d, col, new)

        areas = list(areas_d.values())
        return areas

    @classmethod
    def sortAll(cls): return cls.sort(PRMP_DateTime.now(), 'years')

    # database functions
    @classmethod
    def save1(cls):
        'uses the pickle protocol'
        
        def save(obj):
            if not obj: return

            db = PRMP_File()
            db.saveObj(obj)
            db.save(cls.DAB_FILE1)

        threading.Thread(target=save, args=[cls.areas]).start()
    
    @classmethod
    def load1(cls):
        'uses the pickle protocol'
        db = PRMP_File(cls.DAB_FILE1)
        cls.areas = db.loadObj()
    
    @classmethod
    def save2(cls):
        'uses the sqlite3 protocol'
        if not cls.areas: return
        
        try: os.remove(cls.DAB_FILE2)
        except: pass
        connection = sqlite3.connect(cls.DAB_FILE2)
        cursor = connection.cursor()

        # create table
        cursor.execute('CREATE TABLE areas (number INTEGER, date TEXT, current INTEGER, last INTEGER, next INTEGER, upfrontLoan INTEGER, upfrontRepay INTEGER, paidout INTEGER, transfer INTEGER, bto INTEGER, withdraw INTEGER)')

        cols = ['number', dict(date='date'), 'current', 'last', 'next', 'upfrontLoan', 'upfrontRepay', 'paidout', 'transfer', 'bto', 'withdraw']

        areas_cols = tuple([tuple(area[cols]) for area in cls.areas])
        cursor.executemany('INSERT INTO areas VALUES (?,?,?,?,?,?,?,?,?,?,?)', areas_cols)
        connection.commit()
        connection.close()
    
    @classmethod
    def load2(cls):
        'uses the sqlite3 protocol'
        connection = sqlite3.connect(cls.DAB_FILE2)
        cursor = connection.cursor()

        areas = list(cursor.execute('SELECT * FROM areas'))
        
        for area in areas:
            number, date, *data = area
            datas = dict(zip(Area.columns, data))
            area = cls.createArea(number, date, **datas)
    
    @classmethod
    def load3(cls):
        'loads from dab_datas.py, edit the dab.datas.py to update the areas.'
        from dab_datas import dab_datas
        for date, number_d in dab_datas.items():
            for number, datas in number_d.items(): Areas.createArea(number, date, **datas)
        cls.save()
    
    save = save1
    load = load1

if 0:
    Areas.load()
    # Areas.areas = Areas.areas[:-2]
    Areas.save1()
    Areas.save2()
    exit()

Areas.load()
SAVE_DAB_DB = Areas.save


from prmp_lib.prmp_gui import *
from prmp_lib.prmp_gui.scrollables import PRMP_ListBox, Table
from prmp_lib.prmp_gui.two_widgets import TwoWidgets, LabelCombo, LabelEntry, LabelSpin, DateWidget
from prmp_lib.prmp_gui.tushed_widgets import Hierachy
from prmp_lib.prmp_gui.dialogs import PRMP_Dialog, PRMP_MsgBox
from prmp_lib.prmp_gui.plot_canvas import OptPlot, PlotDatas


class DAB_Input(PRMP_FillWidgets, Frame):
    fields = ['date', 'number', *Area.columns]
    
    def __init__(self, master, area=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self, area)
        
        self.area = area

        self.date = DateWidget(self, topKwargs={'text': 'Date'}, place=dict(x=10, y=10, w=180, h=40), orient='h', longent=.4)
        
        self.number = LabelSpin(self, topKwargs={'text': 'Number'}, place=dict(x=10, y=60, w=190, h=40), orient='h', bottomKwargs=dict(_type='number', very=1, from_=1, to=100))

        income = LabelFrame(self, text='Income', place=dict(x=0, y=100, w=255, h=155))
        
        self.last = LabelEntry(income, topKwargs={'text': 'Last'}, place=dict(x=0, y=0, w=210, h=40), orient='h', bottomKwargs=dict(_type='number', very=1), longent=.53)
        self.current = LabelEntry(income, topKwargs={'text': 'Current'}, place=dict(x=0, y=40, w=210, h=40), orient='h', bottomKwargs=dict(_type='number', very=1), longent=.53)
        self.next = LabelEntry(income, topKwargs={'text': 'Next'}, place=dict(x=0, y=80, w=210, h=40), orient='h', bottomKwargs=dict(_type='number', very=1), longent=.53)

        upfront = LabelFrame(self, text='Upfront', place=dict(x=380, y=0, w=215, h=115))
        
        self.upfrontLoan = LabelEntry(upfront, topKwargs={'text': 'Loan'}, place=dict(x=0, y=0, w=210, h=40), orient='h', bottomKwargs=dict(_type='number', very=1), longent=.53)
        self.upfrontRepay = LabelEntry(upfront, topKwargs={'text': 'Repay'}, place=dict(x=0, y=40, w=210, h=40), orient='h', bottomKwargs=dict(_type='number', very=1), longent=.53)

        debit = LabelFrame(self, text='Debit', place=dict(x=280, y=140, w=215, h=115))
        
        self.paidout = LabelEntry(debit, topKwargs={'text': 'Paidout'}, place=dict(x=0, y=0, w=210, h=40), orient='h', bottomKwargs=dict(_type='number', very=1), longent=.53)
        self.withdraw = LabelEntry(debit, topKwargs={'text': 'Withdraw'}, place=dict(x=0, y=40, w=210, h=40), orient='h', bottomKwargs=dict(_type='number', very=1), longent=.53)

        broughtToOffice = LabelFrame(self, text='Brought To Office', place=dict(x=510, y=140, w=215, h=115))
        
        self.transfer = LabelEntry(broughtToOffice, topKwargs={'text': 'Transfer'}, place=dict(x=0, y=0, w=210, h=40), orient='h', bottomKwargs=dict(_type='number', very=1), longent=.53)
        self.bto = LabelEntry(broughtToOffice, topKwargs={'text': 'Bto'}, place=dict(x=0, y=40, w=210, h=40), orient='h', bottomKwargs=dict(_type='number', very=1), longent=.53)

        self.addResultsWidgets(self.fields)
        self.set(area)

    def createArea(self):
        data = self.get()
        if self.validateData(data):
            try:
                area = Areas.createArea(**data)
                SAVE_DAB_DB()
                return area

            except Exception as error: PRMP_MsgBox(self, title=error.__class__.__name__, msg=error, _type='error')
        return False

    def validateData(self, data):
        data = data or self.get()
        if not isinstance(data['date'], PRMP_DateTime):
            PRMP_MsgBox(self, title='Invalid Date', msg='Provided date is of invalid type.', _type='error')
            return False
        if not data['number']:
            PRMP_MsgBox(self, title='Invalid Number', msg='Provide number above zero.', _type='error')
            return False
        data = list({k: v for k, v in data.items() if k not in ['date', 'number']}.values())
        if data.count(None) == len(data):
            PRMP_MsgBox(self, title='Invalid Transaction', msg='Provide atleast a transaction.', _type='error')
            return False
        return True


class DAB_Dialog(PRMP_Dialog):

    def __init__(self, master=None, **kwargs):
        self.tree = master
        super().__init__(master, geo=(740, 400), callback=self.updateArea, _return=1, **kwargs)

    def _setupDialog(self):
        self.addEditButton()
        self.input = DAB_Input(self.cont, place=dict(x=2, y=2, relw=.99, relh=.85), area=self.kwargs.get('area'))

        for field in DAB_Input.fields: setattr(self, field, self.input.getFromSelf(field))

        self.addResultsWidgets(DAB_Input.fields)
    
    def updateArea(self, data):
        area = self.kwargs.get('area')
        if area and data:
            if self.input.validateData(data):
                area.__dict__.update(data)
                SAVE_DAB_DB()
            self.tree.reload()
    
    def action(self):
        self.destroyDialog()
    
    def save(self): SAVE_DAB_DB()


class DAB_Hierachy(Hierachy):

    @property
    def openDialog(self):
        def load(master, obj):
            if obj: DAB_Dialog(master, area=obj)
        return load
    
    def reload(self, event=None):
        if self.last: self.master.viewObjs(self.last[0])


class DAB_Ui(PRMP_MainWindow):

    mixin = PRMP_StrMixins()
    join = lambda file: os.path.join(os.path.dirname(__file__), file)
    T_FILE1 = join('theme.db')

    def sign(num):
        if num:
            res = DAB_Ui.mixin.numWithSign_Commas(num)
            return res
        return ''
    
    columns = [dict(text='Date', attr={'date': 'date'}), dict(text='DC', attr='number', type=int), dict(text='Last', type=sign), dict(text='Current', type=sign), dict(text='Next', type=sign), dict(text='Total', type=sign), dict(text='Upfront Loan', type=sign), dict(text='Upfront Repay', type=sign), dict(text='Excess', type=sign), dict(text='Deficit', type=sign), dict(text='Paidout', type=sign), dict(text='Transfer', type=sign), dict(text='B-T-O', attr='bto', type=sign), dict(text='Withdraw', type=sign)]
    
    columns_lists = ['Last', 'Current', 'Next', 'Total', 'Upfront Loan', 'Upfront Repay', 'Excess', 'Deficit', 'Paidout', 'Transfer', 'Bto', 'Withdraw']
    
    _title_ = 'Daily Analysis Book of %s'
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, geo=(1500, 850), resize=(1, 1), be=1, **kwargs)

        self.table = Table(self.cont, place=dict(x=0, y=0, relw=1, relh=.55), treeKwargs=dict(columns=self.columns), reserve=2, output=DAB_Ui.sign, converter=self.mixin.stripSignFromNum, treeWidget=DAB_Hierachy)

        relh = .6
        self.loaded = 0
        
        note = Notebook(self.cont, place=dict(x=0, rely=relh, relw=.5, relh=1-relh))

        self.input = DAB_Input(note)
        note.add(self.input)
        note.tab(0, text='Input')
        Button(self.input, text='Add', place=dict(x=650, y=20, w=50, h=30), command=self.add)
        self.bind('<Return>', lambda e: self.add())

        self.list = PRMP_ListBox(self.cont, place=dict(relx=.5, rely=relh, relw=.15, relh=1-relh), listboxConfig=dict(values=self.columns_lists, selectmode='multiple'))

        Button(self.list, text='Load', place=dict(relx=.6, rely=.8, relw=.25, relh=.1), command=self.loadPlot)

        sort = Frame(note)
        note.add(sort)
        note.tab(1, text='Sort')

        self.sort_type = LabelCombo(sort, topKwargs={'text': 'Sorts'}, place=dict(x=10, y=10, w=180, h=40), orient='h', longent=.4, bottomKwargs=dict(values=Areas.sorts), func=self.sort)
        self.sort_date = DateWidget(sort, topKwargs={'text': 'Date'}, place=dict(x=10, y=50, w=220, h=40), orient='h', longent=.4)
        
        Button(sort, text='Sort', place=dict(x=250, y=10, w=60, h=30), command=self.sort)
        Button(sort, text='View All', place=dict(x=10, y=200, w=220, h=40), command=lambda: self.updateTable(Areas.areas, 'All Areas.'))

        Button(sort, text='Delete', command=self.deleteArea, place=dict(x=550, y=10, w=60, h=30))

        self._areas = []
        self._title = ''
        self._sort_type = ''
        self.plot = None

        self.after(100, self.loadUI)
        # self.after(200, os.sys.exit)
        self.bind('<<DropDown_value_changed>>', self.date_chosen)

        self.start()
    
    def deleteArea(self): pass
    
    def loadUI(self):
        self.sort_type.set('date')

        date = PRMP_DateTime.now().addTimes(days=-1)
        self.input.date.set(date)
        self.sort_date.set(date)
        
        self._sort(date, 'date')
        
        relh = .6
        self.plot = OptPlot(self.cont, place=dict(relx=.65, rely=relh, relw=.35, relh=1-relh))
        self.plot.paint()

        self.loaded = 1

    def date_chosen(self, event=None):
        if event and (str(event.widget) == str(self.sort_date.B)): self.sort(quiet=1)
        else:
            date = self.input.date.get()
            if date: self._sort(date, 'date')

    def sort(self, event=None, quiet=0):
        date = self.sort_date.get()
        if not date:
            if not quiet: PRMP_MsgBox(self, title='Invalid Date', msg='Choose a valid date.', _type='error')
            
        sort_type = self.sort_type.get()
        if sort_type not in self.sort_type.B.values: PRMP_MsgBox(self, title='Invalid Sort Type', msg='Choose a valid Sort Type.', _type='error')

        self._sort(date, sort_type)

    def _sort(self, date, sort_type):
        if not date: return

        self._sort_type = sort_type
        self._areas = areas = Areas.sort(date, sort_type)

        if sort_type == 'date': text = f'{date.dayName}, {date.day} of {date.monthName} {date.year}.'
        elif sort_type == 'week': text = f'Week {date.week} of {date.monthName} {date.year}.'
        elif sort_type == 'month': text = f'{date.monthName} {date.year}.'
        elif sort_type == 'year': text = f'{date.year}.'
        elif sort_type == 'years': text = 'Years.'
        
        if areas:
            self.updateTable(areas, text)
            self.loadPlot(areas)
        else: self.clear()
    
    def clear(self):
        if self.plot: self.plot.canvas.clear()
        self.table.clear()

    def loadPlot(self, areas=[]):
        if not self.plot: return
        areas = areas or self._areas

        lists = self.list.selected or self.columns_lists
        datas = [area[lists] for area in areas]
        names = [f'Area {int(area.number)}' for area in areas]

        if self.loaded and self.plot and self._sort_type != 'years': self.plot.load(xticks=lists, ys=datas, labels=names, xlabel='Areas', ylabel='Amounts', title=self._title)

    def add(self):
        area = self.input.createArea()
        areas = Areas.sort(area.date, 'date')
        self.updateTable(areas, area.date.date)
    
    def updateTable(self, areas, title):
        if not areas: return

        areas.sort()
        self._areas = areas
        self._title = self._title_ % title
        self.table.updateTable(self._title, areas)

    def _paint(self):
        self.save1()
    
    # database functions
    @classmethod
    def save1(cls):
        'uses the pickle protocol'
        
        def save(obj):
            if not obj: return

            db = PRMP_File()
            db.saveObj(obj)
            db.save(cls.T_FILE1)

        threading.Thread(target=save, args=[PRMP_Theme.currentThemeIndex()]).start()
    
    @classmethod
    def load(cls):
        'uses the pickle protocol'
        db = PRMP_File(cls.T_FILE1)
        themeIndex = db.loadObj()
        return themeIndex

    def save(self):
        SAVE_DAB_DB()
        self.save1()



if __name__ == '__main__':
    themeIndex = DAB_Ui.load()
    DAB_Ui(themeIndex=themeIndex)




