from .gam_extensions import *
from ...backend.gam.gam import GaM_Settings, GaM, Region
from ...backend.office.office_regions import Office



class GaM_Dialog(PRMP_Dialog):
    # def __init__(self, master=None, delay=0, **kwargs): super().__init__(master, delay=delay, **kwargs)

    def defaults(self):
        self._save = GaM_Settings.threadSave
        self._load = GaM_Settings.threadLoad

    def save(self):
        # from .auths_gui import make_change
        # make_change(self._save, silent=1)
        
        self._save()
        PRMP_MsgBox(title='Successful', message='Saving is successful.', )


class PersonDialog(GaM_Dialog):

    def __init__(self, master=None, title='Person Dialog', person=None, manager=None, geo=(550, 390), values={}, **kwargs):

        self.manager = manager
        self.person = person
        
        if person: title = f'{person.master.className} {title}'
        values = person or values
        

        super().__init__(master=master, title=title, geo=geo, values=values, **kwargs)

    def _setupDialog(self):
        
        # name = self.values.get('name')
        # if name: self.setTitle(name)

        self.addEditButton()
        
        self.contact = self.addWidget(PRMP_Style_LabelFrame, config=dict(config=dict(text='Contact Details')), place=dict(x=2, y=2, h=250, relw=.55))
        
        self.name = LabelEntry(self.contact,  topKwargs=dict(config=dict(text='Name')), bottomKwargs=dict(very=True), orient='h', place=dict(relx=.02, rely=0, relh=.15, relw=.96), longent=.25)
        
        self.phone = LabelEntry(self.contact,  topKwargs=dict(config=dict(text='Phone Number')), bottomKwargs=dict(_type='number'), place=dict(relx=.02, rely=.14, relh=.15, relw=.96), longent=.5, orient='h')
        
        self.email = LabelEntry(self.contact,  topKwargs=dict(config=dict(text='Email')), bottomKwargs=dict(_type='email'), place=dict(relx=.02, rely=.28, relh=.15, relw=.96), longent=.25, orient='h')
        
        self.gender = LabelCombo(self.contact,  topKwargs=dict(config=dict(text='Gender')), bottomKwargs=dict(type_='gender'), place=dict(relx=.02, rely=.42, relh=.15, relw=.96), longent=.25, orient='h')
        
        self.address = LabelText(self.contact,  topKwargs=dict(config=dict(text='Address')), place=dict(relx=.02, rely=.56, relh=.44, relw=.96), bottomKwargs=dict(very=True), longent=.3, orient='h')
        
        self.image = PRMP_ImageLabel(self.container, place=dict(relx=.58, y=10, h=190, relw=.41))

        self.date = LabelDateButton(self.container, topKwargs=dict(config=dict(text='Reg Date')), place=dict(relx=.58, y=205, h=40, relw=.41), orient='h')

        self.addResultsWidgets(['name', 'phone', 'email', 'image', 'address', 'gender', 'date'])

    def action(self):
        if self.result:
            if self.person: PRMP_MsgBox(self, title='Edit Person Details', message='Are you sure to edit the details of this person?', _type='question', callback=self.updatePerson)
            
            elif self.manager: PRMP_MsgBox(self, title='Person Creation', message='Are you sure to create a new person?', _type='question', callback=self.newPerson)
            else: PRMP_MsgBox(self, title='Person Dialog Error', message='No Person or Manager is given.', _type='error', ask=0)

    def updatePerson(self, w):
        if w:
            self.person.update(self.result)
            self._setResult(self.person)
        self.destroyDialog()

    def newPerson(self, w):
        if w:
            person = self.manager.createPerson(**self.result)
            self._setResult(person)
        self.destroyDialog()
PerD = PersonDialog

