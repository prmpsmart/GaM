from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot
from .core import Frame, Mixins
import random


class Bar:
    def __init__(self, xticks, ys, labels):
        self.xticks = xticks
        self.ys = ys
        self.labels = labels
        self._x_axis()
    
    def float_it(self, num):
        re = float('%.2f' % num)
        return re

    def _x_axis(self):
        try:
            assert len(self.labels) == len(self.ys)
            assert len(self.xticks) == len(self.ys[0])
            
            self.x_points = len(self.ys[0])
            self.d_1_point = len(self.ys)
            self.width = self.float_it(1. / (self.d_1_point + 1))
            self.space = self.float_it(1. / (self.d_1_point))

        except:
            self.x_points = len(self.ys)
            self.d_1_point = 1
            self.width = .6
            self.space = self.width
            
        finally:
            self.ranges = range(self.x_points)
            self.d_ranges = range(self.d_1_point)
            self._plot_points()

    def _plot_points(self):
        point = 0
        self.plot_points = []
        try:
            assert len(self.xticks) == len(self.ys[0])
            for _ in self.ys:
                e_tick_points = [self.float_it(p + point) for p in range(self.x_points)]
                self.plot_points.append(e_tick_points)
                point += self.width
        except: self.plot_points = self.ranges

    def switch(self):
        if self.d_1_point != 1:
            self.xticks, self.labels = self.labels, self.xticks
            self.ys = [[b[self.ys[0].index(bar)] for b in self.ys] for bar in self.ys[0]]
            self._x_axis()
            return 1
        else: print('d_1_point=1', __file__)


class Plots(Mixins):
    bkcol = 'white'
    def __init__(self, bkcol=''):
        self.big = 1
        self.figure = pyplot.figure(facecolor=bkcol or self.bkcol)
        self.subplot = self.figure.add_subplot(self.big,1,1)
        
        self._pie = None

        self.chart = 'plot'
        self.annotation = {}
    
    def annotate(self, xlabel='', ylabel='', title='', xticks=0, yticks=0, set_xticks=0, set_yticks=0, axisrotate=(50, 0), lblrotate=(0, 90)):

        if xlabel: self.subplot.set_xlabel(xlabel, rotation=lblrotate[0])
        if ylabel: self.subplot.set_ylabel(ylabel, rotation=lblrotate[1])
        
        if set_xticks: self.subplot.set_xticks(set_xticks)
        if set_yticks: self.subplot.set_yticks(set_yticks)

        if xticks: self.subplot.set_xticklabels(xticks, rotation=axisrotate[0])
        if yticks: self.subplot.set_yticklabels(yticks, rotation=axisrotate[1])
        
        if title: self.subplot.set_title(title)
        # if self.chart != 'pie': self.subplot.set_title(title)
    
    def genAnnot(self, xlabel='', ylabel='', title='', xticks=0, yticks=0, set_xticks=0, set_yticks=0, axisrotate=(50, 0), lblrotate=(0, 90)): return dict(xlabel=xlabel, ylabel=ylabel, title=title, xticks=xticks, yticks=yticks, set_xticks=set_xticks, set_yticks=set_yticks, axisrotate=axisrotate, lblrotate=lblrotate)
    
    def doAnnotation(self):
        if self.annotation: self.annotate(**self.genAnnot(**self.annotation))
    
    def doPloting(self, chart='plot', grid=None, adjust={}, draw=True, autoAdjust=False, **kwargs):
        self.clear()
        self.chart = chart

        func = self.getFromSelf(chart)
        func(self, **kwargs)
        
        self.doAnnotation()
        # self.legend()
        self.set_grid(grid)

        if autoAdjust:
            adjust = {}
            self.adjust()
        elif adjust: self.adjust(**adjust)

        if draw: self.draw()
    
    def adjust(self, left=.2, bottom=.5, right=.94, top=.88, wspace=.2, hspace=0): self.figure.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
    
    def draw(self): self.figure.canvas.draw()

    def legend(self):
        self.subplot.legend()
        return
        try: self.subplot.legend()
        except Exception as e: print(e)
    
    def set_grid(self, grid):
        if not grid: return
        lw, ls, c = grid['lw'], grid['ls'], grid['c']
        self.subplot.grid(lw=lw, ls=ls, c=c)

    def clear(self):
        self.subplot.cla()
        self.draw()
        self.chart_datas = {}
    
    def plot(self, xticks=[], ys=[], labels=[], markers=[], lss=[], lw=0, alpha=0):
        if not lw: lw = 2
        if not alpha:  alpha = 1

        try:
            assert len(labels) == len(ys)
            assert len(xticks) == len(ys[0])
            indexes = range(len(labels))
            for index in indexes:
                y = ys[index]
                label = labels[index]
                
                if markers:
                    marker = markers[index]
                    markersize = 10
                else:
                    marker = None
                    markersize = None
                if lss: ls = lss[index]
                else: ls = None

                self.subplot.plot(xticks, y, label=label, marker=marker, ls=ls, lw=lw, markersize=markersize, alpha=alpha)

        except Exception as e:

            if markers:
                markers = markers[0]
                markersize = 10
            else:
                markers = None
                markersize = None
            
            if lss: lss = lss[0]
            else: lss = None

        self.subplot.plot(xticks, ys, label=labels, marker=markers, ls=lss, lw=lw, markersize=markersize, alpha=alpha)
        
    def bar(self, xticks=[], ys=[], labels=[], xlabel='', title='', switch='', ylabel=''):

        barObj = Bar(xticks, ys, labels)
        if switch:
            barObj.switch()
            xlabel, ylabel = ylabel, xlabel

        
        self.annotation = dict(xlabel=xlabel, axisrotate=(50,0), title=title, ylabel=ylabel)
        if self.chart == 'bar':
            bar_h = self.subplot.bar
            self.annotation.update(dict(set_xticks=barObj.ranges, xticks=barObj.xticks))
        else:
            bar_h = self.subplot.barh
            self.annotation.update(dict(set_yticks=barObj.ranges, yticks=barObj.xticks))

        if barObj.d_1_point != 1:
            for ind in barObj.d_ranges:
                x = barObj.plot_points[ind]
                y = barObj.ys[ind]
                label = barObj.labels[ind]
                
                bar_h(x, y, barObj.width,  label=label)

        else: bar_h(barObj.plot_points, barObj.ys, label=barObj.labels)
    
    barh = bar
    
    def hist(self, *args): pass

    def pie(self,  ys=[], labels=[], explode=[], shadow=None, title=''):
        self.annotation = dict(title=title)
        
        if not self.pie: return

        self._pie(ys, labels=labels, explode=explode, autopct='%1.1f%%', shadow=shadow, labeldistance=1.1)
        self.adjust(left=0, bottom=.4, right=1, top=.88, wspace=.2, hspace=0)


