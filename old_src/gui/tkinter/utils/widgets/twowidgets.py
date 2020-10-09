from tkinter.ttk import Combobox, Spinbox

from ..decorate.styles import Styles, Fonts
from tkinter import Label, LabelFrame, Checkbutton, Entry, Radiobutton

__author__ = 'PRMPSmart'


class TwoWidgets(LabelFrame):
    
    def __init__(self, master, background=Styles.background, relx=0, rely=0, relw=0, relh=0, top='', bottom='', bordermode='inside', func=None, orient='v', activebackground=Styles.background, activeforeground="blue", disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, justify='left', overrelief="groove", relief="groove", variable=None,  command=None, text='', longent=None, textvariable=None, values=(0,), value='1', from_=.1, to=1, increment=.1, show=None):
        super().__init__(master, text='')
        
        self.relx, self.rely, self.relh, self.relw = relx, rely, relh, relw

        self.variable = variable
        self.value = value
        self.top = top
        self.orient = orient
        self.longent = longent

        if top.lower() == 'checkbutton':
            if not command: command = self.checked
            self.Top = Checkbutton(self, text=text, variable=variable, command=command)
        elif top.lower() == 'label': self.Top = Label(self, text=text)
        elif top.lower() == 'radiobutton': 
            if not command: command = self.checked
            self.Top = Radiobutton(self, text=text, variable=variable, command=command, value=value)

        if bottom.lower() == 'entry': self.Bottom = Entry(self, textvariable=textvariable, show=show)
        elif bottom.lower() == 'combobox':
            self.Bottom = Combobox(self, values=values, textvariable=textvariable, show=show)
            if func: self.Bottom.bind('<<ComboboxSelected>>', func)
        elif bottom.lower() == 'spinbox':
            self.Bottom = Spinbox(self, from_=from_, to=to, increment=increment)
            if func:
                self.Bottom.bind('<<Increment>>', func)
                self.Bottom.bind('<<Decrement>>', func)

        
        self.style()
        self.checked()


    def checked(self):
        if self.variable:
            if self.variable.get() == self.value:
                self.normal('b')
                self.Top['foreground'] = 'blue'
            else:
                self.disabled('b')
                self.Top['foreground'] = Styles.foreground

    def get_top(self): return self.Top
    def get_bottom(self): return self.Bottom
    def disabled(self, wh=''):
        if wh == 't': self.Top.config(state='disabled')
        elif wh == 'b': self.Bottom.config(state='disabled')
        else:
            self.Top.config(state='disabled')
            self.Bottom.config(state='disabled')
    def active(self, wh=''):
        if wh == 't': self.Top.config(state='active')
        elif wh == 'b': self.Bottom.config(state='active')
        else:
            self.Top.config(state='active')
            self.Bottom.config(state='active')
    def normal(self, wh=''):
        if wh == 't': self.Top.config(state='normal')
        elif wh == 'b': self.Bottom.config(state='normal')
        else:
            self.Top.config(state='normal')
            self.Bottom.config(state='normal')
    def set(self, values): self.Bottom.config(values=values)
    def get(self): return self.Bottom.get()
    def config(self, **kwargs): self.Top.config(**kwargs)
    def style(self):
        self['background'] = Styles.background
        if self.top in ['checkbutton', 'radiobutton']: self.Top.config(background=Styles.background, activebackground=Styles.background, activeforeground="blue", disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, justify='left', overrelief="ridge", relief="groove")
        else: self.Top.config(background=Styles.background,  activebackground=Styles.background, activeforeground="blue", disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, justify='left', relief="groove")

    def place_widgs(self):
        self.place(relx=self.relx, rely=self.rely, relh=self.relh, relw=self.relw)
        if self.orient == 'h':
            if self.longent: self.relw, self.relwb = .3, .7
            else: self.relwb = self.relw = .5
            self.Top.place(relx=0, rely=0, relh=1, relw=self.relw)
            self.Bottom.place(relx=self.relw, rely=0, relh=1, relw=self.relwb)
        else:
            self.Top.place(relx=0, rely=0, relw=1, relh=.6)
            self.Bottom.place(relx=0, rely=.6, relw=1, relh=.4)

class RadioCombo(TwoWidgets):
    def __init__(self, master, relx=0, rely=0, relw=0, relh=0, text='', func=None, orient='v', activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, justify='left', overrelief="groove", relief='groove', variable=None, bordermode='ignore', value=None, values=(0,), command=None, longent=None, textvariable=None, show=None):
        
        super().__init__(master, background=background, relx=relx, rely=rely, relw=relw, relh=relh, top='radiobutton', bottom='combobox', bordermode=bordermode, text=text, orient=orient, activebackground=activebackground, activeforeground=activeforeground, disabledforeground=disabledforeground, font=Fonts.font11b, foreground=foreground, highlightbackground=highlightbackground, highlightcolor=highlightcolor, relief=relief, variable=variable, command=command, values=values, value=value, func=func, longent=longent, textvariable=textvariable, show=show)

