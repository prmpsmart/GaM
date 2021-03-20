

# prmp_errors.py


class PRMP_Errors(Exception):
    class PRMP_DateTimeError(Exception): pass
    class PRMP_ZipError(Exception): pass


# prmp_mixins.py

import re, os, io
py = os.sys.version_info[0]

class PRMP_Mixins:
    tempFile = 'prmpsmartTempFile'
    _unget = '_prmp_'

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

    if py == 3:
        upArrow = chr(11014)
        downArrow = chr(11015)
        x_btn1 = chr(10060)
        x_btn2 = chr(10062)

        max_ = chr(9645)
        min_ = chr(10134)

        naira = chr(8358)
        _moneySign = naira + chr(32)


    Errors = PRMP_Errors
    containers = list, set, tuple
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def getNumsInStrAsList(self, string, length=[], dontRaise=False):
        strs = list(string.replace(' ', ''))

        numbers = []
        count = 0
        non_num = []

        for a in strs:
            try: int(a)
            except: non_num.append(count)
            count += 1

        if len(non_num) not in length:
            if not dontRaise: raise AssertionError(f'Provide {length} numbers separated by non-numerics')
            return

        count = 0
        for n in non_num:
            numbers.append(strs[count:n])
            count = n+1
        numbers.append(strs[count:])

        strs = [int(''.join(d)) for d in numbers]
        return strs

    @property
    def mroStr(self): return [s.__name__ for s in self.mro]

    def getDate(self, date=None):
        if date == None: date = PRMP_DateTime.now()
        elif isinstance(date, str): date = PRMP_DateTime.getDMYFromDate(date)
        PRMP_DateTime.checkDateTime(date, 1)
        return date

    def numWithCommas(self, num=None, fl=0):
        if num == None: num = self

        num = float(num) if fl else int(num)

        div = 3
        str_num = str(num)

        if fl:
            str_num, afterFloat = str_num.split('.')
            if afterFloat == '0': afterFloat = '00'

        minus = 0
        if str_num.startswith('-'):
            minus = 1
            str_num = str_num[1:]

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

        result = "".join(num_list)
        if fl: result = result + '.' + afterFloat

        _minus = '-' if minus else ''
        result = _minus + result
        return result

    def numWithSign_Commas(self, num): return self.addSignToNum(self.numWithCommas(num, 1))

    def addSignToNum(self, num):
        try: float(num)
        except:
            if num == self._moneySign: return num

        return '{} {}'.format(self._moneySign, num)

    numberToMoney = addSignToMoney = addSignToNum

    def stripSignFromNum(self, num):
        num = num.replace(self._moneySign, '')
        num = num.replace(' ', '')
        return num.replace(' ', '').replace(self._moneySign, '')

    moneyToNumber = stripSignFromMoney = stripSignFromNum

    @property
    def mro(self): return self.class_.__mro__

    @property
    def class_(self): return self.__class__

    def attrError(self, attr): raise AttributeError('"{}" does not exist in {}'.format(attr, self))

    def getFromSelf(self, name, unget=None):
        ret = self.__dict__.get(name, unget)
        if ret != unget: return ret
        else:
            for cl in self.mro:
                ret = cl.__dict__.get(name, unget)
                if ret != unget: return ret.__get__(self)
        return unget

    # get = getFromSelf

    def printError(self, func, error): print("Errors from {}->{}: {}".format(self, func, error))

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

    @classmethod
    def notImp(cls): raise NotImplementedError('A subclass of {} should call this method.'.format(cls))

    @property
    def className(self): return self.__class__.__name__

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
        for a in args: print(a, '=')
        print()

    def __bool__(self): return True

    def getImageData(self, image):
        temp = io.BytesIO()
        image.save(temp, 'png')
        data = temp.getvalue()
        return data

    def decimalPlace(self, num, place=1):
        num = float(num)
        numStr = str(num) + '0'
        endIndex = numStr.index('.') + place + 1
        return numStr[:endIndex]

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


# prmp_exts.py
from io import BytesIO
from base64 import b64encode, b64decode
import zlib, pickle


class PRMP_ImageType:

    tests = []

    def test_jpeg(data):
        """JPEG data in JFIF or Exif format"""
        if data[6:10] in (b'JFIF', b'Exif'):
            return 'jpeg'

    tests.append(test_jpeg)

    def test_png(data):
        if data.startswith(b'\211PNG\r\n\032\n'):
            return 'png'

    tests.append(test_png)

    def test_gif(data):
        """GIF ('87 and '89 variants)"""
        if data[:6] in (b'GIF87a', b'GIF89a'):
            return 'gif'

    tests.append(test_gif)

    def test_tiff(data):
        """TIFF (can be in Motorola or Intel byte order)"""
        if data[:2] in (b'MM', b'II'):
            return 'tiff'

    tests.append(test_tiff)

    def test_rgb(data):
        """SGI image library"""
        if data.startswith(b'\001\332'):
            return 'rgb'

    tests.append(test_rgb)

    def test_pbm(data):
        """PBM (portable bitmap)"""
        if len(data) >= 3 and \
            data[0] == ord(b'P') and data[1] in b'14' and data[2] in b' \t\n\r':
            return 'pbm'

    tests.append(test_pbm)

    def test_pgm(data):
        """PGM (portable graymap)"""
        if len(data) >= 3 and \
            data[0] == ord(b'P') and data[1] in b'25' and data[2] in b' \t\n\r':
            return 'pgm'

    tests.append(test_pgm)

    def test_ppm(data):
        """PPM (portable pixmap)"""
        if len(data) >= 3 and \
            data[0] == ord(b'P') and data[1] in b'36' and data[2] in b' \t\n\r':
            return 'ppm'

    tests.append(test_ppm)

    def test_rast(data):
        """Sun raster file"""
        if data.startswith(b'\x59\xA6\x6A\x95'):
            return 'rast'

    tests.append(test_rast)

    def test_xbm(data):
        """X bitmap (X10 or X11)"""
        if data.startswith(b'#define '):
            return 'xbm'

    tests.append(test_xbm)

    def test_bmp(data):
        if data.startswith(b'BM'):
            return 'bmp'

    tests.append(test_bmp)

    def test_webp(data):
        if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
            return 'webp'

    tests.append(test_webp)

    def test_exr(data):
        if data.startswith(b'\x76\x2f\x31\x01'):
            return 'exr'

    tests.append(test_exr)

    @classmethod
    def get(cls, file=None, data=b'', base64=b'', image=None):
        if file:
            if isinstance(file, (str, bytes)): file = open(file, 'rb')
            data = file.read(32)
        elif base64: data = b64decode(base64)
        elif image:
            file = BytesIO()
            image.save(file)
            data = file.getvalue()

        if data:
            _needed = data[:32]
            return cls._get(_needed)

    @classmethod
    def _get(cls, data):
        for test in cls.tests:
            ext = test(data)
            if ext: return ext