class RecordDialog(GaM_Dialog):
    
    def __init__(self, master=None, title='Record Dialog', geo=(350, 350), manager=None, record=None, values={}, **kwargs):
        
        self.manager = manager
        self.record = record
        if record: title = f'{record.className} Record'

        super().__init__(master=master, title=title, geo=geo, values=record or values, **kwargs)
    
    def _setupDialog(self):
        self.addEditButton()

        bothcont = Frame(self.container, place=dict(relx=.005, rely=.005, relh=.85, relw=.989))
        self.cont = Frame(bothcont, place=dict(relx=0, rely=0, relh=1, relw=1), relief='groove')

        self.money = LabelEntry(self.cont, place=dict(relx=.02, rely=.01, relh=.15, relw=.96), longent=.35, topKwargs=dict(config=dict(text='Money')), orient='h', bottomKwargs=dict(_type='money'))
        self.date = LabelDateButton(self.cont, topKwargs=dict(config=dict(text='Date')), place=dict(relx=.02, rely=.16, relh=.15, relw=.96), longent=.35, orient='h')
        self.note = LabelText(self.cont, topKwargs=dict(config=dict(text='Note')), place=dict(relx=.02, rely=.32, relh=.5, relw=.96), longent=.35, orient='h')
        self.chee = Checkbutton(self.cont, place=dict(relx=.63, rely=.84, relh=.14, relw=.34), text='Co Records', command=self.openCoRecords)

        self.coRecords = SubsList(bothcont, text='Co Records', highlightable=0)

        self.addResultsWidgets(['note', 'money', 'date'])
    
    def openCoRecords(self):
        self.changeGeo()

    def changeGeo(self):
        if self.chee.get():
            geo, relw = (600, 350), .5
            self.coRecords.set(self.record.linkedRecords, showAttr='name')
            self.coRecords.place(relx=relw, rely=0, relh=1, relw=relw)
        else:
            geo, relw = (350, 350), 1
            self.coRecords.place_forget()
        self.changeGeometry(geo=geo)
        self.cont.place(relx=0, rely=0, relh=1, relw=relw)

    def action(self):
        if self.result: 
            if self.record: PRMP_MsgBox(self, title='Edit Record Details', message='Are you sure to edit the details of this record?', _type='question', callback=self.updateRecord)
        
            elif self.manager: PRMP_MsgBox(self, title='Record Creation', message='Are you sure to create a new record?', _type='question', callback=self.newRecord)
            else: PRMP_MsgBox(self, title='Record Dialog Error', message='No Record or Manager is given.', _type='error', ask=0)

        if self._return: self.destroy()

    def updateRecord(self, w):
        if w: self.record.update(self.result)
        self.destroyDialog()

    def newRecord(self, w):
        if w:
            record = self.manager.createRecord(**self.result)
            self._setResult(record)
        self.destroyDialog()
RecD = RecordDialog

class AccountDialog(GaM_Dialog):

    def __init__(self, master=None, title='Account Dialog', account=None, manager=None, geo=(300, 300), values={}, **kwargs):

        self.manager = manager
        self.account = account
        if account: title = f'{account.master.className} {title}'
        
        super().__init__(master=master, title=title, geo=geo, values=account if account else values, **kwargs)
    
    def _setupDialog(self):
        name = self.values.get('name')
        if name: self.setTitle(name)
        
        self.addEditButton()
        
        self.month = LabelMonthYearButton(self.container, topKwargs=dict(config=dict(text='Month')), place=dict(relx=.005, y=10, h=40, relw=.8), orient='h', longent=.4)

        self.addResultsWidgets('month')
    
    def action(self):
        if self.result:

            if self.account: PRMP_MsgBox(self, title='Edit Account Details', message='Are you sure to edit the details of this account?', _type='question', callback=self.updateAccount)
        
            elif self.manager: PRMP_MsgBox(self, title='Account Creation', message='Are you sure to create a new account?', _type='question', callback=self.newAccount)
            else: PRMP_MsgBox(self, title='Account Dialog Error', message='No Account or Manager is given.', _type='error', ask=0)
    @property
    def result(self):
        res = super().result
        if 'month' in res:
            res['date'] = res['month']
            del res['month']
        return res
        
    def updateAccount(self, w):
        if w: self.account.update(self.result)
        self.destroyDialog()

    def newAccount(self, w):
        if w:
            try:
                account = self.manager.createAccount(**self.result)
                self._setResult(account)
            except Exception as error:
                # print(error)
                font = self.DEFAULT_FONT.copy()
                font['size'] = 15
                PRMP_MsgBox(self, title='Account Creation Error', message=error, _type='error', ask=0, msgFont=font)
        self.destroyDialog()
AccD = AccountDialog

class OfficeDialog(GaM_Dialog):
    
    def __init__(self, master=None, title='Office Dialog', office=None, manager=None, geo=(300, 300), values={}, first=False, **kwargs):

        self.first = first
        self.manager = manager
        self.office = office
        if office: title = f'{office.master.className} {title}'
        
        super().__init__(master=master, title=title, geo=geo, values=office if office else values, **kwargs)
    
    def _setupDialog(self):
        name = self.values.get('name')
        if name: self.setTitle(name)
        
        self.addEditButton()
        
        self.name = LabelEntry(self.container, topKwargs=dict(config=dict(text='Name')), place=dict(relx=.005, y=10, h=40, relw=.8), orient='h', longent=.4, bottomKwargs=dict(very=1))
        self.location = LabelEntry(self.container, topKwargs=dict(config=dict(text='Location')), place=dict(relx=.005, y=60, h=40, relw=.8), orient='h', longent=.4, bottomKwargs=dict(very=1))
        self.date = LabelDateButton(self.container, topKwargs=dict(config=dict(text='Date')), place=dict(relx=.005, y=130, h=40, relw=.8), orient='h', longent=.4, bottomKwargs=dict(very=1))

        self.addResultsWidgets(['date', 'location', 'name'])
    
    def action(self):
        if self.result:

            if self.office: PRMP_MsgBox(self, title='Edit Office Details', message='Are you sure to edit the details of this office?', _type='question', callback=self.updateOffice)
        
            elif self.manager: PRMP_MsgBox(self, title='Office Creation', message='Are you sure to create a new office?', _type='question', callback=self.newOffice)
            else:
                if self.first: self.destroyDialog()
                else: PRMP_MsgBox(self, title='Office Dialog Error', message='No Office or Manager is given.', _type='error', ask=0)
        
    def updateOffice(self, w):
        if w: self.office.update(self.result)
        self.destroyDialog()

    def newOffice(self, w):
        if w:
            try:
                office = self.manager.createOffice(**self.result)
                self._setResult(office)
            except Exception as error:
                # print(error)
                font = self.DEFAULT_FONT.copy()
                font['size'] = 15
                PRMP_MsgBox(self, title='Office Creation Error', message=error, _type='error', ask=0, msgFont=font)
        self.destroyDialog()



