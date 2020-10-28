
from os import path, walk
from io import BytesIO


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
            except: files[0]
        elif isinstance(bitmap, str):
            files = cls.filesDict()
            try: return files[bitmap]
            except: filesL[0]

class Xbms(Pics):
    subDir = 'xbms'
    
class Pngs(Pics):
    subDir = 'pngs'

class ImageFile(BytesIO):
    
    def __init__(self, fileName):
        super().__init__(open(fileName, 'rb').read())
        self.name = path.basename(fileName)
        self.ext = path.splitext(self.name)[1]
    
    def __str__(self): return f'ImageFile({self.name})'
    