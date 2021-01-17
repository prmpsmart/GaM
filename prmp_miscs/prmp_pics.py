
from io import BytesIO
from PIL.ImageTk import Image, PhotoImage, BitmapImage
from PIL import ImageSequence
import zlib, pickle, os
from base64 import b64encode, b64decode
from .prmp_images import PRMP_PNGS, PRMP_GIFS, PRMP_XBMS

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

class PRMP_ImageFile(BytesIO):
    count = 0

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

    def __init__(self, filename='', inbuilt=False, inExt='png', base64=b'', image=None, data=b''):
        passed = [bool(a) for a in [filename, base64, image]].count(True)
        assert passed <= 1, 'Only one is required in [filename, base64, image]'

        self.name = None
        self._data = data
        
        if data: self.name = f'data_{PRMP_ImageFile.count}'

        elif filename:
            self.name = os.path.basename(filename)
            if inbuilt: self._data = PRMP_Images.get(filename, inExt)
            else: self._data = open(filename, 'rb').read()

        elif base64:
            self._data = b64decode(base64)
            self.name = f'base64_{PRMP_ImageFile.count}'

        super().__init__(self._data)
        
        if image: image.save(self, inExt)

        PRMP_ImageFile.count += 1

    def __str__(self):
        if self.name: return f'PRMP_ImageFile({self.name})'
        else: return f'PRMP_ImageFile({PRMP_ImageFile.count})'

    def __len__(self): return self.size

    @property
    def data(self): return self.getvalue()
    
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


    @property
    def image(self): return Image.open(self)

    def pickle(self, file   ):
        try: f = open(file, 'wb')
        except: f = file
        obj = None
        pickle.dump(self, f)

    def save(self, file):
        try: f = open(file, 'wb')
        except: f = file

        f.write(self.data)

class PRMP_Image:
    count = 0
    def __init__(self, filename='', inbuilt=False, inExt='png', resize=(), thumb=(), image=None):
        
        pic = None
        self.imageFile = None
        self.imgClass = PhotoImage
        self.resizedImage = None
        
        self._thumb = thumb
        self._resize = resize

        self.image = None
        self.tkImage = None
        self.name = ''
        self._animatedTkFrames = []
        self._animatedFrames = []

        if filename or image:
            if isinstance(filename, (str, bytes)): self.imageFile = PRMP_ImageFile(filename, inbuilt=inbuilt, inExt=inExt)
            elif image: self.imageFile = PRMP_ImageFile(image=image)
            else: self.imageFile = filename or image

            if not isinstance(self.imageFile, PRMP_ImageFile): raise ValueError(f'{filename} or {image} is not a valid value. ')
            
            self.name = self.imageFile.name
            self.ext = self.imageFile.ext
            
            if self.ext == 'xbm': self.imgClass = BitmapImage

            img = self.image = Image.open(self.imageFile)
            self.info = img.info

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
        return f'PRMP_Image({PRMP_Image.count})'

    def resize(self, rz): return self.image.resize(rz)

    def get(self): return self.imageFile

    def resizeTk(self, rz): return self.imgClass(self.resize(rz))

    def thumbnail(self, rz): self.image.thumbnail(rz)
    
    def thumbnailTk(self, rz): 
        self.thumbnail(rz)
        return self.imgClass(self.image)






# tranxfer_c2 -D -A192.168.43.1 -P7767