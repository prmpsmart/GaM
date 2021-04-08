from . import PRMP_Frame
import random
from prmp_lib.prmp_miscs.prmp_mixins import PRMP_ClassMixins


class PlotDatas:
    def __init__(self, xticks=[], ys=[], labels=[], xlabel='', ylabel='', plot=0):
        self.xticks = xticks
        self.ys = ys
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.labels = labels
        self._x_axis(plot)

    def float_it(self, num):
        re = float('%.2f' % num)
        return re

    def _x_axis(self, plot=0):
        try:
            assert len(self.labels) == len(self.ys), f'Length of "labels-> {len(self.labels)}" must be equal to the length of "ys-> {len(self.ys)}"'

            assert len(self.xticks) == len(self.ys[0]), f'Length of "xticks-> {len(self.xticks)}" must be equal to the length of "ys[0]-> {len(self.ys[0])}"'

            self.x_points = len(self.ys[0])
            self.d_1_point = len(self.ys)
            self.width = self.float_it(1. / (self.d_1_point + 1))
            self.space = self.float_it(1. / (self.d_1_point))

        except Exception as e:
            # print(e)
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
            assert len(self.xticks) == len(self.ys[0]), f'Length of "xticks-> {len(self.xticks)}" must be equal to the length of "ys[0]-> {len(self.ys[0])}"'

            for _ in self.ys:
                e_tick_points = [self.float_it(p + point) for p in range(self.x_points)]
                self.plot_points.append(e_tick_points)
                point += self.width
        except: self.plot_points = self.ranges

    def switch(self):
        if self.d_1_point != 1:
            self.xticks, self.labels = self.labels, self.xticks
            self.xlabel, self.ylabel = self.ylabel, self.xlabel


            rly = range(len(self.ys[0]))
            _ys = []

            for yn in rly:
                y = []
                for _y in self.ys:
                    x = _y[yn]
                    y.append(x)
                _ys.append(y)

            self.ys = _ys
            self._x_axis()

            return 1
        else: print('d_1_point=1', __file__)

Bar = PlotDatas

class Plots(PRMP_ClassMixins):
    bkcol = 'white'
    def __init__(self, bkcol=''):
        self.big = 1

        from matplotlib import pyplot
        self.pyplot = pyplot

        self.figure = pyplot.figure(facecolor=bkcol or self.bkcol)
        self.subplot = self.figure.add_subplot(self.big,1,1)

        self._pie = None
        self._grid = None

        self.chart = 'plot'
        self.annotation = {}

    def annotate(self, xlabel='', ylabel='', title='', xticks=0, yticks=0, set_xticks=0, set_yticks=0, axisrotate=(0, 0), lblrotate=(0, 90)):

        if xlabel: self.subplot.set_xlabel(xlabel, rotation=lblrotate[0])
        if ylabel: self.subplot.set_ylabel(ylabel, rotation=lblrotate[1])

        if set_xticks: self.subplot.set_xticks(set_xticks)
        if set_yticks: self.subplot.set_yticks(set_yticks)

        if xticks: self.subplot.set_xticklabels(xticks)
        if xticks: self.subplot.set_xticklabels(xticks, rotation=axisrotate[0])

        if yticks: self.subplot.set_yticklabels(yticks, rotation=axisrotate[1])

        if title: self.subplot.set_title(title)
        if self.chart != 'pie': self.subplot.set_title(title)

    def genAnnot(self, xlabel='', ylabel='', title='', xticks=0, yticks=0, set_xticks=0, set_yticks=0, axisrotate=(0, 0), lblrotate=(0, 90)): return dict(xlabel=xlabel, ylabel=ylabel, title=title, xticks=xticks, yticks=yticks, set_xticks=set_xticks, set_yticks=set_yticks, axisrotate=axisrotate, lblrotate=lblrotate)

    def doAnnotation(self):
        if self.annotation: self.annotate(**self.genAnnot(**self.annotation))

    def doPlotting(self, chart='plot', grid=None, adjust={}, draw=True, autoAdjust=False, **kwargs):
        self.clear()
        self.chart = chart.lower()

        func = self.getFromSelf(self.chart)
        
        if self.chart == 'pie': kwargs = {k: v for k, v in kwargs.items() if k in ['ys', 'labels', 'explode', 'shadow', 'title']}
        func(**kwargs)

        # if kwargs:
        self.doAnnotation()
        self.legend()
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
        # return
        # try: self.subplot.legend()
        # except Exception as e: print(e)

    def set_grid(self, grid):
        if not grid: return
        self._grid = grid
        lw, ls, c = grid['lw'], grid['ls'], grid['c']
        self.subplot.grid(lw=lw, ls=ls, c=c)

    def clear(self):
        self.subplot.cla()
        self.draw()
        self.chart_datas = {}

    def plot(self, xticks=[], ys=[], labels=[], markers=[], lss=[], linestyle=[], lw=0, linewidth=0, alpha=0, switch=0):
        if linestyle: lss = linestyle
        if linewidth: lw = linewidth
        if not lw: lw = 2
        if not alpha:  alpha = 1

        plotDatas = PlotDatas(xticks=xticks, ys=ys, labels=labels, xlabel=self.chart_datas.get('xlabel', ''), ylabel=self.chart_datas.get('ylabel', ''), plot=1)

        if switch: plotDatas.switch()

        self.annotation.update(dict(xticks=plotDatas.xticks, xlabel=plotDatas.xlabel, ylabel=plotDatas.ylabel))

        try:
            indexes = range(len(plotDatas.labels))
            for index in indexes:
                y = plotDatas.ys[index]
                label = plotDatas.labels[index]

                if markers:
                    marker = markers[index]
                    markersize = 10
                else:
                    marker = None
                    markersize = None
                if lss: ls = lss[index]
                else: ls = None

                self.subplot.plot(plotDatas.xticks, y, label=label, marker=marker, ls=ls, lw=lw, markersize=markersize, alpha=alpha)

        except Exception as e:
            # print(e, 'error first')
            if markers:
                markers = markers[0]
                markersize = 10
            else:
                markers = None
                markersize = None

            if lss: lss = lss[0]
            else: lss = None

            try: self.subplot.plot(plotDatas.xticks, plotDatas.ys, label=plotDatas.labels, marker=markers, ls=lss, lw=lw, markersize=markersize, alpha=alpha)
            except Exception as e:
                # print(e)
                pass

    def bar(self, xticks=[], ys=[], labels=[], xlabel='', title='', switch='', ylabel='', axisrotate=(20, 0)):

        barObj = PlotDatas(xticks=xticks, ys=ys, labels=labels, xlabel=xlabel, ylabel=ylabel)
        if switch: barObj.switch()

        self.annotation = dict(xlabel=barObj.xlabel, axisrotate=axisrotate, title=title, ylabel=barObj.ylabel)
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

    def pie(self, ys=[], labels=[], explode=[], shadow=None, title=''):
        self.annotation = dict(title=title)

        if not self.pie: return
        try: ys = [y[0] for y in ys]
        except: pass

        self._pie(ys, labels=labels, explode=explode, autopct='%1.1f%%', shadow=shadow, labeldistance=1.1)
        self.adjust(left=0, bottom=.4, right=1, top=.88, wspace=.2, hspace=0)


