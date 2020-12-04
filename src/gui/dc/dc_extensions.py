from ..core.prmp_gui.extensions import *


class DC_Digits(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    # Incomes
        self.incomes = LabelFrame(self, text='Incomes')
        self.incomes.place(relx=.02, rely=.008, relh=.256, relw=.96)

        self.incomesS = Label(self.incomes, text='₦ 3,000,000i', asEntry=True)
        self.incomesS.place(relx=.03, rely=0, relh=.24, relw=.94)

        self.savings = Label(self.incomes, text='Savings')
        self.savings.place(relx=.03, rely=.27, relh=.21, relw=.48)

        self.savingsS = Label(self.incomes, text='₦ 50,000s', asEntry=True)
        self.savingsS.place(relx=.53, rely=.27, relh=.21, relw=.44)

        self.transfers = Label(self.incomes, text='Transfers')
        self.transfers.place(relx=.03, rely=.51, relh=.21, relw=.48)

        self.transfersS = Label(self.incomes, text='₦ 30,000tr', asEntry=True)
        self.transfersS.place(relx=.53, rely=.51, relh=.21, relw=.44)

        self.commissions = Label(self.incomes, text='Commissions')
        self.commissions.place(relx=.03, rely=.74, relh=.21, relw=.48)

        self.commissionsS = Label(self.incomes, text='₦ 30,000c', asEntry=True)
        self.commissionsS.place(relx=.53, rely=.74, relh=.22, relw=.44)

    # Debits
        self.debits = LabelFrame(self, text='Debits')
        self.debits.place(relx=.02, rely=.267, relh=.21, relw=.96)

        self.debitsS = Label(self.debits, text='₦ 80,000d', asEntry=True)
        self.debitsS.place(relx=.03, rely=0, relh=.32, relw=.94)

        self.withdrawals = Label(self.debits, text='Withdrawals')
        self.withdrawals.place(relx=.03, rely=.35, relh=.3, relw=.48)

        self.withdrawalsS = Label(self.debits, text='₦ 50,000w', asEntry=True)
        self.withdrawalsS.place(relx=.53, rely=.35, relh=.3, relw=.44)

        self.paidouts = Label(self.debits, text='Paidouts')
        self.paidouts.place(relx=.03, rely=.68, relh=.28, relw=.48)

        self.paidoutsS = Label(self.debits, text='₦ 30,000p', asEntry=True)
        self.paidoutsS.place(relx=.53, rely=.68, relh=.28, relw=.44)

    # Upfronts
        self.upfronts = LabelFrame(self, text='Upfronts')
        self.upfronts.place(relx=.02, rely=.48, relh=.198, relw=.96)

        self.upfrontsS = Label(self.upfronts, text='₦ 980,000up', asEntry=True)
        self.upfrontsS.place(relx=.03, rely=.05, relh=.32, relw=.94)

        self.repaid = Label(self.upfronts, text='Repaid')
        self.repaid.place(relx=.03, rely=.4, relh=.25, relw=.48)

        self.repaidS = Label(self.upfronts, text='₦ 850,000r', asEntry=True)
        self.repaidS.place(relx=.53, rely=.4, relh=.25, relw=.44)

        self.overdue = Label(self.upfronts, text='Overdue')
        self.overdue.place(relx=.03, rely=.7, relh=.25, relw=.48)

        self.overdueS = Label(self.upfronts, text='₦ 130,000ov', asEntry=True)
        self.overdueS.place(relx=.53, rely=.7, relh=.25, relw=.44)

    # Balances
        self.balances = LabelFrame(self, text='Balances')
        self.balances.place(relx=.02, rely=.68, relh=.312, relw=.96)

        self.balancesS = Label(self.balances, text='₦ 1,080,000', asEntry=True)
        self.balancesS.place(relx=.03, rely=0, relh=.18, relw=.94)

        self.broughts = Label(self.balances, text='Brought-Fs')
        self.broughts.place(relx=.03, rely=.2, relh=.18, relw=.48)

        self.broughtsS = Label(self.balances, text='₦ 500,000br', asEntry=True)
        self.broughtsS.place(relx=.53, rely=.2, relh=.18, relw=.44)

        self.btos = Label(self.balances, text='B-T-Os')
        self.btos.place(relx=.03, rely=.4, relh=.18, relw=.48)

        self.btosS = Label(self.balances, text='₦ 30,000bto', asEntry=True)
        self.btosS.place(relx=.53, rely=.4, relh=.18, relw=.44)

        self.deficits = Label(self.balances, text='Deficits')
        self.deficits.place(relx=.03, rely=.6, relh=.18, relw=.48)

        self.deficitsS = Label(self.balances, text='₦ 30,000def', asEntry=True)
        self.deficitsS.place(relx=.53, rely=.6, relh=.18, relw=.44)

        self.excesses = Label(self.balances, text='Excesses')
        self.excesses.place(relx=.03, rely=.8, relh=.18, relw=.48)

        self.excessesS = Label(self.balances, text='₦ 30,000exc', asEntry=True)
        self.excessesS.place(relx=.53, rely=.8, relh=.14, relw=.44)

class DC_Overview(Frame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        
        self.plotCanvas1 = FramedCanvas(self, relief='groove', canvasConfig=dict(background="yellow", borderwidth="2"))
        self.plotCanvas1.place(relx=.375, rely=0, relh=.5, relw=.625)

        self.plotCanvas2 = FramedCanvas(self, relief='groove', canvasConfig=dict(background="yellow", borderwidth="2"))
        self.plotCanvas2.place(relx=.375, rely=.5, relh=.5, relw=.625)


        self.dcDigits = DC_Digits(self, relief='groove')
        self.dcDigits.place(relx=0, rely=0, relh=1, relw=.369)



