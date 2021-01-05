from ..core.agam_apps import *
from ...backend.dc.dc_regions import *
from ...backend.dc.dc_specials import *
from prmp_gui.plot_canvas import PRMP_PlotCanvas, random, ChartSort


class DC_ChartSort(ChartSort): pass


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
        self._debits = debits = LabelFrame(self, text='Debits')
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
        self._debits.place(relx=.02, rely=.267, relh=.21, relw=.96)
        self._upfronts.place(relx=.02, rely=.48, relh=.198, relw=.96)
        self._balances.place(relx=.02, rely=.68, relh=.312, relw=.96)

    def placeHorizontally(self):
        self._incomes.place(relx=0, rely=0, relh=1, relw=.25)
        self._debits.place(relx=.25, rely=0, relh=1, relw=.25)
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
    
    def __init__(self, master, title='DC Overview', orient='v', region=None, account=None, **kwargs):
        super().__init__(master, title=title, **kwargs)
        self.region = region
        self.account = region.lastAccount if region else account

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
        self.month.set(self.formatMonth(account.date))
        if isinstance(account.region, Client): self.ledgerNumber.set(account.ledgerNumber)
        self.dcDigits.update(account)
    
    def formatMonth(self, month): return f'{month.monthName} {month.year}'

    def next(self):
        if not self.account: return
        print(self.account)
        _next = self.account.next
        if _next: self.updateDCDigits(_next)

    def prev(self):
        if not self.account: return
        _prev = self.account.previous
        if _prev: self.updateDCDigits(_prev)


class NewThrift(PRMP_FillWidgets, Frame):
    def __init__(self, master=None, thrift=None, manager=None, callback=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self, thrift)

        self.thrift = thrift
        self.manager = manager

        self.ledgerNumber = LabelEntry(self, topKwargs=dict(config=dict(text='Ledger Number')), bottomKwargs=dict(_type='number'), place=dict(relx=.005, rely=.005, relh=.18, relw=.99), orient='h', longent=.46)

        self.monthYear = LabelMonthYearButton(self, topKwargs=dict(config=dict(text='Month-Year')), place=dict(relx=.005, rely=.18, relh=.18, relw=.99), orient='h', longent=.46)

        self.income = LabelEntry(self, topKwargs=dict(config=dict(text='Income')), bottomKwargs=dict(_type='money'), place=dict(relx=.005, rely=.36, relh=.18, relw=.5), orient='h', longent=.5)
        self.money = Checkbutton(self, text='Money?', place=dict(relx=.52, rely=.37, relh=.13, relw=.23))
        self.transfer = Checkbutton(self, text='Transfer?', place=dict(relx=.76, rely=.37, relh=.13, relw=.24))

        self.debit = LabelEntry(self, topKwargs=dict(config=dict(text='Debit')), bottomKwargs=dict(_type='money', default=0), orient='h', place=dict(relx=.005, rely=.54, relh=.18, relw=.6))
        self.paidout = Checkbutton(self, text='Paidout?', place=dict(relx=.62, rely=.555, relh=.13, relw=.235))

        self.date = LabelDateButton(self, topKwargs=dict(config=dict(text='Date')), place=dict(relx=.005, rely=.73, relh=.18, relw=.6), orient='h', longent=.46)



class ThriftDetail(Frame):
    def __init__(self, master=None, thrift=None, manager=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self, thrift)

        self.thrift = thrift
        self.manager = manager

        self.contributed = None
        self.income = None
        self.debit = None
        self.paidout = None
        self.transfer = None

        self.upfrontRepay = None
        self.show_debRecord = None
        self.show_contRecord = None
        self.updateBtn = None

        self.date = None



















