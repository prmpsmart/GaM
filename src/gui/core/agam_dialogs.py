
from .prmp_tk.two_widgets import *
from .prmp_tk.dialogs import *

class PersonDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Person Dialog', person=None, geo=(550, 320), values={}, **kwargs):
        self.person = person
        
        super().__init__(master=master, title=title, geo=geo, values=values, **kwargs)


    
    def _setupDialog(self):
        name = self.values.get('name')
        if name: self.addTitleBar(name)
        
        self.addEditButton(self.editInput)
        
        contact = self.addWidget(LF, config=dict(text='Contact Details'), place=dict(relx=0, rely=0, h=200, relw=.55))
        
        self.name = LE(contact,  topKwargs={'text': 'Name'}, orient='h', relx=.02, rely=0, relh=.15, relw=.96, longent=.25)
        
        self.phone = LE(contact,  topKwargs={'text': 'Phone Number'}, relx=.02, rely=.14, relh=.15, relw=.96, longent=.5, orient='h')
        
        self.email = LE(contact,  topKwargs={'text': 'Email'}, relx=.02, rely=.28, relh=.15, relw=.96, longent=.25, orient='h')
        
        self.gender = LC(contact,  topKwargs={'text': 'Gender'}, bottomKwargs={'values': ['Male', 'Female']}, relx=.02, rely=.42, relh=.15, relw=.96, longent=.25, orient='h')
        
        self.address = LT(contact,  topKwargs={'text': 'Address'}, relx=.02, rely=.56, relh=.44, relw=.96, longent=.3, orient='h')
        
        self.image = IL(self.container)
        self.image.place(relx=.58, y=10, h=190, relw=.41)

        self.addResultsWidgets(['name', 'phone', 'email', 'image', 'address', 'gender'])
        
PD = PersonDialog

class RecordDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Record Dialog', region=None, geo=(500, 280), **kwargs):
        
        if region: title = f'{region.className} {title}'
        
        super().__init__(master=master, title=title, geo=geo,  **kwargs)
        self.region = region
    
    def _setupDialog(self):
        self.addTitleBar(self.titleText)

 









