from .packed import *
from tkinter.colorchooser import askcolor






class ChartOptions(Frame):

    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)
                
      ########## Chart Options
        self.chart_lblfrm = LabelFrame(self, text='Chart Options', place=dict(relx=.005, rely=.005, relh=.99, relw=.99))

       ### Fig number
        self.fig = LabelSpin(self.chart_lblfrm, topKwargs=dict(text='Fig. No.'), bottomKwargs=dict(to=4, from_=1, increment=1), orient='h', place=dict(relx=.003, rely=.003, relh=.18, relw=.35))

       ###### Chart Type
        self.chart_type = None
        self.chart_types = LabelCombo(self.chart_lblfrm,  topKwargs=dict(text='Chart Types'), bottomKwargs=dict(values=['Plot', 'Bar', 'Barh', 'Hist', 'Pie']), func=self.chart_types_choser, orient='h', place=dict(relx=.37, rely=.003, relh=.18, relw=.62), longent=.45)

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

     # Defaults
        self.paint()
        self.chart_types_choser()
        self.grid_decide()

    def grid_decide(self):
        self.grid_style.checked()

        options = [self.grid_style, self.grid_width, self.grid_color]

        if self.grid_style.T.get():
            for option in options[:-1]: option.normal('b')
            options[-1].normal()
        else:
            self._grid_style = 'None'
            self.grid_style.set(self._grid_style)
            self._grid_color = 'black'
            for option in options[:-1]: option.disabled('b')
            options[-1].disabled()

    def grid_color_choser(self):
        rgb_name, self._grid_color = askcolor(self._grid_color)
        self.grid_color.config(background=self._grid_color)

    def grid_style_choser(self, e=0): self._grid_style = self.grid_style.get().lower()

    def chart_types_choser(self, e=0):
        self.chart_type = self.chart_types.get().lower()

        plot_conf = [ self.linestyle, self.marker]
        plot_dis = [self.linewidth, self.alpha]

        if self.chart_type != 'plot':
            for conf in plot_conf: conf.disabled()
            for dis in plot_dis: dis.disabled()
        else:
            for conf in plot_conf: conf.normal()
            for dis in plot_dis: dis.normal()


        if self.chart_type not in ['bar', 'barh']: self.switch.disabled()
        else: self.switch.normal()

        pie_conf = [self.explode, self.shadow, self.inapp]
        if self.chart_type != 'pie':
            for conf in pie_conf: conf.disabled()
        else:
            for conf in pie_conf: conf.normal()

    def alpha_choser(self):
        num = self.alpha.get()
        if num: return float(num)
        else: return 0

    def plot_color_choser(self):
        self.plot_colors = []
        rgb_name, plot_color = askcolor('blue')
        self.plot_colors.append(plot_color)
        self.plot_colors_btn.config(background=plot_color)

    def plot_linewidth_choser(self):
        num = self.linewidth.get()
        if num: return float(num)
        else: return 0

    def inapp_info(self):
        if self.inapp.get(): PRMP_MsgBox(title='Under Testing', message='Using Pie in Inapp will distrupt the other chart drawing', _type='warn', delay=0)

    def chart_sort(self):
        str_region = self.region_cbtn.get()
        datas = self.data_cbtn.get()
        spec_datas = self.spec_cbtn.get() or None
        month = area = day = week = None
        sole = self.sole_cbtn.get()
        go = 0
        if str_region == 'years':
            try:
                region = self.plot_years

                if self.plot_spec_cbtn.get() != '1':
                    if sole == '1':
                        title = 'ALL Years DETAILS'
                        xlabel = 'Records'
                        ylabel = ''
                        go = 1
                    elif datas == 'years':
                        title = 'All Years'
                        xlabel = 'Years'
                        ylabel = 'Records'
                        go = 1
                    elif datas == 'months':
                        title = 'Months in All Years'
                        xlabel = 'Months'
                        ylabel = 'Records'
                        go = 1
                    elif datas == 'areas':
                        title = 'Areas in All Years'
                        xlabel = 'Areas'
                        ylabel = 'Records'
                        go = 1
                    else: PRMP_MsgBox(self, message='Choose Years or Months or Areas', title='Required Datas', _type='error'); go = 0
                else:
                    if spec_datas == 'spec_month':
                        month = self.s_d_month.get()

                        title = f'{month} in ALL Years'
                        xlabel = 'Years'
                        ylabel = 'Records'
                        go = 1
                    elif spec_datas == 'spec_area':
                        area = self.s_d_area.get()

                        title = f'{area} in ALL Years'
                        xlabel = 'Years'
                        ylabel = 'Records'
                        go = 1
            except: PRMP_MsgBox(self, title='Requires Regions', message='Not loaded', _type='error'); go = 0

        elif str_region == 'year':
            try:
                region = self.plot_year
                if self.plot_spec_cbtn.get() != '1':

                    if sole == '1':
                        title = f'{region} DETAILS'
                        xlabel = 'Records'
                        ylabel = ''
                        go = 1
                    elif datas == 'months':
                        title = f'Months in Year {region}'
                        xlabel = 'Months'
                        ylabel = 'Records'
                        go = 1
                    elif datas == 'areas':
                        title = f'Areas in Year {region}'
                        xlabel = 'Areas'
                        ylabel = 'Records'
                        go = 1
                    else: PRMP_MsgBox(self, message='Choose Months or Areas', title='Required Datas', _type='error'); go = 0
                else:
                    if spec_datas == 'spec_area':
                        area = self.s_d_area.get()

                        title = f'{area} in {region}'
                        xlabel = 'Months'
                        ylabel = 'Records'
                        go = 1
            except: PRMP_MsgBox(self, title='Requires Regions', message='Pick a valid Year', _type='error'); go = 0

        elif str_region == 'month':
            try:
                region = self.plot_month

                if sole == '1':
                    title = f'{region} DETAILS'
                    xlabel = 'Records'
                    ylabel = ''
                    go = 1
                elif datas == 'areas':
                    title = f'Areas in {region}'
                    xlabel = 'Areas'
                    ylabel = 'Records'
                    go = 1
                elif datas == 'weeks':
                    title = f'Weeks in {region}'
                    xlabel = 'Weeks'
                    ylabel = 'Records'
                    go = 1
                else: PRMP_MsgBox(self, message='Choose Areas or Weeks', title='Required Datas', _type='error'); go = 0
            except: PRMP_MsgBox(self, title='Requires Regions', message='Pick a valid Month', _type='error'); go = 0

        elif str_region == 'area':
            try:
                region = self.plot_area
                if sole == '1':
                    title = f'{region} DETAILS'
                    xlabel = 'Records'
                    ylabel = ''
                    go = 1
                elif datas == 'weeks':
                    title = f'Weeks in {region}'
                    xlabel = 'Years'
                    ylabel = 'Records'
                    go = 1
                else: PRMP_MsgBox(self, message='Choose Weeks', title='Required Datas', _type='error'); go = 0
            except: PRMP_MsgBox(self, title='Requires Regions', message='Pick a valid Area', _type='error'); go = 0


        else: PRMP_MsgBox(self, message='Choose All Years or Year or Month or Area_or Client', title='Required Regions', _type='error'); go = 0

        if go:
            self.sorted_datas = Chart_Sort(region=region, yaxis=self.get_datas(), sole=sole, month=month, area=area, header=datas)
            self.sorted_datas.xlabel = xlabel
            self.sorted_datas.ylabel = ylabel
            self.sorted_datas.title = title
            self.gather_to_plot()

        elif go == 0: PRMP_MsgBox(self, message='This is not implemented yet Value = Zero', title='Not Implemented', _type='info')

    def clear_plot(self):
        num = self.fig.get()
        if num:
            num = int(num)
            # fig = self.plots_figures[num - 1]
            # fig.clear()
        else: PRMP_MsgBox(self, message='Pick a chart number', title='Required Chart Number', _type='error')









