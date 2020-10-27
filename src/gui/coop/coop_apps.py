from ..core.agam_apps import *

class CoopRegionDetails(RegionDetails):
    
    def __init__(self, region=None, title='Coop Region Details', geo=(800, 600), **kwargs):
        super().__init__(title=title, geo=geo,**kwargs)
    
    def setupApp(self):
        super().setupApp()
        
        
        account = LF(self, text='Account')
        account.place(x=10, y=220, h=370, w=780)
        
        
        self.childWidgets += [account]
        # self.resultsWidgets += []