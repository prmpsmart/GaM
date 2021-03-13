from ..gam.gam_apps import *
from ...backend.dc.dc_regions import *
from ...backend.dc.dc_specials import *
from prmp.prmp_gui.plot_canvas import PRMP_PlotCanvas, random#, ChartSort
from tkinter.colorchooser import askcolor



class DC_Digits(PRMP_FillWidgets, Frame):

    def __init__(self, master, values={}, **kwargs):
        Frame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self, values)
        font = self.PRMP_FONT.copy()
        font['size'] = 24
        font2 = self.PRMP_FONT.copy()
        font2['size'] = 16

     # Incomes
        self._incomes = incomes = LabelFrame(self, text='Incomes')
        Label(incomes, text='Savings', place=dict(relx=.03, rely=.27, relh=.21, relw=.48), font=font2)
        Label(incomes, text='Transfers', place=dict(relx=.03, rely=.51, relh=.21, relw=.48), font=font2)
        self.comm = Label(incomes, text='Commissions', place=dict(relx=.03, rely=.74, relh=.21, relw=.48), font=font2)

        self.incomes = Entry_Label(incomes, text='₦ 3,000,000i', place=dict(relx=.03, rely=0, relh=.24, relw=.94), font=font)
        self.savings = Entry_Label(incomes, text='₦ 50,000s', place=dict(relx=.53, rely=.27, relh=.21, relw=.44), font=font2)
        self.transfers = Entry_Label(incomes, text='₦ 30,000tr', place=dict(relx=.53, rely=.51, relh=.21, relw=.44), font=font2)
        self.commissions = Entry_Label(incomes, text='₦ 30,000c', place=dict(relx=.53, rely=.74, relh=.22, relw=.44), font=font2)

     # Debits
        self._paidoutits = debits = LabelFrame(self, text='Debits')
        Label(debits, text='Withdrawals', place=dict(relx=.03, rely=.35, relh=.3, relw=.48), font=font2)
        Label(debits, text='Paidouts', place=dict(relx=.03, rely=.68, relh=.28, relw=.48), font=font2)

        self.debits = Entry_Label(debits, text='₦ 80,000d', place=dict(relx=.03, rely=0, relh=.32, relw=.94), font=font)
        self.withdrawals = Entry_Label(debits, text='₦ 50,000w', place=dict(relx=.53, rely=.35, relh=.3, relw=.44), font=font2)
        self.paidouts = Entry_Label(debits, text='₦ 30,000p', place=dict(relx=.53, rely=.68, relh=.28, relw=.44), font=font2)

     # Upfronts
        self._upfronts = upfronts = LabelFrame(self, text='Upfronts')
        Label(upfronts, text='Repaid', place=dict(relx=.03, rely=.35, relh=.3, relw=.48), font=font2)
        Label(upfronts, text='Overdue', place=dict(relx=.03, rely=.68, relh=.28, relw=.48), font=font2)

        self.upfronts = Entry_Label(upfronts, text='₦ 980,000up', place=dict(relx=.03, rely=0, relh=.32, relw=.94), font=font)
        self.repaid = Entry_Label(upfronts, text='₦ 850,000r', place=dict(relx=.53, rely=.35, relh=.3, relw=.44), font=font2)
        self.overdue = Entry_Label(upfronts, text='₦ 130,000ov', place=dict(relx=.53, rely=.68, relh=.28, relw=.44), font=font2)

     # Balances
        self._balances = balances = LabelFrame(self, text='Balances')
        Label(balances, text='Brought-Fs', place=dict(relx=.03, rely=.2, relh=.18, relw=.48), font=font2)
        Label(balances, text='B-T-Os', place=dict(relx=.03, rely=.4, relh=.18, relw=.48), font=font2)
        Label(balances, text='Deficits', place=dict(relx=.03, rely=.6, relh=.18, relw=.48), font=font2)
        Label(balances, text='Excesses', place=dict(relx=.03, rely=.8, relh=.18, relw=.48), font=font2)
        fon = font.copy()
        fon['size'] = 15
        self.balances = Entry_Label(balances, text='₦ 1,080,000', place=dict(relx=.03, rely=0, relh=.18, relw=.94), font=fon)
        self.broughts = Entry_Label(balances, text='₦ 500,000br', place=dict(relx=.53, rely=.2, relh=.18, relw=.44), font=font2)
        self.btos = Entry_Label(balances, text='₦ 30,000bto', place=dict(relx=.53, rely=.4, relh=.18, relw=.44), font=font2)
        self.deficits = Entry_Label(balances, text='₦ 30,000def', place=dict(relx=.53, rely=.6, relh=.18, relw=.44), font=font2)
        self.excesses = Entry_Label(balances, text='₦ 30,000exc', place=dict(relx=.53, rely=.8, relh=.18, relw=.44), font=font2)

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
            incomes=float(account.incomes),
            savings=float(account.savings),

            debits=float(debits),

            withdrawals=float(account.withdrawals),
            paidouts=float(account.paidouts),

            upfronts=float(upfronts),
            repaid=float(upfronts.repaid),
            overdue=float(upfronts.overdue),

            balances=float(account.balances),
            broughts=float(account.broughtForwards),
            transfers=float(account.transfers)
            )

        if not isinstance(account.region, Client):
            not_client = dict(
                commissions=float(account.commissions),
                btos=float(account.btos),
                deficits=float(account.deficits),
                excesses=float(account.excesses))
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
        # self.incomes.set(account.incomes.name)



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
        from .dc_dialogs import PlotDialog

        self.plotDialog = Button(self, text='Plot Dialog', command=lambda: PlotDialog(self, obj=self.account))

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
        self.plotCanvas1.doPlotting(chart='plot', ys=ys, xticks=xs, labels=lbls, grid=dict(lw=1, ls=ls, c='red'), marker=1)
        self.plotCanvas2.doPlotting(chart='pie', ys=ys, labels=xs, explode=9, expand=0, shadow=9, title='Love', inApp=0)


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
        if account:
            assert isinstance(account, Account)
            self.account = account
            self.month.set(self.account.month.monthYear)
            self.ledgerNumber.set(account.ledgerNumber)
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

        # self.uniqueID = LabelEntry(self, topKwargs=dict(text='Unique ID'), place=dict(relx=.005, rely=.799, relh=.2, relw=.99), bottomKwargs=dict(state='readonly', placeholder='Unique ID here.'))

        self.addResultsWidgets(['contributed', 'transfer', 'income', 'paidout', 'saved', 'upfrontRepay', 'cash'])


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


        records = LabelFrame(self, text='Records', place=dict(relx=.005, rely=.605, relw=.99, relh=.25))

        self.contRecord = Button(records, text='Contribution', place=dict(relx=.005, rely=.005, relh=.3, relw=.4), command=self.openContRecord)
        self.conTranRecord = Button(records, text='ConTransfer', place=dict(relx=.005, rely=.345, relh=.3, relw=.4), command=self.openConTranRecord)
        self.tranRecord = Button(records, text='Transfer', place=dict(relx=.005, rely=.685, relh=.3, relw=.4), command=self.openTranRecord)

        self.debRecord = Button(records, text='Debit', place=dict(relx=.55, rely=.005, relh=.3, relw=.4), command=self.openDebRecord)
        self.paidoutRecord = Button(records, text='Paidout', place=dict(relx=.55, rely=.345, relh=.3, relw=.4), command=self.openPaidoutRecord)
        self.editBtn = Button(records, text='Edit', place=dict(relx=.55, rely=.685, relh=.3, relw=.4), command=self.openThrift)

        self.updateBtn = Button(self, text='Update', place=dict(relx=.005, rely=.88, relh=.07, relw=.4), command=self.updateThriftRecords)

        self.uniqueIDBtn = UniqueID(self, place=dict(relx=.55, rely=.88, relh=.07, relw=.4), obj=self.thrift)

    def updateThriftRecords(self): PRMP_MsgBox(self, title='Confirmation', message='Are you sure to update the records of this thrift?', callback=self._updateThriftRecords, ask=1)

    def _updateThriftRecords(self, w):
        if w and self.thrift: self.thrift.updateRecords()
        self.loadOtherObjects()

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
            DailyContributionDailog(self, dcContrib=self._manager)

    def openAccount(self):
        if self._account:
            from .dc_apps import DC_AccountHome
            DC_AccountHome(account=self._account, tm=1, tw=0, resize=(1,1))

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

        self.lastMonthIncome = LabelEntry(self, topKwargs=dict(text='Last Month'), bottomKwargs=dict(state='readonly'), place=dict(relx=.007, rely=.21, relw=.3, relh=.16), orient='h')
        self.currentMonthIncome = LabelEntry(self, topKwargs=dict(text='Current'), bottomKwargs=dict(state='readonly'), place=dict(relx=.32, rely=.21, relw=.3, relh=.16), orient='h')
        self.nextMonthIncome = LabelEntry(self, topKwargs=dict(text='Next'), bottomKwargs=dict(state='readonly'), place=dict(relx=.633, rely=.21, relw=.3, relh=.16), orient='h')

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
        self.addResultsWidgets(['lastMonthIncome', 'currentMonthIncome', 'nextMonthIncome', 'accounts', 'bto', 'excess', 'deficit', 'transfer', 'income', 'paidout', 'saved', 'upfrontRepay', 'cash'])

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


