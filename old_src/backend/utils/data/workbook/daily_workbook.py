from xlsxwriter import Workbook as WORKBOOK
from ..path import Path
from ...details.tdetails import TDetails
from ...sort.thrift.regions import Regions
from ...debug.debug import Debug


class Daily_Workbook:
    space_12 = " " * 12
    one = TDetails.mul_1000
    ones = TDetails.mul_1000s
    def __str__(self): return "{} WB".format(self.path)
    def __repr__(self): return self.__str__()
    def __init__(self, area):
        self.area = area
        self.path = Path.area_file(area, ext="dxlsx")
        if self.path:
            self.area = area
            self.daily_wb = WORKBOOK(self.path)
        
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
            self.daily_datas()
            # Debug.printcol("closing %s"%self.path, "green")
            self.daily_wb.close()


    def formats(self):
        
        self.underline = self.daily_wb.add_format({"underline":True})
        self.blue = self.daily_wb.add_format({"align": "center", "valign": "vcenter", "bold": True, "color":"blue"})
        self.center = self.daily_wb.add_format({"align": "center"})
        self.green = self.daily_wb.add_format({"align": "center", "valign": "vcenter", "bold": True, "color":"green"})
        self.red = self.daily_wb.add_format({"align": "center", "valign": "vcenter", "bold":True, "color":"red"})

    def daily_datas(self):
        dailies = list(Regions.area_dailies(self.area))
        if dailies:
            for daily in dailies:
                title = "Daily %s"%daily.date
                title.replace("/", "-")
                self.dd = self.daily_wb.add_worksheet(title)
    
                self.dd.set_column("A:A", 5, self.blue)
                self.dd.set_column("B:B", 20, self.center)
                self.dd.set_column("C:I", 16, self.center)
                self.dd.set_column("G:H", 16, self.red)
                self.dd.set_column("I:I", 16, self.center)
                self.dd.set_column("J:K", 16, self.red)
    
            # merge range and write
                self.dd.merge_range("A1:K1", "", self.blue) #thrift_days
                self.dd.write_rich_string("A1", self.blue, "Daily %s"%daily.date, self.ref_in, self.blue, "Area:", self.underline, self.ref_ar, self.blue, self.space_12, self.blue, "Month:", self.underline, self.ref_mn, self.blue, self.space_12, self.blue, "Year:", self.underline, self.ref_yr, self.blue)
            
                self.dd.write("A2:A2", "S/N")
                self.dd.write("B2:B2", "Clients", self.blue)
                self.dd.write("C2:C2", "Rate", self.blue)
                self.dd.write("D2:D2", "Old Thrifts", self.blue)
                self.dd.write("E2:E2", "Today Thrift", self.blue)
                self.dd.write("F2:F2", "Savings", self.blue)
                self.dd.write("G2:G2", "Debits")
                self.dd.write("H2:H2", "Upfronts")
                self.dd.write("I2:I2", "Total Savings", self.blue)
                self.dd.write("J2:J2", "Total Debits")
                self.dd.write("K2:K2", "Total Upfronts")
    
                count = 3
                for data in daily.datas:
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
                    
                    # DD
                    self.ones(data)
                    self.dd.write(A, data[0])
                    self.dd.write(B, data[1])
                    self.dd.write(C, data[2])
                    self.dd.write(D, data[3])
                    self.dd.write(E, data[4])
                    self.dd.write(F, data[5])
                    self.dd.write(G, data[6])
                    self.dd.write(H, data[7])
                    self.dd.write(I, data[8])
                    self.dd.write(J, data[9])
                    self.dd.write(K, data[10])
                    count += 1




