from ..core.gam_apps import *
from ...backend.dc.dc_regions import *
from ...backend.dc.dc_specials import *
from prmp_gui.plot_canvas import PRMP_PlotCanvas, random#, ChartSort


# class DC_ChartSort(ChartSort): pass


class DC_Digits(PRMP_FillWidgets, Frame):
    
    def __init__(self, master, values={}, **kwargs):
        Frame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self, values)
        font = self.DEFAULT_FONT.copy()
        font['size'] = 20
     # Incomes
        self._incomes = incomes = LabelFrame(self, text='Incomes')
        Label(incomes, text='Savings', place=dict(relx=.03, rely=.27, relh=.21, relw=.48))
        Label(incomes, text='Transfers', place=dict(relx=.03, rely=.51, relh=.21, relw=.48))
        self.comm = Label(incomes, text='Commissions', place=dict(relx=.03, rely=.74, relh=.21, relw=.48))

        self.incomes = Entry_Label(incomes, text='₦ 3,000,000i', place=dict(relx=.03, rely=0, relh=.24, relw=.94), font=font)
        self.savings = Entry_Label(incomes, text='₦ 50,000s', place=dict(relx=.53, rely=.27, relh=.21, relw=.44))
        self.transfers = Entry_Label(incomes, text='₦ 30,000tr', place=dict(relx=.53, rely=.51, relh=.21, relw=.44))
        self.commissions = Entry_Label(incomes, text='₦ 30,000c', place=dict(relx=.53, rely=.74, relh=.22, relw=.44))

     # Debits
        self._paidoutits = debits = LabelFrame(self, text='Debits')
        Label(debits, text='Withdrawals', place=dict(relx=.03, rely=.35, relh=.3, relw=.48))
        Label(debits, text='Paidouts', place=dict(relx=.03, rely=.68, relh=.28, relw=.48))

        self.debits = Entry_Label(debits, text='₦ 80,000d', place=dict(relx=.03, rely=0, relh=.32, relw=.94), font=font)
        self.withdrawals = Entry_Label(debits, text='₦ 50,000w', place=dict(relx=.53, rely=.35, relh=.3, relw=.44))
        self.paidouts = Entry_Label(debits, text='₦ 30,000p', place=dict(relx=.53, rely=.68, relh=.28, relw=.44))

     # Upfronts
        self._upfronts = upfronts = LabelFrame(self, text='Upfronts')
        Label(upfronts, text='Repaid', place=dict(relx=.03, rely=.35, relh=.3, relw=.48))
        Label(upfronts, text='Overdue', place=dict(relx=.03, rely=.68, relh=.28, relw=.48))

        self.upfronts = Entry_Label(upfronts, text='₦ 980,000up', place=dict(relx=.03, rely=0, relh=.32, relw=.94), font=font)
        self.repaid = Entry_Label(upfronts, text='₦ 850,000r', place=dict(relx=.53, rely=.35, relh=.3, relw=.44))
        self.overdue = Entry_Label(upfronts, text='₦ 130,000ov', place=dict(relx=.53, rely=.68, relh=.28, relw=.44))

     # Balances
        self._balances = balances = LabelFrame(self, text='Balances')
        Label(balances, text='Brought-Fs', place=dict(relx=.03, rely=.2, relh=.18, relw=.48))
        Label(balances, text='B-T-Os', place=dict(relx=.03, rely=.4, relh=.18, relw=.48))
        Label(balances, text='Deficits', place=dict(relx=.03, rely=.6, relh=.18, relw=.48))
        Label(balances, text='Excesses', place=dict(relx=.03, rely=.8, relh=.18, relw=.48))
        fon = font.copy()
        fon['size'] = 15
        self.balances = Entry_Label(balances, text='₦ 1,080,000', place=dict(relx=.03, rely=0, relh=.18, relw=.94), font=fon)
        self.broughts = Entry_Label(balances, text='₦ 500,000br', place=dict(relx=.53, rely=.2, relh=.18, relw=.44))
        self.btos = Entry_Label(balances, text='₦ 30,000bto', place=dict(relx=.53, rely=.4, relh=.18, relw=.44))
        self.deficits = Entry_Label(balances, text='₦ 30,000def', place=dict(relx=.53, rely=.6, relh=.18, relw=.44))
        self.excesses = Entry_Label(balances, text='₦ 30,000exc', place=dict(relx=.53, rely=.8, relh=.18, relw=.44))

        self.addResultsWidgets(['incomes', 'savings', 'debits', 'withdrawals', 'paidouts', 'upfronts', 'repaid', 'overdue', 'balances', 'broughts', 'commissions', 'btos', 'transfers', 'deficits', 'excesses', 'comm'])

    def placeVertically(self):
        self._incomes.place(relx=.02, rely=.008, relh=.256, relw=.96)
        self._paidoutits.place(relx=.02, rely=.267, relh=.21, relw=.96)
        self._upfronts.place(relx=.02, rely=.48, relh=.198, relw=.96)
        self._balances.place(relx=.02, rely=.68, relh=.312, relw=.96)

    def placeHorizontally(self):
        self._incomes.place(relx=0, rely=0, relh=1, relw=.25)
        self._paidoutits.place(relx=.25, rely=0, relh=1, relw=.25)
        self._upfronts.place(relx=.5, rely=0, relh=1, relw=.25)
        self._balances.place(relx=.75, rely=0, relh=1, relw=.25)

    def update(self, account):
        
        debits = account.debits
        upfronts = account.upfronts
        
        fillDict = dict(
            incomes=int(account.incomes),
            savings=int(account.savings),
        
            debits=int(debits),

            withdrawals=int(account.withdrawals),
            paidouts=int(account.paidouts),
        
            upfronts=int(upfronts),
            repaid=int(upfronts.repaid),
            overdue=int(upfronts.overdue),

            balances=int(account.balances),
            broughts=int(account.broughtForwards),
            transfers=int(account.transfers)
            )
        
        if not isinstance(account.region, Client):
            not_client = dict(
                commissions=int(account.commissions),
                btos=int(account.btos),
                deficits=int(account.deficits),
                excesses=int(account.excesses))
            fillDict.update(not_client)
        else:
            client = dict(commissions=account.rate)
            fillDict.update(client)
        
        for key in fillDict:
            val = fillDict[key]
            new_val = self.numWithSign_Commas(val)
            fillDict[key] = new_val
        
        fillDict['comm'] = 'Commissions' if not isinstance(account.region, Client) else 'Rate'

        self.fill(fillDict)