class DateDetails(PRMP_FillWidgets, LabelFrame):
    def __init__(self, master, date=None, obj=None, text='Date Details', **kwargs):
        LabelFrame.__init__(self, master, text=text, **kwargs)
        PRMP_FillWidgets.__init__(self)

        self.obj = obj

        self.date = LabelDateButton(self, topKwargs=dict(text='Date'), bottomKwargs=dict(callback=self.update, anchor='center'), place=dict(relx=.02, rely=.02, relw=.45, relh=.325), orient='h', longent=.4)

        self.account = LabelSpin(self, topKwargs=dict(text='Accounts'), place=dict(relx=.5, rely=.02, relw=.5, relh=.325), bttk=1, orient='h', longent=.6, bottomKwargs=dict(placeholder=''))

        self.monthName = LabelLabel(self, topKwargs=dict(text='Month'), place=dict(relx=.02, rely=.35, relw=.3, relh=.6))
        self.week = LabelLabel(self, topKwargs=dict(text='Week'), place=dict(relx=.35, rely=.35, relw=.3, relh=.6))
        self.dayName = LabelLabel(self, topKwargs=dict(text='Day Name'), place=dict(relx=.68, rely=.35, relw=.3, relh=.6))

        self.addResultsWidgets(['monthName', 'week', 'dayName'])
        if date: self.date.set(date)

    def get(self): return PRMP_FillWidgets.get(self, ['date', 'account'])

    def update(self, date):
        self.set(date)

        if isinstance(self.obj, DCRegion):
            accounts = self.obj.accountsManager.objectSort.sortSubsBySeasons(date, attr='month', seasons=['month'])

            accLen = len(accounts)
            if accLen:
                self.account.B.configure(from_=1, to=accLen)
                self.account.B.set(1)
            else:
                self.account.B.configure(from_=0, to=0)
                self.account.B.set(0)


