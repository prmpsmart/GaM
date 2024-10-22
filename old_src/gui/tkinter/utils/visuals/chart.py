
from tkinter import Frame

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from .render import Render, pyplot, Bar

from ..decorate.styles import Styles
import random


class Chart(Frame):
    charts = ["plot", "bar", "barh", "hist", "pie"]


    def __init__(self, master=None, relx=0, rely=0, relh=.5, relw=.5):
        super().__init__(master, relief="solid")
        self.relx, self.rely, self.relh, self.relw = relx, rely, relh, relw
        
        if isinstance(Styles.chart, str): self.bkcol = Styles.chart
        elif Styles.chart == True: self.bkcol = Styles.background
        
        self.figure = pyplot.figure(facecolor=self.bkcol)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self).get_tk_widget()
        self.canvas.config(relief="solid")
        self.canvas.bind("<1>", self.show)
        
        self._chart = self.charts[0]
        
        self.subplot = self.figure.add_subplot(1,1,1)
        
        self.render_chart = ""
        self.render_chart_datas = {}
        self.render_chart_annotation = {}

    def ls_choser(self, num):
        lss = ["dashed", "dashdot", "solid", "dotted"]
        ls = []
        while len(ls) <= num:
            l = random.choice(lss)
            ls.append(l)
        if num == 1: return ls[0]
        else: return ls
    
    def marker_choser(self, num):
        markers = {"point":".", "circle":"o", "triangle_down ":"v", "triangle_up":"^", "triangle_left":"<", "triangle_right":">", "octagon":"8", "square":"s", "pentagon":"p", "plus": "P", "star" :"*", "hexagon1":"h", "hexagon2":"H", "cancel":"X", "diamond":"D", "thin_diamond":"d", "underscore":"_"}
        markers = list(markers.values())
        markers_give = [] 
        while len(markers_give) <= num:
            mark = random.choice(markers)
            if mark in markers_give: pass
            else: markers_give.append(mark)
        return markers_give


    def plot(self, xticks=[], ys=[], labels=[], grid={}, xlabel="", ylabel="", title="", marker=None, lss=None, lw=0, alpha=0, expand=None):
        
        self.clear()
        

        if marker:
            markers = self.marker_choser(len(labels))
            markersize = 10
        else: markers = markersize = None
        
        if lss:
            lss = self.ls_choser(len(labels))
        
        if lw: pass
        else: lw = 2
        if alpha: pass
        else: alpha = 1

        try:
            assert len(labels) == len(ys)
            assert len(xticks) == len(ys[0])
            indexes = range(len(labels))
            for index in indexes:
                
                y = ys[index]
                label = labels[index]
                if markers: marker = markers[index]

                if lss: ls = lss[index]
                else:
                    ls = None
                    
                # print(xticks, ys, end="\n")

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
        
        self.legend()

        self.annotate(xticks=xticks, axisrotate=(50,0), xlabel=xlabel, title=title, ylabel=ylabel)

        if grid: self.set_grid(grid)

        self.render_chart = "plot"
        self.render_chart_datas = {"xticks": xticks, "ys": ys, "labels": labels, "markers": markers, "lss":lss, "lw": lw, "alpha": alpha, "grid": grid}
        
        if expand: self.show(0)
        else: self.draw()


    def bar(self, xticks=[], ys=[], labels=[], which="bar", grid={}, xlabel="", title="", switch="", ylabel="", expand=None):
        
        self.clear()
        
        bar = Bar(xticks, ys, labels)
        if switch == "1":
            bar.switch()
            xlabel, ylabel = ylabel, xlabel
        if which == "bar":
            self.render_chart = which
            bar_h = self.subplot.bar
            self.annotate(set_xticks=bar.ranges, xticks=bar.xticks, xlabel=xlabel, axisrotate=(50,0), title=title, ylabel=ylabel)
        else:
            self.render_chart = "barh"
            bar_h = self.subplot.barh
            self.annotate(set_yticks=bar.ranges, yticks=bar.xticks, xlabel=xlabel, axisrotate=(50,0), title=title, ylabel=ylabel)


        if bar.d_1_point != 1:
            for ind in bar.d_ranges:
                x = bar.plot_points[ind]
                y = bar.ys[ind]
                label = bar.labels[ind]
                
                bar_h(x, y, bar.width,  label=label)

        else:
            bar_h(bar.plot_points, bar.ys, label=bar.labels)
        self.legend()
        
        if grid: self.set_grid(grid)

        self.render_chart_datas = {"xticks": xticks, "ys": ys, "labels": labels, "grid":grid, "which":which, "switch":switch}
        
        if expand: self.show(0)
        else: self.draw()

    def hist(self, *args): pass

    def pie(self, ys=[], labels=[], explode=None, shadow=None, title="", inapp="", expand=None):
        
        self.clear()
        
        if explode: explode = [.1 for _ in labels]
        else: explode = [0 for _ in labels]

        self.render_chart = "pie"
        self.render_chart_datas = {"explode": explode, "ys": ys, "labels": labels, "shadow":shadow, "title":title}
        
        self.annotate(title=title)
        
        if expand: self.show(0)
        else:
            if inapp == "1":
                self.subplot.pie(ys, labels=labels, explode=explode, autopct="%1.1f%%", shadow=shadow, labeldistance=1.1)
                self.draw(left=0, bottom=.3, right=1, top=.88, wspace=.2, hspace=0)
            
            else: self.show(0)


    def annotate(self, xlabel="", ylabel="", title="", xticks=0, yticks=0, set_xticks=0, set_yticks=0, axisrotate=(50, 0), lblrotate=(0, 90)):

        if xlabel: self.subplot.set_xlabel(xlabel, rotation=lblrotate[0])
        if ylabel: self.subplot.set_ylabel(ylabel, rotation=lblrotate[1])
        
        if set_xticks: self.subplot.set_xticks(set_xticks)
        if set_yticks: self.subplot.set_yticks(set_yticks)

        if xticks: self.subplot.set_xticklabels(xticks, rotation=axisrotate[0])
        if yticks: self.subplot.set_yticklabels(yticks, rotation=axisrotate[1])
        
        if self.render_chart != "pie": self.subplot.set_title(title)
        
        ### Annotation for RENDER
        self.render_chart_annotation = {}
        if xlabel: self.render_chart_annotation["xlabel"] = xlabel
        if ylabel: self.render_chart_annotation["ylabel"] = ylabel
        if title: self.render_chart_annotation["title"] = title
        if xticks: self.render_chart_annotation["xticks"] = xticks
        if yticks: self.render_chart_annotation["yticks"] = yticks
        if set_xticks: self.render_chart_annotation["set_xticks"] = set_xticks
        if set_yticks: self.render_chart_annotation["set_yticks"] = set_yticks
        if axisrotate: self.render_chart_annotation["axisrotate"] = axisrotate
        if lblrotate: self.render_chart_annotation["lblrotate"] = lblrotate


    def draw(self, left=.2, bottom=.5, right=.94, top=.88, wspace=.2, hspace=0):
        self.figure.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)
        
        self.figure.canvas.draw()

    def legend(self): self.subplot.legend()
    def clear(self):
        self.subplot.cla()
        self.draw()
        self.render_chart_datas = []
    
    def set_grid(self, grid):
        lw, ls, c = grid["lw"], grid["ls"], grid["c"]
        self.subplot.grid(lw=lw, ls=ls, c=c)
    
    def show(self, o):
        render = Render(bkcol=self.bkcol)
        render.annotation = self.render_chart_annotation
        
        if self.render_chart == "plot": func = render.plot
        elif "bar" in self.render_chart: func = render.bar
        elif self.render_chart == "pie": func = render.pie

        a = self.render_chart_datas

        if a: func(**a)
        else: render()
        
    def place_widgs(self):
        self.place(relx=self.relx, rely=self.rely, relh=self.relh, relw=self.relw)
        self.canvas.place(relx=0, rely=-.03, relh=1.5, relw=1)