class DC_Overview(Frame):
    
    def __init__(self, master, title='DC Overview', orient='v', obj=None, account=None, **kwargs):
        super().__init__(master, title=title, **kwargs)
        self.obj = obj

        if not account:
            if isinstance(obj, AccountsManager): account = obj.lastAccount
            elif isinstance(obj, Region): account = obj.lastAccount
        
        self.account = account

        self.month = LabelLabel(self, topKwargs=dict(text='Month'), orient='h', longent=.3)

        self.ledgerNumber = LabelLabel(self, topKwargs=dict(text='Ledger Number'), orient='h', longent=.65)

        self._prev = Button(self, text='Previous', command=self.prev)

        self._next = Button(self, text='Next', command=self.next)

        self.plotDialog = Button(self, text='Plot Dialog')

        self.dcDigits = DC_Digits(self)

        self.plotCanvas1 = PRMP_PlotCanvas(self, relief='groove', canvasConfig=dict(background="yellow", borderwidth="2"))

        self.plotCanvas2 = PRMP_PlotCanvas(self, relief='groove', canvasConfig=dict(background="yellow", borderwidth="2"))

        if orient == 'v': self.placeVertically()
        else: self.placeHorizontally()

        if self.account: self.updateDCDigits(self.account)

        self.topest.addAfters(self.afterload)
    
    def afterload(self):
        self.plotCanvas1.draw()
        self.plotCanvas2.draw()
        self.testDraw()
    
    def testDraw(self):
        # xs = list(range(1, 10))
        xs = [chr(64+a) for a in range(1, 10)]
        ys = [random.randint(2, 9) for a in xs]
        lbls = 'Test'
        ls = self.plotCanvas1.ls_choser()
        self.plotCanvas1.doPloting(chart='plot', ys=ys, xticks=xs, labels=lbls, grid=dict(lw=1, ls=ls, c='red'), marker=1)
        self.plotCanvas2.doPloting(chart='pie', ys=ys, labels=xs, explode=9, expand=0, shadow=9, title='Love', inApp=0)

    
    def placeVertically(self):
        self.month.place(relx=.005, rely=.002, relh=.051, relw=.3)
        self.ledgerNumber.place(relx=.31, rely=.002, relh=.05, relw=.2)
        self.dcDigits.place(relx=0, rely=.051, relh=.949, relw=.369)
        self._prev.place(relx=.52, rely=.005, relw=.15, relh=.04)
        self._next.place(relx=.68, rely=.005, relw=.15, relh=.04)
        self.plotDialog.place(relx=.85, rely=.005, relw=.15, relh=.04)
        self.dcDigits.placeVertically()
        self.plotCanvas1.place(relx=.375, rely=.051, relh=.4745, relw=.625)
        self.plotCanvas2.place(relx=.375, rely=.5255, relh=.4745, relw=.625)

    def placeHorizontally(self):
        self.month.place(relx=.005, rely=.002, relh=.051, relw=.3)
        self.ledgerNumber.place(relx=.31, rely=.004, relh=.05, relw=.2)
        self._prev.place(relx=.694, rely=.007, relh=.04, relw=.12)
        self._next.place(relx=.816, rely=.007, relh=.04, relw=.08)
        self.plotDialog.place(relx=.898, rely=.007, relh=.04, relw=.1)
        self.dcDigits.place(relx=0, rely=.05, relh=.28, relw=1)
        self.dcDigits.placeHorizontally()
        self.plotCanvas1.place(relx=0, rely=.33, relh=.67, relw=.5)
        self.plotCanvas2.place(relx=.5, rely=.33, relh=.67, relw=.5)
    
    def updateDCDigits(self, account):
        self.account = account
        self.month.set(self.account.month.monthYear)
        if isinstance(account.region, Client): self.ledgerNumber.set(account.ledgerNumber)
        self.dcDigits.update(account)
    
    def next(self):
        if not self.account: return
        _next = self.account.next
        # print(_next)
        if _next: self.updateDCDigits(_next)

    def prev(self):
        if not self.account: return
        _prev = self.account.previous
        if _prev: self.updateDCDigits(_prev)


