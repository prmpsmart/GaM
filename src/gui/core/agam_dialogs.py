
from .prmp_tk.two_widgets import *
from .prmp_tk.dialogs import *

class PersonDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Person Dialog', person=None, geo=(500, 320), **kwargs):
        super().__init__(master=master, title=title, geo=geo,  **kwargs)
        self.person = person
    
    def _setupDialog(self):
        self.addTitleBar(self.titleText)
        # self.addStatusBar()
        self.addSubmitButton(self.processInput)
        self.addEditButton(self.editInput)
        
        contact = LF(self, text='Contact Details')
        contact.place(x=10, y=30, h=240, w=250)
        
        self.name = LE(contact,  topKwargs={'text': 'Name'}, orient='h', relx=.02, rely=0, relh=.12, relw=.96, longent=.25)
        
        self.phone = LE(contact,  topKwargs={'text': 'Phone Number'}, relx=.02, rely=.14, relh=.12, relw=.96, longent=.5, orient='h')
        
        self.email = LE(contact,  topKwargs={'text': 'Email'}, relx=.02, rely=.28, relh=.12, relw=.96, longent=.25, orient='h')
        
        self.gender = LC(contact,  topKwargs={'text': 'Gender'}, bottomKwargs={'values': ['Male', 'Female']}, relx=.02, rely=.42, relh=.12, relw=.96, longent=.25, orient='h')
        
        self.address = LT(contact,  topKwargs={'text': 'Address'}, relx=.02, rely=.56, relh=.44, relw=.96, longent=.3, orient='h')
        
        self.image = IL(self)
        self.image.place(x=270, y=40, h=190, w=220)
        contact.addChildWidgets([self.name, self.phone, self.email, self.address, self.gender])
        self.addChildWidgets([contact, self.image])
        self.addResultsWidgets(['name', 'phone', 'email', 'image', 'address', 'gender'])
PD = PersonDialog

class RecordDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Record Dialog', region=None, geo=(500, 280), **kwargs):
        
        if region: title = f'{region.className} {title}'
        
        super().__init__(master=master, title=title, geo=geo,  **kwargs)
        self.region = region
    
    def _setupDialog(self):
        self.addTitleBar(self.titleText)

 









