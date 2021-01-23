from xlsxwriter import Workbook as WORKBOOK
from win32com.client import Dispatch
import threading

class Colours:
    colours = {"Almond": "#EFDECD",
            "Antique Brass": "#CD9575",
            "Apricot": "#FDD9B5",
            "Aquamarine": "#78DBE2",
            "Asparagus": "#87A96B",
            "Atomic Tangerine": "#FFA474",
            "Banana Mania": "#FAE7B5",
            "Beaver": "#9F8170",
            "Bittersweet": "#FD7C6E",
            "Black": "#000000",
            "Blue": "#1F75FE",
            "Blue Bell": "#A2A2D0",
            "Blue Green": "#0D98BA",
            "Blue Violet": "#7366BD",
            "Blush": "#DE5D83",
            "Brick Red": "#CB4154",
            "Brown": "#B4674D",
            "Burnt Orange": "#FF7F49",
            "Burnt Sienna": "#EA7E5D",
            "Cadet Blue": "#B0B7C6",
            "Canary": "#FFFF99",
            "Caribbean Green": "#00CC99",
            "Carnation Pink": "#FFAACC",
            "Cerise": "#DD4492",
            "Cerulean": "#1DACD6",
            "Chestnut": "#BC5D58",
            "Copper": "#DD9475",
            "Cornflower": "#9ACEEB",
            "Cotton Candy": "#FFBCD9",
            "Dandelion": "#FDDB6D",
            "Denim": "#2B6CC4",
            "Desert Sand": "#EFCDB8",
            "Eggplant": "#6E5160",
            "Electric Lime": "#CEFF1D",
            "Fern": "#71BC78",
            "Forest Green": "#6DAE81",
            "Fuchsia": "#C364C5",
            "Fuzzy Wuzzy": "#CC6666",
            "Gold": "#E7C697",
            "Goldenrod": "#FCD975",
            "Granny Smith Apple": "#A8E4A0",
            "Gray": "#95918C",
            "Green": "#1CAC78",
            "Green Yellow": "#F0E891",
            "Hot Magenta": "#FF1DCE",
            "Inchworm": "#B2EC5D",
            "Indigo": "#5D76CB",
            "Jazzberry Jam": "#CA3767",
            "Jungle Green": "#3BB08F",
            "Laser Lemon": "#FEFE22",
            "Lavender": "#FCB4D5",
            "Macaroni and Cheese": "#FFBD88",
            "Magenta": "#F664AF",
            "Mahogany": "#CD4A4C",
            "Manatee": "#979AAA",
            "Mango Tango": "#FF8243",
            "Maroon": "#C8385A",
            "Mauvelous": "#EF98AA",
            "Melon": "#FDBCB4",
            "Midnight Blue": "#1A4876",
            "Mountain Meadow": "#30BA8F",
            "Navy Blue": "#1974D2",
            "Neon Carrot": "#FFA343",
            "Olive Green": "#BAB86C",
            "Orange": "#FF7538",
            "Orchid": "#E6A8D7",
            "Outer Space": "#414A4C",
            "Outrageous Orange": "#FF6E4A",
            "Pacific Blue": "#1CA9C9",
            "Peach": "#FFCFAB",
            "Periwinkle": "#C5D0E6",
            "Piggy Pink": "#FDDDE6",
            "Pine Green": "#158078",
            "Pink Flamingo": "#FC74FD",
            "Pink Sherbert": "#F78FA7",
            "Plum": "#8E4585",
            "Purple Heart": "#7442C8",
            "Purple Mountains Majesty": "#9D81BA",
            "Purple Pizzazz": "#FE4EDA",
            "Radical Red": "#FF496C",
            "Raw Sienna": "#D68A59",
            "Razzle Dazzle Rose": "#FF48D0",
            "Razzmatazz": "#E3256B",
            "Red": "#EE204D",
            "Red Orange": "#FF5349",
            "Red Violet": "#C0448F",
            "Robin's Egg Blue": "#1FCECB",
            "Royal Purple": "#7851A9",
            "Salmon": "#FF9BAA",
            "Scarlet": "#FC2847",
            "Screamin' Green": "#76FF7A",
            "Sea Green": "#93DFB8",
            "Sepia": "#A5694F",
            "Shadow": "#8A795D",
            "Shamrock": "#45CEA2",
            "Shocking Pink": "#FB7EFD",
            "Silver": "#CDC5C2",
            "Sky Blue": "#80DAEB",
            "Spring Green": "#ECEABE",
            "Sunglow": "#FFCF48",
            "Sunset Orange": "#FD5E53",
            "Tan": "#FAA76C",
            "Tickle Me Pink": "#FC89AC",
            "Timberwolf": "#DBD7D2",
            "Tropical Rain Forest": "#17806D",
            "Tumbleweed": "#DEAA88",
            "Turquoise Blue": "#77DDE7",
            "Unmellow Yellow": "#FFFF66",
            "Violet (Purple)": "#926EAE",
            "Violet Red": "#F75394",
            "Vivid Tangerine": "#FFA089",
            "Vivid Violet": "#8F509D",
            "White": "#FFFFFF",
            "Wild Blue Yonder": "#A2ADD0",
            "Wild Strawberry": "#FF43A4",
            "Wild Watermelon": "#FC6C85",
            "Wisteria": "#CDA4DE",
            "Yellow": "#FCE883",
            "Yellow Green": "#C5E384",
            "Yellow Orange": "#FFAE42"}

    bright_colours = {"Sun": "#8F509D", "Mon": "#CD4A4C", "Tue": "#17806D", "Wed": "#EE204D", "Thur": "#FF6E4A", "Fri": "#1FCECB", "Sat": "#FF1DCE"}

    colors_keys = list(colours.keys())
    colors_values = [a.lower() for a in list(colours.values())]
    bright_colors = list(bright_colours.values())
    @classmethod
    def getti(cls, a): return (cls.colors_keys[a], cls.colors_values[a])
    @classmethod
    def get(cls, name):return cls.colours.get(name.title(), "white")


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

