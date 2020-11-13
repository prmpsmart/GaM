
from .prmp_gui.two_widgets import *
from .prmp_gui.dialogs import *

class PersonDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Person Dialog', person=None, geo=(550, 320), values={}, **kwargs):
        self.person = person
        
        super().__init__(master=master, title=title, geo=geo, values=values, **kwargs)
    
    def _setupDialog(self):
        name = self.values.get('name')
        if name: self.addTitleBar(name)
        
        self.addEditButton()
        
        contact = self.addWidget(PRMP_LabelFrame, config=dict(text='Contact Details'), place=dict(x=2, y=2, h=200, relw=.55))
        
        self.name = LabelEntry(contact,  topKwargs=dict(config=dict(text='Name')), bottomKwargs=dict(placeholder='Love'), orient='h', relx=.02, rely=0, relh=.15, relw=.96, longent=.25)
        
        self.phone = LabelEntry(contact,  topKwargs=dict(config=dict(text='Phone Number')), relx=.02, rely=.14, relh=.15, relw=.96, longent=.5, orient='h')
        
        self.email = LabelEntry(contact,  topKwargs=dict(config=dict(text='Email')), bottomKwargs=dict(type_='email'), relx=.02, rely=.28, relh=.15, relw=.96, longent=.25, orient='h')
        
        self.gender = LabelCombo(contact,  topKwargs=dict(config=dict(text='Gender')), bottomKwargs=dict(type_='gender'), relx=.02, rely=.42, relh=.15, relw=.96, longent=.25, orient='h')
        
        self.address = LabelText(contact,  topKwargs=dict(config=dict(text='Address')), relx=.02, rely=.56, relh=.44, relw=.96, longent=.3, orient='h')
        
        self.image = ImageLabel(self.container)
        self.image.place(relx=.58, y=10, h=190, relw=.41)

        self.addResultsWidgets(['name', 'phone', 'email', 'image', 'address', 'gender'])
PerD = PersonDialog

class RecordDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Record Dialog', region=None, geo=(300, 300), record=None, **kwargs):
        
        if region: title = f'{region.className} {title}'
        self.record = record
        self.region = region

        super().__init__(master=master, _ttk_=0, title=title, geo=geo,  **kwargs)
    
    def _setupDialog(self):
        self.addEditButton()

        self.money = LabelEntry(self.container, relx=.02, rely=.01, relh=.15, relw=.96, longent=.35, topKwargs=dict(config=dict(text='Money')), orient='h')
        def setMoney(money): self.money.B.clear(); self.money.B.insert(0, self.addSignToMoney(money))
        self.money.set = setMoney
        self.money.set('')
        self.date = LabelDateButton(self.container, topKwargs=dict(config=dict(text='Date')), relx=.02, rely=.16, relh=.15, relw=.96, longent=.35, orient='h')
        self.note = LabelText(self.container, topKwargs=dict(config=dict(text='Note')), relx=.02, rely=.32, relh=.5, relw=.96, longent=.35, orient='h')
        self.addResultsWidgets(['note', 'money', 'date'])

RecD = RecordDialog
 









