
from .prmp_tk.two_widgets import *
from .prmp_tk.dialogs import *

class PersonDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Person Dialog', person=None, geo=(550, 320), values={}, **kwargs):
        self.person = person
        
        super().__init__(master=master, title=title, geo=geo, values=values, **kwargs)


    
    def _setupDialog(self):
        name = self.values.get('name')
        if name: self.addTitleBar(name)
        
        self.addEditButton()
        
        contact = self.addWidget(LF, config=dict(text='Contact Details'), place=dict(relx=0, rely=0, h=200, relw=.55))
        
        self.name = LE(contact,  topKwargs=dict(text='Name'), bottomKwargs=dict(placeholder='Love'), orient='h', relx=.02, rely=0, relh=.15, relw=.96, longent=.25)
        
        self.phone = LE(contact,  topKwargs=dict(text='Phone Number'), relx=.02, rely=.14, relh=.15, relw=.96, longent=.5, orient='h')
        
        self.email = LE(contact,  topKwargs=dict(text='Email'), bottomKwargs=dict(type_='email'), relx=.02, rely=.28, relh=.15, relw=.96, longent=.25, orient='h')
        
        self.gender = LC(contact,  topKwargs=dict(text='Gender'), bottomKwargs=dict(type_='gender'), relx=.02, rely=.42, relh=.15, relw=.96, longent=.25, orient='h')
        
        self.address = LT(contact,  topKwargs=dict(text='Address'), relx=.02, rely=.56, relh=.44, relw=.96, longent=.3, orient='h')
        
        self.image = IL(self.container)
        self.image.place(relx=.58, y=10, h=190, relw=.41)

        self.addResultsWidgets(['name', 'phone', 'email', 'image', 'address', 'gender'])
        
PD = PersonDialog

class RecordDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Record Dialog', region=None, geo=(300, 300), **kwargs):
        
        if region: title = f'{region.className} {title}'
        self.region = region

        super().__init__(master=master, title=title, geo=geo, tw=1,  **kwargs)
    
    def _setupDialog(self):
        self.addEditButton()
        
        self.money = LE(self.container, relx=.02, rely=.01, relh=.15, relw=.96, longent=.35, topKwargs=dict(text='Money'), orient='h')
        self.date = LDB(self.container, topKwargs=dict(text='Date'), relx=.02, rely=.16, relh=.15, relw=.96, longent=.35, orient='h')
        self.note = LT(self.container, topKwargs=dict(text='Note'), relx=.02, rely=.32, relh=.5, relw=.96, longent=.35, orient='h')
        
 









