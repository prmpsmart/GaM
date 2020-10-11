


# Some handy unicode symbols
j = ''
sq = '█'
o = '⚫'
of = '◯'
up = '▲'
r = '►'
l =  '◄'
d =  '▼'
x = '❎'

money = {'naira': 8358, 'dollar': 36, 'euro': 163, 'yen': 165}

def generate():
    f = 'unicode chars.txt'
    tf = 'tkunicode chars.txt'
    f_ = 'unicode each line.txt'
    tf_ = 'tk_unicode each line.txt'

    uni = 0x110000 or 1114112
    tkuni = 65535


    fi = open(f, 'wb')
    fl = open(f_, 'wb')
    tfi = open(tf, 'wb')
    tfl = open(tf_, 'wb')
    for a  in range(uni):
        ch = chr(a) + ' '
        ch_ = chr(a) + '\n'
        try: ch_byt = bytes(ch, 'utf-8')#.encode()
        except: ch_byt = b''
        try: ch__byt = bytes(ch_, 'utf-8')#.encode()
        except: ch__byt = b''
        
        fi.write(ch_byt)
        fl.write(ch__byt)
        
        if a < tkuni + 1:
            tfi.write(ch_byt)
            tfl.write(ch__byt)

stylish_fonts =[(119808, 120831), (127248, 127386), (127462, 127487), (65281, 65510)]
beautiful = [(40960, 42654), (42752, 42935)]
decks_cards = (126976, 127221)
emoticons = [(127744, 129195), (129296, 129510)]
others = [(12272, 13317), (8352, 11623), (6320, 6389), (5130, 5872)]


def c(i): print(chr(i))
def o(i): print(ord(i))


from tkinter import Tk, Label, Button, StringVar, Entry



class UnicodeViewer(Tk):
    def __init__(self):
        super().__init__()
        font13 = "-family {Times New Roman} -size 48 -weight bold "  \
            "-slant roman -underline 0 -overstrike 0"

        self.geometry("336x430")
        self.resizable(0, 0)
        self.title("Unicode Viewer")
        self.attributes('-topmost', 1, '-toolwindow', 1, '-transparentcolor', 'yellow')
        self.configure(background="#d9d9d9")

        
        self.current = 0
        self.maxOrd = 1114112
        self.tkMaxOrd = 65535
        self.minOrd = 0
        
        self.unicode_display = Label(self, background="#d9d9d9", disabledforeground="#a3a3a3", font=font13, foreground="#000000", relief="raised", text=self.c)
        self.unicode_display.place(relx=0.06, rely=0.07, height=163, width=303)

        self.prev = Button(self, activebackground="#ececec", activeforeground="#000000", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='Previous', command=self.prevChar)
        self.prev.place(relx=0.238, rely=0.907, height=28, width=72)

        self.next = Button(self, activebackground="#ececec", activeforeground="#000000", background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black", pady="0", text='Next', command=self.nextChar)
        self.next.place(relx=0.536, rely=0.907, height=28, width=59)

        self.surfEnt = Entry(self, background="white", disabledforeground="#a3a3a3", font="-family {Courier New} -size 10", foreground="#000000", insertbackground="black")
        self.surfEnt.place(relx=0.387, rely=0.814,height=20, relwidth=0.31)
        self.surfEnt.bind('<Return>', self.processSurf)

        self.max = Label(self, background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", text=f'Max = {self.maxOrd}')
        self.max.place(relx=0.06, rely=0.535, height=23, width=109)

        self.min = Label(self, background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", text=f'Min = {self.minOrd}')
        self.min.place(relx=0.089, rely=0.605, height=23, width=58)

        self.cur = Label(self, background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", text='Current')
        self.cur.place(relx=0.595, rely=0.558, height=23, width=58)

        self.currentOrd = Label(self, background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", text=self.current)
        self.currentOrd.place(relx=0.774, rely=0.558, height=23, width=42)

        self.surf = Label(self, background="#d9d9d9", disabledforeground="#a3a3a3", font="-family {Times New Roman} -size 11 -weight bold", foreground="#000000", relief="groove", text='Surf')
        self.surf.place(relx=0.238, rely=0.814, height=23, width=42)
        
        self.after(500, self.nextChar)
        self.mainloop()
    @property
    def c(self): return chr(self.current)
    @property
    def o(self): return self.current
    
    def processSurf(self, e=0):
        pass
    
    def nextChar(self):
        if self.minOrd <= self.current < self.maxOrd:
            self.current += 1
            if self.current >= self.maxOrd: self.current = self.minOrd
            self.process()
        # self.after(5, self.nextChar)

    def prevChar(self):
        if self.minOrd <= self.current < self.maxOrd:
            self.current -= 1
            if self.current <= self.minOrd: self.current = self.maxOrd - 1
            self.process()

    def process(self):
        try: 
            self.unicode_display['text'] = self.c
            self.currentOrd['text'] = self.o
        except Exception as e: print(self.current, e, end=' | ')


UnicodeViewer()
# generate()
