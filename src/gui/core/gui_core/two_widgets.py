from .prmp_tk import *
from ....backend.core.date_time import DateTime


class TwoWidgets(PRMP_Frame):
    
    def __init__(self, master, background=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, relx=0, rely=0, relw=0, relh=0, top='', bottom='', bordermode='inside', func=None, orient='v', activebackground=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, activeforeground="blue", disabledforeground=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, font=PTh.DEFAULT_LABEL_FONT, foreground=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, highlightbackground=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, highlightcolor=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, justify='left', overrelief="groove", relief="groove", command=None, text='', longent=.5, values=(0,), value='1', from_=.1, to=1, increment=.1, show=None, imageFile=None, ilh=0):
        super().__init__(master)
        
        self.relx, self.rely, self.relh, self.relw = relx, rely, relh, relw
        
        self.value = value
        self.ilh = ilh
        self.top = top.lower()
        self.bottom = bottom.lower()
        self.orient = orient
        self.longent = longent

        if top.lower() == 'checkbutton':
            
            if not command: command = self.checked
            self.Top = PRMP_Checkbutton(self, text=text, command=command, font=font)
        elif top.lower() == 'label': self.Top = PRMP_Label(self, text=text, font=font)
        elif top.lower() == 'radiobutton': 
            if not command: command = self.checked
            self.Top = PRMP_Radiobutton(self, text=text, command=command, value=value, font=font)

        if bottom.lower() == 'entry': self.Bottom = PRMP_Entry(self, show=show)
        elif bottom.lower() == 'button': self.Bottom = PRMP_Button(self)
        elif bottom.lower() == 'datebutton': self.Bottom = PRMP_DateButton(self)
        elif bottom.lower() == 'combobox':
            self.Bottom = PRMP_Combobox(self, values=values, show=show)
            if func: self.Bottom.bind('<<ComboboxSelected>>', func)
        elif bottom.lower() == 'spinbox':
            self.Bottom = ttk.Spinbox(self, from_=from_, to=to, increment=increment)
            if func:
                self.Bottom.bind('<<Increment>>', func)
                self.Bottom.bind('<<Decrement>>', func)
        elif bottom.lower() == 'text': self.Bottom = PRMP_Text(self, show=show)
        elif bottom.lower() == 'regionbutton': self.Bottom = PRMP_RegionButton(self,)
        
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
    
    def set(self, values):
        if self.bottom == 'combobox': self.Bottom.config(values=values)
        elif self.bottom == 'entry': self.Bottom.insert(0, values)
        elif self.bottom == 'text': self.Bottom.insert(0.0, values)
        elif self.bottom == 'datebutton': self.Bottom.set(values)
        else: self.Bottom.config(text=values)
    
    def get(self): return self.Bottom.get()
    
    def config(self, **kwargs): self.Top.configure(**kwargs)
    
    def style(self):
        self['background'] = PRMP_Theme.DEFAULT_BACKGROUND_COLOR
        if self.top in ['checkbutton', 'radiobutton']: self.Top.config(background=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, activebackground=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, activeforeground="blue", disabledforeground=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, font=PRMP_Theme.DEFAULT_FONT, foreground=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, highlightbackground=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, highlightcolor=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, justify='left', overrelief="ridge", relief="groove")
        else: self.Top.config(background=PRMP_Theme.DEFAULT_BACKGROUND_COLOR,  activebackground=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, activeforeground="blue", disabledforeground=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, foreground=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, highlightbackground=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, highlightcolor=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, justify='left', relief="groove")

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
    def __init__(self, master, **kwargs): super().__init__(master, top='label', bottom='datebutton',**kwargs)
    
LDB = LabelDateButton

# ?? removing soon

class LabelRegionButton(TwoWidgets):
    
    def __init__(self, master=None, region=None, **kwargs):
        super().__init__(master, top='label', bottom='regionbutton', command=self.openDetails, **kwargs)
        self.region = region
        self.loadRegion(region)
        self.bindEntryHighlight()
    
    def loadRegion(self, region=None):
        if region: self['text'] = region.name
    
    def openDetails(self):
        
        # open RegionDetailsDialog
        pass

LRB = LabelRegionButton

