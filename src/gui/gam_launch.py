from src.gui.gam.gam_apps import GaM_Settings, Splash
from src.gui.gam.gam_images import GaM_PNGS


from src.utils.auths import Authorisation

GaM_Settings.loadOtherDatas()
# Authorisation.login_cmd('prmpsmart', 'princerm')

def startGaM(func):
    from src.gui.gam.gam_apps import openCores
    func()
    # print(GaM_Settings.GaM)
    openCores(obj=GaM_Settings.GaM)

def testGaM(func):
    # GaM_Settings.loadDatas()
    if not GaM_Settings.GaM:
        from src.gui.gam.gam_apps import DCOffice_StartDialog
        func()
        DCOffice_StartDialog(callback=startGaM)
    else: startGaM(func)

def testLogin(func):
    from src.utils.auths import Authorisation

    if Authorisation.logged_in(): testGaM(func)
    else:
        from src.gui.gam.auths_gui import Login
        func()
        Login(geo=(600, 600), tw=1, title='Login', callback=testGaM)

def start(): Splash(imageKwargs=dict(b64=GaM_PNGS['red_gam']), asb=0, callback=testLogin, delay=50000, geo=(1200, 700))


testLogin(int)
# start()

