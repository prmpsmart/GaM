from .agam_extensions import *

class PersonDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Person Dialog', person=None, manager=None, geo=(550, 390), values={}, **kwargs):

        self.manager = manager
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

    def processInput(self):
        result = super().processInput()

        if self.person and PRMP_MsgBox(self, title='Edit Person Details', message='Are you sure to edit the details of this person?', _type='question').result == True: self.person.update(result)
        
        elif self.manager and PRMP_MsgBox(self, title='Person Creation', message='Are you sure to create a new person?', _type='question').result == True:
            person = self.manager.createPerson(**result)
            self._setResult(person)

        if self._return: self.destroy()
PerD = PersonDialog

class RecordDialog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Record Dialog', geo=(350, 350), manager=None,  record=None, values={}, **kwargs):
        
        self.manager = manager
        self.record = record
        if record: title = f'{record.className} Record'

        super().__init__(master=master, title=title, geo=geo, values=record if record else values, **kwargs)
    
    def _setupDialog(self):
        self.addEditButton()

        bothcont = Frame(self.container, place=dict(relx=.005, rely=.005, relh=.85, relw=.989))
        self.cont = Frame(bothcont, place=dict(relx=0, rely=0, relh=1, relw=1), relief='groove')

        self.money = LabelEntry(self.cont, place=dict(relx=.02, rely=.01, relh=.15, relw=.96), longent=.35, topKwargs=dict(config=dict(text='Money')), orient='h', bottomKwargs=dict(_type='money'))
        self.date = LabelDateButton(self.cont, topKwargs=dict(config=dict(text='Date')), place=dict(relx=.02, rely=.16, relh=.15, relw=.96), longent=.35, orient='h')
        self.note = LabelText(self.cont, topKwargs=dict(config=dict(text='Note')), place=dict(relx=.02, rely=.32, relh=.5, relw=.96), longent=.35, orient='h')
        self.chee = Checkbutton(self.cont, place=dict(relx=.63, rely=.84, relh=.14, relw=.34), text='Co Records', command=self.openCoRecords)

        self.coRecords = SubsList(bothcont, text='Co Records', highlightable=0)
        self.coRecords.total.T.config(text='Total')

        self.addResultsWidgets(['note', 'money', 'date'])
    
    def openCoRecords(self):
        self.changeGeo()

    def changeGeo(self):
        if self.chee.get():
            geo, relw = (600, 350), .5
            self.coRecords.set(self.record.linkedRecords)
            self.coRecords.place(relx=relw, rely=0, relh=1, relw=relw)
        else:
            geo, relw = (350, 350), 1
            self.coRecords.place_forget()
        self.changeGeometry(geo=geo)
        self.cont.place(relx=0, rely=0, relh=1, relw=relw)

    def processInput(self):
        result = super().processInput()

        if self.record and PRMP_MsgBox(self, title='Edit Record Details', message='Are you sure to edit the details of this record?', _type='question').result == True: self.record.update(result)
        
        elif self.manager and PRMP_MsgBox(self, title='Record Creation', message='Are you sure to create a new record?', _type='question').result == True:
            record = self.manager.createRecord(**result)
            self._setResult(record)

        if self._return: self.destroy()
RecD = RecordDialog


class AccountDialog(PRMP_Dialog):

    
    def __init__(self, master=None, title='Account Dialog', account=None, manager=None, geo=(300, 300), values={}, **kwargs):

        self.manager = manager
        self.account = account
        if account: title = f'{account.master.className} {title}'
        
        super().__init__(master=master, title=title, geo=geo, values=account if account else values, **kwargs)
    
    def _setupDialog(self):
        name = self.values.get('name')
        if name: self.addTitleBar(name)
        
        # self.addEditButton()
        
        self.date = LabelMonthYearButton(self.container, topKwargs=dict(config=dict(text='Month')), place=dict(relx=.005, y=10, h=40, relw=.8), orient='h', longent=.4)

        # self.addResultsWidgets(['name', 'phone', 'email', 'image', 'address', 'gender', 'regDate'])


AccD = AccountDialog








