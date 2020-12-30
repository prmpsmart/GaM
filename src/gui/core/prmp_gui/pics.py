
from os import path, walk
from io import BytesIO
from PIL.ImageTk import Image, PhotoImage, BitmapImage
import tkinter


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
    def __init__(self, fileName='', data=b''):
        self.name = None
        self.basename = None
        self.ext = None
        self.data = None

        if fileName:
            self.name = fileName
            self.basename = path.basename(fileName)
            self.ext = path.splitext(self.name)[1]
            self.data = open(fileName, 'rb').read()
        elif data:
            self.data = data
        super().__init__(self.data)
        ImageFile.count += 1
    
    def __str__(self):
        if self.name:return f'ImageFile({self.name})'
        else: return f'ImageFile({ImageFile.count})'

class PRMP_Image:
    count = 0
    def __init__(self, picName=None, ext='png', resize=(), thumb=(), db=0):
        
        pic = None
        self.ext = 'jpg'
        self.imageFile = None
        self.imgClass = PhotoImage
        self.resizedImage = None
        self.image = None
        self.tkImage = None
        self.name = picName

        if picName:
            if isinstance(picName, str):
                e = path.splitext(picName)[-1]

                if e in ['.png', '.xbm', '.gif', '.jpg', '.jpeg']: self.ext = e[1:]
                else: self.ext = ext
                if db:
                    if self.ext == 'png': pic = Pngs.get(picName)
                    elif self.ext == 'gif': pic = Gifs.get(picName)
                else: pic = picName
                
            elif isinstance(picName, ImageFile):
                pic = self.imageFile = picName
                self.name = picName.name
                self.ext = picName.ext
            
            elif isinstance(picName, bytes): pic = self.imageFile = ImageFile(data=picName)
                
            if self.ext == 'xbm': self.imgClass = BitmapImage

            if pic:
                if isinstance(picName, bytes): print('pic - data')
                img = self.image = Image.open(pic)

            if resize and len(resize) == 2:
                self.resizedImage = self.image.resize(resize)
                img = self.resizedImage
            
            if thumb and len(thumb) == 2: img.thumbnail(thumb)
            print(img)
            self.tkImage = self.imgClass(img, name=self.basename)
            PRMP_Image.count += 1


    def __str__(self): return str(self.tkImage)

    @property
    def basename(self):
        if self.name:
            base = path.basename(self.name)
            extsplit = path.splitext(base)[0]
            return extsplit
        return f'PRMP_Image({PRMP_Image.count})'

    def resize(self, rz): return self.image.resize(rz)

    def resizeTk(self, rz): return self.imgClass(self.resize(rz))

    def thumbnail(self, rz): self.image.thumbnail(rz)
    
    def thumbnailTk(self, rz): 
        self.thumbnail(rz)
        return self.imgClass(self.image)






