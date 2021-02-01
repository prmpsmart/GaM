from ..core.bases import ObjectSort

class DCSort(ObjectSort):

    def __init__(self, dcRegion):
        super().__init__(dcRegion)
        self.dcRegion = self.object
    
    def sortRegionsByYear(self): pass




