
from .....backend.utils.sort.bar import Bar
from matplotlib import pyplot
from ..decorate.styles import Styles

class Render:
    bkcol = ""
    def __call__(self): self.show()
    def __init__(self, bkcol="white"):
        self.plt = pyplot
        self.big = 1
        self.figure = self.plt.figure(facecolor=bkcol)
        self.subplot = self.figure.add_subplot(self.big,1,1)
        self.figure.canvas.set_window_title("AKURE GOODNESS AND MERCY") 
        self.annotation = {}

    def plot(self, xticks="", ys="", labels="", grid={}, markers=[], lss=[], lw=0, alpha=0):
        
        self.clear()
        
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
                else:
                    ls = None

                self.subplot.plot(xticks, y, label=label, marker=marker, ls=ls, lw=lw, markersize=markersize, alpha=alpha)

        except Exception as e:
            if markers:
                markers = markers[0]
                markersize = 10
            else:
                markers = None
                markersize = None

            self.subplot.plot(xticks, ys, label=labels, marker=markers, ls=lss, lw=lw, markersize=markersize, alpha=alpha)
        
        self.legend()

        if self.annotation: self.annotate(**self.annotation)
        
        if grid: self.set_grid(grid)
        
        self()

    def bar(self, xticks=[], ys=[], labels=[], which="", grid={}, switch=""):
        
        self.clear()

        bar = Bar(xticks, ys, labels)
        if switch == "1": bar.switch()
        if which == "bar": bar_h = self.subplot.bar
            
        else: bar_h = self.subplot.barh

        if bar.d_1_point != 1:
            for ind in bar.d_ranges:
                x = bar.plot_points[ind]
                y = bar.ys[ind]
                label = bar.labels[ind]
                bar_h(x, y, bar.width, label=label)

        else: bar_h(bar.plot_points, bar.ys, label=bar.labels)
        self.legend()

        if self.annotation: self.annotate(**self.annotation)

        if grid: self.set_grid(grid)
        self()



    def hist(self, *args): pass

    def pie(self, ys=[], labels=[], explode=None, shadow=None, title=""):
        
        self.clear()
        self.annotate(title=title)

        self.plt.pie(ys, labels=labels, explode=explode, autopct="%1.1f%%", shadow=shadow, labeldistance=1.1)
        
        self.show(left=0, bottom=0, right=1, top=.88, wspace=.2, hspace=0)
    

    def annotate(self, xlabel="", ylabel="", title="", xticks=0, yticks=0, set_xticks=0, set_yticks=0, axisrotate=(50, 0), lblrotate=(0, 90)):
        
        
        self.subplot.set_xlabel(xlabel, rotation=lblrotate[0])
        self.subplot.set_ylabel(ylabel, rotation=lblrotate[1])
        self.subplot.set_title(title)
        
        if set_xticks: self.subplot.set_xticks(set_xticks)
        if set_yticks: self.subplot.set_yticks(set_yticks)

        if xticks: self.subplot.set_xticklabels(xticks, rotation=axisrotate[0])
        if yticks: self.subplot.set_yticklabels(yticks, rotation=axisrotate[1])
        
    def legend(self): self.subplot.legend()
    def clear(self): self.subplot.cla()
    def set_grid(self, grid):
        lw, ls, c = grid["lw"], grid["ls"], grid["c"]
        self.plt.grid(lw=lw, ls=ls, c=c)
    def show(self, left=.18, bottom=.25, right=.94, top=.88, wspace=.2, hspace=0):
        self.figure.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
        self.figure.show()

