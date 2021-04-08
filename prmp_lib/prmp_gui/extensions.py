from .core import *
from .miscs import create_container, bound_to_mousewheel, Columns, Column
from prmp.prmp_miscs.prmp_pics import *
from prmp.prmp_miscs.prmp_pics import _PIL_
from prmp.prmp_miscs.prmp_datetime import PRMP_DateTime

picTypes = ['Pictures {.jpg .png .jpeg .gif .xbm}']

class PRMP_FillWidgets(PRMP_Mixins):

    def __init__(self, values={}):
        self.__resultsWidgets = []
        self.__notEditables = []
        self.values = values
        self.fill = self.set
        self.empty = self.get

    def addResultsWidgets(self, child):
        if child not in self.__resultsWidgets:
            if isinstance(child, self.containers):
                for ch in child: self.addResultsWidgets(ch)
            else: self.__resultsWidgets.append(child)

    def addNotEditables(self, child):
        if child not in self.__notEditables:
            if isinstance(child, self.containers):
                for ch in child: self.addNotEditables(ch)
            else: self.__notEditables.append(child)

    def emptyWidgets(self, widgets=[]):
        widgets = widgets or self.resultsWidgets
        for widgetName in widgets:
            widget = self.getFromSelf(widgetName)
            if widget:
                B = widget.getFromSelf('Bottom', None)
                if B: B.set(B.getFromSelf('placeholder'))
                else: widget.set(widget.getFromSelf('placeholder', widget['text']))

    @property
    def notEditables(self): return self.__notEditables
    @property
    def resultsWidgets(self): return self.__resultsWidgets

    def set(self, values={}, widgets=[]):
        if values:
            widgets = widgets or self.__resultsWidgets
            for widgetName in widgets:
                widget = self.getFromSelf(widgetName)
                if widget:
                    # try:
                        val = values.get(widgetName, '')
                        widget.set(val)
                    # except Exception as er: print(f'ERROR {er}.')
                else: print(f'Error [{widgetName}, {widget}]')
            if isinstance(values, dict): self.values.update(values)
            return True
        else:
            if self.values: return self.set(self.values)

    def get(self, widgets=[]):
        result = {}

        widgets = widgets or self.__resultsWidgets
        for widgetName in widgets:
            if widgetName in self.__notEditables: continue

            wid = self.__dict__.get(widgetName)
            if wid:
                get = wid.get()
                verify = getattr(wid, 'verify', None)
                if verify and wid.required:
                    verified = verify()
                    if verified: result[widgetName] = get
                    else:
                        try: wid.flash()
                        except: pass

                        from .dialogs import PRMP_MsgBox
                        PRMP_MsgBox(self, title='Required Input', message=f'{widgetName.title()}* is required to proceed!', _type='error', okText='Understood')
                        return
                else: result[widgetName] = get
        return result
FW = PRMP_FillWidgets

class PRMP_SolidScreen(PRMP_MainWindow):
    def __init__(self, side='top-center', gaw=1, bd=12, geo=(),**kwargs):
        super().__init__(tm=1, gaw=gaw, geo=geo or (500, 500), side=side, **kwargs)

        self.container.configure(borderwidth=bd)

        self.paint()

SS = PRMP_SolidScreen

class PRMP_FramedCanvas(Frame):
    def __init__(self, master, canvasConfig={}, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = Canvas(self, **canvasConfig, place=dict(relx=.005, rely=.005, relh=.99, relw=.99))


class PRMP_Entry_Label(Label):

    def __init__(self, master, font='DEFAULT_FONT', **kwargs): super().__init__(master, asEntry=True, font=font, **kwargs)
Entry_Label = PRMP_Entry_Label


class PasswordEntry(SFrame):
    def __init__(self, master, **kwargs):
        '''
        a password widget that features a show button and action button.
        '''
        super().__init__(master, **kwargs)
        
        ffont = self.PRMP_FONT.copy()
        ffont['size'] = 20
        self.entry = Entry(self, show='*', place=dict(relx=0, rely=0, relw=.8, relh=1), relief='flat', font=ffont)
        self.entry.focus()
        
        res = 20

        view = PRMP_ImageSButton(self, place=dict(relx=.8, rely=0, relw=.1, relh=1), prmpImage='highlight', imageKwargs=dict(bindMenu=0, inbuilt=1, inExt='png'), resize=(res, res), tipKwargs=dict(text='Show'))
        view.bind('<ButtonPress-1>', self.view)
        view.bind('<ButtonRelease-1>', self.hide)

        PRMP_ImageSButton(self, place=dict(relx=.9, rely=0, relw=.1, relh=1), prmpImage='next', imageKwargs=dict(bindMenu=0, inbuilt=1, inExt='png'), command=self.action, resize=(res, res), tipKwargs=dict(text='Submit'))
    
    def hide(self, event=None): self.entry.configure(show='*')
    def view(self, event=None): self.entry.configure(show='')
    
    def action(self):
        pass
