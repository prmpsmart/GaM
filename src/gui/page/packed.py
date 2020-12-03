from ..core.prmp_gui.core import *


class FramedCanvas(tk.Frame):
    def __init__(self, master, canvasConfig={}, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, **canvasConfig)
        self.canvas.place(relx=0.012, rely=0.017, relh=0.966, relw=0.976)

class DC_Digits(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.incomes = tk.LabelFrame(self, relief='groove', font="-family {Times New Roman} -size 11 -weight bold", foreground="black", text='Incomes', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        self.incomes.place(relx=0.02, rely=0.008, relh=0.248, relw=0.96)

        self.incomesS = tk.Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 14 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 3,000,000i')
        self.incomesS.place(relx=0.041, rely=0.134, h=33, w=223, bordermode='ignore')

        self.savings = tk.Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Savings')
        self.savings.place(relx=0.041, rely=0.403, h=23, w=113, bordermode='ignore')

        self.savingsS = tk.Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 50,000s')
        self.savingsS.place(relx=0.576, rely=0.403, h=23, w=93, bordermode='ignore')

        self.transfers = tk.Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Transfers')
        self.transfers.place(relx=0.041, rely=0.604, h=23, w=113, bordermode='ignore')

        self.transfersS = tk.Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000tr')
        self.transfersS.place(relx=0.576, rely=0.57, h=23, w=93, bordermode='ignore')

        self.commissions = tk.Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Commissions')
        self.commissions.place(relx=0.041, rely=0.772, h=23, w=113, bordermode='ignore')

        self.commissions = tk.Label(self.incomes, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000c')
        self.commissions.place(relx=0.576, rely=0.772, h=23, w=93, bordermode='ignore')

        self.Labelframe1_6 = tk.LabelFrame(self, relief='groove', font="-family {Times New Roman} -size 11 -weight bold", foreground="black", text='Debits', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        self.Labelframe1_6.place(relx=0.02, rely=0.258, relh=0.205, relw=0.96)

        self.Label1_4 = tk.Label(self.Labelframe1_6, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Withdrawals')
        self.Label1_4.place(relx=0.041, rely=0.488, h=23, w=113, bordermode='ignore')

        self.Label2_1 = tk.Label(self.Labelframe1_6, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 50,000')
        self.Label2_1.place(relx=0.576, rely=0.488, h=23, w=93, bordermode='ignore')

        self.Label1_2 = tk.Label(self.Labelframe1_6, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Paidouts')
        self.Label1_2.place(relx=0.041, rely=0.732, h=23, w=113, bordermode='ignore')

        self.Label2_3 = tk.Label(self.Labelframe1_6, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000')
        self.Label2_3.place(relx=0.576, rely=0.732, h=23, w=93, bordermode='ignore')

        self.Label2_8 = tk.Label(self.Labelframe1_6, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 14 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 80,000')
        self.Label2_8.place(relx=0.041, rely=0.163, h=33, w=223, bordermode='ignore')

        self.Labelframe1_4 = tk.LabelFrame(self, relief='groove', font="-family {Times New Roman} -size 11 -weight bold", foreground="black", text='Upfronts', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        self.Labelframe1_4.place(relx=0.02, rely=0.474, relh=0.198, relw=0.96)

        self.Label1_3 = tk.Label(self.Labelframe1_4, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Repaid')
        self.Label1_3.place(relx=0.041, rely=0.462, h=23, w=113, bordermode='ignore')

        self.Label2_4 = tk.Label(self.Labelframe1_4, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 850,000')
        self.Label2_4.place(relx=0.576, rely=0.462, h=23, w=93, bordermode='ignore')

        self.Label1_7 = tk.Label(self.Labelframe1_4, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Overdue')
        self.Label1_7.place(relx=0.041, rely=0.714, h=23, w=113, bordermode='ignore')

        self.Label2_9 = tk.Label(self.Labelframe1_4, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 130,000')
        self.Label2_9.place(relx=0.576, rely=0.714, h=23, w=93, bordermode='ignore')

        self.Label2_5 = tk.Label(self.Labelframe1_4, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 14 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 980,000')
        self.Label2_5.place(relx=0.041, rely=0.168, h=33, w=223, bordermode='ignore')

        self.Labelframe1_8 = tk.LabelFrame(self, relief='groove', font="-family {Times New Roman} -size 11 -weight bold", foreground="black", text='Balances', background="#d9d9d9", highlightbackground="#d9d9d9", highlightcolor="black")
        self.Labelframe1_8.place(relx=0.02, rely=0.674, relh=0.304, relw=0.96)

        self.Label2_6 = tk.Label(self.Labelframe1_8, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 500,000')
        self.Label2_6.place(relx=0.576, rely=0.328, h=23, w=93, bordermode='ignore')

        self.Label2_10 = tk.Label(self.Labelframe1_8, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000')
        self.Label2_10.place(relx=0.576, rely=0.492, h=23, w=93, bordermode='ignore')

        self.Label2_7 = tk.Label(self.Labelframe1_8, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 14 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 1,080,000')
        self.Label2_7.place(relx=0.041, rely=0.109, h=33, w=223, bordermode='ignore')

        self.Label1_8 = tk.Label(self.Labelframe1_8, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='B-T-Os')
        self.Label1_8.place(relx=0.041, rely=0.492, h=23, w=113, bordermode='ignore')

        self.Label1_9 = tk.Label(self.Labelframe1_8, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Deficits')
        self.Label1_9.place(relx=0.041, rely=0.656, h=23, w=113, bordermode='ignore')

        self.Label1_9 = tk.Label(self.Labelframe1_8, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Excesses')
        self.Label1_9.place(relx=0.041, rely=0.82, h=23, w=113, bordermode='ignore')

        self.Label2_11 = tk.Label(self.Labelframe1_8, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000')
        self.Label2_11.place(relx=0.576, rely=0.656, h=23, w=93, bordermode='ignore')

        self.Label1_10 = tk.Label(self.Labelframe1_8, activebackground="#f9f9f9", activeforeground="black", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", relief="groove", text='Brought-Fs')
        self.Label1_10.place(relx=0.041, rely=0.328, h=23, w=113, bordermode='ignore')

        self.Label2_11 = tk.Label(self.Labelframe1_8, activebackground="#f9f9f9", activeforeground="black", anchor='ne', background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", justify='left', relief="sunken", text='₦ 30,000')
        self.Label2_11.place(relx=0.576, rely=0.82, h=23, w=93, bordermode='ignore')