class ThriftInput(PRMP_FillWidgets, Frame):
    def __init__(self, master, thrift=None, values={}, manager=None, callback=None, **kwargs):
        Frame.__init__(self, master, **kwargs)

        self.thrift = thrift
        PRMP_FillWidgets.__init__(self, thrift or values)
        self.manager = manager
        
        _date = ''
        if thrift:_date = thrift.date.date
        elif manager:_date = manager.date.date
        
        state = (None, None)
        if thrift: state = 'readonly', 'disabled'

        self.ledgerNumber = LabelEntry(self, topKwargs=dict(text='Ledger Number'), bottomKwargs=dict(_type='number', state=state[0]), place=dict(relx=.005, rely=.005, relh=.18, relw=.99), orient='h', longent=.46)

        self.month = LabelMonthYearButton(self, topKwargs=dict(text='Month-Year'), place=dict(relx=.005, rely=.18, relh=.18, relw=.99), orient='h', longent=.46, bottomKwargs=dict(state=state[1]))

        self._income = LabelEntry(self, topKwargs=dict(text='Income'), bottomKwargs=dict(_type='money'), place=dict(relx=.005, rely=.36, relh=.18, relw=.47), orient='h', longent=.4)
        self.transfer = LabelEntry(self, topKwargs=dict(text='Transfer'), place=dict(relx=.48, rely=.36, relh=.18, relw=.515), orient='h', longent=.48, bottomKwargs=dict(_type='money'))
        self.money = Checkbutton(self, text='Money?', place=dict(relx=.76, rely=.545, relh=.13, relw=.24))

        self.paidout = LabelEntry(self, topKwargs=dict(text='Paidout'), bottomKwargs=dict(_type='money'), orient='h', place=dict(relx=.005, rely=.54, relh=.18, relw=.6))

        self.date = LabelEntry(self, topKwargs=dict(text='Date'), place=dict(relx=.005, rely=.73, relh=.18, relw=.6), orient='h', longent=.46, bottomKwargs=dict(state='readonly', placeholder=_date))
        
        self.addResultsWidgets(['ledgerNumber', 'month', '_income', 'money', 'paidout', 'transfer'])
    
    def get(self):
        res = super().get()

        res['income'] = res['_income']
        del res['_income']
        
        if self.thrift: del res['ledgerNumber'], res['month']

        return res


