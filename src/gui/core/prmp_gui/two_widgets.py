from .core import *
from ....backend.core.date_time import DateTime

#  These widgets doesn't need or can't be used with PRMP_Widget.addWidget()

class TwoWidgets(PRMP_Frame):
    top_widgets = {'label': PRMP_Label, 'checkbutton': PRMP_Checkbutton, 'radiobutton': PRMP_Radiobutton}
    bottom_widgets = {'label': PRMP_Label, 'datebutton': PRMP_DateButton, 'entry': PRMP_Entry, 'text': PRMP_Text, 'combobox': PRMP_Combobox, 'spinbox': ttk.Spinbox}
    events = {'combobox': ['<<ComboboxSelected>>', '<Return>'], 'spinbox': ['<<Increment>>', '<<Decrement>>', '<Return>']}
    top_defaults = {'asLabel': True}
    bottom_defaults = {'borderwidth': 3, 'relief': 'sunken', 'asEntry': True}
    
    def __init__(self, master, relx=0, rely=0, relw=0, relh=0, top='', bottom='', func=None, orient='v', relief="groove", command=None, longent=.5, ilh=0, topKwargs=dict(), bottomKwargs=dict(), placeholder='', disableOnTogle=True, dot=None):
        super().__init__(master)
        
        self.relx, self.rely, self.relh, self.relw = relx, rely, relh, relw
        
        self.ilh = ilh
        self.top = top.lower()
        self.bottom = bottom.lower()
        self.orient = orient
        self.longent = longent
        
        if dot != None: disableOnTogle = dot
        self.disableOnTogle = disableOnTogle
        
        
        top_wid = self.top_widgets[top]
        bottom_wid = self.bottom_widgets[bottom]
        
        top_defaults = {k:v for k, v in self.top_defaults.items()}
        
        if top in ['checkbutton', 'radiobutton']: topKw = dict(command=command or self.checked, **topKwargs)
        else: topKw = dict(**topKwargs)
            
        self.Top = top_wid(self, **topKwargs)
        
        bottom_def = {k:v for k, v in self.bottom_defaults.items()}
        placeholder = placeholder or bottomKwargs.get('placeholder') or f'Enter {topKwargs.get("text")}.'
        
        bottomKwargs['placeholder'] = placeholder
        
        if bottom in ['label', 'datebutton']:
            del bottomKwargs['placeholder']
            bottomKw = dict(**bottom_def, **bottomKwargs)
        else: bottomKw = dict(**bottomKwargs)
        
        if bottom == 'datebutton': placeholder = 'Choose Date'
        
        self.Bottom = bottom_wid(self, status=placeholder, **bottomKw)
        
        del topKwargs, bottomKwargs
        
        events = self.events.get(bottom)
        if events:
            for event in events: self.Bottom.bind(event, self.clicked)
        
        self.B = self.Bottom
        self.T = self.Top
        
        self.val, self.var = self.value, self.variable = self.T.val, self.T.var

        self.rt = None
        
        if self.value and self.variable: self.checked()
        
        
        self.place_widgs()
        
    def clicked(self, e=0): return self.B.get()
    
    def light(self):
        self.normal('b')
        self.T.light()
        self.B.focus()
    
    def unlight(self):
        # self.readonly()
        self.disabled('b')
        self.T.unlight()
    
    def toggleSwitch(self):
        self.onFg = False
        if self.toggleGroup: self.T.bind('<1>', self.switchGroup)
        
    def readonly(self):
        try: self.Bottom.readonly()
        except Exception as e: self.disabled('b')
        
    def disabled(self, wh=''):
        if not self.disableOnTogle: return
        
        if wh == 't': self.Top.disabled()
        elif wh == 'b': self.Bottom.disabled()
        else:
            self.Top.disabled()
            self.Bottom.disabled()
    

    def active(self, wh=''):
        if wh == 't': self.Top.active()
        elif wh == 'b': self.Bottom.active()
        else:
            self.Top.active()
            self.Bottom.active()
    
    def normal(self, wh=''):
        if wh == 't': self.Top.normal()
        elif wh == 'b': self.Bottom.normal()
        else:
            self.Top.normal()
            self.Bottom.normal()
        
    
    def set(self, values): self.Bottom.set(values)
    
    def get(self): return self.Bottom.get()
    
    def changeValues(self, values): self.Bottom.changeValues(values)
    
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
LT = LabelText

class LabelCombo(TwoWidgets):
    def __init__(self, master, **kwargs):

        super().__init__(master, top='label', bottom='combobox', **kwargs)
        
        self.choosen = None
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


