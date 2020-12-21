from .agam_extensions import *

class PersonDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Person Dialog', person=None, geo=(550, 390), values={}, **kwargs):

        self.person = person
        if person: title = f'{person.master.className} {title}'
        
        super().__init__(master=master, title=title, geo=geo, values=person if person else values, **kwargs)
    
    def _setupDialog(self):
        name = self.values.get('name')
        if name: self.addTitleBar(name)
        
        self.addEditButton()
        
        self.contact = self.addWidget(PRMP_Style_LabelFrame, config=dict(config=dict(text='Contact Details')), place=dict(x=2, y=2, h=250, relw=.55))
        
        self.name = LabelEntry(self.contact,  topKwargs=dict(config=dict(text='Name')), bottomKwargs=dict(very=True), orient='h', place=dict(relx=.02, rely=0, relh=.15, relw=.96), longent=.25)
        
        self.phone = LabelEntry(self.contact,  topKwargs=dict(config=dict(text='Phone Number')), bottomKwargs=dict(_type='number'), place=dict(relx=.02, rely=.14, relh=.15, relw=.96), longent=.5, orient='h')
        
        self.email = LabelEntry(self.contact,  topKwargs=dict(config=dict(text='Email')), bottomKwargs=dict(_type='email'), place=dict(relx=.02, rely=.28, relh=.15, relw=.96), longent=.25, orient='h')
        
        self.gender = LabelCombo(self.contact,  topKwargs=dict(config=dict(text='Gender')), bottomKwargs=dict(type_='gender'), place=dict(relx=.02, rely=.42, relh=.15, relw=.96), longent=.25, orient='h')
        
        self.address = LabelText(self.contact,  topKwargs=dict(config=dict(text='Address')), place=dict(relx=.02, rely=.56, relh=.44, relw=.96), bottomKwargs=dict(very=True), longent=.3, orient='h')
        
        self.image = ImageLabel(self.container, place=dict(relx=.58, y=10, h=190, relw=.41))

        self.regDate = LabelDateButton(self.container, topKwargs=dict(config=dict(text='Reg Date')), place=dict(relx=.58, y=205, h=40, relw=.41), orient='h')

        self.addResultsWidgets(['name', 'phone', 'email', 'image', 'address', 'gender', 'regDate'])
PerD = PersonDialog

class RecordDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Record Dialog', geo=(300, 300), record=None, values={}, **kwargs):
        
        self.record = record
        if record: title = f'{record.region.className} {title}'

        super().__init__(master=master, title=title, geo=geo, values=record if record else values **kwargs)
    
    def _setupDialog(self):
        self.addEditButton()

        self.money = LabelEntry(self.container, place=dict(relx=.02, rely=.01, relh=.15, relw=.96), longent=.35, topKwargs=dict(config=dict(text='Money')), orient='h', bottomKwargs=dict(_type='money'))
        self.date = LabelDateButton(self.container, topKwargs=dict(config=dict(text='Date')), place=dict(relx=.02, rely=.16, relh=.15, relw=.96), longent=.35, orient='h')
        self.note = LabelText(self.container, topKwargs=dict(config=dict(text='Note')), place=dict(relx=.02, rely=.32, relh=.5, relw=.96), longent=.35, orient='h')
        self.addResultsWidgets(['note', 'money', 'date'])
    
    def processInput(self):
        result = super().processInput()
        print('Before', self.record.values)
        if self.record: self.record.update(result)
        print('After', self.record.values)
        return result

RecD = RecordDialog
 