class PRMP_File(BytesIO, PRMP_Mixins):
    count = 0

    def __init__(self, filename='', base64=b'', data=b''):

        passed = [bool(a) for a in [filename, base64]].count(True)
        assert passed <= 1, 'Only one is required in [filename, base64, image]'

        self.name = None
        self._data = data

        if data: self.name = 'data_%d'%PRMP_File.count

        elif filename:
            self.name = os.path.basename(filename)
            if os.path.isfile(filename):
                try: self._data = open(filename, 'rb').read()
                except: pass

        elif base64:
            self._data = b64decode(base64)
            self.name = 'base64_%d'%PRMP_File.count

        super().__init__(self._data)

        PRMP_File.count += 1

    def __str__(self):
        if self.name: return f'{self.className}(%s)'%self.name
        else: return f'{self.className}(%d)'%PRMP_File.count

    def __len__(self): return self.size

    @property
    def data(self): return self.getvalue()

    def read(self, _read=0):
        data = self.data
        if _read == 0: return data
        else: return super().read(_read)


    # def read(self, _read=0):
    #     print(_read)
    #     self._read = 0
    #     data = self.data
    #     if _read in [0, 1]: return data
    #     else:
    #         self._read =+ _read
    #         return data[:self._read]
    #     return data

    @property
    def ext(self): return PRMP_ImageType.get(self)

    @property
    def size(self): return len(self.data)

    def get(self): return self.data

    @property
    def compressedData(self): return zlib.compress(self.data)

    @property
    def cdata(self): return self.compressedData

    @property
    def base64Data(self): return b64encode(self.data)

    def pickle(self, file=''):
        file = file or self
        try: f = open(file, 'wb')
        except: f = file

        pickle.dump(self, f)

    def unpickle(self, file=''):
        file = file or self

        try: f = open(file, 'wb')
        except: f = file

        obj = pickle.load(f)
        return obj

    def save(self, file=''):
        file = file or self.name

        try: f = open(file, 'wb')
        except: f = file
        f.write(self.data)

    def saveObj(self, obj): pickle.dump(obj, self)
    def loadObj(self): return self.unpickle()


# prmp_pics.py

try:
    from PIL.ImageTk import Image, PhotoImage, BitmapImage
    from PIL import ImageSequence
    _PIL_ = True
except Exception as e:
    _PIL_ = False
    print('PIL <pillow> image library is not installed.')
    print(e)

from prmp_images import PRMP_PNGS, PRMP_GIFS, PRMP_XBMS


class PRMP_Pics:
    _dir = 'prmp_pics'
    subDir = ''

    @classmethod
    def picsExt(cls):
        ext = cls.subDir[:-1]
        return ext.replace('prmp_', '')

    @classmethod
    def picsHome(cls): return os.path.join(os.path.dirname(__file__), cls._dir)

    @classmethod
    def picName(cls, pic): return os.path.splitext(os.path.basename(pic))[0]

    @classmethod
    def files(cls):
        _dir = os.path.join(cls.picsHome(), cls.subDir)
        _files = []

        for r, d, ff in os.walk(_dir):
            for f in ff:
                if f.endswith(cls.picsExt()):
                    _files.append(os.path.join(r, f))

        return _files

    @classmethod
    def filesDict(cls):
        files = cls.files()
        _filesDict = {cls.picName(file): file for file in files}
        return _filesDict

    @classmethod
    def get(cls, bitmap):
        filesL = cls.files()

        if isinstance(bitmap, int):
            try: return filesL[bitmap]
            except: filesL[0]
        elif isinstance(bitmap, str):
            files = cls.filesDict()
            try: return files[bitmap]
            except: filesL[0]

    @classmethod
    def get(cls, bitmap):
        filesL = cls.files()

        if isinstance(bitmap, int):
            try: return filesL[bitmap]
            except: filesL[0]
        elif isinstance(bitmap, str):
            files = cls.filesDict()
            try: return files[bitmap]
            except: filesL[0]

class PRMP_Xbms(PRMP_Pics): subDir = 'prmp_xbms'

class PRMP_Pngs(PRMP_Pics): subDir = 'prmp_pngs'

class PRMP_Gifs(PRMP_Pics): subDir = 'prmp_gifs'

class PRMP_Images:

    @classmethod
    def get(cls, inbuilt, ext):
        base64 = cls.getBase64(inbuilt, ext)
        return b64decode(base64)

    @classmethod
    def getBase64(cls,  inbuilt, ext):
        if ext == 'png': return PRMP_PNGS[inbuilt]
        elif ext == 'gif': return PRMP_GIFS[inbuilt]
        elif ext == 'xbm': return PRMP_XBMS[inbuilt]

