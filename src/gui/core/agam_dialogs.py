
from .prmp_tk.two_widgets import *
from .prmp_tk.dialogs import *

class PersonDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Person Dialog', person=None, geo=(550, 320), **kwargs):
        super().__init__(master=master, title=title, geo=geo,  **kwargs)
        self.person = person
    
    def _setupDialog(self):
        self.addTitleBar(self.titleText)
        # self.addStatusBar()
        self.addSubmitButton(self.processInput)
        self.addEditButton(self.editInput)
        
        contact = LF(self, text='Contact Details')
        contact.place(relx=0, y=30, h=240, relw=.6)
        
        self.name = LE(contact,  topKwargs={'text': 'Name'}, orient='h', relx=.02, rely=0, relh=.15, relw=.96, longent=.25)
        
        self.phone = LE(contact,  topKwargs={'text': 'Phone Number'}, relx=.02, rely=.14, relh=.15, relw=.96, longent=.5, orient='h')
        
        self.email = LE(contact,  topKwargs={'text': 'Email'}, relx=.02, rely=.28, relh=.15, relw=.96, longent=.25, orient='h')
        
        self.gender = LC(contact,  topKwargs={'text': 'Gender'}, bottomKwargs={'values': ['Male', 'Female']}, relx=.02, rely=.42, relh=.15, relw=.96, longent=.25, orient='h')
        
        self.address = LT(contact,  topKwargs={'text': 'Address'}, relx=.02, rely=.56, relh=.44, relw=.96, longent=.3, orient='h')
        
        self.image = IL(self)
        self.image.place(relx=.6, y=40, h=190, relw=.4)

        self.addResultsWidgets(['name', 'phone', 'email', 'image', 'address', 'gender'])
        
PD = PersonDialog

class RecordDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Record Dialog', region=None, geo=(500, 280), **kwargs):
        
        if region: title = f'{region.className} {title}'
        
        super().__init__(master=master, title=title, geo=geo,  **kwargs)
        self.region = region
    
    def _setupDialog(self):
        self.addTitleBar(self.titleText)

 









