from xlsxwriter import Workbook as WORKBOOK
from ..path import Path
from ...details.tdetails import TDetails
from ...sort.thrift.regions import Regions
from ...sort.thrift.weeks import Weeks, Date, DAYS_NAMES
from ...sort.thrift.days import Days
from ...debug.debug import Debug



class Month_Workbook:
    space_12 = " " * 12
    one = TDetails.mul_1000
    ones = TDetails.mul_1000s
    
    def __str__(self): return "{} WB".format(self.path)
    def __repr__(self): return self.__str__()
    

    def __init__(self, month):
        #globals
        self.path = Path.month_file(month, ext="xlsx")
        self.month = month
        if self.path:
            self.month_wb = WORKBOOK(self.path)
        
            self.form = "{0}%s{1}".format(self.space_12, self.space_12)
        
            self.month_name = month.name
            self.year_name = month.year_name
        
        #formats
            self.ref_mn = self.form%self.month_name
            self.ref_yr = self.form%self.year_name
            self.ref_in = self.form%"in"
          
            self.formats()
            self.headers()
            self.areas_datas()
            self.weekly_datas()
            self.daily_datas()
            self.wk_d_datas()
            self.wk_a_datas()
            self.day_datas()
        
            Debug.printcol("closing %s"%self.path, "red")
            self.month_wb.close()

    def formats(self):
        self.underline = self.month_wb.add_format({"underline":True})
        self.blue = self.month_wb.add_format({"align": "center", "valign": "vcenter", "bold": True, "color":"blue"})
        self.center = self.month_wb.add_format({"align": "center"})
        self.green = self.month_wb.add_format({"align": "center", "valign": "vcenter", "bold": True, "color":"green"})
        self.red = self.month_wb.add_format({"align": "center", "valign": "vcenter", "bold":True, "color":"red"})

    def headers(self):
        ## Areas Worksheet
        self.aw = self.month_wb.add_worksheet("Areas Worksheet")
        
        # columns
        self.aw.set_column("A:N", 12, self.center)
        self.aw.set_column("C2:D2", 15)
        self.aw.set_column("F:F", 12, self.red)
        self.aw.set_column("H:I", 12, self.red)
        self.aw.set_column("J:K", 12, self.green)
        self.aw.set_column("L:M", 12, self.red)
        self.aw.set_column("N:N", 12, self.green)
        
        # merge range and write
        self.aw.merge_range("A1:N1", "", self.blue) 
        self.aw.write_rich_string("A1", self.blue, "Areas", self.ref_in, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
        self.aw.write("A2", "Areas", self.blue)
        self.aw.write("B2", "Clients", self.blue)
        self.aw.write("C2", "Brought-Fs", self.blue)
        self.aw.write("D2", "Commissions", self.blue)
        self.aw.write("E2", "Savings", self.blue)
        self.aw.write("F2", "Debits")
        self.aw.write("G2", "Not-Paids", self.blue)
        self.aw.write("H2", "Upfronts")
        self.aw.write("I2", "P-Upfronts")
        self.aw.write("J2", "R-Upfronts")
        self.aw.write("K2", "Balances")
        self.aw.write("L2", "Deficits")
        self.aw.write("M2", "Excesses")
        self.aw.write("N2", "B-T-Os")

    
        ## Weekly Worksheet
        self.ww = self.month_wb.add_worksheet("Weekly Worksheet")
        
        # columns
        self.ww.set_column("A:N", 12, self.center)
        self.ww.set_column("C2:D2", 15)
        self.ww.set_column("F:F", 12, self.red)
        self.ww.set_column("H:I", 12, self.red)
        self.ww.set_column("J:K", 12, self.green)
        self.ww.set_column("L:M", 12, self.red)
        self.ww.set_column("N:N", 12, self.green)
        
        # merge range and write
        self.ww.merge_range("A1:N1", "", self.blue)
        self.ww.write_rich_string("A1", self.blue, "Weeks", self.ref_in, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
        
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
        self.dw = self.month_wb.add_worksheet("Daily Worksheet")
        
        # columns
        self.dw.set_column("A:O", 12, self.center)
        self.dw.set_column("B:B", 15, self.center)
        self.dw.set_column("D:E", 15, self.center)
        self.dw.set_column("A:A", 12, self.blue)
        self.dw.set_column("G:G", 12, self.red)
        self.dw.set_column("H:H", 12)
        self.dw.set_column("I:J", 12, self.red)
        self.dw.set_column("K:L", 12, self.green)
        self.dw.set_column("M:N", 12, self.red)
        self.dw.set_column("O:O", 12, self.green)
        
        # merge range and write
        self.dw.merge_range("A1:O1", "", self.blue)
        self.dw.write_rich_string("A1", self.blue, "Days", self.ref_in, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
        
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
            wd = self.month_wb.add_worksheet("%s Days Worksheet"%week)
            self.wds.append(wd)
                
            # columns
            wd.set_column("A:L", 12, self.center)
            wd.set_column("B:B", 15, self.center)
            wd.set_column("D:E", 15, self.center)
            wd.set_column("A:A", 12, self.blue)
            wd.set_column("G:G", 12, self.red)
            wd.set_column("H:H", 12)
            wd.set_column("I:J", 12, self.red)
            wd.set_column("K:L", 12, self.green)
            wd.set_column("M:N", 12, self.red)
            wd.set_column("O:O", 12, self.green)
            
            # merge range and write
            wd.merge_range("A1:O1", "", self.blue)
            wd.write_rich_string("A1", self.blue, "%s Days"%week, self.ref_in, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
            
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
        
       ## Weeks Areas Worksheet
        self.wcs = []
        for week in Weeks.weeks[:-1]:
            wc = self.month_wb.add_worksheet("%s Areas Worksheet"%week)
            self.wcs.append(wc)
                
            # columns
            wc.set_column("A:N", 12, self.center)
            wc.set_column("C:D", 15, self.center)
            wc.set_column("F:F", 12, self.red)
            wc.set_column("H:I", 12, self.red)
            wc.set_column("J:K", 12, self.green)
            wc.set_column("L:M", 12, self.red)
            wc.set_column("N:N", 12, self.green)
            
            # merge range and write
            wc.merge_range("A1:N1", "", self.blue) 
            wc.write_rich_string("A1", self.blue, "%s Areas"%week, self.ref_in, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
            wc.write("A2", "Areas", self.blue)
            wc.write("B2", "Clients", self.blue)
            wc.write("C2", "Brought-Fs", self.blue)
            wc.write("D2", "Commissions", self.blue)
            wc.write("E2", "Savings", self.blue)
            wc.write("F2", "Debits")
            wc.write("G2", "Not-Paids", self.blue)
            wc.write("H2", "Upfronts")
            wc.write("I2", "P-Upfronts")
            wc.write("J2", "R-Upfronts")
            wc.write("K2", "Balances")
            wc.write("L2", "Deficits")
            wc.write("M2", "Excesses")
            wc.write("N2", "B-T-Os")
        
    
        ## Days Worksheet
        self.dws = []
        for day in DAYS_NAMES[0:5]:
            dw = self.month_wb.add_worksheet("%ss Worksheet"%day)
            self.dws.append(dw)
                
            # columns
            dw.set_column("A:N", 12, self.center)
            dw.set_column("C:D", 15, self.center)
            dw.set_column("F:F", 12, self.red)
            dw.set_column("H:I", 12, self.red)
            dw.set_column("J:K", 12, self.green)
            dw.set_column("L:M", 12, self.red)
            dw.set_column("N:N", 12, self.green)
            
            # merge range and write
            dw.merge_range("A1:N1", "", self.blue)
            dw.write_rich_string("A1", self.blue, "%ss"%day, self.ref_in, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
            
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

    def areas_datas(self):
        # Inputing data
        count = 3
        for area in self.month:
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
            
            data = area.datas()
            self.ones(data)
            self.aw.write(A, data[0])
            self.aw.write(B, data[1])
            self.aw.write(C, data[2])
            self.aw.write(D, data[3])
            self.aw.write(E, data[4])
            self.aw.write(F, data[5])
            self.aw.write(G, data[6])
            self.aw.write(H, data[7])
            self.aw.write(I, data[8])
            self.aw.write(J, data[9])
            self.aw.write(K, data[10])
            self.aw.write(L, data[11])
            self.aw.write(M, data[12])
            self.aw.write(N, data[13])
            
            count += 1

        #self.ct.hide_row_col_headers()
        #self.aw.hide_row_col_headers()

    def weekly_datas(self):
        count = 3
        for data in Weeks.weekly_sort(self.month):
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

    def daily_datas(self):
        count = 3
        for data in Days.daily_sort(self.month):
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

    def wk_d_datas(self):
        count = 3
        for week in Weeks.weeks[:-1]:
            wd = self.wds[Weeks.weeks.index(week)]
            for data in Days.daily_sort(self.month, week=week):
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

    def wk_a_datas(self):
        count = 3
        for week in Weeks.weeks[:-1]:
            wd = self.wcs[Weeks.weeks.index(week)]
            for area in self.month.areas:
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
    
                data = Weeks.week_column(area, week)
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
                
                count += 1
            count = 3

    def day_datas(self):
        count = 3
        for day in DAYS_NAMES[:-2]:
            dw = self.dws[DAYS_NAMES[:].index(day)]
            for data in Days.month_day_columns(self.month, day):
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


