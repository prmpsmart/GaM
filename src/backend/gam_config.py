# from .gam.gam import GaM
import pickle, os, io, zlib, threading
from prmp_gui.core import PRMP_Theme


class GaM_Settings:
    TOP = None

    GaM = None

    ThemeIndex = 38
    cwd = os.getcwd()
    dataPath = os.path.join(cwd, 'data.prmp')
    otherDataPath = os.path.join(cwd, 'specialData.prmp')
    SaveDir = ''

    @classmethod
    def loadAll(cls):
        # try:
        cls.loadDatas()
        cls.loadOtherDatas()
        # except Exception as e: print(e)

        PRMP_Theme.setThemeIndex(cls.ThemeIndex)

    @classmethod
    def saveAll(cls):
        try:
            cls.saveDatas()
            cls.saveOtherDatas()
        except Exception as e: print(e)

    @classmethod
    def compress(cls, data, destFile):
        # temp = io.ByetsIO()
        compData = zlib.compress(data)
        file = open(destFile, 'wb')
        file.write(compData)
        file.close()
    
    @classmethod
    def decompress(cls, file):
        compData = open(file, 'rb').read()
        data = zlib.decompress(compData)
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
        dataBytes = cls.decompress(cls.otherDataPath)
        data = pickle.loads(dataBytes)
        for k, v in data.items(): setattr(GaM_Settings, k, v)
        # saveDir
        # auths
        pass
    @classmethod
    def saveOtherDatas(cls):
        data = dict(SaveDir=GaM_Settings.SaveDir, ThemeIndex=PRMP_Theme.currentThemeIndex())
        dataBytes = pickle.dumps(data)
        cls.compress(dataBytes, cls.otherDataPath)

    @classmethod
    def threadLoad(cls): cls.usingThread(cls.loadAll)
    @classmethod
    def threadSave(cls): cls.usingThread(cls.saveAll)

    @classmethod
    def usingThread(cls, func, *args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()





