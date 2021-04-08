import hashlib, zlib, base64
from prmp_lib.prmp_miscs.prmp_mixins import PRMP_Mixins

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
    def decify(cls, byt): return cls._decompit(byt).decode()
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
    def get_admin_text(cls):
        decomp = cls._decompit(cls.admin_text)
        dec = decomp.decode()
        return dec
    @classmethod
    def get_non_admin_text(cls):
        decomp = cls._decompit(cls.non_admin_text)
        dec = decomp.decode()
        return dec
    @classmethod
    def get_empty(cls):
        decomp = cls._decompit(cls.non_empty)
        dec = decomp.decode()
        return dec
    @classmethod
    def get_wrong_pass(cls):
        decomp = cls._decompit(cls.wrong_pass)
        dec = decomp.decode()
        return dec
    @classmethod
    def get_no_user(cls):
        decomp = cls._decompit(cls.no_user)
        dec = decomp.decode()
        return dec
    @classmethod
    def get_insuffcient(cls):
        decomp = cls._decompit(cls.insuffcient)
        dec = decomp.decode()
        return dec
    @classmethod
    def get_added(cls):
        decomp = cls._decompit(cls.added)
        dec = decomp.decode()
        return dec
    @classmethod
    def get_pass_changed(cls):
        decomp = cls._decompit(cls.pass_changed)
        dec = decomp.decode()
        return dec
    @classmethod
    def get_user_changed(cls):
        decomp = cls._decompit(cls.user_changed)
        dec = decomp.decode()
        return dec
    @classmethod
    def get_cant_super(cls):
        decomp = cls._decompit(cls.del_super)
        dec = decomp.decode()
        return dec
    @classmethod
    def get_login_successful(cls):
        decomp = cls._decompit(cls.login_successful)
        dec = decomp.decode()
        return dec

    @classmethod
    def _hashit(cls, text):
        try: text = text.encode()
        except: pass
        comp = zlib.compress(text)
        enc = base64.b64encode(comp)
        sha = hashlib.sha224(enc)
        hexdigest = sha.hexdigest()
        return hexdigest

    @classmethod
    def _compit(cls, text):
        try: text = text.encode()
        except: pass
        comp = zlib.compress(text)
        enc = base64.b64encode(comp)
        return enc

    @classmethod
    def _decompit(cls, text):
        try: text = text.encode()
        except: pass
        dec = base64.b64decode(text)
        decomp = zlib.decompress(dec)
        return decomp


class User(PRMP_Mixins):
    super_user = False
    ADMIN = False

    def __init__(self, name, usr, pwd, hint, permission):
        self.__name = name
        self.__username = usr
        self.__password = pwd
        self.__hint = hint
        self.__permission = permission

    def __repr__(self): return '<{}, {}>'.format(self.username, self.permission)

    def __str__(self):
        text = "{}(name={}, username={}, password={}, hint={}, permission={})".format(self.className, self.name, self.username, self.password, self.hint, self.permission)
        return text

    @property
    def _name(self): return self.__name
    @property
    def _username(self): return self.__username
    @property
    def _hint(self): return self.__hint
    @property
    def _permission(self): return self.__permission

    @property
    def name(self): return Auths_Vars._decompit(self.__name).decode()
    @property
    def username(self): return Auths_Vars._decompit(self.__username).decode()

    @property
    def name_lower(self): return self.name.lower()
    @property
    def username_lower(self): return self.username.lower()
    @property
    def password(self): return self.__password
    @property
    def _password(self): return Auths_Vars._decompit(self.__password).decode()
    @property
    def hint(self):
        hint = Auths_Vars._decompit(self.__hint).decode()
        if not hint: return "EMPTY"
        return hint
    @property
    def permission(self): return Auths_Vars.get_permission(self.__permission)[1]

    @property
    def status(self): return (self.name, self.username)

    @property
    def unhash(self):
        vals = [self.name, self.username, self.password, self.hint, self.permission]
        return vals


    @property
    def is_admin(self): return Auths_Vars.permission(self.permission)[0]

    @property
    def _hash(self):
        vals = [self.__name, self.__username, self.__password, self.__hint, self.__permission]
        return vals


