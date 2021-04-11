from . import *
from .datewidgets import *
from .scrollables import *
from .dropdowns import *



#  These widgets doesn't need or can't be used with PRMP_Widget.addWidget()

class TwoWidgets(PRMP_Frame):
    top_widgets = {'label': PRMP_Label, 'checkbutton': PRMP_Checkbutton, 'radiobutton': PRMP_Radiobutton}
    stop_widgets = {'label': PRMP_Style_Label, 'checkbutton': PRMP_Style_Checkbutton, 'radiobutton': PRMP_Style_Radiobutton}
    bottom_widgets = {'label': PRMP_Label, 'datebutton': PRMP_DateButton, 'entry': PRMP_Entry, 'text': PRMP_Text, 'stext': PRMP_ScrollText, 'combobox': PRMP_Combobox, 'spinbox': PRMP_Spinbox, 'button': PRMP_Button, 'monthbutton': PRMP_MonthButton, 'monthyearbutton': PRMP_MonthYearButton}
    sbottom_widgets = {'label': PRMP_Style_Label, 'datebutton': PRMP_DateButton, 'entry': PRMP_Style_Entry, 'text': PRMP_Text, 'stext': PRMP_ScrollText, 'combobox': PRMP_Combobox, 'spinbox': PRMP_Style_Spinbox, 'button': PRMP_Button, 'dropdownentry': PRMP_DropDownEntry}
    events = {'combobox': ['<<ComboboxSelected>>', '<Return>'], 'spinbox': ['<<Increment>>', '<<Decrement>>', '<Return>']}
    top_defaults = {'asLabel': True}
    bottom_defaults = {'borderwidth': 3, 'relief': 'sunken', 'asEntry': True}

    def __init__(self, master, top='', bottom='', orient='v', relief='groove', command=None, longent=.5, widthent=0, topKwargs=dict(), bottomKwargs=dict(), disableOnToggle=True, dot=None, tttk=False, bttk=False, func=None, **kwargs):
        super().__init__(master, **kwargs)

        self.orient = orient
        self.longent = longent
        self.widthent = widthent

        if dot != None: disableOnToggle = dot
        self.disableOnToggle = disableOnToggle

 # top part

        if isinstance(top, str):
            self.top = top.lower()

            if tttk: top_wid = self.stop_widgets[top]
            else: top_wid = self.top_widgets[top]

            top_defaults = {k:v for k, v in self.top_defaults.items()}

            if top in ['checkbutton', 'radiobutton']: topKw = dict(command=command or self.checked, **topKwargs)
            else: topKw = dict(**topKwargs)

        else:
            self.top = top.__name__.lower()

            top_wid = top
            placeholder = ''
            topKw = topKwargs.copy()

        self.Top = top_wid(self, **topKw)
        text = topKwargs.get('text')
        if not text:
            config = topKwargs.get('config')
            if config: text = config.get('text')

 # bottom part
        if isinstance(bottom, str):
            self.bottom = bottom.lower()

            if bttk: bottom_wid = self.sbottom_widgets[bottom]
            else: bottom_wid = self.bottom_widgets[bottom]

            placeholder = bottomKwargs.get('placeholder', f'Enter {text}.')

            if bottom in ['label', 'datebutton', 'button']:
                bottomKw = dict(**self.bottom_defaults, **bottomKwargs)
                if self._ttk_: bottomKw['style'] = 'entry.Label'
            else:
                if bottomKwargs.get('placeholder', None) != None: bottomKw = dict(**bottomKwargs)
                else: bottomKw = dict(placeholder=placeholder, **bottomKwargs)

            if bottom == 'datebutton': placeholder = 'Choose Date'

        else:
            self.bottom = bottom.__name__.lower()

            bottom_wid = bottom
            placeholder = ''
            bottomKw = bottomKwargs.copy()

        self.Bottom = bottom_wid(self, status=placeholder, **bottomKw)
        # if bottom == 'entry': print(bottomKw)

        self.required = getattr(self.Bottom, 'required', False)

        events = self.events.get(bottom)
        if events:
            for event in events:
                self.Bottom.bind(event, self.clicked, '+')
                if func: self.Bottom.bind(event, func, '+')

        self.B = self.Bottom
        self.T = self.Top

        if self.T.checkVar:
            self.value, self.variable = self.T.value, self.T.variable
            if self.value and self.variable: self.checked()

        self.rt = None

        self.place_widgs()
 
    def clicked(self, e=0): return self.B.get()

    def light(self):
        # print(self)
        self.normal('b')
        self.T.light()
        self.B.focus()

    def unlight(self):
        # self.readonly()
        self.disabled('b')
        self.T.unlight()

    def verify(self): return self.Bottom.verify()

    def toggleSwitch(self):
        self.onFg = False
        if self.toggleGroup: self.T.bind('<1>', self.switchGroup)

    def readonly(self):
        try: self.Bottom.readonly()
        except Exception as e: self.disabled('b')

    def disabled(self, wh=''):
        if not self.disableOnToggle: return

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
        if self.orient == 'h':
            if self.bottom == 'text': self.Top.place(relx=0, rely=0, relh=self.widthent or .3, relw=self.longent)
            else: self.Top.place(relx=0, rely=0, relh=1, relw=self.longent)
            self.Bottom.place(relx=self.longent + .02, rely=0, relh=.945, relw=1 - self.longent - .02)
        else:
            self.Top.place(relx=0, rely=0, relw=1, relh=self.longent)
            self.Bottom.place(relx=0, rely=self.longent+.05, relw=1, relh=1 - self.longent - .05)
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

class LabelSText(TwoWidgets):
    def __init__(self, master, **kwargs):
        super().__init__(master, top='label', bottom='stext', **kwargs)
LST = LabelSText

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

class LabelLabel(TwoWidgets):
    def __init__(self, master, bottomKwargs={}, **kwargs):
        if not bottomKwargs.get('font'): bottomKwargs['font'] = 'DEFAULT_FONT'
        super().__init__(master, top='label', bottom='label', bottomKwargs=bottomKwargs, **kwargs)
LL = LabelLabel

class LabelDateButton(TwoWidgets):
    def __init__(self, master, **kwargs): super().__init__(master, top='label', bottom='datebutton', **kwargs)
LDB = LabelDateButton

class LabelMonthButton(TwoWidgets):
    def __init__(self, master, **kwargs): super().__init__(master, top='label', bottom='monthbutton', **kwargs)
LMB = LabelMonthButton

class LabelMonthYearButton(TwoWidgets):
    def __init__(self, master, **kwargs): super().__init__(master, top='label', bottom='monthyearbutton', **kwargs)
LMYB = LabelMonthYearButton


