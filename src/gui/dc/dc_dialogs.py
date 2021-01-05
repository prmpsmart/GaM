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
        result = super().processInput(e)

        if result == None: return

        if self.client and PRMP_MsgBox(self, title='Edit Client Details', message='Are you sure to edit the details of this client?', _type='question').result == True: print('yes')
        
        elif self.manager and PRMP_MsgBox(self, title='Client Creation', message='Are you sure to create a new client?', _type='question').result == True: client = self.manager.createClient(**result)

        if self._return: self.destroy()

        print(result)


class ClientAccountDialog(AccountDialog):

    def _setupDialog(self):
        super()._setupDialog()
        self.addEditButton()
        
        self.rate = LabelEntry(self.container, topKwargs=dict(config=dict(text='Rate')), bottomKwargs=dict(_type='money'),orient='h', place=dict(relx=.005, y=52, h=40, relw=.8), longent=.4)
        
        self.addResultsWidgets('rate')


class NewThriftDialog(PRMP_Dialog):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def _setupDialog(self):
        self.addEditButton()
        self.thrifts = NewThrift(self.container, callback=self.set, place=dict(relx=.02, rely=.02, relh=.8, relw=.96))

        self.ledgerNumber = self.thrifts.ledgerNumber
        self.monthYear = self.thrifts.monthYear
        self.income = self.thrifts.income
        self.money = self.thrifts.money
        self.debit = self.thrifts.debit
        self.paidout = self.thrifts.paidout
        self.transfer = self.thrifts.transfer

        self.addResultsWidgets(['ledgerNumber', 'monthYear', 'income', 'money', 'debit', 'paidout', 'transfer'])

class ThriftsDetailsDialog(PRMP_Dialog):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

    def _setupDialog(self):
        self.thrifts = NewThrift(self, callback=self.set)

class DailyContributionDailog(PRMP_Dialog):
    
    def __init__(self, master=None, title='Area 1 Daily Contribution', area=None, **kwargs):
        super().__init__(master, **kwargs)

    def _setupDialog(self):
        self.area = area
        self.addTitleBar(title)

        self.showAccount = Button





