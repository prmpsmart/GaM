import hashlib, zlib, base64


class Auths_Vars:
    
    admin = b'eJwrzk0sKgEABnMCKA=='
    non_admin = b'eJwryczNzEnNyMwDABL+A8Q='
    
    admin_text = b'eJxzdPH19AMABCEBag=='
    non_admin_text = b'eJzz8/fTdXTx9fQDAAyLAoI='
    
    empty = b'eJwDAAAAAAE='
    wrong_pass = b'eJwLL8rPS1cISCwuLs8vSgEAKDcFgQ=='
    no_user = b'eJzzy1dILi0qSs0rUQgtTi0CACvfBaA='
    
    insufficient = b'eJzzzCsuTUvLTM5MzStRyEnNSy/JUMhPUygtTi3KS8xNVcgvUihILC4uzy9KAQBsAhCT'
    added = b'eJxzTElJTVEILk1OTi0uTivNyakEAD41Bvg='
    pass_changed = b'eJwLSCwuLs8vSlFIzkjMS09NUQguTU5OLS5OK83JqQQAp8YLYw=='
    user_changed = b'eJwLLU4tykvMTVVIzkjMS09NUQguTU5OLS5OK83JqQQApi0LUA=='
    del_super = b'eJxzTsxTL1FISc1JLUlVCC4tSC2KDy1OLSoGAGkdCOE='
    login_successful = b'eJzzyU/PzFMILk1OTi0uTivNAQAy6QY6'

    
    @classmethod
    def get_permission(cls, admin):
        if admin == True: return [cls.admin, cls.get_admin_text()]
        elif admin == False: return [cls.non_admin, cls.get_non_admin_text()]
        elif admin == cls.admin: return [True, cls.get_admin_text()]
        elif admin == cls.non_admin: return [False, cls.get_non_admin_text()]
        elif admin == cls.admin_text: return cls.get_admin_text()
        elif admin == cls.non_admin_text: return cls.get_non_admin_text()
    
    @classmethod
    def not_exist(cls, usr): return "User %s doesn't exist"%usr
    
    @classmethod
    def get_admin_text(cls): return cls.__decompit(cls.admin_text).decode()
    @classmethod
    def get_non_admin_text(cls): return cls.__decompit(cls.non_admin_text).decode()
    @classmethod
    def get_empty(cls): return cls.__decompit(cls.non_admin_text).decode()
    @classmethod
    def get_wrong_pass(cls): return cls.__decompit(cls.wrong_pass).decode()
    @classmethod
    def get_no_user(cls): return cls.__decompit(cls.no_user).decode()
    @classmethod
    def get_insuffcient(cls): return cls.__decompit(cls.insuffcient).decode()
    @classmethod
    def get_added(cls): return cls.__decompit(cls.added).decode()
    @classmethod
    def get_pass_changed(cls): return cls.__decompit(cls.pass_changed).decode()
    @classmethod
    def get_user_changed(cls): return cls.__decompit(cls.user_changed).decode()
    @classmethod
    def get_cant_super(cls): return cls.__decompit(cls.del_super).decode()
    @classmethod
    def get_login_successful(cls): return cls.__decompit(cls.login_successful).decode()

    
    @classmethod
    def __hashit(cls, text):
        try: text = text.encode()
        except: pass
        return hashlib.sha224(base64.b64encode(zlib.compress(text))).hexdigest()
    
    @classmethod
    def __compit(cls, text):
        try: text = text.encode()
        except: pass
        return base64.b64encode(zlib.compress(text))
    
    @classmethod
    def __decompit(cls, text):
        try: text = text.encode()
        except: pass
        return zlib.decompress(base64.b64decode(text))


