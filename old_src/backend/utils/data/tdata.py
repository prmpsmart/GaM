from ._sql import Sql, Authorisation
# from ._xml import Xml
from .path import Path, os
from ..debug.debug import Debug
from ..sort.date import Date
from ..details.tdetails import TDetails
from ..sort.thrift.regions import Years
from ..sort.thrift.regions import Saving_Daily
from ....gui.tkinter.utils.decorate.styles import Styles
from ....gui.tkinter.utils.visuals.table import Table
from ....gui.tkinter.utils.decorate.styles import Styles
from ....gui.tkinter.utils.visuals.table import Table
import pickle, time, zlib
import threading

from datetime import datetime

#### DATA 
class TData:
    usedb = False
    going = False
    loaded = False
    wanted = ["agam_prmp.picdb", "agam_dailies.picdb", "agam_years.picdb", "agam_prmp.sqldb", "agam_current.picdb", "agam_years.xmldb", "agam_calc_history.txt"]
    @classmethod
    def delete(cls, file):
        try: os.remove(file)
        except Exception as e: print(e)
    
    @classmethod
    def delete_junks(cls):
        print("CLEANING")
        try:
            time.sleep(1)
            database = Path.database()
            for fil in os.listdir(database):
                path = os.path.join(database, fil)
                if fil not in cls.wanted:
                    try: cls.delete(path)
                    except Exception as e: print(e)
            return 1
        except Exception as e: print(e)
    @classmethod
    def save_data(cls):
        if cls.going == True: pass
        else:
            TDetails.update()
            try:
                print("Start Save", datetime.now())
                threading.Thread(target=cls.save_users_db).start()
                threading.Thread(target=cls.save_current).start()
                
                cls.save_other_datas()
                cls.save_pic()
                cls.save_daily_thrifts()
                print("End Save", datetime.now())
            except Exception as e: print(e)
            # finally: cls.delete_junks()
        
    @classmethod
    def load_data(cls, wh=None):
        if not cls.loaded:
            if wh:
                if os.environ.get("PRMP_TK", None) == "RUNNING": cls.load_data()
            else:
                try: 
                    print(datetime.now())
                    threading.Thread(target=cls.load_current).start()
                    threading.Thread(target=cls.load_users_db).start()
                    cls.load_other_datas()
                    cls.load_daily_thrifts()
                    cls.load_pic()
                    cls.delete_junks()
                    print(datetime.now())
                except Exception as e: print(e)
                finally: cls.loaded = True

    @classmethod
    def save_users_db(cls):
        sql_file = Path.get_save_sql()
        tempfile = Path.temp_filename()
        try:
            Sql.save_users_db(tempfile)
            with open(tempfile, "rb") as temp:
                with open(sql_file, "wb") as ys_pf:
                    raw_data = temp.read()
                    en_data = zlib.compress(raw_data)
                    # print(raw_data)
                    ys_pf.write(en_data)
        except Exception as e: print(e)
        finally: cls.delete(tempfile)
        Path.current_files.remove(tempfile)

    @classmethod
    def load_users_db(cls):
        sql_file = Path.get_save_sql()
        tempfile = Path.temp_filename()
        try:
            with open(sql_file, "rb") as ys_pf: de_data = zlib.decompress(ys_pf.read())
            with open(tempfile, "wb") as temp: temp.write(de_data)
            Sql.load_users_db(tempfile)
        except Exception as e: print(e)
        finally: cls.delete(tempfile)
        Path.current_files.remove(tempfile)

    @classmethod
    def save_pic(cls):
        years_file = Path.get_save_picdb()
        tempfile = Path.temp_filename()
        if Years.years:
            with open(tempfile, "wb")as temp:
                for yr in Years.years: pickle.dump(yr, temp)
            with open(tempfile, "rb") as temp: data_ = temp.read()
            with open(years_file, "wb") as ys_pf: ys_pf.write(zlib.compress(data_))
            cls.delete(tempfile)# cls.delete_junks()
        Path.current_files.remove(tempfile)
    @classmethod
    def load_pic(cls):
        cls.going = True
        tempfile = Path.temp_filename()
        years_file = Path.get_save_picdb()
        try:
            with open(years_file, "rb") as ys_pf: en_data = ys_pf.read()
            with open(tempfile, "wb") as temp: temp.write(zlib.decompress(en_data))
            with open(tempfile, "rb") as temp:
                while True:
                    try:
                        year = pickle.load(temp)
                        if year.name in Years.years_names: continue
                        Years.add(year)
                    except EOFError: break
            cls.going = False
        except Exception as e:
            cls.going = False
            print(e)
        finally: cls.delete(tempfile)
        Path.current_files.remove(tempfile)
    @classmethod #new
    def save_current(cls):
        cur_file = Path.get_current_thf()
        tempfile = Path.temp_filename()
        cur_year = Years.get(Date.get_year())
        if cur_year:
            with open(tempfile, "wb")as temp: pickle.dump(cur_year, temp)
            with open(tempfile, "rb") as temp: data_ = temp.read()
            with open(cur_file, "wb") as ys_pf: ys_pf.write(zlib.compress(data_))
            cls.delete(tempfile)
        Path.current_files.remove(tempfile)
    @classmethod #new
    def load_current(cls, wh=None):
        if wh == "reload":
            if os.environ.get("PRMP_TK") == "RUNNING": cls.load_data()
        else:
            tempfile = Path.temp_filename()
            years_file = Path.get_current_thf()
            try:
                with open(years_file, "rb") as ys_pf: en_data = ys_pf.read()
                with open(tempfile, "wb") as temp: temp.write(zlib.decompress(en_data))
                with open(tempfile, "rb") as temp: Years.add(pickle.load(temp))
            except Exception as e: print(e)
            finally: cls.delete(tempfile)
            Path.current_files.remove(tempfile)
    @classmethod
    def save_daily_thrifts(cls):
        try:
            dailies_file = Path.get_save_dailies()
            tempfile = Path.temp_filename()
            with open(tempfile, "wb") as temp:
                for ar in Saving_Daily.area_dailies: pickle.dump(ar, temp, protocol=2)
            with open(tempfile, "rb") as temp: data_ = temp.read()
            with open(dailies_file, "wb") as ds_pf: ds_pf.write(zlib.compress(data_))
        except Exception as e: print(e)
        finally:
            Path.current_files.remove(tempfile)
            cls.delete(tempfile)
    @classmethod
    def load_daily_thrifts(cls):
        tempfile = Path.temp_filename()
        dailies_file = Path.get_save_dailies()
        try:
            with open(dailies_file, "rb") as ds_pf: en_data = ds_pf.read()
            with open(tempfile, "wb") as temp: temp.write(zlib.decompress(en_data))
            with open(tempfile, "rb") as temp:
                while True:
                    try:
                        area = pickle.load(temp)
                        Saving_Daily.add(area)
                    except EOFError: break
        except Exception as e: print(e)
        finally: cls.delete(tempfile)
        Path.current_files.remove(tempfile)
    @classmethod
    def save_other_datas(cls):
        try:
            prmp_file = Path.prmp_data()
            tempfile = Path.temp_filename()
            dict_data = {"style": Styles.get_state(), 
                         "path": Path.get_state(), 
                         "table": Table.get_state(), 
                        }
        
            with open(tempfile, "wb") as temp: pickle.dump(dict_data, temp)
            with open(tempfile, "rb") as temp: data_ = temp.read()
            with open(prmp_file, "wb") as ds_pf: ds_pf.write(zlib.compress(data_))
        except Exception as e: print(e)
        finally:
            Path.current_files.remove(tempfile)
            cls.delete(tempfile)
    @classmethod
    def load_other_datas(cls):
        
        prmp_file = Path.prmp_data()
        tempfile = Path.temp_filename()
        try:
            with open(prmp_file, "rb") as ds_pf: en_data = ds_pf.read()
            with open(tempfile, "wb") as temp: temp.write(zlib.decompress(en_data))
            with open(tempfile, "rb") as temp: data_ = pickle.load(temp)
            Styles.load_state(data_["style"])
            Path.load_state(data_["path"])
            Table.load_state(data_["table"])
            
        except Exception as e: print(e)
        finally: cls.delete(tempfile)
        Path.current_files.remove(tempfile)
#### DATA

