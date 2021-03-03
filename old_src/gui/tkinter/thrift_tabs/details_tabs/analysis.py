
from ...utils.decorate.styles import Fonts, Styles
from ...utils.widgets.debug import show, confirm
from tkinter import StringVar, colorchooser, Button, Frame
from tkinter.ttk import Notebook
from .....backend.thrift.regions.years import Years
from .....backend.utils.threads import Threads
from .....backend.utils.sort.thrift.weeks import Weeks, Date, MONTHS_NAMES, DAYS_NAMES
from .....backend.utils.debug.debug import Debug
from .....backend.utils.details.tdetails import TDetails
from .....backend.utils.sort.thrift.chart_sort import Chart_Sort, Regions
from ...utils.widgets.twowidgets import LabelCombo, CheckCombo, LabelSpin, RadioCombo, TwoWidgets, Checkbutton, LabelFrame, Radiobutton

class Thrift_Analysis(Frame):
    plots_figures = []
    def __init__(self, master, small_details, full_details, details_output, **kw):
        super().__init__(master, **kw)

       #### General Widgets
        self.small_details = small_details
        self.full_details = full_details
        self.details_output = details_output

        self.details_lblfrm = LabelFrame(self)


       ####### Variables #########

        self.region_cbtn = StringVar()
        self.data_cbtn = StringVar()
        self.spec_cbtn = StringVar()
        self.plot_spec_cbtn = StringVar()
        self.expand_cbtn = StringVar()

        self.clnt_cbtn = StringVar()
        self.sav_cbtn = StringVar()
        self.deb_cbtn = StringVar()
        self.not_paid_cbtn = StringVar()
        self.brf_cbtn = StringVar()
        self.bal_cbtn = StringVar()
        self.upf_cbtn = StringVar()
        self.pupf_cbtn = StringVar()
        self.rupf_cbtn = StringVar()
        self.com_cbtn = StringVar()
        self.sole_cbtn = StringVar()
        self.def_cbtn = StringVar()
        self.exc_cbtn = StringVar()
        self.bto_cbtn = StringVar()


        self.switch_cbtn = StringVar()
        self.grid_cbtn = StringVar()
        self.explode_cbtn = StringVar()
        self.shadow_cbtn = StringVar()
        self.inapp_cbtn = StringVar()


        self.grid_style_cbtn = StringVar()
        self.marker_cbtn = StringVar()
        self.lss_cbtn = StringVar()

      ############## Get
        self.get_lblfrm = LabelFrame(self.details_lblfrm, text="""Get Details""")



        self.get_yr_lblcb = RadioCombo(self.get_lblfrm, text="""Year""", func=self.get_year, relx=.037, rely=.144, relh=.331, relw=.3, variable=self.region_cbtn, value="year", command=self.choosable)

        self.get_mn_lblcb = RadioCombo(self.get_lblfrm, text="""Month""", func=self.get_month, relx=.36, rely=.144, relh=.331, relw=.3, variable=self.region_cbtn, value="month", command=self.choosable)

        self.get_ar_lblcb = RadioCombo(self.get_lblfrm,  text="""Area""", func=self.get_area, relx=.68, rely=.144, relh=.331, relw=.3, variable=self.region_cbtn, value="area", command=self.choosable)

        self.get_cl_lblcb = RadioCombo(self.get_lblfrm, text="""Client""", func=self.get_client, relx=.037, rely=.565, relh=.331, relw=.3, variable=self.region_cbtn, value="client", command=self.choosable)


        self.get_wk_lblcb = LabelCombo(self.get_lblfrm, text="""Week""", relx=.38, rely=.565, relh=.331, relw=.3, func=self.get_week)

        self.get_dy_lblcb = LabelCombo(self.get_lblfrm,  text="""Days""", relx=.68, rely=.565, relh=.331, relw=.3, func=self.get_day)

      ############ Datas
        self.data_lblfrm = LabelFrame(self.details_lblfrm, text=""" Datas""")


        self.years_rb = Radiobutton(self.data_lblfrm,  text="""Years""", value="years", variable=self.data_cbtn, command=self.rb_clicked)


        self.months_rb = Radiobutton(self.data_lblfrm, text="""Months""", value="months", variable=self.data_cbtn, command=self.rb_clicked)



        self.areas_rb = Radiobutton(self.data_lblfrm,text="""Areas""", value="areas", variable=self.data_cbtn, command=self.rb_clicked)

        self.clients_rb = Radiobutton(self.data_lblfrm, text="""Clients""", value="clients", variable=self.data_cbtn, command=self.rb_clicked)

        self.weeks_rb = Radiobutton(self.data_lblfrm, text="""Weeks""", value="weeks", variable=self.data_cbtn, command=self.rb_clicked)


        self.days_rb = Radiobutton(self.data_lblfrm, text="""Days""", value="days", variable=self.data_cbtn, command=self.rb_clicked)


      ############ Specific Datas
        self.s_data_lblfrm = LabelFrame(self.details_lblfrm, text="""Specific Datas""")


        self.s_d_month_chkcb = RadioCombo(self.s_data_lblfrm, text="""Months""", variable=self.spec_cbtn, relx=.05, rely=.16, relh=.4, relw=.45, values=MONTHS_NAMES[1:], value="spec_month", command=self.spec_choosable, func=self.get_spec_month)

        self.s_d_week_chkcb = RadioCombo(self.s_data_lblfrm, text="""Weeks""", variable=self.spec_cbtn, relx=.05, rely=.57, relh=.4, relw=.45, values=Weeks.weeks,  value="spec_week", command=self.spec_choosable, func=self.get_spec_week)

        self.s_d_day_chkcb = RadioCombo(self.s_data_lblfrm, text="""Days""", variable=self.spec_cbtn, relx=.55, rely=.16, relh=.4, relw=.4, values=DAYS_NAMES,  value="spec_day", command=self.spec_choosable, func=self.get_spec_day)


        self.s_d_area_chkcb = RadioCombo(self.s_data_lblfrm, text="""Areas""", variable=self.spec_cbtn,  relx=.55, rely=.57, relh=.4, relw=.4, bordermode="ignore",value="spec_area", command=self.spec_choosable, func=self.get_spec_area)

      ############ Plot Datas
        self.fig1, self.fig2, self.fig3, self.fig4 = self.plots_figures

        self.plot_data_lblfrm = LabelFrame(self.details_lblfrm, text="""Datas (Y-axis)""",)


        self.p_clnt_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""Clients""", variable=self.clnt_cbtn, command=self.cb_clicked)


        self.p_brf_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""Brought-Fs""", variable=self.brf_cbtn, command=self.cb_clicked)


        self.p_com_chkbtn = Checkbutton(self.plot_data_lblfrm, text="Commissions", variable=self.com_cbtn, command=self.cb_clicked)

        self.p_sav_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""Savings""", variable=self.sav_cbtn, command=self.cb_clicked)

        self.p_deb_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""Debits""", variable=self.deb_cbtn, command=self.cb_clicked)

        self.p_not_paid_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""Not-Paids""", variable=self.not_paid_cbtn, command=self.cb_clicked)

        self.p_upf_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""Upfronts""", variable=self.upf_cbtn, command=self.cb_clicked)


        self.p_pupf_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""P-Upfronts""", variable=self.pupf_cbtn, command=self.cb_clicked)


        self.p_rupf_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""R-Upfronts""", variable=self.rupf_cbtn, command=self.cb_clicked)

        self.p_bal_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""Balances""", variable=self.bal_cbtn, command=self.cb_clicked)


        self.p_bto_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""B-T-Os""", variable=self.bto_cbtn, command=self.cb_clicked)

        self.p_def_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""Deficits""", variable=self.def_cbtn, command=self.cb_clicked)

        self.p_exc_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""Excesses""", variable=self.exc_cbtn, command=self.cb_clicked)


        self.sole_chkbtn = Checkbutton(self.plot_data_lblfrm, text="""Sole Region""", variable=self.sole_cbtn, command=self.rest_datas)

      ########## Chart Options
        self.chart_lblfrm = LabelFrame(self.details_lblfrm, text="""Chart Options""")

       ### Fig number
        self.fig_lblsb = LabelSpin(self.chart_lblfrm, text="""Fig. No.""", relx=.003, rely=.003, relh=.18, relw=.4, to=4, from_=1, increment=1, orient="h")

       ###### Chart Type
        self.chart_type = None
        self.chart_types = LabelCombo(self.chart_lblfrm,  text="Chart Types", relx=.403, rely=.003, relh=.18, relw=.58, values=["Plot", "Bar", "Barh", "Hist", "Pie"], func=self.chart_types_choser, orient="h")

       ########## Chart Types Options
        self.ch_ty_op_nb = Notebook(self.chart_lblfrm)

        self.grid_options = LabelFrame(self.chart_lblfrm, takefocus="")
        self.ch_ty_op_nb.add(self.grid_options, padding=1)
        self.ch_ty_op_nb.tab(0, text="Grid Options",compound="left",underline="0")

        self.plot_options = LabelFrame(self.chart_lblfrm, takefocus="")
        self.ch_ty_op_nb.add(self.plot_options, padding=1)
        self.ch_ty_op_nb.tab(1, text="Plot Options",compound="left",underline="0")

        self.bar_options = LabelFrame(self.chart_lblfrm, takefocus="")
        self.ch_ty_op_nb.add(self.bar_options, padding=1)
        self.ch_ty_op_nb.tab(2, text="Bar Options",compound="left",underline="0")

        self.pie_options = LabelFrame(self.chart_lblfrm, takefocus="")
        self.ch_ty_op_nb.add(self.pie_options, padding=1)
        self.ch_ty_op_nb.tab(3, text="Pie Options",compound="left",underline="0")

       ########## Grid lines
        self.grid_style = "None"
        self.grid_color = Styles.background

        self.grid_style_lblcb = CheckCombo(self.grid_options, text="""Grid Style""", variable=self.grid_cbtn, func=self.grid_style_choser, command=self.grid_decide, relx=.02, rely=.02, relh=.25, relw=.65, values=["None", "Solid", "Dashed", "Dashdot", "Dotted"], orient="h")

        self.grid_width_lblsb = LabelSpin(self.grid_options, text="""Grid Width""", from_=.1, to=1, increment=.1, relx=.02, rely=.3, relh=.25, relw=.65, orient="h")

        self.grid_col_btn = Button(self.grid_options, text="""Color""", command=self.grid_color_choser)

       ### Plot options

        self.marker = Checkbutton(self.plot_options, variable=self.marker_cbtn, text="Marker", command=self.cb_clicked)

        self.linestyle_chkbtn = Checkbutton(self.plot_options, text="Line Style", variable=self.lss_cbtn, command=self.cb_clicked)

        self.linewidth_lblsb = LabelSpin(self.plot_options,  text="Line Width", relx=.02, rely=.52, relh=.24, relw=.64, to=1, from_=.1, increment=.1, orient="h")


        self.alpha_lblsb = LabelSpin(self.plot_options,  text="Alpha", relx=.02, rely=.76, relh=.24, relw=.64, to=1, from_=.1, increment=.1, orient="h")

       ## Bar Options
        self.switch = Checkbutton(self.bar_options, variable=self.switch_cbtn, text="Switch", command=self.cb_clicked)

       ###### Pie Options

        self.inapp_chkbtn = Checkbutton(self.pie_options, text="""Inapp""", variable=self.inapp_cbtn, command=self.inapp_info)

        self.explode_chkbtn = Checkbutton(self.pie_options, text="""Explode""", variable=self.explode_cbtn, command=self.cb_clicked)

        self.shadow_chkbtn = Checkbutton(self.pie_options,text="""Shadow""", variable=self.shadow_cbtn, command=self.cb_clicked)

      ############ Plot and Clear

        self.plot_btn = Button(self.chart_lblfrm, command=self.chart_sort, text="Plot")

        self.clear_btn = Button(self.chart_lblfrm, command=self.clear_plot, text="Clear")


      ##### All Years CheckButton
        self.years_chkbtn = Radiobutton(self.details_lblfrm,text="""ALL\nYears""", command=self.get_years, value="years", variable=self.region_cbtn)
        self.plot_spec_chkbtn = Checkbutton(self.details_lblfrm, text="""Plot\nSpec""", variable=self.plot_spec_cbtn, command=self.cb_clicked)

        self.expand_chkbtn = Checkbutton(self.details_lblfrm,text="""Expand""", variable=self.expand_cbtn, command=self.cb_clicked)

        ############# Defaults
        self.load()
        self.default()
        self.style()


 ### Regions sort
    def get_years(self):
        self.rb_clicked()
        self.choosable()
        header = self.data_cbtn.get()
        if Years.years:
            total_areas = max([year.max_areas for year in Years.years])
            if total_areas:
                self.plot_years = Years
                str_areas = [f"Area_{num}" for num in range(1, total_areas + 1)]
                self.s_d_area_chkcb.set(str_areas)

            else: show("No Areas", "No area data to load", "error")

            if header in ["years", "months","areas"]:
                title = "All Years"
                if header == "months": title = "Months in " + title
                elif header == "areas": title = "Areas in " + title

                self.get_small_details(title=title,  header=header, region=Years)
            else:
                ttl, msg = "Requires Datas", "Choose Years or Months or Areas first"
                show(ttl, msg, "error")

    def get_year(self, e):
        self.region_cbtn.set("year")
        self.choosable()
        header = self.data_cbtn.get()
        self.year = Regions.check_year(self.get_yr_lblcb.get())
        if self.year:
            self.plot_year = self.year
            months = [month.name for month in self.year.months]
            self.get_mn_lblcb.set(values=months)

            if header in ["months","areas"]:  self.get_small_details(title=self.year,  header=header, region=self.year)
            else:
                ttl, msg = "Requires Datas", "Choose Months or Areas first"
                show(ttl, msg, "error")
        else: show("Require Year", "Select Year", "error")

    def get_month(self, e):
        self.region_cbtn.set("month")
        self.choosable()
        header = self.data_cbtn.get()
        self.month = Regions.check_month(self.get_yr_lblcb.get(), self.get_mn_lblcb.get())
        if self.month:
            self.plot_month = self.month
            areas = [area.name for area in self.month.areas]
            self.get_ar_lblcb.set(values=areas)
            self.get_wk_lblcb.set(Weeks.weeks)
            self.s_d_area_chkcb.set(areas)

            if header in ["areas", "weeks", "days"]: self.get_small_details(title=self.month, region =self.month,  header=header)
            else:
                ttl, msg = "Requires Datas", "Choose Areas or Weeks or Days first"
                show(ttl, msg, "error")
        else: show("Requires Regions", "Pick a valid Year", "error")

    def get_area_number(self, area_name):
        try: return area_name.split("_")[1]
        except Exception as e:
            print(e);
            ttl, msg = "Requires Area", "Choose an Area_first"
            show(ttl, msg, "error")

    def get_area(self, *args):
        self.region_cbtn.set("area")
        self.choosable()
        area_number = self.get_area_number(self.get_ar_lblcb.get())
        self.area = Regions.check_area(self.get_yr_lblcb.get(), self.get_mn_lblcb.get(), area_number)
        if self.area:
            self.plot_area = self.area
            header = header = self.data_cbtn.get()
            clients = [client.name for client in self.area.clients]
            Regions.number_name(clients)
            self.get_cl_lblcb.set(values=clients)

            if header in ["clients", "weeks", "days"]: self.get_small_details(title=self.area, region=self.area,  header=header)
            else:
                ttl, msg = "Requires Datas", "Choose Clients or Weeks or Days first"
                show(ttl, msg, "error")
        else: show("Requires Regions", "Pick a valid Month", "error")

    def get_client(self, *args):
        self.region_cbtn.set("client")
        self.choosable()
        self.client = Regions.check_client(self.get_yr_lblcb.get(), self.get_mn_lblcb.get(), self.get_area_number(self.get_ar_lblcb.get()), name=self.get_cl_lblcb.get().split(". ", maxsplit=1)[1])

        if self.client:
            self.plot_client = self.client
            header = self.data_cbtn.get()

            if header in ["weeks", "days"]:
                if header == "weeks": header = "clnt_weeks"
                elif header == "days": header = "clnt_days"

                self.get_small_details(title=self.client, region=self.client,  header=header)
            else:
                ttl, msg = "Requires Datas", "Choose  Weeks or Days first"
                show(ttl, msg, "error")
        else: show("Requires Regions", "Pick a valid Area", "error")

    def get_week(self, e):
        go = 0
        week = self.get_wk_lblcb.get()
        self.week = week
        str_region = self.region_cbtn.get()
        header = self.data_cbtn.get()
        if str_region in ["month", "area", "client"]:
            if str_region == "month":
                region = self.month
                if header in ["areas", "days"]: go = 1
                else: self.details_output("Choose among Areas, Days", title="Requires Datas", which="error")

            if str_region == "area":
                region = self.area
                if header in ["clients", "days"]: go = 1
                else: self.details_output("Choose among Clients, Days", title="Requires Datas", which="error")

            if str_region == "client":
                region = self.client
                if header == "days":
                    header = "clnt_days"
                    go = 1
                else: self.details_output("Choose among Days", title="Requires Datas", which="error")

            if go:
                title = f"{week} | {region}"

                self.get_dy_lblcb.set(Weeks.date_name_string(self.month, week))

                self.get_small_details(title=title, region=region, header=header, week=week)
        else: self.details_output("Choose among Month, Area, Client", title="Requires Region", which="error")

    def get_day(self, e):
        go = 0
        str_region = self.region_cbtn.get()
        header = self.data_cbtn.get()
        day = self.get_dy_lblcb.get()
        date, name = day.split(" | ")

        if str_region in ["month", "area", "client"]:
            if str_region == "month":
                region = self.month
                if header == "areas": go = 1
                else: self.details_output("Choose among Areas", title="Requires Datas", which="error")

            if str_region == "area":
                region = self.area
                if header == "clients": go = 1
                else: self.details_output("Choose among Clients", title="Requires Datas", which="error")

            if str_region == "client":
                region = self.client
                go = 1

            if go:
                week = self.week
                title = f"{day} | {week} | {region}"

                self.get_small_details(title=title, region=region, header=header, week=week, day=date)
        else: self.details_output("Choose among Month, Area, Client", title="Requires Region", which="error")

    def get_spec_month(self, e):
        if self.data_cbtn.get() == "years":
            header = "spec_month"
            self.spec_cbtn.set(header)
            month_name = self.s_d_month_chkcb.get()
            title = f"{month_name} in All Years"
            self.get_small_details(title=title, header=header, region=title, month=month_name, spec=header)
        else: self.details_output("Choose Years", title="Requires Datas", which="error")

    def get_spec_week(self, e):
        if self.data_cbtn.get() == "months":
            header = "spec_week"
            self.spec_cbtn.set(header)

            try:
                year = self.year
                week_name = self.s_d_week_chkcb.get()
                title = f"{week_name}s in {year}"
                self.get_small_details(title=title, header=header, region=year, week=week_name, spec=header)

            except Exception as e:
                print(e)
                ttl, msg = "Requires Year", "Choose a Year first"
                show(ttl, msg, "error")
        else: self.details_output("Choose among Months", title="Requires Datas", which="error")

    def get_spec_day(self, e):
        str_region = self.region_cbtn.get()
        day = self.s_d_day_chkcb.get()
        header = "spec_day"
        self.spec_cbtn.set(header)

        if str_region in ["month", "area", "client"]:
            if str_region == "month": region = self.month
            elif str_region == "area": region = self.area
            elif str_region == "client": region = self.client

            title = f"{day}s in {region}"

            self.get_small_details(title=title, region=region, header=header, spec=header, day=day)

        else: self.details_output("Choose among Month, Area, Client", title="Requires Region", which="error")

    def get_spec_area(self, e):
        go = 0
        area_name = self.s_d_area_chkcb.get()

        self.spec_cbtn.set("spec_area")
        if self.data_cbtn.get() in ["years", "months"]:
            self.spec_cbtn.set("spec_area")
            if self.data_cbtn.get() == "months":
                if self.region_cbtn.get() == "year":
                    go = 1
                    region = self.year
                    title = f"{area_name}s in {self.year}"
                    header = "spec_area_yr"

                else: self.details_output("Choose Year", title="Requires Regions", which="error")
            else:
                title = f"{area_name}s in Years"
                go = 1
                region = None
                header = "spec_area_yrs"
            if go: self.get_small_details(title=title,  header=header, region=region, spec="spec_area", area=area_name)
        else: self.details_output("Choose among Years or Months", title="Requires Datas", which="error")

    def get_small_details(self, title='', header='', region=None, week='', day='', month='', spec='', area=''):

        if not spec: self.small_details.thrift_update(region=region, week=week, day=day, month=month)

        if isinstance(region, str): pass
        elif region.which == "client" and header == "days": pass
        else: self.full_details(title=title, region=region, header=header, week=week, day=day, month=month, spec=spec, area=area)

        if region == Years: region = "All Years"
        elif "spec" in header: region = title
        self.details_output(region)

 ######### Ploting

    def get_datas(self):
        plotable = []
        if self.clnt_cbtn.get() == "1": plotable.append("clnt")
        if self.sav_cbtn.get() == "1": plotable.append("sav")
        if self.deb_cbtn.get() == "1": plotable.append("deb")
        if self.not_paid_cbtn.get() == "1": plotable.append("not_paid")
        if self.brf_cbtn.get() == "1": plotable.append("brf")
        if self.bal_cbtn.get() == "1": plotable.append("bal")
        if self.upf_cbtn.get() == "1": plotable.append("upf")
        if self.pupf_cbtn.get() == "1": plotable.append("pupf")
        if self.rupf_cbtn.get() == "1": plotable.append("rupf")
        if self.com_cbtn.get() == "1": plotable.append("com")
        if self.bto_cbtn.get() == "1": plotable.append("bto")
        if self.def_cbtn.get() == "1": plotable.append("def")
        if self.exc_cbtn.get() == "1": plotable.append("exc")

        return plotable


    def chart_sort(self):
        str_region = self.region_cbtn.get()
        datas = self.data_cbtn.get()
        spec_datas = self.spec_cbtn.get() or None
        month = area = day = week = None
        sole = self.sole_cbtn.get()
        go = 0
        if str_region == "years":
            try:
                region = self.plot_years

                if self.plot_spec_cbtn.get() != "1":
                    if sole == "1":
                        title = "ALL Years DETAILS"
                        xlabel = "Records"
                        ylabel = ""
                        go = 1
                    elif datas == "years":
                        title = "All Years"
                        xlabel = "Years"
                        ylabel = "Records"
                        go = 1
                    elif datas == "months":
                        title = "Months in All Years"
                        xlabel = "Months"
                        ylabel = "Records"
                        go = 1
                    elif datas == "areas":
                        title = "Areas in All Years"
                        xlabel = "Areas"
                        ylabel = "Records"
                        go = 1
                    else: self.details_output("Choose Years or Months or Areas", title="Required Datas", which="error"); go = 0
                else:
                    if spec_datas == "spec_month":
                        month = self.s_d_month_chkcb.get()

                        title = f"{month} in ALL Years"
                        xlabel = "Years"
                        ylabel = "Records"
                        go = 1
                    elif spec_datas == "spec_area":
                        area = self.s_d_area_chkcb.get()

                        title = f"{area} in ALL Years"
                        xlabel = "Years"
                        ylabel = "Records"
                        go = 1
            except: show("Requires Regions", "Not loaded", "error"); go = 0

        elif str_region == "year":
            try:
                region = self.plot_year
                if self.plot_spec_cbtn.get() != "1":

                    if sole == "1":
                        title = f"{region} DETAILS"
                        xlabel = "Records"
                        ylabel = ""
                        go = 1
                    elif datas == "months":
                        title = f"Months in Year {region}"
                        xlabel = "Months"
                        ylabel = "Records"
                        go = 1
                    elif datas == "areas":
                        title = f"Areas in Year {region}"
                        xlabel = "Areas"
                        ylabel = "Records"
                        go = 1
                    else: self.details_output("Choose Months or Areas", title="Required Datas", which="error"); go = 0
                else:
                    if spec_datas == "spec_area":
                        area = self.s_d_area_chkcb.get()

                        title = f"{area} in {region}"
                        xlabel = "Months"
                        ylabel = "Records"
                        go = 1
            except: show("Requires Regions", "Pick a valid Year", "error"); go = 0

        elif str_region == "month":
            try:
                region = self.plot_month

                if sole == "1":
                    title = f"{region} DETAILS"
                    xlabel = "Records"
                    ylabel = ""
                    go = 1
                elif datas == "areas":
                    title = f"Areas in {region}"
                    xlabel = "Areas"
                    ylabel = "Records"
                    go = 1
                elif datas == "weeks":
                    title = f"Weeks in {region}"
                    xlabel = "Weeks"
                    ylabel = "Records"
                    go = 1
                else: self.details_output("Choose Areas or Weeks", title="Required Datas", which="error"); go = 0
            except: show("Requires Regions", "Pick a valid Month", "error"); go = 0

        elif str_region == "area":
            try:
                region = self.plot_area
                if sole == "1":
                    title = f"{region} DETAILS"
                    xlabel = "Records"
                    ylabel = ""
                    go = 1
                elif datas == "weeks":
                    title = f"Weeks in {region}"
                    xlabel = "Years"
                    ylabel = "Records"
                    go = 1
                else: self.details_output("Choose Weeks", title="Required Datas", which="error"); go = 0
            except: show("Requires Regions", "Pick a valid Area", "error"); go = 0


        else: self.details_output("Choose All Years or Year or Month or Area_or Client", title="Required Regions", which="error"); go = 0

        if go:
            self.sorted_datas = Chart_Sort(region=region, yaxis=self.get_datas(), sole=sole, month=month, area=area, header=datas)
            self.sorted_datas.xlabel = xlabel
            self.sorted_datas.ylabel = ylabel
            self.sorted_datas.title = title
            self.gather_to_plot()

        elif go == 0: self.details_output("This is not implemented yet Value = Zero", title="Not Implemented", which="info")

    def gather_to_plot(self):

        if self.sorted_datas.go:
            xticks = self.sorted_datas.xticks
            ys = self.sorted_datas.ys
            labels = self.sorted_datas.labels
            print(labels)

            xlabel = self.sorted_datas.xlabel
            ylabel = self.sorted_datas.ylabel
            title = self.sorted_datas.title

            if self.lss_cbtn.get() == "1": lss = True
            else: lss = None

            lw = self.plot_linewidth_choser()

            if self.marker_cbtn.get() == "1": marker = True
            else: marker = None

            alpha = self.alpha_choser()

            if self.explode_cbtn.get() == "1": explode = True
            else: explode = None


            if self.shadow_cbtn.get() == "1": shadow = True
            else: shadow = None

            grid = {"lw":self.grid_width_choser(), "ls":self.grid_style, "c":self.grid_color}
            # print(xticks)
            # print(ys)
            # print(labels)
            # return
            if ys: self.plot(xticks=xticks, ys=ys, labels=labels, xlabel=xlabel, ylabel=ylabel, title=title, marker=marker,  lss=lss, lw=lw, alpha=alpha,explode=explode, shadow=shadow, grid=grid)
            else: self.details_output("No selected datas to plot.", title="Select Ys", which="error")

        else: self.details_output("No road to go", title="Blockage", which="error")

    def plot(self, xticks=[], ys=[], labels=[], xlabel="", ylabel="", title="", marker=None, lss="", lw=0, alpha=0, which="", explode=None, shadow=None, grid={}):

        num = self.fig_lblsb.get()
        expand = self.expand_cbtn.get()
        if expand == "1": pass
        else: expand = None

        if num:
            num = int(num)

            fig = self.plots_figures[num - 1]



            if self.chart_type in ["bar","barh"]: fig.bar(xticks=xticks, ys=ys, labels=labels, grid=grid, xlabel=xlabel, ylabel=ylabel,title=title, which=self.chart_type, switch=self.switch_cbtn.get(), expand=expand)

            elif self.chart_type == "plot": fig.plot(xticks=xticks, ys=ys, labels=labels, grid=grid, xlabel=xlabel, ylabel=ylabel,title=title, marker=marker, lss=lss, lw=lw, alpha=alpha, expand=expand)

            elif self.chart_type == "pie":
                if isinstance(labels, str): fig.pie(ys=ys, labels=xticks, explode=explode, shadow=shadow, title=f"{labels} of {title}", inapp=self.inapp_cbtn.get(), expand=expand)
                else: self.details_output("Pick only one of Datas Y-axis for Pie Chart", title="Required One Y-axis", which="warn")

            elif self.chart_type == "hist": pass

            else: self.details_output("Pick a chart type", title="Required Chart Number", which="error")

        else: self.details_output("Pick a chart number", title="Required Chart Number", which="error")

    def clear_plot(self):
        num = self.fig_lblsb.get()
        if num:
            num = int(num)

            fig = self.plots_figures[num - 1]
            fig.clear()
        else: self.details_output("Pick a chart number", title="Required Chart Number", which="error")
    def inapp_info(self):
        self.cb_clicked()
        if self.inapp_cbtn.get() == "1": show("Under Testing", "Using Pie in Inapp will distrupt the other chart drawing", "warn")
        else: pass

  ######### Grid

    def grid_decide(self):
        self.grid_style_lblcb.checked()
        options = [(self.grid_style_lblcb, "b"), (self.grid_width_lblsb, ""), self.grid_col_btn]
        if self.grid_cbtn.get() == "1":
            for option, val in options[:-1]: option.normal(val)
            options[-1]["state"] = "normal"
        else:
            self.grid_style = "None"
            self.grid_style_cbtn.set(self.grid_style)
            self.grid_color = "black"
            for option, val in options[:-1]: option.disabled(val)
            options[-1]["state"] = "disable"

    def grid_color_choser(self):
        rgb_name, self.grid_color = colorchooser.askcolor(self.grid_color)
        self.grid_col_btn.config(background=self.grid_color)
    def grid_width_choser(self):
        num = self.grid_width_lblsb.get()
        if num: return float(num)
        else: return 0
    def grid_style_choser(self, e): self.grid_style = self.grid_style_lblcb.get().lower()
    def chart_types_choser(self, e):
        self.chart_type = self.chart_types.get().lower()

        plot_conf = [ self.linestyle_chkbtn, self.marker]
        plot_dis = [self.linewidth_lblsb,self.alpha_lblsb]

        if self.chart_type != "plot":
            for conf in plot_conf: conf["state"] = "disable"
            for dis in plot_dis: dis.disabled()
        else:
            for conf in plot_conf: conf["state"] = "normal"
            for dis in plot_dis: dis.normal()


        if self.chart_type not in ["bar", "barh"]: self.switch["state"] = "disable"
        else: self.switch["state"] = "normal"

        pie_conf = [self.explode_chkbtn, self.shadow_chkbtn, self.inapp_chkbtn]
        if self.chart_type != "pie":
            for conf in pie_conf: conf["state"] = "disable"
        else:
            for conf in pie_conf: conf["state"] = "normal"


    def alpha_choser(self):
        num = self.alpha_lblsb.get()
        if num: return float(num)
        else: return 0
    def plot_color_choser(self):
        self.plot_colors = []
        rgb_name, plot_color = colorchooser.askcolor("blue")
        self.plot_colors.append(plot_color)
        self.plot_colors_btn.config(background=plot_color)

    def plot_linewidth_choser(self):
        num = self.linewidth_lblsb.get()
        if num: return float(num)
        else: return 0

 ###### load and save
    def load(self): self.get_yr_lblcb.set(Years.years_names)
    def save(self): Threads.save_data()

    def default(self):
        self.region_cbtn.set(" ")
        self.data_cbtn.set("areas")
        self.spec_cbtn.set(" ")
        self.plot_spec_cbtn.set(" ")

        self.expand_cbtn.set(" ")

        self.clnt_cbtn.set(" ")
        self.sav_cbtn.set(" ")
        self.deb_cbtn.set(" ")
        self.not_paid_cbtn.set(" ")
        self.brf_cbtn.set(" ")
        self.bal_cbtn.set(" ")
        self.upf_cbtn.set(" ")
        self.pupf_cbtn.set(" ")
        self.rupf_cbtn.set(" ")
        self.com_cbtn.set(" ")
        self.sole_cbtn.set(" ")
        self.def_cbtn.set(" ")
        self.exc_cbtn.set(" ")
        self.bto_cbtn.set(" ")

        self.switch_cbtn.set(" ")
        self.grid_cbtn.set(" ")
        self.grid_style_cbtn.set("None")
        self.explode_cbtn.set(" ")
        self.shadow_cbtn.set(" ")
        self.inapp_cbtn.set(" ")
        self.lss_cbtn.set(" ")

        self.marker_cbtn.set(" ")

        self.grid_decide()
        self.chart_types_choser(0)

 ######### Choosable buttons
    def rest_datas(self):
        self.cb_clicked()
        actives = [self.p_clnt_chkbtn, self.p_brf_chkbtn, self.p_com_chkbtn, self.p_sav_chkbtn, self.p_deb_chkbtn, self.p_not_paid_chkbtn, self.p_rupf_chkbtn, self.p_pupf_chkbtn, self.p_upf_chkbtn, self.p_bal_chkbtn, self.p_def_chkbtn, self.p_bto_chkbtn, self.p_exc_chkbtn]
        if self.sole_cbtn.get() == "1":
            for active in actives: active.config(state="disabled")
        else:
            for active in actives: active["state"] = "normal"

    def activate(self):
        actives = [self.p_clnt_chkbtn, self.p_brf_chkbtn, self.p_com_chkbtn, self.p_sav_chkbtn, self.p_deb_chkbtn, self.p_not_paid_chkbtn, self.p_upf_chkbtn, self.p_pupf_chkbtn, self.p_rupf_chkbtn, self.p_bal_chkbtn, self.sole_chkbtn,  self.years_rb, self.months_rb, self.areas_rb, self.clients_rb, self.weeks_rb, self.days_rb, self.s_d_month_chkcb, self.s_d_week_chkcb, self.s_d_area_chkcb, self.s_d_day_chkcb, self.get_yr_lblcb, self.get_mn_lblcb, self.get_ar_lblcb, self.get_cl_lblcb]
        for active in actives: active.config(state="active")

    def choosable(self):
        self.load()

        self.get_cl_lblcb.checked()
        self.get_ar_lblcb.checked()
        self.get_mn_lblcb.checked()
        self.get_yr_lblcb.checked()


        choices = {"years":self.years_rb, "months":self.months_rb, "areas":self.areas_rb, "clients":self.clients_rb, "weeks":self.weeks_rb, "days":self.days_rb}
        region = self.region_cbtn.get()
        headers = []

        if region == "years":
            headers = ["years", "months", "areas"]
            remains = ["clients", "weeks", "days"]
        elif region == "year":
            headers = ["months", "areas"]
            remains = ["years", "clients", "weeks", "days"]
        elif region == "month":
            headers = ["areas", "weeks", "days"]
            remains = ["years", "months", "clients"]
        elif region == "area":
            headers = ["clients", "weeks", "days"]
            remains = ["years", "months", "areas"]
        elif region == "client":
            headers = ["weeks", "days"]
            remains = ["years", "months", "areas", "clients"]

        if headers:
            for header in headers:
                choices[header]["state"] = "normal"
            for choice in remains: choices[choice].config(state="disabled")

    def spec_choosable(self):
        self.s_d_month_chkcb.checked()
        self.s_d_week_chkcb.checked()
        self.s_d_day_chkcb.checked()
        self.s_d_area_chkcb.checked()

        choices = {"years":self.years_rb, "months":self.months_rb, "areas":self.areas_rb, "clients":self.clients_rb, "weeks":self.weeks_rb, "days":self.days_rb}
        spec = self.spec_cbtn.get()
        headers = []
        remains = []
        if spec == "spec_month":
            headers = ["years"]
            remains = ["clients", "weeks", "days", "months", "areas"]


        elif spec == "spec_week":
            headers = ["months"]
            remains = ["clients", "weeks", "days", "years", "areas"]

        elif spec == "spec_day":
            headers = ["months", "areas", "clients"]
            remains = ["years",  "weeks", "days"]

        elif spec == "spec_area":
            headers = ["years", "months"]
            remains = ["clients", "weeks", "days", "areas"]

        if headers:
            for header in headers:
                choices[header]["state"] = "normal"
            for choice in remains: choices[choice].config(state="disabled")

 ###### Style
    def style(self):
        self.config(background=Styles.background)
        buttons = [self.years_rb, self.months_rb, self.areas_rb, self.clients_rb, self.weeks_rb, self.days_rb, self.p_clnt_chkbtn, self.p_brf_chkbtn, self.p_brf_chkbtn, self.p_com_chkbtn, self.p_sav_chkbtn, self.p_deb_chkbtn, self.p_not_paid_chkbtn, self.p_upf_chkbtn, self.p_pupf_chkbtn, self.p_rupf_chkbtn, self.p_bal_chkbtn, self.sole_chkbtn, self.switch, self.marker, self.linestyle_chkbtn, self.inapp_chkbtn, self.explode_chkbtn, self.shadow_chkbtn, self.plot_spec_chkbtn, self.expand_chkbtn, self.grid_col_btn, self.p_exc_chkbtn, self.p_bto_chkbtn, self.p_def_chkbtn]
        for button in buttons: button.config(activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor="white", justify="left", overrelief="ridge", relief="groove")


        frames = [self.grid_options, self.plot_options, self.bar_options, self.pie_options, self.plot_data_lblfrm, self.details_lblfrm, self.get_lblfrm, self.data_lblfrm, self.s_data_lblfrm, self.chart_lblfrm]
        for frame in frames: frame.config(relief="groove", font=Fonts.font11b, foreground=Styles.foreground, background=Styles.background, highlightbackground=Styles.background, highlightcolor=Styles.foreground)

        radiobuttons = [self.years_chkbtn, self.plot_btn, self.clear_btn]
        for radiobutton in radiobuttons:
            if radiobutton == self.years_chkbtn: Fonts.font = Fonts.font11b
            else: Fonts.font = Fonts.font22b
            radiobutton.config(activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, justify="left", overrelief="groove", relief="solid")

        styles = [sty for sty in list(self.__dict__.values()) if isinstance(sty, TwoWidgets)]
        for style in styles: style.style()

        self.cb_clicked()
        self.rb_clicked()

    def cb_clicked(self):
        buts = {self.p_clnt_chkbtn:self.clnt_cbtn, self.p_brf_chkbtn:self.brf_cbtn, self.p_com_chkbtn:self.com_cbtn, self.p_sav_chkbtn:self.sav_cbtn, self.p_deb_chkbtn:self.deb_cbtn, self.p_not_paid_chkbtn:self.not_paid_cbtn, self.p_upf_chkbtn:self.upf_cbtn, self.p_pupf_chkbtn:self.pupf_cbtn, self.p_rupf_chkbtn:self.rupf_cbtn, self.p_bal_chkbtn:self.bal_cbtn, self.p_bto_chkbtn:self.bto_cbtn, self.p_def_chkbtn:self.def_cbtn, self.p_exc_chkbtn:self.exc_cbtn, self.shadow_chkbtn:self.shadow_cbtn, self.plot_spec_chkbtn:self.plot_spec_cbtn, self.sole_chkbtn:self.sole_cbtn, self.switch:self.switch_cbtn, self.marker:self.marker_cbtn, self.linestyle_chkbtn:self.lss_cbtn, self.inapp_chkbtn:self.inapp_cbtn, self.explode_chkbtn:self.explode_cbtn, self.expand_chkbtn:self.expand_cbtn}
        for but in buts:
            var = buts[but]
            if var.get() == "1": but["fg"] = "blue"
            else: but["fg"] = Styles.foreground

    def rb_clicked(self):
        data = [self.years_rb, self.months_rb, self.areas_rb, self.clients_rb, self.weeks_rb, self.days_rb]
        region = [self.years_chkbtn]
        buts = data + region

        for but in buts:
            var = self.data_cbtn
            if but in region: var = self.region_cbtn
            val = but["value"]
            if var.get() == val: but["fg"] = "blue"
            else: but["fg"] = Styles.foreground

    def place_widgs(self):
        self.details_lblfrm.place(relx=0, rely=0, relh=1, relw=1)
        self.get_lblfrm.place(relx=0, rely=0, relh=.3, relw=.5)
        self.data_lblfrm.place(relx=.5, rely=0, relh=.17, relw=.5)
        self.years_rb.place(relx=.05, rely=.3, relh=.25, relw=.26, bordermode="ignore")
        self.months_rb.place(relx=.365, rely=.3, relh=.25, relw=.26, bordermode="ignore")
        self.areas_rb.place(relx=.68, rely=.3, relh=.25, relw=.29, bordermode="ignore")
        self.clients_rb.place(relx=.05, rely=.65, relh=.25, relw=.26, bordermode="ignore")
        self.weeks_rb.place(relx=.365, rely=.65, relh=.25, relw=.26, bordermode="ignore")
        self.days_rb.place(relx=.68, rely=.65, relh=.25, relw=.29, bordermode="ignore")
        self.s_data_lblfrm.place(relx=.5, rely=.17, relh=.22, relw=.5)
        self.plot_data_lblfrm.place(relx=0, rely=.3, relh=.3, relw=.5)
        self.p_clnt_chkbtn.place(relx=.04, rely=.13, relh=.124, relw=.45, bordermode="ignore")
        self.p_brf_chkbtn.place(relx=.51, rely=.13, relh=.124, relw=.45, bordermode="ignore")
        self.p_com_chkbtn.place(relx=.04, rely=.254, relh=.124, relw=.45, bordermode="ignore")
        self.p_sav_chkbtn.place(relx=.51, rely=.254, relh=.124, relw=.45, bordermode="ignore")
        self.p_deb_chkbtn.place(relx=.04, rely=.37, relh=.124, relw=.45, bordermode="ignore")
        self.p_not_paid_chkbtn.place(relx=.51, rely=.37, relh=.124, relw=.45, bordermode="ignore")
        self.p_upf_chkbtn.place(relx=.04, rely=.502, relh=.124, relw=.45, bordermode="ignore")
        self.p_pupf_chkbtn.place(relx=.51, rely=.502, relh=.124, relw=.45, bordermode="ignore")
        self.p_rupf_chkbtn.place(relx=.04, rely=.627, relh=.124, relw=.45, bordermode="ignore")
        self.p_bal_chkbtn.place(relx=.51, rely=.627, relh=.124, relw=.45, bordermode="ignore")
        self.p_bto_chkbtn.place(relx=.04, rely=.751, relh=.124, relw=.45, bordermode="ignore")
        self.p_def_chkbtn.place(relx=.51, rely=.751, relh=.124, relw=.45, bordermode="ignore")
        self.p_exc_chkbtn.place(relx=.04, rely=.875, relh=.124, relw=.45, bordermode="ignore")
        self.sole_chkbtn.place(relx=.51, rely=.875, relh=.124, relw=.45, bordermode="ignore")
        self.chart_lblfrm.place(relx=0, rely=.6, relh=.4, relw=.53)
        self.ch_ty_op_nb.place(relx=.003, rely=.2, relh=.8, relw=.99)
        self.grid_col_btn.place(relx=.02, rely=.7, relh=.2, relw=.65, bordermode="ignore")
        self.marker.place(relx=.02, rely=.04, relh=.24, relw=.4)
        self.linestyle_chkbtn.place(relx=.02, rely=.28, relh=.24, relw=.4)
        self.switch.place(relx=.02, rely=.14, relh=.25, relw=.3)
        self.inapp_chkbtn.place(relx=.02, rely=.04, relh=.24, relw=.32)
        self.explode_chkbtn.place(relx=.02, rely=.28, relh=.24, relw=.32)
        self.shadow_chkbtn.place(relx=.02, rely=.52, relh=.24, relw=.32)
        self.plot_btn.place(relx=.72, rely=.45, relh=.2, relw=.2)
        self.clear_btn.place(relx=.72, rely=.7, relh=.2, relw=.2)
        self.years_chkbtn.place(relx=.51, rely=.4, relh=.07, relw=.13)
        self.plot_spec_chkbtn.place(relx=.65, rely=.4, relh=.07, relw=.13)
        self.expand_chkbtn.place(relx=.79, rely=.4, relh=.07, relw=.13)

        styles = [sty for sty in list(self.__dict__.values()) if isinstance(sty, TwoWidgets)]
        for style in styles: style.place_widgs()


