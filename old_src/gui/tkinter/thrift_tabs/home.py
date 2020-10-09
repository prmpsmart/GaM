

from ..utils.decorate.calculator import Calculator
from tkinter import StringVar
from ..utils.visuals.notice import Notice, Styles, Fonts
from ....backend.utils.sort.date import Date
from ....backend.utils.sort.thrift.regions import Regions, Years
from ....backend.utils.sort.thrift.days import Days, Weeks
from ..utils.widgets.debug import show
from ....backend.utils.sort.thrift.chart_sort import Chart_Sort
from ..utils.visuals.chart import Chart


from tkinter import  Frame, Label, Radiobutton, LabelFrame, Button

class Thrift_Home(Frame):
    yaxis = records = ["clnt", "brf", "com", "sav", "deb", "not_paid", "upf", "pupf", "rupf", "bal"]
    go = 0
    def __init__(self, master):
        super().__init__(master)
        # self.master = master
        self.status = StringVar()
        self.header = StringVar()
        self.time = StringVar()
        
        self.title = Label(self, text="OVERVIEW OF AKURE GOODNESS AND MERCY COOP AND DAILY CONTRIBUTION")
        
       ############
        self.yr_nb = Notice(self,  text="Year", relx=0, rely=.05, relh=.365, relw=.333)
        
        self.mn_nb = Notice(self,  text="Month", relx=0, rely=.42, relh=.365, relw=.333)
        
        self.wk_nb = Notice(self,  text="Week", relx=.333, rely=.05, relh=.365, relw=.333)
        
        self.dy_nb = Notice(self,  text="Day", relx=.666, rely=.05, relh=.365, relw=.333)
       
        self.frame = Frame(self, background="black", relief="sunken", bd="3")
        
        self.plots_frame = Frame(self.frame)
        
       ##############

        self.options = LabelFrame(self, text="Options")
        
        self.year_choose = Radiobutton(self.options, variable=self.time, value="year", text="Year", command=self.rb_clicked)
    
        self.month_choose = Radiobutton(self.options, variable=self.time, value="month", text="Month", command=self.rb_clicked)
        
        self.week_choose = Radiobutton(self.options,  variable=self.time, value="week", text="Week", command=self.rb_clicked)
        
        self.day_choose = Radiobutton(self.options, variable=self.time, value="day", text="Day", command=self.rb_clicked)
        
        self.plot_btn = Button(self.options, text="Plot", command=self.plot_charts)
        
        self.calc_btn = Button(self.options, text="Calculator", command=Calculator)
        
        self.default_choose = Radiobutton(self.options, text="""Default""", value="default", variable=self.header, command=self.notice)
        
        self.area_choose = Radiobutton(self.options, text="""Areas""", value="areas", variable=self.header, command=self.notice)
        
        self.sole_choose = Radiobutton(self.options, variable=self.header,   value="sole", text="Sole", command=self.notice)
        
        self.hm_ne_chkbtn = Radiobutton(self.options, text="""Next""", value="next", variable=self.status, command=self.notice)
        
        self.hm_cur_chkbtn = Radiobutton(self.options, text="""Current""", value="current", variable=self.status, command=self.notice)
        
        self.hm_pr_chkbtn = Radiobutton(self.options, text="""Previous""", value="previous", variable=self.status, command=self.notice)
        
        self.status.set("current")
        self.header.set("default")
        self.time.set("year")
        
        self.grid = {"lw":1, "ls":"dotted", "c":"black"}
        
        self.plot_figs()
        self.style()

    
    def notice(self):
        self.rb_clicked()
        if not Years.years: return
        time = self.time.get()
        if time == "year": self.yr_notice()
        elif time == "month": self.mn_notice()
        elif time == "week": self.wk_notice()
        elif time == "day": self.dy_notice()

    def yr_notice(self):
        status = self.status.get()
        year = Date.get_year(status)
        year =  Regions.check_year(year)

        if year:
            print(year)
            self.yr_nb.update(yr="Months", region=year)

            header = self.header.get()
            
            if header == "default": header = "months"
            
            if header != "sole":
                area_sort = Chart_Sort(year, self.yaxis, header=header)
                area_sort.xlabel = header.title()
                area_sort.ylabel = "Records"
                area_sort.title = f"{header.title()} in {year}"
                if area_sort.go: self.plot_it(area_sort)
            
            else:
                
                sole_sort = Chart_Sort(year, self.yaxis, sole="1")
                sole_sort.xlabel = "Records"
                sole_sort.ylabel = "Records"
                sole_sort.title = f"Records in {year}"
                if sole_sort.go: self.plot_it(sole_sort)
            
            return 1
        
        else: show(title="Not found", msg="Year not found", which="error")

    def mn_notice(self):
        status = self.status.get()
        month_name, year = Date.get_month(status, 1)
        month =  Regions.check_month(year, month_name)
        
        if month:
            self.mn_nb.update(region=month)
            
            header = self.header.get()
            
            if header == "default": header = "weeks"
            
            if header != "sole":
                area_sort = Chart_Sort(month, self.yaxis, header=header)
                area_sort.xlabel = header.title()
                area_sort.ylabel = "Records"
                area_sort.title = f"{header.title()} in {month}"
                if area_sort.go: self.plot_it(area_sort)
            
            else:
                sole_sort = Chart_Sort(month, self.yaxis, sole="1")
                sole_sort.xlabel = "Records"
                sole_sort.ylabel = "Records"
                sole_sort.title = f"Records in {month}"
                if sole_sort.go: self.plot_it(sole_sort)

        else: show(title="Not found", msg="Previous Month not found", which="error")
 
    def wk_notice(self):
        status = self.status.get()
        month_name, year = Date.get_month("current", 1)
        columns = []
        month = Regions.check_month(year, month_name)
        if month:
            try: month, week = Weeks.new_week_month(month, status)
            except: month = week = None
            if month and week:
                columns = Weeks.week_column(month, week)
                columns[0] = month.total_areas
                columns.insert(0, week)
            
        if columns:
            self.wk_nb.update(column=columns)
            
            header = self.header.get()
            
            if header == "default": header = "days"
            
            if header != "sole":
                area_sort = Chart_Sort(month, self.yaxis, header=header, week=week)
                area_sort.xlabel = header.title()
                area_sort.ylabel = "Records"
                area_sort.title = f"{header.title()} in {week} | {month}"
                if area_sort.go: self.plot_it(area_sort)
            
            else:
                sole_sort = Chart_Sort(month, self.yaxis, week=week)

                sole_sort.xlabel = "Records"
                sole_sort.ylabel = "Records"
                sole_sort.title = f"Records in {week} | {month}"
                if sole_sort.go: self.plot_it(sole_sort)

        else: show(title="Not found", msg="Previous Month not found", which="error")

    def dy_notice(self):
        status = self.status.get()
        month_name, year = Date.get_month("current", 1)
        columns = []
        month =  Regions.check_month(year, month_name)
        month, week = Weeks.new_week_month(month, "current")
        if month and week:
            if status == "current": status = 0
            elif status == "next": status = 1
            elif status == "previous": status = -1
            day = Date.date(status=status, form=1)
            if day:
                columns = Days.day_column(month, day)
                columns[0] = month.total_areas
                columns.insert(0, day)
            
        if columns:
            self.dy_nb.update(column=columns)

            header = self.header.get()
            
            # if header == "default": header = "areas"
            
            if header != "sole":
                area_sort = Chart_Sort(month, self.yaxis, header="areas", day=day)
                area_sort.xlabel = "Areas"
                area_sort.ylabel = "Records"
                area_sort.title = f"Areas in {day} | {week} | {month}"
                if area_sort.go: self.plot_it(area_sort)

            else:
                sole_sort = Chart_Sort(month, self.yaxis, day=day)
                sole_sort.xlabel = "Records"
                sole_sort.ylabel = "Records"
                sole_sort.title = f"Records in {day} | {week} | {month}"
                if sole_sort.go: self.plot_it(sole_sort)

        else: show(title="Not found", msg="Previous Month not found", which="error")

    def draw_charts(self):
        self.plot_canvas.draw()
        self.bar_canvas.draw()
    def plot_charts(self):
        if Years.years:
            for time in ["year", "month", "week", "day"]:
                self.time.set(time)
                self.notice()
            self.time.set("year")
        else: show('No data', 'No Data to plots', 'error')
    
    def plot_it(self, sort):
        charts = [self.plot, self.bar]

        xlabel = sort.xlabel
        ylabel = sort.ylabel
        title = sort.title

        xticks = sort.xticks
        ys = sort.ys
        labels = sort.labels

        for chart in charts:
            chart(xticks=xticks, ys=ys, labels=labels, grid=self.grid, xlabel=xlabel, ylabel=ylabel,title=title)

    def plot_figs(self):
        self.plot_canvas = Chart(master=self.plots_frame, relw=.492, relh=1)
        self.plot = self.plot_canvas.plot
        self.bar_canvas = Chart(master=self.plots_frame, relx=.495, relh=1, relw=.505)
        self.bar = self.bar_canvas.bar

    def style(self):
        self.config(highlightbackground=Styles.background, background=Styles.background, highlightcolor=Styles.foreground)
        # self.cover_frame.config(background=Styles.background)
        self.title.config(foreground=Styles.foreground, background=Styles.background, font=Fonts.font17b, relief="raised", bd="4")

        self.options.config(background=Styles.background)
        self.plots_frame.config(background="black")
        radiobuttons = [self.year_choose, self.month_choose, self.week_choose, self.day_choose, self.default_choose, self.area_choose, self.sole_choose, self.plot_btn, self.calc_btn, self.hm_ne_chkbtn, self.hm_cur_chkbtn, self.hm_pr_chkbtn]
        for radiobutton in radiobuttons: radiobutton.config(activebackground=Styles.background, activeforeground=Styles.foreground, background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor="white", justify="left", overrelief="ridge", relief="groove")

        self.yr_nb.style()
        self.mn_nb.style()
        self.wk_nb.style()
        self.dy_nb.style()
        
        
        self.rb_clicked()

    def rb_clicked(self):
        time = [self.year_choose, self.month_choose, self.week_choose, self.day_choose]
        header = [self.default_choose, self.area_choose, self.sole_choose]
        status = [self.hm_ne_chkbtn, self.hm_cur_chkbtn, self.hm_pr_chkbtn]
        buts = time + header + status
        
        for but in buts:
            var = self.time
            if but in header: var = self.header
            elif but in status: var = self.status
            val = but["value"]
            if var.get() == val: but["fg"] = "blue"
            else: but["fg"] = Styles.foreground

    def place_widgs(self):
        self.title.place(relx=0, rely=0, relh=.05, relw=1)
        self.frame.place(relx=.336, rely=.42, relh=.58, relw=.664)
        self.plots_frame.place(relx=.001, rely=.005, relh=.99, relw=.998)
        self.options.place(relx=0, rely=.8, relh=.2, relw=.335)
        self.year_choose.place(relx=.01, rely=.01, relh=.2, relw=.13)
        self.month_choose.place(relx=.15, rely=.01, relh=.2, relw=.15)
        self.week_choose.place(relx=.31, rely=.01, relh=.2, relw=.15)
        self.day_choose.place(relx=.47, rely=.01, relh=.2, relw=.15)
        self.default_choose.place(relx=.01, rely=.25, relh=.2, relw=.16)
        self.area_choose.place(relx=.18, rely=.25, relh=.2, relw=.13)
        self.sole_choose.place(relx=.32, rely=.25, relh=.2, relw=.13)
        
        self.calc_btn.place(relx=.1, rely=.5, relh=.2, relw=.15)
        self.plot_btn.place(relx=.3, rely=.5, relh=.2, relw=.15)
        
        self.hm_ne_chkbtn.place(relx=.75, rely=.15, relh=.2, relw=.2, bordermode="ignore")
        self.hm_cur_chkbtn.place(relx=.75, rely=.4, relh=.2, relw=.2, bordermode="ignore")
        self.hm_pr_chkbtn.place(relx=.75, rely=.65, relh=.2, relw=.2, bordermode="ignore")
        sls = [self.plot_canvas, self.bar_canvas, self.yr_nb, self.mn_nb, self.wk_nb, self.dy_nb]
        for a in sls: a.place_widgs()



