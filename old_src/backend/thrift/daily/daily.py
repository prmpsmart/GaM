

class Daily:
    def __repr__(self): return f"{self.area_daily} | {self.date}"
    def __str__(self): return f"{self.area_daily} | {self.date}"
    
    def __init__(self, area_daily, area, date):
        self.area_daily = area_daily
        self.area = area
        self.date = date
        self.datas = []
        self.s_n = 0
        self.bto = 0
        self.excess = 0
        self.deficit = 0
        self.total_savings = 0
        self.total_debits = 0
        self.total_upfronts = 0
        self.clients = []
        self.client_updated = False
        self.area_updated = False
        self.updated = False

    def delete(self, num):
        if num <= len(self.datas):
            num -= 1
            dt = self.datas[num]
            number = dt[0]
            savings = dt[5]
            debit = dt[6]
            upfront = dt[7]
            self.clients.remove(dt[1])
            del self.datas[num]
            
            self.s_n -= 1
            self.total_savings -= savings
            self.total_debits -= debit
            self.total_upfronts -= upfront
            
            for data in self.datas[number-1:]:
                data[0] -= 1
                data[-3] -= savings
                data[-2] -= debit
                data[-1] -= upfront

    def totate(self, bto):
        shu_bto = self.total_savings + self.total_upfronts - self.total_debits
        if bto < shu_bto: self.deficit = shu_bto - bto
        else: self.excess = bto - shu_bto

    def add(self, client, thrift=0, debit=0):
        if client not in self.clients:
            if client and thrift or debit:
                self.clients.append(client)
                self.s_n += 1
                savings = upfront = 0
                rate = client.rate
                old_thrifts = client.thrifts
                old_savings = client.savings
                today_thrift = thrift
                today_debit = debit
                self.total_debits += debit
                
                if client.p_upfront > 0:
                    upfront = rate * today_thrift
                    self.total_upfronts += upfront
                else:
                    savings = rate * today_thrift
                    self.total_savings += savings
                
                data = [self.s_n, client, rate, old_thrifts, today_thrift, savings, today_debit, upfront, self.total_savings, self.total_debits, self.total_upfronts]
                
                self.datas.append(data)

    def add_bto(self, bto): self.bto = bto

    def update_clients(self):
        for data in self.datas:
            client = data[1]
            thrift = data[4]
            debit = data[6]
            
            client.add_thrift(thrift)
            client.add_debit(debit)

    def check_client(self, client, thrift=0, debit=0):
        thf = 0
        deb = 0

        if thrift: thf = client.addable("thrift", thrift)
        if debit: deb = client.addable("debit", debit)
        
        if thf and deb: return 11
        elif thf: return 1
        elif deb: return 2
        else: return 0
    
    def update_area_bto(self): self.area.add_bto(self.bto)
    
    def update(self):
        if self.client_updated != True:
            self.update_clients()
            self.client_updated = True
        if self.area_updated != True and self.bto != 0:
            self.update_area_bto()
            self.area_updated = True
        
        if self.client_updated and self.area_updated: self.updated = True

