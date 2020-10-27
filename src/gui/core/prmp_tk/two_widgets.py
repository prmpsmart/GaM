from .core import *
from ....backend.core.date_time import DateTime


class TwoWidgets(PRMP_Frame):
    top_widgets = {'label': PRMP_Label, 'checkbutton': PRMP_Checkbutton, 'radiobutton': PRMP_Radiobutton}
    bottom_widgets = {'label': PRMP_Label, 'datebutton': PRMP_DateButton, 'entry': PRMP_Entry, 'text': PRMP_Text, 'combobox': PRMP_Combobox, 'spinbox': ttk.Spinbox}
    events = {'combobox': ['<<ComboboxSelected>>'], 'spinbox': ['<<Increment>>', '<<Decrement>>']}
    bottom_defaults = {'borderwidth': 3, 'relief': 'sunken', 'asEntry': True}
    
    def __init__(self, master, relx=0, rely=0, relw=0, relh=0, top='', bottom='', func=None, orient='v', relief="groove", command=None, longent=.5, value='1', ilh=0, topKwargs={}, bottomKwargs={}):
        super().__init__(master)
        
        self.relx, self.rely, self.relh, self.relw = relx, rely, relh, relw
        
        self.value = value
        self.ilh = ilh
        self.top = top.lower()
        self.bottom = bottom.lower()
        self.orient = orient
        self.longent = longent
        top_wid = self.top_widgets[top]
        bottom_wid = self.bottom_widgets[bottom]
        
        events = self.events.get(bottom) if func else None

        if top.lower() in ['checkbutton', 'radiobutton']:
            if not command: command = self.checked
            self.Top = top_wid(self, command=command, **topKwargs)
            
        else: self.Top = top_wid(self, **topKwargs)
        
        bottom_defaults = self.bottom_defaults.copy() if bottom in ['label', 'datebutton'] else {}
        bottom_defaults.update(bottomKwargs)
        
        self.Bottom = bottom_wid(self, **bottom_defaults)
        
        if events:
            for event in events: self.Bottom.bind(event, func)
        
        self.B = self.Bottom
        self.T = self.Top
        
        try: self.variable = self.T.var
        except: self.variable = None

        self.rt = None
        try: self.bindOverrelief(self.B, 'solid')
        except: pass
        
        self.childWidgets += [self.T, self.B]
        
        if self.value and self.variable: self.checked()
        
        self.place_widgs()
    
    def checked(self):
        if self.variable:
            if self.variable.get() == self.value:
                self.normal('b')
            else:  self.disabled('b')
    
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
    
    def set(self, values): self.Bottom.set(values)
    
    def get(self): return self.Bottom.get()
    
    def config(self, **kwargs): self.Top.configure(**kwargs)

    def place_widgs(self):
        self.place(relx=self.relx, rely=self.rely, relh=self.relh, relw=self.relw)
        if self.orient == 'h':
            if self.bottom == 'text': self.Top.place(relx=0, rely=0, relh=self.ilh or .3, relw=self.longent)
            else: self.Top.place(relx=0, rely=0, relh=1, relw=self.longent)
            self.Bottom.place(relx=self.longent + .02, rely=0, relh=.945, relw=1 - self.longent - .02)
        else:
            self.Top.place(relx=0, rely=0, relw=1, relh=self.longent)
            self.Bottom.place(relx=0, rely=.6, relw=1, relh=1 - self.longent - .05)
        return self
    
TW = TwoWidgets

class RadioCombo(TwoWidgets):
    def __init__(self, master, **kwargs): super().__init__(master, top='radiobutton', bottom='combobox', **kwargs)
RC = RadioCombo

class RadioEntry(TwoWidgets):
    def __init__(self, master, **kwargs): super().__init__(master, top='radiobutton', bottom='entry', **kwargs)
RE = RadioEntry

class LabelSpin(TwoWidgets):
    def __init__(self, master, **kwargs):

        super().__init__(master, top='label', bottom='spinbox', **kwargs)

    def set(self, from_=.1, to=1, increment=.1): self.Bottom.config(from_=from_, to=to, increment=increment)
    
LS = LabelSpin

class LabelEntry(TwoWidgets):
    def __init__(self, master, **kwargs): super().__init__(master, top='label', bottom='entry', **kwargs)
LE = LabelEntry

class LabelText(TwoWidgets):
    def __init__(self, master, **kwargs):
        super().__init__(master, top='label', bottom='text', **kwargs)
    
    def get(self): return self.B.get('1.0', 'end').strip('\n')
LT = LabelText

class LabelCombo(TwoWidgets):
    def __init__(self, master, **kwargs):

        super().__init__(master, top='label', bottom='combobox', **kwargs)
        
        self.choosen = None
    
    def set(self, values):
        
        # use a dict mechanism, show only the key
        # so when a key is choosen, we get the real value using that key
        # the key is the region / account name
        '''
        in the case of account
        [account] [combobox (showing the account managers {dc} which in turn shows the recordmanagers / recordmanagers {directly in coop})]
        clicking one above will update the records list on the right
        
        '''
        pass
    
    def get(self):
        pass
    
LC = LabelCombo

class CheckEntry(TwoWidgets):
    def __init__(self, master, **kwargs): super().__init__(master, top='checkbutton', bottom='entry', **kwargs)
CE = CheckEntry

class CheckCombo(TwoWidgets):
    def __init__(self, master, **kwargs):
        super().__init__(master, top='checkbutton', bottom='combobox',**kwargs)
        
CC = CheckCombo

class LabelButton(TwoWidgets):
    def __init__(self, master, **kwargs): super().__init__(master, top='label', bottom='button',**kwargs)
LB = LabelButton

class LabelDateButton(TwoWidgets):
    def __init__(self, master, **kwargs): super().__init__(master, top='label', bottom='datebutton', **kwargs)
    
LDB = LabelDateButton


