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


class ThriftDialog(PRMP_Dialog):
    def __init__(self, master=None, thrift=None, title='Thrift Dialog', values={}, manager=None, **kwargs):
        self.thrift = thrift
        self.values = values
        self.manager = manager
        super().__init__(master, geo=(350, 300), title=title, **kwargs)

    def _setupDialog(self):
        self.addEditButton()
        self.thrifts = ThriftInput(self.container, callback=self.set, place=dict(relx=.01, rely=.01, relh=.82, relw=.96), thrift=self.thrift, values=self.values, manager=self.manager)

        self.get = self.thrifts.get
        self.set = self.thrifts.set
        
        for k in self.thrifts.resultsWidgets: self.__dict__[k] = self.thrifts.__dict__[k]

        self.addResultsWidgets(self.thrifts.resultsWidgets)

    # def set(self, values={}):
    #     if values:
    #         if isinstance(values, Thrift):
    #             values.get('money')
    #             values['income'] = values
    #         elif isinstance(values, dict):
    #             if values.get('money'): values.


    def action(self):
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
    
    def __init__(self, master=None, title='Area 1 Daily Contribution', dcContrib=None, geo=(1200, 800), **kwargs):
        
        self.dcContrib = dcContrib
        super().__init__(master, title=title, geo=geo, **kwargs)
    
    def changeDate(self, date):
        if date: self.totals.date.set(date.date)
    
    def _placeSubmitButton(self):
        x, y = self.containerGeo
        self.submitBtn.place(x=120 , y=y-40, h=30, w=60)

    def _setupDialog(self):
        self.addEditButton()

        self.area = Button(self.container, command=self.openArea, text='Area', place=dict(relx=.007, rely=.005, relw=.17, relh=.05))

        self.date = LabelDateButton(self.container, topKwargs=dict(text='Date'), place=dict(relx=.18, rely=.005, relw=.11, relh=.05), orient='h', bottomKwargs=dict(callback=self.changeDate), longent=.37)

        self.account = LabelCombo(self.container, topKwargs=dict(text='Area\'s Account'), place=dict(relx=.005, rely=.06, relw=.2, relh=.1), longent=.4, func=self.setAreaAccountDependents)
        self.account.get = self.account.B.getObj
        
        self.month = LabelMonthYearButton(self.container, topKwargs=dict(text='Month'), place=dict(relx=.21, rely=.06, relw=.08, relh=.1), longent=.4)

        PRMP_Separator(self.container, place=dict(relx=.005, rely=.19, relh=.005, relw=.29))

        self.newClient = Button(self.container, text='New Client', place=dict(relx=.007, rely=.225, relw=.1, relh=.04))
        self.newClientAccount = Button(self.container, text='New Client Account', place=dict(relx=.11, rely=.225, relw=.15, relh=.04))

        self.ledgerNumber = LabelSpin(self.container, topKwargs=dict(text='Ledger Number'), place=dict(relx=.005, rely=.275, relw=.25, relh=.05), longent=.43, orient='h', func=self.clientNumberChanged)
        
        self.clientName = LabelLabel(self.container, topKwargs=dict(text='Client Name'), place=dict(relx=.005, rely=.33, relw=.29, relh=.05), longent=.32, orient='h')

        PRMP_Separator(self.container, place=dict(relx=.005, rely=.412, relh=.005, relw=.29))

        self.income = LabelEntry(self, topKwargs=dict(text='Income'), bottomKwargs=dict(_type='money'), place=dict(relx=.005, rely=.46, relh=.05, relw=.14), orient='h')
        self.money = Checkbutton(self, text='Money?', place=dict(relx=.18, rely=.467, relh=.03, relw=.065))

        self.transfer = LabelEntry(self, topKwargs=dict(text='Transfer'), place=dict(relx=.005, rely=.515, relh=.05, relw=.14), orient='h', bottomKwargs=dict(_type='money'))

        self.paidout = LabelEntry(self, topKwargs=dict(text='Paidout'), bottomKwargs=dict(_type='money'), orient='h', place=dict(relx=.005, rely=.57, relh=.05, relw=.14))

        self.ready = Checkbutton(self.container, text='Ready?', place=dict(relx=.2, rely=.525, relh=.04, relw=.07))
        self.addThriftBtn = Button(self.container, text='Add Thrift', place=dict(relx=.18, rely=.575, relh=.04, relw=.09), command=self.addThrift)

        PRMP_Separator(self.container, place=dict(relx=.005, rely=.663, relh=.005, relw=.29))

        self.contributed = LabelSpin(self.container, topKwargs=dict(text='Contributed'), place=dict(relx=.005, rely=.685, relw=.22, relh=.05), orient='h', longent=.4)

        self.delete = Button(self.container, text='Delete', place=dict(relx=.23, rely=.685, relw=.06, relh=.04))

        PRMP_Separator(self.container, place=dict(relx=.005, rely=.765, relh=.005, relw=.29))

        self.bto = LabelEntry(self.container, topKwargs=dict(text='Brought To Office'), place=dict(relx=.005, rely=.8, relw=.2, relh=.05), orient='h', longent=.6, bottomKwargs=dict(placeholder='Enter B-T-O', _type='money'))

        self.addBto = Button(self.container, text='Add B-T-O', place=dict(relx=.21, rely=.805, relw=.08, relh=.04))

        PRMP_Separator(self.container, place=dict(relx=.005, rely=.882, relh=.005, relw=.29))

        self.manUpdate = Button(self.container, text='Update', place=dict(relx=.225, rely=.945, relw=.07, relh=.04), command=self.update)


        self.view = Hierachy(self.container, place=dict(relx=.3, rely=.005, relw=.695, relh=.69))
        self.view.setColumns(TreeColumns.columns(self.dcContrib))

        self.totals = DailyContTotal(self.container, place=dict(relx=.3, rely=.7, relw=.692, relh=.29), relief='groove', dcContrib=self.dcContrib)

        self.addResultsWidgets(['area', 'date', 'ledgerNumber', 'clientName', 'month', 'newClientAccount', 'newClient', 'account', 'income', 'money', 'paidout', 'transfer', 'contributed', 'delete', 'bto', 'addBto', 'ready', 'addThriftBtn', 'manUpdate'])
        
    def defaults(self):

        self.bind('<Up>', self.increaseClientNumber, '+')
        self.bind('<Down>', self.decreaseClientNumber, '+')
        self.bind('<Return>', self.addThrift, '+')
        
        self.container.bind('<1>', lambda e: self.focus())

        self._account = None
        self._clientAccount = None
        
        if self.dcContrib: self._area = self.dcContrib.manager.master
        else: self._area = None

        if self._area:
            self.account.B.setObjs(self._area, 'name')
            self.area.set(self._area.name)
        
        self.update()

        # self.editBtn.set(False)
        # self.editInput()

    def getThriftDetails(self): return self.get(['income', 'paidout', 'money', 'transfer', 'ledgerNumber', 'account'])

    def update(self):
        if not self.dcContrib: return

        self.date.set(self.dcContrib.date.date)
        self.view.viewSubs(self.dcContrib)
        self.totals.set()


    def openArea(self): pass

    def processInput(self):
        pass

    def addThrift(self, e=0):
        if e and (e.widget == self.ledgerNumber.B): return

        if not self.editBtn.get(): return
        thriftDetails = self.getThriftDetails()
        
        try: assert self._account == thriftDetails['account'], 'No area account is selected.'
        except AssertionError:
            PRMP_MsgBox(self, title='Account Error', message='No area account is selected.', ask=0, _type='error')
            return


        try: self.dcContrib.createThrift(**thriftDetails)
        except Exception as error: PRMP_MsgBox(self, title='Thrift Creation Error', message=error, ask=0, _type=error)
        self.update()
        print(self.dcContrib[:])

    def clientsAccounts(self):
        if self._account: return self._account.clientsAccounts()
        return []

    def setAreaAccountDependents(self, e=None):
        self._account = self.account.B.getObj()
        self.setClientNumbers()

    def maxNum(self): return len(self.clientsAccounts())

    def setClientNumbers(self):
        max_ = self.maxNum()
        
        self.ledgerNumber.B.configure(from_=1, to=max_ or 1, increment=1)
    
    def decreaseClientNumber(self, e=0):
        if e.widget == self.account.B: return

        get = self.ledgerNumber.get() or 0
        get = int(float(get))
        
        if get == 0: val = self.maxNum()
        elif get: val = get - 1
        else: val = 1
        
        if e.widget != self.ledgerNumber.B: self.ledgerNumber.B.set(val)
        self.ledgerNumber.B.event_generate('<<Decrement>>')

    def increaseClientNumber(self, e=0):
        if e.widget == self.account.B: return

        maxNum = self.maxNum()
        get = self.ledgerNumber.get() or maxNum
        get = int(float(get))
        val = maxNum

        if get == maxNum: val = 1
        else: val = get + 1
        
        if e.widget != self.ledgerNumber.B: self.ledgerNumber.B.set(val)

        self.ledgerNumber.B.event_generate('<<Increment>>')

    def clientNumberChanged(self, e=None):
        num = self.ledgerNumber.get()
        if num == None: return
        if not self._account:
            PRMP_MsgBox(self, title='No Area Account', message=f'An area account has not been choosen.', ask=0, _type='error')
            return

        num = int(num)
        clientAccount = self._account.getClientAccount(num)
        
        if clientAccount:
            self._clientAccount = clientAccount
            self.clientName.set(self._clientAccount.region.name)
        else:
            self._clientAccount = None
            PRMP_MsgBox(self, title='Not Found', message=f'No Client with account\'s ledger number = {num}.', ask=0, _type='error')









