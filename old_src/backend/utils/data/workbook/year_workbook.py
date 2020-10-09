from xlsxwriter import Workbook as WORKBOOK
from ..path import Path
from ...debug.debug import Debug
from ...details.tdetails import TDetails
from ...sort.thrift.regions import Regions



class Year_Workbook:
    space_12 = " " * 12
    one = TDetails.mul_1000
    ones = TDetails.mul_1000s
    
    def __str__(self): return "{} WB".format(self.path)
    def __repr__(self): return self.__str__()
    

    def __init__(self, year):
        #globals
        self.path = Path.year_file(year, ext="xlsx")
        self.year = year
        self.year_wb = WORKBOOK(self.path)
        
        self.form = "{0}%s{1}".format(self.space_12, self.space_12)
        
        self.year_name = year.name
        
        #formats
        self.ref_yr = self.form%self.year_name
        self.ref_in = self.form%"in"
          
        self.formats()
        self.headers()
        self.areas_datas()
        self.months_datas()
        
        Debug.printcol("closing %s"%self.path, "yellow")
        self.year_wb.close()

    def formats(self):
        self.underline = self.year_wb.add_format({"underline":True})
        self.blue = self.year_wb.add_format({"align": "center", "valign": "vcenter", "bold": True, "color":"blue"})
        self.center = self.year_wb.add_format({"align": "center"})
        self.green = self.year_wb.add_format({"align": "center", "valign": "vcenter", "bold": True, "color":"green"})
        self.red = self.year_wb.add_format({"align": "center", "valign": "vcenter", "bold":True, "color":"red"})

    def headers(self):
        ## Months Worksheet
        self.mw = self.year_wb.add_worksheet("Months Worksheet")
        
        # columns
        self.mw.set_column("A:N", 12, self.center)
        self.mw.set_column("C2:D2", 15, self.center)
        self.mw.set_column("F:F", 12, self.red)
        self.mw.set_column("H:I", 12, self.red)
        self.mw.set_column("J:K", 12, self.green)
        self.mw.set_column("L:M", 12, self.red)
        self.mw.set_column("N:N", 12, self.green)
        
        # merge range and write
        self.mw.merge_range("A1:N1", "", self.blue) 
        self.mw.write_rich_string("A1", self.blue, "Months", self.ref_in, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
        self.mw.write("A2", "Months", self.blue)
        self.mw.write("B2", "Clients", self.blue)
        self.mw.write("C2", "Brought-Fs", self.blue)
        self.mw.write("D2", "Commissions", self.blue)
        self.mw.write("E2", "Savings", self.blue)
        self.mw.write("F2", "Debits")
        self.mw.write("G2", "Not-Paids", self.blue)
        self.mw.write("H2", "Upfronts")
        self.mw.write("I2", "P-Upfronts")
        self.mw.write("J2", "R-Upfronts")
        self.mw.write("K2", "Balances")
        self.mw.write("L2", "Deficits")
        self.mw.write("M2", "Excesses")
        self.mw.write("N2", "B-T-Os")
    
        ## Areas Worksheet
        self.aw = self.year_wb.add_worksheet("Areas Worksheet")
        
        # columns
        self.aw.set_column("A:N", 12, self.center)
        self.aw.set_column("C2:D2", 15, self.center)
        self.aw.set_column("F:F", 12, self.red)
        self.aw.set_column("H:I", 12, self.red)
        self.aw.set_column("J:K", 12, self.green)
        self.aw.set_column("L:M", 12, self.red)
        self.aw.set_column("N:N", 12, self.green)
        
        # merge range and write
        self.aw.merge_range("A1:N1", "", self.blue)
        self.aw.write_rich_string("A1", self.blue, "Areas", self.ref_in, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
        
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

    def months_datas(self):
        count = 3
        for month in self.year.months:
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

            data = month.datas()
            self.ones(data)
            self.mw.write(A, data[0])
            self.mw.write(B, data[2])
            self.mw.write(C, data[3])
            self.mw.write(D, data[4])
            self.mw.write(E, data[5])
            self.mw.write(F, data[6])
            self.mw.write(G, data[7])
            self.mw.write(H, data[8])
            self.mw.write(I, data[9])
            self.mw.write(J, data[10])
            self.mw.write(K, data[11])
            self.mw.write(L, data[12])
            self.mw.write(M, data[12])
            self.mw.write(N, data[13])

            count += 1

    def areas_datas(self):
        # Inputing data
        count = 3
        for data in Regions.sum_areas_in_year(self.year):
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
        #self.mw.hide_row_col_headers()


