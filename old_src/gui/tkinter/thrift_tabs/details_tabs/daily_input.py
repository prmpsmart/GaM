
from ...utils.decorate.styles import Fonts
from tkinter import Button, Frame, StringVar, Menu
from tkinter.ttk import Menubutton
from ...utils.widgets.debug import show, confirm
from ...utils.widgets.admin_req import make_change
from ...utils.widgets.twowidgets import LabelCombo, LabelEntry, CheckCombo, CheckEntry, TwoWidgets, Label, LabelFrame, Radiobutton, Entry, Checkbutton, Styles
from .....backend.utils.sort.date import Date
from .....backend.utils.sort.thrift.regions import Regions
from .....backend.utils.create.tcreate import TCreate
from .....backend.utils.data.tdata import TData
from .....backend.utils.threads import Threads
from .....backend.thrift.daily.saving_daily import Saving_Daily

class Daily_Input(Frame):
    
    def __init__(self, master, small_details, full_details, details_output, **kw):
        super().__init__(master, **kw)
        
       #### General Widgets
        self.small_details = small_details
        self.full_details = full_details
        self.details_output = details_output
        
        
        self.daily_ready_cbtn = StringVar()
        self.daily_update1_cbtn = StringVar()
        self.daily_update2_cbtn = StringVar()
        self.daily_update3_cbtn = StringVar()
        self.daily_status = StringVar()
        self.area_cbtn = StringVar()
        
        self.thrift_cbtn = StringVar()
        self.debit_cbtn = StringVar()
        # self.daily_status.set("current")
        
        self.daily_input_pane = LabelFrame(self)
        
       ##### Month
        self.month_lbl = Label(self.daily_input_pane, text="Month")

       ##### Area
        self.area_lbl = Label(self.daily_input_pane, text="Area")
        
        
       ##### Client
        self.client_lbl = Label(self.daily_input_pane, text="Client")
        
        
       ##### Month Radiobuttons
        self.current_mn_rb = Radiobutton(self.daily_input_pane, text="Current\nMonth", value="current", variable=self.daily_status, command=self.get_month)
        

        self.next_mn_rb = Radiobutton(self.daily_input_pane, text="Next\nMonth", value="next", variable=self.daily_status, command=self.get_month)
        
       
       ##### Areas Name
        self.ar_lblcb = CheckCombo(self.daily_input_pane, text=" Area", func=self.get_area, relx=.02, rely=.18, relh=.06, relw=.31, bordermode="ignore", orient="h", variable=self.area_cbtn)

       ##### Clients 
        self.cl_lblcb = LabelCombo(self.daily_input_pane,  text="Client", func=self.get_client, relx=.02, rely=.25, relh=.06, relw=.31, bordermode="ignore", orient="h")

       ##### Thrift
        self.thrift_daily_lblcb = CheckEntry(self.daily_input_pane, variable=self.thrift_cbtn,  text="Thrift", relx=.02, rely=.32, relh=.06, relw=.31, bordermode="ignore", orient="h")

       ##### Debit
        self.debit_daily_lblcb = CheckEntry(self.daily_input_pane, variable=self.debit_cbtn, text="Debit", relx=.02, rely=.39, relh=.06, relw=.31, bordermode="ignore", orient="h")

       ####### Brought to office
        self.edb = LabelFrame(self.daily_input_pane,  text="Brougth To Office")
        

        self.bto_lblent = LabelEntry(self.edb, highlightcolor=Styles.foreground, relief="groove", text="B-T-O", relx=.02, rely=.1, relh=.8, relw=.62, bordermode="ignore")

        self.add_edb_btn = Button(self.edb, text="Add to\n Area", command=self.bto)
        

       ####### Delete Input
        self.delete_daily_thrift = LabelFrame(self.daily_input_pane, text="Delete Daily  Input")
        
        
        self.daily_del_ent = Entry(self.delete_daily_thrift, takefocus="")
        
        
        self.delete_daily_btn = Button(self.delete_daily_thrift, text="Delete", command=self.delete_input)
        
       
       ##### Ready and Add buttons

        self.daily_ready = Checkbutton(self.daily_input_pane,text="READY", variable=self.daily_ready_cbtn, command=self.cb_clicked)
        

        self.daily_add_btn = Button(self.daily_input_pane, text="ADD", command=self.add_daily)
        
        
       ###### Search by date and area
        self.search_lblfrm = LabelFrame(self.daily_input_pane, text="Search Daily Input by Dates")
        
        
        self.areas_box = LabelCombo(self.search_lblfrm, highlightcolor=Styles.foreground, relief="groove", values=sorted(Saving_Daily.area_dailies_names), text="Area", func=self.get_search_area_daily, relx=.04, rely=.04, relh=.4, relw=.7, bordermode="ignore", orient="h")
        
        self.dates_box = LabelCombo(self.search_lblfrm, highlightcolor=Styles.foreground, relief="groove", text="Date", bordermode="ignore", relx=.04, rely=.55, relh=.4, relw=.7, orient="h")

        self.search_menu = Menu(self.search_lblfrm, tearoff=0)

        self.search_list = Menubutton(self.search_lblfrm, menu=self.search_menu, text="Dailies")
        
        
        self.search_btn = Button(self.search_lblfrm, text="Search", command=self.search_dates)
        
        
       ########### 3 Update Check Buttons and Update and Tip
        self.update_daily_thrift = LabelFrame(self.daily_input_pane, text="Daily Thrifts Update Clients")
        

        self.daily_tip = Label(self.update_daily_thrift, text="Check all buttons\nbelow to update\nthe affected clients.")
        
        
        self.daily_update_btn = Button(self.update_daily_thrift, text="Update the clients", command=self.update_regions)
        
        
        self.up_daily_1 = Checkbutton(self.update_daily_thrift,  variable=self.daily_update1_cbtn, command=self.cb_clicked)
        

        self.up_daily_2 = Checkbutton(self.update_daily_thrift, variable=self.daily_update2_cbtn, command=self.cb_clicked)
        

        self.up_daily_3 = Checkbutton(self.update_daily_thrift, variable=self.daily_update3_cbtn, command=self.cb_clicked)
        
        
        self.daily = None
        self.area_daily = None
        self.search_area_daily = None
        self.area = None
        self.client = None
        self.month = None
        
        
        self.daily_input_reset()
        self.style()
        
        # self.get_month()

    def daily_input_reset(self):
        self.daily_status.set("current")
        self.daily_ready_cbtn.set(" ")
        self.daily_update1_cbtn.set(" ")
        self.daily_update2_cbtn.set(" ")
        self.daily_update3_cbtn.set(" ")
        self.area_cbtn.set(" ")
        self.thrift_cbtn.set(" ")
        self.debit_cbtn.set(" ")

    def get_month(self):
        self.rb_clicked()
        self.search_areas_put()
        status = self.daily_status.get()
        self.area = self.client = None
        if status in ["current", "next"]: 
            month_name, year = Date.get_month(status, 1)
            self.month =  Regions.check_month(year, month_name)
            if self.month:
                self.month_lbl.config(text=self.month)
                self.ar_lblcb.set(self.month.areas_names)
                self.get_small_details(title=self.month, region =self.month)
            else: show("Not found", "No month is found", "error")
    def get_area(self, *args):
        if self.month:
            self.client = None
            self.area = [area for area in self.month.areas if area.name == self.ar_lblcb.get()][0]
            self.area_lbl.config(text=self.area)
            
            self.area_daily = self.get_area_daily()

            clients = [client.name for client in self.area.clients]
            Regions.number_name(clients)
            self.cl_lblcb.set(values=clients)
            
            self.get_small_details(title=self.area, region=self.area)
            self.update_table()

    def get_client(self, *args):
        if self.area:
            self.client = [client for client in self.area.clients if client.name == self.cl_lblcb.get().split(". ")[1]][0]
            self.client_lbl.config(text=self.client)
            self.get_small_details(region=self.client)

    def get_small_details(self, title=None, region=None, day=None):
        self.small_details.thrift_update(region=region, day=day)
        if region.which != "client": self.full_details(header="daily", title=region)
        self.details_output(region)

    def update_table(self, daily=None):
        if daily: self.daily = daily
        else: daily = self.get_daily()
        if daily: self.full_details(title=daily, header="daily", daily=daily, region=daily.area)
        
    def update_regions(self): make_change(self._update_regions)

    def _update_regions(self):
        if self.daily_update1_cbtn.get() == "1" and self.daily_update2_cbtn.get() == "1" and self.daily_update3_cbtn.get() == "1":
            if self.daily:
                
                if not self.daily.area_updated: show(title="Not Updated", msg="The Area of this Daily has not been Updated", which="warn")
                if not self.daily.client_updated: show("Not Updated", "The Clients of this Daily has not been Updated", which="warn")
                
                if self.daily.updated: show(title="Updated", msg="This Daily has been Updated", which="info")
                
                else:
                    if confirm(title="Confirm update", msg="Are you sure you want to updates the clients and area bto", num=1):
                        self.daily.update()
                        Threads.save_current()
                        # Threads.save_data()
            else: show(title="Error", msg="No daily selected", which="warn")
        else: show(title="Confirm", msg="Check all three buttons", which="warn")

    def add_daily(self):
        thf, deb = self.thrift_cbtn.get(), self.debit_cbtn.get()
        go = thrift = debit = 0
        
        if self.area and self.client:
            self.get_daily()
            if thf == "1" and deb == "1":
                try:
                    thrift = int(self.thrift_daily_lblcb.get())
                    debit = int(self.debit_daily_lblcb.get())
                    if self.client.addable("thrift", thrift) == 1 and self.client.addable("debit", debit) == 1: go = 1
                    else:
                        show(title="Thrift and/ or Debit", msg="Thrift or Debit is incorrect", which="error")
                        go = 2
                except Exception as e: show(title="Incorrect input", msg="Thrift and Debit must be numberic", which="error"); go = 2; print(e)
            
            elif thf == "1":
                try:
                    thrift = int(self.thrift_daily_lblcb.get())
                    if self.client.addable("thrift", thrift) == 1: go = 1
                    else:
                        show(title="Thrift", msg="Thrift is incorrect", which="error")
                        go = 2
                except Exception as e: show(title="Incorrect input", msg="Thrift must be numberic", which="error"); go = 2; print(e)
            elif deb == "1":
                try:
                    debit = int(self.debit_daily_lblcb.get())
                    if self.client.addable("debit", debit) == 1: go = 1
                    else:
                        show(title="Debit", msg="Debit is incorrect", which="error")
                        go = 2
                except Exception as e: show(title="Incorrect input", msg="Debit must be numberic", which="error"); go = 2; print(e)
            if go == 1:
                gone = 0
                if self.daily_ready_cbtn.get() == "1": gone = 1
                elif confirm(title="Confirm", msg="Are you sure you want to add this", num=1): gone = 1
                if gone:
                    if self.daily:
                        self.daily.add(self.client, thrift=thrift, debit=debit)
                        self.update_table()
                        
                        Threads.save_data()
                
                    else: show(title="Daily not found", msg="A Daily is not found", which="error")
                
            elif go == 0: show(title="Thrift and/ or Debit", msg="Select if thrift or debit", which="error")


        else: show(title="Select an Area_and a Client", msg="An Area_and a Client must be selected to proceed", which="error")

    def delete_input(self):
        num = self.daily_del_ent.get()
        # try:
        if self.daily:
            num = int(num)
            if num != 0:
                if confirm(title="Delete", msg=f"Are you sure you want to delete input {num}", num=1):
                    self.daily.delete(num)
                    self.update_table()
                    # Threads.save_data()
            else:
                print(num)
                show(title="Maximum", msg="The input must be less than the total input and not ZERO (0)", which="error")
        else: show(title="No input", msg="There\"s no current input", which="error")
        # except Exception as e:
        #     print(e)
        #     show(title="Number", msg="The input must be numeric", which="error")

    def get_area_daily(self):
        if self.area: return TCreate.area_daily(self.area.name)

    def bto(self):
        try:
            num = int(self.bto_lblent.get())
            if self.daily:
                self.daily.totate(num)
                if confirm(title="Confirm", msg=f"Are you sure you want to add this BROUGHT TO OFFICE of {num} to {self.area} for this day {Date.date(form=1)}\n\nB-T-Os = {num}\nDEFICIT = {self.daily.deficit}\nEXCESS = {self.daily.excess}", num=1): self.daily.add_bto(num)
            else: show(title="Exist", msg="Pick an Area", which="error")
        
        except: show(title="Wrong Input", msg="The inputed BROUGHT TO OFFICE must be numeric", which="error")

    def get_daily(self):
        self.area_daily = self.get_area_daily()
        if self.area_daily:
            self.daily = self.area_daily.today_daily(self.area)
            return self.daily

    def search_dates(self):
        self.areas_box.set(sorted(Saving_Daily.area_dailies_names))
        if self.search_area_daily:
            date = self.dates_box.get()
            daily = self.search_area_daily.get(date)
            if daily: self.update_table(daily=daily)
            else: show(title="Exist", msg=f"The inputed date --> {date} does not exist", which="error")

    def get_search_area_daily(self, *a):
        area = self.areas_box.get()
        area_daily = Saving_Daily.get(area)
        if area_daily:
            self.search_area_daily = area_daily
            self.dates_box.set(values=[area_daily.dailies_dates])
            
            self.search_menu = Menu(self.search_lblfrm)
            self.search_list["menu"] = self.search_menu
            for daily in area_daily.dailies: self.search_menu.add_radiobutton(value=daily.date, label=daily.date, command=lambda daily=daily: self.update_table(daily=daily))


    def style(self):
        self.config(background=Styles.background)
        labelframes = [self.search_lblfrm, self.update_daily_thrift, self.edb, self.delete_daily_thrift, self.daily_input_pane]
        for labelframe in labelframes: labelframe.config(relief="groove", font=Fonts.font11b, foreground=Styles.foreground, background=Styles.background, highlightbackground=Styles.background, highlightcolor=Styles.foreground)

        buttons = [self.search_btn, self.add_edb_btn, self.delete_daily_btn, self.daily_add_btn, self.daily_update_btn]
        for button in buttons: button.config(activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground,relief="solid", overrelief="groove")

        labels = [self.daily_tip, self.month_lbl, self.area_lbl, self.client_lbl]
        for label in labels:
            Fonts.font = Fonts.font14b
            if label == self.client_lbl: Fonts.font = Fonts.font11b
            label.config(activebackground=Styles.background, activeforeground="black", background=Styles.higbg, disabledforeground=Styles.foreground, font=Fonts.font, foreground=Styles.higfg, highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief="solid")
        
        checkbuttons = [self.daily_ready, self.up_daily_1, self.up_daily_2, self.up_daily_3, self.current_mn_rb, self.next_mn_rb]
        for checkbutton in checkbuttons: checkbutton.config(activebackground=Styles.background, activeforeground=Styles.foreground, background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, justify="left", relief="groove")
        
        self.daily_del_ent["borderwidth"] = 3
        
        styles = [sty for sty in list(self.__dict__.values()) if isinstance(sty, TwoWidgets)]
        for style in styles: style.style()
        
        
        self.cb_clicked()
        self.rb_clicked()

    def search_areas_put(self): self.areas_box.set(values=sorted(Saving_Daily.area_dailies_names))
    
    
    
    def cb_clicked(self):
        buts = {self.up_daily_1:self.daily_update1_cbtn, self.up_daily_2:self.daily_update2_cbtn, self.up_daily_3:self.daily_update3_cbtn, self.daily_ready:self.daily_ready_cbtn}
        for but in buts:
            var = buts[but]
            if var.get() == "1": but["fg"] = "blue"
            else: but["fg"] = Styles.foreground
    def rb_clicked(self):
        buts = [self.current_mn_rb, self.next_mn_rb]
        for but in buts:
            var = self.daily_status
            val = but["value"]
            if var.get() == val: but["fg"] = "blue"
            else: but["fg"] = Styles.foreground

    def place_widgs(self):
        self.daily_input_pane.place(relx=0, rely=0, relh=1, relw=1)
        self.month_lbl.place(relx=.01, rely=.01, relh=.075, relw=.65, bordermode="ignore")
        self.area_lbl.place(relx=.01, rely=.09, relh=.075, relw=.48, bordermode="ignore")
        self.client_lbl.place(relx=.5, rely=.09, relh=.075, relw=.48, bordermode="ignore")
        self.current_mn_rb.place(relx=.67, rely=.02, relh=.065, relw=.15, bordermode="ignore")
        self.next_mn_rb.place(relx=.83, rely=.02, relh=.065, relw=.15, bordermode="ignore")
        self.edb.place(relx=.53, rely=.27, relh=.13, relw=.46)
        self.add_edb_btn.place(relx=.66, rely=.1, relh=.8, relw=.3)
        self.delete_daily_thrift.place(relx=.02, rely=.465, relh=.1, relw=.35)
        self.daily_del_ent.place(relx=.03, rely=.4, relh=.5, relw=.4, bordermode="ignore")
        self.delete_daily_btn.place(relx=.54, rely=.4, relh=.5, relw=.4, bordermode="ignore")
        self.daily_ready.place(relx=.35, rely=.3, relh=.06, relw=.15, bordermode="ignore")
        self.daily_add_btn.place(relx=.35, rely=.375, relh=.06, relw=.12, bordermode="ignore")
        self.search_lblfrm.place(relx=0, rely=.58, relh=.16, relw=.53)
        self.search_list.place(relx=.75, rely=.15, relh=.3, relw=.24)
        self.search_btn.place(relx=.75, rely=.6, relh=.3, relw=.24)
        self.update_daily_thrift.place(relx=0, rely=.74, relh=.25, relw=.53)
        self.daily_tip.place(relx=.074, rely=.2, relh=.5, relw=.867, bordermode="ignore")
        self.daily_update_btn.place(relx=.444, rely=.75, relh=.18, relw=.45, bordermode="ignore")
        self.up_daily_1.place(relx=.074, rely=.75, relh=.2, relw=.093, bordermode="ignore")
        self.up_daily_2.place(relx=.185, rely=.75, relh=.2, relw=.093, bordermode="ignore")
        self.up_daily_3.place(relx=.296, rely=.75, relh=.2, relw=.093, bordermode="ignore")
        
        styles = [sty for sty in list(self.__dict__.values()) if isinstance(sty, TwoWidgets)]
        for style in styles: style.place_widgs()




