

from tkinter import Label, Button, Entry, Toplevel, IntVar, Checkbutton, messagebox
import os
from .....backend.utils.data.images.images import Images, Path


class Base_Convert:
    def __init__(self):
        self.bin_to_bin = self.bin_to_bin
        self.bin_to_dec = self.bin_to_dec
        self.bin_to_oct = self.bin_to_oct
        self.bin_to_hex = self.bin_to_hex
        self.dec_to_bin = self.dec_to_bin
        self.dec_to_dec = self.dec_to_dec
        self.dec_to_oct = self.dec_to_oct
        self.dec_to_hex = self.dec_to_hex
        self.oct_to_bin = self.oct_to_bin
        self.oct_to_dec = self.oct_to_dec
        self.oct_to_oct = self.oct_to_oct
        self.oct_to_hex = self.oct_to_hex
        self.hex_to_bin = self.hex_to_bin
        self.hex_to_dec = self.hex_to_dec
        self.hex_to_oct = self.hex_to_oct
        self.hex_to_hex = self.hex_to_hex
    
    # ********************* ALL CONVERTING FUNCTIONS START *************************
    # @classmethod
    def bin_to_bin(self, b): return (bin(int(str(b), 2)))[2:]
    # @classmethod
    def bin_to_dec(self, b): return int(str(b), 2)
    # @classmethod
    def bin_to_oct(self, b): return oct(int(str(b), 2))[2:]
    # @classmethod
    def bin_to_hex(self, b): return hex(int(str(b), 2))[2:]
    # @classmethod
    def dec_to_bin(self, d): return bin(int(d))[2:]
    # @classmethod
    def dec_to_dec(self, d): return int(d)
    # @classmethod
    def dec_to_oct(self, d): return oct(int(d))[2:]
    # @classmethod
    def dec_to_hex(self, d): return hex(int(d))[2:]
    # @classmethod
    def oct_to_bin(self, o): return bin(int(str(o), 8))[2:]
    # @classmethod
    def oct_to_dec(self, o): return int(str(o), 8)
    # @classmethod
    def oct_to_oct(self, o): return oct(int(str(o), 8))[2:]
    # @classmethod
    def oct_to_hex(self, o): return hex(int(str(o), 8))[2:]
    # @classmethod
    def hex_to_bin(self, h): return bin(int(str(h), 16))[2:]
    # @classmethod
    def hex_to_dec(self, h): return int(str(h), 16)
    # @classmethod
    def hex_to_oct(self, h): return oct(int(str(h), 16))[2:]
    # @classmethod
    def hex_to_hex(self, h): return hex(int(str(h), 16))[2:]

    # ********************* ALL CONVERTING FUNCTIONS STOP *************************

