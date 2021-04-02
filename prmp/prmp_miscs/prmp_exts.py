from io import BytesIO
from base64 import b64encode, b64decode
import zlib, pickle
from .prmp_mixins import PRMP_Mixins, os


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

        self.name = filename
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
        
        self.basename = os.path.basename(self.name)
        self.name_n_ext = self.basename.split('.')[0]
        
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
    def decompressedData(self): return zlib.decompress(self.data)

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


