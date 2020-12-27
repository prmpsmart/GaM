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
        else: print(51, 'd_1_point = 1', file=__file__)


class Plots(Mixins):
    bkcol = 'white'
    def __init__(self, bkcol=''):
        self.big = 1
        self.figure = pyplot.figure(facecolor=bkcol or self.bkcol)
        self.subplot = self.figure.add_subplot(self.big,1,1)
        
        self.pie = None

        self.chart = 'plot'
        self.annotation = {}
        self.chart_datas = {}
    
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
        
        self.legend()

        self.doAnnotation()
        self.set_grid(grid)

        if autoAdjust:
            adjust = {}
            self.adjust()
        
        if adjust: self.adjust(**adjust)

        # if chart != 'pie': self.adjust(**adjust)
        if draw: self.draw()
    
    def adjust(self, left=.2, bottom=.5, right=.94, top=.88, wspace=.2, hspace=0): self.figure.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
    
    def draw(self): self.figure.canvas.draw()

    def legend(self): self.subplot.legend()
    
    def set_grid(self, grid):
        if not grid: return
        lw, ls, c = grid['lw'], grid['ls'], grid['c']
        self.subplot.grid(lw=lw, ls=ls, c=c)

    def clear(self):
        self.subplot.cla()
        self.draw()
        self.chart_datas = []
    
    def plot(self, xticks=[], ys=[], labels=[], grid={}, markers=[], lss=[], lw=0, alpha=0):
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
        
    def bar(self, xticks=[], ys=[], labels=[], grid={}, xlabel='', title='', switch='', ylabel=''):

        barObj = Bar(xticks, ys, labels)
        if switch == '1': barObj.switch()
        if self.chart == 'bar': bar_h = self.subplot.bar
        else: bar_h = self.subplot.barh

        if self.chart == 'bar': self.annotation.update(dict(set_xticks=barObj.ranges, xticks=barObj.xticks))
        else: self.annotation.update(dict(set_yticks=barObj.ranges, yticks=barObj.xticks))

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

        self.pie(ys, labels=labels, explode=explode, autopct='%1.1f%%', shadow=shadow, labeldistance=1.1)
        self.adjust(left=0, bottom=.3, right=1, top=.88, wspace=.2, hspace=0)


class Render(Plots):
    def __init__(self, bkcol='white', annotation={}):
        super().__init__(bkcol)
        self.figure.canvas.set_window_title('Goodness and Mercy')
        self.pie = pyplot.pie
        self.annotation = annotation
    
    def drawIt(self): self.show()

    def draw(self): self.figure.show()


class PlotCanvas(Plots, Frame):
    charts = ['plot', 'bar', 'barh', 'hist', 'pie']
    lss = ['dashed', 'dashdot', 'solid', 'dotted']
    def __init__(self, master=None, relief='solid', **kwargs):
        Frame.__init__(self, master, relief=relief, **kwargs)
        Plots.__init__(self)
        self.expand = False

        self.pie = self.subplot.pie

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

    def doPloting(self, expand=False, adjust={}, **kwargs):
        inApp = kwargs.get('inApp', False)
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

    def bar(self, xlabel='', title='', switch='', ylabel='', annot={}, **kwargs):
        
        if switch == '1': xlabel, ylabel = ylabel, xlabel

        self.annotation = dict(xlabel=xlabel, axisrotate=(50,0), title=title, ylabel=ylabel, **annot)

        self.chart_datas = dict(switch=switch, title=title, **kwargs)
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
        