class DataChoose(PRMP_FillWidgets, LabelFrame):
    def __init__(self, master, text='Data Choose', generalAction=None, **kwargs):
        LabelFrame.__init__(self, master, text=text, **kwargs)
        PRMP_FillWidgets.__init__(self)

        self.season = tk.StringVar()
        self.season.set('month')

        relief = 'solid'

     # month
        self.month = RadioCombo(self, topKwargs=dict(text='Month', variable=self.season, value='month'), bottomKwargs=dict(values=['Weeks', 'Days', 'Spec Days', 'Spec Day']), place=dict(relx=.01, rely=0, relw=.98, relh=.3), orient='h', longent=.3)
        self.month.set('Weeks')

     # week
        self.week = RadioCombo(self, topKwargs=dict(text='Week', variable=self.season, value='week'), bottomKwargs=dict(values=['Days']), place=dict(relx=.01, rely=.31, relw=.68, relh=.3), orient='h', longent=.4)

     # subs
        self.subs = RadioCombo(self, topKwargs=dict(text='Subs', variable=self.season, value='subs'), bottomKwargs=dict(values=['Date', 'Week', 'Month', 'Year']), place=dict(relx=.01, rely=.62, relw=.98, relh=.3), orient='h', longent=.3)
     #
        self.setRadioGroups([self.month, self.week, self.subs])

        Button(self, text='Parse', command=generalAction, place=dict(relx=.78, rely=.32, relw=.2, relh=.22))
        self.bind_all('<Control-S>', generalAction)
        self.bind_all('<Control-s>', generalAction)

    def get(self, e=0):
        season = self.season.get()
        val = {}
        if season in ['0', '']: PRMP_MsgBox(self, title='Season Error', message='Pick the valid options [Week, Month, Subs]')

        if season:
            va = PRMP_FillWidgets.get(self, [season])
            val['season'] = list(va.keys())[0]
            val['which'] = list(va.values())[0].replace(' ', '').lower()

        counts = sum([bool(a) for a in list(val.values())])

        if counts != 2: PRMP_MsgBox(self, title='Invalid Input', message='Pick the valid options')

        return val


