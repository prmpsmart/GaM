from ..core.details import Detail, DetailsManager

class ClientDetail(Detail):
    
    @property
    def client(self): return self.manager

class DCCO(Detail):
    'Daily Contribution Cash Officer.'

class DCCOsManager(DetailsManager):
    regionClass = DCCO
    
    
    def createDCCo(self, **kwargs): return self.createDetail(**kwargs)