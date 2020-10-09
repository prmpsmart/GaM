

class Regionals:
    
    @classmethod
    def form_cl(cls, cl):
        "streamline the dumpable parts of the client __dict__"
        dic = cl.__dict__.copy()
        for _ in ["area", "month", "year"]: del dic[_]
        return dic
        
    @classmethod
    def form_ar(cls, ar):
        "streamline the dumpable parts of the area __dict__"
        dic = {}
        for _ in ["number", "name", "month_name", "year_name", "btos", "btos_dates", "deficits", "deficits_dates", "excesses", "excesses_dates"]: dic[_] = ar.__dict__[_]
        return dic
        
    @classmethod
    def client_reg(cls, cl):
        d = cls.form_cl(cl)
        res = {}
        res["year_name"] = d["year_name"]
        res["month_name"] = d["month_name"]
        res["area_number"] = d["area_number"]
        res["number"] = d["number"]
        res["name"] = d["name"]
        res["rate"] = d["rate"]
        res["details"] = cls.details_cl_str(d)
        return res
        
    @classmethod
    def dets_str(cls, dict_):
        "converting dict to str"
        str_ = ""
        for key in dict_:
            if isinstance(dict_[key], int): str_ += "%s:%d,"%(key, dict_[key])
            elif isinstance(dict_[key], str): str_ += "%s:%s,"%(key, dict_[key])
        return str_[:-1]
        
    @classmethod
    def dets_dict(cls, str_):
        "converting str to dict"
        dict_ = {}
        lists = str_.split(",")
        for dic in lists:
            a, b = dic.split(":")
            try: dict_[a] = int(b)
            except: dict_[a] = b
        return dict_
        
    @classmethod
    def det_date_str(cls, dict_):
        "converting nested dict dates to str"
        str_ = ""
        for key in dict_:
            if isinstance(dict_[key], dict):
                str_ += "%s~%s#"%(key, cls.dets_str(dict_[key]) if dict_[key] else "{}")
        return str_[:-1]
        
    @classmethod
    def det_date_dict(cls, str_):
        "converting nested str dates to dict"
        dict_ = {}
        lists = str_.split("#")
        for dic in lists:
            a, b = dic.split("~")
            dict_[a] = cls.dets_dict(b) if b != "{}" else {}
        return dict_
        
    @classmethod
    def dets_litu_str(cls, dict_):
        str_ = ""
        for key in dict_:
            if isinstance(dict_[key], list):
                key_str = "%s@"%key
                for tup in dict_[key]: key_str += "%s:%s,"%tuple(tup)
                str_ += "%s$"%key_str
        return str_[:-2]
        
    @classmethod
    def dets_str_litu(cls, str_):
        dict_ = {}
        lists = str_.split("$")
        for li in lists:
            key, val = li.split("@")
            list_ = []
            vals = val.split(",")
            for v in vals:
                if v: list_.append(tuple(v.split(":")))
            dict_[key] = list_
        return dict_
        
    @classmethod
    def details_cl_str(cls, dict_):
        amnt = cls.dets_str(dict_)
        date = cls.det_date_str(dict_)
        litu = cls.dets_litu_str(dict_)
        return "%s^%s^%s"%(amnt, date, litu)
        
    @classmethod
    def details_cl_dict(cls, str_):
        a, b, c = str_.split("^")
        amnt = cls.dets_dict(a)
        date = cls.det_date_dict(b)
        litu = cls.dets_str_litu(c)
        date.update(litu)
        amnt.update(date)
        return amnt
        
    @classmethod
    def details_ar_str(cls, dict_):
        amnt = cls.dets_str(dict_)
        date = cls.det_date_str(dict_)
        return "%s^%s"%(amnt, date)
 
    @classmethod
    def details_ar_dict(cls, str_):
        a, b = str_.split("^")
        amnt = cls.dets_dict(a)
        date = cls.det_date_dict(b)
        amnt.update(date)
        return amnt
    
    @classmethod
    def details_str(cls, region):
        if region.which == "client": return cls.details_cl_str(region.__dict__)
        elif region.which == "area": return cls.details_ar_str(region.__dict__)
        
    @classmethod
    def details_dict(cls, str_):
        if "rate" in str_: return cls.details_cl_dict(str_)
        elif "bto" in str_: return cls.details_ar_dict(str_)
        
    @classmethod
    def comp_dict(cls, d1, d2, pr=0):
        go = 0
        try: d1.get("None", None); go = 1
        except:
            try: d1 = d1.__dict__; go = 1
            except: print("First arg isn't a dict object")
        try: d2.get("None", None); go = 1
        except:
            try: d2 = d2.__dict__; go = 1
            except: print("Second arg isn't a dict object")
        t1, f1 = 0, 0
        t2, f2 = 0, 0
        for key in d1:
            if d1[key] == d2[key]: t1 += 1
            else:
                f1 += 1
                if pr: print("{0} ->  {1} <>  {2} \n".format(key, d1[key], d2[key]))
        #print("NEXT")
        for key in d2:
            if d2[key] == d1[key]: t2 += 1
            else: f2 += 1
        return [(t1, f1), (t2, f2)]
