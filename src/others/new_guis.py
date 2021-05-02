from src.gui.gam.gam_apps import GaM_App
from prmp_lib.prmp_miscs.prmp_images import PRMP_ImageFile
from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime
from prmp_lib.prmp_gui import *
from src.gui.dc.dc_extensions import DC_Digits
from src.gui.gam.gam_extensions import GaM_Hierachy
from src.gui.gam.gam_images import *
from prmp_lib.prmp_gui.image_widgets import *
from prmp_lib.prmp_gui.plot_canvas import *
from prmp_lib.prmp_gui.scrollables import *

# from owode_dc import OWODE
import sys; sys.path.append('seen_others')
from test_dc import dcoffice as OWODE

OWODE.balanceAccounts()

relief = 'flat'
# relief = 'groove'

class Total_Label:
    font1 = PRMP_Theme.DEFAULT_FONT.copy()
    font1['size'] = 15
    font2 = PRMP_Theme.PRMP_FONT.copy()
    font2['size'] = 15
    anchors = {0: 'n', 1: 'ne', 2: 'e', 3: 'se', 4: 's', 5: 'sw', 6: 'w', 7: 'nw', 8: 'center'}

    def __init__(self, master, name='', y=0, h=0, text=''):
        Label(master, text=name, place=dict(y=y, h=h, relx=0, relw=.7), relief=relief, font=self.font1, hl=0, anchor=self.anchors[6])
        rw = .25
        self.edit = Label(master, text=text, place=dict(y=y, h=h, relx=1-rw, relw=rw), relief=relief, font=self.font2, hl=1, anchor=self.anchors[8], asEntry=1)

    def set(self, text): self.edit.config(text=text)


def rewrite_words(words):
    caps = [chr(a) for a in range(65, 91)]

    rw = ''
    for a in words:
        if a in caps: a = ' %s'%a
        rw += a
    return rw


class Tiled_DC_Digits(DC_Digits):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self._incomes.place(relx=0, rely=0, relh=.6, relw=.49)
        self._paidouts.place(relx=0, rely=.6, relh=.4, relw=.49)
        self._upfronts.place(relx=.5, rely=0, relh=.45, relw=.49)
        self._balances.place(relx=.5, rely=.45, relh=.55, relw=.49)


class DCOfficeWindow(GaM_App, PRMP_FillWidgets):
    
    def __init__(self, **kwargs):
        GaM_App.__init__(self, geo=(1500, 800), title=OWODE, themeIndex=60, resize=(0, 0), obj=OWODE, **kwargs)
        PRMP_FillWidgets.__init__(self)
    
    def _setupApp(self):
        align1 = 300
        # self.change_color(image=PRMP_ImageFile('blue_lux', inbuilt=1, inExt='jpeg').image)

        self.gam = PRMP_Image('gam', b64=GaM_PNGS['gam'], for_tk=1)
        self.red_gam = PRMP_Image('red_gam', b64=GaM_PNGS['red_gam'], for_tk=1)

        self.logo = PRMP_ImageSLabel(self.cont, imageKwargs=dict(prmpImage=self.gam), place=dict(x=2, y=2, relh=.25, w=align1), bindMenu=0, imgDelay=0, config=dict(relief=relief))
        self.logo.bind('<Enter>', self.changeLogo)
        self.logo.bind('<Leave>', self.changeLogo)

        managers = LabelFrame(self.cont, text='Managers', place=dict(x=2, rely=.3, w=align1, h=80), hl=0)
        self.areas_menu = Menubutton(managers, config=dict(text='Areas', style='Button.TMenubutton'), place=dict(relx=.02, y=0, relw=.45, relh=.85))
        self.areas_menu.bind('<3>', lambda e: print(e))
        self.accounts_menu = Menubutton(managers, config=dict(text='Accounts', style='Button.TMenubutton'), place=dict(relx=.52, y=0, relw=.45, relh=.85))

        Button(self.cont, text='BalanceAccount', command=OWODE.balanceAccounts, place=dict(x=50, rely=.5, w=150, h=30))

        t_h = 30
        h = len(OWODE.accountsManager[0]) * (t_h+4.55)
        t_y = t_h*2
        h = t_y+4.3

        totals = Frame(self.cont, place=dict(x=align1+20, y=2, w=400, h=h), relief=relief, hl=0)
        self.total_areas = Total_Label(totals, name='Areas', y=0, h=t_h)

        self.total_active_client_accounts = Total_Label(totals, name='Active Client Accounts', y=t_h, h=t_h)
        
        self.dc_digits = Tiled_DC_Digits(self.cont, place=dict(x=align1+10, y=h+10, h=350, w=560), relief=relief)

        self.plot = OptPlot(self.cont, place=dict(x=align1+8, y=h+370, w=556, h=300))

        self.list = ListBox(self.cont, place=dict(x=2, y=h+370, w=align1-10, h=300), listboxConfig=dict(selectmode='multiple'))
        Button(self.list, text='Load Plot', place=dict(relx=.63, rely=.8, relw=.3, relh=.1), command=self.doPlot)

        x = align1 + 560 + 10
        w = self.geo[0] - x - 2
        self.hierachy = GaM_Hierachy(self.cont, place=dict(x=x, y=2, w=w, relh=.99))

        self.addAfter(self.updateDatas)
        # self.after(10, sys.exit)

    def changeLogo(self, event):
        if event.type == tk.EventType.Leave: img = self.gam
        else: img = self.red_gam

        self.logo.loadImage(img)
    
    def updateDatas(self):
        area_menu = Menu(self.areas_menu)
        self.areas_menu["menu"] = area_menu
        for area in OWODE.areasManager: area_menu.add_command(label=area.name, command=lambda area=area: print(area))
        
        account_menu = Menu(self.accounts_menu)
        self.accounts_menu["menu"] = account_menu
        for account in OWODE.accountsManager: account_menu.add_command(label=account.name, command=lambda account=account: print(account))
        
        month = OWODE.accountsManager.last.month

        areas = OWODE.areasManager
        self.total_areas.set(len(areas))

        num = 0

        for area in areas:
            acc = area.accountsManager.getAccount(month=month)
            num += acc.ledgerNumbers

        self.total_active_client_accounts.set(num)

        self.dc_digits.update(OWODE.accounts[-1])

        self.hierachy.setColumns([('Name', '', '', 250), ['Date', {'date': 'date'}, '', 20], 'Active Date'])
        self.hierachy.viewObjs(OWODE)

        self._last = OWODE[-1]
        self._lists = [rm.className for rm in self._last]
        self.list.set(self._lists)

        self.doPlot()

    def doPlot(self):
        selected = self.list.selected or self._lists

        datas = self._last[selected]
        datas = [float(data) for data in datas]

        self.plot.load(xticks=selected, ys=[datas])





DCOfficeWindow()