class ThriftDetailPart(PRMP_FillWidgets, Frame):
    
    def __init__(self, master, dc=None, values={}, **kwargs):
        Frame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self, dc or values)
        
        _date = ''
        if dc: _date = dc.date.date
        self.date = LabelEntry(self, topKwargs=dict(text='Date'), place=dict(relx=.005, rely=.005, relh=.1, relw=.7), orient='h', bottomKwargs=dict(state='readonly', placeholder=_date))

        PRMP_Separator(self, place=dict(relx=.005, rely=.11, relh=.005, relw=.99))

        self.contributed = LabelEntry(self, topKwargs=dict(text='Contributed'), place=dict(relx=.005, rely=.12, relh=.1, relw=.8), orient='h', bottomKwargs=dict(state='readonly'))
        self.cash = LabelEntry(self, topKwargs=dict(text='Cash'), place=dict(relx=.005, rely=.23, relh=.1, relw=.43), orient='h', longent=.4, bottomKwargs=dict(state='readonly'))
        self.transfer = LabelEntry(self, topKwargs=dict(text='Transfer'), place=dict(relx=.45, rely=.23, relh=.1, relw=.54), orient='h', longent=.42, bottomKwargs=dict(state='readonly'))
        self.income = LabelEntry(self, topKwargs=dict(text='Income'), place=dict(relx=.005, rely=.34, relh=.1, relw=.8), orient='h', bottomKwargs=dict(state='readonly'))
        self.paidout = LabelEntry(self, topKwargs=dict(text='Paidout'), place=dict(relx=.005, rely=.45, relh=.1, relw=.8), orient='h', bottomKwargs=dict(state='readonly'))

        PRMP_Separator(self, place=dict(relx=.005, rely=.555, relh=.005, relw=.99))

        self.saved = LabelEntry(self, topKwargs=dict(text='Saved'), place=dict(relx=.005, rely=.57, relh=.1, relw=.8), orient='h', bottomKwargs=dict(state='readonly'))
        self.upfrontRepay = LabelEntry(self, topKwargs=dict(text='Upfront Repay'), place=dict(relx=.005, rely=.677, relh=.1, relw=.99), orient='h', longent=.4, bottomKwargs=dict(state='readonly'))

        PRMP_Separator(self, place=dict(relx=.005, rely=.785, relh=.005, relw=.99))

        self.uniqueID = LabelEntry(self, topKwargs=dict(text='Unique ID'), place=dict(relx=.005, rely=.799, relh=.2, relw=.99), bottomKwargs=dict(state='readonly', placeholder='Unique ID here.'))

        self.addResultsWidgets(['contributed', 'transfer', 'income', 'paidout', 'saved', 'upfrontRepay', 'uniqueID', 'cash'])


