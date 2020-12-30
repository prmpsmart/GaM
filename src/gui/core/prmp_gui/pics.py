
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

    def __init__(self, picName=None, ext='png', resize=(), thumb=(), image=None, db=0):
        
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
                    if self.ext == 'png': pic = Pngs.get(picName);print(pic, picName)
                    elif self.ext == 'gif': pic = Gifs.get(picName)
                else: pic = picName
                
            elif isinstance(picName, ImageFile):
                pic = self.imageFile = picName
                self.name = picName.name
                self.ext = picName.ext
                
            if self.ext == 'xbm': self.imgClass = BitmapImage

            # if self.imageFile: self.imageFile = ImageFile(pic)

            img = self.image = Image.open(pic)

            if resize and len(resize) == 2:
                self.resizedImage = self.image.resize(resize)
                img = self.resizedImage
            
            if thumb and len(thumb) == 2: img.thumbnail(thumb)
            self.tkImage = self.imgClass(img, name=self.basename)

        elif image:
            self.image = image
            self.tkImage = self.imgClass(image=image)

    def __str__(self):
        try: return str(self.tkImage)
        except:
            try: return str(self.image)
            except: raise ValueError

    @property
    def basename(self):
        base = path.basename(self.name)
        extsplit = path.splitext(base)[0]
        return extsplit

    def resize(self, rz): return self.image.resize(rz)

    def resizeTk(self, rz): return self.imgClass(self.resize(rz))

    def thumbnail(self, rz): self.image.thumbnail(rz)
    
    def thumbnailTk(self, rz): 
        self.thumbnail(rz)
        return self.imgClass(self.image)






