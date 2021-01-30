from .packed import *






class PlotDialog(Frame):

    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)

        
      ########## Chart Options
        self.chart_lblfrm = LabelFrame(self.details_lblfrm, text='Chart Options')

       ### Fig number
        self.fig_lblsb = LabelSpin(self.chart_lblfrm, text='Fig. No.', relx=.003, rely=.003, relh=.18, relw=.4, to=4, from_=1, increment=1, orient='h')

       ###### Chart Type
        self.chart_type = None
        self.chart_types = LabelCombo(self.chart_lblfrm,  text='Chart Types', relx=.403, rely=.003, relh=.18, relw=.58, values=['Plot', 'Bar', 'Barh', 'Hist', 'Pie'], func=self.chart_types_choser, orient='h')

       ########## Chart Types Options
        self.ch_ty_op_nb = Notebook(self.chart_lblfrm)

        self.grid_options = LabelFrame(self.chart_lblfrm, takefocus='')
        self.ch_ty_op_nb.add(self.grid_options, padding=1)
        self.ch_ty_op_nb.tab(0, text='Grid Options',compound='left',underline='0')

        self.plot_options = LabelFrame(self.chart_lblfrm, takefocus='')
        self.ch_ty_op_nb.add(self.plot_options, padding=1)
        self.ch_ty_op_nb.tab(1, text='Plot Options',compound='left',underline='0')

        self.bar_options = LabelFrame(self.chart_lblfrm, takefocus='')
        self.ch_ty_op_nb.add(self.bar_options, padding=1)
        self.ch_ty_op_nb.tab(2, text='Bar Options',compound='left',underline='0')

        self.pie_options = LabelFrame(self.chart_lblfrm, takefocus='')
        self.ch_ty_op_nb.add(self.pie_options, padding=1)
        self.ch_ty_op_nb.tab(3, text='Pie Options',compound='left',underline='0')

       ########## Grid lines
        self.grid_style = 'None'
        self.grid_color = Styles.background

        self.grid_style_lblcb = CheckCombo(self.grid_options, text='Grid Style', variable=self.grid_cbtn, func=self.grid_style_choser, command=self.grid_decide, relx=.02, rely=.02, relh=.25, relw=.65, values=['None', 'Solid', 'Dashed', 'Dashdot', 'Dotted'], orient='h')

        self.grid_width_lblsb = LabelSpin(self.grid_options, text='Grid Width', from_=.1, to=1, increment=.1, relx=.02, rely=.3, relh=.25, relw=.65, orient='h')

        self.grid_col_btn = Button(self.grid_options, text='Color', command=self.grid_color_choser)

       ### Plot options

        self.marker = Checkbutton(self.plot_options, variable=self.marker_cbtn, text='Marker', command=self.cb_clicked)

        self.linestyle_chkbtn = Checkbutton(self.plot_options, text='Line Style', variable=self.lss_cbtn, command=self.cb_clicked)

        self.linewidth_lblsb = LabelSpin(self.plot_options,  text='Line Width', relx=.02, rely=.52, relh=.24, relw=.64, to=1, from_=.1, increment=.1, orient='h')


        self.alpha_lblsb = LabelSpin(self.plot_options,  text='Alpha', relx=.02, rely=.76, relh=.24, relw=.64, to=1, from_=.1, increment=.1, orient='h')

       ## Bar Options
        self.switch = Checkbutton(self.bar_options, variable=self.switch_cbtn, text='Switch', command=self.cb_clicked)

       ###### Pie Options

        self.inapp_chkbtn = Checkbutton(self.pie_options, text='Inapp', variable=self.inapp_cbtn, command=self.inapp_info)

        self.explode_chkbtn = Checkbutton(self.pie_options, text='Explode', variable=self.explode_cbtn, command=self.cb_clicked)

        self.shadow_chkbtn = Checkbutton(self.pie_options,text='Shadow', variable=self.shadow_cbtn, command=self.cb_clicked)