class ThriftDetail(PRMP_FillWidgets, Frame):
    
    def __init__(self, master, thrift=None, values={}, **kwargs):
        Frame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self, thrift or values)

        self.thrift = thrift
        
        self._account = None
        self._manager = None
        self._paidoutRecord = None
        self._contRecord = None
        self._tranRecord = None
        self._debRecord = None
        self._conTranRecord = None

        self.loadOtherObjects()

        self.manager = Button(self, text='Manager', place=dict(relx=.005, rely=.01, relh=.06, relw=.35), command=self.openManager)
        self.clientAccount = Button(self, text='Client Account', place=dict(relx=.4, rely=.01, relh=.06, relw=.55), command=self.openAccount)

        self.detailsPart = ThriftDetailPart(self, place=dict(relx=.002, rely=.075, relh=.67, relw=.996), dc=thrift)
        
        for k in self.detailsPart.resultsWidgets: self.__dict__[k] = self.detailsPart.__dict__[k]
        
        self.get = self.detailsPart.get
        self.set = self.detailsPart.set


        PRMP_Separator(self, place=dict(relx=.005, rely=.755, relh=.005, relw=.99))

        records = LabelFrame(self, text='Records', place=dict(relx=.005, rely=.765, relw=.99, relh=.23))

        self.contRecord = Button(records, text='Contribution', place=dict(relx=.005, rely=.005, relh=.25, relw=.4), command=self.openContRecord)
        self.conTranRecord = Button(records, text='ConTransfer', place=dict(relx=.005, rely=.3, relh=.25, relw=.4), command=self.openConTranRecord)
        self.tranRecord = Button(records, text='Transfer', place=dict(relx=.005, rely=.6, relh=.25, relw=.4), command=self.openTranRecord)
        self.debRecord = Button(records, text='Debit', place=dict(relx=.55, rely=.005, relh=.25, relw=.4), command=self.openDebRecord)
        self.paidoutRecord = Button(records, text='Paidout', place=dict(relx=.55, rely=.3, relh=.25, relw=.4), command=self.openPaidoutRecord)

        self.updateBtn = Button(records, text='Update', place=dict(relx=.56, rely=.6, relh=.25, relw=.4), command=self.openThrift)
    
    def loadOtherObjects(self):
        if self.thrift:
            self._account = self.thrift.account
            self._manager = self.thrift.manager
            
            self._paidoutRecord = self.thrift.paidoutRecord
            self._contRecord = self.thrift.contRecord
            self._tranRecord = self.thrift.tranRecord
            self._debRecord = self.thrift.debRecord
            self._conTranRecord = self.thrift.conTranRecord

    def openManager(self):
        if self._manager:
            from .dc_dialogs import DailyContributionDailog
            DailyContributionDailog(self, dailyContribution=self._manager)
    def openAccount(self):
        if self._account:
            from .dc_dialogs import AccountDetailsDailog
            AccountDetailsDailog(self, dailyContribution=self._account)
    def openContRecord(self):
        if self._contRecord:
            from .dc_dialogs import RecordDialog
            RecordDialog(self, record=self._contRecord)
    def openPaidoutRecord(self):
        if self._paidoutRecord:
            from .dc_dialogs import RecordDialog
            RecordDialog(self, record=self._paidoutRecord)
    def openTranRecord(self):
        if self._tranRecord:
            from .dc_dialogs import RecordDialog
            RecordDialog(self, record=self._tranRecord)
    def openConTranRecord(self):
        if self._conTranRecord:
            from .dc_dialogs import RecordDialog
            RecordDialog(self, record=self._conTranRecord)
    def openDebRecord(self):
        if self._debRecord:
            from .dc_dialogs import RecordDialog
            RecordDialog(self, record=self._debRecord)
    def openThrift(self):
        from .dc_dialogs import ThriftDialog
        self.thriftDialog = ThriftDialog(self, thrift=self.thrift, callback=self.update)
    def changeStates(self, r=0):
        for rw in [self.getFromSelf(w) for w in self.resultsWidgets]:
            if r: rw.readonly()
            else: rw.normal()
    def update(self, thrift):
        if thrift is self.thrift:
            self.changeStates()
            self.set(thrift)
            self.changeStates(1)
            self.loadOtherObjects()


