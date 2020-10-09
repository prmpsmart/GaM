
from ..decorate.styles import Fonts, Styles

from tkinter import LabelFrame, Label
from .....backend.thrift.regions.years import Years
from .....backend.thrift.regions.year import Year
from .....backend.thrift.regions.month import Month
from .....backend.thrift.regions.area import Area
from .....backend.thrift.regions.client import Client
from .....backend.utils.details.tdetails import TDetails
from .....backend.utils.sort.thrift.smalling import Smalling


class Small_Details(LabelFrame):
    go = 1
    def __init__(self, master, relx=.206, rely=.4, relh=.6, relw=.18):
        super().__init__(master, text='''Details''')
        self.relx, self.rely, self.relh, self.relw = relx, rely, relh, relw

        self.time_lbl = Label(self,  text='''Time''')

        self.name_lbl = Label(self, text='''Name''')
        
        self.brf_memb_lbl = Label(self)

        self.rt_brf_lbl = Label(self)
        
        self.thf_comm_lbl = Label(self)
        
        self.sav_lbl = Label(self, text='''Savings''')
        
        self.deb_lbl = Label(self, text='''Debits''')        
        
        self.not_paid_lbl = Label(self, text='''Not-Paids''')
        
        self.upf_lbl = Label(self, text='''Upfronts''')
        

        self.pupf_lbl = Label(self, text='''P-Upfronts''')
        
        

        self.rupf_lbl = Label(self, text='''R-Upfronts''')
        

        self.bal_lbl = Label(self, text='''Balances''')
        
        
        self.def_lbl = Label(self, text='''Deficits''')
        
        
        self.exc_lbl = Label(self, text='''Excesses''')
        
        
        self.bto_lbl = Label(self, text='''B-T-Os''')
        
        
        ###################

        self.time_lbl_show = Label(self, text="Month | Week | Day")
        

        self.name_lbl_show = Label(self, text="Apata Miracle Peter")
        

        self.brf_memb_lbl_show = Label(self)
        

        self.rt_brf_lbl_show = Label(self)
        

        self.thf_comm_lbl_show = Label(self)
        

        self.sav_lbl_show = Label(self)
        

        self.deb_lbl_show = Label(self)
        

        self.not_paid_lbl_show = Label(self)
        

        self.upf_lbl_show = Label(self)
        

        self.pupf_lbl_show = Label(self)
        

        self.rupf_lbl_show = Label(self)
        

        self.bal_lbl_show = Label(self)
        
        
        self.def_lbl_show = Label(self)
        
        
        self.exc_lbl_show = Label(self)
        

        self.bto_lbl_show = Label(self)
        
        
        self.style()

    def show(self, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen=0, fourteen=0, fifteen=0):
        lists = [one, two[0], two[1], three[0], three[1], four[0], four[1], five[0], five[1], six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen]
        TDetails.mul_1000s(lists)
        
        self.time_lbl_show.config(text=lists[0])
        self.name_lbl.config(text=lists[1])
        self.name_lbl_show.config(text=lists[2])
        self.brf_memb_lbl.config(text=lists[3])
        self.brf_memb_lbl_show.config(text=lists[4])
        self.rt_brf_lbl.config(text=lists[5])
        self.rt_brf_lbl_show.config(text=lists[6])
        self.thf_comm_lbl.config(text=lists[7])
        self.thf_comm_lbl_show.config(text=lists[8])
        self.sav_lbl_show.config(text=lists[9])
        self.deb_lbl_show.config(text=lists[10])
        self.not_paid_lbl_show.config(text=lists[11])
        self.upf_lbl_show.config(text=lists[12])
        self.pupf_lbl_show.config(text=lists[13])
        self.rupf_lbl_show.config(text=lists[14])
        self.bal_lbl_show.config(text=lists[15])
        self.def_lbl_show.config(text=lists[16])
        self.exc_lbl_show.config(text=lists[17])
        self.bto_lbl_show.config(text=lists[18])
    
    def thrift_update(self, region=None, week=None, day=None, month=None):
        columns = Smalling.thrift_small(region=region, week=week, day=day, month=month)
        if columns: self.show(*columns)
    
    def style(self):
        self.config(relief='groove', font=Fonts.font14b, foreground=Styles.foreground, background=Styles.background, highlightbackground="black", highlightcolor=Styles.foreground)
        small = [self.thf_comm_lbl, self.rupf_lbl]
        Fonts.font15_lbl = [self.time_lbl,  self.rt_brf_lbl, self.sav_lbl, self.not_paid_lbl, self.bal_lbl, self.bto_lbl, self.thf_comm_lbl]
        reds = [self.upf_lbl_show, self.pupf_lbl_show, self.def_lbl_show, self.exc_lbl_show, self.deb_lbl_show, ]
        redlbls = [self.upf_lbl, self.pupf_lbl, self.def_lbl, self.exc_lbl, self.deb_lbl]
        Fonts.font22_lbl = [self.brf_memb_lbl, self.name_lbl]
        labels_shows = [self.time_lbl_show, self.name_lbl_show, self.bal_lbl_show, self.rt_brf_lbl_show, self.exc_lbl_show, self.bto_lbl_show, self.thf_comm_lbl_show, self.sav_lbl_show, self.not_paid_lbl_show, self.brf_memb_lbl_show, self.rupf_lbl_show, ]
        
        lbls = Fonts.font15_lbl + Fonts.font22_lbl + reds + redlbls + Fonts.font22_lbl + labels_shows + small


        
        
        for lbl in lbls:
            bd = None
            fg = Styles.foreground
            bg = Styles.background
            relief="ridge"
            if lbl in redlbls:
                Fonts.font = Fonts.font15b
                fg = Styles.showred
            if lbl in reds:
                Fonts.font = Fonts.font22b
                if lbl == self.pupf_lbl: Fonts.font = Fonts.font11b
                fg = Styles.showred
                bg = Styles.showbg
                relief = 'sunken'
                bd = '4'
            if lbl in labels_shows:
                Fonts.font = Fonts.font22b
                fg = "black"
                bg = Styles.showbg
                relief = 'sunken'
                bd = '4'
            if lbl in small: Fonts.font = Fonts.font14b
            if lbl in Fonts.font15_lbl: Fonts.font = Fonts.font15b
                

            lbl.config(activebackground=Styles.background, activeforeground="black", background=bg, borderwidth=bd, disabledforeground=Styles.foreground, font=Fonts.font, foreground=fg, highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief=relief)

    def place_widgs(self):
        self.place(relx=self.relx, rely=self.rely, relh=self.relh, relw=self.relw)
        self.time_lbl.place(relx=.02, rely=.06, relh=.055, relw=.3, bordermode='ignore')
        self.name_lbl.place(relx=.02, rely=.1226, relh=.055, relw=.3, bordermode='ignore')
        self.brf_memb_lbl.place(relx=.02, rely=.185, relh=.055, relw=.46, bordermode='ignore')
        self.rt_brf_lbl.place(relx=.02, rely=.248, relh=.055, relw=.46, bordermode='ignore')
        self.thf_comm_lbl.place(relx=.02, rely=.3106, relh=.055, relw=.46, bordermode='ignore')
        self.sav_lbl.place(relx=.02, rely=.373, relh=.055, relw=.46, bordermode='ignore')
        self.deb_lbl.place(relx=.02, rely=.436, relh=.055, relw=.46, bordermode='ignore')
        self.not_paid_lbl.place(relx=.02, rely=.4986, relh=.055, relw=.46, bordermode='ignore')
        self.upf_lbl.place(relx=.02, rely=.561, relh=.055, relw=.46, bordermode='ignore')
        self.pupf_lbl.place(relx=.02, rely=.624, relh=.055, relw=.46, bordermode='ignore')
        self.rupf_lbl.place(relx=.02, rely=.686, relh=.055, relw=.46, bordermode='ignore')
        self.bal_lbl.place(relx=.02, rely=.749, relh=.055, relw=.46, bordermode='ignore')
        self.def_lbl.place(relx=.02, rely=.812, relh=.055, relw=.46, bordermode='ignore')
        self.exc_lbl.place(relx=.02, rely=.874, relh=.055, relw=.46, bordermode='ignore')
        self.bto_lbl.place(relx=.02, rely=.937, relh=.055, relw=.46, bordermode='ignore')
        self.time_lbl_show.place(relx=.315, rely=.06, relh=.055, relw=.67, bordermode='ignore')
        self.name_lbl_show.place(relx=.315, rely=.1226, relh=.055, relw=.67, bordermode='ignore')
        self.brf_memb_lbl_show.place(relx=.485, rely=.185, relh=.055, relw=.5, bordermode='ignore')
        self.rt_brf_lbl_show.place(relx=.485, rely=.248, relh=.055, relw=.5, bordermode='ignore')
        self.thf_comm_lbl_show.place(relx=.485, rely=.3106, relh=.055, relw=.5, bordermode='ignore')
        self.sav_lbl_show.place(relx=.485, rely=.373, relh=.055, relw=.5, bordermode='ignore')
        self.deb_lbl_show.place(relx=.485, rely=.436, relh=.055, relw=.5, bordermode='ignore')
        self.not_paid_lbl_show.place(relx=.485, rely=.4986, relh=.055, relw=.5, bordermode='ignore')
        self.upf_lbl_show.place(relx=.485, rely=.561, relh=.055, relw=.5, bordermode='ignore')
        self.pupf_lbl_show.place(relx=.485, rely=.624, relh=.055, relw=.5, bordermode='ignore')
        self.rupf_lbl_show.place(relx=.485, rely=.686, relh=.055, relw=.5, bordermode='ignore')
        self.bal_lbl_show.place(relx=.485, rely=.749, relh=.055, relw=.5, bordermode='ignore')
        self.def_lbl_show.place(relx=.485, rely=.812, relh=.055, relw=.5, bordermode='ignore')
        self.exc_lbl_show.place(relx=.485, rely=.874, relh=.055, relw=.5, bordermode='ignore')
        self.bto_lbl_show.place(relx=.485, rely=.937, relh=.055, relw=.5, bordermode='ignore')




