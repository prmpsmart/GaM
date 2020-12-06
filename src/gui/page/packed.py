from ..core.prmp_gui.extensions import *
from ..dc.dc_extensions import *
from ..core.agam_extensions import *



class Small:
    def __init__(self, top=None):
        self.datetime = DateTimeView(top)
        self.datetime.place(relx=.005, rely=.01, relh=.1, relw=.99)

        self.dc = DC_Overview(top)
        self.dc.place(relx=.005, rely=.115, relh=.88, relw=.99)
        self.fillDCDigits = self.dc.fillDCDigits






class New:
    def __init__(self, top=None):
        # font9 = "-family {Times New Roman} -size 11 -weight bold -slant roman -underline 0 -overstrike 0"

        self.Labelframe1 = OfficeDetails(top, text='DC Office Details', place=dict(relx=.005, rely=.005, relh=.226, relw=.468))


        self.Labelframe2 = MonthBox(top, place=dict(relx=.503, rely=.005, relh=.28, relw=.47))

        self.Labelframe3 = AccountHighlight(top, text='DC Account Highlight', place=dict(relx=.0, rely=.397, relh=.587, relw=.997))









