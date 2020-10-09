from tkinter import Frame
from tkinter.ttk import Notebook
from ..utils.widgets import ScrolledTreeView
from ..utils.widgets.debug import Out_Message, show
from ....backend.thrift import YEARS
from ....backend.utils.details.tdetails import TDetails
from ....backend.utils.sort.thrift.regions import Regions
from ....backend.utils.threads import Threads
from ..utils.visuals.small import Small_Details, Styles
from ..utils.visuals.table import Table
from ..utils.visuals.chart import Chart
from .details_tabs import Thrift_Analysis, Daily_Input, Thrift_Update

class Thrift_Details(Notebook):
    go = 0
    def __init__(self, master):
        super().__init__(master)
        # Daily Thrift Detail
        self.details_note = Notebook(self, takefocus="")
        
        self.details_note.enable_traversal()
        
        # Daily Thrift Visual
        self.visuals_note = Notebook(self, takefocus="")
        

        self.scroll_confirm = 0
        self.init = 1
        
        self.analysis_note = Notebook(self.details_note, takefocus="")
        
        # Children
        ################## Output
        self.out_message = Out_Message(self, relw=.207, rely=.8, relx=.0015, relh=.21)
        self.out_message.config(text="")
        ############ Small Details
        self.small_details = Small_Details(self)
        
        self._visuals_note()
        self._analysis_note()
        self.style()

        
    def _visuals_note(self):
        self.table_tab = Frame(self.visuals_note, takefocus="")

        self.visuals_note.add(self.table_tab, padding=1)
        self.visuals_note.tab(0, text="Thrift Tables",compound="left",underline="0")
        
       # Daily Thrift Plots
        self.plots_frame = Frame(self.visuals_note, takefocus="")
        self.visuals_note.add(self.plots_frame, padding=1)
        self.visuals_note.tab(1, text="Thrift Plots",compound="left",underline="0")
        
        self.visuals_set()

    def _analysis_note(self):
       # Daily Thrift Input
        self.daily_input =  Daily_Input(self.analysis_note, self.small_details, self.full_details, self.details_output, takefocus="")
        self.analysis_note.add(self.daily_input, padding=1)
        self.analysis_note.tab(0, text="Daily Thrift Input",compound="left",underline="0")
        
       # Thrift Analysis
        Thrift_Analysis.plots_figures = self.plots_figures
        self.thrift_analysis = Thrift_Analysis(self.analysis_note, self.small_details, self.full_details, self.details_output, takefocus="")
        self.analysis_note.add(self.thrift_analysis, padding=1)
        self.analysis_note.tab(1, text="Thrift Analysis",compound="left",underline="0")
        
       # Thrift Update
        self.thrift_update = Thrift_Update(self.analysis_note, self.small_details, self.full_details, self.details_output, takefocus="")
        self.analysis_note.add(self.thrift_update, padding=1)
        self.analysis_note.tab(2, text="Thrift Update",compound="left",underline="0")

    def visuals_set(self):
        self.table = Table(self.table_tab, "months")
        self.fig1 = Chart(master=self.plots_frame, relw=.492)
        self.fig2 = Chart(master=self.plots_frame, rely=.505, relw=.492)
        self.fig3 = Chart(master=self.plots_frame, relx=.495)
        self.fig4 = Chart(master=self.plots_frame, relx=.495, rely=.505)
        self.plots_figures = [self.fig1, self.fig2, self.fig3, self.fig4]

    def draw_charts(self):
        for fig in self.plots_figures: fig.draw()

    def full_details(self, title='', region=None, header='', week='', day='', month='', spec='', area='', refresh=False, daily=''):
        self.table.thrift_update(title=title, header=header, region=region, month=month, week=week, day=day, spec=spec, area=area, refresh=refresh, daily=daily)
        Threads.save_other_datas()

    def details_output(self, msg, which=None, title=None):
        self.out_message.set_message(msg)
        if which and title: show(title, msg, which)

    def style(self):
        self.daily_input.style()
        self.thrift_analysis.style()
        self.thrift_update.style()
        self.table.style()
        self.out_message.style()
        self.small_details.style()

    def place_widgs(self):
        self.details_note.place(relx=0, rely=0, relh=.81, relw=.389)
        self.visuals_note.place(relx=.389, rely=0, relh=1, relw=.62)
        self.analysis_note.place(relx=0, rely=0, relh=1, relw=1)
        self.daily_input.place_widgs()
        self.thrift_analysis.place_widgs()
        self.thrift_update.place_widgs()
        self.table.place_widgs()
        self.out_message.place_widgs()
        self.small_details.place_widgs()
        
        for a in self.plots_figures: a.place_widgs()


