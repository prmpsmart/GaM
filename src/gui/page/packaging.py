from .packed import *
from tkinter.colorchooser import askcolor






class PlotDialog(Frame, Thrift_Analysis):

    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)
                
      ########## Chart Options
        self.chart_lblfrm = LabelFrame(self, text='Chart Options', place=dict(relx=.005, rely=.005, relh=.99, relw=.99))

       ### Fig number
        self.fig = LabelSpin(self.chart_lblfrm, topKwargs=dict(text='Fig. No.'), bottomKwargs=dict(to=4, from_=1, increment=1), orient='h', place=dict(relx=.003, rely=.003, relh=.18, relw=.4))

       ###### Chart Type
        self.chart_type = None
        self.chart_types = LabelCombo(self.chart_lblfrm,  topKwargs=dict(text='Chart Types'), bottomKwargs=dict(values=['Plot', 'Bar', 'Barh', 'Hist', 'Pie']), func=self.chart_types_choser, orient='h', place=dict(relx=.403, rely=.003, relh=.18, relw=.58))

       ########## Chart Types Options
        note = Notebook(self.chart_lblfrm, place=dict(relx=.003, rely=.2, relh=.8, relw=.99))

        self.grid_options = LabelFrame(self.chart_lblfrm, takefocus='')
        note.add(self.grid_options, padding=1)
        note.tab(0, text='Grid Options',compound='left',underline='0')

        self.plot_options = LabelFrame(self.chart_lblfrm, takefocus='')
        note.add(self.plot_options, padding=1)
        note.tab(1, text='Plot Options',compound='left',underline='0')

        self.bar_options = LabelFrame(self.chart_lblfrm, takefocus='')
        note.add(self.bar_options, padding=1)
        note.tab(2, text='Bar Options',compound='left',underline='0')

        self.pie_options = LabelFrame(self.chart_lblfrm, takefocus='')
        note.add(self.pie_options, padding=1)
        note.tab(3, text='Pie Options',compound='left',underline='0')

       ########## Grid lines
        self._grid_style = 'None'
        self._grid_color = PRMP_Theme.DEFAULT_BACKGROUND_COLOR

        self.grid_style = CheckCombo(self.grid_options, topKwargs=dict(text='Grid Style'), func=self.grid_style_choser, command=self.grid_decide, bottomKwargs=dict(values=['None', 'Solid', 'Dashed', 'Dashdot', 'Dotted']), orient='h', place=dict(relx=.02, rely=.02, relh=.25, relw=.65), longent=.4)

        self.grid_width = LabelSpin(self.grid_options, topKwargs=dict(text='Grid Width'), bottomKwargs=dict(from_=.1, to=1, increment=.1), orient='h', place=dict(relx=.02, rely=.3, relh=.25, relw=.65))

        self.grid_color = Button(self.grid_options, text='Color', command=self.grid_color_choser, place=dict(relx=.02, rely=.7, relh=.2, relw=.65,))

       ### Plot options

        self.marker = Checkbutton(self.plot_options, text='Marker', place=dict(relx=.02, rely=.04, relh=.24, relw=.4))

        self.linestyle = Checkbutton(self.plot_options, text='Line Style', place=dict(relx=.02, rely=.28, relh=.24, relw=.4))

        self.linewidth = LabelSpin(self.plot_options,  topKwargs=dict(text='Line Width'), bottomKwargs=dict(to=1, from_=.1, increment=.1), orient='h', place=dict(relx=.02, rely=.52, relh=.24, relw=.64))


        self.alpha = LabelSpin(self.plot_options,  topKwargs=dict(text='Alpha'), bottomKwargs=dict(to=1, from_=.1, increment=.1), orient='h', place=dict(relx=.02, rely=.76, relh=.24, relw=.64))

       ## Bar Options

        self.switch = Checkbutton(self.bar_options, text='Switch', place=dict(relx=.02, rely=.14, relh=.25, relw=.3))

       ###### Pie Options

        self.inapp = Checkbutton(self.pie_options, text='Inapp', command=self.inapp_info, place=dict(relx=.02, rely=.04, relh=.24, relw=.32))

        self.explode = Checkbutton(self.pie_options, text='Explode', place=dict(relx=.02, rely=.28, relh=.24, relw=.32))

        self.shadow = Checkbutton(self.pie_options,text='Shadow', place=dict(relx=.02, rely=.52, relh=.24, relw=.32))

      ############ Plot and Clear

        self.plot_btn = Button(self.chart_lblfrm, command=self.chart_sort, text='Plot', place=dict(relx=.72, rely=.45, relh=.2, relw=.2))

        self.clear_btn = Button(self.chart_lblfrm, command=self.clear_plot, text='Clear', place=dict(relx=.72, rely=.7, relh=.2, relw=.2))

    def grid_decide(self):
        self.grid_style.checked()

        options = [(self.grid_style, 'b'), (self.grid_width, ''), self.grid_color]

        if self.grid_style.T.get():
            for option, val in options[:-1]: option.normal(val)
            options[-1].normal()
        else:
            self._grid_style = 'None'
            self.grid_style.set(self._grid_style)
            self._grid_color = 'black'
            for option, val in options[:-1]: option.disabled(val)
            options[-1].disabled()

    def grid_color_choser(self):
        rgb_name, self.grid_color = askcolor(self.grid_color)
        self.grid_color.config(background=self.grid_color)

    def grid_style_choser(self, e): self._grid_style = self.grid_style.get().lower()

    def chart_types_choser(self, e):
        self.chart_type = self.chart_types.get().lower()

        plot_conf = [ self.linestyle, self.marker]
        plot_dis = [self.linewidth, self.alpha]

        if self.chart_type != 'plot':
            for conf in plot_conf: conf.disable()
            for dis in plot_dis: dis.disabled()
        else:
            for conf in plot_conf: conf.normal()
            for dis in plot_dis: dis.normal()


        if self.chart_type not in ['bar', 'barh']: self.switch.disable()
        else: self.switch.normal()

        pie_conf = [self.explode, self.shadow, self.inapp]
        if self.chart_type != 'pie':
            for conf in pie_conf: conf.disable()
        else:
            for conf in pie_conf: conf.normal()

    def alpha_choser(self):
        num = self.alpha.get()
        if num: return float(num)
        else: return 0
        
    def plot_color_choser(self):
        self.plot_colors = []
        rgb_name, plot_color = colorchooser.askcolor('blue')
        self.plot_colors.append(plot_color)
        self.plot_colors_btn.config(background=plot_color)

    def plot_linewidth_choser(self):
        num = self.linewidth.get()
        if num: return float(num)
        else: return 0

    def inapp_info(self):
        if self.inapp.get(): PRMP_MsgBox(title='Under Testing', message='Using Pie in Inapp will distrupt the other chart drawing', _type='warn', delay=0)











