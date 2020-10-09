from ..core.details import Detail, DetailsManager

class CEO(Detail):
    pass

class CEOsManager(DetailsManager):
    regionClass = CEO

    def createCEO(self, **kwargs): return self.createDetail(**kwargs)