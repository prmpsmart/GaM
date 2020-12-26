from .regions import *

class RegionsManager(ObjectsManager):
    ObjectType = Region
    subTypes = ['Regions']
    MultipleSubsPerMonth = True
    subsName = 'Regions'
    
    def __init__(self, master):
        ObjectsManager.__init__(self, master)
        self.__master = master
        self.addRegion = self.addSub
        
    def __len__(self): return len(self.regions)
    def __repr__(self): return f'<{self}>'
    def __str__(self): return f'{self.master} | {self.name}'
    
    @property
    def name(self): return f'{self.className}({self.master.name})'


    @property
    def firstRegion(self): return self.first
    @property
    def lastRegion(self): return self.last
    
    @property
    def region(self): return self.master
    
    @property
    def date(self): return self.master.date
    
    @property
    def regions(self): return self.subs
    
    def getRegion(self, number=None, name=None, phone=None, email=None, image=None):
        ## provide mechanism to scan pictures.
        self.getSub(dict(number=number, name=name, phone=phone, email=email, image=image))
            
    @classmethod
    def getFromAllRegions(cls, number):
        for region in cls.allRegions():
            if region.number == number: return region
    
    def regionExists(self, **kwargs):
        if self.getRegion(**kwargs): return True
        return False
    
    def createRegion(self, **kwargs): return self.createSub(sup=self.master, **kwargs)
    

 ########## Sorting
  
  # Regions Accounts
   #Date Sorting
    def sortRegionsAccountsByDate(self):
        pass

   #Day Sorting
    def sortRegionsAccountsByDay(self):
        pass
    def sortRegionsAccountsIntoDaysInWeek(self):
        pass
    def sortRegionsAccountsIntoDaysInMonth(self):
        pass
    
   #Week Sorting
    def sortRegionsAccountsByWeek(self):
        pass
    def sortRegionsAccountsIntoWeeksInMonth(self):
        pass
    def sortRegionsAccountsIntoWeeksInYear(self):
        pass
    
   #Month Sorting
    def sortRegionsAccountsByMonth(self, month):
        DateTime.checkDateTime(month)
        clients = [client for client in self.clients if client.lastAccount.date.isSameMonth(month)]
        accounts = []
        for client in clients:
            clientAccounts = client.accountsManager.sortAccountsByMonth(month)
            accounts.extend(clientAccounts)
        return accounts
        
    def sortRegionsAccountsIntoMonthsInYear(self):
        pass
    def sortRegionsAccountsIntoMonthsInYears(self):
        pass
    
   #Year Sorting
    def sortRegionsAccountsByYear(self):
        pass
    def sortRegionsAccountsIntoYears(self):
        pass


class PersonsManager(ObjectsManager):
    ObjectType = Person
    subTypes = ['Persons']

    @property
    def lastPerson(self): return self.last
    def createPerson(self, **kwargs): return self.createSub(**kwargs)