class PRMP_ImageFile(PRMP_File):

    def getImageFile(self, pix, ext='.png', db=0):
        if isinstance(pix, str):
            e = os.path.splitext(pix)[-1]

            if e in ['.png', '.xbm', '.gif', '.jpg', '.jpeg']: self.ext = e[1:]
            else: self.ext = ext

            if db:
                if self.ext == 'png': pic = PRMP_Pngs.get(pix)
                elif self.ext == 'gif': pic = PRMP_Gifs.get(pix)
                elif self.ext == 'xbm': pic = PRMP_Xbms.get(pix)
            else: pic = pix
            self.name = pix
            self.basename = os.path.basename(pic)
            return pic

    @property
    def image(self):
        if _PIL_: return Image.open(self)


    def __init__(self, imageFileName='', inbuilt=False, inExt='png', image=None, **kwargs):

        passed = [bool(a) for a in [imageFileName, image]].count(True)
        assert passed <= 1, 'Only one is required in [imageFileName, image]'

        if imageFileName and inbuilt: kwargs['data'] = PRMP_Images.get(imageFileName, inExt)

        super().__init__(filename=imageFileName, **kwargs)

        if image: image.save(self, inExt)

        PRMP_ImageFile.count += 1

class PRMP_Image:
    count = 0
    def __init__(self, filename='', inbuilt=False, inExt='png', resize=(), thumb=(), image=None, base64=b''):

        pic = None
        self.imageFile = None
        self.imgClass = PhotoImage
        self.resizedImage = None

        self._thumb = thumb
        self._resize = resize
        # print(base64)

        self.image = None
        self.tkImage = None
        self.name = ''
        self._animatedTkFrames = []
        self._animatedFrames = []

        if filename or image or base64:
            if filename:
                self.imageFile = filename if isinstance(filename, PRMP_ImageFile) else PRMP_ImageFile(filename, inbuilt=inbuilt, inExt=inExt)
            elif image: self.imageFile = PRMP_ImageFile(image=image)
            elif base64: self.imageFile = PRMP_ImageFile(base64=base64)
            else: self.imageFile = filename or image

            if not isinstance(self.imageFile, PRMP_ImageFile): raise ValueError('{} or {} is not a valid value.'.format(filename, image))

            self.name = self.imageFile.name
            self.ext = self.imageFile.ext

            if self.ext == 'xbm': self.imgClass = BitmapImage

            img = self.image = Image.open(self.imageFile) if _PIL_ else None
            if img: self.info = img.info

            if resize and len(resize) == 2 and resize[0] > 0 and resize[1] > 0: img = self.resizedImage = self.image.resize(resize)

            if thumb and len(thumb) == 2 and thumb[0] > 0 and thumb[1] > 0: img.thumbnail(thumb)

            self.img = img

            self.tkImage = self.imgClass(img, name=self.basename)

            PRMP_Image.count += 1

        else: raise ValueError('imageFile is None')

    def __str__(self): return str(self.tkImage)

    @property
    def animatedTkFrames(self):
        if self._animatedTkFrames: return self._animatedTkFrames
        else:
            for frame in ImageSequence.Iterator(self.img):
                if self._resize: img = frame.resize(self._resize)
                if self._thumb:
                    frame.thumbnail(self._thumb)
                    img = frame
                else: img = frame
                tkimg = self.imgClass(img)
                self._animatedTkFrames.append(tkimg)

            # for img in self.animatedFrames:
            #     tkimg = self.imgClass(img)
            #     self._animatedTkFrames.append(tkimg)
        return self._animatedTkFrames

    @property
    def animatedFrames(self):
        if self._animatedFrames: return self._animatedFrames
        else:
            for frame in ImageSequence.Iterator(self.img):
                print(99)
                if self._resize: img = frame.resize(self._resize)
                elif self._thumb:
                    frame.thumbnail(self._thumb)
                    img = frame
                else: img = frame
                self._animatedFrames.append(img)
            print(self._animatedFrames)
        return self._animatedFrames

    @property
    def interframe_durations(self): return [anf.info.get('duration', 0) for anf in self.animatedFrames]

    @property
    def basename(self):
        if self.imageFile: return self.imageFile.name
        return 'PRMP_Image(%d)'%PRMP_Image.count

    def resize(self, rz): return self.image.resize(rz)

    def get(self): return self.imageFile

    def resizeTk(self, rz): return self.imgClass(self.resize(rz))

    def thumbnail(self, rz): self.image.thumbnail(rz)

    def thumbnailTk(self, rz):
        self.thumbnail(rz)
        return self.imgClass(self.image)


# prmp_usefuls.py
import os, zipfile, subprocess

def zipPath(resource, destination='', latest=False):
    # Create name of new zip file, based on original folder or file name
    resource = resource.rstrip('\\').rstrip('/')
    # if resource in destination: TranxFerLogger.warning('Loop: Save somewhere else!')

    if not os.path.exists(resource): return

    if destination:
        if os.path.isdir(destination):
            baseFileName = os.path.basename(resource) + '.zip'
            zipFileName = os.path.join(destination, baseFileName)
        else: zipFileName = destination

    else: zipFileName = resource + '.zip'

    if os.path.isdir(resource): zipRootDir = os.path.basename(resource)

    if (os.path.isfile(zipFileName) == True) and (latest == False): return zipFileName

    # Create zip file
    with zipfile.ZipFile(zipFileName, "w", compression=zipfile.ZIP_DEFLATED) as zipFile:
        if os.path.isdir(resource):
            for root, dirs, files in os.walk(resource):
               for file in files:
                   filename = os.path.join(root, file)
                   arc = root.replace(resource, zipRootDir)
                   arcname = os.path.join(arc, file)
                   zipFile.write(filename, arcname, zipfile.ZIP_DEFLATED)
        else: zipFile.write(resource, zipFileName, zipfile.ZIP_DEFLATED)
    return zipFileName

class Reloader:
    def runner(self):
        args, env = [os.sys.executable] + os.sys.argv,  os.environ
        env["PRMP_TK"] = "RUNNING"
        while True:
            exit_code = subprocess.call(args, env=env, close_fds=False)
            if exit_code != 63: return exit_code
    def reloader(self, e=None):
        try: os.system("cls")
        except: os.system("clear")
        print("Reloading")
        os.sys.exit(63)
    def reload(self, func):
        try:
            if os.environ.get("PRMP_TK") == "RUNNING": func()
            else: os.sys.exit(self.runner())
        except Exception as E: pass


