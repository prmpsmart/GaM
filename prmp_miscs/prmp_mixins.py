from .prmp_errors import PRMP_Errors
import re

class PRMP_Mixins:
    tempFile = 'prmpsmartTempFile'
    _unget = '_prmp_'
    
    containers = list, set, tuple
    naira = chr(8358)
    dollar = chr(36)
    euro = chr(163)
    yen = chr(165)
    _moneySign = naira + chr(32)
    Errors = PRMP_Errors
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    
    @property
    def mroStr(self): return [s.__name__ for s in self.mro]
    
    def numWithCommas(self, num=None):
        if num == None: num = int(self)
        
        div = 3
        str_num = str(num)
        num_list = list(str_num)
        num_len = len(str_num)
        num_rem = num_len % div
        num_div = num_len // div
        if not num_rem: num_div -= 1
        co, to = -3, 0
        for _ in range(num_div):
            num_list.insert(co - to, ",")
            co -= 3
            to += 1
        return "".join(num_list)
    
    def numWithSign_Commas(self, num): return self.addSignToNum(self.numWithCommas(num))

    
    def addSignToNum(self, num): return f'{self._moneySign}{num}'

    def stripSignFromNum(self, num):
        num = num.replace(self._moneySign, '')
        num = num.replace(' ', '')
        return num.replace(' ', '').replace(self._moneySign, '')
    
    
    @property
    def mro(self): return self.class_.__mro__

    @property
    def class_(self): return self.__class__

    def attrError(self, attr): raise AttributeError(f'"{attr}" does not exist in {self}')

    def getFromSelf(self, name, unget=None):
        ret = self.__dict__.get(name, unget)
        if ret != unget: return ret
        else:
            for cl in self.mro:
                ret = cl.__dict__.get(name, unget)
                if ret != unget:
                    if isinstance(ret, property): return ret.fget(self)
                    return ret
        return unget
        
    def printError(self, func, error): print(f"Errors from {self}->{func}: ", error)
    
    def checkEmail(self, email): return True if re.search(self.email_regex, email) else False
    
    def checkNumber(self, number): return str(number).isdigit()

    
    @classmethod
    def notImp(cls): raise NotImplementedError(f'A subclass of {cls} should call this method.')

    @property
    def className(self): return f'{self.__class__.__name__}'
    
    @property
    def AlphabetsSwitch(self):
        d = {}
        for n in range(65, 91):
            d[chr(n)] = chr(n+32)
            d[chr(n+32)] = chr(n)
        return d
    
    def propertize(self, name):
        if name.startswith('_'): return name
        if name:
            name = str(name)
            nm = name.replace(' ', '')
            fin = self.AlphabetsSwitch[nm[0].upper()] + nm[1:]
            return fin
    
    def testPrint(self, *args):
        print()
        for a in args: print(a, end='=')
        print()
    
    def __bool__(self): return True
        
    
    def getImageData(self, image):
        temp = io.BytesIO()
        image.save(temp, 'png')
        data = temp.getvalue()
        return data









