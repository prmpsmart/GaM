from .image_list import agams, apps, icos, logins, prmpsmart
from base64 import b64decode, b64encode
from io import BytesIO
from ..path import Path


class Images:
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'
    G = 'G'
    I = 'I'
    H = 'H'
    J = 'J'
    K = 'K'
    L = 'L'
    M = 'M'
    N = 'N'
    PRMP = 'Z'

    AGAMS = {A: agams[0], B: agams[1]}
    APPS = {A: apps[0], B: apps[1], C: apps[2]}
    ICOS = {A: icos[0], B: icos[1], C: icos[2], D: icos[3]}
    LOGINS = {A: logins[0], B: logins[1], C: logins[2], D: logins[3], E: logins[4], F: logins[5], G: logins[6], H: logins[7], I: logins[8], J: logins[9], K: logins[10], L: logins[11], M: logins[12], N: logins[13]}
    
    
    current_agam = A
    current_app = A
    current_ico = A
    current_login = A
    
    def __init__(self, ag, ap, ic, lo):
        self.current_agam = ag
        self.current_app = ap
        self.current_ico = ic
        self.current_login = lo

    @classmethod
    def agam(cls):
        image = cls.AGAMS[cls.current_agam]
        return cls.convert2bytesio(image)
        
    @classmethod
    def login(cls):
        image = cls.LOGINS[cls.current_login]
        return cls.convert2bytesio(image)

    @classmethod
    def app(cls):
        image = cls.APPS[cls.current_app]
        return cls.convert2bytesio(image)

    @classmethod
    def ico(cls):
        image = cls.ICOS[cls.current_app]
        img = cls.convert2image(image)
        
        tempfile = Path.tempfile() + ".ico"
        with open(tempfile, 'wb') as temp: temp.write(img)
        print(tempfile)
        return tempfile
        

    @classmethod
    def set_agam(cls, char): cls.get_agam(char.title())
        
    @classmethod
    def set_login(cls, char): cls.get_login(char.title())
        
    @classmethod
    def set_app(cls, char): cls.get_app(char.title())
        
    @classmethod
    def get_agam(cls, char):
        char = char.title()
        if cls.A <= char <= cls.B:
            cls.current_agam = char
            return cls.convert2bytesio(cls.AGAMS[char])
        elif char == cls.PRMP: return cls.convert2bytesio(prmpsmart)
        else: return cls.convert2bytesio(cls.AGAMS[cls.A])
    
    @classmethod
    def get_app(cls, char):
        char = char.title()
        if cls.A <= char <= cls.D:
            cls.current_app = char
            return cls.convert2bytesio(cls.APPS[char])
        elif char == cls.PRMP: return cls.convert2bytesio(prmpsmart)
        else: return cls.convert2bytesio(cls.APPS[cls.A])
    
    @classmethod
    def get_ico(cls, char):
        char = char.title()
        img = ''
        if cls.A <= char <= cls.D:
            cls.current_ico = char
            img = cls.convert2image(cls.ICOS[char])
        else: img = cls.convert2image(cls.ICOS[cls.A])
        if img:
            tempfile = Path.tempfile() + ".ico"
            with open(tempfile, 'wb') as temp: temp.write(img)
            print(tempfile)
            return tempfile
        
    
    @classmethod
    def get_login(cls, char):
        char = char.title()
        if cls.A <= char <= cls.N:
            cls.current_login = char
            return cls.convert2bytesio(cls.LOGINS[char])
        elif char == cls.PRMP: return cls.convert2bytesio(prmpsmart)
        else: return cls.convert2bytesio(cls.LOGINS[cls.A])
    
    
    @classmethod
    def get_state(cls): return cls(cls.current_agam, cls.current_app, cls.current_ico, cls.current_login)
    @classmethod
    def load_state(cls, imageobj):
        if isinstance(imageobj, cls):
            cls.current_agam = imageobj.current_agam
            cls.current_app = imageobj.current_app
            cls.current_ico = imageobj.current_ico
            cls.current_login = imageobj.current_login
    @classmethod
    def reset(cls):
        cls.current_agam = cls.A
        cls.current_app = cls.A
        cls.current_ico = cls.A
        cls.current_login = cls.A
    
    @classmethod
    def convert2image(cls, txt): return b64decode(txt)
    @classmethod
    def convert2bytesio(cls, txt): return BytesIO(cls.convert2image(txt))