# prmp_datetime.py
__author__ = 'PRMPSmart@gmail.com'

import datetime
from calendar import day_abbr, day_name, month_abbr, month_name, Calendar

DAYS_ABBRS, DAYS_NAMES, MONTHS_ABBRS, MONTHS_NAMES = day_abbr[:], day_name[:], month_abbr[:], month_name[:]
WEEKS = ['Week %d'%a for a in range(1, 6)]


_DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

_DAYS_BEFORE_MONTH = [-1]  # -1 is a placeholder for indexing purposes.
dbm = 0
for dim in _DAYS_IN_MONTH[1:]:
    _DAYS_BEFORE_MONTH.append(dbm)
    dbm += dim
del dbm, dim

def _is_leap(year):
    "year -> 1 if leap year, else 0."
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def _days_before_year(year):
    "year -> number of days before January 1st of year."
    y = year - 1
    return y*365 + y//4 - y//100 + y//400

def _days_in_month(year, month):
    "year, month -> number of days in that month in that year."
    assert 1 <= month <= 12, month
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]

def _days_before_month(year, month):
    "year, month -> number of days in year preceding first day of month."
    assert 1 <= month <= 12, 'month must be in 1..12'
    return _DAYS_BEFORE_MONTH[month] + (month > 2 and _is_leap(year))

def _ymd2ord(year, month, day):
    "year, month, day -> ordinal, considering 01-Jan-0001 as day 1."
    assert 1 <= month <= 12, 'month must be in 1..12'
    dim = _days_in_month(year, month)
    assert 1 <= day <= dim, ('day must be in 1..%d' % dim)
    return (_days_before_year(year) +
            _days_before_month(year, month) +
            day)

_DI400Y = _days_before_year(401)    # number of days in 400 years
_DI100Y = _days_before_year(101)    #    "    "   "   " 100   "
_DI4Y   = _days_before_year(5)      #    "    "   "   "   4   "

# A 4-year cycle has an extra leap day over what we'd get from pasting
# together 4 single years.
assert _DI4Y == 4 * 365 + 1

# Similarly, a 400-year cycle has an extra leap day over what we'd get from
# pasting together 4 100-year cycles.
assert _DI400Y == 4 * _DI100Y + 1

# OTOH, a 100-year cycle has one fewer leap day than we'd get from
# pasting together 25 4-year cycles.
assert _DI100Y == 25 * _DI4Y - 1

def _ord2ymd(n):
    "ordinal -> (year, month, day), considering 01-Jan-0001 as day 1."

    # n is a 1-based index, starting at 1-Jan-1.  The pattern of leap years
    # repeats exactly every 400 years.  The basic strategy is to find the
    # closest 400-year boundary at or before n, then work with the offset
    # from that boundary to n.  Life is much clearer if we subtract 1 from
    # n first -- then the values of n at 400-year boundaries are exactly
    # those divisible by _DI400Y:
    #
    #     D  M   Y            n              n-1
    #     -- --- ----        ----------     ----------------
    #     31 Dec -400        -_DI400Y       -_DI400Y -1
    #      1 Jan -399         -_DI400Y +1   -_DI400Y      400-year boundary
    #     ...
    #     30 Dec  000        -1             -2
    #     31 Dec  000         0             -1
    #      1 Jan  001         1              0            400-year boundary
    #      2 Jan  001         2              1
    #      3 Jan  001         3              2
    #     ...
    #     31 Dec  400         _DI400Y        _DI400Y -1
    #      1 Jan  401         _DI400Y +1     _DI400Y      400-year boundary
    n -= 1
    n400, n = divmod(n, _DI400Y)
    year = n400 * 400 + 1   # ..., -399, 1, 401, ...

    # Now n is the (non-negative) offset, in days, from January 1 of year, to
    # the desired date.  Now compute how many 100-year cycles precede n.
    # Note that it's possible for n100 to equal 4!  In that case 4 full
    # 100-year cycles precede the desired day, which implies the desired
    # day is December 31 at the end of a 400-year cycle.
    n100, n = divmod(n, _DI100Y)

    # Now compute how many 4-year cycles precede it.
    n4, n = divmod(n, _DI4Y)

    # And now how many single years.  Again n1 can be 4, and again meaning
    # that the desired day is December 31 at the end of the 4-year cycle.
    n1, n = divmod(n, 365)

    year += n100 * 100 + n4 * 4 + n1
    if n1 == 4 or n100 == 4:
        assert n == 0
        return year-1, 12, 31

    # Now the year is correct, and n is the offset from January 1.  We find
    # the month via an estimate that's either exact or one too large.
    leapyear = n1 == 3 and (n4 != 24 or n100 == 3)
    assert leapyear == _is_leap(year)
    month = (n + 50) >> 5
    preceding = _DAYS_BEFORE_MONTH[month] + (month > 2 and leapyear)
    if preceding > n:  # estimate is too large
        month -= 1
        preceding -= _DAYS_IN_MONTH[month] + (month == 2 and leapyear)
    n -= preceding
    assert 0 <= n < _days_in_month(year, month)

    # Now the year and month are correct, and n is the offset from the
    # start of that month:  we're done!
    return year, month, n+1

class OldCompareByDate:
    def __lt__(self, other):
        if other == None: return False
        return self.date < other.date
    def __le__(self, other):
        if other == None: return False
        return self.date <= other.date
    def __eq__(self, other):
        if other == None: return False
        return self.date is other.date
    def __ne__(self, other):
        if other == None: return True
        return self.date != other.date
    def __gt__(self, other):
        if other == None: return True
        return self.date > other.date
    def __ge__(self, other):
        if other == None: return True
        return self.date >= other.date

