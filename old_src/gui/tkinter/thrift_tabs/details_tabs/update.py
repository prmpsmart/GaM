
from tkinter import Button, Frame, StringVar
from tkinter.ttk import Combobox

from ...utils.widgets.admin_req import make_change

from .....backend.thrift.regions.years import Years
from .....backend.utils.create.tcreate import TCreate
from .....backend.utils.debug.debug import Debug
from .....backend.utils.sort.date import MONTHS_NAMES, Date
from .....backend.utils.sort.thrift.regions import Regions
from .....backend.utils.threads import Threads
from ...utils.decorate.styles import Fonts, Styles
from ...utils.widgets.debug import Out_Message, confirm, show
from ...utils.widgets.admin_req import make_change
from ...utils.widgets.twowidgets import (Checkbutton, CheckCombo, CheckEntry,
                                         LabelCombo, LabelFrame, Radiobutton,
                                         RadioCombo, RadioEntry, TwoWidgets)


class Thrift_Update(Frame):
    go = 1
    def __init__(self, master, small_details, full_details, details_output, **kw):
        super().__init__(master, **kw)
        
        #### General Widgets
        self.small_details = small_details
        self.full_details = full_details
        self.details_output = details_output
        
       ####### Variables #########
        # Regions
        self.regions = StringVar()
        self.cr_cbtn = StringVar()
        self.status = StringVar()
        
        self.amount_cbtn = StringVar()
        
        self.man_region = StringVar()
        
        
        # Update
        self.chng_name_chkbtn = StringVar()
        self.ready_cbtn = StringVar()
        self.rate_cbtn = StringVar()
        self.thrift_cbtn = StringVar()
        self.brought_cbtn = StringVar()
        self.debit_cbtn = StringVar()
        self.upfront_cbtn = StringVar()
        self.amount_update = StringVar()
        self.area_confirm = None
        self.up_client = None
        
        
      ############ Regions
        self.regions_lblfrm = LabelFrame(self, text="""Regions""")
        

        self.rg_yr_rb = Radiobutton(self.regions_lblfrm, text="""Year""", value="year", variable=self.regions, command=self.rb_clicked)
        

        self.rg_mn_rb = Radiobutton(self.regions_lblfrm, text="""Month""", value="month", variable=self.regions, command=self.rb_clicked)
        
 
        self.rg_ar_rb = Radiobutton(self.regions_lblfrm, text="""Area""", value="area", variable=self.regions, command=self.rb_clicked)
        

        self.rg_cl_rb = Radiobutton(self.regions_lblfrm, text="""Client""", value="client", variable=self.regions, command=self.rb_clicked)
        

        self.rg_ne_rb = Radiobutton(self.regions_lblfrm, text="""Next""", value="next", variable=self.status, command=self.set_areas)
        
        
        self.rg_cur_rb = Radiobutton(self.regions_lblfrm, text="""Current""", value="current", variable=self.status, command=self.set_areas)
        
        
        self.rg_pr_rb = Radiobutton(self.regions_lblfrm, text="""Previous""", value="previous", variable=self.status, command=self.rb_clicked)
        

        self.rg_cr_chkbtn = Checkbutton(self.regions_lblfrm, text="""Create""", variable=self.cr_cbtn, command=self.cb_clicked)
        

        self.cr_rg_btn = Button(self.regions_lblfrm, text="""Create""", command=self.create)
        
        
        
      ############ Update
        self.update_lblfrm = LabelFrame(self, text="""Update Client Details""")
        
       ######### Area
        self.upd_ar_lblcb = LabelCombo(self.update_lblfrm, text="""Area""", func=self.upd_area, relx=.01, rely=.02, relh=.14, relw=.5, orient="h")
 
       ######### Client
        self.upd_cl_lblcb = CheckCombo(self.update_lblfrm, text="""Client""", relx=.01, rely=.16, relh=.14, relw=.78, func=self.upd_client, variable=self.chng_name_chkbtn, orient="h", longent=1)
       
       ######### Thrift
        self.upd_thf_lblent = CheckEntry(self.update_lblfrm,  text="""Thrift""", relx=.012, rely=.33, relh=.12, relw=.5, bordermode="ignore", variable=self.thrift_cbtn, orient="h")

       ######### Rate
        self.upd_rt_lblent = CheckEntry(self.update_lblfrm,  text="""Rate""", relx=.01, rely=.47, relh=.12, relw=.5, variable=self.rate_cbtn, orient="h")
        
       ######### Brought-F
        self.upd_brf_lblent = CheckEntry(self.update_lblfrm,  text="Brought-F", relx=.01, rely=.6, relh=.12, relw=.65, variable=self.brought_cbtn, orient="h")
        
       ######### Debit
        self.upd_deb_lblent = CheckEntry(self.update_lblfrm, text="""Debit""", relx=.01, rely=.73, relh=.12, relw=.5, variable=self.debit_cbtn, orient="h")
        
       ######### Upfront
        self.upd_upf_lblent = CheckEntry(self.update_lblfrm, text="""Upfront""", relx=.01, rely=.86, relh=.12, relw=.6, variable=self.upfront_cbtn, orient="h")
        
       #### Update Button
        self.ready_chkbtn = Checkbutton(self.update_lblfrm, text="""READY""", variable=self.ready_cbtn, command=self.cb_clicked)
        
        
        self.update_btn = Button(self.update_lblfrm, text="""Update""", command=self.update_thrift)
        

        
      ##### Manual Update of Old Datas
        self.man_data_lblfrm = LabelFrame(self, text="""Datas (Y-axis)""")
        
        
        self.m_clnt_chkbtn = Radiobutton(self.man_data_lblfrm, text="""Clients""", variable=self.amount_cbtn, value="clnt", command=self.rb_clicked)
        
        
        self.m_brf_chkbtn = Radiobutton(self.man_data_lblfrm, text="""Brought-Fs""", variable=self.amount_cbtn, value="brf", command=self.rb_clicked)
        

        self.m_com_chkbtn = Radiobutton(self.man_data_lblfrm, text="""Commissions""", variable=self.amount_cbtn, value="com", command=self.rb_clicked)
        
        
        self.m_sav_chkbtn = Radiobutton(self.man_data_lblfrm, text="""Savings""", variable=self.amount_cbtn, value="sav", command=self.rb_clicked)
        
        
        self.m_deb_chkbtn = Radiobutton(self.man_data_lblfrm, text="""Debits""", variable=self.amount_cbtn, value="deb", command=self.rb_clicked)
        
        
        self.m_upf_chkbtn = Radiobutton(self.man_data_lblfrm, text="""Upfronts""", variable=self.amount_cbtn, value="upf", command=self.rb_clicked)
        
        
        
        self.m_pupf_chkbtn = Radiobutton(self.man_data_lblfrm, text="""P-Upfronts""", variable=self.amount_cbtn, value="pupf", command=self.rb_clicked)
        
        
        
        self.m_rupf_chkbtn = Radiobutton(self.man_data_lblfrm, text="""R-Upfronts""", variable=self.amount_cbtn, value="rupf", command=self.rb_clicked)
        
        
        self.m_bal_chkbtn = Radiobutton(self.man_data_lblfrm, text="""Balances""", variable=self.amount_cbtn, value="bal", command=self.rb_clicked)
        

        self.m_def_chkbtn = Radiobutton(self.man_data_lblfrm, text="""Deficits""", variable=self.amount_cbtn, value="def", command=self.rb_clicked)
        

        self.m_exc_chkbtn = Radiobutton(self.man_data_lblfrm, text="""Excessess""", variable=self.amount_cbtn, value="exc", command=self.rb_clicked)
        

        self.m_bto_chkbtn = Radiobutton(self.man_data_lblfrm, text="""B-T-Os""", variable=self.amount_cbtn, value="bto", command=self.rb_clicked)
        
        
       ######## Input Manual Datas
        self.manual_lblfrm = LabelFrame(self, text="Manual Update of Old Datas")
        

        self.man_year = RadioEntry(self.manual_lblfrm, text="""Year""", value="year", variable=self.man_region, relx=.15, rely=.04, relh=.15, relw=.7, orient="h", command=self.toggle)
        
        self.man_month = RadioCombo(self.manual_lblfrm, text="""Month""", variable=self.man_region, value="month", values=MONTHS_NAMES[1:], relx=.15, rely=.27, relh=.15, relw=.7, orient="h", command=self.toggle, func=self.man_month)
        
        self.man_area = RadioCombo(self.manual_lblfrm, text="""Area""", value="area", variable=self.man_region, relx=.15, rely=.45, relh=.15, relw=.7, orient="h", command=self.toggle)
        
        self.man_entry = CheckEntry(self.manual_lblfrm, text="""Records""", relx=.15, rely=.65, relh=.15, relw=.7, orient="h", command=self.toggle, variable=self.amount_update)

        self.man_add_btn = Button(self.manual_lblfrm,  text="""Manual Update""", command=self.man_add)
        

        self.man_create_btn = Button(self.manual_lblfrm,  text="""Manual Create""", command=self.man_create)
        


        self.reset()
        self.status.set("current")
        self.set_areas()
        

        self.style()
    
    def man_create(self, *a): make_change(self._man_create)

    def _man_create(self):
        region = self.man_region.get()
        if region == "year":
            try:
                year = int(self.man_year.get())
                cur_year = int(Date.curr_year())
                if cur_year >= year and 1990 <= year:
                    if Regions.check_year(str(year)): show(title="Exists", msg=f"Year {year} already exists", which="error")
                    else:
                        if confirm(title="Confirm", msg=f"Are you sure you want create Year {year}", num=1):
                            TCreate.man_year(year)
                            Threads.save_data()
                else: show(title="Invalid", msg=f"Enter a year lower than {cur_year} and greater than 1990", which="error")
            except: show(title="Invalid", msg="Enter a valid year", which="error")

        elif region == "month":
            year = Regions.check_year(self.man_year.get())
            if year:
                month = self.man_month.get()
                if month in Date.months:
                    if Regions.check_month(year.name, month): show(title="Exists", msg=f"Month {month} already exists", which="error")
                    else:
                        if confirm(title="Confirm", msg=f"Are you sure you want create Month {month}", num=1):
                            TCreate.man_month(year, month)
                            Threads.save_data()
                else: show(title="Invalid", msg="Enter a valid month", which="error")

            else: show(title="Invalid", msg="Enter a valid year", which="error")

        elif region == "area":
            month = Regions.check_month(self.man_year.get(), self.man_month.get())
            if month:
                area = "Area_%d" % (month.total_areas + 1)
                if confirm(title="Confirm", msg=f"Are you sure you want create {area} in {month}", num=1):
                    TCreate.man_area(month.year_name, month.name)
            else: show(title="Exists", msg=f"Month doesn\"t exists", which="error")

    def man_month(self, *a):
        year = Regions.check_year(self.man_year.get())
        if year:
            month = self.man_month.get()
            if month in Date.months:
                month = Regions.check_month(year.name, month)
                if month: self.man_area.set(month.areas_names)

    def man_add(self): make_change(self._man_add)
    
    def _man_add(self):
        if self.amount_update.get() == "1":
            amount = self.amount_cbtn.get()
            try:
                cur_year = int(Date.curr_year())
                year = int(self.man_year.get())
                if cur_year >= year and 1990 <= year:
                    month = Regions.check_month(str(year), self.man_month.get())
                    AMOUNT = ""
                    if month:
                        area = month.get(self.man_area.get())
                        if area:
                            if amount == "clnt": AMOUNT = "Clients"
                            elif amount == "brf": AMOUNT = "Brought-Fs"
                            elif amount == "sav": AMOUNT = "Savings"
                            elif amount == "deb": AMOUNT = "Debits"
                            elif amount == "upf": AMOUNT = "Upfronts"
                            elif amount == "pupf": AMOUNT = "P-Upfronts"
                            elif amount == "rupf": AMOUNT = "R-Upfronts"
                            elif amount == "bal": AMOUNT = "Balances"
                            elif amount == "def": AMOUNT = "Deficits"
                            elif amount == "exc": AMOUNT = "Excesses"
                            elif amount == "bto": AMOUNT = "B-T-Os"
                            elif amount == "com": AMOUNT = "Commmissions"
                            else: show(title="Required", msg="Pick a Data", which="error")
                    else: show(title="Exists", msg="Month not found", which="error")
                    if AMOUNT:
                        try:
                            num = int(self.man_entry.get())
                            if confirm(title="Confirm", msg=f"Are you sure you want to add {num} as the {AMOUNT} of {area}", num=1): self.append_man(area, amount, num)
                        except Exception as e: show(title="Invalid", msg="Enter a valid amount", which="error")
                else: show(title="Invalid", msg=f"Enter a year lower than {cur_year} and greater than 1990", which="error")
            except Exception as e: show(title="Invalid", msg="Enter a valid year", which="error")
        else: show(title="Invalid", msg="Check the Amount", which="error")
    def append_man(self, area, amount, num):
        if amount == "clnt": area.total_clients = num
        elif amount == "brf": area.brought_forwards = num
        elif amount == "sav": area.savings = num
        elif amount == "deb": area.debits = num
        elif amount == "upf": area.upfronts = num
        elif amount == "pupf": area.p_upfronts = num
        elif amount == "rupf": area.r_upfronts = num
        elif amount == "bal": area.balances = num
        elif amount == "def": area.deficits = num
        elif amount == "exc": area.excesses = num
        elif amount == "bto": area.btos = num
        elif amount == "com": area.commissions = num

    def toggle(self):
        lins = [self.man_year, self.man_month, self.man_area, self.man_entry]
        for lin in lins: lin.checked()

    def create(self): make_change(self._create)

    def _create(self):
        c_y = "Creation of Year"
        c_m = "Creation of Month"
        c_a = "Creation of Area"
        c_c = "Creation of Client"
        msg = "Are you sure you want to create \n"
        
        if self.cr_cbtn.get() == "1":
            region = self.regions.get()
            status = self.status.get()
            if status != "previous":
                if region == "year":
                    year = Date.get_year(status)
                    if year in Years.years_names: self.details_output(year + " already  exists",title="Exists", which="warn")
                    else:
                        if confirm(c_y, msg + year, 1):
                            year = TCreate.year(status)
                            self.details_output(str(year) + " created successfully", title="Creation Successful", which="info")
                            Threads.save_data()
                elif region == "month":
                    month = Date.get_month(status, y_r=True)
                    year = Regions.check_year(month[1])
                    if year:
                        if month[0] in year.months_names:
                            self.details_output(month[0] + " " + month[1] + " already  exists", title="Exists", which="warn")
                        else:
                            if confirm(c_m, msg + month[0] + " " + month[1], 1):
                                month = TCreate.month(status)
                                self.details_output(str(month) + " created successfully", title="Creation Successful", which="info")
                                Threads.save_data()
                    else: self.details_output(month[1] + " " + month[1] + " doesn\"t exists", title="Not Exists", which="error")
                elif region == "area":
                    month = Date.get_month(status, y_r=True)
                    ar_month = Regions.check_month(month[1], month[0])
                    if ar_month:
                        area_name = "Area_" + str(ar_month.total_areas + 1)
                        if confirm(c_a, msg + area_name + " " + month[0] + " " + month[1], 1):
                            area = TCreate.area(status)
                            self.details_output(str(area) + " created successfully", title="Creation Successful", which="info")
                            Threads.save_data()
                    else: self.details_output(Debug.get_bug(), title="Not found", which="error")
                elif region == "client":
                    if self.chng_name_chkbtn.get() == "1" and self.ready_cbtn.get() == "1":
                        area_name = self.upd_ar_cbox.get()
                        area = self.up_areas[self.up_areas_names.index(area_name)]
                        if area:
                            area_number = area.number
                            month = area.month
                            year = area.year
                            client_name = self.upd_nm_ent.get()
                            rt, thf =  self.rate_cbtn.get(), self.thrift_cbtn.get()
                            if rt == "1" and thf =="1":
                                rate, thrift = self.upd_rt_ent.get(), self.upd_thf_ent.get()
                            
                                if Regions.check_number(rate) and Regions.check_number(thrift):
                                    irate = int(rate)
                                    ithrift = int(thrift)
                                    savings = irate * ithrift
                                    bal = savings - irate
                                    msgc = msg + f"Client with the following starting details:\nArea_= {area}\nName = {client_name}\nRate = {rate}\nFirst Thrift = {thrift}\nSavings = {savings}\nBalance = {bal}\nIf yes:\nCheck Details tab for full details of the new client"
                                    if confirm(c_c, msgc, 1):
                                        self.up_client = TCreate.client(area_number, client_name, irate, ithrift, status=status)
                                        self.details_output(str(self.up_client) + " created successfully", title="Creation Successful", which="info")
                                        Threads.save_data()
                                        self.reset()
                                        self.get_small_details("client", self.up_client)
                                        self.full_details(refresh=True)
                                else: self.details_output("Rate and Thrit must be numeric", title="Required", which="error")
                            else: self.details_output("Click the Rate and Thrift checkbuttons", title="Required", which="error")
                        else: self.details_output(Debug.get_bug(), title="Not found", which="error")
                    else: self.details_output("Click the New and Ready checkbuttons", title="Required", which="error")
            else: show("Unable" ,"Can\"t create anything PREVIOUS","error")
        else:
            msg = "Click the Create Checkbutton"
            self.details_output(msg, title="Required", which="error")

    def update_thrift(self): make_change(self._update_thrift)
    
    def _update_thrift(self):
        if self.ready_cbtn.get() == "1":
            if self.up_client:
                if self.up_client.name == self.upd_cl_lblcb.get():
                    client = self.up_client
                    rt, thf, dbt, upf, brf = self.rate_cbtn.get(), self.thrift_cbtn.get(), self.debit_cbtn.get(), self.upfront_cbtn.get(), self.brought_cbtn.get()
                    
                    rate, thrift, debit, upfront, broughtf = self.upd_rt_lblent.get(), self.upd_thf_lblent.get(), self.upd_deb_lblent.get(), self.upd_upf_lblent.get(), self.upd_brf_lblent.get()
                    
                    if rt == "1":
                        if Regions.check_number(rate):
                            rate = int(rate)
                            rm = f"\nRate = {rate}\n"
                        else:
                            self.details_output("Rate is checked, but not number", title="Rate", which="warn")
                    else:
                        rate = 0
                        rm = ""
                    if thf == "1":
                        if Regions.check_number(thrift):
                            thrift = int(thrift)
                            if client.addable("thrift", thrift):
                                self.details_output(f"Client thrift can\"t be more than 31\n\t Only {31 - client.thrifts} are needed not {thrift}", title="Thrift Error", which="warn")
                                tm = f"\nThrift = {thrift}\n"
                            else:
                                thrift = 0
                                tm = ""
                        else:
                            self.details_output("Thrift is checked, but not number", title="Thrift", which="warn")
                    else:
                        thrift = 0
                        tm = ""
                    if dbt == "1":
                        if Regions.check_number(debit):
                            debit = int(debit)
                            if client.addable("debit", debit):  um = f"\nDebit = {debit}\n"
                            else:
                                show("Not addable", f"This {debit} can't be debitted from this client -> {client} as balance is {client.balance}", "error")
                                debit = 0
                                um = ""
                            dm = f"\nDebit = {debit}\n"
                        else: self.details_output("Debit is checked, but not number", title="Debit", which="warn")
                    else:
                        debit = 0
                        dm = ""
                    if upf == "1":
                        if Regions.check_number(upfront):
                            upfront = int(upfront)
                            if client.addable("upfront", upfront):  um = f"\nUpfront = {upfront}\n"
                            else:
                                show("Not addable", f"This {upfront} is not a multiple of the client's rate", "error")
                                upfront = 0
                                um = ""
                        else:
                            self.details_output("Upfront is checked, but not number", title="Upfront", which="warn")
                    else:
                        upfront = 0
                        um = ""
                    if brf == "1":
                        if Regions.check_number(broughtf):
                            broughtf = int(broughtf)
                            bm = f"\nBrought-F = {broughtf}\n"
                        else:
                            self.details_output("Brought-F is checked, but not number", title="Brought-F", which="warn")
                    else:
                        broughtf = 0
                        bm = ""
                    upd = "Updating Client Details"
                    head = "Are you sure you want to update Client details with the following:  \n"
                    area = f"\n{client.area}\n"
                    name = f"\nName = {client.name}\n"
                    msg = head + area + name + rm + tm + dm + um + bm
                    if confirm(upd, msg, 1):
                        n_t = thrift + client.thrifts
                        if rate:
                            n_r = rate
                            n_s = n_t * n_r
                        else:
                            n_r = client.rate
                            n_s = n_t * n_r
                        n_u = upfront + client.upfront
                        n_pu = upfront + client.p_upfront
                        n_ru = client.r_upfront
                        n_d = debit + client.debit
                        n_br  = broughtf + client.brought_forward
                        n_bal = n_br + n_s - n_u - n_d - n_r
                        head2 = "The new details of this client will be: "
                        rm2 = f"\nRate = {n_r}\n"
                        tm2 = f"\nThrift = {n_t}\n"
                        dm2 = f"\nDebit = {n_d}\n"
                        um2 = f"\nUpfront = {n_u}\n"
                        pum2 = f"\nP_Upfront = {n_pu}\n"
                        rum2 = f"\nR_Upfront = {n_ru}\n"
                        bm2 = f"\nBrought-F = {n_br}\n"
                        bal2 = f"\nBalance = {n_bal}\n"
                        sav2 = f"\nSavings = {n_s}\n"
                        msg2 = head2 + area + name + rm2 + tm2 + sav2 + dm2 + um2 + pum2 + rum2 + bm2 + bal2
                        if confirm(upd, msg2, 1):
                            self.details_output("Confirmed", title="Test", which="info")
                            finished = None
                            datas = [rate, upfront, debit, broughtf, thrift]
                            bool_data = [True if data else False for data in datas]
                            functions = [client.update_rate, client.add_upfront, client.add_debit, client.add_brought_forward, client.add_thrift]
                            for data in datas:
                                indx = datas.index(data)
                                func = functions[indx]
                                if bool_data[indx]:
                                    conf = func(data)
                                    if conf: continue
                                    else:
                                        self.details_output(Debug.get_bug())
                                        break
                            
                            finished = True
                            if finished:
                                self.get_small_details(region=self.up_client)
                                self.full_details(refresh=True)
                                Threads.save_data()

                else: self.details_output("Please re-choose a client", title="Required", which="error")
            else: self.details_output("Please choose a client", title="Required", which="error")
        else: self.details_output("Click the Ready checkbutton", title="Required", which="error")

    def set_areas(self):
        status = self.status.get()
        self.rb_clicked()
        month = None
        if status: 
                month_name, year = Date.get_month(status, 1)
                month =  Regions.check_month(year, month_name)
                if month:
                    self.up_areas = month.areas
                    self.up_areas_names = [area.name for area in self.up_areas]
                    self.upd_ar_lblcb.set(values=self.up_areas_names)

    def upd_area(self, *args):
        for area in self.up_areas:
            if area.name == self.upd_ar_lblcb.get():
                self.up_area = area
                self.get_small_details(region=area)
                self.details_output(area)
                self.up_clients = [client for client in area.clients]
                clients_names = [client.name for client in area.clients]
                self.upd_cl_lblcb.set(values=clients_names)

    def upd_client(self, *args):
        for client in self.up_clients:
            if client.name == self.upd_cl_lblcb.get():
                self.up_client = client
                self.get_small_details(region=client)
                self.details_output(client)

    def get_small_details(self, region=None):

        self.small_details.thrift_update(region=region)
        if region.which != "client": self.full_details(title=region, region=region, header="clients")

    def reset(self):
        self.regions.set(" ")
        self.cr_cbtn.set(" ")
        self.status.set(" ")
        
        self.chng_name_chkbtn.set(" ")
        self.ready_cbtn.set(" ")
        self.cr_cbtn.set(" ")
        self.rate_cbtn.set(" ")
        self.thrift_cbtn.set(" ")
        self.brought_cbtn.set(" ")
        self.debit_cbtn.set(" ")
        self.upfront_cbtn.set(" ")
        self.amount_update.set(" ")
        
        self.amount_cbtn.set(" ")
        
        self.man_region.set(" ")

    def style(self):
        self.config(background=Styles.background)
        rds = [self.rg_mn_rb, self.rg_ar_rb, self.rg_yr_rb, self.rg_cl_rb, self.rg_ne_rb, self.rg_cur_rb, self.rg_pr_rb, self.rg_cr_chkbtn, self.ready_chkbtn, self.m_clnt_chkbtn, self.m_brf_chkbtn, self.m_com_chkbtn, self.m_sav_chkbtn, self.m_deb_chkbtn, self.m_upf_chkbtn, self.m_pupf_chkbtn, self.m_rupf_chkbtn, self.m_bal_chkbtn, self.m_def_chkbtn, self.m_exc_chkbtn, self.m_bto_chkbtn]
        for rd in rds: rd.config(activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor="white", justify="left", overrelief="groove", relief="ridge")
        
        btns = [self.cr_rg_btn, self.update_btn, self.man_create_btn, self.man_add_btn]
        for btn in btns: btn.config(activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, overrelief="raised", relief="solid", pady="0")
        
        lblfrms = [self.update_lblfrm, self.regions_lblfrm, self.manual_lblfrm, self.man_data_lblfrm]
        for lblfrm in lblfrms: lblfrm.config(relief="groove", font=Fonts.font11b, foreground=Styles.foreground, background=Styles.background, highlightbackground=Styles.background, highlightcolor=Styles.foreground)
        styles = [sty for sty in list(self.__dict__.values()) if isinstance(sty, TwoWidgets)]
        for style in styles: style.style()
        
        self.cb_clicked()
        self.rb_clicked()

    def cb_clicked(self):
        buts = {self.rg_cr_chkbtn:self.cr_cbtn, self.ready_chkbtn:self.ready_cbtn}
        for but in buts:
            var = buts[but]
            if var.get() == "1": but["fg"] = "blue"
            else: but["fg"] = Styles.foreground
            
    def rb_clicked(self):
        region = [self.rg_yr_rb, self.rg_mn_rb, self.rg_ar_rb, self.rg_cl_rb]
        status = [self.rg_ne_rb, self.rg_cur_rb, self.rg_pr_rb]
        amount = [self.m_clnt_chkbtn, self.m_brf_chkbtn, self.m_com_chkbtn, self.m_sav_chkbtn, self.m_deb_chkbtn, self.m_upf_chkbtn, self.m_bal_chkbtn, self.m_def_chkbtn, self.m_exc_chkbtn, self.m_bto_chkbtn]
        buts = status + amount + region
        
        for but in buts:
            var = self.amount_cbtn
            if but in status: var = self.status
            elif but in region: var = self.regions
            val = but["value"]
            if var.get() == val: but["fg"] = "blue"
            else: but["fg"] = Styles.foreground


    def place_widgs(self):
        self.regions_lblfrm.place(relx=0, rely=0, relh=.17, relw=.533)
        self.rg_yr_rb.place(relx=.428, rely=.147, relh=.2, relw=.279, bordermode="ignore")
        self.rg_mn_rb.place(relx=.706, rely=.147, relh=.2, relw=.26, bordermode="ignore")
        self.rg_ar_rb.place(relx=.428, rely=.46, relh=.2, relw=.279, bordermode="ignore")
        self.rg_cl_rb.place(relx=.706, rely=.46, relh=.2, relw=.279, bordermode="ignore")
        self.rg_ne_rb.place(relx=.037, rely=.167, relh=.167, relw=.335, bordermode="ignore")
        self.rg_cur_rb.place(relx=.037, rely=.350, relh=.173, relw=.335, bordermode="ignore")
        self.rg_pr_rb.place(relx=.037, rely=.54, relh=.173, relw=.3355, bordermode="ignore")
        self.rg_cr_chkbtn.place(relx=.037, rely=.75, relh=.208, relw=.335, bordermode="ignore")
        self.cr_rg_btn.place(relx=.706, rely=.7, height=25, width=70, bordermode="ignore")
        self.update_lblfrm.place(relx=.0, rely=.46, relh=.52, relw=.533)
        self.ready_chkbtn.place(relx=.677, rely=.75, relh=.1, relw=.28, bordermode="ignore")
        self.update_btn.place(relx=.677, rely=.87, relh=.1, relw=.28, bordermode="ignore")
        self.man_data_lblfrm.place(relx=0, rely=.18, relh=.26, relw=.533)
        self.m_clnt_chkbtn.place(relx=.04, rely=.2, relh=.13, relw=.45, bordermode="ignore")
        self.m_brf_chkbtn.place(relx=.51, rely=.2, relh=.13, relw=.45, bordermode="ignore")
        self.m_com_chkbtn.place(relx=.04, rely=.33, relh=.13, relw=.45, bordermode="ignore")
        self.m_sav_chkbtn.place(relx=.51, rely=.33, relh=.13, relw=.45, bordermode="ignore")
        self.m_deb_chkbtn.place(relx=.04, rely=.46, relh=.13, relw=.45, bordermode="ignore")
        self.m_upf_chkbtn.place(relx=.51, rely=.46, relh=.13, relw=.45, bordermode="ignore")
        self.m_pupf_chkbtn.place(relx=.04, rely=.60, relh=.13, relw=.45, bordermode="ignore")
        self.m_rupf_chkbtn.place(relx=.51, rely=.60, relh=.13, relw=.45, bordermode="ignore")
        self.m_bal_chkbtn.place(relx=.04, rely=.73, relh=.13, relw=.45, bordermode="ignore")
        self.m_def_chkbtn.place(relx=.51, rely=.73, relh=.13, relw=.45, bordermode="ignore")
        self.m_exc_chkbtn.place(relx=.04, rely=.86, relh=.13, relw=.45, bordermode="ignore")
        self.m_bto_chkbtn.place(relx=.51, rely=.86, relh=.13, relw=.45, bordermode="ignore")
        self.manual_lblfrm.place(relx=.533, rely=0, relh=.44, relw=.467)
        self.man_add_btn.place(relx=.05, rely=.82, relh=.15, relw=.5)
        self.man_create_btn.place(relx=.57, rely=.82, relh=.15, relw=.4)
        
        styles = [sty for sty in list(self.__dict__.values()) if isinstance(sty, TwoWidgets)]
        for style in styles: style.place_widgs()
