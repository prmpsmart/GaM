# for python 2
#  -*- coding: utf-8 -*-

from .prmp_errors import PRMP_Errors
import re, os, io

class PRMP_Mixins:
    tempFile = 'prmpsmartTempFile'
    _unget = '_prmp_'
    
    Errors = PRMP_Errors
    containers = list, set, tuple

    def propertize(self, name):
        if name.startswith('_'): return name
        if name:
            name = str(name)
            nm = name.replace(' ', '')
            fin = self.AlphabetsSwitch[nm[0].upper()] + nm[1:]
            return fin

    @property
    def AlphabetsSwitch(self):
        d = {}
        for n in range(65, 91):
            d[chr(n)] = chr(n+32)
            d[chr(n+32)] = chr(n)
        return d

    def printError(self, func, error, file=''): print("Errors from {}->{}: {}, {}".format(self, func, error, file))

    @classmethod
    def notImp(cls): raise NotImplementedError('A subclass of {} should call this method.'.format(cls))

    def testPrint(self, *args):
        print()
        for a in args: print(a, '=')
        print()

    def __bool__(self): return True



class PRMP_ClassMixins(PRMP_Mixins):
    
    @property
    def mroStr(self): return [s.__name__ for s in self.mro]

    @property
    def mro(self): return self.__class__.__mro__

    @property
    def class_(self): return self.__class__

    def attrError(self, attr): raise AttributeError('"{}" does not exist in {}'.format(attr, self))

    @property
    def className(self): return self.__class__.__name__

    def getFromSelf(self, name, unget=None):
        ret = self.__dict__.get(name, unget)
        if ret != unget: return ret
        else:
            for cl in self.mro:
                ret = cl.__dict__.get(name, unget)
                if ret != unget: return ret.__get__(self)
        return unget

    # get = getFromSelf
    
    # def __getattr__(self, attr, dontRaise=False):
    #     ret = self.getFromSelf(attr, self._unget)
    #     if ret != self._unget: return ret
    #     elif not dontRaise: self.attrError(attr)

    # def __setattr__(self, attr, value): return None

    # def __setitem__(self, key, value):
    #     var = self.getFromSelf(self.propertize(key))
    #     var = value

    def __len__(self): return len(self[:])
    
    def __getitem__(self, item):
        if isinstance(item, self.containers):
            res = []
            for it in item: res.append(self[it])
            return res

        elif isinstance(item, str): return self.getFromSelf(self.propertize(item))

        elif isinstance(item, dict):
            res = []
            for k, v in item.items():
                head = self[k]
                if isinstance(v, dict):
                    tail = []
                    tail_props = [(g, h) for g, h in v.items()]
                    last = tail_props[-1]
                    count = 0
                    length_of_tail_props = len(tail_props)
                    while count < length_of_tail_props:
                        tail_prop = tail_props[count]
                        try: tail_1 = head[tail_prop[0]]
                        except: tail_1  = getattr(head, tail_prop[0])

                        try: tail_2 = tail_1[tail_prop[1]]
                        except: tail_2  = getattr(tail_1, tail_prop[1])

                        tail.append(tail_2)
                        count += 1
                else:
                    if head:
                        try: tail = head[v]
                        except: tail = getattr(head, v)
                    else: self.attrError(k)
                res.append(tail)
            return res if len(res) > 1 else res[0]

        # if self.subs: return self.subs[item]
        # else: return None
        return self.subs[item]


class PRMP_AdvMixins(PRMP_ClassMixins):
    
    def isArray(self, array):
        try:
            array.any()
            return True
        except: return False

    def getDate(self, date=None):
        from .prmp_datetime import PRMP_DateTime

        if not date: date = PRMP_DateTime.now()

        elif isinstance(date, (str, bytes)): date = PRMP_DateTime.getDMYFromString(date)
        PRMP_DateTime.checkDateTime(date, 1)
        return date

    def getImageData(self, image):
        temp = io.BytesIO()
        image.save(temp, 'png')
        data = temp.getvalue()
        return data