class StartDialog(GaM_Dialog):
    TOPS = ['GaM', 'Office', 'DC_Office', 'COOP_Office']
    TOP = Region
    MANAGER = 'Manager'
    
    def __init__(self, master=None, title='Start Dialog', geo=(500, 400), **kwargs):
        
        self.Top = None
        self.Manager = None
        self.font = PRMP_Theme.PRMP_FONT.copy()
        self.font['size'] = 15
        self.topName = self.TOP.__name__

        if GaM_Settings.GaM:
            self.Top = GaM_Settings.GaM
            self.Manager = self.Top.person
        
        super().__init__(master, title=title, geo=geo, **kwargs)

    def _setupDialog(self):

        self.addSubmitButton()
        self.submitBtn.config(command=self.action)
        self._placeSubmitButton()

        self.welcome = PRMP_Label(self.container, text=f'Welcome to GaM Software, create the {self.MANAGER} details !!!', place=dict(relx=.02, rely=.02, relw=.96, relh=.1), asEntry=1, font=self.font)

        self.create = PRMP_Button(self.container, text=f'Create {self.topName}', place=dict(relx=.1, rely=.26, relw=.3, relh=.1), command=self.createTOP)

        self.manager = PRMP_Button(self.container, text=f'{self.MANAGER} Details', place=dict(relx=.6, rely=.26, relw=.3, relh=.1), command=self.openManagerDetail)

        self.uniqueID = LabelEntry(self.container, topKwargs=dict(text='Unique ID'), place=dict(relx=.1, rely=.6, relw=.8, relh=.25), bottomKwargs=dict(state='readonly'))
    
    def defaults(self): self.uniqueID.set(self.Top.uniqueID if self.Top else '')



    def createTOP(self):
        if self.Top: PRMP_MsgBox(self, message=f'A {self.topName} object already existed.', title='{self.topName} Error', ask=0, _type='error')
        else: PRMP_MsgBox(self, message=f'Are you sure to create a {self.topName} object?', title=f'{self.topName} creation confirmation', callback=self._createTOP, _type='question')

    def startDefaults(self): GaM_Settings.GaM = self.Top

    def _createTOP(self, e=0):
        if not e: return
        self.uniqueID.set(self.Top.uniqueID)
        self.startDefaults()
        self.save()

        PRMP_MsgBox(self, message=f'{self.topName} Object created successfully, update the {self.MANAGER}\'s details using the {self.MANAGER} details button.', title=f'{self.topName} creation successful.', ask=0, _type='info')

    def openManagerDetail(self):
        if not self.Top:
            PRMP_MsgBox(self, message=f'No {self.topName} object created', title=f'{self.topName} Error', ask=0)
            return
        personsManager = self.Top.personsManager
        if len(personsManager): dic = dict(person=personsManager[-1])
        else: dic = dict(manager=personsManager)

        PersonDialog(self, title=f'{self.MANAGER} Details', callback=self.setMANAGER, **dic)
    
    def setMANAGER(self, manager):
        if not self.MANAGER: self.MANAGER = manager

    def action(self):
        if self.callback: self.callback(self.destroy)

class GaM_StartDialog(StartDialog):
    TOP = GaM
    MANAGER = 'CEO'
    def __init__(self, master=None, title='GaM Start Dialog', **kwargs):

        super().__init__(master, title=title, **kwargs)
    
    def _setupDialog(self):
        super()._setupDialog()
        self.date = LabelDateButton(self.container, topKwargs=dict(text='Date'), bottomKwargs=dict(text=self.Top.date.date if self.Top else ''), place=dict(relx=.02, rely=.14, relw=.4, relh=.1), orient='h', longent=.4)
    
    def _createTOP(self, e=0):
        date = self.date.get()
        if not date:
            PRMP_MsgBox(self, title='Date Error', message='Please choose a date.', ask=0, _type='error')
            return
        self.Top = self.TOP(date=date)
        super()._createTOP(e)

class Office_StartDialog(StartDialog):
    TOP = Office
    
    def __init__(self, master=None, title='Office Start Dialog', **kwargs): super().__init__(master, title=title, **kwargs)

    def _setupDialog(self):
        self.font['size'] = 14
        super()._setupDialog()

    def _createTOP(self, e=0):
        if e: OfficeDialog(self, callback=self._createOFFICE, first=1)

    def _createOFFICE(self, result=0):
        if not result: return
        self.Top = self.TOP(result['name'], **result)
        super()._createTOP(1)

class DCOffice_StartDialog(Office_StartDialog):
    TOP = Office
    
    def startDefaults(self, e=0):
        self.Top = self.Top.dcOffice
        super().startDefaults()

















