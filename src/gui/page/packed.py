from ..core.prmp_gui.extensions import *
from tkinter import *


class DC_Digits(Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
    # Incomes
        self.incomes = LabelFrame(self, relief='groove', font="-family {Times New Roman} -size 11 -weight bold", foreground="black", text='Incomes', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        self.incomes.place(relx=.02, rely=.008, relh=.248, relw=.96)

        self.incomesS = Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 14 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 3,000,000i')
        self.incomesS.place(relx=.03, rely=.134, relh=.225, relw=.94, bordermode='ignore')

        self.savings = Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Savings')
        self.savings.place(relx=.03, rely=.403, relh=.17, relw=.48, bordermode='ignore')

        self.savingsS = Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 50,000s')
        self.savingsS.place(relx=.53, rely=.403, relh=.17, relw=.44, bordermode='ignore')

        self.transfers = Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Transfers')
        self.transfers.place(relx=.03, rely=.604, relh=.17, relw=.48, bordermode='ignore')

        self.transfersS = Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000tr')
        self.transfersS.place(relx=.53, rely=.604, relh=.17, relw=.44, bordermode='ignore')

        self.commissions = Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Commissions')
        self.commissions.place(relx=.03, rely=.8, relh=.17, relw=.48, bordermode='ignore')

        self.commissionsS = Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000c')
        self.commissionsS.place(relx=.53, rely=.8, relh=.17, relw=.44, bordermode='ignore')

    # Debits
        self.debits = LabelFrame(self, relief='groove', font="-family {Times New Roman} -size 11 -weight bold", foreground="black", text='Debits', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        self.debits.place(relx=.02, rely=.267, relh=.205, relw=.96)

        self.debitsS = Label(self.debits, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 14 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 80,000d')
        self.debitsS.place(relx=.03, rely=.163, relh=.27, relw=.94, bordermode='ignore')

        self.withdrawals = Label(self.debits, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Withdrawals')
        self.withdrawals.place(relx=.03, rely=.488, relh=.2, relw=.48, bordermode='ignore')

        self.withdrawalsS = Label(self.debits, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 50,000w')
        self.withdrawalsS.place(relx=.53, rely=.488, relh=.2, relw=.44, bordermode='ignore')

        self.paidouts = Label(self.debits, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Paidouts')
        self.paidouts.place(relx=.03, rely=.732, relh=.2, relw=.48, bordermode='ignore')

        self.paidoutsS = Label(self.debits, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000p')
        self.paidoutsS.place(relx=.53, rely=.732, relh=.2, relw=.44, bordermode='ignore')

    # Upfronts
        self.upfronts = LabelFrame(self, relief='groove', font="-family {Times New Roman} -size 11 -weight bold", foreground="black", text='Upfronts', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        self.upfronts.place(relx=.02, rely=.48, relh=.198, relw=.96)

        self.upfrontsS = Label(self.upfronts, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 14 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 980,000up')
        self.upfrontsS.place(relx=.03, rely=.168, relh=.27, relw=.94, bordermode='ignore')

        self.repaid = Label(self.upfronts, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Repaid')
        self.repaid.place(relx=.03, rely=.48, relh=.22, relw=.48, bordermode='ignore')

        self.repaidS = Label(self.upfronts, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 850,000r')
        self.repaidS.place(relx=.53, rely=.48, relh=.22, relw=.44, bordermode='ignore')

        self.overdue = Label(self.upfronts, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Overdue')
        self.overdue.place(relx=.03, rely=.745, relh=.22, relw=.48, bordermode='ignore')

        self.overdueS = Label(self.upfronts, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 130,000ov')
        self.overdueS.place(relx=.53, rely=.745, relh=.22, relw=.44, bordermode='ignore')

    # Balances
        self.balances = LabelFrame(self, relief='groove', font="-family {Times New Roman} -size 11 -weight bold", foreground="black", text='Balances', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        self.balances.place(relx=.02, rely=.69, relh=.304, relw=.96)

        self.balancesS = Label(self.balances, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 14 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 1,080,000')
        self.balancesS.place(relx=.03, rely=.109, relh=.18, relw=.94, bordermode='ignore')

        self.broughts = Label(self.balances, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Brought-Fs')
        self.broughts.place(relx=.03, rely=.328, relh=.14, relw=.48, bordermode='ignore')

        self.broughtsS = Label(self.balances, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 500,000br')
        self.broughtsS.place(relx=.53, rely=.328, relh=.14, relw=.44, bordermode='ignore')

        self.btos = Label(self.balances, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='B-T-Os')
        self.btos.place(relx=.03, rely=.492, relh=.14, relw=.48, bordermode='ignore')

        self.btosS = Label(self.balances, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000bto')
        self.btosS.place(relx=.53, rely=.492, relh=.14, relw=.44, bordermode='ignore')

        self.deficits = Label(self.balances, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Deficits')
        self.deficits.place(relx=.03, rely=.656, relh=.14, relw=.48, bordermode='ignore')

        self.deficitsS = Label(self.balances, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000def')
        self.deficitsS.place(relx=.53, rely=.656, relh=.14, relw=.44, bordermode='ignore')

        self.excesses = Label(self.balances, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Excesses')
        self.excesses.place(relx=.03, rely=.82, relh=.14, relw=.48, bordermode='ignore')

        self.excessesS = Label(self.balances, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000exc')
        self.excessesS.place(relx=.53, rely=.82, relh=.14, relw=.44, bordermode='ignore')

class DC_Overview(Frame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        
        self.plotCanvas1 = FramedCanvas(self, relief='groove', borderwidth="2", background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black", canvasConfig=dict(background="white", borderwidth="2", highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black", relief="groove", selectbackground="#c4c4c4", selectforeground="black"))
        self.plotCanvas1.place(relx=.375, rely=0, relh=.5, relw=.625)

        self.plotCanvas2 = FramedCanvas(self, relief='groove', borderwidth="2", background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black", canvasConfig=dict(background="white", borderwidth="2", highlightbackground="#d9d9d9", highlightcolor="black", insertbackground="black", relief="groove", selectbackground="#c4c4c4", selectforeground="black"))
        self.plotCanvas2.place(relx=.375, rely=.5, relh=.5, relw=.625)


        self.dcDigits = DC_Digits(self, relief='groove', borderwidth="2", background="#d9d9d9")
        self.dcDigits.place(relx=0, rely=0, relh=1, relw=.369)










