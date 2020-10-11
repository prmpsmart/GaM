from ..core.regions import Person, PersonsManager

class CEO(Person):
    pass

class CEOsManager(PersonsManager):
    regionClass = CEO

    def createCEO(self, **kwargs): return self.createPerson(**kwargs)