class Workbook:
    @classmethod
    def run(cls, func, *args):
        thread = threading.Thread(target=func, args=args) if args else threading.Thread(target=func)
        thread.start()
    @classmethod
    def open_wb(cls, region, daily=None):
        file = ""
        if region.which == "years": file = Years_Workbook().path
        elif region.which == "year": file = Year_Workbook(region).path
        elif region.which == "month": file = Month_Workbook(region).path
        elif region.which == "area":
            if daily: file = Daily_Workbook(region).path
            else: file = Area_Workbook(region).path
        if file:
            xl = Dispatch("Excel.Application")
            xl.Visible = True
            wb = xl.Workbooks.Open(file)
    @classmethod
    def all_workbooks(cls):
        years = Years.years
        if years:
            cls.run(Years_Workbook)
            for year in years:
                cls.run(Year_Workbook, year)
                for month in year.months:
                    cls.run(Month_Workbook, month)
                    for area in month.areas:
                        cls.run(Area_Workbook, area)
                        cls.run(Daily_Workbook, area)
    @classmethod
    def cur_year_wb(cls):
        year = Years.get(Date.get_year())
        if year:
            cls.run(Year_Workbook, year)
            for month in year.months:
                cls.run(Month_Workbook, month)
                for area in month.areas:
                    cls.run(Area_Workbook, area)
                    cls.run(Daily_Workbook, area)
    @classmethod
    def cur_month_wb(cls):
       year = Years.get(Date.get_year())
       if year:
           month = year.get(Date.get_month())
           if month:
               cls.run(Month_Workbook, month)
               for area in month.areas:
                   cls.run(Area_Workbook, area)
                   cls.run(Daily_Workbook, area)

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

