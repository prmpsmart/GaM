from src.gui.core.gam_apps import GaM_Settings, Splash
from src.gui.core.gam_images import GAM_PNGS


from src.utils.auths import Authorisation

print(Authorisation.login_cmd('prmpsmart', 'princerm'))
GaM_Settings.loadOtherDatas()

def startGaM(func):
    from src.gui.core.gam_apps import openCores
    func()
    # print(GaM_Settings.GaM)
    openCores(obj=GaM_Settings.GaM)

def testGaM(func):
    GaM_Settings.loadDatas()
    if not GaM_Settings.GaM:
        from src.gui.core.gam_apps import DCOffice_StartDialog
        func()
        DCOffice_StartDialog(callback=startGaM)
    else: startGaM(func)

def testLogin(func):
    from src.utils.auths import Authorisation

    if Authorisation.logged_in(): testGaM(func)
    else:
        from src.gui.core.auths_gui import Login
        func()
        Login(geo=(600, 600), tw=1, 
        title='Login', callback=testGaM)

def start(): Splash(imageKwargs=dict(base64=GAM_PNGS['red_gam']), asb=0, callback=testLogin, delay=3000)




