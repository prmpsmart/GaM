from ..core.prmp_gui.extensions import *

class DC_Digits(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    # Incomes
        incomes = LabelFrame(self, text='Incomes', place=dict(relx=.02, rely=.008, relh=.256, relw=.96))
        Label(incomes, text='Savings', place=dict(relx=.03, rely=.27, relh=.21, relw=.48))
        Label(incomes, text='Transfers', place=dict(relx=.03, rely=.51, relh=.21, relw=.48))
        Label(incomes, text='Commissions', place=dict(relx=.03, rely=.74, relh=.21, relw=.48))

        self.incomes = Entry_Label(incomes, text='₦ 3,000,000i', place=dict(relx=.03, rely=0, relh=.24, relw=.94))
        self.savings = Entry_Label(incomes, text='₦ 50,000s', place=dict(relx=.53, rely=.27, relh=.21, relw=.44))
        self.transfersS = Entry_Label(incomes, text='₦ 30,000tr', place=dict(relx=.53, rely=.51, relh=.21, relw=.44))
        self.commissionsS = Entry_Label(incomes, text='₦ 30,000c', place=dict(relx=.53, rely=.74, relh=.22, relw=.44))

    # Debits
        debits = LabelFrame(self, text='Debits', place=dict(relx=.02, rely=.267, relh=.21, relw=.96))
        Label(debits, text='Withdrawals', place=dict(relx=.03, rely=.35, relh=.3, relw=.48))
        Label(debits, text='Paidouts', place=dict(relx=.03, rely=.68, relh=.28, relw=.48))

        self.debitsS = Entry_Label(debits, text='₦ 80,000d', place=dict(relx=.03, rely=0, relh=.32, relw=.94))
        self.withdrawalsS = Entry_Label(debits, text='₦ 50,000w', place=dict(relx=.53, rely=.35, relh=.3, relw=.44))
        self.paidoutsS = Entry_Label(debits, text='₦ 30,000p', place=dict(relx=.53, rely=.68, relh=.28, relw=.44))

    # Upfronts
        upfronts = LabelFrame(self, text='Upfronts', place=dict(relx=.02, rely=.48, relh=.198, relw=.96))
        Label(upfronts, text='Repaid', place=dict(relx=.03, rely=.4, relh=.25, relw=.48))
        Label(upfronts, text='Overdue', place=dict(relx=.03, rely=.7, relh=.25, relw=.48))

        self.upfronts = Entry_Label(upfronts, text='₦ 980,000up', place=dict(relx=.03, rely=.05, relh=.32, relw=.94))
        self.repaid = Entry_Label(upfronts, text='₦ 850,000r', place=dict(relx=.53, rely=.4, relh=.25, relw=.44))
        self.overdue = Entry_Label(upfronts, text='₦ 130,000ov', place=dict(relx=.53, rely=.7, relh=.25, relw=.44))

    # Balances
        balances = LabelFrame(self, text='Balances', place=dict(relx=.02, rely=.68, relh=.312, relw=.96))
        Label(balances, text='Brought-Fs', place=dict(relx=.03, rely=.2, relh=.18, relw=.48))
        Label(balances, text='B-T-Os', place=dict(relx=.03, rely=.4, relh=.18, relw=.48))
        Label(balances, text='Deficits', place=dict(relx=.03, rely=.6, relh=.18, relw=.48))
        Label(balances, text='Excesses', place=dict(relx=.03, rely=.8, relh=.18, relw=.48))

        self.balances = Entry_Label(balances, text='₦ 1,080,000', place=dict(relx=.03, rely=0, relh=.18, relw=.94))
        self.broughts = Entry_Label(balances, text='₦ 500,000br', place=dict(relx=.53, rely=.2, relh=.18, relw=.44))
        self.btos = Entry_Label(balances, text='₦ 30,000bto', place=dict(relx=.53, rely=.4, relh=.18, relw=.44))
        self.deficits = Entry_Label(balances, text='₦ 30,000def', place=dict(relx=.53, rely=.6, relh=.18, relw=.44))
        self.excesses = Entry_Label(balances, text='₦ 30,000exc', place=dict(relx=.53, rely=.8, relh=.14, relw=.44))

class DC_Overview(Frame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        
        self.plotCanvas1 = FramedCanvas(self, relief='groove', canvasConfig=dict(background="yellow", borderwidth="2"))
        self.plotCanvas1.place(relx=.375, rely=0, relh=.5, relw=.625)

        self.plotCanvas2 = FramedCanvas(self, relief='groove', canvasConfig=dict(background="yellow", borderwidth="2"))
        self.plotCanvas2.place(relx=.375, rely=.5, relh=.5, relw=.625)


        self.dcDigits = DC_Digits(self, relief='groove')
        self.dcDigits.place(relx=0, rely=0, relh=1, relw=.369)



