from ..core.prmp_gui.extensions import *


class DC_Digits(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    # Incomes
        self.incomes = LabelFrame(self, text='Incomes')
        self.incomes.place(relx=.02, rely=.008, relh=.248, relw=.96)

        self.incomesS = Label(self.incomes, text='₦ 3,000,000i')
        self.incomesS.place(relx=.03, rely=.134, relh=.225, relw=.94, bordermode='ignore')

        self.savings = Label(self.incomes, text='Savings')
        self.savings.place(relx=.03, rely=.403, relh=.17, relw=.48, bordermode='ignore')

        self.savingsS = Label(self.incomes, text='₦ 50,000s')
        self.savingsS.place(relx=.53, rely=.403, relh=.17, relw=.44, bordermode='ignore')

        self.transfers = Label(self.incomes, text='Transfers')
        self.transfers.place(relx=.03, rely=.604, relh=.17, relw=.48, bordermode='ignore')

        self.transfersS = Label(self.incomes, text='₦ 30,000tr')
        self.transfersS.place(relx=.53, rely=.604, relh=.17, relw=.44, bordermode='ignore')

        self.commissions = Label(self.incomes, text='Commissions')
        self.commissions.place(relx=.03, rely=.8, relh=.17, relw=.48, bordermode='ignore')

        self.commissionsS = Label(self.incomes, text='₦ 30,000c')
        self.commissionsS.place(relx=.53, rely=.8, relh=.17, relw=.44, bordermode='ignore')

    # Debits
        self.debits = LabelFrame(self, text='Debits')
        self.debits.place(relx=.02, rely=.267, relh=.205, relw=.96)

        self.debitsS = Label(self.debits, text='₦ 80,000d')
        self.debitsS.place(relx=.03, rely=.163, relh=.27, relw=.94, bordermode='ignore')

        self.withdrawals = Label(self.debits, text='Withdrawals')
        self.withdrawals.place(relx=.03, rely=.488, relh=.2, relw=.48, bordermode='ignore')

        self.withdrawalsS = Label(self.debits, text='₦ 50,000w')
        self.withdrawalsS.place(relx=.53, rely=.488, relh=.2, relw=.44, bordermode='ignore')

        self.paidouts = Label(self.debits, text='Paidouts')
        self.paidouts.place(relx=.03, rely=.732, relh=.2, relw=.48, bordermode='ignore')

        self.paidoutsS = Label(self.debits, text='₦ 30,000p')
        self.paidoutsS.place(relx=.53, rely=.732, relh=.2, relw=.44, bordermode='ignore')

    # Upfronts
        self.upfronts = LabelFrame(self, text='Upfronts')
        self.upfronts.place(relx=.02, rely=.48, relh=.198, relw=.96)

        self.upfrontsS = Label(self.upfronts, text='₦ 980,000up')
        self.upfrontsS.place(relx=.03, rely=.168, relh=.27, relw=.94, bordermode='ignore')

        self.repaid = Label(self.upfronts, text='Repaid')
        self.repaid.place(relx=.03, rely=.48, relh=.22, relw=.48, bordermode='ignore')

        self.repaidS = Label(self.upfronts, text='₦ 850,000r')
        self.repaidS.place(relx=.53, rely=.48, relh=.22, relw=.44, bordermode='ignore')

        self.overdue = Label(self.upfronts, text='Overdue')
        self.overdue.place(relx=.03, rely=.745, relh=.22, relw=.48, bordermode='ignore')

        self.overdueS = Label(self.upfronts, text='₦ 130,000ov')
        self.overdueS.place(relx=.53, rely=.745, relh=.22, relw=.44, bordermode='ignore')

    # Balances
        self.balances = LabelFrame(self, text='Balances')
        self.balances.place(relx=.02, rely=.69, relh=.304, relw=.96)

        self.balancesS = Label(self.balances, text='₦ 1,080,000')
        self.balancesS.place(relx=.03, rely=.109, relh=.18, relw=.94, bordermode='ignore')

        self.broughts = Label(self.balances, text='Brought-Fs')
        self.broughts.place(relx=.03, rely=.328, relh=.14, relw=.48, bordermode='ignore')

        self.broughtsS = Label(self.balances, text='₦ 500,000br')
        self.broughtsS.place(relx=.53, rely=.328, relh=.14, relw=.44, bordermode='ignore')

        self.btos = Label(self.balances, text='B-T-Os')
        self.btos.place(relx=.03, rely=.492, relh=.14, relw=.48, bordermode='ignore')

        self.btosS = Label(self.balances, text='₦ 30,000bto')
        self.btosS.place(relx=.53, rely=.492, relh=.14, relw=.44, bordermode='ignore')

        self.deficits = Label(self.balances, text='Deficits')
        self.deficits.place(relx=.03, rely=.656, relh=.14, relw=.48, bordermode='ignore')

        self.deficitsS = Label(self.balances, text='₦ 30,000def')
        self.deficitsS.place(relx=.53, rely=.656, relh=.14, relw=.44, bordermode='ignore')

        self.excesses = Label(self.balances, text='Excesses')
        self.excesses.place(relx=.03, rely=.82, relh=.14, relw=.48, bordermode='ignore')

        self.excessesS = Label(self.balances, text='₦ 30,000exc')
        self.excessesS.place(relx=.53, rely=.82, relh=.14, relw=.44, bordermode='ignore')

class DC_Overview(Frame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        
        self.plotCanvas1 = FramedCanvas(self, relief='groove', borderwidth="2", canvasConfig=dict(background="yellow", borderwidth="2"))
        self.plotCanvas1.place(relx=.375, rely=0, relh=.5, relw=.625)

        self.plotCanvas2 = FramedCanvas(self, relief='groove', borderwidth="2", canvasConfig=dict(background="yellow", borderwidth="2"))
        self.plotCanvas2.place(relx=.375, rely=.5, relh=.5, relw=.625)


        self.dcDigits = DC_Digits(self, relief='groove', borderwidth="2", background="#d9d9d9")
        self.dcDigits.place(relx=0, rely=0, relh=1, relw=.369)