class DailyContTotal(PRMP_FillWidgets, Frame):
    
    def __init__(self, master, dcContrib=None, **kwargs):
        Frame.__init__(self, master, **kwargs)

        self.dcContrib = dcContrib

        self.date = LabelLabel(self, topKwargs=dict(text='Date'), place=dict(relx=.007, rely=.01, relw=.3, relh=.16), orient='h')
        
        UniqueID(self, place=dict(relx=.63, rely=.01, relw=.15, relh=.16), obj=dcContrib)

        Button(self, text='Refresh', place=dict(relx=.83, rely=.01, relw=.15, relh=.16), command=self.refresh)

        PRMP_Separator(self, place=dict(relx=.002, rely=.185, relh=.01, relw=.996))

        self.lastMonths = LabelEntry(self, topKwargs=dict(text='Last Month'), bottomKwargs=dict(state='readonly'), place=dict(relx=.007, rely=.21, relw=.3, relh=.16), orient='h')
        self.currentMonths = LabelEntry(self, topKwargs=dict(text='Current'), bottomKwargs=dict(state='readonly'), place=dict(relx=.32, rely=.21, relw=.3, relh=.16), orient='h')
        self.nextMonths = LabelEntry(self, topKwargs=dict(text='Next'), bottomKwargs=dict(state='readonly'), place=dict(relx=.633, rely=.21, relw=.3, relh=.16), orient='h')

        PRMP_Separator(self, place=dict(relx=.002, rely=.395, relh=.01, relw=.996))

        self.accounts = LabelEntry(self, topKwargs=dict(text='Accounts'), bottomKwargs=dict(state='readonly'), place=dict(relx=.007, rely=.425, relw=.22, relh=.15), orient='h')
        self.cash = LabelEntry(self, topKwargs=dict(text='Cash'), bottomKwargs=dict(state='readonly'), place=dict(relx=.26, rely=.425, relw=.22, relh=.15), orient='h')
        self.transfer = LabelEntry(self, topKwargs=dict(text='Transfer'), bottomKwargs=dict(state='readonly'), place=dict(relx=.52, rely=.425, relw=.22, relh=.15), orient='h')
        self.paidout = LabelEntry(self, topKwargs=dict(text='Paidout'), bottomKwargs=dict(state='readonly'), place=dict(relx=.78, rely=.425, relw=.22, relh=.15), orient='h')
        self.income = LabelEntry(self, topKwargs=dict(text='Income'), bottomKwargs=dict(state='readonly'), place=dict(relx=.007, rely=.585, relw=.22, relh=.15), orient='h')
        self.saved = LabelEntry(self, topKwargs=dict(text='Saved'), bottomKwargs=dict(state='readonly'), place=dict(relx=.26, rely=.585, relw=.22, relh=.15), orient='h')
        self.upfrontRepay = LabelEntry(self, topKwargs=dict(text='Upfront Repay'), bottomKwargs=dict(state='readonly'), place=dict(relx=.52, rely=.585, relw=.32, relh=.15), orient='h')
        
        PRMP_Separator(self, place=dict(relx=.002, rely=.75, relh=.01, relw=.996))


        self.bto = LabelEntry(self, topKwargs=dict(text='Brought To Office'), bottomKwargs=dict(state='readonly'), place=dict(relx=.007, rely=.77, relw=.4, relh=.16), orient='h')
        self.excess = LabelEntry(self, topKwargs=dict(text='Excess'), bottomKwargs=dict(state='readonly'), place=dict(relx=.52, rely=.77, relw=.22, relh=.16), orient='h')
        self.deficit = LabelEntry(self, topKwargs=dict(text='Deficit'), bottomKwargs=dict(state='readonly'), place=dict(relx=.75, rely=.77, relw=.22, relh=.16), orient='h')
        
        PRMP_FillWidgets.__init__(self, dcContrib)
        self.addResultsWidgets(['lastMonths', 'currentMonths', 'nextMonths', 'accounts', 'bto', 'excess', 'deficit', 'transfer', 'income', 'paidout', 'saved', 'upfrontRepay', 'cash'])

        self._refresh()
    
    def _refresh(self):
        if  not self.dcContrib: return
        self.date.set(self.dcContrib.date.date)
        for wid in self.resultsWidgets: self.getFromSelf(wid).normal()
        self.set()
        for wid in self.resultsWidgets: self.getFromSelf(wid).readonly()

    def refresh(self):
        self._refresh()
        PRMP_MsgBox(self, title='Successful', message='The refresh is successful.', ask=0, okText='Ok')
















