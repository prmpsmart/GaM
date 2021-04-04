import io, base64, zlib, pickle
from .prmp_mixins import PRMP_Mixins, os



class PRMP_File(io.BytesIO, PRMP_Mixins):
    count = 0

    def __init__(self, filename='', b64=b'', data=b''):

        passed = [bool(a) for a in [filename, b64, data]]
        
        assert passed.count(True) <= 2, 'Only one is required in [filename, b64, data]'

        self.name = filename
        self._data = data

        if data: self.name = self.name or 'data_%d'%PRMP_File.count

        elif filename and not (b64 or data):
            self.name = os.path.basename(filename)
            if os.path.isfile(filename):
                try: self._data = open(filename, 'rb').read()
                except: pass

        elif b64:
            self._data = base64.b64decode(b64)
            self.name = self.name or 'base64_%d'%PRMP_File.count
        
        self.basename = os.path.basename(self.name)
        self.name_n_ext = self.basename.split('.')[0]
        
        super().__init__(self._data)

        PRMP_File.count += 1

    def __repr__(self):
        if self.name: return f'<%s(%s)>'%(self.className, self.name)
        else: return '<%s(%d)>'%(self.className, PRMP_File.count)
    
    def __str__(self):
        if self.name: return self.name
        else: return '<%s(%d)>'%(self.className, PRMP_File.count)

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
    def size(self): return len(self.data)

    def get(self): return self.data

    @property
    def compressedData(self): return zlib.compress(self.data)
    
    @property
    def decompressedData(self): return zlib.decompress(self.data)

    @property
    def cdata(self): return self.compressedData

    @property
    def base64Data(self): return base64.b64encode(self.data)

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


