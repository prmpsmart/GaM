from ..decorate.styles import Fonts, Styles
from ..decorate.calculator import Calculator, Path
from tkinter import Label, Button
from ..widgets import ScrolledTreeView
from .....backend.utils.details.tdetails import TDetails
from .....backend.thrift.regions.years import Years
from .....backend.utils.sort.thrift.tabling import Tabling
from .....backend.utils.sort.thrift.regions import Regions
from .....backend.utils.sort.thrift.weeks import Weeks
from .....backend.utils.sort.thrift.days import Days
from .....backend.utils.sort.thrift.column import Column
from .....backend.utils.data.workbook.workbook import Workbook
from ..widgets.debug import show


class Table:
    
    current = {}

    def class_set(self, title=None, header=None, region=None, month=None, area=None, week=None, day=None, spec=None, daily=None):
        self.current = dict(title=title, header=header, region=region, month=month, area=area, week=week, day=day, spec=spec, daily=daily)
        Table.current = self.current.copy()

    def __init__(self, master=None, header='', current=''):
        if current: self.current = current
        else:
            self.master = master
            self._title = Label(self.master, text="Testing")
            
            self.loaded = False
            self.refresh = Button(self.master, text="Refresh", command=self.refresh_)
            self.calc_btn = Button(self._title, text="Calculator", command=Calculator)
            

            self.generate = Button(self.master, text='''Generate Excel File''', command=self.gen_file)
            
            
            self.table = None
            self.headers('AKURE GOODNESS AND MERCY COOP', header)
            
            self.current = Table.current.copy()
            self.refresh_()
            self.style()
        

    def headers(self, title, header):
        self._title.config(text=title)
        columns = Column.get_columns(header)
        if columns:
            del self.table
            self.table = ScrolledTreeView(self.master, columns=columns, show='headings')
            if self.loaded: self.table.place(relx=0, rely=.05, relh=.9, relw=.988)
            
            for column in columns: 
                self.table.heading(column, text=column, anchor="center")
                self.table.column(column, width=70, minwidth="20", stretch="1",  anchor="w")
            if header == 'clients':
                self.table.column('S/N',  width='40', minwidth="20", stretch="1", anchor="w")
                self.table.column('Clients',  width=150, minwidth="5", stretch="1",  anchor="w")
            if header == 'daily':
                self.table.column('S/N',  width='10', minwidth="20", stretch="1", anchor="w")
                self.table.column('Rate',  width='20', minwidth="20", stretch="1", anchor="w")
                self.table.column('Clients',  width=150, minwidth="20", stretch="1",  anchor="w")
            return 1

    def thrift_update(self, title=None, header=None, region=None, month=None, area=None, week=None, day=None, spec=None, refresh=False, daily=None):
        if refresh: self.thrift_update(**self.current)
        else: self.class_set(title=title, header=header, region=region, month=month, area=area, week=week, day=day, spec=spec, daily=daily)
        if region:
            if region.which == 'client' and spec == 'spec_day': header = 'clnt_days'

            if self.headers(title, header):
                if daily: columns = daily.datas
                elif spec:
                    columns = self.spec_update(region=region, week=week, day=day, month=month, spec=spec, area=area)
                else:
                    columns = Tabling.thrift_table(region=region, header=header, week=week, day=day, month=month)
                
                if columns:
                    for column in columns:
                        if column:
                            col = column.copy()
                            if daily: col[1] = col[1].name

                            TDetails.mul_1000s(col)
                            self.table.insert('', 'end', values=col)

    def spec_update(self, region=None, week=None, day=None, month=None, spec=None, area=None):

        if spec == 'spec_month':
            columns = []
            for column in Regions.same_months(month):
                del column[1]
                columns.append(column)
            return columns
        elif spec == 'spec_week':
            columns = []
            for column in Weeks.year_week_columns(region, week): columns.append(column)
            return columns
        elif spec == 'spec_day': return Days.month_day_columns(region=region, day=day)

        elif spec == 'spec_area':
            if region: return Regions.same_areas_year(region, area)
            else: return Regions.same_areas_years(area)

    def refresh_(self): self.thrift_update(refresh=True)

    def style(self): 
        buttons = [self.generate, self.refresh, self.calc_btn]
        for button in buttons: button.config(activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor="white", justify='left', overrelief="groove", relief="solid")

        self._title.config(relief='groove', background=Styles.higbg, foreground=Styles.higfg, font=Fonts.font22)

    def gen_file(self):
        if Path.get_save_dir():
            region = self.current['region']
            daily = self.current['daily']
            Workbook.open_wb(region, daily)
        else: show(title='Not Set', msg='Save Directory is not set', which='error')


    def gen_all(self):
        if Path.get_save_dir(): Workbook.all_workbooks()
        else: show(title='Not Set', msg='Save Directory is not set', which='error')

    def place_widgs(self):
        self._title.place(relx=0, rely=0, relh=.05, relw=.988)
        self.refresh.place(relx=0, rely=.95, relh=.05, relw=.1)
        self.generate.place(relx=.1, rely=.95, relh=.05, relw=.887)
        self.table.place(relx=0, rely=.05, relh=.9, relw=.988)
        
        self.calc_btn.place(relx=0, rely=.05, relh=.9, relw=.15)
        self.loaded = True
        
    @classmethod
    def get_state(cls): return cls.current
    @classmethod
    def load_state(cls, current):
        if isinstance(current, dict): cls.current = current



