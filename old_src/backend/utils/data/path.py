from ..debug.debug import Debug
import string, random, os

class Path:
    
    current_files = []
    save_dir = None
    _database = ''
    
    def __init__(self, save): Path._database = save
    
    @classmethod
    def join(cls, root, last): return os.path.join(root, last)
    @classmethod
    def ext_det(cls, ext):
        if ext == "picdb": return ".picdb"
        elif ext == "xmldb": return ".xmldb"
        elif ext == "sqldb": return ".sqldb"
        elif ext == "xlsx": return ".xlsx"
        elif ext == "ico": return ".ico"
        else:
            message = "File Extension is either picdb or xmldb or sqldb or xlsx or ico"
            line = 24
            Debug.print_bug(line, message, file=__file__)
    @classmethod
    def check_path(cls, df_path): return os.path.exists(df_path)
    @classmethod
    def confirm_path(cls, df_path):
        if os.path.isdir(df_path): return "dir"
        elif os.path.isfile(df_path): return "file"
        else: return False
    @classmethod
    def dir_creator(cls, root, folder):
        dir_path = cls.join(root, folder)
        if cls.confirm_path(dir_path) != "dir":
            try: os.mkdir(dir_path)
            except:
                try: os.makedirs(dir_path)
                except: pass
        else: pass#Debug.print_bug("Directory exists")
        return (dir_path)
    @classmethod
    def database(cls):
        save_root = "database"
        cwd = os.getcwd()
        a = os.path.basename(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        if a == "src": root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        else: root_dir = cwd
        database_ = cls.join(root_dir, save_root)
        
        if cls._database: database_ = cls._database
        if cls.confirm_path(database_) != "dir":
            try: os.mkdir(database_)
            except Exception as e:
                print(e)
                os.makedirs(database_)
        return database_

    @classmethod
    def set_save_dir(cls, path, file=None):
        if cls.confirm_path(path) == "dir":
            cls.save_dir = path
            return 1
        else:
            message = "Path provided is invalid " + str(file)
            line = 64
            Debug.print_bug(line, message, file=__file__)
            return 0

    @classmethod
    def get_save_dir(cls):
        if cls.save_dir != None:
            pat = os.path.join(cls.save_dir, "Thrift")
            try: os.makedirs(pat)
            except: pass
            return pat
    @classmethod
    def calc_history(cls): return cls.join(cls.database(), "agam_calc_history.txt")
    @classmethod
    def get_save_picdb(cls): return cls.join(cls.database(), "agam_years.picdb")
    @classmethod
    def get_current_thf(cls): return cls.join(cls.database(), "agam_current.picdb")
    @classmethod
    def get_save_sql(cls): return cls.join(cls.database(), "agam_prmp.sqldb")
    @classmethod
    def get_save_xml(cls): return cls.join(cls.database(), "agam_years.xmldb")
    @classmethod
    def get_save_dailies(cls): return cls.join(cls.database(), "agam_dailies.picdb")
    
    
    @classmethod
    def year_dir(cls, year):
        save_dir = cls.get_save_dir()
        if save_dir:
            year_save_dir = cls.dir_creator(save_dir, year.name)
            return year_save_dir
        else:
            message = "Saving Directory not set"
            line = 101
            Debug.print_bug(line, message, file=__file__)
    @classmethod
    def month_dir(cls, month):
        year = month.year
        if year:
            year_path = cls.year_dir(year)
            if year_path:
                month_path = cls.dir_creator(year_path, month.name)
                return month_path
    @classmethod
    def area_dir(cls, area):
        month = area.month
        if month:
            month_path = cls.month_dir(month)
            if month_path:
                area_path = cls.dir_creator(month_path, area.name)
                return area_path
    # Workbooks
    @classmethod
    def years_file(cls, ext=None):
        file_ext = cls.ext_det(ext)
        if file_ext:
            years_file_name = "Years" + file_ext
            years_file_path = cls.join(cls.get_save_dir(), years_file_name)
            return years_file_path
    @classmethod
    def year_file(cls, year, ext=None):
        file_ext = cls.ext_det(ext)
        if ext == "xlsx" or ext == "txt":
            if file_ext:
                year_file_name = year.name + file_ext
                year_path = cls.year_dir(year)
                year_file_path = cls.join(year_path, year_file_name)
                return year_file_path
        elif ext == "rm_thf":
            if file_ext:
                year_file_name = year.name + file_ext
                year_file_path = cls.join(cls.database(), year_file_name)
                return year_file_path
    @classmethod
    def month_file(cls, month, ext=None):
        file_ext = cls.ext_det(ext)
        if file_ext:
            month_file_name = month.name + file_ext
            month_path = cls.month_dir(month)
            month_file_path = cls.join(month_path, month_file_name)
            return month_file_path
    @classmethod
    def area_file(cls, area, ext=None):
        file_ext = cls.ext_det(ext) if ext != "dxlsx" else " DWB.xlsx"
        if file_ext:
            area_file_name = area.name + file_ext
            area_path = cls.area_dir(area)
            if area_path:
                area_file_path = cls.join(area_path, area_file_name)
                return area_file_path
    @classmethod
    def temp_filename(cls):
        alphabet = string.ascii_letters + string.digits
        temp = "".join(random.choice(alphabet) for i in range(10))
        file = cls.join(cls.database(), temp)
        if file not in cls.current_files:
            cls.current_files.append(file)
            return file
        else: return cls.temp_filename()
    
    tempfile = temp_filename

    @classmethod
    def prmp_data(cls): return cls.join(cls.database(), "agam_prmp.picdb")
    
    @classmethod
    def get_state(cls): return cls(cls.save_dir)
    @classmethod
    def load_state(cls, imageobj):
        if isinstance(imageobj, cls): cls.save_dir = imageobj.save_dir




