from ..core.agam_extensions import *
from ..core.prmp_gui.two_widgets import *
from ...backend.dc.dc_regions import Client

class DC_Digits(FillWidgets, Frame):
    
    def __init__(self, master, values={}, **kwargs):
        Frame.__init__(self, master, **kwargs)
        FillWidgets.__init__(self, values)
        font = self.DEFAULT_FONT
        font['size'] = 20
     # Incomes
        self._incomes = incomes = LabelFrame(self, text='Incomes')
        Label(incomes, text='Savings', place=dict(relx=.03, rely=.27, relh=.21, relw=.48))
        Label(incomes, text='Transfers', place=dict(relx=.03, rely=.51, relh=.21, relw=.48))
        Label(incomes, text='Commissions', place=dict(relx=.03, rely=.74, relh=.21, relw=.48))

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

        self.balances = Entry_Label(balances, text='₦ 1,080,000', place=dict(relx=.03, rely=0, relh=.18, relw=.94), font=font)
        self.broughts = Entry_Label(balances, text='₦ 500,000br', place=dict(relx=.53, rely=.2, relh=.18, relw=.44))
        self.btos = Entry_Label(balances, text='₦ 30,000bto', place=dict(relx=.53, rely=.4, relh=.18, relw=.44))
        self.deficits = Entry_Label(balances, text='₦ 30,000def', place=dict(relx=.53, rely=.6, relh=.18, relw=.44))
        self.excesses = Entry_Label(balances, text='₦ 30,000exc', place=dict(relx=.53, rely=.8, relh=.18, relw=.44))

        self.addResultsWidgets(['incomes', 'savings', 'debits', 'withdrawals', 'paidouts', 'upfronts', 'repaid', 'overdue', 'balances', 'broughts', 'commissions', 'btos', 'transfers', 'deficits', 'excesses'])

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
            broughts=int(account.broughtForwards))
        
        if not isinstance(account.region, Client):
            not_client = dict(
                commissions=int(account.commissions),
                btos=int(account.btos),
                transfers=int(account.transfers),
                deficits=int(account.deficits),
                excesses=int(account.excesses))
            fillDict.update(not_client)
        
        for key in fillDict:
            val = fillDict[key]
            new_val = self.numWithSign_Commas(val)
            fillDict[key] = new_val
            

        self.fill(fillDict)


class DC_Overview(Frame):
    
    def __init__(self, master, title='DC Overview', orient='v', **kwargs):
        super().__init__(master, title=title, **kwargs)
        
        self.dcDigits = DC_Digits(self, relief='groove')

        self.plotDialog = Button(self, text='Plot Dialog')

        self.plotCanvas1 = FramedCanvas(self, relief='groove', canvasConfig=dict(background="yellow", borderwidth="2"))

        self.plotCanvas2 = FramedCanvas(self, relief='groove', canvasConfig=dict(background="yellow", borderwidth="2"))

        if orient == 'v': self.placeVertically()
        else: self.placeHorizontally()
    
    def placeVertically(self):
        x, y = self.toplevel.geo

        self.dcDigits.place(relx=0, rely=0, relh=1, relw=.369)
        self.plotDialog.place(relx=.85, y=0, relw=.15, relh=.04)
        self.dcDigits.placeVertically()
        self.plotCanvas1.place(relx=.375, rely=.04, relh=.48, relw=.625)
        self.plotCanvas2.place(relx=.375, rely=.52, relh=.48, relw=.625)


    def placeHorizontally(self):
        self.dcDigits.place(relx=0, rely=0, relh=.28, relw=1)
        self.dcDigits.placeHorizontally()
        self.plotDialog.place(relx=.425, rely=.285, relh=.04, relw=.15)
        self.plotCanvas1.place(relx=0, rely=.33, relh=.67, relw=.5)
        self.plotCanvas2.place(relx=.5, rely=.33, relh=.67, relw=.5)
    
    def updateDCDigits(self, account): self.dcDigits.update(account)


class SupDCDetails(FillWidgets, LabelFrame):
    def __init__(self, master, text='Details', region=None, **kwargs):
        LabelFrame.__init__(self, master, text=text, **kwargs)

        self.region = region
        FillWidgets.__init__(self, self.derivedValues)
        
        self.persons = LabelButton(self, topKwargs=dict(config=dict(text='Persons')), place=dict(relx=.02, rely=0, relh=.35, relw=.2), orient='h', longent=.5)

        self.subs = LabelButton(self, topKwargs=dict(config=dict(text='Total Subs', anchor='center')), place=dict(relx=.02, rely=.4, relh=.35, relw=.25), orient='h', longent=.55)

        self.actSubs = LabelButton(self, topKwargs=dict(config=dict(text='Active Subs', anchor='center')), place=dict(relx=.3, rely=0, relh=.35, relw=.3), orient='h')

        self.accounts = LabelButton(self, topKwargs=dict(config=dict(text='Total Accounts', anchor='center')), place=dict(relx=.3, rely=.4, relh=.35, relw=.3), orient='h', longent=.65)
        
        self.actSubsAccs = LabelButton(self, topKwargs=dict(config=dict(text='Active Subs Accounts', anchor='center')), place=dict(relx=.62, rely=0, relh=.35, relw=.32), orient='h', longent=.65)

        Button(self, place=dict(relx=.65, rely=.632, h=28, w=119), text='Object Details', command=self.openObjDet)

        Button(self, place=dict(relx=.795, rely=.632, h=28, w=119), text='Search', command=self.openSNS)

        self.sns = None
        self.objdet = None
    
    def derivedValues(self):
        values = dict(
            persons=self.region.personsManager.totalSubs
            subs=self.region.
            actSubs=self.region.
            accounts=self.region.
            actSubsAccs=self.region.
        )
    
    def openSNS(self):
        if self.sns: self.sns.topmost()
        self.sns = SortNSearch(self, sup=self.region)
        self.sns.mainloop()
    
    def openObjDet(self):
        if self.objdet: self.objdet.topmost()
        self.objdet = ObjectDetails(self, sup=self.region)
        self.objdet.mainloop()



















