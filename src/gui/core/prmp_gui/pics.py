
from os import path, walk
from io import BytesIO
from PIL.ImageTk import Image, PhotoImage, BitmapImage
import zlib, pickle

class Pics:
    _dir = 'pics'
    subDir = ''
    
    @classmethod
    def picsExt(cls): return cls.subDir[:-1]
    
    @classmethod
    def picsHome(cls): return path.join(path.dirname(__file__), cls._dir)
    
    @classmethod
    def picName(cls, pic): return path.splitext(path.basename(pic))[0]
    
    @classmethod
    def files(cls):
        _dir = path.join(cls.picsHome(), cls.subDir)
        _files = []
        
        for r, d, ff in walk(_dir):
            for f in ff:
                if f.endswith(cls.picsExt()):
                    _files.append(path.join(r, f))
        
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

class Xbms(Pics): subDir = 'xbms'
    
class Pngs(Pics): subDir = 'pngs'
    
class Gifs(Pics): subDir = 'gifs'

class ImageFile(BytesIO):
    count = 0

    def getFile(self, pix, ext='.png', db=0):
        if isinstance(pix, str):
            e = path.splitext(pix)[-1]

            if e in ['.png', '.xbm', '.gif', '.jpg', '.jpeg']: self.ext = e[1:]
            else: self.ext = ext

            if db:
                if self.ext == 'png': pic = Pngs.get(pix)
                elif self.ext == 'gif': pic = Gifs.get(pix)
            else: pic = pix
            self.name = pix
            self.basename = path.basename(pic)
            return pic

    def __init__(self, fp=None, ext='.png', db=0, image=None):
        self.name = None
        self.basename = None
        self.ext = ext
        self._data = b''

        if isinstance(fp, str):
            file = self.getFile(fp, ext=ext, db=db)
            self._data = open(file, 'rb').read()
        elif isinstance(fp, bytes): self._data = fp

        super().__init__(self._data)

        if image: image.save(self, 'png')

        ImageFile.count += 1

    def __str__(self):
        if self.name:return f'ImageFile({self.name})'
        else: return f'ImageFile({ImageFile.count})'

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

        if imageFile:
            if isinstance(imageFile, (str, bytes)): self.imageFile = ImageFile(imageFile, ext=ext, db=db)
            elif image: self.imageFile = ImageFile(image=image)
            
            self.name = self.imageFile.name
            self.ext = self.imageFile.ext
            
            if self.ext in ['xbm', '.xbm']: self.imgClass = BitmapImage

            img = self.image = Image.open(self.imageFile)

            if resize and len(resize) == 2:
                self.resizedImage = self.image.resize(resize)
                img = self.resizedImage
            
            if thumb and len(thumb) == 2: img.thumbnail(thumb)
            
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






