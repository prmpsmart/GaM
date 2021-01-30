from .packed import *

class ProperDetails(Frame, Thrift_Analysis):
    
    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)

      ############ Datas
        self.data_cbtn = tk.StringVar()

        data_lblfrm = LabelFrame(self, text=' Datas', place=dict(relx=.005, rely=.005, relw=.99, relh=.15))


        self.years_rb = Radiobutton(data_lblfrm,  text='Years', value='years', variable=self.data_cbtn, place=dict(relx=.01, rely=.005, relw=.3, relh=.45))

        self.months_rb = Radiobutton(data_lblfrm, text='Months', value='months', variable=self.data_cbtn, place=dict(relx=.345, rely=.005, relw=.3, relh=.45))

        self.areas_rb = Radiobutton(data_lblfrm,text='Areas', value='areas', variable=self.data_cbtn, place=dict(relx=.68, rely=.005, relw=.3, relh=.45))

        self.clients_rb = Radiobutton(data_lblfrm, text='Clients', value='clients', variable=self.data_cbtn, place=dict(relx=.01, rely=.5, relw=.3, relh=.45))

        self.weeks_rb = Radiobutton(data_lblfrm, text='Weeks', value='weeks', variable=self.data_cbtn, place=dict(relx=.345, rely=.5, relw=.3, relh=.45))

        self.days_rb = Radiobutton(data_lblfrm, text='Days', value='days', variable=self.data_cbtn, place=dict(relx=.68, rely=.5, relw=.3, relh=.45))

        self.setRadioGroups([self.years_rb, self.months_rb, self.areas_rb, self.clients_rb, self.weeks_rb, self.days_rb])


      ############## Get
        self.region_cbtn = tk.StringVar()

        get_lblfrm = LabelFrame(self, text='Get Details', place=dict(relx=.005, rely=.16, relw=.99, relh=.35))

        self.get_yr = RadioCombo(get_lblfrm, topKwargs=dict(text='Year', variable=self.region_cbtn, value='year'), func=self.get_year, place=dict(relx=.005, rely=.005, relh=.24, relw=.55), orient='h', longent=.36)

        self.get_mn = RadioCombo(get_lblfrm, topKwargs=dict(text='Month', variable=self.region_cbtn, value='month'), func=self.get_month, place=dict(relx=.005, rely=.25, relh=.24, relw=.55), orient='h', longent=.36)

        self.get_ar = RadioCombo(get_lblfrm,  topKwargs=dict(text='Area', variable=self.region_cbtn, value='area'), func=self.get_area, place=dict(relx=.005, rely=.5, relh=.24, relw=.55), orient='h', longent=.36)

        self.get_cl = RadioCombo(get_lblfrm, topKwargs=dict(text='Client', variable=self.region_cbtn, value='client'), func=self.get_client, place=dict(relx=.005, rely=.75, relh=.24, relw=.55), orient='h', longent=.36)

        self.setRadioGroups([self.get_yr, self.get_mn, self.get_ar, self.get_cl])

        self.get_wk = LabelCombo(get_lblfrm, topKwargs=dict(text='Week'), place=dict(relx=.62, rely=.005, relh=.45, relw=.36), func=self.get_week)

        self.get_dy = LabelCombo(get_lblfrm,  topKwargs=dict(text='Days'), place=dict(relx=.62, rely=.5, relh=.45, relw=.36), func=self.get_day)


        self.years_chkbtn = Radiobutton(self, text='ALL\nYears', value='years', variable=self.region_cbtn, place=dict())


      ############ Specific Datas
        self.spec_cbtn = StringVar()

        self.s_data_lblfrm = LabelFrame(self, text='Specific Datas', place=dict(relx=.005, rely=.515, relw=.99, relh=.3))


        self.s_d_month = RadioCombo(self.s_data_lblfrm, topKwargs=dict(text='Months', variable=self.spec_cbtn, value='spec_month'), place=dict(relx=.05, rely=.16, relh=.4, relw=.45), bottomKwargs=dict(values=MONTHS_NAMES[1:]), func=self.get_spec_month)

        self.s_d_week = RadioCombo(self.s_data_lblfrm, topKwargs=dict(text='Weeks', variable=self.spec_cbtn, value='spec_week'), place=dict(relx=.05, rely=.57, relh=.4, relw=.45), bottomKwargs=dict(values=WEEKS), func=self.get_spec_week)

        self.s_d_day = RadioCombo(self.s_data_lblfrm, topKwargs=dict(text='Days', variable=self.spec_cbtn, value='spec_day'), place=dict(relx=.55, rely=.16, relh=.4, relw=.4), bottomKwargs=dict(values=DAYS_NAMES), func=self.get_spec_day)

        self.s_d_area = RadioCombo(self.s_data_lblfrm, topKwargs=dict(text='Areas', variable=self.spec_cbtn, value='spec_area'),  place=dict(relx=.55, rely=.57, relh=.4, relw=.4), bordermode='ignore', func=self.get_spec_area)

        self.setRadioGroups([self.s_d_month, self.s_d_week, self.s_d_day, self.s_d_area])



