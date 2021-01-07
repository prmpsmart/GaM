
from io import BytesIO
from PIL.ImageTk import Image, PhotoImage, BitmapImage
from PIL import ImageSequence
import zlib, pickle, os, imghdr
from base64 import b64encode, b64decode
from .prmp_images import PRMP_PNGS, PRMP_GIFS, PRMP_XBMS



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
        assert passed == 1, 'Only one is required in [filename, base64, image]'

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

        self.ext = imghdr.what(image or self)
        if image: image.save(self, self.ext)

        PRMP_ImageFile.count += 1

    def __str__(self):
        if self.name: return f'PRMP_ImageFile({self.name})'
        else: return f'PRMP_ImageFile({PRMP_ImageFile.count})'

    def __len__(self): return self.size

    @property
    def data(self): return self.getvalue()
    @property
    def compressedData(self): return zlib.compress(self.data)
    @property
    def cdata(self): return self.compressedData
    @property
    def base64Data(self): return b64encode(self.data)
    @property
    def size(self): return len(self.data)
    def get(self): return self.data

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
        self.image = None
        self.tkImage = None
        self.name = ''
        self.animatedFrames = []
        self.animatedTksImages = []
        self.interframe_duration = None

        if filename or image:
            if isinstance(filename, (str, bytes)): self.imageFile = PRMP_ImageFile(filename, inbuilt=inbuilt, inExt=inExt)
            elif image: self.imageFile = PRMP_ImageFile(image=image)
            
            self.name = self.imageFile.name
            self.ext = self.imageFile.ext
            
            if self.ext == 'xbm': self.imgClass = BitmapImage

            img = self.image = Image.open(self.imageFile)

            if resize and len(resize) == 2:
                self.resizedImage = self.image.resize(resize)
                img = self.resizedImage
            
            if thumb and len(thumb) == 2: img.thumbnail(thumb)
            
            try:
                self.info = img.info
                print(img.__dict__['tile'][0][0], '\n')
                sequence = [self.imgClass(img) for img in ImageSequence.Iterator(img)]
                self.interframe_duration = 0
            except: pass
            
            self.tkImage = self.imgClass(img, name=self.basename)

            PRMP_Image.count += 1
            
        else: raise ValueError('imageFile is None')

    def __str__(self): return str(self.tkImage)

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






