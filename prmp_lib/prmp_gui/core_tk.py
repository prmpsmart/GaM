from .core import *

__all__ = ['PRMP_Button', 'PRMP_Checkbutton', 'PRMP_Entry', 'PRMP_Frame', 'PRMP_Label', 'PRMP_LabelFrame', 'PRMP_Menu', 'PRMP_OptionMenu', 'PRMP_PanedWindow', 'PRMP_Radiobutton', 'PRMP_Scale', 'PRMP_Scrollbar', 'PRMP_Spinbox', 'PRMP_Canvas', 'PRMP_Message', 'PRMP_Text', 'PRMP_Listbox', 'Button', 'Checkbutton', 'Entry', 'Frame', 'Label', 'LabelFrame', 'Menu', 'OptionMenu', 'PanedWindow', 'Radiobutton', 'Scale', 'Scrollbar', 'Spinbox', 'Canvas', 'Message', 'Text', 'Listbox']


picTypes = ['Pictures {.jpg .png .jpeg .gif .xbm}']


class PRMP_(PRMP_Widget):

    def __init__(self, **kwargs):
        super().__init__(_ttk_=False, **kwargs)
P_ = PRMP_

#   from tk widgets --> PRMP_

class PRMP_Button(PRMP_, tk.Button):
    TkClass = tk.Button

    def __init__(self, master=None, font='DEFAULT_BUTTON_FONT', asEntry=False, asLabel=False, config={}, **kwargs):
        kwargs.update(config)
        font = kwargs.get('font', font)
        kwargs['font'] = font
        PRMP_.__init__(self, master=master, asEntry=asEntry, **kwargs)

    @property
    def PRMP_WIDGET(self): return 'Button'
Button = PB = PRMP_Button

class PRMP_Checkbutton(PRMP_InputButtons, PRMP_, tk.Checkbutton):
    TkClass = tk.Checkbutton

    def __init__(self, master=None, asLabel=False, config={}, var=1, **kwargs):
        PRMP_.__init__(self, master=master, asLabel=asLabel, config=config, var=var, **kwargs)

        self.toggleSwitch()

    @property
    def PRMP_WIDGET(self): return 'Checkbutton'
    def disabled(self):
        self['fg'] = PRMP_Theme.DEFAULT_BACKGROUND_COLOR
        self.state('disabled')

Checkbutton = PC = PRMP_Checkbutton

class PRMP_Entry(PRMP_Input, PRMP_, tk.Entry):
    TkClass = tk.Entry

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master, config=config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)

    @property
    def PRMP_WIDGET(self): return 'Entry'
Entry = PE = PRMP_Entry

class PRMP_Frame(PRMP_, tk.Frame):
    TkClass = tk.Frame

    def __init__(self, master=None, bd=2, relief='flat', highlightable=False, config={}, **kwargs):

        PRMP_.__init__(self, master=master,relief=relief, highlightable=highlightable, nonText=True, config=config, **kwargs)

    @property
    def PRMP_WIDGET(self): return 'Frame'
Frame = PF = PRMP_Frame

class PRMP_Label(PRMP_, tk.Label):
    TkClass = tk.Label

    def __init__(self, master=None, font='DEFAULT_LABEL_FONT', config={}, **kwargs):

        PRMP_.__init__(self, master=master,font=font, config=config, **kwargs)

    @property
    def PRMP_WIDGET(self): return 'Label'
Label = PL = PRMP_Label

class PRMP_LabelFrame(PRMP_, tk.LabelFrame):
    TkClass = tk.LabelFrame

    def __init__(self, master=None, font='DEFAULT_LABELFRAME_FONT', config={}, **kwargs):

        PRMP_.__init__(self, master=master,font=font, config=config, **kwargs)

    @property
    def PRMP_WIDGET(self): return 'LabelFrame'
LabelFrame = PLF = PRMP_LabelFrame

class PRMP_Menu(PRMP_, tk.Menu):
    TkClass = tk.Menu

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master, config=config, **kwargs)
Menu = PM = PRMP_Menu

