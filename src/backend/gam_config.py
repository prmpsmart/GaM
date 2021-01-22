# from .gam.gam import GaM
import pickle, os, io, zlib, threading

class GaM_Settings:
    GaM = None
    ThemeIndex = 38
    cwd = os.getcwd()
    dataPath = os.path.join(cwd, 'data.prmp')
    otherDataPath = os.path.join(cwd, 'specialData.prmp')
    
    @classmethod
    def compress(cls, data, destFile):
        # temp = io.ByetsIO()
        compData = zlib.compress(data)
        file = open(destFile, 'wb')
        file.write(compData)
        file.close()
    
    @classmethod
    def decompress(cls, file):
        # temp = io.ByetsIO()
        compData = open(file, 'rb').read()
        data = zlib.decompress(data)
        return data

    @classmethod
    def loadDatas(cls):
        gamBytes = cls.decompress(cls.dataPath)
        gam = pickle.loads(gamBytes)
        GaM_Settings.GaM = gam

    @classmethod
    def saveDatas(cls):
        gam = GaM_Settings.GaM
        gamBytes = pickle.dumps(gam)
        cls.compress(gamBytes, cls.dataPath)

    @classmethod
    def loadOtherDatas(cls):
        # saveDir
        # auths
        pass
    @classmethod
    def saveOtherDatas(cls):
        pass

    @classmethod
    def usingThread(cls, func, *args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()