class OneInAll(PRMP_FillWidgets, LabelFrame):
    def __init__(self, master, **kwargs):
        LabelFrame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self)

        self.oneInAll = tk.StringVar()
        self.oneInAll.set('0')

        self.months = RadioCombo(self, topKwargs=dict(text='Months', variable=self.oneInAll, value='months'), bottomKwargs=dict(values=MONTHS_NAMES[1:]), orient='h', place=dict(relx=.005, rely=.005, relh=.325, relw=.69))

        self.weeks = RadioCombo(self, topKwargs=dict(text='Weeks', variable=self.oneInAll, value='weeks'), bottomKwargs=dict(values=WEEKS), orient='h', place=dict(relx=.005, rely=.32, relh=.325, relw=.69))

        self.days = RadioCombo(self, topKwargs=dict(text='Days', variable=self.oneInAll, value='days'), bottomKwargs=dict(values=DAYS_NAMES), orient='h', place=dict(relx=.005, rely=.66, relh=.325, relw=.69))

        self.setRadioGroups([self.months, self.weeks, self.days])

        self.isOneinAll = Checkbutton(self, text='This?', place=dict(relx=.78, rely=.66, relh=.325, relw=.18))

        # self.addResultsWidgets(['months', 'weeks', 'days'])


    def get(self, e=0):
        PRMP_FillWidgets.get(self)

        oneInAll = self.oneInAll.get()
        val = ''
        if oneInAll == '0': oneInAll = ''
        if oneInAll:
            # wid = self.getFromSelf(oneInAll)
            # if wid: val = wid.get()
            val = PRMP_FillWidgets.get(self, [oneInAll])

        res = [oneInAll, val]
        return res


class ProperDetails(PRMP_FillWidgets, Frame):

    def __init__(self, master, obj=None, callback=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self)

        self.obj = obj
        self.callback = callback

        self.date = DateDetails(self, place=dict(relx=.005, rely=.005, relw=.99, relh=.26), relief='groove', obj=obj, date=PRMP_DateTime.now())

        self.dataChoose = DataChoose(self, text='Data Choose', place=dict(relx=.005, rely=.27, relw=.99, relh=.3), generalAction=self.parser)

        self.lists = ListBox(self, place=dict(relx=.005, rely=.59, relw=.99, relh=.41), listboxConfig=dict(selectmode='multiple'))

        Button(self, text='Load', command=self.load, place=dict(relx=.72, rely=.85, relw=.2, relh=.05))
        self.bind_all('<Control-L>', self.load)
        self.bind_all('<Control-l>', self.load)

        self.date_acc = {}
        self.data = {}
        self.columns = []
        self.heads = []

    def parser(self, e=0):
        if not self.obj: return

        self.date_acc = self.date.get()
        date = self.date_acc['date']

      # date verification
        if not date:
            PRMP_MsgBox(self, title='Date Error', message='Please choose a date', _type='error', delay=1500)
            return

      # normal
        self.data = self.dataChoose.get()

        obj, w = self.obj.objectSort.getObj(**self.date_acc, **self.data)

        columns, num = self.obj.objectSort.getColumns(**self.data, w=w)

        self.heads = columns[:num]

        self.columns = columns[num:]
        self.lists.set(self.columns)

    def load(self, e=0):
        if not self.obj: return

        cols = self.lists.selected or self.columns

        if self.callback: self.callback(columns=cols, heads=self.heads, **self.date_acc, **self.data)


