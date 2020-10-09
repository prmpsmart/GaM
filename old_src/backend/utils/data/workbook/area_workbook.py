from xlsxwriter import Workbook as WORKBOOK
from ..path import Path
from ...details.tdetails import TDetails
from ...sort.thrift.regions import Regions
from ...sort.thrift.weeks import Weeks, Date, DAYS_NAMES
from ...sort.thrift.days import Days
from ...debug.debug import Debug



class Area_Workbook:
    colors = {"Sun": "#8F509D", "Mon": "#CD4A4C", "Tue": "#17806D", "Wed": "#EE204D", "Thu": "#FF6E4A", "Fri": "#1FCECB", "Sat": "#FF1DCE"}
    space_12 = " " * 12
    one = TDetails.mul_1000
    ones = TDetails.mul_1000s
    
    def __str__(self): return "{} WB".format(self.path)
    def __repr__(self): return self.__str__()

    def __init__(self, area):
        
        #globals
        self.path = Path.area_file(area, ext="xlsx")
        if self.path:
            self.area = area
            self.area_wb = WORKBOOK(self.path)
        
            self.form = "{0}%s{1}".format(self.space_12, self.space_12)
        
            self.month_name = area.month_name
            self.area_name = area.name
            self.year_name = area.year_name
        
        #formats
            self.ref_ar = self.form%self.area_name
            self.ref_mn = self.form%self.month_name
            self.ref_yr = self.form%self.year_name
            self.ref_in = self.form%"in"
          
            self.formats()
            self.headers()
        #    self.daily_datas()
            self.clients_datas()
            self.weekly_datas()
            self.daily_datas()
            self.wk_d_datas()
            self.wk_c_datas()
            self.day_datas()
        
            Debug.printcol("closing %s"%self.path)
            self.area_wb.close()

    def thrifts_days_index(self):
        st = 68
        end = 64
        index = []
        for _ in range(31):
            st +=1
            if st < 91: index.append(chr(st))
            elif st > 90:
                end += 1
                index.append(chr(65) + chr(end))
            else : break
        return index

    def formats(self):
        
        self.underline = self.area_wb.add_format({"underline":True})
        self.blue = self.area_wb.add_format({"align": "center", "valign": "vcenter", "bold": True, "color":"blue"})
        self.center = self.area_wb.add_format({"align": "center"})
        self.green = self.area_wb.add_format({"align": "center", "valign": "vcenter", "bold": True, "color":"green"})
        self.red = self.area_wb.add_format({"align": "center", "valign": "vcenter", "bold":True, "color":"red"})

    def headers(self):
        # Clients Thrifts
        self.ct = self.area_wb.add_worksheet("Clients Thrifts")
        
        # columns
        self.ct.set_column("A:A", 5, self.blue)
        self.ct.set_column("B:B", 20, self.center)
        self.ct.set_column("C:C", 17, self.center)
        self.ct.set_column("D:D", 6, self.center)
        self.ct.set_column("E:AI", 2, self.center)
        self.ct.set_column("AJ:AL", 15, self.center)
        self.ct.set_column("AJ:AJ", 15, self.red)
        self.ct.set_column("AK:AK", 15, self.green)
        self.ct.set_column("AL:AL", 15, self.red)
        self.ct.set_column("AM:AM", 15, self.blue)

        # merge range and write
        self.ct.merge_range("E1:AI1", "", self.blue) #thrift_days
        self.ct.write_rich_string("E1", self.blue, "Area:", self.underline, self.ref_ar, self.blue, self.space_12, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
        self.ct.merge_range("A1:A2", "S/N")
        self.ct.merge_range("B1:B2", "Name", self.blue)
        self.ct.merge_range("C1:C2", "Brought-Forward", self.blue)
        self.ct.merge_range("D1:D2", "Rate", self.blue)
        
        for day in range(31):
            index = self.thrifts_days_index()[day]
            cell = index + str(2)
            self.ct.write(cell, day + 1, self.blue)
        
        self.ct.merge_range("AJ1:AJ2", "Debit")
        self.ct.merge_range("AK1:AK2", "Balance")
        self.ct.merge_range("AL1:AL2", "Upfront")
        self.ct.merge_range("AM1:AM2", "Paid")
       
        ## Clients Worksheet
        self.cw = self.area_wb.add_worksheet("Clients Worksheet")
        
        # columns
        self.cw.set_column("A:A", 5, self.blue)
        self.cw.set_column("B:B", 20, self.center)
        self.cw.set_column("C:C", 17, self.center)
        self.cw.set_column("D:D", 6, self.center)
        self.cw.set_column("E:J", 15, self.center)
        self.cw.set_column("G:G", 15, self.red)
        self.cw.set_column("I:J", 15, self.red)
        self.cw.set_column("K:L", 15, self.green)
        self.cw.set_column("M:M", 15, self.blue)
        
        # merge range and write
        self.cw.merge_range("A1:M1", "", self.blue) 
        self.cw.write_rich_string("A1", self.blue, "Clients", self.ref_in, self.blue, "Area:", self.underline, self.ref_ar, self.blue, self.space_12, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
        self.cw.write("A2", "S/N")
        self.cw.write("B2", "Name", self.blue)
        self.cw.write("C2", "Brought-Fs", self.blue)
        self.cw.write("D2", "Rate", self.blue)
        self.cw.write("E2", "Thrifts", self.blue)
        self.cw.write("F2", "Savings", self.blue)
        self.cw.write("G2", "Debit")
        self.cw.write("H2", "Not-Paid", self.blue)
        self.cw.write("I2", "Upfront")
        self.cw.write("J2", "P-Upfront")
        self.cw.write("K2", "R-Upfront")
        self.cw.write("L2", "Balance")
        self.cw.write("M2", "Paid")
    
        ## Weekly Worksheet
        self.ww = self.area_wb.add_worksheet("Weekly Worksheet")
        
        # columns
        self.ww.set_column("A:N", 15, self.center)
        self.ww.set_column("F:F", 15, self.red)
        self.ww.set_column("H:I", 15, self.red)
        self.ww.set_column("J:K", 15, self.green)
        self.ww.set_column("L:M", 15, self.red)
        self.ww.set_column("N:N", 15, self.green)
        
        # merge range and write
        self.ww.merge_range("A1:N1", "", self.blue)
        self.ww.write_rich_string("A1", self.blue, "Weeks", self.ref_in, self.blue, "Area:", self.underline, self.ref_ar, self.blue, self.space_12, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
        
        self.ww.write("A2", "Weeks", self.blue)
        self.ww.write("B2", "Clients", self.blue)
        self.ww.write("C2", "Brought-Fs", self.blue)
        self.ww.write("D2", "Commissions", self.blue)
        self.ww.write("E2", "Savings", self.blue)
        self.ww.write("F2", "Debits")
        self.ww.write("G2", "Not-Paids", self.blue)
        self.ww.write("H2", "Upfronts")
        self.ww.write("I2", "P-Upfronts")
        self.ww.write("J2", "R-Upfronts")
        self.ww.write("K2", "Balances")
        self.ww.write("L2", "Deficits")
        self.ww.write("M2", "Excesses")
        self.ww.write("N2", "B-T-Os")
    
        ## Daily Worksheet
        self.dw = self.area_wb.add_worksheet("Daily Worksheet")
        
        # columns
        self.dw.set_column("A:O", 15, self.center)
        self.dw.set_column("D:E", 15, self.center)
        self.dw.set_column("A2:A2", 15, self.blue)
        self.dw.set_column("G:G", 15, self.red)
        self.dw.set_column("I:J", 15, self.red)
        self.dw.set_column("K:L", 15, self.green)
        self.dw.set_column("M:N", 15, self.red)
        self.dw.set_column("O:O", 15, self.green)
        
        # merge range and write
        self.dw.merge_range("A1:O1", "", self.blue)
        self.dw.write_rich_string("A1", self.blue, "Days", self.ref_in, self.blue, "Area:", self.underline, self.ref_ar, self.blue, self.space_12, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
        
        self.dw.write("A2", "Dates", self.blue)
        self.dw.write("B2", "Days", self.blue)
        self.dw.write("C2", "Clients", self.blue)
        self.dw.write("D2", "Brought-Fs", self.blue)
        self.dw.write("E2", "Commissions", self.blue)
        self.dw.write("F2", "Savings", self.blue)
        self.dw.write("G2", "Debits")
        self.dw.write("H2", "Not-Paids", self.blue)
        self.dw.write("I2", "Upfronts")
        self.dw.write("J2", "P-Upfronts")
        self.dw.write("K2", "R-Upfronts")
        self.dw.write("L2", "Balances")
        self.dw.write("M2", "Deficits")
        self.dw.write("N2", "Excesses")
        self.dw.write("O2", "B-T-Os")
    
    
        ## Weeks Days Worksheet
        self.wds = []
        for week in Weeks.weeks[:-1]:
            wd = self.area_wb.add_worksheet("%s Days Worksheet"%week)
            self.wds.append(wd)
                
            # columns
            wd.set_column("A:O", 15, self.center)
            wd.set_column("D:E", 15, self.center)
            wd.set_column("A2:A2", 15, self.blue)
            wd.set_column("G:G", 15, self.red)
            wd.set_column("I:J", 15, self.red)
            wd.set_column("L:L", 15, self.red)
            wd.set_column("M:N", 15, self.green)
            wd.set_column("O:O", 15, self.green)
            
            # merge range and write
            wd.merge_range("A1:O1", "", self.blue)
            wd.write_rich_string("A1", self.blue, "%s Days"%week, self.ref_in, self.blue, "Area:", self.underline, self.ref_ar, self.blue, self.space_12, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
            
            wd.write("A2", "Dates", self.blue)
            wd.write("B2", "Days", self.blue)
            wd.write("C2", "Clients", self.blue)
            wd.write("D2", "Brought-Fs", self.blue)
            wd.write("E2", "Commissions", self.blue)
            wd.write("F2", "Savings", self.blue)
            wd.write("G2", "Debits")
            wd.write("H2", "Not-Paids", self.blue)
            wd.write("I2", "Upfronts")
            wd.write("J2", "P-Upfronts")
            wd.write("K2", "R-Upfronts")
            wd.write("L2", "Balances")
            wd.write("M2", "Deficits")
            wd.write("N2", "Excesses")
            wd.write("O2", "B-T-Os")
        
       ## Weeks Clients Worksheet
        self.wcs = []
        for week in Weeks.weeks[:-1]:
            wc = self.area_wb.add_worksheet("%s Clients Worksheet"%week)
            self.wcs.append(wc)
                
            # columns
            wc.set_column("A:A", 5, self.blue)
            wc.set_column("B:B", 20, self.center)
            wc.set_column("C:C", 17, self.center)
            wc.set_column("D:J", 15, self.center)
            wc.set_column("G:G", 15, self.red)
            wc.set_column("I:J", 15, self.red)
            wc.set_column("K:L", 15, self.green)
            
            # merge range and write
            wc.merge_range("A1:L1", "", self.blue) 
            wc.write_rich_string("A1", self.blue, "%s Clients"%week, self.ref_in, self.blue, "Area:", self.underline, self.ref_ar, self.blue, self.space_12, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
            wc.write("A2", "S/N")
            wc.write("B2", "Name", self.blue)
            wc.write("C2", "Brought-Forwards", self.blue)
            wc.write("D2", "Rate", self.blue)
            wc.write("E2", "Thrifts", self.blue)
            wc.write("F2", "Savings", self.blue)
            wc.write("G2", "Debit")
            wc.write("H2", "Not-Paid", self.blue)
            wc.write("I2", "Upfront")
            wc.write("J2", "P-Upfront")
            wc.write("K2", "R-Upfront")
            wc.write("L2", "Balance")

        ## Days Worksheet
        self.dws = []
        for day in DAYS_NAMES[0:5]:
            dw = self.area_wb.add_worksheet("%ss Worksheet"%day)
            self.dws.append(dw)
                
            # columns
            dw.set_column("A:N", 15, self.center)
            dw.set_column("C:D", 15, self.center)
            dw.set_column("A:A", 15, self.blue)
            dw.set_column("F:F", 15, self.red)
            dw.set_column("H:I", 15, self.red)
            dw.set_column("J:K", 15, self.green)
            dw.set_column("L:M", 15, self.red)
            dw.set_column("N:N", 15, self.green)
            
            # merge range and write
            dw.merge_range("A1:N1", "", self.blue)
            dw.write_rich_string("A1", self.blue, "%ss"%day, self.ref_in, self.blue, "Area:", self.underline, self.ref_ar, self.blue, self.space_12, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
            
            dw.write("A2", "Dates", self.blue)
            dw.write("B2", "Clients", self.blue)
            dw.write("C2", "Brought-Fs", self.blue)
            dw.write("D2", "Commissions", self.blue)
            dw.write("E2", "Savings", self.blue)
            dw.write("F2", "Debits")
            dw.write("G2", "Not-Paids", self.blue)
            dw.write("H2", "Upfronts")
            dw.write("I2", "P-Upfronts")
            dw.write("J2", "R-Upfronts")
            dw.write("K2", "Balances")
            dw.write("L2", "Deficits")
            dw.write("M2", "Excesses")
            dw.write("N2", "B-T-Os")

    def clients_datas(self):
        # Inputing data
        count = 3
        for client in self.area:
            A = "A" + str(count)
            B = "B" + str(count)
            C = "C" + str(count)
            D = "D" + str(count)
            E = "E" + str(count)
            F = "F" + str(count)
            G = "G" + str(count)
            H = "H" + str(count)
            I = "I" + str(count)
            J = "J" + str(count)
            K = "K" + str(count)
            L = "L" + str(count)
            M = "M" + str(count)
            AJ = "AJ" + str(count)
            AK = "AK" + str(count)
            AL = "AL" + str(count)
            AM = "AM" + str(count)

            # CT
            self.ct.write(A, self.one(client.number))
            self.ct.write(B, client.name)
            self.ct.write(C, self.one(client.brought_forward))
            self.ct.write(D, self.one(client.rate))
            self.ct.write(AJ, self.one(client.debit))
            self.ct.write(AK, self.one(client.balance))
            self.ct.write(AL, self.one(client.upfront))

            thrifts_days = client.thrifts_days
            thrifts_days_names = [d_n[0] for d_n in thrifts_days]
            thrifts_days_number = [d_n[1] for d_n in thrifts_days]


            ind = 0
            for day_index in range(len(thrifts_days_number)):
                index = self.thrifts_days_index()[ind]
                day = thrifts_days_number[day_index]
                day_name = thrifts_days_names[day_index]
                format_color = self.area_wb.add_format({"color": self.colors[day_name]})
                cell = index + str(count)
                self.ct.write(cell, day, format_color)
                ind += 1

            # CW
            data = client.datas()
            self.ones(data)
            self.cw.write(A, data[0])
            self.cw.write(B, data[1])
            self.cw.write(C, data[2])
            self.cw.write(D, data[3])
            self.cw.write(E, data[4])
            self.cw.write(F, data[5])
            self.cw.write(G, data[6])
            self.cw.write(H, data[7])
            self.cw.write(I, data[8])
            self.cw.write(J, data[9])
            self.cw.write(K, data[10])
            self.cw.write(L, data[11])

            if client.balance == 0:
                self.ct.write(AM, "PAID", self.blue)
                self.cw.write(K, "PAID", self.blue)

            count += 1

        #self.ct.hide_row_col_headers()
        #self.cw.hide_row_col_headers()

    def daily_datas(self):
        count = 3
        for data in Days.daily_sort(self.area):
            A = "A" + str(count)
            B = "B" + str(count)
            C = "C" + str(count)
            D = "D" + str(count)
            E = "E" + str(count)
            F = "F" + str(count)
            G = "G" + str(count)
            H = "H" + str(count)
            I = "I" + str(count)
            J = "J" + str(count)
            K = "K" + str(count)
            L = "L" + str(count)
            M = "M" + str(count)
            N = "N" + str(count)
            O = "O" + str(count)

            # DW
            self.ones(data)
            self.dw.write(A, data[0])
            self.dw.write(B, data[1])
            self.dw.write(C, data[2])
            self.dw.write(D, data[3])
            self.dw.write(E, data[4])
            self.dw.write(F, data[5])
            self.dw.write(G, data[6])
            self.dw.write(H, data[7])
            self.dw.write(I, data[8])
            self.dw.write(J, data[9])
            self.dw.write(K, data[10])
            self.dw.write(L, data[11])
            self.dw.write(M, data[12])
            self.dw.write(N, data[13])
            self.dw.write(O, data[14])
            
            count += 1

    def weekly_datas(self):
        count = 3
        for data in Weeks.weekly_sort(self.area):
            A = "A" + str(count)
            B = "B" + str(count)
            C = "C" + str(count)
            D = "D" + str(count)
            E = "E" + str(count)
            F = "F" + str(count)
            G = "G" + str(count)
            H = "H" + str(count)
            I = "I" + str(count)
            J = "J" + str(count)
            K = "K" + str(count)
            L = "L" + str(count)
            M = "M" + str(count)
            N = "N" + str(count)

            # DW
            self.ones(data)
            self.ww.write(A, data[0])
            self.ww.write(B, data[1])
            self.ww.write(C, data[2])
            self.ww.write(D, data[3])
            self.ww.write(E, data[4])
            self.ww.write(F, data[5])
            self.ww.write(G, data[6])
            self.ww.write(H, data[7])
            self.ww.write(I, data[8])
            self.ww.write(J, data[9])
            self.ww.write(K, data[10])
            self.ww.write(L, data[11])
            self.ww.write(M, data[12])
            self.ww.write(N, data[13])
            
            count += 1

    def wk_d_datas(self):
        count = 3
        for week in Weeks.weeks[:-1]:
            wd = self.wds[Weeks.weeks.index(week)]
            for data in Days.daily_sort(self.area, week=week):
                A = "A" + str(count)
                B = "B" + str(count)
                C = "C" + str(count)
                D = "D" + str(count)
                E = "E" + str(count)
                F = "F" + str(count)
                G = "G" + str(count)
                H = "H" + str(count)
                I = "I" + str(count)
                J = "J" + str(count)
                K = "K" + str(count)
                L = "L" + str(count)
                M = "M" + str(count)
                N = "N" + str(count)
                O = "O" + str(count)
    
                self.ones(data)
                wd.write(A, data[0])
                wd.write(B, data[1])
                wd.write(C, data[2])
                wd.write(D, data[3])
                wd.write(E, data[4])
                wd.write(F, data[5])
                wd.write(G, data[6])
                wd.write(H, data[7])
                wd.write(I, data[8])
                wd.write(J, data[9])
                wd.write(K, data[10])
                wd.write(L, data[11])
                wd.write(M, data[12])
                wd.write(N, data[13])
                wd.write(O, data[14])
                
                count += 1
            count = 3

    def wk_c_datas(self):
        count = 3
        for week in Weeks.weeks[:-1]:
            wc = self.wcs[Weeks.weeks.index(week)]
            for client in self.area.clients:
                A = "A" + str(count)
                B = "B" + str(count)
                C = "C" + str(count)
                D = "D" + str(count)
                E = "E" + str(count)
                F = "F" + str(count)
                G = "G" + str(count)
                H = "H" + str(count)
                I = "I" + str(count)
                J = "J" + str(count)
                K = "K" + str(count)
                L = "L" + str(count)
    
                data = Weeks.week_column(client, week)
                self.ones(data)
                wc.write(A, data[0])
                wc.write(B, data[1])
                wc.write(C, data[2])
                wc.write(D, data[3])
                wc.write(E, data[4])
                wc.write(F, data[5])
                wc.write(G, data[6])
                wc.write(H, data[7])
                wc.write(I, data[8])
                wc.write(J, data[9])
                wc.write(K, data[10])
                
                count += 1
            count = 3

    def day_datas(self):
        count = 3
        for day in DAYS_NAMES[:-2]:
            dw = self.dws[DAYS_NAMES[:].index(day)]
            for data in Days.month_day_columns(self.area, day):
                A = "A" + str(count)
                B = "B" + str(count)
                C = "C" + str(count)
                D = "D" + str(count)
                E = "E" + str(count)
                F = "F" + str(count)
                G = "G" + str(count)
                H = "H" + str(count)
                I = "I" + str(count)
                J = "J" + str(count)
                K = "K" + str(count)
                L = "L" + str(count)
                M = "M" + str(count)
                N = "N" + str(count)
    
                self.ones(data)
                dw.write(A, data[0])
                dw.write(B, data[1])
                dw.write(C, data[2])
                dw.write(D, data[3])
                dw.write(E, data[4])
                dw.write(F, data[5])
                dw.write(G, data[6])
                dw.write(H, data[7])
                dw.write(I, data[8])
                dw.write(J, data[9])
                dw.write(K, data[10])
                dw.write(L, data[11])
                dw.write(M, data[12])
                dw.write(N, data[13])
                
                count += 1
            count = 3