class Years_Workbook:
    space_12 = " " * 12
    one = TDetails.mul_1000
    ones = TDetails.mul_1000s
    
    def __str__(self): return "{} WB".format(self.path)
    def __repr__(self): return self.__str__()
    

    def __init__(self):
        #globals
        self.path = Path.years_file(ext="xlsx")
        self.years_wb = WORKBOOK(self.path)
        
        self.form = "{0}%s{1}".format(self.space_12, self.space_12)
        
        self.years_name = "Years"
        
        #formats
        self.ref_yr = self.form%self.years_name
        self.ref_in = self.form%"in"
          
        self.formats()
        self.headers()
        self.years_datas()
        self.months_datas()
        self.areas_datas()
        
        Debug.printcol("closing %s"%self.path, "white")
        self.years_wb.close()

    def formats(self):
        self.underline = self.years_wb.add_format({"underline":True})
        self.blue = self.years_wb.add_format({"align": "center", "valign": "vcenter", "bold": True, "color":"blue"})
        self.center = self.years_wb.add_format({"align": "center"})
        self.green = self.years_wb.add_format({"align": "center", "valign": "vcenter", "bold": True, "color":"green"})
        self.red = self.years_wb.add_format({"align": "center", "valign": "vcenter", "bold":True, "color":"red"})

    def headers(self):
        ## Years Worksheet
        self.yw = self.years_wb.add_worksheet("Years Worksheet")
        
        # columns
        self.yw.set_column("A:N", 12, self.center)
        self.yw.set_column("C2:D2", 15, self.center)
        self.yw.set_column("F:F", 12, self.red)
        self.yw.set_column("H:I", 12, self.red)
        self.yw.set_column("J:K", 12, self.green)
        self.yw.set_column("L:M", 12, self.red)
        self.yw.set_column("N:N", 12, self.green)
        
        # merge range and write
        self.yw.merge_range("A1:N1", "", self.blue) 
        self.yw.write_rich_string("A1", self.blue, "Years", self.ref_in, self.blue, self.ref_yr)
        self.yw.write("A2", "Years", self.blue)
        self.yw.write("B2", "Clients", self.blue)
        self.yw.write("C2", "Brought-Fs", self.blue)
        self.yw.write("D2", "Commissions", self.blue)
        self.yw.write("E2", "Savings", self.blue)
        self.yw.write("F2", "Debits")
        self.yw.write("G2", "Not-Paids", self.blue)
        self.yw.write("H2", "Upfronts")
        self.yw.write("I2", "P-Upfronts")
        self.yw.write("J2", "R-Upfronts")
        self.yw.write("K2", "Balances")
        self.yw.write("L2", "Deficits")
        self.yw.write("M2", "Excesses")
        self.yw.write("N2", "B-T-Os")
    
        ## Months Worksheet
        self.mw = self.years_wb.add_worksheet("Months Worksheet")
        
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
        self.aw = self.years_wb.add_worksheet("Areas Worksheet")
        
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

    def years_datas(self):
        count = 3
        for year in Years.years:
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
            
            data = year.datas()
            self.ones(data)
            self.yw.write(A, data[0])
            self.yw.write(B, data[2])
            self.yw.write(C, data[3])
            self.yw.write(D, data[4])
            self.yw.write(E, data[5])
            self.yw.write(F, data[6])
            self.yw.write(G, data[7])
            self.yw.write(H, data[8])
            self.yw.write(I, data[9])
            self.yw.write(J, data[10])
            self.yw.write(K, data[11])
            self.yw.write(L, data[12])
            self.yw.write(M, data[13])
            self.yw.write(N, data[14])

            count += 1

    def months_datas(self):
        count = 3
        for data in Regions.sum_months_in_years():
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
            self.mw.write(M, data[13])
            self.mw.write(N, data[14])

            count += 1

    def areas_datas(self):
        # Inputing data
        count = 3
        for data in Regions.sum_areas_in_years():
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




