from .regions import Regions
from .weeks import Weeks
from .days import Days


class Chart_Sort:
    records = ["clnt", "brf", "com", "sav", "deb", "not_paid", "upf", "pupf", "rupf", "bal", "def", "exc", "bto"]
    class_xticks = ["Clients", "Brought-F", "Commissions", "Savings", "Debits", "Not-Paids", "Upfronts", "P-Upfronts", "R-Upfronts", "Balances", "Deficits", "Excesses", "B-T-Os"]
    def __init__(self, region, yaxis, month=None, area=None, week=None, day=None, spec=None, sole="", header=None):
        self.go = 0
        self.plot_data_sort(region, yaxis, area=area, sole=sole, month=month, header=header, week=week, day=day)


    def get_labels(self, yaxis):
        labels = []
        ck = self.class_xticks
        if self.records[0] in yaxis: labels.append(ck[0])
        if self.records[1] in yaxis: labels.append(ck[1])
        if self.records[2] in yaxis: labels.append(ck[2])
        if self.records[3] in yaxis: labels.append(ck[3])
        if self.records[4] in yaxis: labels.append(ck[4])
        if self.records[5] in yaxis: labels.append(ck[5])
        if self.records[6] in yaxis: labels.append(ck[6])
        if self.records[7] in yaxis: labels.append(ck[7])
        if self.records[8] in yaxis: labels.append(ck[8])
        if self.records[9] in yaxis: labels.append(ck[9])
        if self.records[10] in yaxis: labels.append(ck[10])
        if self.records[11] in yaxis: labels.append(ck[11])
        if self.records[12] in yaxis: labels.append(ck[12])
        if len(yaxis) == 1: return labels[0]
        else: return labels

    def plot_data_sort(self, region, yaxis, month=None, area=None, week=None, day=None, spec=None, sole="", header=None):
        sub_regions = []
        columns = []
        ## sub_Ys
        clnt = []
        brf = []
        com = []
        sav = []
        deb = []
        not_paid = []
        upf = []
        pupf = []
        rupf = []
        bal = []
        def_ = []
        exc = []
        bto = []
        ## X_ticks
        xticks = []
        ## Labels
        labels = self.get_labels(yaxis)
        ## Real Ys
        ys = []
        ## Getting the sub_regions
        if region.which == "years":
            if month: sub_regions = Regions.same_months_in_years(month)
            elif header == "months":
                columns = Regions.sum_months_in_years()
                for column in columns: del column[1]
            elif header == "areas": columns = Regions.sum_areas_in_years()
            else: sub_regions = region.years

        elif region.which == "year":
            if area:
                sub_regions = Regions.same_areas_in_year(region, area)
            elif header == "areas": columns = Regions.sum_areas_in_year(region)
            else: sub_regions = region.months

        elif region.which == "month":
            if header == "areas":
                areas = region.areas
                for area in areas:
                    if day: column = Days.day_column(area, day)

                    elif week: column = Weeks.week_column(area, week)

                    else: column = area.datas()
                    columns.append(column)

            elif header == "weeks": columns = list(Weeks.weekly_sort(region))
            elif header == "days":
                columns = list(Days.daily_sort(region, week=week))
                for column in columns: del column[0]
            elif week:
                column = Weeks.week_column(region, week)
                self.xticks = self.class_xticks
                self.ys = column[1:]
                self.labels = column[0]
                self.go = 1
                return
            elif day:
                column = Days.day_column(region, day)
                self.xticks = self.class_xticks
                self.ys = column[1:]
                self.labels = column[0]
                self.go = 1
                return

        elif region.which == "area":
            if header == "areas": sub_regions = region.areas
            elif header == "weeks": columns = Weeks.weekly_sort(region)
            elif header == "days": columns = Days.daily_sort(region, week=week)

        ## Sorting the required records for ploting
        if sole == "1":
            num = 1
            self.xticks = self.class_xticks
            if region.which in ["year", "month"]: num = 2
            datas = region.datas()
            self.ys = datas[num:]

            self.labels = datas[0]
            self.go = 1
            return

        elif sub_regions:
            for sub_region in sub_regions:
                if month: xticks.append(sub_region.year_name)
                elif area:
                    if sub_region.which == "year": xticks.append(sub_region.name)
                    else: xticks.append(sub_region.month_name)
                else: xticks.append(sub_region.name)

                if self.records[0] in yaxis: clnt.append(sub_region.total_clients)

                if self.records[1] in yaxis: brf.append(sub_region.brought_forwards)

                if self.records[2] in yaxis: com.append(sub_region.commissions)

                if self.records[3] in yaxis: sav.append(sub_region.savings)

                if self.records[4] in yaxis: deb.append(sub_region.debits)

                if self.records[5] in yaxis: not_paid.append(sub_region.not_paids)

                if self.records[6] in yaxis: upf.append(sub_region.upfronts)

                if self.records[7] in yaxis: pupf.append(sub_region.p_upfronts)

                if self.records[8] in yaxis: rupf.append(sub_region.r_upfronts)

                if self.records[9] in yaxis: bal.append(sub_region.balances)

                if self.records[10] in yaxis: def_.append(sub_region.deficits)

                if self.records[11] in yaxis: exc.append(sub_region.excesses)

                if self.records[12] in yaxis: bto.append(sub_region.btos)

        elif columns:
            for data in columns:
                xticks.append(data[0])
                if self.records[0] in yaxis: clnt.append(data[1])

                if self.records[1] in yaxis: brf.append(data[2])

                if self.records[2] in yaxis: com.append(data[3])

                if self.records[3] in yaxis: sav.append(data[4])

                if self.records[4] in yaxis: deb.append(data[5])

                if self.records[5] in yaxis: not_paid.append(data[6])

                if self.records[6] in yaxis: upf.append(data[7])

                if self.records[7] in yaxis: pupf.append(data[8])

                if self.records[8] in yaxis: rupf.append(data[9])

                if self.records[9] in yaxis: bal.append(data[10])

                if self.records[10] in yaxis: def_.append(data[11])

                if self.records[11] in yaxis: exc.append(data[12])

                if self.records[12] in yaxis: bto.append(data[13])

        if columns or sub_regions:
            for y in [clnt, brf, com, sav, deb, not_paid, upf, pupf, rupf, bal, def_, exc, bto]:
                if y: ys.append(y)

            self.xticks = xticks
            # print('xticks', xticks)
            # print('ys', ys)
            # print('labels', labels)

            if len(yaxis) == 1: self.ys = ys[0]
            else: self.ys = ys

            self.labels = labels
            self.go = 1