class PRMP_OptionMenu(PRMP_, tk.OptionMenu):
    TkClass = tk.OptionMenu

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master, config=config, **kwargs)
OptionMenu = PO = PRMP_OptionMenu

class PRMP_PanedWindow(PRMP_, tk.PanedWindow):
    TkClass = tk.PanedWindow

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master, config=config, **kwargs)
PanedWindow = PP = PRMP_PanedWindow

class PRMP_Radiobutton(PRMP_InputButtons, PRMP_, tk.Radiobutton):
    TkClass = tk.Radiobutton

    def __init__(self, master=None, asLabel=False, config={}, **kwargs):

        PRMP_.__init__(self, master=master,asLabel=asLabel, config=config, **kwargs)

    @property
    def PRMP_WIDGET(self): return 'Radiobutton'
Radiobutton = PR = PRMP_Radiobutton

class PRMP_Scale(PRMP_, tk.Scale):
    TkClass = tk.Scale

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master, config=config, **kwargs)
Scale = PS = PRMP_Scale

class PRMP_Scrollbar(PRMP_, tk.Scrollbar):
    TkClass = tk.Scrollbar

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master, config=config, **kwargs)

    def set(self, first, last): return tk.Scrollbar.set(self, first, last)
Scrollbar = PSc = PRMP_Scrollbar

class PRMP_Spinbox(PRMP_Input, PRMP_, tk.Spinbox):
    TkClass = tk.Spinbox

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master, config=config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)

    def get(self): return float(self.TkClass.get(self))

Spinbox = PSp = PRMP_Spinbox


# based on tk only

class PRMP_Canvas(PRMP_, tk.Canvas):
    TkClass = tk.Canvas

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master, config=config, **kwargs)
Canvas = PCv = PRMP_Canvas

class PRMP_Message(PRMP_, PRMP_Input, tk.Message):
    TkClass = tk.Message

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master, config=config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)
Message = PM = PRMP_Message

class PRMP_Text(PRMP_Input, PRMP_, tk.Text):
    TkClass = tk.Text

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master, config=config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)

    def _get(self): return tk.Text.get(self, '0.0', 'end').strip('\n')

    def set(self, values): self.clear(); self.insert('0.0', str(values))

    def clear(self): self.delete('0.0', 'end')

    @property
    def PRMP_WIDGET(self): return 'Text'
Text = PTx = PRMP_Text

class PRMP_Listbox(PRMP_, tk.Listbox):
    selectmodes = ['single', 'browse', 'multiple', 'extended']
    TkClass = tk.Listbox

    def __init__(self, master=None, config={}, values=[], callback=None, defBinds=1, bindings=[], **kwargs):

        if isinstance(values, (list, tuple, dict)): self.values = values.copy()
        else: self.values = values

        self.last = 0
        self.callback = callback

        defaultBinds = [('<<ListboxSelect>>', self.clicked, '+')]


        PRMP_.__init__(self, master=master, config=config, **kwargs)

        if defBinds: self.bindings(defaultBinds)
        self.bindings(bindings)


    def bindings(self, binds):
        for bind, func, sign in binds: self.bind(bind, func, sign)

    def clear(self):
        self.delete(0, self.last)
        self.values = []

    def insert(self, value, position='end'):
        self.values.append(value)
        self.last = len(self.values)
        tk.Listbox.insert(self, position, str(value))


    def set(self, values, showAttr=''):
        self.clear()
        for val in values:
            value = val[showAttr] if showAttr else str(val)
            # value = getattr(val, showAttr, None) if showAttr else str(val)
            self.insert(value)
        self.values = values

    def clicked(self, event=None):
        if self.callback:
            selected = self.selected
            if selected: self.callback(event=event, selected=self.selected)

    @property
    def selected(self):
        sels = self.curselection()
        if sels:
            select = []
            for sel in sels: select.append(self.values[sel])
            return select
Listbox = PLb = PRMP_Listbox