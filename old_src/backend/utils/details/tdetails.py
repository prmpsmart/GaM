from ...thrift.regions.years import Years
from ..debug.debug import Debug
from ..sort.date import Date

class TDetails:
    "Everything about Details"
    
    @classmethod
    def update(cls):
        year = Years.get(Date.get_year())
        if year:
            for month in year:
                for area in month:
                    for client in area: client.update(1)
                    area.update(1)
                month.update(1)
            year.update(1)
        Years.update()

    @classmethod
    def mul_1000(cls, num):
        div = 3
        str_num = str(num)
        num_list = list(str_num)
        num_len = len(str_num)
        num_rem = num_len % div
        num_div = num_len // div
        
        if not num_rem: num_div -= 1
        
        co, to = -3, 0
        
        for _ in range(num_div):
            num_list.insert(co - to, ",")
            co -= 3
            to += 1
        return "".join(num_list)
    @classmethod
    def mul_1000s(cls, lists):
        for a in lists:
            ind = lists.index(a)
            if isinstance(a, int): lists[ind] = cls.mul_1000(a)
    @classmethod
    def ints(cls, lists):
        for a in lists:
            ind = lists.index(a)
            if cls.isnumeric(a): lists[ind] = int(a)
    @classmethod
    def isnumeric(cls, num):
        try: int(num); return True
        except: return False
