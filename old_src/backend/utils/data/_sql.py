import sqlite3
from ...thrift.regions.years import Years
from ...thrift.regions.year import Year
from ...thrift.regions.month import Month
from ...thrift.regions.area import Area
from ...thrift.regions.client import Client
from ..sort.date import Date
from .regionals import Regionals
from .passwords.authorisation import Authorisation

class Sql:
    @classmethod
    def sq_con(cls, file_):
        con = sqlite3.connect(file_)
        cur = con.cursor()
        exc = cur.execute
        return [con, cur, exc]
    @classmethod
    def cl_db(cls, cl): return Regionals.client_reg(cl).values()
    @classmethod
    def db_cl(cls, tup): return Regionals.details_cl_dict(tup[-1])
    @classmethod
    def ar_db(cls, ar):
        d = Regionals.form_ar(ar)
        year = d["year_name"]
        month = d["month_name"]
        number = d["number"]
        details = Regionals.details_ar_str(d)
        r = (year, month, number, details)
        return r
    @classmethod
    def db_ar(cls, tup): return Regionals.details_ar_dict(tup[-1])
    @classmethod
    def yr_db(cls, yr):
        d = yr.__dict__
        year = d["name"]
        months_names = ""
        for month in yr: months_names += month.name + "^"
        months_names = months_names[:-1]
        r = (year, months_names)
        return r
    @classmethod
    def save_all(cls, tempfile):
        yrs = Years.years
        if yrs:
            con, cur, exc = cls.sq_con(tempfile)
            exc("CREATE TABLE IF NOT EXISTS years (year, months_names)")
            exc("CREATE TABLE IF NOT EXISTS areas (year, month, number, details)")
            exc("CREATE TABLE IF NOT EXISTS clients (year, month, area, number, name, rate, details)")
            exc("CREATE TABLE IF NOT EXISTS prmp (tab, style, pass, path, chart)")
            for yr in yrs:
                exc("INSERT INTO years VALUES (?,?)", cls.yr_db(yr))
                for mn in yr:
                    for ar in mn:
                        exc("INSERT INTO areas VALUES (?,?,?,?)", cls.ar_db(ar))
                        for cl in ar: exc("INSERT INTO clients VALUES (?,?,?,?,?,?,?)", tuple(cls.cl_db(cl)))
            _ = con.commit(), cur.close(), con.close()
    @classmethod
    def load_regions(cls, tempfile):
        con, cur, exc = cls.sq_con(tempfile)
        years = list(exc("SELECT * FROM years"))
        for year in years:
            year_name = year[0]
            # if year_name in Years.years_names: continue
            yr = Year(year_name, 1)
            months = year[1]
            months_names = months.split("^")
            total_months = len(months_names)
            for num in range(0, total_months):
                month_name = months_names[num]
                mn = Month(yr, month_name, 1)
                cmd = "SELECT * FROM areas WHERE year=? AND month=? ORDER BY number"
                areas = list(exc(cmd, (year_name, month_name)))
                for area in areas:
                    area_det = area[-1]
                    area_dict = Regionals.details_ar_dict(area_det)
                    ar = Area(mn, 1)
                    area_name = ar.name
                    ar.__dict__.update(area_dict)
                    cmd = "SELECT * FROM clients WHERE year=? AND month=? AND area=? ORDER BY number"
                    clients = list(exc(cmd, (year_name, month_name, area_name)))
                    for client in clients:
                        client_dict = cls.db_cl(client)
                        client_name = client_dict["name"]
                        client_rate = client_dict["rate"]
                        cl = Client(ar, client_name, client_rate, 1)
                        cl.__dict__.update(client_dict)
        _ = con.commit(), cur.close(), con.close()
    @classmethod
    def load_current_year(cls, tempfile):
        con, cur, exc = cls.sq_con(tempfile)
        years = list(exc("SELECT * FROM years WHERE year=?", (Date.get_year(),)))
        for year in years:
            year_name = year[0]
            if year_name in Years.years_names: continue
            yr = Year(year_name, 1)
            months = year[1]
            months_names = months.split("^")
            total_months = len(months_names)
            for num in range(0, total_months):
                month_name = months_names[num]
                mn = Month(yr, month_name, 1)
                cmd = "SELECT * FROM areas WHERE year=? AND month=? ORDER BY number"
                areas = list(exc(cmd, (year_name, month_name)))
                for area in areas:
                    area_name = area[2]
                    area_det = area[-1]
                    area_dict = Regionals.details_ar_dict(area_det)
                    ar = Area(mn, 1)
                    ar.__dict__.update(area_dict)
                    cmd = "SELECT * FROM clients WHERE year=? AND month=? AND area=? ORDER BY number"
                    clients = list(exc(cmd, (year_name, month_name, area_name)))
                    for client in clients:
                        client_dict = cls.db_cl(client)
                        client_name = client_dict["name"]
                        client_rate = client_dict["rate"]
                        cl = Client(ar, client_name, client_rate, 1)
                        cl.__dict__.update(client_dict)
        _ = con.commit(), cur.close(), con.close()
    
    @classmethod
    def update_user(cls, tempfile, action='', **kws):
        con, cur, exc = cls.sq_con(tempfile)
        if action == "add":
            ad = Authorisation.admin if kws.get("ad", False) else Authorisation.non_admin
            exc("INSERT INTO users VALUES (?,?,?,?)", (kws["usr"], kws["pwd"], ad))
        elif action == "delete": exc("DELETE ROW FROM users WHERE username=?", (kws["usr"],))
        elif action == "chg_pwd": exc("UPDATE ROW FROM users WHERE username=?, password=?", (kws["usr"], kws["pwd"]))
        elif action == "chg_usr": exc("UPDATE ROW FROM users WHERE username=?, username=?", (kws["form_usr"], kws["new_usr"]))
        elif action == "mk_ad": exc("UPDATE ROW FROM users WHERE username=?, admin=?", (kws["usr"], Authorisation.admin))
        elif action == "mk_nad": exc("UPDATE ROW FROM users WHERE username=?, admin=?", (kws["usr"], Authorisation.non_admin))
        
        _ = con.commit(), cur.close(), con.close()
    
    @classmethod
    def create_users_table(cls, tempfile):
        con, cur, exc = cls.sq_con(tempfile)
        exc("CREATE TABLE IF NOT EXISTS users (name, username, password, hint, permission)")
        exc("CREATE TABLE IF NOT EXISTS sup_users (name, username, password, hint, permission)")
        return [con, cur, exc]
    
    @classmethod
    def save_users_db(cls, tempfile):
        con, cur, exc = cls.create_users_table(tempfile)
        for user in Authorisation.users:
            name, usr, pwd, hint, ad = user.get_hash()
            exc("INSERT INTO users VALUES (?,?,?,?,?)", (name, usr, pwd, hint, ad))
        for user in Authorisation.super_users:
            name, usr, pwd, hint, ad = user.get_hash()
            exc("INSERT INTO sup_users VALUES (?,?,?,?,?)", (name, usr, pwd, hint, ad))
        _ = con.commit(), cur.close(), con.close()
    @classmethod
    def load_users_db(cls, tempfile):
        con, cur, exc = cls.create_users_table(tempfile)
        users = []
        for user in list(exc("SELECT * FROM users")):
            users_ = []
            for au in user: users_.append(au)
            users.append(users_)
        Authorisation.load_users(users)
        
        super_users = []
        for user in list(exc("SELECT * FROM sup_users")):
            users_ = []
            for au in user: users_.append(au)
            super_users.append(users_)
        Authorisation.load_super_users(super_users)

        _ = con.commit(), cur.close(), con.close()
    
    


