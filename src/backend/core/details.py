from .regions import Errors, Region, Mixins, RegionsManager
from PIL.ImageTk import PhotoImage, Image
from tkinter import Label, Tk, LabelFrame


class Detail(Mixins):
    Manager = 'DetailsManager'
    
    __male = 'male', 'm'
    __female = 'female', 'f'
    
    def __init__(self, manager=None, gender='n', phone='', photo='', email='', address='', date=None, name=None, **kwargs):
        
        if isinstance(manager, str): pass
        elif isinstance(manager, Region): self.__date = manager.date
        else: assert manager.className == self.Manager, f'Manager should be {self.Manager} not {manager.className}'
        gender = gender.lower()
        
        if gender in self.__male:  self.__gender = self.__male[0].title()
        elif gender in self.__female:  self.__gender = self.__female[0].title()
        
        else: self.__gender = 'Neutral'
        
        self.__name = name
        self.__phone = phone
        self.__photo = photo
        self.__email = email
        self.__address = address
        self.__manager = manager
    
    def __str__(self): return f'{self.manager} | {self.className}'
    
    @property
    def name(self): 
        if not self.__name: return self.manager.name
        return self.__name
    @property
    def manager(self): return self.__manager
    @property
    def gender(self): return self.__gender
    @property
    def address(self): return self.__address
    @address.setter
    def address(self, addr):
        assert addr, 'Address must be str and not empty.'
        self.__address = addr
    @property
    def image(self):
        pass
    @property
    def email(self): return self.__email
    @email.setter
    def email(self, em): 
        # confirm if email is valid
        self.__email = em
    @property
    def phone(self): return self.__phone
    @phone.setter
    def phone(self, number):
        assert number, 'Number must be valid.'
        # confirm if number is valid
        self.__phone = number
    
    def show(self):
        pass

class DetailsManager(RegionsManager):
    regionClass = Detail
    
    def createDetail(self, **kwargs): return self.createRegion(**kwargs)