class Super_User(User):
    super_user = True
    ADMIN = True


class Authorisation(Auths_Vars):
    current_user = None
    __users = []
    __super_users = [
        Super_User(b'eJwL8nf2jlTw9QxydI5UCHANcQ0CADAnBQ4=', b'eJwrKMotKM5NLCoBABOSA+c=', b'eJwrKMrMS04tygUAD04DYQ==', b'eJzLyy/KTcwBAAkCAoo=', Auths_Vars.admin),
        Super_User(b'eJzz9/EPCvUL8XfyVHBydQwJ8nR2VXB0cXUJ9fN2BQBznQfO', b'eJxLTElKTSzJzwYADjoDPA==', b'eJxLSk0sSSnNywYADpsDTw==', b'eJzLS1RIKc3LTgUADSwDBw==',  Auths_Vars.admin)
        ]

    @classmethod
    def get_users(cls): return cls.__users
    @classmethod
    def get_super_users(cls): return cls.__super_users
    @classmethod
    def check_super(cls, usr, pwd):
        user = cls.get_user(usr, pwd)
        return user.super_user

    @classmethod
    def change_hint(cls, usr='', pwd='', hint=''):
        user = cls.get_user(usr, pwd)

    @classmethod
    def check_user(cls, usr, pwd):
        user = cls.get_user(usr, pwd)
        if user == cls.not_exist(usr): return 0
        elif user == cls.wrong_pass: return 2
        else: return 1

    @classmethod
    def check_username(cls, usr):
        users = cls.get_usernames_lower()
        bol  = usr.lower() in users
        return bol

    @classmethod
    def check_name(cls, name): return name.strip().lower() in cls.get_names_lower()

    @classmethod
    def check_super_users(cls, usr): return cls._compit(usr) in [user._hash[0] for user in cls.__super_users]

    @classmethod
    def add_user(cls, name, usr, pwd, hint='', admin=False):
        if (5 <= len(usr) <= 20) and (10 <= len(pwd) <= 20):
            if name and usr and pwd:
                name = name.strip()
                usr = usr.strip()
                if cls.check_name(name): return "Name already exists"
                elif cls.check_username(usr): return "Username already exists"
                else:
                    new = User(cls._compit(name), cls._compit(usr), cls._compit(pwd), cls._compit(hint), cls.admin if admin else cls.non_admin)
                    cls.__users.append(new)
                    return cls.added, new
        else: return cls.insufficient

    @classmethod
    def get_usernames(cls):
        users = [*[user.username for user in cls.__users], *[user.username for user in cls.__super_users]]
        return users

    @classmethod
    def get_usernames_lower(cls):
        users = [*[user.username_lower for user in cls.__users], *[sup_user.username_lower for sup_user in cls.__super_users]]
        return users

    @classmethod
    def get_names(cls): return [*[user.name for user in cls.__users], *[user.name for user in cls.__super_users]]

    @classmethod
    def get_names_lower(cls): return [*[user.name_lower for user in cls.__users], *[user.name for user in cls.__super_users]]

    @classmethod
    def get_users(cls): return [*cls.__users, *cls.__super_users]

    @classmethod
    def get_username(cls, h_usr):
        for usr in cls.get_usernames():
            if h_usr == cls._compit(usr): return usr

    @classmethod
    def get_user(cls, usr, pwd):
        all_ = cls.get_users()
        for user in all_:
            if cls._compit(usr) == user._username:
                if cls._compit(pwd) == user.password: return user
                else: return cls.wrong_pass
        return cls.not_exist(usr)

    @classmethod
    def _get_user_unhash(cls, usr, pwd):
        user = cls.get_user(usr, pwd)
        if user != cls.wrong_pass and user != cls.not_exist(usr):
            au = [user.unhash]
            au[-1] = cls.get_permission(au[-1])
            return au
        return user

    @classmethod
    def get_user_hint(cls, usr):
        if cls.check_username(usr) == 1:
            users = cls.get_users()
            for user in users:
                if usr == user.username: return user.hint

    @classmethod
    def delete_user(cls, usr, pwd):
        if usr:
            if cls.check_super_users(usr): return cls.get_cant_super()
            elif cls.check_username(usr):
                for user in cls.__users:
                    if user.username == usr and user.password == pwd:
                        cls.__users.remove(user)
                        del user
            else:  return "User %s doesn't exists"%usr
    @classmethod
    def change_password(cls, usr, old_pwd, new_pwd, hint=''):
        if usr and old_pwd and new_pwd:
            if cls.check_username(usr):
                h_usr = cls._compit(usr)
                h_old_pwd = cls._compit(old_pwd)
                h_new_pwd = cls._compit(new_pwd)
                for user in cls.__users:
                    if (user.username == h_usr) and (user.password == h_old_pwd):
                        user.password = h_new_pwd
                        return cls.pass_changed
            else: return "User %s doesn't exists"%usr
    @classmethod
    def change_username(cls, old_usr, pwd, new_usr):
        if old_usr and new_usr and pwd:
            if cls.check_username(new_usr): return "Username already exists"
            else:
                h_old_usr = cls._compit(old_usr)
                h_new_usr = cls._compit(new_usr)
                h_pwd = cls._compit(pwd)
                for user in cls.__users:
                    if (user.username == h_old_usr) and (user.password == h_pwd): user.username = h_new_usr
                return cls.user_changed
    @classmethod
    def make_admin(cls, usr='', pwd=''):
        if usr and pwd:
            h_usr = cls._compit(usr)
            h_pwd = cls._compit(pwd)
            for user in cls.__users:
                if (user._username == h_usr) and (user._password == h_pwd): user._User__permission = cls.admin
    @classmethod
    def make_non_admin(cls, usr='', pwd=''):
        if usr and pwd:
            h_usr = cls._compit(usr)
            h_pwd = cls._compit(pwd)
            for user in cls.__users:
                if (user._username == h_usr) and (user._password == h_pwd): user._User__permission = cls.non_admin

    @classmethod
    def load_users(cls, users):
        for user_ in users:
            if user_.username in [user.username for user in cls.__users]: continue
            else: cls.__users.append(user_)

    @classmethod
    def load_super_users(cls, users):
        for user_ in users:
            if user_.username in [user.username for user in cls.__users]: continue
            else: cls.__super_users.append(user_)

    @classmethod
    def login(cls, usr, pwd):
        user = cls.get_user(usr, pwd)
        if (user == cls.wrong_pass): return 2
        elif (user == cls.not_exist(usr)): return 0
        else:
            cls.current_user = user
            return 1

    @classmethod
    def login_cmd(cls, usr, pwd):
        log = cls.login(usr, pwd)
        if (log == 2): return cls.get_wrong_pass()
        elif (log == 0): return cls.not_exist(usr)
        elif log == 1: return cls.get_login_successful()

    @classmethod
    def logout(cls): cls.current_user = None

    @classmethod
    def get_current_user(cls):
        if cls.current_user: return cls.current_user
        return cls.get_no_user()
    @classmethod
    def get_current_user_permission(cls):
        if cls.current_user: return cls.current_user.permission
        return cls.get_non_admin_text()
    @classmethod
    def logged_in(cls): return cls.current_user != None

    @classmethod
    def is_admin(cls): return cls.get_current_user_permission() == cls.get_admin_text()

    @classmethod
    def all_users(cls): return cls.get_users()

    @classmethod
    def _all_users_unhash(cls):
        users = []
        for user in cls.all_users(): users.append(user.unhash)
        return users

    @classmethod
    def get_hash_permission_from_bool(cls, admin): return cls.get_permission(admin)[0]

    @classmethod
    def get_text_permission_from_bool(cls, admin): return cls.get_permission(admin)[1]