class RadioEntry(TwoWidgets):
    def __init__(self, master, relx=0, rely=0, relw=0, relh=0, text='', variable=None, value=None,  command=None, activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, orient='h', foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, justify='left', overrelief="ridge", relief="groove", bordermode='inside', longent=None, textvariable=None, show=None):
        
        super().__init__(master, background=background, relx=relx, rely=rely, relw=relw, relh=relh, top='radiobutton', bottom='entry', bordermode=bordermode, text=text, orient=orient, activebackground=activebackground, activeforeground=activeforeground, disabledforeground=disabledforeground, font=Fonts.font11b, foreground=foreground, highlightbackground=highlightbackground, highlightcolor=highlightcolor, relief=relief, variable=variable, command=command, value=value, longent=longent, textvariable=textvariable, show=show)

class LabelSpin(TwoWidgets):
    def __init__(self, master, relx=0, rely=0, relw=0, relh=0, text='', func=None, orient='v', activebackground=Styles.background, activeforeground="black", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief="groove", justify='left', bordermode='inside', from_=.1, to=1, increment=.1, longent=None, show=None):

        super().__init__(master, background=background, relx=relx, rely=rely, relw=relw, relh=relh, top='label', bottom='spinbox', bordermode=bordermode, text=text, orient=orient, activebackground=activebackground, activeforeground=activeforeground, disabledforeground=disabledforeground, font=Fonts.font11b, foreground=foreground, highlightbackground=highlightbackground, highlightcolor=highlightcolor, relief=relief, from_=from_, to=to, increment=increment, longent=longent)

    def set(self, from_=.1, to=1, increment=.1): self.Bottom.config(from_=from_, to=to, increment=increment)

class LabelEntry(TwoWidgets):
    def __init__(self, master, relx=0, rely=0, relw=0, relh=0, text='', orient='v', activebackground=Styles.background, activeforeground="black", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief="groove", bordermode='inside', longent=None, textvariable=None, show=None):

        super().__init__(master, background=background, relx=relx, rely=rely, relw=relw, relh=relh, top='label', bottom='entry', bordermode=bordermode, text=text, orient=orient, activebackground=activebackground, activeforeground=activeforeground, disabledforeground=disabledforeground, font=Fonts.font11b, foreground=foreground, highlightbackground=highlightbackground, highlightcolor=highlightcolor, relief=relief, longent=longent, textvariable=textvariable, show=show)

class LabelCombo(TwoWidgets):
    def __init__(self, master, relx=0, rely=0, relw=0, relh=0, text='', func=None, orient='v', activebackground=Styles.background, activeforeground="black", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief="groove", bordermode='inside', values=(0,), longent=None, textvariable=None, show=None):

        super().__init__(master, background=background, relx=relx, rely=rely, relw=relw, relh=relh, top='label', bottom='combobox', bordermode=bordermode, text=text, func=func, orient=orient, activebackground=activebackground, activeforeground=activeforeground, disabledforeground=disabledforeground, font=Fonts.font11b, foreground=foreground, highlightbackground=highlightbackground, highlightcolor=highlightcolor, relief=relief, values=values, longent=longent, textvariable=textvariable, show=show)

class CheckEntry(TwoWidgets):
    def __init__(self, master, relx=0, rely=0, relw=0, relh=0, text='', orient='v', activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, justify='left', overrelief="groove", relief="groove", variable=None, bordermode='inside', command=None, longent=None, textvariable=None, show=None):
        
        super().__init__(master, background=background, relx=relx, rely=rely, relw=relw, relh=relh, top='checkbutton', text=text, bottom='entry', bordermode=bordermode, activebackground=activebackground, activeforeground=activebackground, disabledforeground=disabledforeground, font=Fonts.font11b, foreground=foreground, highlightbackground=highlightbackground, highlightcolor=highlightcolor, justify=justify, overrelief=overrelief, relief=relief, variable=variable, command=command, orient=orient, longent=longent, textvariable=textvariable, show=show)

class CheckCombo(TwoWidgets):
    def __init__(self, master, relx=0, rely=0, relw=0, relh=0, text='', func=None, orient='v', activebackground=Styles.background, activeforeground="blue", background=Styles.background, disabledforeground=Styles.foreground, font=Fonts.font11b, foreground=Styles.foreground, highlightbackground=Styles.background, highlightcolor=Styles.foreground, relief="groove", overrelief='groove', justify='left', variable=None, bordermode='inside', values=(0,), command=None, longent=0, textvariable=None, show=None):
        
        super().__init__(master, background=background, relx=relx, rely=rely, relw=relw, relh=relh, top='checkbutton', bottom='combobox', bordermode=bordermode, activebackground=activebackground, activeforeground=activebackground, disabledforeground=disabledforeground, font=Fonts.font11b, foreground=foreground, highlightbackground=highlightbackground, highlightcolor=highlightcolor, relief=relief, overrelief=overrelief, text=text, justify=justify, variable=variable, command=command, values=values, orient=orient, func=func, longent=longent, textvariable=textvariable, show=show)

