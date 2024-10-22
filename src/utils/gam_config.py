# from .gam.gam import GaM
import pickle, os, io, zlib, threading
from prmp_lib.prmp_gui.core import PRMP_Theme
from ..utils.auths import Authorisation


class GaM_Settings:
    TOP = None
    GaM = None
    ThemeIndex = 21
    SaveDir = ''
    Users = []
    Super_Users = []

    cwd = os.path.dirname(__file__)
    dataPath = os.path.join(cwd, 'GaM_data.db')
    otherDataPath = os.path.join(cwd, 'GUIData.db')

    @classmethod
    def loadAll(cls):
        # try:
        cls.loadDatas()
        cls.loadOtherDatas()
        # except Exception as e: print(e)

    @classmethod
    def saveAll(cls):
        try:
            cls.saveDatas()
            cls.saveOtherDatas()
        except Exception as e: print(e)

    @classmethod
    def compress(cls, data, destFile):
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
        try:
            gamBytes = cls.decompress(cls.dataPath)
            gam = pickle.loads(gamBytes)
            GaM_Settings.GaM = gam
        except Exception as e: print(e)

    @classmethod
    def saveDatas(cls):
        gam = GaM_Settings.GaM
        if not gam:
            print(f'{GaM_Settings.GaM = }')
            return

        gamBytes = pickle.dumps(gam)
        cls.compress(gamBytes, cls.dataPath)

    @classmethod
    def loadOtherDatas(cls):
        try:
            dataBytes = cls.decompress(cls.otherDataPath)
            data = pickle.loads(dataBytes)
            for k, v in data.items(): setattr(GaM_Settings, k, v)
            # saveDir
            # auths
        except Exception as e: print(e)
        cls.setLoads()

    @classmethod
    def setLoads(cls):
        PRMP_Theme.setThemeIndex(cls.ThemeIndex)
        Authorisation.load_users(cls.Users)
        Authorisation.load_super_users(cls.Super_Users)

    @classmethod
    def saveOtherDatas(cls):
        data = dict(SaveDir=GaM_Settings.SaveDir, ThemeIndex=PRMP_Theme.currentThemeIndex(), Users=Authorisation.get_users(), Super_users=Authorisation.get_super_users())
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





