from ..debug.debug import Debug
class Bar:
    def __init__(self, xticks, ys, labels):
        self.xticks = xticks
        self.ys = ys
        self.labels = labels
        self._x_axis()
    
    def float_it(self, num):
        re = float("%.2f" % num)
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
        else: Debug.print_bug(51, "d_1_point = 1", file=__file__)