class Render(Plots):
    def __init__(self, bkcol='white', annotation={}):
        super().__init__(bkcol)
        self.figure.canvas.set_window_title('Goodness and Mercy')
        self._pie = pyplot.pie
        self.annotation = annotation
    
    def draw(self): self.figure.show()

    def pie(self,  **kwargs):
        super().pie(**kwargs)
        self.adjust(left=0, bottom=.1, right=1, top=.88, wspace=.2, hspace=0)


class PlotCanvas(Plots, Frame):
    charts = ['plot', 'bar', 'barh', 'hist', 'pie']
    lss = ['dashed', 'dashdot', 'solid', 'dotted']
    def __init__(self, master=None, relief='solid', **kwargs):
        Frame.__init__(self, master, relief=relief, **kwargs)
        Plots.__init__(self)
        self.expand = False
        
        self.chart_datas = {}
        self._pie = self.subplot.pie

        self.canvas = FigureCanvasTkAgg(self.figure, master=self).get_tk_widget()
        self.canvas.bind('<1>', self.show)
        
        self.canvas.place(relx=-.05, rely=-.03, relh=1.7, relw=1.05)

        self.adjust()

    def ls_choser(self, num=1):
        ls = []
        while len(ls) <= num:
            l = random.choice(self.lss)
            ls.append(l)
        if num == 1: return ls[0]
        else: return ls
    
    def marker_choser(self, num):
        markers = {'point':'.', 'circle':'o', 'triangle_down ':'v', 'triangle_up':'^', 'triangle_left':'<', 'triangle_right':'>', 'octagon':'8', 'square':'s', 'pentagon':'p', 'plus': 'P', 'star' :'*', 'hexagon1':'h', 'hexagon2':'H', 'cancel':'X', 'diamond':'D', 'thin_diamond':'d', 'underscore':'_'}
        markers = list(markers.values())
        markers_give = [] 
        while len(markers_give) <= num:
            mark = random.choice(markers)
            if mark in markers_give: pass
            else: markers_give.append(mark)
        return markers_give

    def doPloting(self, expand=False, inApp=1, adjust={}, **kwargs):
        pie = kwargs.get('pie', False)
        draw = True

        if pie:
            if not adjust: adjust = dict(left=0, bottom=.3, right=1, top=.88, wspace=.2, hspace=0)
            if not inApp: draw = False
        
        dic = dict(draw=draw, **kwargs)

        if adjust: dic['adjust'] = adjust

        super().doPloting(**dic)
        if expand: self.show()

    def plot(self, xticks=[], labels=[], xlabel='', ylabel='', title='', marker=None, lss=None, annot={}, **kwargs):
        
        if marker: markers, markersize = (self.marker_choser(len(labels)), 10)
        else: markers = markersize = None
        
        if lss: lss = self.ls_choser(len(labels))

        self.annotation = dict(xticks=xticks, axisrotate=(50,0), xlabel=xlabel, title=title, ylabel=ylabel, **annot)

        self.chart_datas = dict(xticks=xticks, labels=labels, markers=markers, lss=lss, **kwargs)
        
        super().plot(**self.chart_datas)
    
    def bar(self, **kwargs):
        self.chart_datas = kwargs
        super().bar(**self.chart_datas)

    def pie(self, labels=[], explode=None, **kwargs):
        
        if explode: explode = [.1 for _ in labels]
        else: explode = [0 for _ in labels]

        self.chart_datas = dict(explode=explode, labels=labels, **kwargs)
        super().pie(**self.chart_datas)

    def set_grid(self, grid):
        self.grid = grid
        super().set_grid(grid)

    def show(self, o=0): Render(bkcol=self.bkcol, annotation=self.annotation).doPloting(chart=self.chart, grid=self.grid, **self.chart_datas)


