
from .vars import Auths_Vars

class User:
    super_user = False
    class_name = "User"

    def __init__(self, name, usr, pwd, hint, admin):
        self.name = name
        self.username = usr
        self.password = pwd
        self.hint = hint
        self.permission = admin
    
    def __repr__(self):
        text = f"{self.class_name}(name={self.get_name()}, username={self.get_username()}, password={self.get_password()}, hint={self.get_hint()}, permission={self.get_permission()})"
        return text
    
    def __str__(self):
        text = f"{self.class_name}(name={self.get_name()}, username={self.get_username()}, password={self.get_password()}, hint={self.get_hint()}, permission={self.get_permission()})"
        return text
    
    def get_status(self): return (self.get_name(), self.get_username())

    def get_name(self): return Auths_Vars._Auths_Vars__decompit(self.name).decode()
    def get_username(self): return Auths_Vars._Auths_Vars__decompit(self.username).decode()
    
    def get_name_lower(self): return self.get_name().lower()
    def get_username_lower(self): return self.get_username().lower()
    
    def get_unhash(self):
        vals = [self.get_name(), self.get_username(), self.get_password(), self.get_hint(), self.get_permission()]
        return vals
    
    def get_password(self): return Auths_Vars._Auths_Vars__decompit(self.password).decode()
    def get_hint(self): 
        hint = Auths_Vars._Auths_Vars__decompit(self.hint).decode()
        if not hint: return "EMPTY"
        return hint
    def get_permission(self): return Auths_Vars.get_permission(self.permission)[1]
    
    def is_admin(self): return Auths_Vars.get_permission(self.permission)[0]
    
    def get_hash(self):
        vals = [self.name, self.username, self.password, self.hint, self.permission]
        return vals
    
    