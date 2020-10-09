from .data.tdata import TData, Years, threading
from .data.workbook.workbook import Workbook


class Threads:

    @classmethod
    def run(cls, func, *args):
        thread = threading.Thread(target=func, args=args) if args else threading.Thread(target=func)
        thread.start()
    
    @classmethod
    def save_sql(cls): cls.run(TData.save_sql)
    @classmethod
    def load_sql(cls): cls.run(TData.load_sql)
    @classmethod
    def save_passwords(cls): cls.run(TData.save_users_db)
    @classmethod
    def load_passwords(cls): cls.run(TData.load_users_db)
    @classmethod
    def save_xml(cls): cls.run(TData.save_xml)
    @classmethod
    def load_xml(cls): cls.run(TData.load_xml)
    @classmethod
    def save_data(cls): cls.run(TData.save_data)
    @classmethod
    def load_data(cls, arg=None): cls.run(TData.load_data, arg)
    @classmethod
    def save_pic(cls): cls.run(TData.save_pic)
    @classmethod
    def load_pic(cls): cls.run(TData.load_pic)
    @classmethod
    def save_other_datas(cls): cls.run(TData.save_other_datas)
    @classmethod
    def save_current(cls): cls.run(TData.save_current)
    @classmethod
    def load_current(cls): cls.run(TData.load_current)
    @classmethod
    def load_other_datas(cls): cls.run(TData.load_other_datas)
    @classmethod
    def save_daily_thrifts(cls): cls.run(TData.save_daily_thrifts)
    @classmethod
    def load_daily_thrifts(cls): cls.run(TData.load_daily_thrifts)


    
