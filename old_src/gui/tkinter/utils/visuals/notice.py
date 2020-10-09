
from ..decorate.styles import Fonts, Styles
from tkinter import LabelFrame, Label
from .....backend.utils.details.tdetails import TDetails




class Notice(LabelFrame):
    
    def __init__(self, master, relx=0, rely=0, relh=1, relw=1, variable=None, command=None, text=None, text1=None):
        self.master = master
        super().__init__(self.master, text=text)
        self.relx, self.rely, self.relh, self.relw = relx, rely, relh, relw

        self.nb_ars_lbl = Label(self, text=text1 or "Areas")
        

        self.nb_cls_lbl = Label(self, text="""Clients""")
        
        
        self.nb_brfs_lbl = Label(self, text="""Brought-Fs""")
        


        self.nb_debs_lbl = Label(self, text="""Debits""")
        
        
        self.nb_upfs_lbl = Label(self, text="""Upfronts""")
        
        
        self.nb_pupfs_lbl = Label(self, text="""P-Upfronts""")
        
        
        self.nb_defs_lbl = Label(self, text="""Deficits""")
        

        self.nb_excs_lbl = Label(self, text="Excesses")
        
        
        ###################

        self.nb_ars_lbl_show = Label(self)
        

        self.nb_cls_lbl_show = Label(self)
        

        self.nb_brfs_lbl_show = Label(self)
        

        self.nb_debs_lbl_show = Label(self)
        

        self.nb_upfs_lbl_show = Label(self)
        

        self.nb_pupfs_lbl_show = Label(self)
        


        self.nb_defs_lbl_show = Label(self)
        

        self.nb_excs_lbl_show = Label(self)
        
    
     ##########################
     ##########################

        self.nb_sav_lbl = Label(self, text="""Savings""")
        
        
        self.nb_rupfs_lbl = Label(self, text="""R-Upfronts""")
        

        self.nb_coms_lbl = Label(self, text="""Commission""")
        
        
        self.nb_btos_lbl = Label(self, text="""B-T-Os""")
        

        self.nb_not_paids_lbl = Label(self, text="""Not_Paids""")
        
        
        self.nb_bals_lbl = Label(self, text="""Balances""")
        
        
        ##################
        
        self.nb_savs_lbl_show = Label(self)
        
        
        self.nb_rupfs_lbl_show = Label(self)
        

        self.nb_coms_lbl_show = Label(self)
        
        
        self.nb_btos_lbl_show = Label(self)
        
        
        self.nb_not_paids_lbl_show = Label(self)
        
        
        self.nb_bals_lbl_show = Label(self)
        
        
     ##########################
        
        self.nb_lbl = Label(self)
        self.nb_lbl.place(relx=.48, rely=.07, relh=.2, relw=.51, bordermode="ignore")

        
        
        self.style()

    def update(self, yr=None, region=None, column=None):
        if region:
            column = region.datas()
            if yr: column[1] = yr
        self.show(column)
        
    def show(self, cols):
        mul_1000s = TDetails.mul_1000s
        if cols:
            mul_1000s(cols)
            self.nb_lbl.config(text=cols[0])
            self.nb_ars_lbl_show.config(text=cols[1])
            self.nb_cls_lbl_show.config(text=cols[2])
            self.nb_brfs_lbl_show.config(text=cols[3])
            self.nb_coms_lbl_show.config(text=cols[4])
            self.nb_savs_lbl_show.config(text=cols[5])
            self.nb_debs_lbl_show.config(text=cols[6])
            self.nb_not_paids_lbl_show.config(text=cols[7])
            self.nb_upfs_lbl_show.config(text=cols[8])
            self.nb_pupfs_lbl_show.config(text=cols[9])
            self.nb_rupfs_lbl_show.config(text=cols[10])
            self.nb_bals_lbl_show.config(text=cols[11])
            self.nb_defs_lbl_show.config(text=cols[12])
            self.nb_excs_lbl_show.config(text=cols[13])
            self.nb_btos_lbl_show.config(text=cols[14])

        else:
            a = "NAN"
            lbls = [self.nb_ars_lbl_show, self.nb_cls_lbl_show, self.nb_savs_lbl_show, self.nb_debs_lbl_show, self.nb_upfs_lbl_show, self.nb_bals_lbl_show, self.nb_coms_lbl_show, self.nb_brfs_lbl_show, self.nb_lbl, self.nb_defs_lbl_show, self.nb_btos_lbl_show, self.nb_excs_lbl_show, self.nb_not_paids_lbl_show]
            for lbl in lbls: lbl.config(text=a)
    

    def style(self):
        self.config(relief="groove", font=Fonts.font11b, foreground=Styles.foreground, background=Styles.background, highlightbackground=Styles.background, highlightcolor=Styles.foreground)
        
        
        lbls = [self.nb_ars_lbl, self.nb_cls_lbl, self.nb_brfs_lbl]
        for lbl in lbls: lbl.config( activebackground=Styles.background, activeforeground=Styles.foreground, background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief="groove")
        
        lbls_show = [self.nb_ars_lbl_show, self.nb_cls_lbl_show, self.nb_brfs_lbl_show]
        for lblshow in lbls_show: lblshow.config(activebackground=Styles.background, activeforeground=Styles.foreground, background=Styles.showbg, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.showfg, highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief="sunken")
        
        self.nb_lbl.config(background=Styles.higbg, borderwidth="2", disabledforeground=Styles.foreground, font=Fonts.font17b, foreground=Styles.higfg, relief="groove")
        
        sol14 = [self.nb_savs_lbl_show, self.nb_rupfs_lbl_show, self.nb_coms_lbl_show, self.nb_bals_lbl_show, self.nb_btos_lbl_show, self.nb_not_paids_lbl_show]
        for so14 in sol14: so14.config(background=Styles.showbg, borderwidth="3", disabledforeground=Styles.foreground, font=Fonts.font14, foreground=Styles.showfg, relief="solid")

        
        bigs = [self.nb_coms_lbl, self.nb_sav_lbl, self.nb_bals_lbl, self.nb_btos_lbl, self.nb_rupfs_lbl, self.nb_not_paids_lbl]
        for big in bigs:
            Fonts.font = Fonts.font14
            # if big == self.nb_rupfs_lbl: Fonts.font = Fonts.font10b
            big.config(activebackground=Styles.background, activeforeground=Styles.foreground, background="green", disabledforeground=Styles.foreground, font=Fonts.font, foreground="white", highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief="solid", )

        reds = [self.nb_upfs_lbl, self.nb_pupfs_lbl, self.nb_debs_lbl, self.nb_defs_lbl, self.nb_excs_lbl]
        for red in reds:
            Fonts.font = Fonts.font11b
            # if red == self.nb_pupfs_lbl: Fonts.font = Fonts.font9
            red.config(activebackground=Styles.background, activeforeground=Styles.foreground, background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font, foreground=Styles.showred, highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief="groove")
        
        
        reds_shows = [self.nb_debs_lbl_show, self.nb_upfs_lbl_show, self.nb_pupfs_lbl_show, self.nb_defs_lbl_show, self.nb_excs_lbl_show]
        for red_show in reds_shows: red_show.config(activebackground=Styles.background, activeforeground=Styles.foreground, background=Styles.showbg, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.showred, highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief="sunken")
    
    def place_widgs(self):
        self.place(relx=self.relx, rely=self.rely, relh=self.relh, relw=self.relw)
        self.nb_ars_lbl.place(relx=.015, rely=.07, relh=.1, relw=.2, bordermode="ignore")
        self.nb_cls_lbl.place(relx=.015, rely=.185, relh=.1, relw=.2, bordermode="ignore")
        self.nb_brfs_lbl.place(relx=.015, rely=.3, relh=.1, relw=.2, bordermode="ignore")
        self.nb_debs_lbl.place(relx=.015, rely=.415, relh=.1, relw=.21, bordermode="ignore")
        self.nb_upfs_lbl.place(relx=.015, rely=.53, relh=.1, relw=.21, bordermode="ignore")
        self.nb_pupfs_lbl.place(relx=.015, rely=.645, relh=.1, relw=.21, bordermode="ignore")
        self.nb_defs_lbl.place(relx=.015, rely=.76, relh=.1, relw=.21, bordermode="ignore")
        self.nb_excs_lbl.place(relx=.015, rely=.88, relh=.1, relw=.21, bordermode="ignore")
        self.nb_ars_lbl_show.place(relx=.23, rely=.07, relh=.1, relw=.21, bordermode="ignore")
        self.nb_cls_lbl_show.place(relx=.23, rely=.185, relh=.1, relw=.21, bordermode="ignore")
        self.nb_brfs_lbl_show.place(relx=.23, rely=.3, relh=.1, relw=.21,bordermode="ignore")
        self.nb_debs_lbl_show.place(relx=.23, rely=.415, relh=.1, relw=.21, bordermode="ignore")
        self.nb_upfs_lbl_show.place(relx=.23, rely=.53, relh=.1, relw=.21, bordermode="ignore")
        self.nb_pupfs_lbl_show.place(relx=.23, rely=.645, relh=.1, relw=.21, bordermode="ignore")
        self.nb_defs_lbl_show.place(relx=.23, rely=.76, relh=.1, relw=.21, bordermode="ignore")
        self.nb_excs_lbl_show.place(relx=.23, rely=.88, relh=.1, relw=.21, bordermode="ignore")
        self.nb_sav_lbl.place(relx=.48, rely=.3, relh=.1, relw=.25, bordermode="ignore")
        self.nb_rupfs_lbl.place(relx=.48, rely=.415, relh=.1, relw=.25, bordermode="ignore")
        self.nb_coms_lbl.place(relx=.48, rely=.53, relh=.1, relw=.25, bordermode="ignore")
        self.nb_btos_lbl.place(relx=.48, rely=.645, relh=.1, relw=.25, bordermode="ignore")
        self.nb_not_paids_lbl.place(relx=.48, rely=.76, relh=.1, relw=.25, bordermode="ignore")
        self.nb_bals_lbl.place(relx=.48, rely=.88, relh=.1, relw=.25, bordermode="ignore")
        self.nb_savs_lbl_show.place(relx=.74, rely=.3, relh=.1, relw=.25, bordermode="ignore")
        self.nb_rupfs_lbl_show.place(relx=.74, rely=.415, relh=.1, relw=.25, bordermode="ignore")
        self.nb_coms_lbl_show.place(relx=.74, rely=.53, relh=.1, relw=.25, bordermode="ignore")
        self.nb_btos_lbl_show.place(relx=.74, rely=.645, relh=.1, relw=.25, bordermode="ignore")
        self.nb_not_paids_lbl_show.place(relx=.74, rely=.76, relh=.1, relw=.25, bordermode="ignore")
        self.nb_bals_lbl_show.place(relx=.74, rely=.88, relh=.1, relw=.25, bordermode="ignore")