class CompareByDate:
    def __lt__(self, other):
        if other == None: return False
        return self.date.ymdToOrd < other.date.ymdToOrd
    def __le__(self, other):
        if other == None: return False
        return self.date.ymdToOrd <= other.date.ymdToOrd
    def __eq__(self, other):
        if other == None: return False
        return self.date.ymdToOrd is other.date.ymdToOrd
    def __ne__(self, other):
        if other == None: return True
        return self.date.ymdToOrd != other.date.ymdToOrd
    def __gt__(self, other):
        if other == None: return True
        return self.date.ymdToOrd > other.date.ymdToOrd
    def __ge__(self, other):
        if other == None: return True
        return self.date.ymdToOrd >= other.date.ymdToOrd

class CompareByWeek:
    def __lt__(self, other):
        if other == None: return False
        return self.date.weekMonthYearTuple < other.date.weekMonthYearTuple
    def __le__(self, other):
        if other == None: return False
        return self.date.weekMonthYearTuple <= other.date.weekMonthYearTuple
    def __eq__(self, other):
        if other == None: return False
        return self.date.weekMonthYearTuple == other.date.weekMonthYearTuple
    def __ne__(self, other):
        if other == None: return True
        return self.date.weekMonthYearTuple != other.date.weekMonthYearTuple
    def __gt__(self, other):
        if other == None: return True
        return self.date.weekMonthYearTuple > other.date.weekMonthYearTuple
    def __ge__(self, other):
        if other == None: return True
        return self.date.weekMonthYearTuple >= other.date.weekMonthYearTuple

class CompareByMonth:
    def __lt__(self, other):
        if other == None: return False
        return self.date.monthYearTuple < other.date.monthYearTuple
    def __le__(self, other):
        if other == None: return False
        return self.date.monthYearTuple <= other.date.monthYearTuple
    def __eq__(self, other):
        if other == None: return False
        return self.date.monthYearTuple == other.date.monthYearTuple
    def __ne__(self, other):
        if other == None: return True
        return self.date.monthYearTuple != other.date.monthYearTuple
    def __gt__(self, other):
        if other == None: return True
        return self.date.monthYearTuple > other.date.monthYearTuple
    def __ge__(self, other):
        if other == None: return True
        return self.date.monthYearTuple >= other.date.monthYearTuple

class CompareByYear:
    def __lt__(self, other):
        if other == None: return False
        return self.date.year < other.date.year
    def __le__(self, other):
        if other == None: return False
        return self.date.year <= other.date.year
    def __eq__(self, other):
        if other == None: return False
        return self.date.year == other.date.year
    def __ne__(self, other):
        if other == None: return True
        return self.date.year != other.date.year
    def __gt__(self, other):
        if other == None: return True
        return self.date.year > other.date.year
    def __ge__(self, other):
        if other == None: return True
        return self.date.year >= other.date.year

