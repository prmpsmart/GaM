
from io import BytesIO
from PIL.ImageTk import Image, PhotoImage, BitmapImage
import zlib, pickle, os

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

class PRMP_Xbms(PRMP_Pics): subDir = 'prmp_xbms'
    
class PRMP_Pngs(PRMP_Pics): subDir = 'prmp_pngs'
    
class PRMP_Gifs(PRMP_Pics): subDir = 'prmp_gifs'

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

    def __init__(self, fp=None, ext='.png', db=0, image=None):
        self.name = None
        self.basename = None
        self.ext = ext
        self._data = b''

        if isinstance(fp, str):
            file = self.getImageFile(fp, ext=ext, db=db)
            self._data = open(file, 'rb').read()
        elif isinstance(fp, bytes): self._data = fp

        super().__init__(self._data)

        if image: image.save(self, 'png')

        PRMP_ImageFile.count += 1

    def __str__(self):
        if self.name:return f'PRMP_ImageFile({self.name})'
        else: return f'PRMP_ImageFile({PRMP_ImageFile.count})'

    def __len__(self): return self.size

    @property
    def data(self): return self.getvalue()
    @property
    def compressedData(self): return zlib.compress(self.data)
    @property
    def cdata(self): return self.compressedData
    @property
    def size(self): return len(self.data)

    def get(self): return self.data

    def setCompressedData(self, compressedData):
        decomData = zlib.decompress(compressedData)
        self.write(decomData)
    
    def pickle(self, file):
        try: f = open(file, 'wb')
        except: f = file
        pickle.dump(self, f)

    def save(self, file):
        try: f = open(file, 'wb')
        except: f = file

        f.write(self.data)

class PRMP_Image:
    count = 0
    def __init__(self, imageFile=None, ext='png', resize=(), thumb=(), db=0, image=None):
        
        pic = None
        self.ext = 'jpg'
        self.imageFile = imageFile
        self.imgClass = PhotoImage
        self.resizedImage = None
        self.image = None
        self.tkImage = None
        self.name = ''
        self.animatedFrames = []
        self.animatedTksImages = []

        if imageFile or image:
            if isinstance(imageFile, (str, bytes)): self.imageFile = PRMP_ImageFile(imageFile, ext=ext, db=db)
            elif image: self.imageFile = PRMP_ImageFile(image=image)
            
            self.name = self.imageFile.name
            self.ext = self.imageFile.ext
            
            if self.ext in ['xbm', '.xbm']: self.imgClass = BitmapImage

            img = self.image = Image.open(self.imageFile)

            if resize and len(resize) == 2:
                self.resizedImage = self.image.resize(resize)
                img = self.resizedImage
            
            if thumb and len(thumb) == 2: img.thumbnail(thumb)

            
            if self.ext == 'gifs': sequence = [self.imgClass(img) for img in ImageSequence.Iterator(img)]
            
            self.tkImage = self.imgClass(img, name=self.basename)

            PRMP_Image.count += 1
            
        else: raise ValueError('imageFile is None')

    def __str__(self): return str(self.tkImage)

    @property
    def basename(self):
        if self.imageFile and self.imageFile.basename: return self.imageFile.basename
        return f'PRMP_Image({PRMP_Image.count})'

    def resize(self, rz): return self.image.resize(rz)

    def get(self): return self.imageFile

    def resizeTk(self, rz): return self.imgClass(self.resize(rz))

    def thumbnail(self, rz): self.image.thumbnail(rz)
    
    def thumbnailTk(self, rz): 
        self.thumbnail(rz)
        return self.imgClass(self.image)






