from ..core.agam_dialogs import *
from .dc_extensions import *

class ClientDialog(PersonDialog):
    
    def __init__(self, master=None, title='New Client Dialog', manager=None, client=None, geo=(550, 500), **kwargs):
        self.client = client
        self.manager = manager
        if not self.manager:
            if self.client:
                kwargs['values'] = client
                self.manager = self.client.manager
        super().__init__(master=master, title=title, geo=geo, **kwargs)
    
    def _setupDialog(self):
        super()._setupDialog()

        clientDetails = PRMP_LabelFrame(self, config=dict(text='Client Details'))
        clientDetails.place(x=2, y=290, h=100, relw=.35)
        
        self.rate = LabelEntry(clientDetails, topKwargs=dict(config=dict(text='Rate')), bottomKwargs=dict(_type='number'),orient='h', place=dict(relx=.02, rely=0, relh=.45, relw=.8), longent=.45)
        
        self.cardDue = PRMP_Checkbutton(clientDetails, text='Card Due', place=dict(relx=.02, rely=.5, relh=.45, relw=.8))
        # self.addNotEditables('regDate')

        def setCard(val):
            if val: self.cardDue.var.set('1')
            else: self.cardDue.var.set('0')
        
        def getCard():
            val = self.cardDue.var.get()
            if val == '1': return True
            else: return False
        
        # self.cardDue.set = setCard
        # self.cardDue.get = getCard

        self.addResultsWidgets(['rate', 'cardDue'])
    
    def processInput(self, e=0):
        result = super().processInput(1)

        if result:

            if self.client and PRMP_MsgBox(self, title='Edit Client Details', message='Are you sure to edit the details of this client?', _type='question').result == True: print('yes')
            
            elif self.manager and PRMP_MsgBox(self, title='Client Creation', message='Are you sure to create a new client?', _type='question').result == True: client = self.manager.createClient(**result)


        print(result)


class ClientAccountDialog(AccountDialog):

    def _setupDialog(self):
        super()._setupDialog()
        self.addEditButton()
        
        self.rate = LabelEntry(self.container, topKwargs=dict(config=dict(text='Rate')), bottomKwargs=dict(_type='money'),orient='h', place=dict(relx=.005, y=52, h=40, relw=.8), longent=.4)
        
        self.addResultsWidgets('rate')


class AccountDetailsDailog: pass


class ThriftDialog(PRMP_Dialog):
    def __init__(self, master=None, thrift=None, title='Thrift Dialog', values={}, manager=None, **kwargs):
        self.thrift = thrift
        self.values = values
        self.manager = manager
        super().__init__(master, geo=(350, 300), title=title, **kwargs)

    def _setupDialog(self):
        self.addEditButton()
        self.thrifts = ThriftFrame(self.container, callback=self.set, place=dict(relx=.01, rely=.01, relh=.82, relw=.96), thrift=self.thrift, values=self.values, manager=self.manager)

        self.get = self.thrifts.get
        self.set = self.thrifts.set
        # self.after(1000, self.test)
    
    def test(self):
        print(self.get())
    
    def action(self):
        print(self.result)
        if self.result:
            if self.thrift: PRMP_MsgBox(self, title='Edit thrift Details', message='Are you sure to edit the details of this thrift?', _type='question', callback=self.updateThrift)
            
            elif self.manager: PRMP_MsgBox(self, title='Thrift Creation', message='Are you sure to create a new Thrift?', _type='question', callback=newThrift)
            else: PRMP_MsgBox(self, title='Thrift Dialog Error', message='No Thrift or Manager is given.', _type='error', ask=0)
    
    def updateThrift(self, w):
        if w:
            try:
                self.thrift.update(**self.result, reload_=1)
                self._setResult(self.thrift)

            except Exception as error: PRMP_MsgBox(self, title='Thrift Update Error', message=error, _type='error', ask=0)
        self.destroyDialog()
    
    def newThrift(self, w):
        if w:
            try:
                thrift = self.manager.createThrift(**self.result)
                self._setResult(thrift)
            except Exception as error: PRMP_MsgBox(self, title='Thrift Creation Error', message=error, _type='error', ask=0)
        self.destroyDialog()


class ThriftDetailsDialog(PRMP_Dialog):
    def __init__(self, master=None, title='Thrift Details Dialog', thrift=None, geo=(350, 550), values={}, **kwargs):
        self.thrift = thrift
        self.values = values
        super().__init__(master, geo=geo, title=title, **kwargs)

    def _setupDialog(self):
        self.thriftDetail = ThriftDetail(self.container, place=dict(relx=.02, rely=.005, relh=.99, relw=.96), thrift=self.thrift, values=self.values)
        
        self.get = self.thriftDetail.get
        self.set = self.thriftDetail.set


class DailyContributionDailog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Area 1 Daily Contribution', dailyContribution=None, **kwargs):
        
        self.dailyContribution = dailyContribution
        super().__init__(master, title=title, **kwargs)

    def _setupDialog(self):
        self.area = area
        # self.addTitleBar(self.dumTitle)

        self.showAccount = Button
        self.subs = SubsList
        self.date