class PRMP_DateTime(datetime.datetime, PRMP_Mixins):
    date_fmt = "%d/%m/%Y"
    daysAbbr, daysNames, monthsAbbrs, monthsNames = day_abbr[:], day_name[:], month_abbr[:], month_name[:]
    Errors = PRMP_Errors.PRMP_DateTimeError

    timedelta = datetime.timedelta


    # the __add__ and __sub__ are implementaions are purely by PRMPSmart@gmail.com

    def __getitem__(self, item):
        # print(item)
        if item == slice(None, None, None): return self
        return PRMP_Mixins.__getitem__(self, item)

    def __add__(self, add_month):
        if isinstance(add_month, self.timedelta): return self.createDateTime(obj=super().__add__(add_month))

        elif isinstance(add_month, int):
            months = self.month + add_month
            div, mod = divmod(months, 12)
            if (div == 0) or (months == 12):
                # it means that the months falls within the current self.year
                return self.createDateTime(self.year, months, self.day)
            elif div > 0:
                # it means that the new_month falls within the upcoming years
                if not mod:
                    # it means self.month = 12 and sub_month *12
                    mod = 12
                    # the resulting month is 12
                    div -= 1
                    # since self.month = 12 and sub_month *12 therefore div is having an additional self.month 12 in it
                return self.createDateTime(self.year + div, mod, self.day)

    def __sub__(self, sub_month):
        if isinstance(sub_month, self.timedelta): return self.createDateTime(obj=super().__sub__(sub_month))

        elif isinstance(sub_month, self.__class__): return self.diffInMonth(sub_month)
        elif isinstance(sub_month, int):

            if sub_month < self.month:
                # since sub_month is lower than self.month, the new month is within that same year
                return self.createDateTime(self.year, self.month - sub_month, self.day)

            elif sub_month == self.month:
                # since sub_month is equal to self.month, the new month is automatically last month of last year
                return self.createDateTime(self.year - 1, 12, self.day)

            # since the above conditions are not met, it means that the sub_month is actually more than self.month which means that the new month is actually in the recent years if not the last one.
            else:
                # since 12 months == 1 year; recent years in the sub_month = sub_month // 12, and the remaining months is sub_month % 12.
                div, mod =  divmod(sub_month, 12)

                if div == 0:
                    # the sub_month > self.month but < 12
                    rem = sub_month - self.month
                    #  first minus its exact month from itself, then minus the remaining months
                    first = self - self.month
                    second = first - rem
                    return second

                else:
                    # therefore, subtract the recent years from the current year, creating a new PRMP_DateTime with everything else in place except the year
                    # the sub_month is more than 12
                    year = self.createDateTime(self.year - div, self.month, self.day)
                    # the remaining months will now fall into the categories of (sub_month < self.month) and ( sub_month == self.month).
                    # it will now look as if it's a loop, the remaining months will now be subtracted from the new year-PRMP_DateTime, the process will now fall into the first two conditions in the new year-PRMP_DateTime
                    return year - mod

    def __str__(self): return repr(self)
    # def __str__(self): return self.strftime(self.date_fmt)

    def get(self, name, default=''): return self.getFromSelf(name, default)

    @property
    def date(self): return self.strftime(self.date_fmt)

    @property
    def strDate(self): return self.date

    @property
    def totalDays(self): # also equal to _days_in_month
        lis = [1, 3, 5, 7, 8, 10, 12]
        if self.month == 2: return 28 + self.isLeap
        elif self.month in lis: return 31
        else: return 30

    @classmethod
    def getDayNum(cls, day):
        error = cls.Errors('day must be among {} or {}'.format(cls.daysAbbrs, cls.daysNames))
        if isinstance(day, str):
            if day in cls.daysAbbrs: dayNum = cls.daysAbbrs.index(day) + 1
            elif day in cls.daysNames: dayNum = cls.daysNames.index(day) + 1
            else: raise error
            return dayNum
        else: raise error

    @classmethod
    def getDayName(cls, day, abbr=False):
        range_ = list(range(1, 31))
        error = cls.Errors('day must be among {}'.format(range_))
        if isinstance(day, int):
            if day in range_:
                if abbr: dayName = cls.daysAbbrs[day - 1]
                else: dayName = cls.daysNames[day - 1]
            else: raise error
            return dayName
        else: raise error

    @classmethod
    def checkDateTime(cls, date, dontRaise=False):
        date = cls.getDMYFromDate(date)
        if not isinstance(date, PRMP_DateTime):
            if dontRaise: return False
            raise cls.Errors('Date must be an instance of PRMP_DateTime')
        return date

    @classmethod
    def now(cls): return cls.createDateTime(obj=super().now())

    @classmethod
    def getMonthNum(cls, month):
        error = cls.Errors('month must be among {} or {}'.format(cls.monthsAbbrs), cls.monthsNames)
        if isinstance(month, str):
            if month in cls.monthsAbbrs: monthNum = cls.monthsAbbrs.index(month)
            elif month in cls.monthsNames: monthNum = cls.monthsNames.index(month)
            else: raise error
            return monthNum
        else: raise error

    @classmethod
    def getMonthName(cls, month, abbr=False):
        range_ = list(range(1, 12))
        error = cls.Errors('month must be among {}'.format(range_))
        if isinstance(month, int):
            if month in range_:
                if abbr: monthName = cls.monthsAbbrs[month - 1]
                else: monthName = cls.monthsNames[month - 1]
            else: raise error
            return monthName
        else: raise error

    @classmethod
    def createDateTime(cls, year=None, month=1, day=1, auto=False, obj=None, week=None, hour=0, minute=0, second=0):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            year = obj.year
            month = obj.month
            day = obj.day
            try:
                hour = obj.hour
                minute = obj.minute
                second = obj.second
            except: pass

        elif auto: return cls.now()

        elif week:
            assert month and year, 'Month and Year are also required.'
            weeks = cls.monthWeekDays(year, month)
            return weeks[week-1][0]

        if isinstance(month, str): month = cls.getMonthNum(month)

        if isinstance(day, str): day = cls.getDayNum(month)

        dummy = cls(year, month, 1).totalDays
        if dummy < day: day = dummy

        return cls(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    @property
    def dayNum(self): return self.day
    @property
    def dayName(self): return self.strftime('%A')
    @property
    def dayNameAbbr(self): return self.strftime('%a')
    @property
    def monthName(self): return self.strftime('%B')
    @property
    def monthNameAbbr(self): return self.strftime('%b')

    @property
    def monthYear(self): return '{}-{}'.format(self.monthName, self.year)
    @property
    def weekMonthYear(self): return '{}, {}-{}'.format(self.weekName, self.monthName, self.year)
    @property
    def monthYearTuple(self): return (self.year, self.month)
    @property
    def weekMonthYearTuple(self): return (self.year, self.month, self.week)
    @property
    def dayMonthYear(self): return '{}-{}'.format(self.day, self.monthYear)

    @property
    def isoWeekDay(self):
        d = (int(self.isoweekday()) + 1) % 7
        if d == 0: return 7
        return d
    @property
    def weekDay(self): return (int(self.weekday()) + 1) % 7

    @property
    def weekInYear(self): return int(self.isocalendar()[1])

    def isSameDate(self, date):
        self.checkDateTime(date)
        return self.date == date.date

    def isSameDay(self, date): return self.day == date.day

    def isSameDayName(self, date): return self.dayName == date.dayName

    def isSameYear(self, date): return self.year == date.year

    def isSameMonth(self, date): return self.month == date.month

    def isSameWeek(self, date): return self.week == date.week

    def isSameMonthYear(self, date): return self.monthYearTuple == date.monthYearTuple

    def isSameWeekMonthYear(self, date): return self.weekMonthYearTuple == date.weekMonthYearTuple

    @classmethod
    def _monthWeekDays(cls, year=None, month=None, monday=False, dateObj=None):
        'getting the weeks in a month'
        if dateObj: year, month = dateObj.year, dateObj.month

        year = int(year)
        if isinstance(month, str): month = MONTHS_NAMES[:].index(month)

        ca = Calendar(0 if monday else 6)

        month_wks = ca.monthdatescalendar(year, month)
        month_wks2 = ca.monthdays2calendar(year, month)

        weeks = []

        for week in month_wks:
            weeks_days = []

            for day in week:

                Day = cls.createDateTime(obj=day)
                weeks_days.append(Day)

            weeks.append(weeks_days)

        return weeks

    def monthWeekDays(self, **kwargs): return self._monthWeekDays(dateObj=self, **kwargs)

    @classmethod
    def getMonthYearOfDateTimes(cls, dts): return [dt.monthYear for dt in dts]

    @classmethod
    def monthYearOfMonthWeekDays(cls, **kwargs):
        weeks = cls.monthWeekDays(**kwargs)
        weeks_monthYear = [cls.getMonthYearOfDateTimes(week) for week in weeks]
        return weeks_monthYear

    @property
    def weekDates(self):
        'returns all the days in a month in a list of weeks'
        return self.monthWeekDays()

    @property
    def oneDateInWeeks(self):
        'returns a list of containing a day from each weeks in the month'
        weekDates = self.weekDates
        one = weekDates[0]
        last = weekDates[-1]

        dates = []

        for week in weekDates:
            if week == one: dates.append(week[-1])
            else: dates.append(week[0])
            # else: dates.append(week[0])

        return dates
    @property
    def monthDates(self):
        'returns all the days that makes up the 4 or 5 weeks in a list'
        days = []
        for week in self.weekDates:
            for day in week: days.append(day)
        return days

    @property
    def monthOnlyDates(self):
        'returns all the days in a month in a list'
        dates = self.monthDates
        days = [day for day in dates if self.isSameMonthYear(day)]
        return days

    @property
    def allSpecDaysDates(self):
        'returns a list of list each containing the days of the same name'
        allDates = self.monthOnlyDates
        leng = range(len(self.daysNames))

        specs = [[] for a in leng]

        for date in allDates:
            for day in leng:
                dayName = self.daysNames[day]
                if date.dayName == dayName: specs[day].append(date)

        return specs

    @property
    def specDaysDates(self):
        'returns a list of each day from each list returned from allSpecDaysDates'
        allDates = self.allSpecDaysDates
        leng = range(len(allDates))

        specs = [a[0] for a in allDates]

        return specs

    @property
    def monthsInYear(self):
        'returns the months in the year of this current PRMP_DateTime object'
        currentMonth = self.month
        months = range(1, 13)
        monthsDates = []

        for month in months:
            if month < currentMonth: monthsDates.append(self - month)
            elif month == currentMonth: monthsDates.append(self)
            elif month > currentMonth:
                diff = month - currentMonth
                monthsDates.append(self + diff)
        return monthsDates


    @property
    def week(self):
        'returns the week number that this date is in its month'
        weeks = self.weekDates
        for wk in weeks:
            _wk = [w.date for w in wk]
            if self.date in _wk: return weeks.index(wk) + 1
        return 0

    @property
    def weekName(self): return 'Week {}'.format(self.week)

    @classmethod
    def getDate(cls, status=0, form=1, day_=0):

        now = cls.now()
        days = cls.timedelta(status)
        day = now + days

        if form == 0: fmt = "%D"
        elif form == 1:  fmt = "%d/%m/%Y"
        elif form == 2: fmt = "%a %d %B %Y"
        elif form == 3: fmt = "%d %B %Y"
        elif form == 4: fmt = "%d %b %Y"
        elif form == 5: fmt = "%d %a %b %Y"
        if day_:
            add = tuple(day.strftime("%a %d").split()), day.strftime(fmt)
            return tuple(add)
        elif cls.month_year: return day.strftime("%d/") + cls.month_year # testing
        else: return day.strftime(fmt)

    @classmethod
    def getDMYFromDate(cls, date):
        if date:
            if isinstance(date, str):
                try: day, month, year = cls.getNumsInStrAsList(None, date, [2], 1)
                except Exception as e: return

                day, month, year = int(day), int(month), int(year)
                dt = cls(year, month, day)
                return dt
            elif isinstance(date, cls): return date

    def diffInMonth(self, date):
        'returns the different in the current month and the given month'
        self.checkDateTime(date)
        if self.monthYearTuple == date.monthYearTuple: return 0
        elif self > date: maxDate, minDate = self, date
        elif self < date: maxDate, minDate = date, self

        yearDiff = maxDate.year - minDate.year
        monthFromYearDiff = yearDiff * 12
        monthDiff = maxDate.month - minDate.month
        monthsDiff = monthFromYearDiff + monthDiff

        return monthsDiff

    @classmethod
    def is_leap(cls, year): return _is_leap(year)

    @property
    def isLeap(self): return self.is_leap(self.year)

    @classmethod
    def days_before_year(cls, year): return _days_before_year(year)

    @property
    def daysBeforeYear(self): return self.days_before_year(self.year)

    @classmethod
    def days_in_month(cls, year, month): return _days_in_month(year, month)

    @property
    def daysInMonth(self): return self.days_in_month(self.year, self.month)

    @classmethod
    def days_before_month(cls, year, month): return _days_before_month(year, month)

    def daysBeforeMonth(self): return self.days_before_month(self.year, self.month)

    @classmethod
    def ymd2ord(cls, year, month, day): return _ymd2ord(year, month, day)

    @property
    def ymdToOrd(self): return self.ymd2ord(self.year, self.month, self.day)

    @classmethod
    def ord2ymd(cls, ord_): return _ord2ymd(ord_)

    def addTimes(self, **kwargs): return self + self.timedelta(**kwargs)

    def addMonths(self, months): return self + months


# prmp_setup.py

from os import mkdir, path, listdir, sys, chdir, pathsep, system, get_exec_path, getcwd

inno_script_example = '''
    ; Script generated by the PRMP Smart SETUP WIZARD.
    ; SEE THE DOCUMENTATION FOR DETAILS ON CREATING PRMP Smart SETUP SCRIPT FILES!

    #define MyAppName "TranxFer"
    #define MyAppVersion "1.5"
    #define MyAppPublisher "PRMPSmart Inc."
    #define MyAppURL "http://www.tranxFer.com/"
    #define MyAppExeName "TranxFer.exe"

    [Setup]
    ; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
    ; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
    AppId={{C280E116-9281-4691-B2FE-E53773049917}
    AppName={#MyAppName}
    AppVersion={#MyAppVersion}
    ;AppVerName={#MyAppName} {#MyAppVersion}
    AppPublisher={#MyAppPublisher}
    AppPublisherURL={#MyAppURL}
    AppSupportURL={#MyAppURL}
    AppUpdatesURL={#MyAppURL}
    DefaultDirName={autopf}\{#MyAppName}
    DefaultGroupName={#MyAppName}
    AllowNoIcons=yes
    ; The [Icons] "quicklaunchicon" entry uses {userappdata} but its [Tasks] entry has a proper IsAdminInstallMode Check.
    UsedUserAreasWarning=no
    ; Remove the following line to run in administrative install mode (install for all users.)
    PrivilegesRequired=lowest
    PrivilegesRequiredOverridesAllowed=dialog
    OutputDir={output directory here}
    OutputBaseFilename=TranxFer-setup
    Password=mimi
    Compression=lzma
    SolidCompression=yes
    WizardStyle=modern

    [Languages]
    Name: "english"; MessagesFile: "compiler:Default.isl"

    [Tasks]
    Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
    Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

    [Files]
    Source: {put the main exe here};
    DestDir: "{app}"; Flags: ignoreversion
    Source: "{put the path to folder needed here} \*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
    ; NOTE: Don't use "Flags: ignoreversion" on any shared system files

    [Icons]
    Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
    Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
    Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
    Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
    Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

    [Run]
    Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
'''

classifiers = [
    'Development Status :: 1 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Python Software Foundation License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
    'Programming Language :: C/C++',
    'Topic :: Software Development :: Bug Tracking',
]
platforms = ['Windows']
keywords = []
license_ = ''

class Holder: pass

class PRMP_Setup:

    def __init__(self, type_='NaN', *args, **kwargs):
        self.type = type_
        if hasattr(self, self.type): getattr(self, self.type)(*args, **kwargs)
        else: raise ValueError(f'{self.type} is not a valid build type!')

    def build(self):
        func = f'_{self.type}'
        getattr(self, func)()

    def get_scripts(self, folder):
        files = []
        if path.isdir(folder):
            for fi in listdir(folder):
                p = path.join(folder, fi)
                if path.isfile(p): files.append(p)
            return files, f'/{folder}'
        else: return [folder], ''

    def build_ext(self, folder='', scripts=[], description='', meta_datas={}, classifiers=classifiers, platforms=platforms, keywords=[], license='', name='', inplace=False, dest='', version='1.0'):
        self.holder = Holder()
        name = name or path.basename(folder[:-3]) if folder.endswith('.py') else folder

        self.holder.meta_datas = dict(
            name=name,
            version=version,
            author='PRMPSmart',
            author_email='prmpsmart@gmail.com',
            maintainer='PRMPSmart',
            maintainer_email='prmpsmart@gmail.com',
            url=f'github.com/prmpsmart/{name}',
            description=description or f'an extension module for {folder}',
            long_description='an example to test the creation of python extension modules et all.',
            download_url=f'github.com/prmpsmart/{name}.git',
            classifiers=classifiers,
            platforms=platforms,
            keywords=keywords,
            license=license_,
        )
        self.holder.meta_datas.update(meta_datas)

        self.holder.scripts, self.holder.dest = (scripts, dest) or self.get_scripts(folder)

        self.holder.directory = '--inplace' if inplace else f'-b{self.holder.dest}'

    def _build_ext(self):
        from distutils.core import setup
        from Cython.Build import cythonize
        for d in ['c', 'pyd']:
            try: mkdir(d)
            except: pass
        ext_modules = cythonize(self.holder.scripts, language_level=3, build_dir='c', output_dir='c')

        sys.argv.extend(['build_ext', self.holder.directory])
        setup(ext_modules=ext_modules, **self.holder.meta_datas)

    def pyinstaller(self, scripts=[], console=True, extra_commands=[], log_level='info', datas={}, binaries={}, name='', onefile=False, icon='', clean=False, noconfirm=False):
        '''
        :param console: a boolean whether to enable consoled executable or not
        :param extra_commands: commands to pass to PyInstaller
        '''

        # assert scripts, 'Provide script(s) to compile!'

        if isinstance(scripts, str): scripts = [scripts]


        log_level = log_level.upper()
        log_levels = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]
        assert log_level in log_levels, f'{log_level} not in {log_levels}.'

        self.holder = Holder()

        self.holder.scripts = scripts
        self.holder.name = f'-n{name}'

        self.holder.console = '-c' if console else '-w'
        self.holder.onefile = '-F' if onefile else '-D'
        self.holder.icon = '-i{icon}' if icon else ''

        self.holder.datas = []

        for data in datas:
            dat = [f'--add-data', pathsep.join([data, datas[data]])]
            self.holder.datas.extend(dat)

        self.holder.binaries = []

        for binary in binaries:
            dat = [f'--add-binary', pathsep.join([binary, binaries[binary]])]
            self.holder.binaries.extend(dat)

        self.holder.extra_commands = extra_commands
        self.holder.clean = '--clean' if clean else ''
        self.holder.noconfirm = '-y' if noconfirm else ''

        self.holder.log_level = ['--log-level', log_level]

        self.holder.run_parameter = [self.holder.name, self.holder.console, self.holder.onefile, self.holder.icon, *self.holder.extra_commands, *self.holder.datas, *self.holder.binaries, self.holder.clean, self.holder.noconfirm, *self.holder.log_level, *self.holder.scripts]

        while '' in self.holder.run_parameter: self.holder.run_parameter.remove('')

        # print(self.holder.run_parameter)

    def _pyinstaller(self):
        import PyInstaller.__main__
        PyInstaller.__main__.run(self.holder.run_parameter)

    def inno_setup(self, script, old_ver='', new_ver='', gen_script=False, gui=False, customize=False, author='PRMP Smart'):
        self.holder = Holder()
        self.holder.script = script
        self.holder.new_ver = new_ver
        self.holder.old_ver = old_ver
        self.holder.author = author
        self.holder.gui = gui
        self.holder.customize = customize

        self.holder.script = script
        self.holder.gen_script = f'compil32 /wizard "{author} SETUP WIZARD" "{script}"' if gen_script else False


        program = 'iscc' if not gui else 'compil32 /cc'
        self.holder.program = f'{program} {script}'

    def customize_script(self, script, old_ver='', new_ver='', author=''):
        with open(script) as old: text = old.read()
        text = text.replace("INNO", author)
        if old_ver and new_ver: text = text.replace(old_ver, new_ver)
        with open(script, 'w') as new: new.write(text)

    def _inno_setup(self):
        inno_installed = "Inno Setup".upper() in ''.join(get_exec_path()).upper()
        if not inno_installed: raise ValueError('Inno Setup Compiler is not installed. You can get it on https://jrsoftware.org')

        if self.holder.gen_script: system(self.holder.gen_script)
        if self.holder.customize: self.customize_script(self.holder.script, old_var=self.holder.old_ver, new_var=self.holder.new_ver, author=self.holder.author)
        system(self.holder.program)

# end