class Base_Converter(Toplevel):

    def __init__(self):
        super().__init__()
        
        self.file = Path.calc_history()

        Label(self, text="Enter value: ").grid(row=0, sticky='w')
        Label(self, text=" ").grid(row=0, column=1)

        self.entry = Entry(self, bd=3)
        self.entry.grid(row=0, column=1, columnspan=2, ipadx=30, ipady=10)
        
        btn_backspace = Button(self, text="<--", bd=5, relief="groove", bg="#E5EB39", width=15, command=self.backspace).grid(row=0, column=4)
        Button(self, text="RESET", bd=5, relief="groove", bg="#F24B4B",width=15, command=self.reset).grid(row=1, column=4)
        Label(self, text="Convert Base From:").grid(row=2)
        Label(self, text="Convert Base To:").grid(row=2, column=2)
        
        # *************** A ***************
        self.now_a = None
        self.var_a = [IntVar() for _ in range(4)]
        self.ops = ["Binary", "Decimal", "Octal", "Hexa Decimal"]
        self.opsm = ["bin", "dec", "oct", "hex"]
        self.y_a = 3
        self.buttons_a = [Checkbutton(self, text=self.ops[i], variable=self.var_a[i], command=self.cb_a) for i in range(4)]
        for i in range(4): self.buttons_a[i].grid(row=self.y_a+i, sticky='w')

        # *************** A SEPERATES B ***************

        self.now_b = None
        self.var_b = [IntVar() for _ in range(4)]
        self.y_b = 3
        self.buttons_b = [Checkbutton(self, text=self.ops[i], variable=self.var_b[i], command=self.cb_b) for i in range(4)]
        for i in range(4): self.buttons_b[i].grid(row=self.y_b+i, column=2, sticky='w')
        # *************** B ***************

        Button(self, text="CONVERT", bd=5, relief="groove", bg="#0BD72D", width=15,  command=self.convert).grid(row=7, columnspan=3)


        self.nil = "                  NIL                   "
        Label(self, text="Binary: ").grid(row=9, sticky='w')
        self.l_bin_ans = Label(self, text=self.nil, borderwidth=3, height=2, relief="groove")
        self.l_bin_ans.grid(row=9, column=2)

        Label(self, text="Decimal: ").grid(row=10, sticky='w')
        self.l_dec_ans = Label(self, text=self.nil, borderwidth=3, height=2, relief="groove")
        self.l_dec_ans.grid(row=10, column=2)

        Label(self, text="Octal: ").grid(row=11, sticky='w')
        self.l_oct_ans = Label(self, text=self.nil, borderwidth=3, height=2, relief="groove")
        self.l_oct_ans.grid(row=11, column=2)

        Label(self, text="Hexa Decimal: ").grid(row=12, sticky='w')
        self.l_hex_ans = Label(self, text=self.nil, borderwidth=3, height=2, relief="groove")
        self.l_hex_ans.grid(row=12, column=2)
        
        self.varss = [self.l_bin_ans, self.l_dec_ans, self.l_oct_ans, self.l_hex_ans]

        Button(self, text="CALCULATOR", bd=5, width=15, bg="#2B00FF", relief="groove", command=Calculator).grid(row=2, column=4)
        Button(self, text="EXPLANATION", bd=5, width=15, bg="#CC00CC", relief="groove", command=self.explanation).grid(row=3, column=4)
        Button(self, text="HISTORY", bd=5, width=15, bg="cyan", relief="groove", command=self.history).grid(row=4, column=4)
        Button(self, text="ABOUT", bd=5, width=15, bg="grey", relief="groove", command=self.about).grid(row=5, column=4)
        Button(self, text="EXIT", bd=5, width=15, bg="red", relief="groove", command=self.destroy).grid(row=6, column=4)



        self.title("Base Converter")
        try: self.iconbitmap(Images.get_ico('c'))
        except Exception as e: print(e)
        self.attributes("-topmost", True)
        self.reset()
        self.mainloop()

    def backspace(self): self.entry.delete(self.entry.index("insert") - 1)

    def reset(self):
        try: os.remove(self.file)
        except Exception as e: print(e)
        self.entry.delete(0, "end")
        self.entry.insert(0, "")
        self.l_bin_ans.config(text=self.nil)
        self.l_dec_ans.config(text=self.nil)
        self.l_oct_ans.config(text=self.nil)
        self.l_hex_ans.config(text=self.nil)

        for i in range(4):
            self.var_a[i].set(0)
            self.var_b[i].set(0)

    def get_name(self, num): return self.ops[num]
    def get_abbr(self, num): return self.opsm[num]
    def get_errmsg(self):
        msg = ''
        if self.now_a==0:msg = "You have entered invalid input.\nOnly '0' and '1' are accepted."
        if self.now_a==1: msg = "You have entered invalid input.\nOnly numbers are accepted."
        if self.now_a==2: msg = "You have entered invalid input.\nOnly 0 to 7 numbers are accepted."
        if self.now_a==3: msg = "You have entered invalid input.\nOnly 0 to 9 and 'A' to 'F' are accepted."
        return msg
    def check(self):
        if self.now_a == None and self.now_b == None:  messagebox.showerror("ERROR INPUT", "You must tick the two sides")
        else: return True
    def convert(self):
        entry = self.entry.get()
        if self.check():
            if entry == "": messagebox.showinfo("EMPTY", "Please enter value.")
            else:
                func_h = f"{self.get_abbr(self.now_a)}_to_{self.get_abbr(self.now_b)}"
                func = Base_Convert().__dict__[func_h]
                label = self.varss[self.now_b]
                errmsg = answer = None
                try:
                    answer = func(entry)
                    label["text"] = answer
                    header = f"{self.get_name(self.now_a)} To {self.get_name(self.now_b)}: {entry} => {answer}\n"
                    self.write_history(header)
                except Exception as e: messagebox.showinfo("ERROR INPUT", f"{e}\n\n{self.get_errmsg()}", "error")

    def write_history(self, msg):
        with open(self.file, "a") as file: file.write(msg)

    def cb_a(self):
        self.vals_a = [self.var_a[i].get() for i in range(4)]
        if self.now_a != None: self.buttons_a[self.now_a].deselect()
        try: self.now_a = self.vals_a.index(1)
        except ValueError: self.now_a = None

    def cb_b(self):
        self.vals_b = [self.var_b[i].get() for i in range(4)]
        if self.now_b != None: self.buttons_b[self.now_b].deselect()
        try: self.now_b = self.vals_b.index(1)
        except ValueError: self.now_b = None

    def explanation(self):
        self.cb_a()
        self.cb_b()
        msg = "", ""
        if self.now_a==0 and self.now_b==0: msg = "Binary Number System", "Binary number represents any number using 2 digits.\nBinary number system contains 0 and 1."
        elif self.now_a==0 and self.now_b==1: msg = "Binary To Decimal", "1. Start the decimal result at 0.\n2. Remove the most significant binary digit (leftmost) and add it to the result.\n3. If all binary digits have been removed, you’re done. Stop.\n4. Otherwise, multiply the result by 2.\n5. Go to step 2."
        elif self.now_a==0 and self.now_b==2: msg = "Binary To Octal", "An easy way to convert from binary to octal is to group binary digits into sets of three, starting with the least significant (rightmost) digits."
        elif self.now_a==0 and self.now_b==3: msg = "Binary To Hexa Decimal", "An easy way to convert from binary to hexadecimal is to group binary digits into sets of four, starting with the least significant (rightmost) digits."
        elif self.now_a==1 and self.now_b==0: msg = "Decimal To Binary", "1. Divide the decimal number by the desired target radix 2.\n2. Append the remainder as the next most significant digit.\n3. Repeat until the decimal number has reached zero."
        elif self.now_a==1 and self.now_b==1: msg = "Decimal Number System", "Decimal number represents any number using 10 digits.\nDecimal number system contains 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9."
        elif self.now_a==1 and self.now_b==2: msg = "Decimal To Octal", "1. Divide the decimal number by the desired target radix 8.\n2. Append the remainder as the next most significant digit.\n3. Repeat until the decimal number has reached zero."
        elif self.now_a==1 and self.now_b==3: msg = "Decimal To Hexa Decimal", "1. Divide the decimal number by the desired target radix 16.\n2. Append the remainder as the next most significant digit.\n3. Repeat until the decimal number has reached zero.\n4. If any remainder exceed 9 then replace the digits with the corresponding alphabetical letters."
        elif self.now_a==2 and self.now_b==0: msg = "Octal To Binary", "Converting from octal to binary is as easy as converting from binary to octal.\nSimply look up each octal digit to obtain the equivalent group of three binary digits."
        elif self.now_a==2 and self.now_b==1: msg = "Octal To Decimal", "1. Start the decimal result at 0.\n2.Remove the most significant octal digit (leftmost) and add it to the result.\n3. If all octal digits have been removed, you’re done. Stop.\n4. Otherwise, multiply the result by 8.\n5. Go to step 2."
        elif self.now_a==2 and self.now_b==2: msg = "Octal Number Syatem", "Octal number represents any number using 8 digits.\nOctal number system contains 0, 1, 2, 3, 4, 5, 6, 7 and 8."
        elif self.now_a==2 and self.now_b==3: msg = "Octal To Hexa Decimal", "When converting from octal to hexadecimal, it is often easier to first convert the octal number into binary and then from binary into hexadecimal."
        elif self.now_a==3 and self.now_b==0: msg = "Hexa Decimal To Binary", "Converting from hexadecimal to binary is as easy as converting from binary to hexadecimal.\nSimply look up each hexadecimal digit to obtain the equivalent group of four binary digits."
        elif self.now_a==3 and self.now_b==1: msg = "Hexa Decimal To Decimal", "Converting hexadecimal to decimal can be performed in the conventional mathematical way, by showing each digit place as an increasing power of 16.\nOf course, hexadecimal letter values need to be converted to decimal values before performing the math."
        elif self.now_a==3 and self.now_b==2: msg = "Hexa Decimal To Octal", "When converting from hexadecimal to octal, it is often easier to first convert the hexadecimal number into binary and then from binary into octal."
        elif self.now_a==3 and self.now_b==3: msg = "Hecxa Decimal Number System", "Hexa Decimal number represents any number using 10 digits and 6 alphabetical letters.\nHexa Decimal number system contains 0, 1, 2, 3, 4, 5, 6, 7, 8 and 9 as digits and A, B, C, D, E and F as alphabetical letters."
        else: msg = "REQUIREMENT", "Choose options on the both side"
        messagebox.showinfo(*msg)

    def history(self):
        try:
            file = open(self.file, "r")
            data = file.readlines()
            m = ""
            for i in data: m += str(i) + "\n"
            messagebox.showinfo("HISTORY", str(m))
            file.close()
        except Exception as e:
            print(e)
            messagebox.showinfo("EMPTY","There are no histoty recorded.")

    def about(self): messagebox.showinfo("ABOUT","Name: Apata Mracle Peter\nEmail: rockymiracy@gmail.com\n\nNickname: PRMP Smart\nEmail: prmpsmart@gmail.com\n\nFEDERAL UNIVERSITY OF TECHNOLOGY AKURE")