class Render(Plots):
    def __init__(self, bkcol='white', annotation={}):
        super().__init__(bkcol)
        self.figure.canvas.set_window_title('Goodness and Mercy')
        self._pie = self.pyplot.pie
        self.annotation = annotation

    def draw(self): self.figure.show()

    def pie(self,  **kwargs):
        super().pie(**kwargs)
        self.adjust(left=0, bottom=.1, right=1, top=.88, wspace=.2, hspace=0)


class PRMP_PlotCanvas(Plots, PRMP_Frame):
    charts = ['plot', 'bar', 'barh', 'hist', 'pie']
    lss = ['dashed', 'dashdot', 'solid', 'dotted']

    def __init__(self, master=None, relief='solid', **kwargs):
        PRMP_Frame.__init__(self, master, relief=relief, **kwargs)
        Plots.__init__(self)

        self.expand = False

        self.chart_datas = {}
        self._pie = self.subplot.pie

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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

    def doPlotting(self, expand=False, inApp=1, adjust={}, **kwargs):
        pie = kwargs.get('pie', False)
        draw = True

        if pie:
            if not adjust: adjust = dict(left=0, bottom=.3, right=1, top=.88, wspace=.2, hspace=0)
            if not inApp: draw = False

        dic = dict(draw=draw, **kwargs)

        if adjust: dic['adjust'] = adjust

        super().doPlotting(**dic)
        if expand: self.show()

    def plot(self, xticks=[], labels=[], xlabel='', ylabel='', title='', marker=None, lss=None, annot={}, axisrotate=(20, 0), **kwargs):

        if marker: markers = self.marker_choser(len(labels))
        else: markers = None

        if lss: lss = self.ls_choser(len(labels))

        self.annotation = dict(xticks=xticks, axisrotate=axisrotate, xlabel=xlabel, title=title, ylabel=ylabel, **annot)

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

    def set_grid(self, grid): super().set_grid(grid)

    def show(self, o=0): Render(bkcol=self.bkcol, annotation=self.annotation).doPlotting(chart=self.chart, grid=self._grid, **self.chart_datas)