class _ChartSort:
    
    def __init__(self, region, yaxis, month=None, area=None, week=None, day=None, spec=None, sole="", header=None):
        self.go = 0
        self.plot_data_sort(region, yaxis, area=area, sole=sole, month=month, header=header, week=week, day=day)

    def get_labels(self, yaxis):
        labels = []
        ck = self.class_xticks
        if self.records[0] in yaxis: labels.append(ck[0])
        if self.records[1] in yaxis: labels.append(ck[1])
        if self.records[2] in yaxis: labels.append(ck[2])
        if self.records[3] in yaxis: labels.append(ck[3])
        if self.records[4] in yaxis: labels.append(ck[4])
        if self.records[5] in yaxis: labels.append(ck[5])
        if self.records[6] in yaxis: labels.append(ck[6])
        if self.records[7] in yaxis: labels.append(ck[7])
        if self.records[8] in yaxis: labels.append(ck[8])
        if self.records[9] in yaxis: labels.append(ck[9])
        if self.records[10] in yaxis: labels.append(ck[10])
        if self.records[11] in yaxis: labels.append(ck[11])
        if self.records[12] in yaxis: labels.append(ck[12])
        if len(yaxis) == 1: return labels[0]
        else: return labels

    def plot_data_sort(self, region, yaxis, month=None, area=None, week=None, day=None, spec=None, sole="", header=None):
        sub_regions = []
        columns = []
        ## sub_Ys
        clnt = []
        brf = []
        com = []
        sav = []
        deb = []
        not_paid = []
        upf = []
        pupf = []
        rupf = []
        bal = []
        def_ = []
        exc = []
        bto = []
        ## X_ticks
        xticks = []
        ## Labels
        labels = self.get_labels(yaxis)
        ## Real Ys
        ys = []
        ## Getting the sub_regions
        if region.which == "years":
            if month: sub_regions = Regions.same_months_in_years(month)
            elif header == "months":
                columns = Regions.sum_months_in_years()
                for column in columns: del column[1]
            elif header == "areas": columns = Regions.sum_areas_in_years()
            else: sub_regions = region.years

        elif region.which == "year":
            if area:
                sub_regions = Regions.same_areas_in_year(region, area)
            elif header == "areas": columns = Regions.sum_areas_in_year(region)
            else: sub_regions = region.months
        
        elif region.which == "month":
            if header == "areas":
                areas = region.areas
                for area in areas:
                    if day: column = Days.day_column(area, day)
                    
                    elif week: column = Weeks.week_column(area, week)

                    else: column = area.datas()
                    columns.append(column)
                    
            elif header == "weeks": columns = list(Weeks.weekly_sort(region))
            elif header == "days":
                columns = list(Days.daily_sort(region, week=week))
                for column in columns: del column[0]
            elif week:
                column = Weeks.week_column(region, week)
                self.xticks = self.class_xticks
                self.ys = column[1:]
                self.labels = column[0]
                self.go = 1
                return 
            elif day:
                column = Days.day_column(region, day)
                self.xticks = self.class_xticks
                self.ys = column[1:]
                self.labels = column[0]
                self.go = 1
                return 

        elif region.which == "area":
            if header == "areas": sub_regions = region.areas
            elif header == "weeks": columns = Weeks.weekly_sort(region)
            elif header == "days": columns = Days.daily_sort(region, week=week)
        
        ## Sorting the required records for ploting
        if sole == "1":
            num = 1
            self.xticks = self.class_xticks
            if region.which in ["year", "month"]: num = 2
            datas = region.datas()
            self.ys = datas[num:]
            
            self.labels = datas[0]
            self.go = 1
            return

        elif sub_regions:
            for sub_region in sub_regions:
                if month: xticks.append(sub_region.year_name)
                elif area:
                    if sub_region.which == "year": xticks.append(sub_region.name)
                    else: xticks.append(sub_region.month_name)
                else: xticks.append(sub_region.name)
                
                if self.records[0] in yaxis: clnt.append(sub_region.total_clients)
                    
                if self.records[1] in yaxis: brf.append(sub_region.brought_forwards)
                    
                if self.records[2] in yaxis: com.append(sub_region.commissions)
                
                if self.records[3] in yaxis: sav.append(sub_region.savings)
                
                if self.records[4] in yaxis: deb.append(sub_region.debits)
                
                if self.records[5] in yaxis: not_paid.append(sub_region.not_paids)
                
                if self.records[6] in yaxis: upf.append(sub_region.upfronts)
                
                if self.records[7] in yaxis: pupf.append(sub_region.p_upfronts)
                
                if self.records[8] in yaxis: rupf.append(sub_region.r_upfronts)
                
                if self.records[9] in yaxis: bal.append(sub_region.balances)
                
                if self.records[10] in yaxis: def_.append(sub_region.deficits)
                
                if self.records[11] in yaxis: exc.append(sub_region.excesses)
                
                if self.records[12] in yaxis: bto.append(sub_region.btos)

        elif columns:
            for data in columns:
                xticks.append(data[0])
                if self.records[0] in yaxis: clnt.append(data[1])
                
                if self.records[1] in yaxis: brf.append(data[2])
                    
                if self.records[2] in yaxis: com.append(data[3])
                    
                if self.records[3] in yaxis: sav.append(data[4])
                    
                if self.records[4] in yaxis: deb.append(data[5])
                    
                if self.records[5] in yaxis: not_paid.append(data[6])
                
                if self.records[6] in yaxis: upf.append(data[7])
                
                if self.records[7] in yaxis: pupf.append(data[8])
                
                if self.records[8] in yaxis: rupf.append(data[9])
                
                if self.records[9] in yaxis: bal.append(data[10])
                
                if self.records[10] in yaxis: def_.append(data[11])
                
                if self.records[11] in yaxis: exc.append(data[12])
                
                if self.records[12] in yaxis: bto.append(data[13])


        if columns or sub_regions:
            for y in [clnt, brf, com, sav, deb, not_paid, upf, pupf, rupf, bal, def_, exc, bto]:
                if y: ys.append(y)
            
            self.xticks = xticks
            if len(yaxis) == 1: self.ys = ys[0]
            else: self.ys = ys
            
            self.labels = labels
            self.go = 1


class ChartSort:
    
    def __init__(self, _object):
        self.object = _object
    
    def sort(self, labels=[], _type=None, attr='', **kwargs):
        values = []
        # for lbl in labels:


