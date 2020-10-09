from ...utils.debug.debug import Debug
from ...utils.sort.thrift.weeks import Weeks
from ...utils.sort.date import Date
import random

class Area:
    "The Area where clients belong"
    which = "area"
    def __init__(self, month, sole=0):
       # Records
        self.commissions = 0
        self.debits = 0
        self.brought_forwards = 0
        self.upfronts = 0
        self.r_upfronts = 0
        self.p_upfronts = 0
        self.savings = 0
        self.not_paids = 0
        self.balances = 0
        self.total_clients = 0
        self.btos = 0
        self.excesses = 0
        self.deficits = 0
       # Details
        self.clients = []
        self.clients_names = []
        self.month = month
        self.number, self.name = self.month.add(self)
        self.month_name = self.month.name
        self.year = self.month.year
        self.year_name = self.year.name
       # Dates
        self.commissions_dates = {}
        self.debits_dates = {}
        self.savings_dates = {}
        self.upfronts_dates = {}
        self.not_paids_dates = {}
        self.balances_dates = {}
        self.clients_dates = {}
        self.brought_forwards_dates = {}
        self.r_upfronts_dates = {}
        self.p_upfronts_dates = {}
        self.btos_dates = {}
        self.excesses_dates = {}
        self.deficits_dates = {}
       #
        if not sole: self.month.update()
       
    # Details
    
    def __trunc__(self): return int(self.number)
    def __repr__(self): return self.name + " | " + repr(self.month)
    def __str__(self): return self.name + " | " + str(self.month)
    def __getitem__(self, num): return self.clients[num]
    def __len__(self): return self.total_clients
    def __bool__(self): return True
    
    def datas(self): return [self.name, self.total_clients, self.brought_forwards, self.commissions, self.savings, self.debits, self.not_paids, self.upfronts, self.p_upfronts, self.r_upfronts, self.balances, self.deficits, self.excesses, self.btos]
    
    def delete(self, up=False):
        ln, msg = 53, str(self) + " DELETED"
        if up: self.month.delete_area(self)
        for client in self.clients: client.delete()
        del self
        Debug.print_bug(ln, msg, file=__file__)
    def add_client(self, client):
        self.clients.append(client)
        self.total_clients = len(self.clients)
        return self.total_clients

    def delete_client(self, client, sole=0):
        self.clients.remove(client)
        self.update(sole)
        
    def add_bto(self, bto, sole=0):
        date = Date.date(form=1)
        self.btos_dates[date] = bto
        self.btos += bto
        # saving = self.savings_dates[date]
        try: saving = self.savings_dates[date]
        except: saving = random.randrange(4000, 50000, 500)
        if saving < bto: self.__add_excess(bto - saving, date)
        elif saving > bto: self.__add_deficit(saving - bto, date)
        self.update(sole)

    def __add_excess(self, excess, date):
        self.excesses_dates[date] = excess
        self.excesses += excess

    def __add_deficit(self, deficit, date):
        self.deficits_dates[date] = deficit
        self.deficits += deficit
    
    
    def update(self, sole=0):
        if self.clients:
            self.total_clients = len(self.clients)
            self.clients_names = [client.name for client in self.clients]
            self.commissions = sum([client.rate for client in self.clients])
            self.debits = sum([client.debit for client in self.clients])
            self.brought_forwards = sum([client.brought_forward for client in self.clients])
            self.balances = sum([client.balance for client in self.clients])
            self.upfronts = sum([client.upfront for client in self.clients])
            self.r_upfronts = sum([client.r_upfront for client in self.clients])
            self.p_upfronts = sum([client.p_upfront for client in self.clients])
            self.savings = sum([client.savings for client in self.clients])
            self.not_paids = sum([client.not_paid for client in self.clients])
            self.clients_names = [client.name for client in self.clients]
            self.total_clients = len(self.clients)
            
            Weeks.update_area_dates(self)
        
            if not sole: self.month.update()
    
    def get(self, name):
        for client in self.clients:
            if client.name == name: return client

