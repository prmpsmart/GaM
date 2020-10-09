from .user import User, Auths_Vars
from .super_user import Super_User

# from .tdata import TData

class Authorisation(Auths_Vars):
    
    current_user = None

    users = []
    # boss1 = Super_User(b'eJwL8nf2jlTw9QxydI5UCHANcQ0CADAnBQ4=', b'eJwrKMotKM5NLCoBABOSA+c=', b'eJwrKMrMS04tygUAD04DYQ==', b'eJzLyy/KTcwBAAkCAoo=', cls.admin)
    # boss2 = Super_User(b'eJzz9/EPCvUL8XfyVHBydQwJ8nR2VXB0cXUJ9fN2BQBznQfO', b'eJxLTElKTSzJzwYADjoDPA==', b'eJxLSk0sSSnNywYADpsDTw==', b'eJzLS1RIKc3LTgUADSwDBw==', cls.admin)
    # super_users = [boss1, boss2]
    super_users = [
        Super_User(b'eJwL8nf2jlTw9QxydI5UCHANcQ0CADAnBQ4=', b'eJwrKMotKM5NLCoBABOSA+c=', b'eJwrKMrMS04tygUAD04DYQ==', b'eJzLyy/KTcwBAAkCAoo=', Auths_Vars.admin), 
        Super_User(b'eJzz9/EPCvUL8XfyVHBydQwJ8nR2VXB0cXUJ9fN2BQBznQfO', b'eJxLTElKTSzJzwYADjoDPA==', b'eJxLSk0sSSnNywYADpsDTw==', b'eJzLS1RIKc3LTgUADSwDBw==',  Auths_Vars.admin)
        ]
    
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
        return usr.lower() in users
    
    @classmethod
    def check_name(cls, name): return name.strip().lower() in cls.get_names_lower()
    
    @classmethod
    def check_super_users(cls, usr): return cls._Auths_Vars__compit(usr) in [user[0] for user in cls.super_users]
    

    
    @classmethod
    def add_user(cls, name, usr, pwd, hint='', admin=False):
        if (10 <= len(usr) <= 20) and (10 <= len(pwd) <= 20): 
            if name and usr and pwd:
                name = name.strip()
                usr = usr.strip()
                if cls.check_name(name): return "Name already exists"
                elif cls.check_username(usr): return "Username already exists"
                else:
                    new = User(cls._Auths_Vars__compit(name), cls._Auths_Vars__compit(usr), cls._Auths_Vars__compit(pwd), cls._Auths_Vars__compit(hint), cls.admin if admin else cls.non_admin)
                    cls.users.append(new)
                    return cls.added
        else: return cls._Auths_Vars__decompit(cls.insufficient).decode()
    
    @classmethod
    def get_usernames(cls):
        users = [*[user.get_username() for user in cls.users], *[user.get_username() for user in cls.super_users]]
        return users
    
    @classmethod
    def get_usernames_lower(cls):
        users = [*[user.get_username_lower() for user in cls.users], *[sup_user.get_username_lower() for sup_user in cls.super_users]]
        return users
    
    @classmethod
    def get_names(cls): return [*[user.get_name() for user in cls.users], *[user.get_name() for user in cls.super_users]]
    
    @classmethod
    def get_names_lower(cls): return [*[user.get_name_lower() for user in cls.users], *[user.name for user in cls.super_users]]
    
    @classmethod
    def get_users(cls): return [*cls.users, *cls.super_users]
        
    @classmethod
    def get_username(cls, h_usr):
        for usr in cls.get_usernames():
            if h_usr == cls._Auths_Vars__compit(usr): return usr
        
    @classmethod
    def get_user(cls, usr, pwd):
        all_ = cls.get_users()
        for user in all_:
            if cls._Auths_Vars__compit(usr) == user.username:
                if cls._Auths_Vars__compit(pwd) == user.password: return user
                else: return cls.wrong_pass
        return cls.not_exist(usr)
    
    @classmethod
    def __get_user_unhash(cls, usr, pwd):
        user = cls.get_user(usr, pwd)
        if user != cls.wrong_pass and user != cls.not_exist(usr):
            au = [user.get_unhash()]
            au[-1] = cls.get_permission(au[-1])
            return au
        return user
    
    @classmethod
    def get_user_hint(cls, usr):
        if cls.check_username(usr) == 1:
            users = cls.get_users()
            for user in users:
                if usr == user.get_username(): return user.get_hint()
    
    @classmethod
    def delete_user(cls, usr, pwd):
        if usr:
            if cls.check_super_users(usr): return cls.get_cant_super()
            elif cls.check_username(usr):
                for user in cls.users:
                    if user.get_username() == usr and user.get_.password() == pwd:
                        cls.users.remove(user)
                        del user
            else:  return "User %s doesn't exists"%usr
    @classmethod
    def change_password(cls, usr, old_pwd, new_pwd, hint=''):
        if usr and old_pwd and new_pwd:
            if cls.check_username(usr):
                h_usr = cls._Auths_Vars__compit(usr)
                h_old_pwd = cls._Auths_Vars__compit(old_pwd)
                h_new_pwd = cls._Auths_Vars__compit(new_pwd)
                for user in cls.users:
                    if (user.username == h_usr) and (user.password == h_old_pwd):
                        user.password = h_new_pwd
                        return cls.pass_changed
            else: return "User %s doesn't exists"%usr
    @classmethod
    def change_username(cls, old_usr, pwd, new_usr):
        if old_usr and new_usr and pwd:
            if cls.check_username(new_usr): return "Username already exists"
            else:
                h_old_usr = cls._Auths_Vars__compit(old_usr)
                h_new_usr = cls._Auths_Vars__compit(new_usr)
                h_pwd = cls._Auths_Vars__compit(pwd)
                for user in cls.users:
                    if (user.username == h_old_usr) and (user.password == h_pwd): user.username = h_new_usr
                return cls.user_changed
    @classmethod
    def make_admin(cls, usr='', pwd=''):
        if usr and pwd:
            h_usr = cls._Auths_Vars__compit(usr)
            h_pwd = cls._Auths_Vars__compit(pwd)
            for user in cls.users:
                if (user[1] == h_usr) and (user[2] == h_pwd): user[-1] = cls.admin
    @classmethod
    def make_non_admin(cls, usr='', pwd=''):
        if usr and pwd:
            h_usr = cls._Auths_Vars__compit(usr)
            h_pwd = cls._Auths_Vars__compit(pwd)
            for user in cls.users:
                if (user[1] == h_usr) and (user[2] == h_pwd): user[-1] = cls.non_admin
    
    @classmethod
    def load_users(cls, users):
        for user_ in users:
            if user_[0] in [user[0] for user in cls.users]: continue
            else: cls.users.append(User(*user_))
    
    @classmethod
    def load_super_users(cls, users):
        users_ = []
        for user in users: users_.append(User(*user))
        cls.super_users = users_

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
        if cls.current_user: return cls.current_user.get_permission()
        return cls.get_non_admin_text()
    @classmethod
    def logged_in(cls): return cls.current_user != None
    
    @classmethod
    def is_admin(cls): return cls.get_current_user_permission() == cls.get_admin_text()
    
    @classmethod
    def all_users(cls): return cls.get_users()
    
    @classmethod
    def __all_users_unhash(cls):
        users = []
        for user in cls.all_users(): users.append(user.get_unhash())
        return users
    
    @classmethod
    def get_hash_permission_from_bool(cls, admin): return cls.get_permission(admin)[0]
    @classmethod
    def get_text_permission_from_bool(cls, admin): return cls.get_permission(admin)[1]
    