class PRMP_StrMixins(PRMP_ClassMixins):
    
    _top = 'top'
    _left = 'left'
    _right = 'right'
    _bottom = 'bottom'
    _center = 'center'
    _sides = [_top, _left, _right, _bottom, _center]


    _both = '◄►'
    _next = '►'
    _previous = '◄'
    _forward = '⏭'
    _backward = '⏮'

    dollar = chr(36)
    euro = chr(163)
    yen = chr(165)
    _moneySign = dollar + chr(32)

    if os.sys.version_info[0] == 3:
        upArrow = chr(11014)
        downArrow = chr(11015)
        x_btn1 = chr(10060)
        x_btn2 = chr(10062)

        max_ = chr(9645)
        min_ = chr(10134)

        naira = chr(8358)
        _moneySign = naira + chr(32)

    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def getNumsInStrAsList(self, string, lengths=[], dontRaise=False):
        strs = list(string.replace(' ', ''))

        numbers = []
        count = 0
        non_num = []

        for a in strs:
            try: int(a)
            except: non_num.append(count)
            count += 1

        if len(non_num) not in lengths:
            if not dontRaise: raise AssertionError(f'Provide {lengths} numbers separated by non-numerics')
            return

        count = 0
        for n in non_num:
            numbers.append(strs[count:n])
            count = n+1
        numbers.append(strs[count:])

        strs = [int(''.join(d)) for d in numbers]
        return strs

    def numWithCommas(self, num=None, func=float, s='.02f'):
        if num == None: num = func(self)
        # return f'{num:,{s}}'
        return f'{num:,.02f}'

    def numWithSign_Commas(self, num=None):
        return f'{self._moneySign} {num:,.02f}'
        # return self.addSignToNum(self.numWithCommas(num))

    def addSignToNum(self, num):
        if num == self._moneySign: return num

        return f'{self._moneySign} {num}'

    numberToMoney = addSignToMoney = addSignToNum

    def stripSignFromNum(self, num):
        num = num.replace(self._moneySign, '')
        num = num.replace(' ', '')
        num = num.replace(',', '')
        return num

    moneyToNumber = stripSignFromMoney = stripSignFromNum

    def checkEmail(self, email): return True if re.search(self.email_regex, email) else False

    def checkFile(self, file): return os.path.isfile(file)
    def checkDir(self, dir_): return os.path.isdir(dir_)
    def checkPath(self, path): return os.path.exists(path)

    def checkNumber(self, number):
        strNum = str(number)
        dot = '.'
        if dot in strNum:
            if strNum.count(dot) > 1: return False
            strNum = strNum.replace(dot, '')
        test = strNum.isdigit()
        return test

    def checkMoney(self, money):
        try:
            if self._moneySign in money:
                float(self.stripSignFromMoney(money))
                return True
            return False
        except: return False

    def decimalPlace(self, num, place=1):
        return f'{num:.{place}f}'
        ''' below is the prmp implementation
        num = float(num)
        numStr = str(num) + '0'
        endIndex = numStr.index('.') + place + 1
        finised = numStr[:endIndex]
        return float(finised)
        '''

    def approximate(self, num, size=1):
        assert size > 0
        strNum = str(num)
        listNum = list(strNum)
        if len(listNum) <= 3: return num
        app = listNum[size]

        listNum[size:] = ['0' for _ in range(size, len(listNum))]
        add = 0 if int(app) < 5 else 1
        adx = int(listNum[size - 1]) + add
        listNum[size - 1] = str(adx)
        retur = ''.join(listNum)
        return int(retur)

    def stripZeros(self, num, app=1):
        num = self.approximate(num, app)
        strNum = str(num)
        listNum = list(strNum)
        return strNum.strip('0')


class PRMP_GuiMixins(PRMP_StrMixins):
    pass


class PRMP_TkMixins(PRMP_GuiMixins):

    def tkFormatedFileTypes(self, name, exts=[]):
        fexts = '{'
        for ext in exts: fexts += f'.{ext} '
        fexts = fexts[:-1]
        fexts += '}'
        filetypes = ['%s %s'%(name, fexts)]
        return filetypes


# class PRMP_PathMixins:




