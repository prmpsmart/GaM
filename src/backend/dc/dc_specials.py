from ..core.bases import Object, ObjectsManager, PRMP_DateTime

class Daily_Contribution(Object):
    Manager = 'Daily_Contributions'
    
    def __init__(self, manager, **kwargs):
        super().__init__(manager, **kwargs)
    
    @property
    def name(self): return f'{self.manager} | {self.className}({self.date}) '
    
    def __eq__(self, other): return (self.manager is other.manager) and (self.date is other.date)




class Daily_Contributions(ObjectsManager):
    ObjectType = Daily_Contribution
    MultipleSubsPerMonth = True

    def __init__(self, area):
        super().__init__(area)
    
    @property
    def name(self): return f'{self.master} {self.className} '

    def createSub(self, date=None, **kwargs):
        
        if date == None: date = PRMP_DateTime.now()
        PRMP_DateTime.checkDateTime(date)
        
        prevs = self.getSub({'date': date})

        print(prevs, date)
        if prevs: raise ValueError(f'Daily_Contribution({date}) already exists.')

        super().createSub(date=date, **kwargs)