class ChartOptions(Frame):

    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)

      ########## Chart Options
        self.chart_lblfrm = LabelFrame(self, text='Chart Options', place=dict(relx=.005, rely=.005, relh=.99, relw=.99))

       ### Fig number
        self.fig = LabelSpin(self.chart_lblfrm, topKwargs=dict(text='Fig. No.'), bottomKwargs=dict(to=4, from_=1, increment=1), orient='h', place=dict(relx=.003, rely=.003, relh=.18, relw=.35))

       ###### Chart Type
        self.chart_type = None
        self.chart_types = LabelCombo(self.chart_lblfrm,  topKwargs=dict(text='Chart Types'), bottomKwargs=dict(values=['Plot', 'Bar', 'Barh', 'Hist', 'Pie']), func=self.chart_types_choser, orient='h', place=dict(relx=.37, rely=.003, relh=.18, relw=.62), longent=.42)
        self.chart_types.set('Plot')

       ########## Chart Types Options
        note = Notebook(self.chart_lblfrm, place=dict(relx=.003, rely=.2, relh=.8, relw=.99))

        self.grid_options = LabelFrame(self.chart_lblfrm, takefocus='')
        note.add(self.grid_options, padding=1)
        note.tab(0, text='Grid Options',compound='left',underline='0')

        self.plot_options = LabelFrame(self.chart_lblfrm, takefocus='')
        note.add(self.plot_options, padding=1)
        note.tab(1, text='Plot Options',compound='left',underline='0')

        self.switch_options = LabelFrame(self.chart_lblfrm, takefocus='')
        note.add(self.switch_options, padding=1)
        note.tab(2, text='Switch Options',compound='left',underline='0')

        self.pie_options = LabelFrame(self.chart_lblfrm, takefocus='')
        note.add(self.pie_options, padding=1)
        note.tab(3, text='Pie Options',compound='left',underline='0')

       ########## Grid lines
        self._grid_color = PRMP_Theme.DEFAULT_BACKGROUND_COLOR

        self.grid_style = CheckCombo(self.grid_options, topKwargs=dict(text='Grid Style'), command=self.grid_decide, bottomKwargs=dict(values=['Solid', 'Dashed', 'Dashdot', 'Dotted']), orient='h', place=dict(relx=.02, rely=.02, relh=.25, relw=.65), longent=.4)

        self.grid_width = LabelSpin(self.grid_options, topKwargs=dict(text='Grid Width'), bottomKwargs=dict(from_=.1, to=1, increment=.1), orient='h', place=dict(relx=.02, rely=.3, relh=.25, relw=.65))

        self.grid_color = Button(self.grid_options, text='Color', command=self.grid_color_choser, place=dict(relx=.02, rely=.7, relh=.2, relw=.65,))

       ### Plot options

        self.marker = Checkbutton(self.plot_options, text='Marker', place=dict(relx=.02, rely=.048, relh=.23, relw=.3))

        self.linestyle = Checkbutton(self.plot_options, text='Line Style', place=dict(relx=.02, rely=.338, relh=.22, relw=.3))

        self.linewidth = LabelSpin(self.plot_options,  topKwargs=dict(text='Line Width'), bottomKwargs=dict(to=1, from_=.1, increment=.1), orient='h', place=dict(relx=.34, rely=.04, relh=.24, relw=.64))
        self.linewidth.B.set(1)

        self.alpha = LabelSpin(self.plot_options,  topKwargs=dict(text='Alpha'), bottomKwargs=dict(to=1, from_=.1, increment=.1), orient='h', place=dict(relx=.34, rely=.33, relh=.24, relw=.64))
        self.alpha.B.set(1)


       ## switch Options

        self.switch = Checkbutton(self.switch_options, text='Switch', place=dict(relx=.02, rely=.14, relh=.25, relw=.3))

       ###### Pie Options

        self.inapp = Checkbutton(self.pie_options, text='Inapp', command=self.inapp_info, place=dict(relx=.02, rely=.04, relh=.24, relw=.32))

        self.explode = Checkbutton(self.pie_options, text='Explode', place=dict(relx=.34, rely=.38, relh=.24, relw=.32))

        self.shadow = Checkbutton(self.pie_options,text='Shadow', place=dict(relx=.66, rely=.71, relh=.24, relw=.32))

     # Defaults
        self.paint()
        self.chart_types_choser()
        self.grid_decide()

    def grid_decide(self):
        self.grid_style.checked()

        options = [self.grid_style, self.grid_width, self.grid_color]

        if self.grid_style.T.get():
            for option in options[:-1]: option.normal('b')
            options[-1].normal()
        else:
            self.grid_style.set('None')
            self._grid_color = 'black'
            for option in options[:-1]: option.disabled('b')
            options[-1].disabled()

    def grid_color_choser(self):
        rgb_name, self._grid_color = askcolor(self._grid_color)
        self.grid_color.config(background=self._grid_color)

    def chart_types_choser(self, e=0):
        self.chart_type = self.chart_types.get().lower()

        plot_conf = [ self.linestyle, self.marker]
        plot_dis = [self.linewidth, self.alpha]

        if self.chart_type != 'plot':
            for conf in plot_conf: conf.disabled()
            for dis in plot_dis: dis.disabled()
        else:
            for conf in plot_conf: conf.normal()
            for dis in plot_dis: dis.normal()


        # if self.chart_type not in ['bar', 'barh']: self.switch.disabled()
        # else: self.switch.normal()

        pie_conf = [self.explode, self.shadow, self.inapp]
        if self.chart_type != 'pie':
            for conf in pie_conf: conf.disabled()
        else:
            for conf in pie_conf: conf.normal()

    def alpha_choser(self):
        num = self.alpha.get()
        if num: return float(num)
        else: return 0

    def plot_color_choser(self):
        self.plot_colors = []
        rgb_name, plot_color = askcolor('blue')
        self.plot_colors.append(plot_color)
        self.plot_colors_btn.config(background=plot_color)

    def plot_linewidth_choser(self):
        num = self.linewidth.get()
        if num: return float(num)
        else: return 0

    def inapp_info(self):
        if self.inapp.get(): PRMP_MsgBox(title='Under Testing', message='Using Pie in Inapp will distrupt the other chart drawing', _type='warn', delay=0)

    def get(self):
        chart = self.chart_types.get()
        if not chart: PRMP_MsgBox(self, title='Chart Type Error', message='Choose a valid chart type.', _type='error', delay=3000)

        results = dict(figNum=int(self.fig.get()), chart=chart)

        if self.grid_style.T.get():
            grid_style = self.grid_style.get().lower()
            if not grid_style: PRMP_MsgBox(self, title='Grid Style Error', message='Choose a valid grid style.', _type='error', delay=3000)

            grid = dict(ls=grid_style, lw=self.grid_width.get(), c=self._grid_color)
            results['grid'] = grid

        if chart == 'Plot':
            results['marker'] = self.marker.get()
            results['linestyle'] = self.linestyle.get()
            results['linewidth'] = self.linewidth.get()
            results['alpha'] = self.alpha.get()
        elif chart == 'Pie':
            results['inapp'] = self.inapp.get()
            results['explode'] = self.explode.get()
            results['shadow'] = self.shadow.get()

        results['switch'] = self.switch.get()

        return results











