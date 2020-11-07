from .bases import *





class PRMP_Button(PRMP_Widget, tk.Button):
    
    def __init__(self, master=None, font=PTh.DEFAULT_BUTTON_FONT, asEntry=False, asLabel=False, tip=None, tipGeo=None, config={}, **kwargs):
        tk.Button.__init__(self, master=master, **config)
        PRMP_Widget.__init__(self, font=font, asEntry=asEntry, tip=tip, tipGeo=tipGeo, **config, **kwargs)
B = Button = PB = PRMP_Button


class PRMP_DateButton(B):
    def __init__(self, master=None, font=PTh.DEFAULT_FONT, asEntry=True, **kwargs):
        self.date = None
        from .dialogs import CalendarDialog, DateTime
        self.CD = CalendarDialog
        self.DT = DateTime
        super().__init__(master=master, command=self.action, font=font, asEntry=asEntry, **kwargs)
    
    def action(self):
        self.date = self.CD.generate(geo=(300, 200)).result
        self.set(str(self.date))
    
    def get(self): return self.date
    
    def set(self, date):
        if '-' in date: d, m, y = date.split('-')
        elif '/' in date: d, m, y = date.split('/')
        else: return
        self.date = self.DT.createDateTime(int(y), int(m), int(d))
        self['text'] = self.date
PDB = PRMP_DateButton


class PRMP_RegionButton(B):
    
    def __init__(self, master=None, region=None, **kwargs):
        super().__init__(master, command=self.openDetails, **kwargs)
        self.region = region
        self.set(region)
        self.bindEntryHighlight()
    
    def openDetails(self):
        
        # open RegionDetailsDialog
        pass
    
    def get(self): return self.region
    
    def set(self, region=None):
        if region:
            self.region = region
            self['text'] = region.name

PRB = PRMP_RegionButton

class PRMP_Canvas(PRMP_Widget, tk.Canvas):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Canvas.__init__(self, master=master, **config)
        PRMP_Widget.__init__(self, **config, **kwargs)
    
Ca = PCa = Canvas = PRMP_Canvas

class PRMP_Checkbutton(PRMP_Widget, tk.Checkbutton):
    
    def __init__(self, master=None, asLabel=False, config={}, **kwargs):
        self.var = tk.StringVar()
        tk.Checkbutton.__init__(self, master=master, variable=self.var, **config)
        PRMP_Widget.__init__(self, variable=self.var, asLabel=asLabel, **config, **kwargs)
        
        self.var.set('0')
        self.toggleSwitch()

Cb = PCb = Checkbutton = PRMP_Checkbutton


class PRMP_Frame(PRMP_Widget, tk.Frame):
    
    def __init__(self, master=None, bd=2, relief='flat', config={}, **kwargs):
        tk.Frame.__init__(self, master=master, relief=relief, bd=bd, **config)
        PRMP_Widget.__init__(self, relief=relief, **config, **kwargs)
        
F = PF = Frame = PRMP_Frame

class PRMP_Label(PRMP_Widget, tk.Label):
    
    def __init__(self, master=None, font=PRMP_Theme.DEFAULT_LABEL_FONT, tip=None, tipGeo=None, config={}, **kwargs):
        tk.Label.__init__(self, master=master, **config)
        PRMP_Widget.__init__(self, font=font, tip=tip, tipGeo=tipGeo, **config, **kwargs)
        
L = PL = Label = PRMP_Label

class PRMP_LabelFrame(PRMP_Widget, tk.LabelFrame):
    
    def __init__(self, master=None, bd=2, font=PRMP_Theme.DEFAULT_LABELFRAME_FONT, config={}, **kwargs):
        tk.LabelFrame.__init__(self, master=master, bd=bd, **config)
        PRMP_Widget.__init__(self, font=font, **config, **kwargs)
        
LF = LabelFrame = PRMP_LabelFrame



class PRMP_Radiobutton(PRMP_Widget, tk.Radiobutton):
    
    def __init__(self, master=None, asLabel=False, config={}, **kwargs):
        tk.Radiobutton.__init__(self, master=master, **config)
        PRMP_Widget.__init__(self, asLabel=asLabel, **config, **kwargs)

Rb = PRb = Radiobutton = PRMP_Radiobutton

class PRMP_Scrollbar(PRMP_Widget, ttk.Scrollbar):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Scrollbar.__init__(self, master, **config)
        PRMP_Widget.__init__(self, **config, **kwargs)
    
    def set(self, first, last): return ttk.Scrollbar.set(self, first, last)
        
PS = PRMP_Scrollbar


class PRMP_Treeview(PRMP_Widget, ttk.Treeview):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Treeview.__init__(self, master, **config)
        PRMP_Widget.__init__(self, **config, **kwargs)
    
    def set(self, *args):
        print(args)
        
PTv = PRMP_Treeview



class ImageLabel(PRMP_Label, ImageWidget):
    def __init__(self, master, imageFile=None, resize=(), thumb=(), **kwargs):
        PRMP_Label.__init__(self, master, **kwargs)
        ImageWidget.__init__(self, imageFile=imageFile, thumb=thumb, resize=resize)
    
IL = ImageLabel




class PRMP_Combobox(PRMP_Input, ttk.Combobox):
    
    def __init__(self, master=None, type_='', config={}, **kwargs):
        ttk.Combobox.__init__(self, master=master, **config)
        PRMP_Input.__init__(self, **config, **kwargs)
        self.values = []
        if type_.lower() == 'gender': self.changeValues(['Male', 'Female'])
    
    def changeValues(self, values):
        self.values = values
        self['values'] = values
    
    def getValues(self): return self['values']
    

Cx = PCx = Combobox = PRMP_Combobox

class PRMP_Entry(PRMP_Input, tk.Entry):
    
    def __init__(self, master=None, type_='text', config={}, **kwargs):
        tk.Entry.__init__(self, master=master, **config)
        PRMP_Input.__init__(self, **config, **kwargs)
        
        if type_.lower() == 'email':
            self.bind('<KeyRelease>', self.checkingEmail)
            self.verification = self.checkingEmail
    
    

E = PE = Entry = PRMP_Entry

class PRMP_Message(PRMP_Input, tk.Message):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Message.__init__(self, master=master, **config)
        PRMP_Input.__init__(self, **config, **kwargs)

PMs = PRMP_Message

class PRMP_Text(PRMP_Input, tk.Text):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Text.__init__(self, master=master, **config)
        PRMP_Input.__init__(self, **config, **kwargs)
        
    def _get(self): return tk.Text.get(self, '1.0', 'end').strip('\n')
    
    def set(self, values): self.clear(); self.insert('0.0', values)
    
    def clear(self): self.delete('0.0', 'end')
    
PTx = PRMP_Text