class Calculator(Toplevel):
    
    def __init__(self):
        super().__init__()
        label_expression = Label(self, text="Enter expression: ")
        label_expression.grid(row=0, sticky='w')

        entry_cal = Entry(self, bd=3)
        entry_cal.grid(row=0, column=1, columnspan=2, ipadx=30, ipady=10)

        def backspace(): entry_cal.delete(entry_cal.index("insert") - 1)

        self.btn_backspace = Button(self, text="<--", bd=5, bg="#E5EB39", width=14, height=2, relief="groove", command=backspace)
        self.btn_backspace.grid(row=0, column=3)

        label_answer1 = Label(self, text="Answer: ")
        label_answer1.grid(row=3, column=0, sticky='w')

        self.label_space_cal=Label(self, text=" ", bd=2, width=17, height=2, relief="groove")
        self.label_space_cal.grid(row=3, column=1, columnspan=2, ipadx=30)

        def reset_cal():
            entry_cal.delete(0, "end")
            entry_cal.insert(0, "")
            self.label_space_cal: Label.config(text="                                         ")
            self.label_space_cal.grid(row=3, column=1, columnspan=2)

        def bracket_start():
            entry_cal.insert(entry_cal.index("insert"), "(")

        def bracket_end():
            entry_cal.insert(entry_cal.index("insert"), ")")

        def entry_divide():
            entry_cal.insert(entry_cal.index("insert"), "/")

        btn_reset = Button(self, text="RESET", width=15, height=2, bg="#F24B4B", command=reset_cal)
        btn_reset.grid(row=4)

        btn_bracket_start = Button(self, text="(", width=15, height=2, bg="cyan", command=bracket_start)
        btn_bracket_start.grid(row=4, column=1)

        btn_bracket_end = Button(self, text=")", width=15, height=2, bg="cyan", command=bracket_end)
        btn_bracket_end.grid(row=4, column=2)

        btn_divide = Button(self, text="/", width=15, height=2, bg="pink", command=entry_divide)
        btn_divide.grid(row=4, column=3)


        def entry_7():
            entry_cal.insert(entry_cal.index("insert"), "7")

        def entry_8():
            entry_cal.insert(entry_cal.index("insert"), "8")

        def entry_9():
            entry_cal.insert(entry_cal.index("insert"), "9")

        def entry_multiply():
            entry_cal.insert(entry_cal.index("insert"), "*")

        btn_7 = Button(self, text="7",  width=15, height=2, bg="white", command=entry_7)
        btn_7.grid(row=5)

        btn_8 = Button(self, text="8",  width=15, height=2, bg="white", command=entry_8)
        btn_8.grid(row=5, column=1)

        btn_9 = Button(self, text="9",  width=15, height=2, bg="white", command=entry_9)
        btn_9.grid(row=5, column=2)

        btn_multiply = Button(self, text="*",  width=15, height=2, bg="pink", command=entry_multiply)
        btn_multiply.grid(row=5, column=3)
        
        label_result = Label(self)
        label_result.grid(row=3, column=1, columnspan=2)

        def entry_4():
            entry_cal.insert(entry_cal.index("insert"), "4")

        def entry_5():
            entry_cal.insert(entry_cal.index("insert"), "5")

        def entry_6():
            entry_cal.insert(entry_cal.index("insert"), "6")

        def entry_minus():
            entry_cal.insert(entry_cal.index("insert"), "-")

        btn_4 = Button(self, text="4",  width=15, height=2, bg="white", command=entry_4)
        btn_4.grid(row=6)

        btn_5 = Button(self, text="5",  width=15, height=2, bg="white", command=entry_5)
        btn_5.grid(row=6, column=1)

        btn_6 = Button(self, text="6",  width=15, height=2, bg="white", command=entry_6)
        btn_6.grid(row=6, column=2)

        btn_minus = Button(self, text="-",  width=15, height=2, bg="pink", command=entry_minus)
        btn_minus.grid(row=6, column=3)

        def entry_1():
            entry_cal.insert(entry_cal.index("insert"), "1")

        def entry_2():
            entry_cal.insert(entry_cal.index("insert"), "2")

        def entry_3():
            entry_cal.insert(entry_cal.index("insert"), "3")

        def entry_plus():
            entry_cal.insert(entry_cal.index("insert"), "+")

        btn_1 = Button(self, text="1",  width=15, bg="white", height=2, command=entry_1)
        btn_1.grid(row=7)

        btn_2 = Button(self, text="2",  width=15, bg="white", height=2, command=entry_2)
        btn_2.grid(row=7, column=1)

        btn_3 = Button(self, text="3",  width=15, height=2, bg="white", command=entry_3)
        btn_3.grid(row=7, column=2)

        btn_plus = Button(self, text="+",  width=15, height=2, bg="pink", command=entry_plus)
        btn_plus.grid(row=7, column=3)

        def entry_0():
            entry_cal.insert(entry_cal.index("insert"), "0")

        def entry_decimal():
            entry_cal.insert(entry_cal.index("insert"), ".")

        def result():
            try:
                if entry_cal.get()== "":
                    messagebox.showinfo("INVALID", "Please enter expression")
                else:
                    res = eval(str(entry_cal.get()))
                    label_result.config(text=res)
            except ZeroDivisionError:
                messagebox.showinfo("ERROR", "Can not divisible by zero")
            except SyntaxError:
                messagebox.showinfo("ERROR", "You have entered invalid syntax")
            except NameError:
                messagebox.showinfo("ERROR", "Only numbers are allowed")

        btn_exit = Button(self, text="EXIT",  width=15, height=2, bg="red", command=self.destroy)
        btn_exit.grid(row=8)

        btn_0 = Button(self, text="0",  width=15, height=2, bg="white", command=entry_0)
        btn_0.grid(row=8, column=1)

        btn_decimal = Button(self, text=".",  width=15, height=2, bg="cyan", command=entry_decimal)
        btn_decimal.grid(row=8, column=2)

        btn_result = Button(self, text="=",  width=15, height=2, bg="#0BD72D", command=result)
        btn_result.grid(row=8, column=3)

        self.title("AGAM CALCULATOR")
        try:
            self.iconbitmap(Images.get_ico('d'))
        except Exception as e:
            print(e)
            pass
        self.attributes("-topmost", True)
        self.mainloop()


if __name__ == "__main__":
    Base_Converter()
    # Calculator()

