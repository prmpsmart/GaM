
from os import path, walk
from io import BytesIO
from PIL.ImageTk import Image, PhotoImage, BitmapImage


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
    
    def __init__(self, fileName):
        self.name = fileName
        self.basename = path.basename(fileName)
        self.ext = path.splitext(self.name)[1]
        self.data = open(fileName, 'rb').read()
        super().__init__(self.data)
    
    def __str__(self): return f'ImageFile({self.name})'

class PRMP_Image:

    def __init__(self, picName=None, ext='png', resize=(), thumb=(), image=None):
        
        pic = None
        self.__ext = 'jpg'
        self.imageFile = None
        self.imgClass = PhotoImage

        if isinstance(picName, str):
            self.__resizedImage = None
            self.__image = None
            self.__tkImage = None
            self.__name = picName
            
            e = path.splitext(picName)[-1]
            if e in ['.png', '.xbm', '.gif', '.jpg', '.jpeg']: self.__ext = e[1:]
            else: self.__ext = ext

            if self.ext == 'png': pic = Pngs.get(picName)
            elif self.ext == 'xbm': self.imgClass = BitmapImage
            elif self.ext == 'gif': pic = Gifs.get(picName)
            
            else: pic = picName
            
        elif isinstance(picName, ImageFile):
            self.imageFile = picName
            self.__name = picName.name
            self.__ext = picName.ext
            
        if pic == None: pic = picName
        if self.ext == 'xbm': self.imgClass = BitmapImage

        if image: self.__image = image

        elif not self.imageFile: self.imageFile = ImageFile(pic)

        if self.imageFile:
            img = self.__image = Image.open(pic)

            if resize and len(resize) == 2:
                self.__resizedImage = self.__image.resize(resize)
                img = self.__resizedImage
            
            if thumb and len(thumb) == 2: img.thumbnail(thumb)

            # print(img, 'iio')
            self.__tkImage = self.imgClass(img, name=self.basename)
            # print(self.__tkImage)
    
    def __str__(self):
        try: return str(self.__tkImage)
        except:
            try: return str(self.image)
            except: raise ValueError

    @property
    def name(self): return self.__name

    @property
    def basename(self):
        base = path.basename(self.name)
        extsplit = path.splitext(base)[0]
        return extsplit

    @property
    def ext(self): return self.__ext

    @property
    def image(self): return self.__image
    
    @property
    def tkImage(self): return self.__tkImage
    
    @property
    def resizedImage(self): return self.____resizedImage

    def resize(self, rz): return self.image.resize(rz)

    def resizeTk(self, rz): return self.imgClass(self.resize(rz))

    def thumbnail(self, rz): self.image.thumbnail(rz)
    
    def thumbnailTk(self, rz): 
        self.thumbnail(rz)
        return self.imgClass(self.image)






