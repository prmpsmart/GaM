
# miscs.py
import platform

from prmp_miscs import *
from prmp_miscs import _PIL_
import functools


def on_mousewheel(event, widget):
    what = 'units'
    what = 'pages'
    try:
        if platform.system() == 'Windows': widget.yview_scroll(-1*int(event.delta/120), what)
        elif platform.system() == 'Darwin': widget.yview_scroll(-1*int(event.delta),what)
        else:
            if event.num == 4:
                widget.yview_scroll(-1, what)
            elif event.num == 5:
                widget.yview_scroll(1, what)
    except: pass

def on_shiftmouse(event, widget):
    what = 'units'
    what = 'pages'
    try:
        if platform.system() == 'Windows': widget.xview_scroll(-1*int(event.delta/120), what)
        elif platform.system() == 'Darwin': widget.xview_scroll(-1*int(event.delta), what)
        else:
            if event.num == 4: widget.xview_scroll(-1, what)
            elif event.num == 5: widget.xview_scroll(1, what)
    except: pass

def bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: on_shiftmouse(e, child))

def unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def create_container(func):
    '''Creates a Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = PRMP_Frame(master)
        container.bind('<Enter>', lambda e: bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

def copyClassMethods(obj, copyClass, *args):

    for key, val in copyClass.__dict__.items():
        if key.startswith('__'): continue
        if callable(val):
            if obj.class_ == copyClass: func =functools. partial(val, obj)
            else: func = functools.partial(val, *args)

            setattr(obj, key, func)

class Col_Mixins(PRMP_Mixins):

    def __str__(self): return f'{self.className}({str(self.columns)})'

    def __getitem__(self, num): return self.columns[num]

    def __len__(self): return len(self.columns)

class Column(Col_Mixins):

    def __init__(self, index, column):
        self.subs = []
        self.index = '#%d'%index
        self.type = None
        value, width = '', 20
        self._attr = None

        if isinstance(column, (list, tuple)):
            l = len(column)
            self.text = column[0]
            self.attr = column[1] if (l>1) and column[1] else self.propertize(self.text)
            self.value = column[2] if (l>2) and column[2] else value
            self.width = column[3] if (l>3) and column[3] else 20

        elif isinstance(column, dict):
            self.text = column.get('text', value)
            self.attr = column.get('attr', None)
            if not self.attr: self.attr = self.propertize(self.text)
            if isinstance(self.attr, list):
                self._attr = self.attr
                self.attr = self.attr[0]
            self.value = column.get('value', value)
            self.width = column.get('width', None) or width
            self.type = column.get('type')

        else:
            self.text = column
            self.attr = self.propertize(self.text)
            self.value = value
            self.width = width

    def __repr__(self): return f'<{self.index}>'

    @property
    def columns(self): return [self.index, self.text, self.attr, self.value, self.width]

    def getFromObj(self, obj):
        if obj:
            try:
                val = ''
                if self._attr:
                    for attr in self._attr:
                        try:
                            val = obj[attr]
                            if val != None: break
                        except: pass
                else: val = obj[self.attr] or val

                if val:
                    if self.type: val = self.type(val)
                return val or ''

            except Exception as e: return ''

    def proof(self, obj): return self.getFromObj(obj) == self.value

    def __getitem__(self, item): return PRMP_Mixins.__getitem__(self, item)

class Columns(Col_Mixins):
    def __init__(self, columns):
        self.subs = self.columns = []
        self.process(columns)

    def process(self, columns):
        if not columns: return

        self.columns = []
        for col in columns: self.addColumn(col)
        return self.columns

    setColumns = process

    def getFromObj(self, obj): return [col.getFromObj(obj) for col in self]

    def addColumn(self, col):
        colObj = Column(len(self), col) if not isinstance(col, Column) else col
        self.columns.append(colObj)
        return colObj

    def remove(self, col):
        c = dict(text=col.text, attr=col.attr, width=col.width, value=col.value)
        for res in self:
            d = dict(text=res.text, attr=res.attr, width=res.width, value=res.value)
            if d == c: self.sub.remove(res)


# core.py
import os, time, random, ctypes, tkinter as tk, _tkinter
from tkinter.font import Font, families
import tkinter.ttk as ttk


# superclasses

'PRMP_GUI by PRMPSmart prmpsmart@gmail.com'

class PRMP_Theme(PRMP_Mixins):
    # exerpt from PySimpleGUI theming engine

    BLUES = ("#082567", "#0A37A3", "#00345B")
    PURPLES = ("#480656", "#4F2398", "#380474")
    GREENS = ("#01826B", "#40A860", "#96D2AB", "#00A949", "#003532")
    YELLOWS = ("#F3FB62", "#F0F595")
    TANS = ("#FFF9D5", "#F4EFCF", "#DDD8BA")
    NICE_BUTTON_COLORS = ((GREENS[3], TANS[0]), ('#000000', '#FFFFFF'), ('#FFFFFF', '#000000'), (YELLOWS[0], PURPLES[1]), (YELLOWS[0], GREENS[3]), (YELLOWS[0], BLUES[2]))
    COLOR_SYSTEM_DEFAULT = 'SystemButtonFace'
    DEFAULT_BUTTON_COLOR = ('white', BLUES[0])
    OFFICIAL_PRMPSMART_BUTTON_COLOR = ('white', BLUES[0])
    DEFAULT_ERROR_BUTTON_COLOR = ("#FFFFFF", "#FF0000")
    DEFAULT_FOREGROUND_COLOR = 'black'
    DEFAULT_BACKGROUND_COLOR = COLOR_SYSTEM_DEFAULT
    DEFAULT_ELEMENT_BACKGROUND_COLOR = None
    DEFAULT_ELEMENT_TEXT_COLOR = COLOR_SYSTEM_DEFAULT
    DEFAULT_TEXT_ELEMENT_BACKGROUND_COLOR = None
    DEFAULT_INPUT_ELEMENTS_COLOR = COLOR_SYSTEM_DEFAULT
    DEFAULT_INPUT_TEXT_COLOR = COLOR_SYSTEM_DEFAULT
    DEFAULT_SCROLLBAR_COLOR = None
    DEFAULT_PROGRESS_BAR_COLOR = (GREENS[0], '#D0D0D0')
    DEFAULT_PROGRESS_BAR_COMPUTE = ('#000000', '#000000')
    DEFAULT_PROGRESS_BAR_COLOR_OFFICIAL = (GREENS[0], '#D0D0D0')
    DEFAULT_HIGHLIGHT_BG = 'white'
    DEFAULT_HIGHLIGHT_BG = '#004080'

    DEFAULT_RELIEF = 'groove'

    THEMES_DICTS = {
        'SystemDefault': {'BACKGROUND': OFFICIAL_PRMPSMART_BUTTON_COLOR[1], 'TEXT': OFFICIAL_PRMPSMART_BUTTON_COLOR[0], 'INPUT': OFFICIAL_PRMPSMART_BUTTON_COLOR[1], 'TEXT_INPUT': 'yellow', 'SCROLL': COLOR_SYSTEM_DEFAULT, 'BUTTON': OFFICIAL_PRMPSMART_BUTTON_COLOR, 'PROGRESS': COLOR_SYSTEM_DEFAULT},
        'SystemDefaultForReal': {'BACKGROUND': COLOR_SYSTEM_DEFAULT, 'TEXT': COLOR_SYSTEM_DEFAULT, 'INPUT': COLOR_SYSTEM_DEFAULT, 'TEXT_INPUT': COLOR_SYSTEM_DEFAULT, 'SCROLL': COLOR_SYSTEM_DEFAULT, 'BUTTON': COLOR_SYSTEM_DEFAULT, 'PROGRESS': COLOR_SYSTEM_DEFAULT},
        'SystemDefault1': {'BACKGROUND': COLOR_SYSTEM_DEFAULT, 'TEXT': COLOR_SYSTEM_DEFAULT, 'INPUT': COLOR_SYSTEM_DEFAULT, 'TEXT_INPUT': COLOR_SYSTEM_DEFAULT, 'SCROLL': COLOR_SYSTEM_DEFAULT, 'BUTTON': COLOR_SYSTEM_DEFAULT, 'PROGRESS': COLOR_SYSTEM_DEFAULT},
        'Material1': {'BACKGROUND': '#E3F2FD', 'TEXT': '#000000', 'INPUT': '#86A8FF', 'TEXT_INPUT': '#000000', 'SCROLL': '#86A8FF', 'BUTTON': ('#FFFFFF', '#5079D3'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'ACCENT1': '#FF0266', 'ACCENT2': '#FF5C93', 'ACCENT3': '#C5003C'},
        'Material2': {'BACKGROUND': '#FAFAFA', 'TEXT': '#000000', 'INPUT': '#004EA1', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#5EA7FF', 'BUTTON': ('#FFFFFF', '#0079D3'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'ACCENT1': '#FF0266', 'ACCENT2': '#FF5C93', 'ACCENT3': '#C5003C'},
        'Reddit': {'BACKGROUND': '#ffffff', 'TEXT': '#1a1a1b', 'INPUT': '#dae0e6', 'TEXT_INPUT': '#222222', 'SCROLL': '#a5a4a4', 'BUTTON': ('#FFFFFF', '#0079d3'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE,'SLIDER_DEPTH': 0, 'ACCENT1': '#ff5414', 'ACCENT2': '#33a8ff', 'ACCENT3': '#dbf0ff'},
        'Topanga': {'BACKGROUND': '#282923', 'TEXT': '#E7DB74', 'INPUT': '#393a32', 'TEXT_INPUT': '#E7C855', 'SCROLL': '#E7C855', 'BUTTON': ('#E7C855', '#284B5A'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'ACCENT1': '#c15226', 'ACCENT2': '#7a4d5f', 'ACCENT3': '#889743'},
        'GreenTan': {'BACKGROUND': '#9FB8AD', 'TEXT': COLOR_SYSTEM_DEFAULT, 'INPUT': '#F7F3EC', 'TEXT_INPUT': '#000000', 'SCROLL': '#F7F3EC', 'BUTTON': ('#FFFFFF', '#475841'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'Dark': {'BACKGROUND': '#404040', 'TEXT': '#FFFFFF', 'INPUT': '#4D4D4D', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#707070', 'BUTTON': ('#FFFFFF', '#004F00'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightGreen': {'BACKGROUND': '#B7CECE', 'TEXT': '#000000', 'INPUT': '#FDFFF7', 'TEXT_INPUT': '#000000', 'SCROLL': '#FDFFF7', 'BUTTON': ('#FFFFFF', '#658268'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'ACCENT1': '#76506d', 'ACCENT2': '#5148f1', 'ACCENT3': '#0a1c84'},
        'Dark2': {'BACKGROUND': '#404040', 'TEXT': '#FFFFFF', 'INPUT': '#FFFFFF', 'TEXT_INPUT': '#000000', 'SCROLL': '#707070', 'BUTTON': ('#FFFFFF', '#004F00'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'Black': {'BACKGROUND': '#000000', 'TEXT': '#FFFFFF', 'INPUT': '#4D4D4D', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#707070', 'BUTTON': ('#000000', '#FFFFFF'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'Tan': {'BACKGROUND': '#fdf6e3', 'TEXT': '#268bd1', 'INPUT': '#eee8d5', 'TEXT_INPUT': '#6c71c3', 'SCROLL': '#eee8d5', 'BUTTON': ('#FFFFFF', '#063542'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'TanBlue': {'BACKGROUND': '#e5dece', 'TEXT': '#063289', 'INPUT': '#f9f8f4', 'TEXT_INPUT': '#242834', 'SCROLL': '#eee8d5', 'BUTTON': ('#FFFFFF', '#063289'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkTanBlue': {'BACKGROUND': '#242834', 'TEXT': '#dfe6f8', 'INPUT': '#97755c', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#a9afbb', 'BUTTON': ('#FFFFFF', '#063289'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkAmber': {'BACKGROUND': '#2c2825', 'TEXT': '#fdcb52', 'INPUT': '#705e52', 'TEXT_INPUT': '#fdcb52', 'SCROLL': '#705e52', 'BUTTON': ('#000000', '#fdcb52'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkBlue': {'BACKGROUND': '#1a2835', 'TEXT': '#d1ecff', 'INPUT': '#335267', 'TEXT_INPUT': '#acc2d0', 'SCROLL': '#1b6497', 'BUTTON': ('#000000', '#fafaf8'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'Reds': {'BACKGROUND': '#280001', 'TEXT': '#FFFFFF', 'INPUT': '#d8d584', 'TEXT_INPUT': '#000000', 'SCROLL': '#763e00', 'BUTTON': ('#000000', '#daad28'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'Green': {'BACKGROUND': '#82a459', 'TEXT': '#000000', 'INPUT': '#d8d584', 'TEXT_INPUT': '#000000', 'SCROLL': '#e3ecf3', 'BUTTON': ('#FFFFFF', '#517239'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'BluePurple': {'BACKGROUND': '#A5CADD', 'TEXT': '#6E266E', 'INPUT': '#E0F5FF', 'TEXT_INPUT': '#000000', 'SCROLL': '#E0F5FF', 'BUTTON': ('#FFFFFF', '#303952'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'Purple': {'BACKGROUND': '#B0AAC2', 'TEXT': '#000000', 'INPUT': '#F2EFE8', 'SCROLL': '#F2EFE8', 'TEXT_INPUT': '#000000', 'BUTTON': ('#000000', '#C2D4D8'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE,'SLIDER_DEPTH': 0},
        'BlueMono': {'BACKGROUND': '#AAB6D3', 'TEXT': '#000000', 'INPUT': '#F1F4FC', 'SCROLL': '#F1F4FC', 'TEXT_INPUT': '#000000', 'BUTTON': ('#FFFFFF', '#7186C7'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'GreenMono': {'BACKGROUND': '#A8C1B4', 'TEXT': '#000000', 'INPUT': '#DDE0DE', 'SCROLL': '#E3E3E3', 'TEXT_INPUT': '#000000', 'BUTTON': ('#FFFFFF', '#6D9F85'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'BrownBlue': {'BACKGROUND': '#64778d', 'TEXT': '#FFFFFF', 'INPUT': '#f0f3f7', 'SCROLL': '#A6B2BE', 'TEXT_INPUT': '#000000', 'BUTTON': ('#FFFFFF', '#283b5b'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'BrightColors': {'BACKGROUND': '#b4ffb4', 'TEXT': '#000000', 'INPUT': '#ffff64', 'SCROLL': '#ffb482', 'TEXT_INPUT': '#000000', 'BUTTON': ('#000000', '#ffa0dc'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'NeutralBlue': {'BACKGROUND': '#92aa9d', 'TEXT': '#000000', 'INPUT': '#fcfff6', 'SCROLL': '#fcfff6', 'TEXT_INPUT': '#000000', 'BUTTON': ('#000000', '#d0dbbd'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'Kayak': {'BACKGROUND': '#a7ad7f', 'TEXT': '#000000', 'INPUT': '#e6d3a8', 'SCROLL': '#e6d3a8', 'TEXT_INPUT': '#000000', 'BUTTON': ('#FFFFFF', '#5d907d'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'SandyBeach': {'BACKGROUND': '#efeccb', 'TEXT': '#012f2f', 'INPUT': '#e6d3a8', 'SCROLL': '#e6d3a8', 'TEXT_INPUT': '#012f2f', 'BUTTON': ('#FFFFFF', '#046380'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'TealMono': {'BACKGROUND': '#a8cfdd', 'TEXT': '#000000', 'INPUT': '#dfedf2', 'SCROLL': '#dfedf2', 'TEXT_INPUT': '#000000', 'BUTTON': ('#FFFFFF', '#183440'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},

        'Default':   {'BACKGROUND': COLOR_SYSTEM_DEFAULT, 'TEXT': 'black', 'INPUT': 'black', 'TEXT_INPUT': 'black', 'SCROLL': 'black', 'BUTTON': 'black', 'PROGRESS': 'black'},
        'Default1':  {'BACKGROUND': COLOR_SYSTEM_DEFAULT, 'TEXT': 'black', 'INPUT': 'black', 'TEXT_INPUT': COLOR_SYSTEM_DEFAULT, 'SCROLL': COLOR_SYSTEM_DEFAULT, 'BUTTON': 'black', 'PROGRESS': 'black'},
        'DefaultNoMoreNagging':  {'BACKGROUND': COLOR_SYSTEM_DEFAULT, 'TEXT': 'black', 'INPUT': 'black', 'TEXT_INPUT': COLOR_SYSTEM_DEFAULT, 'SCROLL': 'black', 'BUTTON': OFFICIAL_PRMPSMART_BUTTON_COLOR, 'PROGRESS': 'black'},
        'LightBlue': {'BACKGROUND': '#E3F2FD', 'TEXT': '#000000', 'INPUT': '#86A8FF', 'TEXT_INPUT': '#000000', 'SCROLL': '#86A8FF', 'BUTTON': ('#FFFFFF', '#5079D3'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'ACCENT1': '#FF0266', 'ACCENT2': '#FF5C93', 'ACCENT3': '#C5003C'},
        'LightGrey': {'BACKGROUND': '#FAFAFA', 'TEXT': '#000000', 'INPUT': '#004EA1', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#5EA7FF', 'BUTTON': ('#FFFFFF', '#0079D3'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'ACCENT1': '#FF0266', 'ACCENT2': '#FF5C93', 'ACCENT3': '#C5003C'},
        'LightGrey1': {'BACKGROUND': '#ffffff', 'TEXT': '#1a1a1b', 'INPUT': '#dae0e6', 'TEXT_INPUT': '#222222', 'SCROLL': '#a5a4a4', 'BUTTON': ('#FFFFFF', '#0079d3'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'ACCENT1': '#ff5414', 'ACCENT2': '#33a8ff', 'ACCENT3': '#dbf0ff'},
        'DarkBrown': {'BACKGROUND': '#282923', 'TEXT': '#E7DB74', 'INPUT': '#393a32', 'TEXT_INPUT': '#E7C855', 'SCROLL': '#E7C855', 'BUTTON': ('#E7C855', '#284B5A'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'ACCENT1': '#c15226', 'ACCENT2': '#7a4d5f', 'ACCENT3': '#889743'},
        'LightGreen1': {'BACKGROUND': '#9FB8AD', 'TEXT': '#000000', 'INPUT': '#F7F3EC', 'TEXT_INPUT': '#000000', 'SCROLL': '#F7F3EC', 'BUTTON': ('#FFFFFF', '#475841'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkGrey': {'BACKGROUND': '#404040', 'TEXT': '#FFFFFF', 'INPUT': '#4D4D4D', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#707070', 'BUTTON': ('#FFFFFF', '#004F00'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightGreen2': {'BACKGROUND': '#B7CECE', 'TEXT': '#000000', 'INPUT': '#FDFFF7', 'TEXT_INPUT': '#000000', 'SCROLL': '#FDFFF7', 'BUTTON': ('#FFFFFF', '#658268'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'ACCENT1': '#76506d', 'ACCENT2': '#5148f1', 'ACCENT3': '#0a1c84'},
        'DarkGrey1': {'BACKGROUND': '#404040', 'TEXT': '#FFFFFF', 'INPUT': '#FFFFFF', 'TEXT_INPUT': '#000000', 'SCROLL': '#707070', 'BUTTON': ('#FFFFFF', '#004F00'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkBlack': {'BACKGROUND': '#000000', 'TEXT': '#FFFFFF', 'INPUT': '#4D4D4D', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#707070', 'BUTTON': ('#000000', '#FFFFFF'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightBrown': {'BACKGROUND': '#fdf6e3', 'TEXT': '#268bd1', 'INPUT': '#eee8d5', 'TEXT_INPUT': '#6c71c3', 'SCROLL': '#eee8d5', 'BUTTON': ('#FFFFFF', '#063542'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightBrown1': {'BACKGROUND': '#e5dece', 'TEXT': '#063289', 'INPUT': '#f9f8f4', 'TEXT_INPUT': '#242834', 'SCROLL': '#eee8d5', 'BUTTON': ('#FFFFFF', '#063289'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkBlue1': {'BACKGROUND': '#242834', 'TEXT': '#dfe6f8', 'INPUT': '#97755c', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#a9afbb', 'BUTTON': ('#FFFFFF', '#063289'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkBrown1': {'BACKGROUND': '#2c2825', 'TEXT': '#fdcb52', 'INPUT': '#705e52', 'TEXT_INPUT': '#fdcb52', 'SCROLL': '#705e52', 'BUTTON': ('#000000', '#fdcb52'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkBlue2': {'BACKGROUND': '#1a2835', 'TEXT': '#d1ecff', 'INPUT': '#335267', 'TEXT_INPUT': '#acc2d0', 'SCROLL': '#1b6497', 'BUTTON': ('#000000', '#fafaf8'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkBrown2': {'BACKGROUND': '#280001', 'TEXT': '#FFFFFF', 'INPUT': '#d8d584', 'TEXT_INPUT': '#000000', 'SCROLL': '#763e00', 'BUTTON': ('#000000', '#daad28'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkGreen': {'BACKGROUND': '#82a459', 'TEXT': '#000000', 'INPUT': '#d8d584', 'TEXT_INPUT': '#000000', 'SCROLL': '#e3ecf3', 'BUTTON': ('#FFFFFF', '#517239'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightBlue1': {'BACKGROUND': '#A5CADD', 'TEXT': '#6E266E', 'INPUT': '#E0F5FF', 'TEXT_INPUT': '#000000', 'SCROLL': '#E0F5FF', 'BUTTON': ('#FFFFFF', '#303952'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightPurple': {'BACKGROUND': '#B0AAC2', 'TEXT': '#000000', 'INPUT': '#F2EFE8', 'SCROLL': '#F2EFE8', 'TEXT_INPUT': '#000000', 'BUTTON': ('#000000', '#C2D4D8'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightBlue2': {'BACKGROUND': '#AAB6D3', 'TEXT': '#000000', 'INPUT': '#F1F4FC', 'SCROLL': '#F1F4FC', 'TEXT_INPUT': '#000000', 'BUTTON': ('#FFFFFF', '#7186C7'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightGreen3': {'BACKGROUND': '#A8C1B4', 'TEXT': '#000000', 'INPUT': '#DDE0DE', 'SCROLL': '#E3E3E3', 'TEXT_INPUT': '#000000', 'BUTTON': ('#FFFFFF', '#6D9F85'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkBlue3': {'BACKGROUND': '#64778d', 'TEXT': '#FFFFFF', 'INPUT': '#f0f3f7', 'SCROLL': '#A6B2BE', 'TEXT_INPUT': '#000000', 'BUTTON': ('#FFFFFF', '#283b5b'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightGreen4': {'BACKGROUND': '#b4ffb4', 'TEXT': '#000000', 'INPUT': '#ffff64', 'SCROLL': '#ffb482', 'TEXT_INPUT': '#000000', 'BUTTON': ('#000000', '#ffa0dc'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightGreen5': {'BACKGROUND': '#92aa9d', 'TEXT': '#000000', 'INPUT': '#fcfff6', 'SCROLL': '#fcfff6', 'TEXT_INPUT': '#000000', 'BUTTON': ('#000000', '#d0dbbd'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightBrown2': {'BACKGROUND': '#a7ad7f', 'TEXT': '#000000', 'INPUT': '#e6d3a8', 'SCROLL': '#e6d3a8', 'TEXT_INPUT': '#000000', 'BUTTON': ('#FFFFFF', '#5d907d'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightBrown3': {'BACKGROUND': '#efeccb', 'TEXT': '#012f2f', 'INPUT': '#e6d3a8', 'SCROLL': '#e6d3a8', 'TEXT_INPUT': '#012f2f', 'BUTTON': ('#FFFFFF', '#046380'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightBlue3': {'BACKGROUND': '#a8cfdd', 'TEXT': '#000000', 'INPUT': '#dfedf2', 'SCROLL': '#dfedf2', 'TEXT_INPUT': '#000000', 'BUTTON': ('#FFFFFF', '#183440'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'LightBrown4': {'BACKGROUND': '#d7c79e', 'TEXT': '#a35638', 'INPUT': '#9dab86', 'TEXT_INPUT': '#000000', 'SCROLL': '#a35638', 'BUTTON': ('#FFFFFF', '#a35638'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#a35638', '#9dab86', '#e08f62', '#d7c79e']},
        'DarkTeal': {'BACKGROUND': '#003f5c', 'TEXT': '#fb5b5a', 'INPUT': '#bc4873', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#bc4873', 'BUTTON': ('#FFFFFF', '#fb5b5a'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#003f5c', '#472b62', '#bc4873', '#fb5b5a']},
        'DarkPurple': {'BACKGROUND': '#472b62', 'TEXT': '#fb5b5a', 'INPUT': '#bc4873', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#bc4873', 'BUTTON': ('#FFFFFF', '#472b62'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#003f5c', '#472b62', '#bc4873', '#fb5b5a']},
        'LightGreen6': {'BACKGROUND': '#eafbea', 'TEXT': '#1f6650', 'INPUT': '#6f9a8d', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#1f6650', 'BUTTON': ('#FFFFFF', '#1f6650'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#1f6650', '#6f9a8d', '#ea5e5e', '#eafbea']},
        'DarkGrey2': {'BACKGROUND': '#2b2b28', 'TEXT': '#f8f8f8', 'INPUT': '#f1d6ab', 'TEXT_INPUT': '#000000', 'SCROLL': '#f1d6ab', 'BUTTON': ('#2b2b28', '#e3b04b'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#2b2b28', '#e3b04b', '#f1d6ab', '#f8f8f8']},
        'LightBrown6': {'BACKGROUND': '#f9b282', 'TEXT': '#8f4426', 'INPUT': '#de6b35', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#8f4426', 'BUTTON': ('#FFFFFF', '#8f4426'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#8f4426', '#de6b35', '#64ccda', '#f9b282']},
        'DarkTeal1': {'BACKGROUND': '#396362', 'TEXT': '#ffe7d1', 'INPUT': '#f6c89f', 'TEXT_INPUT': '#000000', 'SCROLL': '#f6c89f', 'BUTTON': ('#ffe7d1', '#4b8e8d'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#396362', '#4b8e8d', '#f6c89f', '#ffe7d1']},
        'LightBrown7': {'BACKGROUND': '#f6c89f', 'TEXT': '#396362', 'INPUT': '#4b8e8d', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#396362', 'BUTTON': ('#FFFFFF', '#396362'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#396362', '#4b8e8d', '#f6c89f', '#ffe7d1']},
        'DarkPurple1': {'BACKGROUND': '#0c093c', 'TEXT': '#fad6d6', 'INPUT': '#eea5f6', 'TEXT_INPUT': '#000000', 'SCROLL': '#eea5f6', 'BUTTON': ('#FFFFFF', '#df42d1'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#0c093c', '#df42d1', '#eea5f6', '#fad6d6']},
        'DarkGrey3': {'BACKGROUND': '#211717', 'TEXT': '#dfddc7', 'INPUT': '#f58b54', 'TEXT_INPUT': '#000000', 'SCROLL': '#f58b54', 'BUTTON': ('#dfddc7', '#a34a28'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#211717', '#a34a28', '#f58b54', '#dfddc7']},
        'LightBrown8': {'BACKGROUND': '#dfddc7', 'TEXT': '#211717', 'INPUT': '#a34a28', 'TEXT_INPUT': '#dfddc7', 'SCROLL': '#211717', 'BUTTON': ('#dfddc7', '#a34a28'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#211717', '#a34a28', '#f58b54', '#dfddc7']},
        'DarkBlue4': {'BACKGROUND': '#494ca2', 'TEXT': '#e3e7f1', 'INPUT': '#c6cbef', 'TEXT_INPUT': '#000000', 'SCROLL': '#c6cbef', 'BUTTON': ('#FFFFFF', '#8186d5'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#494ca2', '#8186d5', '#c6cbef', '#e3e7f1']},
        'LightBlue4': {'BACKGROUND': '#5c94bd', 'TEXT': '#470938', 'INPUT': '#1a3e59', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#470938', 'BUTTON': ('#FFFFFF', '#470938'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#470938', '#1a3e59', '#5c94bd', '#f2d6eb']},
        'DarkTeal2': {'BACKGROUND': '#394a6d', 'TEXT': '#c0ffb3', 'INPUT': '#52de97', 'TEXT_INPUT': '#000000', 'SCROLL': '#52de97', 'BUTTON': ('#c0ffb3', '#394a6d'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#394a6d', '#3c9d9b', '#52de97', '#c0ffb3']},
        'DarkTeal3': {'BACKGROUND': '#3c9d9b', 'TEXT': '#c0ffb3', 'INPUT': '#52de97', 'TEXT_INPUT': '#000000', 'SCROLL': '#52de97', 'BUTTON': ('#c0ffb3', '#394a6d'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#394a6d', '#3c9d9b', '#52de97', '#c0ffb3']},
        'DarkPurple5': {'BACKGROUND': '#730068', 'TEXT': '#f6f078', 'INPUT': '#01d28e', 'TEXT_INPUT': '#000000', 'SCROLL': '#01d28e', 'BUTTON': ('#f6f078', '#730068'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#730068', '#434982', '#01d28e', '#f6f078']},
        'DarkPurple2': {'BACKGROUND': '#202060', 'TEXT': '#b030b0', 'INPUT': '#602080', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#602080', 'BUTTON': ('#FFFFFF', '#202040'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#202040', '#202060', '#602080', '#b030b0']},
        'DarkBlue5': {'BACKGROUND': '#000272', 'TEXT': '#ff6363', 'INPUT': '#a32f80', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#a32f80', 'BUTTON': ('#FFFFFF', '#341677'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#000272', '#341677', '#a32f80', '#ff6363']},
        'LightGrey2': {'BACKGROUND': '#f6f6f6', 'TEXT': '#420000', 'INPUT': '#d4d7dd', 'TEXT_INPUT': '#420000', 'SCROLL': '#420000', 'BUTTON': ('#420000', '#d4d7dd'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#420000', '#d4d7dd', '#eae9e9', '#f6f6f6']},
        'LightGrey3': {'BACKGROUND': '#eae9e9', 'TEXT': '#420000', 'INPUT': '#d4d7dd', 'TEXT_INPUT': '#420000', 'SCROLL': '#420000', 'BUTTON': ('#420000', '#d4d7dd'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#420000', '#d4d7dd', '#eae9e9', '#f6f6f6']},
        'DarkBlue6': {'BACKGROUND': '#01024e', 'TEXT': '#ff6464', 'INPUT': '#8b4367', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#8b4367', 'BUTTON': ('#FFFFFF', '#543864'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#01024e', '#543864', '#8b4367', '#ff6464']},
        'DarkBlue7': {'BACKGROUND': '#241663', 'TEXT': '#eae7af', 'INPUT': '#a72693', 'TEXT_INPUT': '#eae7af', 'SCROLL': '#a72693', 'BUTTON': ('#eae7af', '#160f30'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#160f30', '#241663', '#a72693', '#eae7af']},
        'LightBrown9': {'BACKGROUND': '#f6d365', 'TEXT': '#3a1f5d', 'INPUT': '#c83660', 'TEXT_INPUT': '#f6d365', 'SCROLL': '#3a1f5d', 'BUTTON': ('#f6d365', '#c83660'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#3a1f5d', '#c83660', '#e15249', '#f6d365']},
        'DarkPurple3': {'BACKGROUND': '#6e2142', 'TEXT': '#ffd692', 'INPUT': '#e16363', 'TEXT_INPUT': '#ffd692', 'SCROLL': '#e16363', 'BUTTON': ('#ffd692', '#943855'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#6e2142', '#943855', '#e16363', '#ffd692']},
        'LightBrown10': {'BACKGROUND': '#ffd692', 'TEXT': '#6e2142', 'INPUT': '#943855', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#6e2142', 'BUTTON': ('#FFFFFF', '#6e2142'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#6e2142', '#943855', '#e16363', '#ffd692']},
        'DarkPurple4': {'BACKGROUND': '#200f21', 'TEXT': '#f638dc', 'INPUT': '#5a3d5c', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#5a3d5c', 'BUTTON': ('#FFFFFF', '#382039'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#200f21', '#382039', '#5a3d5c', '#f638dc']},
        'LightBlue5': {'BACKGROUND': '#b2fcff', 'TEXT': '#3e64ff', 'INPUT': '#5edfff', 'TEXT_INPUT': '#000000', 'SCROLL': '#3e64ff', 'BUTTON': ('#FFFFFF', '#3e64ff'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#3e64ff', '#5edfff', '#b2fcff', '#ecfcff']},
        'DarkTeal4': {'BACKGROUND': '#464159', 'TEXT': '#c7f0db', 'INPUT': '#8bbabb', 'TEXT_INPUT': '#000000', 'SCROLL': '#8bbabb', 'BUTTON': ('#FFFFFF', '#6c7b95'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#464159', '#6c7b95', '#8bbabb', '#c7f0db']},
        'LightTeal': {'BACKGROUND': '#c7f0db', 'TEXT': '#464159', 'INPUT': '#6c7b95', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#464159', 'BUTTON': ('#FFFFFF', '#464159'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#464159', '#6c7b95', '#8bbabb', '#c7f0db']},
        'DarkTeal5': {'BACKGROUND': '#8bbabb', 'TEXT': '#464159', 'INPUT': '#6c7b95', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#464159', 'BUTTON': ('#c7f0db', '#6c7b95'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#464159', '#6c7b95', '#8bbabb', '#c7f0db']},
        'LightGrey4': {'BACKGROUND': '#faf5ef', 'TEXT': '#672f2f', 'INPUT': '#99b19c', 'TEXT_INPUT': '#672f2f', 'SCROLL': '#672f2f', 'BUTTON': ('#672f2f', '#99b19c'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#672f2f', '#99b19c', '#d7d1c9', '#faf5ef']},
        'LightGreen7': {'BACKGROUND': '#99b19c', 'TEXT': '#faf5ef', 'INPUT': '#d7d1c9', 'TEXT_INPUT': '#000000', 'SCROLL': '#d7d1c9', 'BUTTON': ('#FFFFFF', '#99b19c'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#672f2f', '#99b19c', '#d7d1c9', '#faf5ef']},
        'LightGrey5': {'BACKGROUND': '#d7d1c9', 'TEXT': '#672f2f', 'INPUT': '#99b19c', 'TEXT_INPUT': '#672f2f', 'SCROLL': '#672f2f', 'BUTTON': ('#FFFFFF', '#672f2f'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#672f2f', '#99b19c', '#d7d1c9', '#faf5ef']},
        'DarkBrown3': {'BACKGROUND': '#a0855b', 'TEXT': '#f9f6f2', 'INPUT': '#f1d6ab', 'TEXT_INPUT': '#000000', 'SCROLL': '#f1d6ab', 'BUTTON': ('#FFFFFF', '#38470b'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#38470b', '#a0855b', '#f1d6ab', '#f9f6f2']},
        'LightBrown11': {'BACKGROUND': '#f1d6ab', 'TEXT': '#38470b', 'INPUT': '#a0855b', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#38470b', 'BUTTON': ('#f9f6f2', '#a0855b'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#38470b', '#a0855b', '#f1d6ab', '#f9f6f2']},
        'DarkRed': {'BACKGROUND': '#83142c', 'TEXT': '#f9d276', 'INPUT': '#ad1d45', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#ad1d45', 'BUTTON': ('#f9d276', '#ad1d45'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#44000d', '#83142c', '#ad1d45', '#f9d276']},
        'DarkTeal6': {'BACKGROUND': '#204969', 'TEXT': '#fff7f7', 'INPUT': '#dadada', 'TEXT_INPUT': '#000000', 'SCROLL': '#dadada', 'BUTTON': ('#000000', '#fff7f7'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#204969', '#08ffc8', '#dadada', '#fff7f7']},
        'DarkBrown4': {'BACKGROUND': '#252525', 'TEXT': '#ff0000', 'INPUT': '#af0404', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#af0404', 'BUTTON': ('#FFFFFF', '#252525'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#252525', '#414141', '#af0404', '#ff0000']},
        'LightYellow': {'BACKGROUND': '#f4ff61', 'TEXT': '#27aa80', 'INPUT': '#32ff6a', 'TEXT_INPUT': '#000000', 'SCROLL': '#27aa80', 'BUTTON': ('#f4ff61', '#27aa80'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#27aa80', '#32ff6a', '#a8ff3e', '#f4ff61']},
        'DarkGreen1': {'BACKGROUND': '#2b580c', 'TEXT': '#fdef96', 'INPUT': '#f7b71d', 'TEXT_INPUT': '#000000', 'SCROLL': '#f7b71d', 'BUTTON': ('#fdef96', '#2b580c'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#2b580c', '#afa939', '#f7b71d', '#fdef96']},
        'LightGreen8': {'BACKGROUND': '#c8dad3', 'TEXT': '#63707e', 'INPUT': '#93b5b3', 'TEXT_INPUT': '#000000', 'SCROLL': '#63707e', 'BUTTON': ('#FFFFFF', '#63707e'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#63707e', '#93b5b3', '#c8dad3', '#f2f6f5']},
        'DarkTeal7': {'BACKGROUND': '#248ea9', 'TEXT': '#fafdcb', 'INPUT': '#aee7e8', 'TEXT_INPUT': '#000000', 'SCROLL': '#aee7e8', 'BUTTON': ('#000000', '#fafdcb'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#248ea9', '#28c3d4', '#aee7e8', '#fafdcb']},
        'DarkBlue8': {'BACKGROUND': '#454d66', 'TEXT': '#d9d872', 'INPUT': '#58b368', 'TEXT_INPUT': '#000000', 'SCROLL': '#58b368', 'BUTTON': ('#000000', '#009975'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#009975', '#454d66', '#58b368', '#d9d872']},
        'DarkBlue9': {'BACKGROUND': '#263859', 'TEXT': '#ff6768', 'INPUT': '#6b778d', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#6b778d', 'BUTTON': ('#ff6768', '#263859'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#17223b', '#263859', '#6b778d', '#ff6768']},
        'DarkBlue10': {'BACKGROUND': '#0028ff', 'TEXT': '#f1f4df', 'INPUT': '#10eaf0', 'TEXT_INPUT': '#000000', 'SCROLL': '#10eaf0', 'BUTTON': ('#f1f4df', '#24009c'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#24009c', '#0028ff', '#10eaf0', '#f1f4df']},
        'DarkBlue11': {'BACKGROUND': '#6384b3', 'TEXT': '#e6f0b6', 'INPUT': '#b8e9c0', 'TEXT_INPUT': '#000000', 'SCROLL': '#b8e9c0', 'BUTTON': ('#e6f0b6', '#684949'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#684949', '#6384b3', '#b8e9c0', '#e6f0b6']},
        'DarkTeal8': {'BACKGROUND': '#71a0a5', 'TEXT': '#212121', 'INPUT': '#665c84', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#212121', 'BUTTON': ('#fab95b', '#665c84'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#212121', '#665c84', '#71a0a5', '#fab95b']},
        'DarkRed1': {'BACKGROUND': '#c10000', 'TEXT': '#eeeeee', 'INPUT': '#dedede', 'TEXT_INPUT': '#000000', 'SCROLL': '#dedede', 'BUTTON': ('#c10000', '#eeeeee'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#c10000', '#ff4949', '#dedede', '#eeeeee']},
        'LightBrown5': {'BACKGROUND': '#fff591', 'TEXT': '#e41749', 'INPUT': '#f5587b', 'TEXT_INPUT': '#000000', 'SCROLL': '#e41749', 'BUTTON': ('#fff591', '#e41749'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#e41749', '#f5587b', '#ff8a5c', '#fff591']},
        'LightGreen9': {'BACKGROUND': '#f1edb3', 'TEXT': '#3b503d', 'INPUT': '#4a746e', 'TEXT_INPUT': '#f1edb3', 'SCROLL': '#3b503d', 'BUTTON': ('#f1edb3', '#3b503d'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#3b503d', '#4a746e', '#c8cf94', '#f1edb3'], 'DESCRIPTION': ['Green', 'Turquoise', 'Yellow']},
        'DarkGreen2': {'BACKGROUND': '#3b503d', 'TEXT': '#f1edb3', 'INPUT': '#c8cf94', 'TEXT_INPUT': '#000000', 'SCROLL': '#c8cf94', 'BUTTON': ('#f1edb3', '#3b503d'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#3b503d', '#4a746e', '#c8cf94', '#f1edb3'], 'DESCRIPTION': ['Green', 'Turquoise', 'Yellow']},
        'LightGray1': {'BACKGROUND': '#f2f2f2', 'TEXT': '#222831', 'INPUT': '#393e46', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#222831', 'BUTTON': ('#f2f2f2', '#222831'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#222831', '#393e46', '#f96d00', '#f2f2f2'], 'DESCRIPTION': ['#000000', 'Grey', 'Orange', 'Grey', 'Autumn']},
        'DarkGrey4': {'BACKGROUND': '#52524e', 'TEXT': '#e9e9e5', 'INPUT': '#d4d6c8', 'TEXT_INPUT': '#000000', 'SCROLL': '#d4d6c8', 'BUTTON': ('#FFFFFF', '#9a9b94'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#52524e', '#9a9b94', '#d4d6c8', '#e9e9e5'], 'DESCRIPTION': ['Grey', 'Pastel', 'Winter']},
        'DarkBlue12': {'BACKGROUND': '#324e7b', 'TEXT': '#f8f8f8', 'INPUT': '#86a6df', 'TEXT_INPUT': '#000000', 'SCROLL': '#86a6df', 'BUTTON': ('#FFFFFF', '#5068a9'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#324e7b', '#5068a9', '#86a6df', '#f8f8f8'], 'DESCRIPTION': ['Blue', 'Grey', 'Cold', 'Winter']},
        'DarkPurple6': {'BACKGROUND': '#070739', 'TEXT': '#e1e099', 'INPUT': '#c327ab', 'TEXT_INPUT': '#e1e099', 'SCROLL': '#c327ab', 'BUTTON': ('#e1e099', '#521477'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#070739', '#521477', '#c327ab', '#e1e099'], 'DESCRIPTION': ['#000000', 'Purple', 'Yellow', 'Dark']},
         'DarkPurple7' : {'BACKGROUND': '#191930', 'TEXT': '#B1B7C5', 'INPUT': '#232B5C', 'TEXT_INPUT': '#D0E3E7', 'SCROLL': '#B1B7C5', 'BUTTON': ('#272D38', '#B1B7C5'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkBlue13': {'BACKGROUND': '#203562', 'TEXT': '#e3e8f8', 'INPUT': '#c0c5cd', 'TEXT_INPUT': '#000000', 'SCROLL': '#c0c5cd', 'BUTTON': ('#FFFFFF', '#3e588f'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#203562', '#3e588f', '#c0c5cd', '#e3e8f8'], 'DESCRIPTION': ['Blue', 'Grey', 'Wedding', 'Cold']},
        'DarkBrown5': {'BACKGROUND': '#3c1b1f', 'TEXT': '#f6e1b5', 'INPUT': '#e2bf81', 'TEXT_INPUT': '#000000', 'SCROLL': '#e2bf81', 'BUTTON': ('#3c1b1f', '#f6e1b5'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#3c1b1f', '#b21e4b', '#e2bf81', '#f6e1b5'], 'DESCRIPTION': ['Brown', 'Red', 'Yellow', 'Warm']},
        'DarkGreen3': {'BACKGROUND': '#062121', 'TEXT': '#eeeeee', 'INPUT': '#e4dcad', 'TEXT_INPUT': '#000000', 'SCROLL': '#e4dcad', 'BUTTON': ('#eeeeee', '#181810'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#062121', '#181810', '#e4dcad', '#eeeeee'], 'DESCRIPTION': ['#000000', '#000000', 'Brown', 'Grey']},
        'DarkBlack1': {'BACKGROUND': '#181810', 'TEXT': '#eeeeee', 'INPUT': '#e4dcad', 'TEXT_INPUT': '#000000', 'SCROLL': '#e4dcad', 'BUTTON': ('#FFFFFF', '#062121'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#062121', '#181810', '#e4dcad', '#eeeeee'], 'DESCRIPTION': ['#000000', '#000000', 'Brown', 'Grey']},
        'DarkGrey5': {'BACKGROUND': '#343434', 'TEXT': '#f3f3f3', 'INPUT': '#e9dcbe', 'TEXT_INPUT': '#000000', 'SCROLL': '#e9dcbe', 'BUTTON': ('#FFFFFF', '#8e8b82'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#343434', '#8e8b82', '#e9dcbe', '#f3f3f3'], 'DESCRIPTION': ['Grey', 'Brown']},
        'LightBrown12': {'BACKGROUND': '#8e8b82', 'TEXT': '#f3f3f3', 'INPUT': '#e9dcbe', 'TEXT_INPUT': '#000000', 'SCROLL': '#e9dcbe', 'BUTTON': ('#f3f3f3', '#8e8b82'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE,'PROGRESS_DEPTH': 0, 'COLOR_LIST': ['#343434', '#8e8b82', '#e9dcbe', '#f3f3f3'], 'DESCRIPTION': ['Grey', 'Brown']},
        'DarkTeal9': {'BACKGROUND': '#13445a', 'TEXT': '#fef4e8', 'INPUT': '#446878', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#446878', 'BUTTON': ('#fef4e8', '#446878'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#13445a', '#970747', '#446878', '#fef4e8'], 'DESCRIPTION': ['Red', 'Grey', 'Blue', 'Wedding', 'Retro']},
        'DarkBlue14': {'BACKGROUND': '#21273d', 'TEXT': '#f1f6f8', 'INPUT': '#b9d4f1', 'TEXT_INPUT': '#000000', 'SCROLL': '#b9d4f1', 'BUTTON': ('#FFFFFF', '#6a759b'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#21273d', '#6a759b', '#b9d4f1', '#f1f6f8'], 'DESCRIPTION': ['Blue', '#000000', 'Grey', 'Cold', 'Winter']},
        'LightBlue6': {'BACKGROUND': '#f1f6f8', 'TEXT': '#21273d', 'INPUT': '#6a759b', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#21273d', 'BUTTON': ('#f1f6f8', '#6a759b'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#21273d', '#6a759b', '#b9d4f1', '#f1f6f8'], 'DESCRIPTION': ['Blue', '#000000', 'Grey', 'Cold', 'Winter']},
        'DarkGreen4': {'BACKGROUND': '#044343', 'TEXT': '#e4e4e4', 'INPUT': '#045757', 'TEXT_INPUT': '#e4e4e4', 'SCROLL': '#045757', 'BUTTON': ('#e4e4e4', '#045757'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#222222', '#044343', '#045757', '#e4e4e4'], 'DESCRIPTION': ['#000000', 'Turquoise', 'Grey', 'Dark']},
        'DarkGreen5': {'BACKGROUND': '#1b4b36', 'TEXT': '#e0e7f1', 'INPUT': '#aebd77', 'TEXT_INPUT': '#000000', 'SCROLL': '#aebd77', 'BUTTON': ('#FFFFFF', '#538f6a'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#1b4b36', '#538f6a', '#aebd77', '#e0e7f1'], 'DESCRIPTION': ['Green', 'Grey']},
        'DarkTeal10': {'BACKGROUND': '#0d3446', 'TEXT': '#d8dfe2', 'INPUT': '#71adb5', 'TEXT_INPUT': '#000000', 'SCROLL': '#71adb5', 'BUTTON': ('#FFFFFF', '#176d81'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#0d3446', '#176d81', '#71adb5', '#d8dfe2'], 'DESCRIPTION': ['Grey', 'Turquoise', 'Winter', 'Cold']},
        'DarkGrey6': {'BACKGROUND': '#3e3e3e', 'TEXT': '#ededed', 'INPUT': '#68868c', 'TEXT_INPUT': '#ededed', 'SCROLL': '#68868c', 'BUTTON': ('#FFFFFF', '#405559'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#3e3e3e', '#405559', '#68868c', '#ededed'], 'DESCRIPTION': ['Grey', 'Turquoise', 'Winter']},
        'DarkTeal11': {'BACKGROUND': '#405559', 'TEXT': '#ededed', 'INPUT': '#68868c', 'TEXT_INPUT': '#ededed', 'SCROLL': '#68868c', 'BUTTON': ('#ededed', '#68868c'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#3e3e3e', '#405559', '#68868c', '#ededed'], 'DESCRIPTION': ['Grey', 'Turquoise', 'Winter']},
        'LightBlue7': {'BACKGROUND': '#9ed0e0', 'TEXT': '#19483f', 'INPUT': '#5c868e', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#19483f', 'BUTTON': ('#FFFFFF', '#19483f'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#19483f', '#5c868e', '#ff6a38', '#9ed0e0'], 'DESCRIPTION': ['Orange', 'Blue', 'Turquoise']},
        'LightGreen10': {'BACKGROUND': '#d8ebb5', 'TEXT': '#205d67', 'INPUT': '#639a67', 'TEXT_INPUT': '#FFFFFF', 'SCROLL': '#205d67', 'BUTTON': ('#d8ebb5', '#205d67'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE,'PROGRESS_DEPTH': 0, 'COLOR_LIST': ['#205d67', '#639a67', '#d9bf77', '#d8ebb5'], 'DESCRIPTION': ['Blue', 'Green', 'Brown', 'Vintage']},
        'DarkBlue15': {'BACKGROUND': '#151680', 'TEXT': '#f1fea4', 'INPUT': '#375fc0', 'TEXT_INPUT': '#f1fea4', 'SCROLL': '#375fc0', 'BUTTON': ('#f1fea4', '#1c44ac'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#151680', '#1c44ac', '#375fc0', '#f1fea4'], 'DESCRIPTION': ['Blue', 'Yellow', 'Cold']},
        'DarkBlue16': {'BACKGROUND': '#1c44ac', 'TEXT': '#f1fea4', 'INPUT': '#375fc0', 'TEXT_INPUT': '#f1fea4', 'SCROLL': '#375fc0', 'BUTTON': ('#f1fea4', '#151680'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#151680', '#1c44ac', '#375fc0', '#f1fea4'], 'DESCRIPTION': ['Blue', 'Yellow', 'Cold']},
        'DarkTeal12': {'BACKGROUND': '#004a7c', 'TEXT': '#fafafa', 'INPUT': '#e8f1f5', 'TEXT_INPUT': '#000000', 'SCROLL': '#e8f1f5', 'BUTTON': ('#fafafa', '#005691'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#004a7c', '#005691', '#e8f1f5', '#fafafa'], 'DESCRIPTION': ['Grey', 'Blue', 'Cold', 'Winter']},
        'LightBrown13': {'BACKGROUND': '#ebf5ee', 'TEXT': '#921224', 'INPUT': '#bdc6b8', 'TEXT_INPUT': '#921224', 'SCROLL': '#921224', 'BUTTON': ('#FFFFFF', '#921224'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE,'PROGRESS_DEPTH': 0, 'COLOR_LIST': ['#921224', '#bdc6b8', '#bce0da', '#ebf5ee'], 'DESCRIPTION': ['Red', 'Blue', 'Grey', 'Vintage', 'Wedding']},
        'DarkBlue17': {'BACKGROUND': '#21294c', 'TEXT': '#f9f2d7', 'INPUT': '#f2dea8', 'TEXT_INPUT': '#000000', 'SCROLL': '#f2dea8', 'BUTTON': ('#f9f2d7', '#141829'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#141829', '#21294c', '#f2dea8', '#f9f2d7'], 'DESCRIPTION': ['#000000', 'Blue', 'Yellow']},
        'DarkBrown6': {'BACKGROUND': '#785e4d', 'TEXT': '#f2eee3', 'INPUT': '#baaf92', 'TEXT_INPUT': '#000000', 'SCROLL': '#baaf92', 'BUTTON': ('#FFFFFF', '#785e4d'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#785e4d', '#ff8426', '#baaf92', '#f2eee3'], 'DESCRIPTION': ['Grey', 'Brown', 'Orange', 'Autumn']},
        'DarkGreen6': {'BACKGROUND': '#5c715e', 'TEXT': '#f2f9f1', 'INPUT': '#ddeedf', 'TEXT_INPUT': '#000000', 'SCROLL': '#ddeedf', 'BUTTON': ('#f2f9f1', '#5c715e'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#5c715e', '#b6cdbd', '#ddeedf', '#f2f9f1'], 'DESCRIPTION': ['Grey', 'Green', 'Vintage']},
        'DarkGreen7' : {'BACKGROUND': '#0C231E', 'TEXT': '#efbe1c', 'INPUT': '#153C33', 'TEXT_INPUT': '#efbe1c', 'SCROLL': '#153C33', 'BUTTON': ('#efbe1c', '#153C33'), 'PROGRESS': ('#efbe1c', '#153C33'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkGrey7': {'BACKGROUND': '#4b586e', 'TEXT': '#dddddd', 'INPUT': '#574e6d', 'TEXT_INPUT': '#dddddd', 'SCROLL': '#574e6d', 'BUTTON': ('#dddddd', '#43405d'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#43405d', '#4b586e', '#574e6d', '#dddddd'], 'DESCRIPTION': ['Grey', 'Winter', 'Cold']},
        'DarkRed2': {'BACKGROUND': '#ab1212', 'TEXT': '#f6e4b5', 'INPUT': '#cd3131', 'TEXT_INPUT': '#f6e4b5', 'SCROLL': '#cd3131', 'BUTTON': ('#f6e4b5', '#ab1212'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#ab1212', '#1fad9f', '#cd3131', '#f6e4b5'], 'DESCRIPTION': ['Turquoise', 'Red', 'Yellow']},
        'LightGrey6': {'BACKGROUND': '#e3e3e3', 'TEXT': '#233142', 'INPUT': '#455d7a', 'TEXT_INPUT': '#e3e3e3', 'SCROLL': '#233142', 'BUTTON': ('#e3e3e3', '#455d7a'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE, 'COLOR_LIST': ['#233142', '#455d7a', '#f95959', '#e3e3e3'], 'DESCRIPTION': ['#000000', 'Blue', 'Red', 'Grey']},
        'HotDogStand': {'BACKGROUND': 'red', 'TEXT': 'yellow', 'INPUT': 'yellow', 'TEXT_INPUT': '#000000', 'SCROLL': 'yellow', 'BUTTON': ('red', 'yellow'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE,},
        'DarkGrey8': {'BACKGROUND': '#19232D', 'TEXT': '#ffffff', 'INPUT': '#32414B', 'TEXT_INPUT': '#ffffff', 'SCROLL': '#505F69', 'BUTTON': ('#ffffff', '#32414B'), 'PROGRESS': ('#505F69', '#32414B')},
        'DarkGrey9' : {'BACKGROUND': '#36393F','TEXT': '#DCDDDE','INPUT': '#40444B','TEXT_INPUT': '#ffffff','SCROLL': '#202225','BUTTON': ('#202225', '#B9BBBE'),'PROGRESS': ('#202225', '#40444B')},
        'DarkGrey10' : {'BACKGROUND': '#1c1e23', 'TEXT': '#cccdcf', 'INPUT': '#272a31', 'TEXT_INPUT': '#8b9fde', 'SCROLL': '#313641', 'BUTTON': ('#f5f5f6', '#2e3d5a'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkGrey11' : {'BACKGROUND': '#1c1e23', 'TEXT': '#cccdcf', 'INPUT': '#313641', 'TEXT_INPUT': '#cccdcf', 'SCROLL': '#313641', 'BUTTON': ('#f5f5f6', '#313641'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkGrey12' : {'BACKGROUND': '#1c1e23', 'TEXT': '#8b9fde', 'INPUT': '#313641', 'TEXT_INPUT': '#8b9fde', 'SCROLL': '#313641', 'BUTTON': ('#cccdcf', '#2e3d5a'), 'PROGRESS': DEFAULT_PROGRESS_BAR_COMPUTE},
        'DarkGrey13' : {'BACKGROUND': '#1c1e23', 'TEXT': '#cccdcf', 'INPUT': '#272a31', 'TEXT_INPUT': '#cccdcf', 'SCROLL': '#313641', 'BUTTON': ('#8b9fde', '#313641'), 'PROGRESS': ('#cccdcf','#272a31')},
        'DarkGrey14' : {'BACKGROUND': '#24292e', 'TEXT': '#fafbfc', 'INPUT': '#1d2125', 'TEXT_INPUT': '#fafbfc', 'SCROLL': '#1d2125', 'BUTTON': ('#fafbfc', '#155398'), 'PROGRESS': ('#155398','#1d2125')},
        'DarkBrown7' : {'BACKGROUND': '#2c2417', 'TEXT': '#baa379', 'INPUT': '#baa379', 'TEXT_INPUT': '#000000', 'SCROLL': '#392e1c', 'BUTTON': ('#000000', '#baa379'), 'PROGRESS': ('#baa379','#453923'), 'SLIDER_DEPTH': 1},
        'Python': {'BACKGROUND': '#3d7aab', 'TEXT': '#ffde56', 'INPUT': '#295273', 'TEXT_INPUT': '#ffde56', 'SCROLL': '#295273', 'BUTTON': ('#ffde56', '#295273'), 'PROGRESS': ('#ffde56','#295273'), 'SLIDER_DEPTH': 1}}

    CURRENT_THEME = 'DarkBlue3'

    DEFAULT_FONT = {'family': 'Segoe Marker', 'size': 12, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}

    DEFAULT_MINUTE_FONT = {'family': 'Segoe Marker', 'size': 10, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    BIG_FONT = {'family': 'Segoe Marker', 'size': 31, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}

    DEFAULT_MENU_FONT = {'family': 'Adobe Garamond Pro Bold', 'size': 10, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}

    DEFAULT_BUTTON_FONT = {'family': 'Buxton Sketch', 'size': 14, 'weight': 'bold', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    DEFAULT_BUTTONS_FONT = {'family': 'Buxton Sketch', 'size': 10, 'weight': 'bold', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    DEFAULT_SMALL_BUTTON_FONT = {'family': 'Buxton Sketch', 'size': 12, 'weight': 'bold', 'slant': 'roman', 'underline': 0, 'overstrike': 0}

    DEFAULT_TITLE_FONT = {'family': 'Lucida Calligraphy', 'size': 13, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}

    DEFAULT_STATUS_FONT = DEFAULT_TITLE_FONT


    DEFAULT_LABEL_FONT = {'family': 'Viner Hand ITC', 'size': 14, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}

    DEFAULT_LABELFRAME_FONT = {'family': 'Script MT Bold', 'size': 18, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}

    HEADING_FONT = {'family': 'Clarendon BT', 'size': 10, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}

    NORMAL_FONT = {'family': 'Minion Pro', 'size': 12, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}

    PRMP_FONT = {'family': 'Times New Roman', 'size': 11, 'weight': 'bold', 'slant': 'roman', 'underline': 0, 'overstrike': 0}

    PRMP_FONTS = []

    themedWidgets = ['Combobox', 'Progressbar', 'Scrollbar', 'Treeview', 'Notebook', 'Panedwindow', 'Progressbar', 'Scale', 'Scrollbar', 'Separator', 'Sizegrip', 'Spinbox', 'Treeview', 'Toolbutton']

    @classmethod
    def setTheme(cls, theme):
        # normalize available l&f values
        lf_values = [item.lower() for item in cls.themesList()]
        # option 1
        opt1 = theme.replace(' ', '').lower()
        # option 2 (reverse lookup)
        optx = theme.lower().split(' ')
        optx.reverse()
        opt2 = ''.join(optx)
        # search for valid l&f name
        if opt1 in lf_values: ix = lf_values.index(opt1)
        elif opt2 in lf_values: ix = lf_values.index(opt2)
        else: ix = random.randint(0, len(lf_values) - 1); print('** Warning - {} Theme is not a valid theme. Change your theme call. **'.format(theme))

        selection = cls.themesList()[ix]

        cls.CURRENT_THEME = selection


        try:
            colors = cls.THEMES_DICTS[selection]

            if colors['PROGRESS'] != cls.COLOR_SYSTEM_DEFAULT:
                if colors['PROGRESS'] == cls.DEFAULT_PROGRESS_BAR_COMPUTE:
                    if colors['BUTTON'][1] != colors['INPUT'] and colors['BUTTON'][1] != colors['BACKGROUND']:
                        colors['PROGRESS'] = colors['BUTTON'][1], colors['INPUT']
                    else: colors['PROGRESS'] = (colors['TEXT_INPUT'], colors['INPUT'])
            else:
                colors['PROGRESS'] = cls.DEFAULT_PROGRESS_BAR_COLOR_OFFICIAL

            cls.setOptions(background_color=colors['BACKGROUND'],
                    text_color=colors['TEXT'],
                    input_elements_background_color=colors['INPUT'],
                    button_color=colors['BUTTON'],
                    progress_meter_color=colors['PROGRESS'],
                    scrollbar_color=colors['SCROLL'],
                    input_text_color=colors['TEXT_INPUT'])
            return cls.CURRENT_THEME
        except Exception as er:
            print(f'Error: {er} ')
            print(f'** Warning - Theme value not valid. Change your theme ({theme}) call. **')

    @classmethod
    def setOptions(cls, button_color=None, progress_meter_color=None, background_color=None, input_elements_background_color=None, input_text_color=None, scrollbar_color=None, text_color=None):

        if button_color != None: PRMP_Theme.DEFAULT_BUTTON_COLOR = button_color

        if progress_meter_color != None: PRMP_Theme.DEFAULT_PROGRESS_BAR_COLOR = progress_meter_color

        if background_color != None: PRMP_Theme.DEFAULT_BACKGROUND_COLOR = background_color

        if input_elements_background_color != None: PRMP_Theme.DEFAULT_INPUT_ELEMENTS_COLOR = input_elements_background_color

        if text_color != None: PRMP_Theme.DEFAULT_FOREGROUND_COLOR = text_color

        if scrollbar_color != None: PRMP_Theme.DEFAULT_SCROLLBAR_COLOR = scrollbar_color

        if input_text_color is not None: PRMP_Theme.DEFAULT_INPUT_TEXT_COLOR = input_text_color

        return True

    @classmethod
    def themesList(cls): return sorted(list(cls.THEMES_DICTS.keys()))

    @classmethod
    def setThemeIndex(cls, num):
        themes = cls.themesList()
        total = len(themes)
        if 0 < num < total: cls.setTheme(themes[num])
        else: cls.setTheme(themes[0])

    @property
    def fontsNames(self): return self.tk.splitlist(self.tk.call("font", "names"))

    def parseFont(self, font):
        if isinstance(font, str):
            if font in self.fontsNames: return font
            return Font(name=font)
        elif isinstance(font, dict): return Font(**font)

    def deriveFont(self, kwargs={}, default='DEFAULT_FONT'):
        if not kwargs: font = self.kwargs.get('font')
        else: font = kwargs.pop('font')

        default = self.parseFont(default)
        try:
            font = self.parseFont(font)
            return font
        except: return default

    def createDefaultFonts(self):
        fonts = ['DEFAULT_FONT', 'DEFAULT_MINUTE_FONT', 'BIG_FONT', 'DEFAULT_MENU_FONT', 'DEFAULT_BUTTON_FONT', 'DEFAULT_BUTTONS_FONT', 'DEFAULT_SMALL_BUTTON_FONT', 'DEFAULT_TITLE_FONT', 'DEFAULT_STATUS_FONT', 'DEFAULT_LABEL_FONT', 'DEFAULT_LABELFRAME_FONT', 'HEADING_FONT', 'NORMAL_FONT', 'PRMP_FONT']
        for df in fonts:
            font = PRMP_Theme.__dict__[df]
            try: fo = Font(self, name=df, exists=0, **font)
            except: fo = Font(self, name=df, exists=1, **font)
            PRMP_Theme.PRMP_FONTS.append(fo)

    def _prevTheme(self):
        cur = PRMP_Theme.CURRENT_THEME
        ths = PRMP_Theme.themesList()
        ind = ths.index(cur)
        next_ = ind + 1
        if next_ == len(ths): next_ = 0
        theme = ths[next_]
        PRMP_Theme.setTheme(theme)
        return [theme, next_]

    def _nextTheme(self):
        cur = PRMP_Theme.CURRENT_THEME
        ths = PRMP_Theme.themesList()
        ind = ths.index(cur)
        prev = ind - 1
        if ind == -1: prev = len(ths) - 1
        theme = ths[prev]
        PRMP_Theme.setTheme(theme)
        return [theme, prev]

    def _paint(self):
        if not self._ttk_:
            kwargs = {k: v for k, v in self.kwargs.items() if k not in ['font', 'required', 'placeholder', '_type', 'default', 'tipKwargs', 'very']}

            foreground = kwargs.pop('foreground', PRMP_Theme.DEFAULT_FOREGROUND_COLOR)

            background = kwargs.pop('background', PRMP_Theme.DEFAULT_BACKGROUND_COLOR)
            activebackground = kwargs.pop('activebackground', foreground)
            activeforeground = kwargs.pop('activeforeground', background)
            highlightbackground = kwargs.pop('highlightbackground', background)
            highlightcolor = kwargs.pop('highlightcolor', foreground)
            disabledforeground = kwargs.pop('disabledforeground', foreground)
            borderwidth = kwargs.pop('borderwidth', 2)
            highlightthickness = kwargs.pop('highlightthickness', 1)

            relief = kwargs.pop('relief',  PRMP_Theme.DEFAULT_RELIEF)
            wt = widgetType = self.PRMP_WIDGET

            _dict = {}

            asLabel = kwargs.get('asLabel')
            if asLabel != None:
                asLabel = kwargs.pop('asLabel')
                wt = 'Label' if asLabel else wt

            asEntry = kwargs.get('asEntry')
            if asEntry != None:
                asEntry = kwargs.pop('asEntry')
                wt = 'Entry' if asEntry else wt
                # _dict.update(dict(activebackground=activebackground, activeforeground=activeforeground, highlightbackground=background))
                try: self.config(**dict(activebackground=activebackground, activeforeground=activeforeground, highlightbackground=background))
                except: pass

            oneColor = True
            col = PRMP_Theme.DEFAULT_BUTTON_COLOR
            if isinstance(col, tuple): oneColor = False
            else: background, foreground = 'white', 'black'

            if wt in ['Button', 'Label', 'Radiobutton', 'Checkbutton', 'Menubutton']:

                if wt == 'Button':
                    font = self.deriveFont(default='DEFAULT_BUTTON_FONT')
                    if oneColor == False:
                        if foreground == PRMP_Theme.DEFAULT_FOREGROUND_COLOR: foreground = PRMP_Theme.DEFAULT_BUTTON_COLOR[0]
                        if background == PRMP_Theme.DEFAULT_BACKGROUND_COLOR: background = PRMP_Theme.DEFAULT_BUTTON_COLOR[1]

                else: font = self.deriveFont(default='DEFAULT_LABEL_FONT')
                _dict.update(dict(activebackground=activebackground,
                            activeforeground=activeforeground,
                            background=background,
                            borderwidth=borderwidth,
                            disabledforeground=disabledforeground,
                            foreground=foreground,
                            highlightbackground=highlightbackground,
                            highlightcolor=highlightcolor,
                            font=font,
                            highlightthickness=highlightthickness,
                            relief=relief, **kwargs))

            elif wt == 'LabelFrame':
                font = self.deriveFont(default='DEFAULT_LABELFRAME_FONT')
                _dict.update(dict(background=background, foreground=foreground, relief=relief, **kwargs, borderwidth=borderwidth, font=font))

            elif wt == 'Scale': _dict.update(dict(troughcolor=PRMP_Theme.DEFAULT_SCROLLBAR_COLOR))

            elif wt in ['Entry', 'Text', 'Listbox', 'Spinbox']:
                if foreground == PRMP_Theme.DEFAULT_FOREGROUND_COLOR: foreground = PRMP_Theme.DEFAULT_INPUT_TEXT_COLOR
                if background == PRMP_Theme.DEFAULT_BACKGROUND_COLOR: background = PRMP_Theme.DEFAULT_INPUT_ELEMENTS_COLOR
                font = self.deriveFont(default='DEFAULT_FONT')
                _dict.update(dict(background=background,
                            borderwidth=borderwidth,
                            foreground=foreground,
                            highlightbackground=highlightbackground,
                            highlightcolor=highlightcolor,
                            highlightthickness=highlightthickness,
                            relief='sunken',
                            font=font,
                            **kwargs))

            elif wt in ['Scrollbar']:
                if foreground == PRMP_Theme.DEFAULT_FOREGROUND_COLOR: foreground = PRMP_Theme.DEFAULT_INPUT_TEXT_COLOR
                if background == PRMP_Theme.DEFAULT_BACKGROUND_COLOR: background = PRMP_Theme.DEFAULT_INPUT_ELEMENTS_COLOR

            else:
                try: self.configure(background=background)
                except: pass
                return self
            # print(self)
            self.configure(**_dict)

        if self.var and self.var.get() == self.val: self.checked(1)

        return self

    def _paintChildren(self):
        children = self._children
        for child in children:
            if hasattr(child, 'paint'):
                if str(child) == '.!prmp_style_frame.!datetimeview':
                    child.paint()

                child.paint()

    def _paintAll(self, event=None):
        self._paint()
        self._paintChildren()

    def paint(self, event=None):
        # print(e)
        self._paintAll()

    @classmethod
    def currentThemeIndex(cls): return cls.themesList().index(cls.CURRENT_THEME)
    @classmethod
    def currentThemeDict(cls): return cls.THEMES_DICTS[cls.CURRENT_THEME]
PRMP_Theme = PRMP_Theme

class PRMP_Widget(PRMP_Theme):

    def after(self, time, func):
        # print(func)
        if not self.winfo_exists(): return
        super().after(time, func)

    @property
    def topest(self): return PRMP_Window.TOPEST

    @property
    def _children(self): return self.winfo_children()
    @property
    def topest2(self):
        master = self.master
        while True:
            master = master.master
            if master == None: return master
            master = master
    @property
    def toplevel(self):
        master = self.master
        while True:
            master = master.master
            if isinstance(master, (PRMP_Tk, PRMP_Toplevel)): return master
            master = master

    TkClass = None

    def __init__(self, master=None, _ttk_=False, tipKwargs={}, status='', relief='groove', nonText=False, asEntry=False, highlightable=True, place={}, grid={}, pack={}, font='DEFAULT_FONT', config={}, **kwargs):
        '''
        :param tipKwargs: dict of [Label options, follow, delay]
        '''

        config = config.copy()
        self.kwargs = kwargs.copy()
        kwargs.clear()
        self.kwargs['font'] = font or 'PRMP_FONT'
        self.kwargs.update(config)

        self.master = master

        if asEntry:
            relief = 'sunken'
            self.kwargs['asEntry'] = asEntry
        self.kwargs['relief'] = relief

        self.prmp_master = self.kwargs.pop('prmp_master', self.master)

        self._status = status
        self.font = None
        self.highlightable = highlightable
        self.nonText = nonText

        self.toggleGroup = []

        self.val = self.kwargs.pop('val', '1')
        self.value = self.kwargs.pop('value', self.val)

        var = self.kwargs.pop('var', None) or self.kwargs.get('variable', None)

        if isinstance(var, tk.StringVar): pass
        elif var:
            var = tk.StringVar()
            var.set('0')
        self.var = self.variable = var
        if var: config['variable'] = var

        self._ttk_ = _ttk_
        self.TkClass.__init__(self, self.master, **config)

        try: self.useFont(font)
        except: pass

        if bool(tipKwargs) and not isinstance(tipKwargs, dict) and self.kwargs.get('text'): tipKwargs = dict(text=self.kwargs.get('text'))

        self.tooltip = None

        self.addTip(**tipKwargs)

        self.bind('<Enter>', self.entered, '+')
        self.bind('<Leave>', self.left, '+')

        if not isinstance(self, PRMP_Window): self.positionWidget(place=place, pack=pack, grid=grid)

    def entered(self, event=None):
        if not self.nonText: self.statusShow()
        if self.highlightable:
            try: self.configure(relief='solid')
            except: pass

    def left(self, event=None):
        if self.highlightable:
            re = self.kwargs.get('relief', 'flat')
            try: self.configure(relief=re)
            except: pass

    def statusShow(self):
        root = self.winfo_toplevel()
        if root and getattr(root, 'statusBar', None): root.statusBar.set(self.status)

    def getWid_H_W(self, wid):
        wid.update()
        return (wid.winfo_width(), wid.winfo_height())

    def get(self): return self['text']

    @property
    def width(self):
        self.update()
        try: return int(self.winfo_width())
        except: return -1

    @property
    def height(self):
        self.update()
        try: return int(self.winfo_height())
        except: return -1

    @property
    def winfos(self):
        geo_infos = [self.winfo_geometry, self.winfo_height, self.winfo_pointerx, self.winfo_pointerxy, self.winfo_pointery, self.winfo_rootx, self.winfo_rooty, self.winfo_screendepth, self.winfo_screenheight, self.winfo_width, self.winfo_x, self.winfo_y]

        unnecessaries = [self.winfo_reqheight, self.winfo_reqwidth, self.winfo_depth, self.winfo_screenmmheight, self.winfo_screenmmwidth, self.winfo_vrootheight, self.winfo_vrootwidth, self.winfo_vrootx, self.winfo_vrooty, ]

        return [(a.__name__, a()) for a in geo_infos]

    @property
    def tupled_winfo_geometry(self):
        geo = self.winfo_geometry()
        first = geo.split('x')
        second = first[1].split('+')
        ret = [int(n) for n in (first[0], *second)]

        return ret

    def getText(self):
        try: return self['text']
        except Exception as er: self.printError('get', er)

    @property
    def status(self):
        if self._status: return self._status
        try: return self.kwargs.get('text', '')
        except: return self['text']

    def set(self, values):
        try: self.config(text=values)
        except Exception as er: self.printError('set', er)

    def light(self):
        if self._ttk_: return
        self.configure(background=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, foreground=PRMP_Theme.DEFAULT_BACKGROUND_COLOR)

    def unlight(self):
        if self._ttk_: return
        self.configure(background=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, foreground=PRMP_Theme.DEFAULT_FOREGROUND_COLOR)


    def addWidget(self, widget, config={}, place={}, grid={}, pack={}, container=None):
        container = container or self.container

        widget = widget(container, **config, place=place, pack=pack, grid=grid)
        widget.paint()

        return widget

    def positionWidget(self, widget=None, **positions):
        if widget == None: widget = self

        func = kw = None
        if 'place' in positions:
            kw = positions['place']
            if kw and isinstance(kw, dict):
                widget.place(**kw)
                return
        if 'grid' in positions:
            kw = positions['grid']
            go = 0
            if kw and isinstance(kw, dict):
                widget.grid(**kw)
                go = 1
            elif kw:
                go = 1
                widget.grid()
            if go: return
        if 'pack' in positions:
            kw = positions['pack']
            if kw and isinstance(kw, dict): widget.pack(**kw)
            elif kw: widget.pack()

    def switchOne(self, event=None):
        val = self.var.get() if self.var else None
        if self.onFg == False:
            self.light()
            if self.var: self.var.set('0')
            self.onFg = True
        elif self.PRMP_WIDGET == 'Radiobutton' and val == self.value: self.light()
        elif val != self.value: self.unlight()
        else:
            self.unlight()
            self.onFg = False

    def checked(self, event=None):
        if self.variable:
            if self.variable.get() == self.value: self.light()
            else: self.unlight()

    def switchGroup(self, event=None):
        if e: self.var.set(self.val)
        for w in self.toggleGroup:
            if w == self: self.light()
            else: w.unlight()

    def toggleSwitch(self):
        self.onFg = False
        if self.toggleGroup: self.bind('<1>', self.switchGroup, '+')
        else: self.bind('<1>', self.switchOne, '+')

    def addToggleGroup(self, group=[]):
        if group:
            self.toggleGroup = group
            self.toggleSwitch()

    def setRadioGroups(self, group):
        for one in group: one.addToggleGroup(group)

    def useFont(self, font=None):
        if font: self.font = self.parseFont(font)
        if self.font: self['font'] = self.font

        return self

    def bindOverrelief(self, wid, relief='solid', **kwargs):
        if wid._ttk_: return

        def setRelief(event=None): wid.configure(relief=relief, **kwargs)
        def resetRelief(event=None): wid.paint()

        wid.bind('<Enter>', setRelief, '+')
        wid.bind('<Leave>', resetRelief, '+')

    def bindEntryHighlight(self, **kwargs): self.bindOverrelief(self, **kwargs)

    def readonly(self, wh=''):
        try: self.state('readonly')
        except: self.disabled()

    def disabled(self): self.state('disabled')

    def active(self): self.state('active')

    def normal(self): self.state('normal')

    def state(self, args=''):
        if isinstance(args, (list, tuple)): return self.TkClass.state(self, args)
        elif isinstance(args, str):
            try: return self.TkClass.state(self, args)
            except:
                try: self['state'] = args
                except:
                    try: self.configure(state=args)
                    except: pass
        if self.children:
            for child in self.winfo_children(): child.state(args)

    def config(self, tipKwargs={}, **kwargs):
        if tipKwargs: self.set_tooltip_text(tipKwargs)
        self.kwargs.update(kwargs)
        self.TkClass.configure(self, **kwargs)

    @property
    def PRMP_WIDGET(self): return self.className.replace('PRMP_', '')

    def addTip(self, **kwargs):
        self.tipKwargs = kwargs
        if not kwargs: return

        if not PRMP_Window.TIPSMANAGER: self.tooltip = PRMP_ToolTipsManager(self, **kwargs)
        else: PRMP_Window.TIPSMANAGER.add_tooltip(self, **kwargs)

    def set_tooltip_text(self, tipKwargs):
        tip = self.tooltip or PRMP_Window.TIPSMANAGER
        if tip: tip.set_tooltip_text(self, **tipKwargs)


    def on_mousewheel(self, event):
        if platform.system() == 'Windows': self.yview_scroll(-1*int(event.delta/120),'units')
        elif platform.system() == 'Darwin': self.yview_scroll(-1*int(event.delta),'units')
        else:
            if event.num == 4:
                self.yview_scroll(-1, 'units')
            elif event.num == 5:
                self.yview_scroll(1, 'units')

    def on_shiftmouse(self, event):
        if platform.system() == 'Windows': self.xview_scroll(-1*int(event.delta/120), 'units')
        elif platform.system() == 'Darwin': self.xview_scroll(-1*int(event.delta), 'units')
        else:
            if event.num == 4: self.xview_scroll(-1, 'units')
            elif event.num == 5: self.xview_scroll(1, 'units')

    def bound_to_mousewheel(self, event):
        child = self._children[0]
        if platform.system() == 'Windows' or platform.system() == 'Darwin':
            child.bind_all('<MouseWheel>', lambda e: on_mousewheel(e, child))
            child.bind_all('<Shift-MouseWheel>', lambda e: on_shiftmouse(e, child))
        else:
            child.bind_all('<Button-4>', lambda e: on_mousewheel(e, child))
            child.bind_all('<Button-5>', lambda e: on_mousewheel(e, child))
            child.bind_all('<Shift-Button-4>', lambda e: on_shiftmouse(e, child))
            child.bind_all('<Shift-Button-5>', lambda e: on_shiftmouse(e, child))

    def unbound_to_mousewheel(self, event):
        if platform.system() == 'Windows' or platform.system() == 'Darwin':
            self.unbind_all('<MouseWheel>')
            self.unbind_all('<Shift-MouseWheel>')
        else:
            self.unbind_all('<Button-4>')
            self.unbind_all('<Button-5>')
            self.unbind_all('<Shift-Button-4>')
            self.unbind_all('<Shift-Button-5>')

    def _move(self, event):
        try: self.x, self.y = event.x, event.y
        except: pass

    def _moveroot(self):
        root = self.winfo_toplevel()
        self.bind("<ButtonPress-1>", functools.partial(PRMP_Widget._move, root), '+')
        self.bind("<ButtonRelease-1>",functools. partial(PRMP_Widget._move, root), '+')
        self.bind("<B1-Motion>", functools.partial(PRMP_Widget._onMotion, root), '+')

        self.bind("<ButtonPress-3>", functools.partial(PRMP_Widget._move, root), '+')
        self.bind("<ButtonRelease-3>",functools. partial(PRMP_Widget._move, root), '+')
        self.bind("<B3-Motion>", functools.partial(PRMP_Widget._onMotion, root), '+')

    def _grab_anywhere_on(self):
        self.bind("<ButtonPress-3>", self._move, '+')
        self.bind("<ButtonRelease-3>", self._move, '+')
        self.bind("<B3-Motion>", self._onMotion, '+')

    def _grab_anywhere_off(self):
        self.unbind("<ButtonPress-3>")
        self.unbind("<ButtonRelease-3>")
        self.unbind("<B3-Motion>")

    def _onMotion(self, event):
        try:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.winfo_x() + deltax
            y = self.winfo_y() + deltay
            self.geometry("+%s+%s" % (x, y))
        except Exception as e:
            print('on motion error', e)

    def bindToWidget(self, *args):
        for arg in args: self.bind(arg[0], arg[1], '+')

    def __getitem__(self, item):
        try:
            if self.TkClass: return self.TkClass.__getitem__(self, item)
        except: pass
PWd = PRMP_Widget

class PRMP_(PRMP_Widget):

    def __init__(self, **kwargs):
        super().__init__(_ttk_=False, **kwargs)
P_ = PRMP_

class PRMP_Style_(PRMP_Widget):

    def __init__(self, highlightable=False, **kwargs):
        super().__init__(_ttk_=True, highlightable=highlightable, **kwargs)

    @property
    def style(self): return PRMP_Window.STYLE
PS_ = PRMP_Style_

class PRMP_Input:

    def __init__(self, placeholder='', _type='text', values=[], required=False, default=None, state='normal', very=False, **kwargs):
        _type = _type.lower()

        self._read = False
        if self.kwargs.get('state', None) == 'readonly': self._read = True

        self.values = values
        self.very = very

        self.bind("<FocusIn>", self._clear_placeholder, '+')
        self.bind("<FocusOut>", self._add_placeholder, '+')
        self.returnType = str

        types = ['email', 'number', 'money']

        if _type == 'email':
            self.bind('<KeyRelease>', self.checkingEmail, '+')
            self._verify = self.checkingEmail
        elif _type == 'number':
            self.set = self.setNumber
            self.get = self.getNumber
            self.bind('<KeyRelease>', self.checkingNumber, '+')
            self._verify = self.checkingNumber
            self.returnType = float
        elif _type == 'money':
            placeholder = f'{self._moneySign} 0'
            if default != None: placeholder = f'{self._moneySign}{default}'
            self.set = self.setMoney
            self.get = self.getMoney
            self.bind('<KeyRelease>', self.checkingMoney, '+')
            self._verify = self.checkingMoney
        elif _type == 'dir':
            self.bind('<KeyRelease>', self.checkingDir, '+')
            self._verify = self.checkingDir
        elif _type == 'file':
            self.bind('<KeyRelease>', self.checkingFile, '+')
            self._verify = self.checkingFile
        elif _type == 'path':
            self.bind('<KeyRelease>', self.checkingPath, '+')
            self._verify = self.checkingPath
        else:
            self.bind('<KeyRelease>', self.normVery, '+')
            self._verify = self.normVery

        self.required = required
        if self.values: self.required = True

        self.changePlaceholder(placeholder)

    def changePlaceholder(self, placeholder):
        self.placeholder = placeholder
        self.set(self.placeholder)

    def verify(self): return self._verify()

    def normVery(self, event=None):
        get = self._get()
        if self.values:
            if get in self.values: return self.green()
            else: return self.red()
        elif get not in [self.placeholder, '']: return self.green()
        else:  return self.red()

    def setNumber(self, number=None):
        self.clear()
        if number == self.placeholder: pass
        elif not self.checkNumber(number): return
        self._set(number)

    def getNumber(self):
        number = self._get()
        if self.checkNumber(number): return float(number)

    def setMoney(self, money=None):
        self.clear()
        if money == self.placeholder or not money: money = self.placeholder
        elif not self.checkMoney(money): money = self.numberToMoney(money)
        self._set(money)

    def getMoney(self):
        money = self._get()
        if self.checkMoney(money): return float(self.moneyToNumber(money))
        return money

    def entered(self, event=None):
        super().entered()
        self._clear_placeholder()

    def left(self, event=None):
        super().left()
        self.focus()
        self._add_placeholder()

    def green(self):
        foreground = self.kwargs.get('foreground', 'green')
        if self.very: self.configure(foreground=foreground)
        return True

    def red(self):
        if self.very: self.configure(foreground='red')
        return False

    def checkingPath(self, event=None):
        path = self._get()
        if path:
            if self.checkPath(path): return self.green()
            else: return self.red()

    def checkingDir(self, event=None):
        dir_ = self._get()
        if dir_:
            if self.checkDir(dir_): return self.green()
            else: return self.red()

    def checkingFile(self, event=None):
        file = self._get()
        if file:
            if self.checkFile(file): return self.green()
            else: return self.red()

    def checkingEmail(self, event=None):
        email = self._get()
        if email:
            if self.checkEmail(email): return self.green()
            else: return self.red()

    def checkingNumber(self, event=None):
        number = self._get()
        if number:
            if self.checkNumber(number): return self.green()
            else: return self.red()

    def checkingMoney(self, event=None):
        money = self._get()
        if money:
            if self.checkMoney(money): return self.green()
            elif money == self._moneySign:  self.configure(foreground='orange')
            elif self.moneyToNumber(money).isalnum(): return self.red()
            else:
                self.clear()
                self.set(self._moneySign)
                return self.red()
        else:
            self.clear()
            self.set(self._moneySign)

    def normal(self, force=0):
        if self._read and not force: return
        super().normal()
        self.verify()

    def disabled(self):
        self._add_placeholder()
        super().disabled()
        self.verify()

    def paint(self):
        super().paint()
        self.verify()

    def _set(self, values):
        if self._read: self.normal(1)
        self.clear()
        self.insert(0, str(values))
        if self._read: self.readonly()

    def set(self, values):
        self._set(values)
        self.verify()

    def _clear_placeholder(self, event=None):
        if self._get() == self.placeholder: self.clear()

    def _add_placeholder(self, event=None):
        if self._get() == '': self.set(self.placeholder)

    def empty(self): self.set(self.placeholder)

    def clear(self): self.delete('0', 'end')

    def _get(self): return self.TkClass.get(self)

    def get(self):
        get = self._get()
        if get == self.placeholder: get = ''
        return get

    def state(self, args=''):
        go = super().state(args)
        if go and 'readonly' in args: self._read = True
        return go
PI = PRMP_Input

class PRMP_InputButtons:

    def set(self, val):
        if self.var:
            self.var.set(val)
            # self.val = self.value = val
        else: self.configure(text=val)

    def get(self):
        val = self.var.get() if self.var else None
        if val == self.val: return True
        elif not self.var: return self['text']
        else: return False

PIB = PRMP_InputButtons

# based on tk only

class PRMP_Canvas(PRMP_, tk.Canvas):
    TkClass = tk.Canvas

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master,config=config, **kwargs)
Canvas = PCv = PRMP_Canvas

class PRMP_Message(PRMP_, PRMP_Input, tk.Message):
    TkClass = tk.Message

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master,config=config, **kwargs)
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

# based on ttk only

class PRMP_Combobox(PRMP_Input, PRMP_Style_, ttk.Combobox):
    TkClass = ttk.Combobox

    def __init__(self, master=None, type_='', config={}, values=[], **kwargs):

        if type_.lower() == 'gender': values = ['Male', 'Female']

        PRMP_Style_.__init__(self, master=master, config=config, **kwargs)
        PRMP_Input.__init__(self, values=values, **kwargs)
        self.objects = {}
        self.changeValues(values)

    def setObjs(self, objs, attr):
        values = []
        co = 0
        for obj in objs:
            co += 1
            val = obj[attr]
            val = f'{co}. {val}'
            self.objects[val] = obj
            values.append(val)
        self.changeValues(values)

    def getObj(self):
        get = self.get()
        if get in self.objects: return self.objects[get]

    @property
    def PRMP_WIDGET(self): return 'Combobox'

    def changeValues(self, values):
        self.values = values
        self['values'] = values

    def getValues(self): return self['values']
Combobox = PCb = PRMP_Combobox

class PRMP_LabeledScale(PRMP_Style_, ttk.LabeledScale):
    TkClass = ttk.LabeledScale

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)
LabeledScale = PLS = PRMP_LabeledScale

class PRMP_Notebook(PRMP_Style_, ttk.Notebook):
    TkClass = ttk.Notebook

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)

        self.bind('<Button-1>', self._button_press)
        self.bind('<ButtonRelease-1>', self._button_release)
        self.bind('<Motion>', self._mouse_over)

    def _button_press(self, event):
        widget = event.widget
        element = widget.identify(event.x, event.y)
        if "close" in element:
            index = widget.index("@%d,%d" % (event.x, event.y))
            widget.state(['pressed'])
            widget._active = index

    def _button_release(self, event):
        widget = event.widget
        if not widget.instate(['pressed']):
                return
        element = widget.identify(event.x, event.y)
        try:
            index = widget.index("@%d,%d" % (event.x, event.y))
        except tk.TclError:
            pass
        if "close" in element and widget._active == index:
            widget.forget(index)
            widget.event_generate("<<NotebookTabClosed>>")

        widget.state(['!pressed'])
        widget._active = None

    def _mouse_over(self, event):
        widget = event.widget
        element = widget.identify(event.x, event.y)
        if "close" in element:
            widget.state(['alternate'])
        else:
            widget.state(['!alternate'])
Notebook = PN = PRMP_Notebook

class PRMP_Panedwindow(PRMP_Style_, ttk.Panedwindow):
    TkClass = ttk.Panedwindow

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)
Panedwindow = PPw = PRMP_Panedwindow

class PRMP_Progressbar(PRMP_Style_, ttk.Progressbar):
    TkClass = ttk.Progressbar

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)
Progressbar = PPb = PRMP_Progressbar

class PRMP_Separator(PRMP_Style_, ttk.Separator):
    TkClass = ttk.Separator

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)
Separator = PS = PRMP_Separator

class PRMP_Sizegrip(PRMP_Style_, ttk.Sizegrip):
    TkClass = ttk.Sizegrip

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)
Sizegrip = PSg = PRMP_Sizegrip

class PRMP_Style(ttk.Style, PRMP_Mixins):
    LOADED = False
    ttkthemes = ("black", "blue", 'prmp')
    ttkstyles = ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

    def __init__(self, master=None):
        super().__init__(master)
        if not PRMP_Style.LOADED: self.createPrmp()
        self.theme_use('prmp')

    def tupledFont(self, fontDict):
        options = []
        for k, v in fontDict.items():
            options.append("-"+k)
            options.append(str(v))
        return tuple(options)

    def getPixs(self, name):
        name_dict = {}
        for pix in os.listdir(name):
            base, ext = os.path.splitext(pix)
            name_dict[base] = os.path.join(name, pix)
        return name_dict

    def getImageKeys(self, name):
        nameKeys = []
        for pix in os.listdir(self.getThemePicsPath(name)):
            base, ext = os.path.splitext(pix)
            nameKeys.append(base)
        return nameKeys

    def getThemePicsPath(self, theme):
        cwd = os.path.dirname(__file__)
        dirs = ['pics', 'styles', theme]
        for d in dirs: cwd = os.path.join(cwd, d)
        cwd = cwd.replace('\\', '/')
        return cwd

    def styleImages(self, name):
        script = '''
        set imgdir %s

        proc LoadImages {imgdir} {
            variable I
            foreach file [glob -directory $imgdir *.gif] {
                set img [file tail [file rootname $file]]
                set I($img) [image create photo -file $file -format gif89]
            }
        }

        array set I [LoadImages $imgdir]''' % self.getThemePicsPath(name)

        self.tk.eval(script)
        nameKeys = self.getImageKeys(name)
        imageKeys = {}
        for key in nameKeys:
            tkImageName = self.tk.eval(f'return $I({key})')
            imageKeys[key] = tkImageName
        return imageKeys

    def createPrmp(self):
        if PRMP_Style.LOADED: return

        self._images = (

         tk.PhotoImage("img_close", data='''R0lGODlhDAAMAIQUADIyMjc3Nzk5OT09PT
                 8/P0JCQkVFRU1NTU5OTlFRUVZWVmBgYGF hYWlpaXt7e6CgoLm5ucLCwszMzNbW
                 1v//////////////////////////////////// ///////////yH5BAEKAB8ALA
                 AAAAAMAAwAAAUt4CeOZGmaA5mSyQCIwhCUSwEIxHHW+ fkxBgPiBDwshCWHQfc5
                 KkoNUtRHpYYAADs= '''),

         tk.PhotoImage("img_closeactive", data='''R0lGODlhDAAMAIQcALwuEtIzFL46
                 INY0Fdk2FsQ8IdhAI9pAIttCJNlKLtpLL9pMMMNTP cVTPdpZQOBbQd60rN+1rf
                 Czp+zLxPbMxPLX0vHY0/fY0/rm4vvx8Pvy8fzy8P//////// ///////yH5BAEK
                 AB8ALAAAAAAMAAwAAAVHYLQQZEkukWKuxEgg1EPCcilx24NcHGYWFhx P0zANBE
                 GOhhFYGSocTsax2imDOdNtiez9JszjpEg4EAaA5jlNUEASLFICEgIAOw== '''),

         tk.PhotoImage("img_closepressed", data='''R0lGODlhDAAMAIQeAJ8nD64qELE
                 rELMsEqIyG6cyG7U1HLY2HrY3HrhBKrlCK6pGM7lD LKtHM7pKNL5MNtiViNaon
                 +GqoNSyq9WzrNyyqtuzq+O0que/t+bIwubJw+vJw+vTz+zT z////////yH5BAE
                 KAB8ALAAAAAAMAAwAAAVJIMUMZEkylGKuwzgc0kPCcgl123NcHWYW Fs6Gp2mYB
                 IRgR7MIrAwVDifjWO2WwZzpxkxyfKVCpImMGAeIgQDgVLMHikmCRUpMQgA7 '''),
        )

        elements_creating = {
            'close': {
                'element create': ['image', 'img_close', ("active", "pressed", "!disabled", "img_closepressed"), ("active", "alternate", "!disabled", "img_closeactive"), {'border': 8, 'sticky': ''}]
            },
        }
        settings = self.settings
        elements_creating.update(settings)
        settings = elements_creating

        self.theme_create('prmp', settings=settings)
        PRMP_Style.LOADED = True

    @property
    def settings(self):

        button_color =   PRMP_Theme.DEFAULT_BUTTON_COLOR
        prmpsmart_botton_color = PRMP_Theme.OFFICIAL_PRMPSMART_BUTTON_COLOR
        error_button_color = PRMP_Theme.DEFAULT_ERROR_BUTTON_COLOR
        foreground = PRMP_Theme.DEFAULT_FOREGROUND_COLOR
        background = PRMP_Theme.DEFAULT_BACKGROUND_COLOR
        text_background = PRMP_Theme.DEFAULT_INPUT_ELEMENTS_COLOR
        text_foreground = PRMP_Theme.DEFAULT_INPUT_TEXT_COLOR
        scrollbar_color = PRMP_Theme.DEFAULT_SCROLLBAR_COLOR
        progressbar_color = PRMP_Theme.DEFAULT_PROGRESS_BAR_COLOR
        relief = PRMP_Theme.DEFAULT_RELIEF

        # default_font = self.tupledFont(PRMP_Theme.DEFAULT_FONT)
        # normal_font = self.tupledFont(PRMP_Theme.NORMAL_FONT)
        # big_font = self.tupledFont(PRMP_Theme.BIG_FONT)
        # menu_font = self.tupledFont(PRMP_Theme.DEFAULT_MENU_FONT)
        # button_font = self.tupledFont(PRMP_Theme.DEFAULT_BUTTON_FONT)
        # buttons_font = self.tupledFont(PRMP_Theme.DEFAULT_BUTTONS_FONT)
        # small_button_font = self.tupledFont(PRMP_Theme.DEFAULT_SMALL_BUTTON_FONT)
        # title_font = self.tupledFont(PRMP_Theme.DEFAULT_TITLE_FONT)
        # status_font = self.tupledFont(PRMP_Theme.DEFAULT_STATUS_FONT)
        # label_font = self.tupledFont(PRMP_Theme.DEFAULT_LABEL_FONT)
        # labelframe_font = self.tupledFont(PRMP_Theme.DEFAULT_LABELFRAME_FONT)
        # heading_font = self.tupledFont(PRMP_Theme.HEADING_FONT)

        default_font = 'DEFAULT_FONT'
        normal_font = 'NORMAL_FONT'
        big_font = 'BIG_FONT'
        menu_font = 'DEFAULT_MENU_FONT'
        button_font = 'DEFAULT_BUTTON_FONT'
        buttons_font = 'DEFAULT_BUTTONS_FONT'
        small_button_font = 'DEFAULT_SMALL_BUTTON_FONT'
        title_font = 'DEFAULT_TITLE_FONT'
        status_font = 'DEFAULT_STATUS_FONT'
        label_font = 'DEFAULT_LABEL_FONT'
        labelframe_font = 'DEFAULT_LABELFRAME_FONT'
        heading_font = 'HEADING_FONT'


        oneColor = True

        if isinstance(button_color, tuple): button_foreground, button_background = button_color
        else:
            background, foreground = 'white', 'black'
            button_foreground, button_background = foreground, background

        _settings = {
            '.': {
                'configure': {
                    'foreground': foreground,
                    'background': background,
                    'relief': 'groove',
                    'anchor': 'center',
                    'font': normal_font
                },
                'map': {
                    'anchor': [('hover', 'nw')],
                    'relief': [('pressed', 'solid'), ('selected', 'solid')],
                }
            },
            'TButton': {
                'configure': {
                    'anchor': 'center',
                    # 'font': 'DEFAULT_BUTON_FONT',
                    'font': button_font,
                    'foreground': button_foreground,
                    'background': button_background,
                    # 'border': 7
                },
               'map': {
                    # 'relief': [('pressed', 'solid'), ('hover', 'solid'), ('focus', 'solid'), ('selected', 'solid')],
                    'foreground': [('disabled', 'black'), ('pressed', background)],
                    'background': [('pressed', foreground)],
                },
                'layout': [('Button.border', {'sticky': 'nswe', 'children': [('Button.focus', {'sticky': 'nswe', 'children': [('Button.padding', {'sticky': 'nswe', 'children': [('Button.label', {'sticky': 'nswe'})]})]})]})]
            },
            'exit.TButton': {
                'map': {
                    # 'relief': [('hover', 'flat')],
                    'background': [('hover', 'red')],
                    'anchor': [('hover', 'center')]
                }
            },
            'green.TButton': {
                'map': {
                    # 'relief': [('hover', 'flat')],
                    'background': [('hover', 'green')],
                    'anchor': [('hover', 'center')]
                }
            },
            'yellow.TButton': {
                'map': {
                    # 'relief': [('hover', 'flat')],
                    'background': [('hover', 'yellow')],
                    'anchor': [('hover', 'center')]
                }
            },
            'TCheckbutton': {
                'configure': {
                    'indicatorcolor': background,
                    'padding': 2,
                    'font': buttons_font,
                    'indicatorrelief': 'solid',
                },
                'map': {
                    # 'relief': [('selected', 'solid'), ('hover', 'solid')],
                    'indicatorcolor': [('pressed', background), ('disabled', button_background), ('selected', foreground)]
                },
                'layout': [('Checkbutton.border', {'children': [('Checkbutton.focus', {'sticky': 'nswe', 'children': [('Checkbutton.padding', {'sticky': 'nswe', 'children': [('Checkbutton.indicator', {'side': 'left', 'sticky': ''}), ('Checkbutton.label', {'side': 'left', 'sticky': 'nswe'})]})]})]})]
            },
            'TCombobox': {
                'configure': {
                    'foreground': text_foreground,
                    'fieldbackground': text_background,
                    # 'selectborderwidth': 2,
                    # 'padding': 2,
                    # 'insertwidth': 2,
                    'arrowcolor': foreground
                },
                'layout': [('Combobox.border', {'children': [('Combobox.field', {'sticky': 'nswe', 'children': [
                    # ('Combobox.uparrow', {'side': 'right', 'sticky': 'ns'}),
                    ('Combobox.downarrow', {'side': 'right', 'sticky': 'ns'}), ('Combobox.padding', {'expand': '1', 'sticky': 'nswe', 'children': [('Combobox.textarea', {'sticky': 'nswe'})]})]})]})],
                'map': {
                    'relief': [('hover', 'solid')]
                }
            },
            'dropdownEntry.TCombobox': {
                'configure': {
                    'font': 'DEFAULT_FONT'
                }
            },
            'ComboboxPopdownFrame': {
                'configure': {
                    'background': background
                },
                'layout': [('ComboboxPopdownFrame.background', {'sticky': 'news', 'border': 1, 'children': [('ComboboxPopdownFrame.padding', {'sticky': 'news'})]})]
            },
            'TEntry': {
                'configure': {
                    'foreground': text_foreground,
                    'fieldbackground': text_background,
                    # 'selectborderwidth': .5,
                    # 'padding': .5,
                    # 'insertwidth': .5,
                },
                'layout': [('Entry.border', {'children':[('Entry.field', {'sticky': 'nswe', 'border': '1', 'children': [('Entry.padding', {'sticky': 'nswe', 'children': [('Entry.textarea', {'sticky': 'nswe'})]})]})]})],
                'map': {
                    'relief': [('hover', 'solid')],
                    'selectforeground': [('!focus', 'SystemWindow')]
                }
            },
            'LightAll.TEntry': {
                'configure': {
                    'background': text_background
                }
            },
            'LightAll.TCombobox': {
                'configure': {
                    'background': text_background
                }
            },
            'TFrame': {
                'configure': {
                    'background': background,
                    'relief': 'flat'
                }
            },
            'TLabel': {
                'configure': {
                    'anchor': 'center',
                    'font': label_font,
                },
                'layout': [('Label.border', {'sticky': 'nswe', 'border': '1', 'children': [('Label.padding', {'sticky': 'nswe', 'border': '1', 'children': [('Label.label', {'sticky': 'nswe'})]})]})]
            },
            'entry.TLabel': {
                'configure': {
                    'background': text_background,
                    'foreground': text_foreground,
                    'font': default_font,
                }
            },
            'tooltip.entry.TLabel': {
                'configure': {
                    'relief': 'solid'
                }
            },
            'TLabelframe': {
                'configure': {
                    'background': background,
                    # 'labeloutside': 1,
                    'labelmargins': (14, 0, 14, 4)
                }
            },
            'TLabelframe.Label': {
                'configure': {
                    'font': labelframe_font,
                    'background': background
                }
            },
            'TMenubutton': {
                'configure': {
                    'relief': 'flat'
                },
                'layout': [('Menubutton.border', {'sticky': 'nswe', 'children': [('Menubutton.focus', {'sticky': 'nswe', 'children': [('Menubutton.indicator', {'side': 'right', 'sticky': ''}), ('Menubutton.padding', {'expand': '1', 'sticky': 'we', 'children': [('Menubutton.label', {'side': 'left', 'sticky': ''})]})]})]})]
            },
            'Window.TMenubutton': {
                'configure': {
                    'relief': 'flat',
                    'overrelief': 'groove'
                },
                'mapping': {
                    'relief': [('hover', 'sunken')],
                    'backgound': [('hover', foreground)],
                    'foregound': [('hover', background)]
                },
                # 'layout': [('Menubutton.border', {'sticky': 'nswe', 'children': [('Menubutton.focus', {'sticky': 'nswe', 'children': [('Menubutton.indicator', {'side': 'right', 'sticky': ''}), ('Menubutton.padding', {'expand': '1', 'sticky': 'we', 'children': [('Menubutton.label', {'side': 'left', 'sticky': ''})]})]})]})]
                'layout': [('Menubutton.border', {'sticky': 'nswe', 'children': [('Menubutton.focus', {'sticky': 'nswe', 'children': [('Menubutton.padding', {'expand': '1', 'sticky': 'we', 'children': [('Menubutton.label', {'side': 'left', 'sticky': ''})]})]})]})]
            },
            'TPanedwindow': {
                '': ''
            },
            'TRadiobutton': {
                'configure': {
                    'indicatorcolor': background,
                    'font': label_font,
                    'anchor': 'top',
                    # 'indicatorrelief': 'flat',
                    # 'indicatormargin': (1,1,4,1),
                    # 'indicatorbackground': 'red'
                    'padding': (0, 0, 0, 0),

                },
                'map': {
                    'indicatorcolor': [('pressed', background), ('disabled', button_background), ('selected', foreground)]
                },
                'layout': [('Radiobutton.border', {'children': [('Radiobutton.focus', {'sticky': 'nswe', 'children': [('Radiobutton.padding', {'sticky': 'nswe', 'children': [('Radiobutton.indicator', {'side': 'left'}), ('Radiobutton.label', {'side': 'left', 'expand': 0})]})]})]})]
                # 'layout': [('Radiobutton.border', {'children': [('Radiobutton.padding', {'sticky': 'nswe', 'children': [('Radiobutton.indicator', {'side': 'left', 'sticky': ''}), ('Radiobutton.focus', {'side': 'left', 'sticky': '', 'children': [('Radiobutton.label', {'sticky': 'nswe'})]})]})]})]
            },
            'Group.TRadiobutton': {
                'map': {
                    'indicatorcolor': [('pressed', background), ('disabled', button_background), ('selected', background)],
                    'background': [('selected', foreground)],
                    'foreground': [('selected', background)],
                    'relief': [('hover', 'solid')]
                }
            },
            'Vertical.TScrollbar': {
                'layout': [('Scrollbar.label', {'children': [('Scrollbar.uparrow', {'side': 'top', 'sticky': 'ns'}),('Scrollbar.downarrow', {'side': 'bottom', 'sticky': 'ns'}), ('Vertical.TScrollbar.thumb', {'side': 'left', 'sticky': 'ns'})
                    ]})
                ]
            },
            'Vertical.TScrollbar': {
                'configure': {
                    'troughcolor': foreground,
                    'arrowcolor': foreground,
                }
            },
            'Horizontal.TScrollbar': {
                'layout': [
                    ('Scrollbar.trough', {'children': [('Scrollbar.leftarrow', {'side': 'left', 'sticky': 'we'}), ('Scrollbar.rightarrow', {'side': 'right', 'sticky': 'we'}), ('Horizontal.TScrollbar.thumb', {'side': 'left', 'expand': '1', 'sticky': 'we'})
                    ]})
                ]
            },
            'Horizontal.TScrollbar': {
                'configure': {
                    'troughcolor': foreground,
                    'arrowcolor': foreground,
                }
            },
            'Toolbar': {
                'configure': {
                    'width': 0,
                    'relief': 'flat',
                    'borderwidth': 2,
                    'padding': 4,
                    'background': background,
                    'foreground': '#000000'
                },
                # 'map': {
                #     'background': [
                #         ('active', selectbg)
                #     ],
                #     'foreground': [
                #         ('active', selectfg)
                #     ],
                #     'relief': [
                #         ('disabled', 'flat'),
                #         ('selected', 'sunken'),
                #         ('pressed', 'sunken'),
                #         ('active', 'raised')
                #     ]
                # }
            },
            'TNotebook': {
                'layout': [('client', {'sticky': 'nswe'})]
            },
            'TNotebook.Tab': {
                'layout': [('tab', {'sticky': 'nswe', 'children': [('padding', {'side': 'top', 'sticky': 'nswe', 'children': [('focus', {'side': 'top', 'sticky': 'nswe', 'children': [('label', {'side': 'left', 'sticky': ''}), ('close', {'side': 'left', 'sticky': ''})]})]})]})]
            },
            'TProgressbar': {
                'configure': {
                    'background': foreground,
                    'pbarrelief': 'raised',
                    'troughrelief': 'sunken',
                    'troughcolor': background,
                    'period': 100,
                    'maxphase': 255
                },
                'map': {
                    'pbarrelief': [('hover', 'flat')],
                    'troughrelief': [('hover', 'solid')]
                }
            },
            'TSpinbox': {
                'configure': {
                    'foreground': text_foreground,
                    'background': text_background,
                    'fieldbackground': text_background,
                    # 'arrowsize': 15,
                    # 'selectborderwidth': 2,
                    # 'padding': 2,
                    # 'insertwidth': 2,
                    # 'arrowcolor': foreground,
                    'arrowcolor': background,
                },
                'layout': [('Spinbox.border', {'children': [('Spinbox.field', {'side': 'top', 'sticky': 'we', 'children': [('null', {'side': 'right', 'sticky': '', 'children': [('Spinbox.uparrow', {'side': 'top', 'sticky': 'n'}), ('Spinbox.downarrow', {'side': 'right', 'sticky': 's'})]}), ('Spinbox.padding', {'sticky': 'nswe', 'children': [('Spinbox.textarea', {'sticky': 'nswe'})]})]})]})]
            },
            'Vertical.TScale': {
                'configure': {
                    'relief': 'sunken',
                    'indicatorcolor': 'red',
                    'troughcolor': foreground,
                    'troughrelief': 'sunken',
                    'sliderrelief': 'flat'
                },
                'layout': [('border', {'children': [('Vertical.Scale.trough', {'sticky': 'nswe', 'children': [('Vertical.Scale.slider', {'side': 'top', 'sticky': ''})]})]})],
                'map': {
                    'sliderrelief': [('hover', 'solid')]
                }
            },
            'Horizontal.TScale': {
                'configure': {
                    'relief': 'sunken',
                    'indicatorcolor': 'red',
                    'troughcolor': foreground,
                    'troughrelief': 'sunken',
                    'sliderrelief': 'flat',
                    'sliderwidth': 'ridge'
                },
                'layout': [('border', {'children': [('Horizontal.Scale.trough', {'sticky': 'nswe', 'children': [('Horizontal.Scale.slider', {'side': 'left', 'sticky': ''})]})]})],
                'map': {
                    'sliderrelief': [('hover', 'solid')]
                }
            },
            'TPanedwindow': {
                'configure': {
                    'indicatorrelief': 'solid',
                },
                'layout': [('border', {'children': [('Panedwindow.background', {'sticky': ''})]})]
            },
            'Sash': {
                'configure': {
                    'sashthickness': 6,
                    'gripcount': 10
                }
            },
            'Treeview': {
                'configure': {
                    'rowheight': 28,
                    'fieldbackground': background,
                    'relief': 'raised',
                    # 'columnfont': heading_font,
                },
                'map': {
                    'background': [('selected', text_background), ('hover', button_background)],
                    'foreground': [('selected', text_foreground), ('hover', button_foreground)],
                    'relief': [('hover', 'ridge')]
                }
            },
            # 'TreeCtrl': {
            #     'configure': {
            #         'background': 'red',
            #         'itembackground': 'pink',
            #         'itemfill': 'blue',
            #         'itemaccentfill': 'yellow'
            #     }
            # },
            'Heading': {
                'configure': {
                    'font': heading_font,
                    'relief': 'raised',
                    'background': text_background,
                    'foreground': text_foreground
                },
                'map': {
                    'background': [('pressed', background)],
                    'foreground': [('pressed', foreground)],
                    # 'relief': [('hover', 'flat')]
                }
            },
            'Column': {
                'configure': {
                    'relief': 'raised'
                },
                'map': {
                    'background': [('selected', 'black')],
                    'foreground': [('selected', 'white')]
                }
            },
            'Row': {
                'configure': {
                    'relief': 'groove'
                },
                'map': {
                    'rowbackground': [('selected', 'black')],
                    'foreground': [('selected', 'white')],

                },
                'layout': [('Treeitem.border', {'children': [('Treeitem.row', {'sticky': 'nswe'})]})]
            },
            'Item': {
                'configure': {
                    'font': heading_font,
                    'relief': 'flat'
                },
                'map': {
                    'background': [('selected', 'red')],
                    'foreground': [('selected', 'yellow')],
                    'relief': [('hover', 'solid')]
                },
                'layout': [('border', {'children': [('Treeitem.padding', {'sticky': 'nswe', 'children': [('Treeitem.indicator', {'side': 'left', 'sticky': 'nw'}), ('Treeitem.image', {'side': 'left', 'sticky': ''}), ('Treeitem.text', {'side': 'left', 'sticky': ''})]})]})]
                # 'layout': [('border', {'children': [('Treeitem.padding', {'sticky': 'nswe', 'children': [('Treeitem.indicator', {'side': 'left', 'sticky': 'nw'}), ('Treeitem.image', {'side': 'left', 'sticky': ''}), ('Treeitem.focus', {'side': 'left', 'sticky': '', 'children': [('Treeitem.text', {'side': 'right', 'sticky': ''})]})]})]})]
            },
        }
        PRMP_Window.TOPEST.event_generate('<<PRMP_STYLE_CHANGED>>')
        return _settings

    def update(self, event=None):
        if not PRMP_Style.LOADED: self.createPrmp()
        self.theme_settings('prmp', self.settings)
Style = PSt = PRMP_Style

class PRMP_Treeview(PRMP_Style_, ttk.Treeview):
    TkClass = ttk.Treeview

    def __init__(self, master=None, config={}, callback=None, tipping={}, **kwargs):
        '''
        :param tipping: kwargs for the tips on the items of the tree
        '''
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)
        self.bind('<<TreeviewSelect>>', self.selected)

        self.ivd = self.itemsValuesDict = {}
        self.firstItem = None
        self.callback = callback
        self.current = None

        self.tipManager = None
        self.tipping = tipping

        if tipping: self.createTipsManager()

    def createTipsManager(self):
        if not self.tipManager:
            tipping = self.tipping
            if self.tipping:
                if not isinstance(self.tipping, dict): tipping = {}
            self.tipManager = PRMP_ToolTipsManager(self, **tipping)

    def addItemTip(self, item, tip):
        if tip:
            self.createTipsManager()
            self.tipManager.add_tooltip(item, text=tip)

    def getChildren(self, item=None):
        children = self.get_children(item)
        childrenList = []

        for child in children:
            childValue = self.ivd[child]
            childDicts = self.getChildren(child)
            if childDicts: childValue = {childValue: childDicts}

            childrenList.append(childValue)

        leng = len(childrenList)

        if not leng: return None
        elif leng > 1: return childrenList
        else: return childrenList[0]

    def insert(self, item, position='end',  value=None, text='', tip='', **kwargs):
        newItem = ttk.Treeview.insert(self, item, position, text=text, **kwargs)

        self.ivd[newItem] = value or text
        # print(self.ivd)
        if tip: self.addItemTip(newItem, tip)

        return newItem


    def delete(self, *items):
        for item in items:
            children = self.get_children(item)
            for child in children:
                if child in self.ivd: del self.ivd[child]
            if item in self.ivd: del self.ivd[item]
        ttk.Treeview.delete(self, items)

    def selected(self, event=None):
        item = self.focus()
        self.current = self.ivd.get(item)
        if self.callback: self.callback(self.current)
        return self.current

    def deleteAll(self):
        children = self.get_children()
        for child in children: self.delete(child)
    clear = deleteAll

Treeview = PTv = PRMP_Treeview

#   common to tk and ttk

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

        PRMP_.__init__(self, master=master,config=config, **kwargs)
Menu = PM = PRMP_Menu

class PRMP_Menubutton(PRMP_Style_, ttk.Menubutton):
    TkClass = ttk.Menubutton

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)
Menubutton = PM = PRMP_Menubutton

class PRMP_OptionMenu(PRMP_, tk.OptionMenu):
    TkClass = tk.OptionMenu

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master,config=config, **kwargs)
OptionMenu = PO = PRMP_OptionMenu

class PRMP_PanedWindow(PRMP_, tk.PanedWindow):
    TkClass = tk.PanedWindow

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master,config=config, **kwargs)
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

        PRMP_.__init__(self, master=master,config=config, **kwargs)
Scale = PS = PRMP_Scale

class PRMP_Scrollbar(PRMP_, tk.Scrollbar):
    TkClass = tk.Scrollbar

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master,config=config, **kwargs)

    def set(self, first, last): return ttk.Scrollbar.set(self, first, last)
Scrollbar = PSc = PRMP_Scrollbar

class PRMP_Spinbox(PRMP_Input, PRMP_, tk.Spinbox):
    TkClass = tk.Spinbox

    def __init__(self, master=None, config={}, **kwargs):

        PRMP_.__init__(self, master=master,config=config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)

    def get(self): return float(self.TkClass.get(self))

Spinbox = PSp = PRMP_Spinbox

#   from ttk widgets --> PRMP_Style_

class PRMP_Style_Button(PRMP_Style_, ttk.Button):
    TkClass = ttk.Button

    def __init__(self, master=None, font='DEFAULT_BUTTON_FONT', asEntry=False, asLabel=False, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,font=font, asEntry=asEntry, config=config, **kwargs)
SButton = PSB = PRMP_Style_Button

class PRMP_Style_Checkbutton(PRMP_InputButtons, PRMP_Style_, ttk.Checkbutton):
    TkClass = ttk.Checkbutton

    def __init__(self, master=None, asLabel=False, config={}, var=1, **kwargs):
        PRMP_Style_.__init__(self, master=master, asLabel=asLabel, config=config, var=var, **kwargs)

        self.toggleSwitch()
SCheckbutton = PSC = PRMP_Style_Checkbutton

class PRMP_Style_Entry(PRMP_Input, PRMP_Style_, ttk.Entry):
    TkClass = ttk.Entry

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master, config=config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)
SEntry = PSE = PRMP_Style_Entry

class PRMP_Style_Frame(PRMP_Style_, ttk.Frame):
    TkClass = ttk.Frame

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, nonText=True, **kwargs)
SFrame = PSF = PRMP_Style_Frame

class PRMP_Style_Label(PRMP_Style_, ttk.Label):
    TkClass = ttk.Label

    def __init__(self, master=None, font='DEFAULT_LABEL_FONT', config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,font=font, config=config, **kwargs)
SLabel = PSL = PRMP_Style_Label

class PRMP_Style_LabelFrame(PRMP_Style_, ttk.LabelFrame):
    TkClass = ttk.LabelFrame

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master, config=config, **kwargs)
SLabelFrame = PSLF = PRMP_Style_LabelFrame

class PRMP_Style_Menubutton(PRMP_Style_, ttk.Scrollbar):
    TkClass = ttk.Scrollbar

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)
SScrollbar = PSM = PRMP_Style_Menubutton

class PRMP_Style_OptionMenu(PRMP_Style_, ttk.OptionMenu):
    TkClass = ttk.OptionMenu

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)
SOptionMenu = PSO = PRMP_Style_OptionMenu

class PRMP_Style_PanedWindow(PRMP_Style_, ttk.PanedWindow):
    TkClass = ttk.PanedWindow

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)
SPanedWindow = PSP = PRMP_Style_PanedWindow

class PRMP_Style_Radiobutton(PRMP_InputButtons, PRMP_Style_, ttk.Radiobutton):
    TkClass = ttk.Radiobutton

    def __init__(self, master=None, asLabel=False, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,asLabel=asLabel, config=config, **kwargs)
SRadiobutton = PSR = PRMP_Style_Radiobutton

class PRMP_Style_Scale(PRMP_Style_, ttk.Scale):
    TkClass = ttk.Scale

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)
SScale = PSS = PRMP_Style_Scale

class PRMP_Style_Scrollbar(PRMP_Style_, ttk.Scrollbar):
    TkClass = ttk.Scrollbar

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,config=config, **kwargs)

    def set(self, first, last): return ttk.Scrollbar.set(self, first, last)
SScrollbar = PSSc = PRMP_Style_Scrollbar

class PRMP_Style_Spinbox(PRMP_Input, PRMP_Style_, ttk.Spinbox):
    TkClass = ttk.Spinbox

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master, config=config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)
SSpinbox = PSSp = PRMP_Style_Spinbox

#  windows

class PRMP_Window(PRMP_Widget):
    TOPEST = None
    STYLE = None

    TKICON = ''
    PRMPICON = ''

    TIPSMANAGER = None

    TkClass = None

    def start(self):
        self.paint()
        self.mainloop()

    def __init__(self, container=True, containerConfig={},  gaw=None, ntb=None, tm=None, tw=None, grabAnyWhere=True, geo=(300, 300), geometry=(), noTitleBar=True, topMost=False, alpha=1, toolWindow=False, side='center', title='Window', bindExit=True, nrz=None, notResizable=False, atb=None, asb=None, be=None, resize=(1, 1), addStatusBar=True, addTitleBar=True, tkIcon='', prmpIcon='', grab=False, b4t=None, bind4Theme=1, toggleMenuBar=False, tbm=None, normTk=False, normStyle=False, tipping=False, tt=None, tooltype=False, noWindowButtons=False, nwb=None, themeIndex=0, theme='', **kwargs):

        if themeIndex: PRMP_Theme.setThemeIndex(themeIndex)
        elif theme: PRMP_Theme.setTheme(theme)


        PRMP_Widget.__init__(self, geo=geo, nonText=True, **kwargs)

        if PRMP_Window.TOPEST == None:
            self.bind('<<PRMP_STYLE_CHANGED>>', self.paint)
            PRMP_Window.TOPEST = self
            self.createDefaultFonts()
            if not normStyle: PRMP_Window.STYLE = PRMP_Style(self)
            if tipping: PRMP_Window.TIPSMANAGER = PRMP_ToolTipsManager(self)

        self.container = None
        self.zoomed = False
        self.iconed = False
        self.titleBar = None
        self.menuBar = None
        self.statusBar = None
        self.side = side
        self.titleText = title

        self.__afters = []

        self.title(title)
        self.co = 0


        if container:
            self.container = PRMP_Style_Frame(self)
            self.container.configure(relief='groove')

        if normTk: atb, asb, geo = 0, 0, ()

        if geo != None: geometry = geo
        if gaw != None: grabAnyWhere = gaw
        if ntb != None: noTitleBar = ntb
        if tm != None: topMost = tm
        if nrz != None: notResizable = nrz
        if tw != None: toolWindow = tw
        if be != None: bindExit = be
        if atb != None: addTitleBar = atb
        if asb != None: addStatusBar = asb
        if b4t != None: bind4Theme = b4t
        if tbm != None: toggleMenuBar = tbm
        if tt != None: tooltype = tt
        if nwb != None: noWindowButtons = nwb
        self.noWindowButtons = noWindowButtons

        self.toggleMenuBar = toggleMenuBar
        if notResizable: resize = (0, 0)

        if bindExit and not normTk: self.bindExit()

        if bind4Theme:
            self.bind('<Control-Up>', self.prevTheme)
            self.bind('<Control-Down>', self.nextTheme)

        self.windowAttributes(topMost=topMost, toolWindow=toolWindow, alpha=alpha, noTitleBar=noTitleBar, addTitleBar=addTitleBar, addStatusBar=addStatusBar, prmpIcon=prmpIcon, tkIcon=tkIcon, resize=resize, tooltype=tooltype)

        if grabAnyWhere: self._grab_anywhere_on()
        else: self._grab_anywhere_off()

        self.bindToWidget(('<Configure>', self.placeContainer), ('<FocusIn>', self.placeContainer), ('<Map>', self.deiconed), ('<Control-M>', self.minimize), ('<Control-m>', self.minimize))

        self.placeOnScreen(side, geometry)
        self.bind('<Control-E>', self.destroySelf)
        self.bind('<Control-e>', self.destroySelf)

        if grab: self.grab_set()
        self.focus()

        self.after(100, self.loadAfters)

    def loadAfters(self):
        for al in self.__afters: al()

    def addAfters(self, child):
        if child not in self.__afters:
            if isinstance(child, (list, tuple)):
                for ch in child: self.addAfters(ch)
            else: self.__afters.append(child)

    def windowAttributes(self, topMost=0, toolWindow=0, alpha=1, noTitleBar=1,  addTitleBar=1, addStatusBar=1, tkIcon='', prmpIcon='', resize=(1, 1), tooltype=False):
        self.resize = resize
        self.resizable(*self.resize)

        self.noTitleBar = noTitleBar
        self._addStatusBar = addStatusBar
        self._addTitleBar = addTitleBar

        if addTitleBar:
            if toolWindow: self.__r = 1
            elif self.resize.count(True) > 1: self.__r = 2
            else: self.__r = 0
            self.addTitleBar()
            self.setPRMPIcon(prmpIcon or PRMP_Window.PRMPICON)

        if addStatusBar: self.addStatusBar()

        self.toolWindow = toolWindow
        self.topMost = topMost
        self.alpha = alpha

        if noTitleBar or tooltype:
            self.overrideredirect(True)
            if not tooltype: self.after(10, self.addWindowToTaskBar)

        else: self.attributes('-toolwindow', self.toolWindow, '-alpha', self.alpha, '-topmost', self.topMost)

        self.setTkIcon(tkIcon or PRMP_Window.TKICON)
        self.topmost()

    def topmost(self): self.attributes('-topmost', True)

    def addWindowToTaskBar(self, event=None):
        self.withdraw()
        winfo_id = self.winfo_id()
        parent = ctypes.windll.user32.GetParent(winfo_id)
        res = ctypes.windll.user32.SetWindowLongW(parent, -20, 0)
        self.deiconify()
        if not res: self.after(10, self.addWindowToTaskBar)
        if res: self.attributes('-alpha', self.alpha, '-topmost', self.topMost)

    def placeOnScreen(self, side='', geometry=(400, 300)):
        error_string = f'side must be of {self._sides} or combination of "center-{self._sides[:-1]}" delimited by "-". e.g center-right. but the two must not be the same.'
        if len(geometry) == 4:
            self.lastPoints = geometry
            side = None

        else: self.lastPoints = [0, 0, 0, 0]

        self._geometry = geometry

        if side and geometry:
            if '-' in side:
                one, two = side.split('-')
                sides = one, two
                assert (one in self._sides) and (two in self._sides), error_string
                assert one != two, error_string
                assert not ((self._top in sides) and (self._bottom in sides)), 'both "top" and "bottom" can not be combined'
                assert not ((self._left in sides) and (self._right in sides)), 'both "left" and "right" can not be combined'

                if self._center in sides:
                    main_side = one if one != self._center else two
                    funcs = {self._top: self.centerOfTopOfScreen, self._left: self.centerOfLeftOfScreen, self._right: self.centerOfRightOfScreen, self._bottom: self.centerOfBottomOfScreen}
                elif self._top in sides:
                    main_side = one if one != self._top else two
                    funcs = {self._right: self.topRightOfScreen, self._left: self.topLeftOfScreen}
                elif self._bottom in sides:
                    main_side = one if one != self._bottom else two
                    funcs = {self._right: self.bottomRightOfScreen, self._left: self.bottomLeftOfScreen}

            else:
                assert side in self._sides, error_string
                main_side = side
                funcs = {self._top: self.topOfScreen, self._left: self.leftOfScreen, self._right: self.rightOfScreen, self._bottom: self.bottomOfScreen, self._center: self.centerOfScreen}
            funcs[main_side]()
        else:
            if geometry: self.setGeometry(geometry)

        self.setGeometry(self.lastPoints)

    @property
    def style(self): return PRMP_Window.STYLE
    @property
    def topest(self): return PRMP_Window.TOPEST

    @property
    def screenwidth(self): return self.winfo_screenwidth()
    @property
    def screenheight(self): return self.winfo_screenheight()
    @property
    def screen_xy(self): return (self.screenwidth, self.screenheight)
    @property
    def paddedScreen_xy(self): return (self.screenwidth-70, self.screenheight-70)

    @property
    def geo(self): return self.kwargs.get('geo')

    @property
    def containerGeo(self): return (self.x_w[1], self.y_h[1])

    @property
    def y_h(self): return (30, self.geo[1]-60)

    @property
    def rel_y_h(self):
        x, y = self.geo[:2]
        _y, h = self.y_h
        return (_y, h/y)

    def YH(self, geo=()):
        if not geo: return self.y_h
        x, y = geo[:2]
        return (30, y-60)

    def XW(self, geo=()):
        if not geo: return self.x_w
        x, y = geo[:2]
        return (2, x-4)

    def relYH(self, geo=()):
        if not geo: return self.rel_y_h
        _y, h = self.y_h
        x, y = geo[:2]
        return (_y, h/y)

    def relXW(self, geo=()):
        if not geo: return self.rel_x_w
        _x, w = self.x_w
        x, y = geo[:2]
        return (_x, w/x)

    @property
    def rel_x_w(self):
        x, y = self.geo[:2]
        _x, w = self.x_w
        return (_x, w/x)

    def getWhichSide(self): return random.randint(1, 15) % 3

    @property
    def getXY(self):
        if self._geometry: return self._geometry[:3]
        return (400, 300)

    def _pointsToCenterOfScreen(self, x, y, *a):
        screen_x, screen_y = self.screen_xy
        show_x = (screen_x - x) // 2
        show_y = (screen_y - y) // 2
        return [x, y, show_x, show_y]

    def position(self, pos):
        if len(pos) == 2:
            x, y = pos
            geo = f'+{x}+{y}'
            self.geometry(geo)

    @property
    def pointsToCenterOfScreen(self): return self._pointsToCenterOfScreen(*self.getXY)

    def getSubbedGeo(self, geo):
        assert isinstance(geo, (tuple, list))
        geo = list(geo)

        while len(geo) < 4: geo.append(0)

        if isinstance(geo, list): geo = tuple(geo)
        return '%dx%d+%d+%d'%geo

    def setGeometry(self, points):
        if points[0] and points[1]:
            self.lastPoints = points
            self.geometry(self.getSubbedGeo(points))

    size = setGeometry

    def centerOfTopOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-1] = 50
        self.setGeometry(points)

    def changeGeometry(self, geo=(400, 300)): self.placeOnScreen(side=self.side, geometry=geo)

    def centerOfScreen(self): self.setGeometry(self.pointsToCenterOfScreen)

    def centerOfBottomOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-1] *= 2
        self.setGeometry(points)

    def centerOfLeftOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2] = 50
        self.setGeometry(points)

    def centerOfRightOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2] *= 2
        points[2] -= 50
        print(points)

        self.setGeometry(points)

    def topLeftOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2:] = 50, 50
        self.setGeometry(points)

    def topRightOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-1] = 50
        points[2] *= 2
        points[2] -= 50
        self.setGeometry(points)

    def bottomLeftOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2] = 50
        points[-1] *= 2
        self.setGeometry(points)

    def bottomRightOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-2] *= 2
        points[-2] -= 50
        points[-1] *= 2
        self.setGeometry(points)

    def topOfScreen(self): [self.topLeftOfScreen, self.topRightOfScreen, self.centerOfTopOfScreen][self.getWhichSide()]()
    def bottomOfScreen(self): [self.bottomLeftOfScreen, self.bottomRightOfScreen, self.centerOfBottomOfScreen][self.getWhichSide()]()
    def rightOfScreen(self): [self.bottomRightOfScreen, self.topRightOfScreen, self.centerOfRightOfScreen][self.getWhichSide()]()
    def leftOfScreen(self): [self.bottomLeftOfScreen, self.topLeftOfScreen, self.centerOfLeftOfScreen][self.getWhichSide()]()

    def _isDialog(self, g=1):
        self.attributes('-toolwindow', 1)
        self.resizable(0, 0)
        if g: self.grab_set()
        self.focus()
        self.wait_window()

    def placeContainer(self, event=None, h=0):
        if self._addTitleBar:
            top = 30
            if self._addStatusBar: bottom = 60
            else: bottom = 30
        else:
            top = 0
            if self._addStatusBar: bottom = 30
            else: bottom = 0

        self.container.place(x=0, y=top, w=self.winfo_width(), h=h or self.winfo_height()-bottom)

        self.placeTitlebar()
        self.placeStatusBar()

    @property
    def x_w(self): return (2, self.geo[0]-4)

    def minimize(self, event=None):
        self.withdraw()
        self.overrideredirect(False)
        self.iconify()
        self.iconed = True

    def deiconed(self, event=None):
        if self.iconed:
            self.co += 1
            self.iconed = False
            v = self.winfo_viewable()
            if v:
                if self.noTitleBar: self.overrideredirect(True)
                self.normal()
                self.addWindowToTaskBar()

    def maximize(self, event=None):
        if self.__r != 2: return

        if self.zoomed:
            self.zoomed = False
            self.TkClass.state(self, 'normal')
            self.isNormal()

        else:
            self.zoomed = True
            self.TkClass.state(self, 'zoomed')
            self.isMaximized()

    def isMaximized(self): pass

    def isMinimized(self): pass

    def isNormal(self): pass

    def setTitle(self, title):
        self.title(title)
        if self.titleBar: self.titleBar.set(title or self.titleText)

    def addTitleBar(self, title=''):
        if self.titleBar:
            self.placeTitlebar()
            return
        F, L, B = PRMP_Style_Frame, PRMP_Style_Label, PRMP_Style_Button

        w, y = self.geo[:2]
        fr = F(self)
        self._min = self._max = self._exit = None

        if not self.noWindowButtons and self.__r != 1:
            self.imgMin = PRMP_Image('green', inbuilt=1, resize=(20, 20)) if _PIL_ else None
            self._min = B(fr, config=dict(command=self.minimize, text=self.min_, image=self.imgMin, style='green.TButton'), tip='Minimize', font='DEFAULT_SMALL_BUTTON_FONT')

            self.imgMax = PRMP_Image('yellow', inbuilt=1, resize=(20, 20)) if _PIL_ else None
            self._max = B(fr, config=dict(command=self.maximize, text=self.max_, image=self.imgMax, style='yellow.TButton'), font='DEFAULT_SMALL_BUTTON_FONT')

        if not self.noWindowButtons:
            self.imgExit = PRMP_Image('red', inbuilt=1, resize=(20, 20)) if _PIL_ else None
            self._exit = B(fr, config=dict(text=self.x_btn2, command=self.destroySelf, image=self.imgExit, style='exit.TButton'), font='DEFAULT_SMALL_BUTTON_FONT')

            self._icon = L(fr)

        self.titleBar = L(fr, config=dict( text=title or self.titleText), font='DEFAULT_TITLE_FONT', relief='groove')
        self.menuBar = F(fr, config=dict(relief='groove'))

        if PRMP_Window.TIPSMANAGER:
            tipm = PRMP_Window.TIPSMANAGER
            tipm.add_tooltip(self._max, text='Maximize')
            tipm.add_tooltip(self._min, text='Minimize')
            tipm.add_tooltip(self._exit, text='Exit')
            tipm.add_tooltip(self.titleBar, text='Right click for MENU bar')
            tipm.add_tooltip(self.menuBar, text='Right click for TITLE bar')

        for bar in [self.titleBar, self.menuBar]:
            bar.bind('<Double-1>', self.maximize, '+')
            bar._moveroot()
            bar.bind('<3>', self.switchMenu)

        self.placeTitlebar()

    def switchMenu(self, e=None):
        if e.widget == self.titleBar: self.toggleMenuBar = True
        else: self.toggleMenuBar = False

        self.placeTitlebar()

    def addToMenu(self, widget, **kwargs):
        if self.titleBar and self.menuBar: self.menuBar.addWidget(widget, **kwargs)

    def closing(self): pass

    def save(self):

        pass

    def destroy(self):
        if self == self.topest:
            PRMP_Window.TOPEST = None
            PRMP_Window.STYLE = None
            PRMP_Style.LOADED = False

        super().destroy()

    def destroySelf(self, event=None):
        self.closing()
        # threading.Thread(target=self.save).start()
        self.save()

        def out(u):
            if not u: return
            self.destroy()
            os.sys.exit(self.save())

        if self == self.topest:
            from .dialogs import PRMP_MsgBox
            PRMP_MsgBox(self, title='Exit', message='Are you sure to exit?', callback=out)
        else: self.destroy()

    def setTkIcon(self, icon):
        if icon: self.iconbitmap(icon)

    def setPRMPIcon(self, icon):
        if icon and _PIL_:
            self.imgIcon = PRMP_Image(icon, resize=(20, 20))
            self._icon['image'] = self.imgIcon

    def placeTitlebar(self):
        if self.titleBar:
            x = self.titleBar.master.winfo_width()
            xw = self.titleBar.master.master.winfo_width()
            self.titleBar.master.place(x=0, rely=0, h=30, w=xw)


            if x < 0: return
            w = 30
            if not self.noWindowButtons and self.__r != 1:
                self._min.place(x=x-90, rely=0, relh=1, w=30)
                self._max.place(x=x-60, rely=0, relh=1, w=30)
                w = 90

            if self.toggleMenuBar: bar, unbar = self.menuBar, self.titleBar
            else: unbar, bar = self.menuBar, self.titleBar

            w = x - w
            if not self.noWindowButtons:
                w -= 30
                x = 30
                self._icon.place(x=0, rely=0, relh=1, w=30)
            else:
                x = 0
                w += 30

            bar.place(x=x, rely=0, relh=1, w=w)
            unbar.place_forget()

            if not self.noWindowButtons: self._exit.place(x=xw-30, rely=0, relh=1, w=30)

    def editStatus(self, text):
        if self.statusBar: self.statusBar.set(text)

    def addStatusBar(self):
        if self.statusBar:
            self.placeStatusBar()
            return

        F, L, B = PRMP_Style_Frame, PRMP_Style_Label, PRMP_Style_Button
        self.statusBar = self._up = self._down = None

        fr = F(self)
        self.statusBar = L(fr, config=dict(text='Status' or self.statusText, ), font='DEFAULT_STATUS_FONT')
        self.statusBar._moveroot()
        self._up = B(fr, config=dict(text=self.upArrow, command=self.prevTheme), font='DEFAULT_SMALL_BUTTON_FONT', tip='Previous Theme')
        self._down = B(fr, config=dict(text=self.downArrow, command=self.nextTheme), font='DEFAULT_SMALL_BUTTON_FONT', tip='Next Theme')

        if PRMP_Window.TIPSMANAGER:
            tipm = PRMP_Window.TIPSMANAGER
            tipm.add_tooltip(self.statusBar, text='Status Bar', follow=1)
            tipm.add_tooltip(self._down, text='Previous Theme')
            tipm.add_tooltip(self._up, text='Next Theme')


        self.placeStatusBar()

    def placeStatusBar(self, event=None):
        if self.statusBar:
            y = self.winfo_height()
            x = self.statusBar.master.winfo_width()
            xw = self.statusBar.master.master.winfo_width()
            if x < 0: return
            if y < 0: return
            h = 30
            self.statusBar.master.place(x=0, y=y-h, h=h, w=xw)
            self.statusBar.place(x=0, rely=0, relh=1, w=x-60)
            self._up.place(x=x-60, rely=0, relh=1, w=30)
            self._down.place(x=x-30, rely=0, relh=1, w=30)

    def prevTheme(self, event=None):
        theme, index = self._prevTheme()
        self.editStatus(f'Theme({theme}) | Index({index})')
        self._colorize()

    def nextTheme(self, event=None):
        theme, index = self._nextTheme()
        self.editStatus(f'Theme({theme}) | Index({index})')
        self._colorize()

    @property
    def caller(self): return self.kwargs.get('caller')

    def _colorize(self):
        topest = self.topest
        if topest:
            topest.style.update()
            topest._paintAll()
        else: return

    def paint(self, event=None):
        self._paintAll()
        self.afterPaint()

    def afterPaint(self): pass

    @property
    def toplevel(self): return self

    def bindExit(self):
        def ex(event=None): os.sys.exit()
        self.bind_all('<Control-/>', ex)

PWin = PRMP_Window

class PRMP_Tk(PRMP_Window, tk.Tk):
    TkClass = tk.Tk
    def __init__(self, _ttk_=False, **kwargs):

        PRMP_Window.__init__(self, _ttk_=_ttk_, **kwargs)
Tk = PT = PRMP_Tk

class PRMP_Toplevel(PRMP_Window, tk.Toplevel):
    TkClass = tk.Toplevel
    def __init__(self, master=None, _ttk_=False, **kwargs):

        if isinstance(master, PRMP_Widget):
            try: kwargs['side'] = kwargs.get('side') or master.toplevel.side
            except AttributeError as y: print(y)

        PRMP_Window.__init__(self, _ttk_=_ttk_, **kwargs)
Toplevel = PTl = PRMP_Toplevel


class PRMP_MainWindow(PRMP_Mixins):

    def __init__(self, master=None, _ttk_=False, **kwargs):

        master = master or PRMP_Window.TOPEST

        if master: self.root = PRMP_Toplevel(master, _ttk_=_ttk_, **kwargs)
        else: self.root = PRMP_Tk(_ttk_=_ttk_, **kwargs)
        # self.root.root = self.root

        for k, v in self.class_.__dict__.items():
            if k.startswith('__') or k == 'root': continue
            if callable(v): self.root.__dict__[k] = functools.partial(v, self)


    def __str__(self): return str(self.root)

    def __getitem__(self, name):
        attr = self.getFromSelf(name, self._unget)
        if attr != self._unget: return attr
        else: return getattr(self.root, name)

    def __getattr__(self, name): return self[name]

MainWindow = PMW = PRMP_MainWindow

# ToolTips

class Commons:

    def __setitem__(self, key, value): self.configure(**{key: value})

    def __getitem__(self, key): return self.cget(key)

    def cget(self, key):
        if key == self.key: return self.keyval() if callable(self.keyval) else self.keyval
        else: return self.cgetsub(key) if self.cgetsub else self.cgetsub

class PRMP_ToolTip(Commons, Toplevel):
    'Create a tooltip'
    _initialized = False

    def __init__(self, master, bg='', background='', fg='', foreground='', font='', alpha=.8, pos=None, position=(), text='', _ttk_=0, relief='solid', **kwargs):
        '''
        Construct a Tooltip with parent master.
        kwargs: ttk.Label options,
        alpha: float. Tooltip opacity between 0 and 1.
        '''

        foreground = fg or foreground
        background = bg or background
        position = pos or position or ()

        k = {}
        if Toplevel != tk.Toplevel: k.update(dict(normTk=1))

        super().__init__(master, background=background, padx=0, pady=0, tooltype=True, **k)
        self.transient(master)
        # self.overrideredirect(True)
        self.update_idletasks()
        self.attributes('-alpha', alpha or 0.8, '-topmost', 1)

        if 'linux' in sys.platform: self.attributes('-type', 'tooltip')

        style_dict = {}

        self.updateFg = not bool(foreground)
        self.updateBg = not bool(background)
        self.updateFont = not bool(font)

        if not self.updateFg: style_dict['foreground'] = foreground
        if not self.updateBg: style_dict['background'] = background
        if not self.updateFont: style_dict['font'] = font

        if _ttk_ and not ToolTip._initialized:
            # default tooltip style
            style = ttk.Style(self)
            style.configure('tooltip.TLabel',  relief=relief, **style_dict)
            ToolTip._initialized = True

        # default options
        kw = dict(compound='left', style='tooltip.TLabel', padding=4, text=text, justify=tk.LEFT, relief=tk.SOLID, borderwidth=1)
        # update with given options
        kw.update(kwargs)

        if not _ttk_:
            # do some editting for the tk.Label widget
            del kw['style'], kw['padding']
            kw.update(style_dict)
            Label = tk.Label
        else: Label = ttk.Label

        self.label = Label(self, **kw)
        self.label.pack(fill='both')

        self.key = 'alpha'
        self.keyval = lambda : self.attributes('-alpha')
        self.cgetsub = self.label.cget

        if position: self.position(pos)

    def configure(self, **kwargs):
        if 'alpha' in kwargs: self.attributes('-alpha', kwargs.pop('alpha'))
        self.label.configure(**kwargs)

    config = configure

    def update_style(self):
        style_dict = {}
        if self.updateFg: style_dict['foreground'] = PRMP_Theme.DEFAULT_INPUT_TEXT_COLOR
        if self.updateBg: style_dict['background'] = PRMP_Theme.DEFAULT_INPUT_ELEMENTS_COLOR
        if self.updateFont: style_dict['font'] = 'DEFAULT_FONT'

        self.configure(**style_dict)


    def deiconify(self):
        self.update_style()
        super().deiconify()

    def keys(self):
        keys = list(self.label.keys())
        keys.insert(0, 'alpha')
        return keys

    def position(self, pos):
        if len(pos) == 2:
            x, y = pos
            geo = f'+{x}+{y}'
            self.geometry(geo)

ToolTip = PRMP_ToolTip

class PRMP_ToolTipsManager:

    def __init__(self, widget=None, delay=200, text='', **kwargs):

        self.widget = widget
        self.istree = isinstance(widget, ttk.Treeview)

        self.tooltip_text = {}
        self.tooltip_follows = {}
        self.tooltip_delays = {}

        # time delay before displaying the tooltip
        self.delay = delay
        self.kwargs = kwargs
        self.timer_id = None

        self.tooltip = None

        self.key = 'delay'
        self.keyval = self.delay
        self.current_widget = None

        self.text = text

        # self.configure(**kwargs)
        if self.text:
            self.tooltip_follows[str(self.widget)] = kwargs.pop('follow', False)
            self.widget.bind('<Enter>', self.enter, add=1)
            self.widget.bind('<Motion>', self.motion, add=1)
            self.widget.bind('<Leave>', self.leave, add=1)
            self.widget.bind('<ButtonPress>', self.leave, add=1)
        elif not self.istree:
            # keep track of binding ids to cleanly remove them
            self.bind_enter_ids = {}  # {widget name: bind id, ...}
            self.bind_leave_ids = {}  # {widget name: bind id, ...}
            # widget currently under the mouse if among wrapped widgets:
        else:
            self.current_widget = self.widget
            self.widget.bind('<Motion>', self._on_motion_tree, add=1)
            self.widget.bind('<Leave>', self._on_leave, add=1)

 # for a single widget
    def motion(self, event=None):
        if self.tooltip and self.tooltip_follows[str(self.widget)]: self.tooltip.position((event.x_root+20, event.y_root-10))

    def enter(self, event=None):
        '''
        Called by tkinter when mouse enters a widget
        :param event:  from tkinter.  Has x,y coordinates of mouse

        '''
        if str(event.widget) != str(self.widget): return

        self.x, self.y = event.x, event.y

        # Schedule a timer to time how long mouse is hovering
        self.id = self.widget.after(self.delay, self.showtip)

    def leave(self, event=None):
        '''
        Called by tkinter when mouse exits a widget
        :param event:  from tkinter.  Event info that's not used by function.

        '''
        # Cancel timer used to time mouse hover
        if self.id: self.widget.after_cancel(self.id)
        self.id = None

        # Destroy the tooltip window
        if self.tooltip: self.tooltip.destroy()
        self.tooltip = None

    def showtip(self, event=None):
        '''
        Creates a tooltip window with the tooltip text inside of it
        '''
        if self.tooltip: return
        self.lastMotion = 0

        x = self.widget.winfo_rootx() + self.x
        y = self.widget.winfo_rooty() + self.y - 20

        self.tooltip = PRMP_ToolTip(self.widget, pos=(x, y), text=self.text, **self.kwargs)
 # for a single widget

    def create_tooltip(self):
        self.tooltip = ToolTip(self.widget, **self.kwargs)

        if not self.istree: self.tooltip.bind('<Leave>', self._on_leave_tooltip)

    @property
    def cgetsub(self): return self.tooltip.cget if self.tooltip else self.tooltip

    def configure(self, **kwargs):
        try:
            self.delay = int(kwargs.pop('delay', self.delay))
        except ValueError:
            raise ValueError('expected integer for the delay option.')
        if self.tooltip: self.tooltip.configure(**kwargs)

    config = configure

    def add_tooltip(self, item, follow=False, delay=300, **kwargs):
        '''Add a tooltip with given text to the item.'''
        if not item: return

        name = str(item)
        self.tooltip_text[name] = kwargs
        self.tooltip_follows[name] = follow
        self.tooltip_delays[name] = delay or 200

        if not isinstance(item, str):
            self.bind_enter_ids[name] = item.bind('<Enter>', self._on_enter_widget)
            self.bind_leave_ids[name] = item.bind('<Leave>', self._on_leave)
            self.bind_leave_ids[name] = item.bind('<Motion>', self._on_motion_widget)

    def set_tooltip_text(self, item, follow=False, delay=100, **kwargs):
        '''Change tooltip text for given item.'''
        name = str(item)
        if name in self.tooltip_text:
            self.tooltip_text[name] = kwargs
            self.tooltip_follows[name] = follow
            self.tooltip_delays[name] = delay or 100

    def remove_tooltip(self, item):
        '''Remove widget from manager.'''
        try:
            name = str(item)
            del self.tooltip_text[name]
            if not self.istree:
                item.unbind('<Enter>', self.bind_enter_ids[name])
                item.unbind('<Leave>', self.bind_leave_ids[name])
                del self.bind_enter_ids[name]
                del self.bind_leave_ids[name]
                del self.tooltip_delays[name]
                del self.tooltip_follows[name]
        except KeyError: pass

    def remove_all(self):
        '''Remove all tooltips.'''
        self.tooltip_text.clear()
        if not self.istree:
            for name in self.tooltip_text:
                widget = self.tooltip.nametowidget(name)
                widget.unbind('<Enter>', self.bind_enter_ids[name])
                widget.unbind('<Leave>', self.bind_leave_ids[name])
            self.bind_enter_ids.clear()
            self.bind_leave_ids.clear()
            self.tooltip_follows.clear()
            self.tooltip_delays.clear()

    def _on_enter_widget(self, event):
        '''Change current widget and launch timer to display tooltip.'''
        if self.tooltip == None or not self.tooltip.winfo_ismapped():
            self.timer_id = event.widget.after(self.tooltip_delays[str(event.widget)], self.display_tooltip)
            self.current_widget = event.widget

    def _on_motion_tree(self, event):
        '''Withdraw tooltip on mouse motion and cancel its appearance.'''
        if not self.tooltip: self.create_tooltip()

        if self.tooltip.winfo_ismapped():
            x, y = self.widget.winfo_pointerxy()
            if self.widget.winfo_containing(x, y) != self.tooltip:
                if self.widget.identify_row(y - self.widget.winfo_rooty()):
                    self.tooltip.withdraw()
        else:
            try: self.widget.after_cancel(self.timer_id)
            except ValueError:
                # nothing to cancel
                pass
            self.timer_id = self.widget.after(self.delay, self.display_tooltip)

    def _on_motion_widget(self, event):
        'Tooltip will moves in a widget if the *follow==True*'

        if (self.current_widget == event.widget) and self.tooltip_follows[str(self.current_widget)] and self.tooltip: self.tooltip.position((event.x_root+20, event.y_root-10))

    def _on_leave(self, event):
        '''Hide tooltip if visible or cancel tooltip display.'''

        if self.istree:
            try: self.widget.after_cancel(self.timer_id)
            except ValueError:
                # nothing to cancel
                pass
        else:
            if self.tooltip == None: return

            if self.tooltip.winfo_ismapped():
                x, y = event.widget.winfo_pointerxy()
                if not event.widget.winfo_containing(x, y) in [event.widget, self.tooltip]:
                    self.tooltip.withdraw()
            else:
                try:
                    event.widget.after_cancel(self.timer_id)
                except ValueError:
                    pass
            self.current_widget = None

    def _on_leave_tooltip(self, event):
        '''Hide tooltip.'''
        if self.tooltip == None: return
        x, y = event.widget.winfo_pointerxy()
        if not event.widget.winfo_containing(x, y) in [self.current_widget, self.tooltip]: self.tooltip.withdraw()

    def display_tooltip(self):
        'Display tooltip'

        if self.current_widget is None:
            return

        if not self.tooltip: self.create_tooltip()

        disabled = False
        try: disabled = 'disabled' == self.current_widget['state']
        except AttributeError:
            try: disabled = self.current_widget.cget('state') == 'disabled'
            except: pass

        if self.istree:
            item = self.widget.identify_row(self.widget.winfo_pointery() - self.widget.winfo_rooty())
            x = self.widget.winfo_pointerx() + 14
            bbox = self.widget.bbox(item)
            if len(bbox) < 4:
                # it signifies that the mouse/pointer just moved outside the inside of the treeview widget
                return
            y = self.widget.winfo_rooty() + bbox[1] + bbox[3] - 14
            item = item if item in self.tooltip_text else ''

        else:
            item = str(self.current_widget)
            x = self.current_widget.winfo_pointerx() + 14
            y = self.current_widget.winfo_rooty() + self.current_widget.winfo_height() + 2
            item = item if item in self.tooltip_text else ''

        # print(disabled, '<>', item, '<>')
        if item and not disabled:
            kwargs = self.tooltip_text.get(item, {})
            self.tooltip.configure(**kwargs)
            self.tooltip.deiconify()
            self.tooltip.position((x, y))

ToolTipsManager = PRMP_ToolTipsManager

#   scrollable widgets

class PRMP_ListBox(PRMP_Frame):

    def __getattr__(self, attr):
        ret = self.getFromSelf(attr, self._unget)
        if ret != self._unget: return ret
        else: return getattr(self.listbox, attr)

    def __init__(self, master=None, listboxConfig={}, callback=None, **kwargs):
        super().__init__(master=master, **kwargs)

        self.listbox = PRMP_Listbox(self, callback=callback, **listboxConfig)

        self.clear = self.listbox.clear
        self.set = self.listbox.set
        self.clicked = self.listbox.clicked

        self.xscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="horizontal", command=self.listbox.xview))
        self.yscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="vertical", command=self.listbox.yview))
        self.listbox.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)

        self.xscrollbar.pack(side="bottom", fill="x")
        self.listbox.pack(side='left', fill='both', expand=1)
        self.yscrollbar.pack(side="right", fill="y")

        bound_to_mousewheel(0, self)

    @property
    def selected(self): return self.listbox.selected or []

ListBox = PLB = PRMP_ListBox

class PRMP_TreeView(PRMP_Frame):
    __shows = ['tree', 'headings']
    __slots__ = ['tree']

    # def __getattr__(self, attr):
        # ret = self.getFromSelf(attr, self._unget)
        # if ret != self._unget: return ret
        # else: return getattr(self.treeview, attr)

    def __init__(self, master=None, columns=[], treeviewKwargs={}, **kwargs):
        super().__init__(master=master, **kwargs)

        self.treeview = None
        self.treeviewKwargs = treeviewKwargs
        self.xscrollbar = None
        self.yscrollbar = None
        self.obj = None
        self.firstItem = None

        self.columns = Columns(columns)
        self.setColumns(columns)

    def bindings(self): pass

    def create(self):
        if self.treeview:
            self.treeview.destroy()
            del self.treeview

            self.xscrollbar.destroy()
            del self.xscrollbar

            self.yscrollbar.destroy()
            del self.yscrollbar

        self.t = self.tree = self.treeview = PRMP_Treeview(self, **self.treeviewKwargs)
        self.xscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="horizontal", command=self.treeview.xview))
        self.yscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="vertical", command=self.treeview.yview))
        self.treeview.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)

        self.xscrollbar.pack(side="bottom", fill="x")
        self.treeview.pack(side='left', fill='both', expand=1)
        self.yscrollbar.pack(side="right", fill="y")
        bound_to_mousewheel(0, self)

        self.attributes = []

        self.selected = self.treeview.selected
        self.clear = self.treeview.clear
        self.ivd = self.treeview.ivd
        self.insert = self.treeview.insert
        self.heading = self.treeview.heading
        self.column = self.treeview.column

        self.bindings()

    def tag_config(self, tagName, font=PRMP_Theme.DEFAULT_FONT, **kwargs):
        font = Font(**font)
        # return self.tree.tag_configure(tagName, font=font, **kwargs)
        return self.tree.tag_configure(tagName, **kwargs)

    def treeviewConfig(self, **kwargs): self.treeview.configure(**kwargs)

    tvc = Config = treeviewConfig

    def setColumns(self, columns=[]):
        self.create()

        if isinstance(columns, Columns): self.columns = columns

        else: self.columns.process(columns)

        if len(self.columns) > 1: self.tvc(columns=self.columns[1:])
        self.updateHeading()

    def updateHeading(self):
        for column in self.columns:
            self.heading(column.index, text=column.text, anchor='center')
            self.column(column.index, width=column.width, stretch=1,  anchor="center")#, minwidth=80)
        self.reload()

    def _set(self, obj=None, parent='', subs='subs', op=1):
        name, *columns = self.columns.getFromObj(obj)
        tag = 'prmp'

        # the fourth value of this [text, attr, width, value] can be used in sorting, it wont insert the region and its columns both into self.tree and self.ivd if not equal to value

        item = self.insert(parent, text=name, values=columns, tag=tag, open=op, value=obj)
        self.tag_config(tag)

        if self.firstItem == None:
            self.firstItem = item
            self.treeview.focus(self.firstItem)

        _subs = obj.getFromSelf(subs) if not isinstance(obj, self.containers) else obj
        if _subs:
            for sub in _subs: self._set(obj=sub, parent=item, subs=subs, op=op)

    def set(self, obj, op=1):
        if not obj: return

        self.setColumns()
        self.clear()
        if obj:
            self.obj = obj
            self._set(obj, op=op)

    def reload(self): self.set(self.obj)

TreeView = PTV = PRMP_TreeView

class PRMP_SText(PRMP_Frame):

    def __init__(self, master=None, columns=[], **kwargs):
        super().__init__(master=master, **kwargs)

        self.text = PRMP_Text(self)
        self.xscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="horizontal", command=self.text.xview))
        self.yscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="vertical", command=self.text.yview))
        self.text.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)

        self.xscrollbar.pack(side="bottom", fill="x")
        self.text.pack(side='left', fill='both', expand=1)
        self.yscrollbar.pack(side="right", fill="y")
        bound_to_mousewheel(0, self)
SText = PSTx = PRMP_SText

class PRMP_DropDownWidget:
    WidgetClass = None

    def __init__(self, master=None, ddwc=None, dropdown_windowclass=None, ddwk={}, dropdown_windowkwargs={}, attr='', valueType=str, validatecmd=None, **kwargs):
        """
        Create an entry with a drop-down widget
        """

        self.dropdown_window = None

        self.attr = attr # will be used to get the attr of the return value from the dropdown_windowclass
        self.valueType = valueType # a function to be used to convert the attr of the desired value to be viewed in this widget

        self._determine_downarrow_name_after_id = ''

        # dropdown_window
        dropdown_windowclass = ddwc or dropdown_windowclass
        dropdown_windowkwargs = ddwk or dropdown_windowkwargs
        self.geo = dropdown_windowkwargs.get('geo')

        self.WidgetClass.__init__(self, master, **kwargs)

        if issubclass(dropdown_windowclass, (PRMP_Window, PRMP_MainWindow)): dropdown_windowkwargs.update(dict(tooltype=1, normTk=1))
        self.dropdown_window = dropdown_windowclass(self, callback=self.set, **dropdown_windowkwargs) if dropdown_windowclass else Toplevel(self, **dropdown_windowkwargs)
        self.dropdown_window.withdraw()

        # add validation to Entry so that only desired input format are accepted

        self.validate_cmd = validatecmd
        if validatecmd:
            validatecmd = self.register(validatecmd)
            self.configure(validate='focusout', validatecommand=validatecmd)

        # self._downarrow_name = ''

        # --- bindings
        # determine new downarrow button bbox
        self.bind('<Configure>', self._determine_downarrow_name, '+')
        self.bind('<Map>', self._determine_downarrow_name, '+')

        # handle appearance to make the entry behave like a Combobox but with a drop-down widget instead of a drop-down list
        self.bind('<Leave>', lambda e: self.state(['!active']))
        self.bind('<ButtonPress-1>', self._on_b1_press, '+')
        self.bind('<Down>', self.drop_down, '+')
        # update entry content when date is selected in the Calendar
        # hide dropdown_window if it looses focus
        self.dropdown_window.bind('<FocusOut>', self._on_focus_out_dropdown_window, '+')
        self.dropdown_window.bind('<Up>', self._on_focus_out_dropdown_window, '+')

    def _determine_downarrow_name(self, event=None):
        """Determine downarrow button name."""
        try:
            self.after_cancel(self._determine_downarrow_name_after_id)
        except ValueError:
            # nothing to cancel
            pass
        if self.winfo_ismapped():
            self.update_idletasks()
            y = self.winfo_height() // 2
            x = self.winfo_width() - 10
            try: name = self.identify(x, y)
            except: name = 'no_name'
            if name: self._downarrow_name = name
            else:
                self._determine_downarrow_name_after_id = self.after(10, self._determine_downarrow_name)

    def _on_b1_press(self, event=None):
        """Trigger self.drop_down on widget press and set widget state to ['pressed', 'active']."""

        if str(self['state']) != 'disabled':
            self['state'] = 'pressed'
            self.drop_down()

    def _on_focus_out_dropdown_window(self, event):
        """Withdraw drop-down window when it looses focus."""
        if self.focus_get() is not None:
            if self.focus_get() == self:
                x, y = event.x, event.y
                if (type(x) != int or type(y) != int or self.identify(x, y) != self._downarrow_name):
                    self.dropdown_window.withdraw()
                    self.state(['!pressed'])
            else:
                self.dropdown_window.withdraw()
                self.state(['!pressed'])
        elif self.grab_current():
            # 'active' won't be in state because of the grab
            x, y = self.dropdown_window.winfo_pointerxy()
            xc = self.dropdown_window.winfo_rootx()
            yc = self.dropdown_window.winfo_rooty()
            w = self.dropdown_window.winfo_width()
            h = self.dropdown_window.winfo_height()
            if xc <= x <= xc + w and yc <= y <= yc + h:
                # re-focus dropdown_window so that <FocusOut> will be triggered next time
                self.dropdown_window.focus_force()
            else:
                self.dropdown_window.withdraw()
                self.state(['!pressed'])
        else:
            if 'active' in self.state():
                # re-focus dropdown_window so that <FocusOut> will be triggered next time
                self.dropdown_window.focus_force()
            else:
                self.dropdown_window.withdraw()
                self.state(['!pressed'])

    def set(self, value):
        """Insert text in the entry."""
        self.value = value
        if 'readonly' in self.state():
            readonly = True
            self.state(('!readonly',))
        else: readonly = False

        value = self.getValue(value)
        self.WidgetClass.set(self, value)
        if readonly: self.state(('readonly',))

    def getValue(self, value):
        if self.attr: value = getattr(value, self.attr, None)
        if self.valueType: value = self.valueType(value)
        return value

    def destroy(self):
        try: self.after_cancel(self._determine_downarrow_name_after_id)
        except ValueError: pass
        self.WidgetClass.destroy(self)

    def drop_down(self, event=None):
        """Display or withdraw the drop_down window depending on its current state."""

        if self.dropdown_window.winfo_ismapped(): self.dropdown_window.withdraw()
        else:
            if self.validate_cmd: self.validate_cmd()
            x = self.winfo_rootx()
            h = self.winfo_height()
            y = self.winfo_rooty()
            py = y + h

            if self.geo: self.dropdown_window.size((*self.geo, x, py))
            get = self.get()

            if get: self.dropdown_window.set(get)

            self.dropdown_window.focus_set()
            self.dropdown_window.deiconify()

    def configure(self, cnf={}, **kw):
        """
        Configure resources of a widget.

        The values for resources are specified as keyword
        arguments. To get an overview about
        the allowed keyword arguments call the method :meth:`~PRMP_DropDownEntry.keys`.
        """
        if not isinstance(cnf, dict):
            raise TypeError("Expected a dictionary or keyword arguments.")

        dropdown_windowkwargs = kw.pop('ddwk', {}) or kw.pop('dropdown_windowkwargs', {})
        self.WidgetClass.configure(self, **kw)

        if self.dropdown_window: self.dropdown_window.configure(**dropdown_windowkwargs)

    def config(self, *args, **kwargs): return self.configure(*args, **kwargs)

    def get(self):
        try: get_ = self.dropdown_window.validate_cmd(self.value)
        except: get_ = None

        if get_: self.value = get_
        return self.value
DDW = PRMP_DropDownWidget

class PRMP_DropDownEntry(PRMP_DropDownWidget, SEntry):

    entry_kw = {'cursor': 'xterm', 'style': 'dropdownEntry.TCombobox'}
    WidgetClass = SEntry

    def __init__(self, master=None, **kwargs):

        # sort keywords between entry options and calendar options
        entry_kw = {}

        style = kwargs.pop('style', self.entry_kw['style'])

        for key in self.entry_kw: entry_kw[key] = kwargs.pop(key, self.entry_kw[key])

        entry_kw['font'] = kwargs.get('font', None)
        self._cursor = entry_kw['cursor']

        entry_kw.update(kwargs.pop('config', {}))

        super().__init__(master, config=entry_kw, **kwargs)
        self.bind('<Motion>', self._on_motion, '+')

    def _on_b1_press(self, event):
        """Trigger self.drop_down on downarrow button press and set widget state to ['pressed', 'active']."""
        x, y = event.x, event.y
        if self.identify(x, y) == self._downarrow_name: super()._on_b1_press()

    def _on_motion(self, event):
        """Set widget state depending on mouse position to mimic Combobox behavior."""
        x, y = event.x, event.y
        if 'disabled' not in self.state():
            if self.identify(x, y) == self._downarrow_name:
                self.state(['active'])
                ttk.Entry.configure(self, cursor='arrow')
            else:
                self.state(['!active'])
                ttk.Entry.configure(self, cursor=self._cursor)

    def state(self, args=''):
        """
        Modify or inquire widget state.

        Widget state is returned if statespec is None, otherwise it is
        set according to the statespec flags and then a new state spec
        is returned indicating which flags were changed. statespec is
        expected to be a sequence.
        """
        # change cursor depending on state to mimic Combobox behavior
        if 'disabled' in args or 'readonly' in args: self.configure(cursor='arrow')
        elif '!disabled' in args or '!readonly' in args: self.configure(cursor='xterm')
        return super().state(args)

    def configure(self, cnf={}, **kw):
        kwargs = cnf.copy()
        kwargs.update(kw)

        entry_kw = {}
        keys = list(kwargs.keys())
        for key in keys:
            if key in self.entry_kw: entry_kw[key] = kwargs.pop(key)
        font = kwargs.get('font', None)

        if font is not None: entry_kw['font'] = font

        self._cursor = str(entry_kw.get('cursor', self._cursor))
        if entry_kw.get('state') == 'readonly' and self._cursor == 'xterm' and 'cursor' not in entry_kw:
            entry_kw['cursor'] = 'arrow'
            self._cursor  = 'arrow'

        self.WidgetClass.configure(self, entry_kw)
        super().configure(cnf=cnf, **kwargs)
DDE = DropDownEntry = PRMP_DropDownEntry

class PRMP_DropDownButton(PRMP_DropDownWidget, Button): WidgetClass = Button
DDB = DropDownButton = PRMP_DropDownButton

class PRMP_DropDownCheckbutton(PRMP_DropDownWidget, Checkbutton):
    WidgetClass = Checkbutton

    def getValue(self, val):
        val = super().getValue(val)
        self.configure(text=val)
        return val
DDCb = DropDownCheckbutton = PRMP_DropDownCheckbutton



# extensions.py
picTypes = ['Pictures {.jpg .png .jpeg .gif .xbm}']

class AutoScroll:
    '''Configure the scrollbars for a widget.'''

    def __init__(self, master):
        try:
            self.vsb = tk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        self.hsb = tk.Scrollbar(master, orient='horizontal', command=self.xview)

        try:
            self.configure(yscrollcommand=self._autoscroll(self.vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(self.hsb))

        self.grid(column=0, row=0, sticky='nsew')
        try:
            self.vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        self.hsb.grid(column=0, row=1, sticky='ew')

        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)

        methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        # if py2
        # methods = Pack.__dict__.keys() + Grid.__dict__.keys() + Place.__dict__.keys()

        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)
AS = AutoScroll

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

class PRMP_ImageWidget:
    def __init__(self, prmpImage=None, thumb=None, resize=None, normal=False, **imageKwargs):
        if not _PIL_: print('PIL is not available for this program!')
        self.rt = None
        self.prmpImage = prmpImage
        self.thumb = thumb
        self.resize = resize

        self.frame_counter = 0
        self.frame = None
        self.frames = None
        self.durations = None
        self.isGif = False

        self.default_dp = PRMP_Image('profile_pix', inbuilt=True, thumb=self.thumb)

        self._normal = normal
        self.bindMenu()

        self.after(100, lambda:self.loadImage(self.prmpImage, **imageKwargs))

    def disabled(self):
        self.unBindMenu()
        super().disabled()

    def normal(self):
        self.bindMenu()
        super().normal()

    def loadImage(self, prmpImage=None, **kwargs):
        self.delMenu()
        self.isGif = False

        dif = 20
        # if not kwargs: return
        # print(kwargs)

        self.frame_counter = 0
        # self.thumb = self.resize or self.thumb
        if not (self.resize and self.thumb):
            self.thumb = self.width-dif, self.height-dif
            if self.thumb[0] < 0 and self.thumb[1] < 0:
                # self.thumb = (250, 200)
                self.after(50, lambda: self.loadImage(prmpImage, **kwargs))
                return

        try:
            if not isinstance(prmpImage, PRMP_Image): prmpImage = PRMP_Image(prmpImage, thumb=self.thumb, resize=self.resize, **kwargs)

            if isinstance(prmpImage, PRMP_Image): self.imageFile = prmpImage.imageFile
            else: raise ValueError('prmpImage must be an instance of PRMP_Image')

            self.prmpImage =  prmpImage

            if prmpImage.ext == 'xbm': self.frame = prmpImage.resizeTk(self.resize)

            self.image = self.prmpImage.image

            if self.resize: self.frame = self.prmpImage.resizeTk(self.resize)
            else: self.frame = self.prmpImage.thumbnailTk(self.thumb)

            if self.prmpImage.ext == 'gif':
                # self.frames = self.prmpImage.animatedTkFrames
                # self.durations = self.prmpImage.interframe_durations
                self.frames = []
                self.durations = []
                for frame in ImageSequence.Iterator(self.image):
                    if self.resize: frame = frame.resize(self.resize)
                    elif self.thumb: frame.thumbnail(self.thumb)
                    tkimg = PhotoImage(frame)
                    self.frames.append(tkimg)
                    self.durations.append(frame.info['duration'])
                if self.frames: self.frame = self.frames[self.frame_counter]

                self.isGif = True
                self.__renderGif()

            self.configure(image=self.frame)

        except Exception as e:
            # print(e, __file__, 'Line ', 212)
            self.loadImage(self.default_dp)

    def __renderGif(self):
        if not self.isGif: return
        if not self.frames: return
        if not self.winfo_exists(): return

        # Update Frame
        self.frame = self.frames[self.frame_counter]
        self.config(image=self.frames[self.frame_counter])

        # Loop Counter
        self.frame_counter += 1
        if self.frame_counter >= len(self.frames): self.frame_counter = 0
        self.after(self.durations[self.frame_counter], self.__renderGif)

    def removeImage(self):
        self.delMenu()
        from .dialogs import PRMP_MsgBox

        PRMP_MsgBox(self, title='Profile Picture Removal', message='Are you sure you wanna remove the picture from this profile? ', callback=self._removeImage)

    def _removeImage(self, val):
        if val: self.loadImage()

    def set(self, imageFile=None):
        if imageFile: self.loadImage(imageFile)

    def changeImage(self, e=0):
        self.delMenu()
        file = askopenfilename(filetypes=picTypes)
        if file: self.loadImage(file)

    def bindMenu(self):
        # print(self._normal)
        if self._normal: return
        self.bind('<1>', self.delMenu, '+')
        self.bind('<3>', self.showMenu, '+')
        self.bind('<Double-1>', self.camera, '+')

    def unBindMenu(self):
        self.unbind('<1>')
        self.unbind('<3>')
        self.unbind('<Double-1>')

    def get(self): return self.imageFile

    def delMenu(self, e=0):
        if self.rt:
            self.rt.destroy()
            del self.rt
            self.rt = None

    def camera(self, e=0):
        self.delMenu()
        from .dialogs import PRMP_CameraDialog

        PRMP_CameraDialog(self, title='Profile Photo', tw=1, tm=1, callback=self.set)

    def saveImage(self):
        self.delMenu()
        if self.imageFile:
            file = asksaveasfilename(filetypes=picTypes)
            if file: self.imageFile.save(file)

    def showMenu(self, e=0):
        self.delMenu()
        x, y = e.x, e.y
        x, y = e.x_root, e.y_root
        self.rt = rt = PRMP_Toplevel(self, geo=(50, 75, x, y), tm=1, asb=0, atb=0)
        PRMP_Button(rt, text='Camera', command=self.camera, overrelief='sunken', font=PRMP_Theme.DEFAULT_MENU_FONT, place=dict(relx=0, rely=0, relh=.25, relw=1))
        PRMP_Button(rt, text='Change', command=self.changeImage, overrelief='sunken', font=PRMP_Theme.DEFAULT_MENU_FONT, place=dict(relx=0, rely=.25, relh=.25, relw=1))
        PRMP_Button(rt, config=dict(text='Save', command=self.saveImage, overrelief='sunken'), font=PRMP_Theme.DEFAULT_MENU_FONT, place=dict(relx=0, rely=.5, relh=.25, relw=1))
        PRMP_Button(rt, config=dict(text='Remove', command=self.removeImage, overrelief='sunken'), font=PRMP_Theme.DEFAULT_MENU_FONT, place=dict(relx=0, rely=.75, relh=.25, relw=1))
        rt.paint()

IW = PRMP_ImageWidget

class PRMP_ImageLabel(PRMP_ImageWidget, PRMP_Style_Label):
    def __init__(self, master, prmpImage=None, resize=(), thumb=(), imageKwargs={},  normal=0, config={}, **kwargs):
        PRMP_Style_Label.__init__(self, master, config=dict(anchor='center', **config), **kwargs)
        PRMP_ImageWidget.__init__(self, prmpImage=prmpImage, thumb=thumb, resize=resize, normal=normal, **imageKwargs)
IL = PRMP_ImageLabel

# class PRMP_SImageLabel(PRMP_ImageWidget, PRMP_Label):
#     def __init__(self, master, prmpImage=None, resize=(), thumb=(), imageKwargs={}, normal=0, config={}, callback=None, **kwargs):
#         PRMP_Label.__init__(self, master, config=dict(anchor='center', **config), **kwargs)
#         PRMP_ImageWidget.__init__(self, prmpImage=prmpImage, thumb=thumb, resize=resize, normal=normal, callback=callback, **imageKwargs)
# SIL = PRMP_ImageLabel

class PRMP_ImageButton(PRMP_ImageWidget, PRMP_Button):
    def __init__(self, master, prmpImage=None, resize=(), thumb=(), config={}, imageKwargs={},  normal=0, **kwargs):
        PRMP_Button.__init__(self, master, config=dict(anchor='center', **config), **kwargs)
        PRMP_ImageWidget.__init__(self, prmpImage=prmpImage, thumb=thumb, resize=resize,  normal=normal, **imageKwargs)
IL = PRMP_ImageButton

class PRMP_DateWidget:
    attr = 'date'
    def __init__(self, min_=None, max_=None, callback=None):
        self.callback = callback
        self.date = None
        from .dialogs import PRMP_CalendarDialog, PRMP_DateTime
        self.CD = PRMP_CalendarDialog
        self.DT = PRMP_DateTime
        self.min = min_
        self.max = max_

    def verify(self):
        if self.DT.checkDateTime(self.date, 1): return True
        else: return False

    def action(self): self.CD(self, side=self.topest.side, _return=1, min_=self.min, max_=self.max, callback=self.set)

    def get(self):
        if self.date: return self.date
        text = self['text']
        if text: return PRMP_DateTime.getDMYFromString(text)

    def set(self, date):
        if date == '':
            self.config(text=date)
            return
        if isinstance(date, str):
            try:
                if '-' in date: d, m, y = date.split('-')
                elif '/' in date: d, m, y = date.split('/')
                else: return
                self.date = self.DT.createDateTime(int(y), int(m), int(d))
            except: return
        elif isinstance(date, self.DT): self.date = date
        self.show()

    def show(self):
        if self.date: self.config(text=self.date.getFromSelf(self.attr))
        if self.callback: self.callback(self.date)

class PRMP_DateButton(PRMP_DateWidget, PRMP_Button):
    def __init__(self, master=None, font=PRMP_Theme.DEFAULT_FONT, asEntry=True, placeholder='', min_=None, max_=None, callback=None, anchor='w', **kwargs):

        PRMP_Button.__init__(self, master=master, config=dict(command=self.action, anchor=anchor), font=font, asEntry=asEntry,  **kwargs)

        PRMP_DateWidget.__init__(self, min_=min_, max_=max_, callback=callback)
        self['text'] = placeholder

PDB = PRMP_DateButton

class PRMP_MonthButton(PRMP_DateButton): attr = 'monthName'
PMoB = PRMP_MonthButton

class PRMP_MonthYearButton(PRMP_DateButton): attr = 'monthYear'

class ScrollableFrame(PRMP_Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.canvas = canvas = PRMP_Canvas(self, config=dict(bg='blue'))
        canvas.place(x=0, rely=0, relh=.96, relw=.99)

        # self.canvas.grid_rowconfigure(0, weight=1)

        xscrollbar = PRMP_Scrollbar(self, config=dict(orient="horizontal", command=canvas.xview))
        yscrollbar = PRMP_Scrollbar(self, config=dict(orient="vertical", command=canvas.yview))
        canvas.configure(xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
        xscrollbar.pack(side="bottom", fill="x")

        yscrollbar.pack(side="right", fill="y")

        bound_to_mousewheel(0, self)

        self.scrollable_frame = PRMP_Frame(canvas)
        self.scrollable_frame.pack(side='left', fill='both', expand=1)

        self.scrollable_frame.bind("<Configure>", self.changeFrameBox)

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')

    def changeFrameBox(self, e=0):
        p = self.canvas.bbox("all")
        self.canvas.configure(scrollregion=p)
SF = ScrollableFrame


class PRMP_SolidScreen(PRMP_MainWindow):
    def __init__(self, side='top-center', gaw=1, bd=12, geo=(),**kwargs):
        super().__init__(tm=1, gaw=gaw, geo=geo or (500, 500), side=side, **kwargs)

        self.container.configure(borderwidth=12)

        self.paint()
SS = PRMP_SolidScreen

class ScrolledText(AutoScroll, tk.Text):

    @create_container
    def __init__(self, master, **kw):
        tk.Text.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class ScrolledEntry(AutoScroll, tk.Entry):

    @create_container
    def __init__(self, master, **kw):
        tk.Entry.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)

class PRMP_FramedCanvas(Frame):
    def __init__(self, master, canvasConfig={}, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = Canvas(self, **canvasConfig, place=dict(relx=.005, rely=.005, relh=.99, relw=.99))

class PRMP_DateTimeView(LabelFrame):

    def __init__(self, master, text='Date and Time', **kwargs):
        super().__init__(master, config=dict(text=text), **kwargs)
        self.time = Label(self)
        self.time.place(relx=.005, rely=0, relh=.98, relw=.37)

        self.date = Label(self)
        self.date.place(relx=.39, rely=0, relh=.98, relw=.6)

        self.update()

    def update(self):
        now = PRMP_DateTime.now()
        day = now.day
        dayN = now.dayName
        month = now.monthName
        year = now.year

        date = f'{dayN} {day}, {month} {year}'
        self.date['text'] = date

        hour = str(now.hour % 12).zfill(2)
        minute = str(now.minute).zfill(2)
        second = str(now.second).zfill(2)
        m = now.strftime('%p')

        time = f'{hour} : {minute} : {second} {m}'
        self.time['text'] = time

        self.after(10, self.update)

class PRMP_Calendar(Frame):

    choosen = None
    _version_ = '3.3.0' # Alpha by PRMPSmart

    background=PRMP_Theme.DEFAULT_BACKGROUND_COLOR
    header_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0]
    header_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1]
    month_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1]
    month_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0]
    year_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1]
    year_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0]

    surf_fg=PRMP_Theme.DEFAULT_BUTTON_COLOR[0]
    surf_bg=PRMP_Theme.DEFAULT_BUTTON_COLOR[1]


    class DayLabel(PRMP_Label):
        highlight_bg = PRMP_Theme.DEFAULT_BACKGROUND_COLOR
        highlight_fg = PRMP_Theme.DEFAULT_FOREGROUND_COLOR
        now_fg = 'white'
        now_bg = 'green'
        now_highlight_fg = 'green'
        now_highlight_bg = 'white'
        empty_bg = PRMP_Theme.DEFAULT_BUTTON_COLOR[0]
        choosen_fg = 'white'
        choosen_bg = 'black'
        days_fg = PRMP_Theme.DEFAULT_BACKGROUND_COLOR
        days_bg = PRMP_Theme.DEFAULT_FOREGROUND_COLOR
        notPart = False # for buttons not part of the days button
        count = 0

        def __init__(self, master=None, returnMethod=None, **kw):
            super().__init__(master=master, background=self.days_bg, foreground=self.days_fg, font=PRMP_Theme.DEFAULT_FONT, **kw)
            self.day = None
            self.returnMethod = returnMethod

            # name='DAY'+str(PRMP_Calendar.DayLabel.count)
            # PRMP_Calendar.DayLabel.count += 1

            self.bind('<Enter>', self.onButton, '+')
            self.bind('<Leave>', self.offButton, '+')
            self.bind('<ButtonPress-1>', self.choosen, '+')

        def onButton(self, e=0):
            self.statusShow()
            if self.notPart: return
            if self.day:
                if self.now: self.config(background=self.class_.now_highlight_bg, foreground=self.class_.now_highlight_fg)
                else: self.config(background=PRMP_Theme.DEFAULT_BACKGROUND_COLOR, foreground=PRMP_Theme.DEFAULT_FOREGROUND_COLOR)

        @property
        def status(self):
            if self.day: return self.day.date

        def offButton(self, e=0):
            if self.notPart: return

            if self == PRMP_Calendar.choosen: self.config(background=self.class_.choosen_bg, foreground=self.class_.choosen_fg)
            elif self.now: self.config(background=self.class_.now_bg, foreground=self.class_.now_fg)
            else:
                if self.day: self.config(background=PRMP_Theme.DEFAULT_FOREGROUND_COLOR, foreground='red' if self.redDay else PRMP_Theme.DEFAULT_BACKGROUND_COLOR)
                else: self.config(background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])

        paint = offButton

        def config(self, day=None, command=None, notPart=False, **kwargs):
            self.notPart = notPart
            if day: self.changeDay(day)
            if command:
                self.unbind('<ButtonPress-1>')
                self.bind('<ButtonPress-1>', command, '+')

            background, foreground = kwargs.get('background'), kwargs.get('foreground')
            self.configure(**kwargs)
            # print(kwargs)

            if foreground: self['foreground'] = foreground
            if background: self['background'] = background

        @property
        def now(self):
            day = self.day
            nw = PRMP_DateTime.now()
            if self.day: return day.date == nw.date
            return day == nw

        def changeDay(self, day):
            now = PRMP_DateTime.now()
            if day == now: self.config(background=self.class_.now_bg, foreground=self.class_.now_fg)
            self.day = day
            self.redDay = day.dayName in ['Saturday', 'Sunday']
            self.config(text=self.day.dayNum, state='normal', relief='groove')
            self.offButton()

        def empty(self):
            self.day = None
            self.config(text='', state='disabled', relief='flat', background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])

        def clicked(self, e=0):
            b4 = PRMP_Calendar.choosen
            PRMP_Calendar.choosen = self

            if b4: b4.offButton()

            self.config(background=self.class_.choosen_bg, foreground=self.class_.choosen_fg)

        def choosen(self, e=0):
            if self.day:
                if self.notPart: return
                self.clicked()
                self.returnMethod(self.day)

    def __init__(self, master=None, month=None, callback=None, min_=None, max_=None, **kwargs):
        super().__init__(master, **kwargs)
        month = kwargs.pop('date', month)

        month = PRMP_DateTime.checkDateTime(month, dontRaise=1)
        if not month: month = PRMP_DateTime.now()

        self.min = PRMP_DateTime.getDMYFromString(min_)
        self.max = PRMP_DateTime.getDMYFromString(max_)
        self.__date = None
        self.month = month
        self.callback = callback

        self.daysButtons = []

        self._back = PRMP_Button(self, text=self._backward, command=self.previousYear, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], font=PRMP_Theme.DEFAULT_MINUTE_FONT)
        self._back.place(relx=0, rely=0, relw=.12, relh=.1)

        self._prev = PRMP_Button(self, text=self._previous, command=self.previousMonth, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])
        self._prev.place(relx=.12, rely=0, relw=.12, relh=.1)

        self.monthNameLbl = PRMP_Label(self, text=self.month.monthName, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])
        self.monthNameLbl.place(relx=.24, rely=0, relw=.36, relh=.1)

        self.yearLbl = PRMP_Label(self, text=self.month.year, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])
        self.yearLbl.place(relx=.6, rely=0, relw=.16, relh=.1)

        self._nxt = PRMP_Button(self, text=self._next, command=self.nextMonth, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0])
        self._nxt.place(relx=.76, rely=0, relw=.12, relh=.1)

        self._for = PRMP_Button(self, text=self._forward, command=self.nextYear, background=PRMP_Theme.DEFAULT_BUTTON_COLOR[1], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], font=PRMP_Theme.DEFAULT_MINUTE_FONT)
        self._for.place(relx=.88, rely=0, relw=.12, relh=.1)

        col = 0
        self.headers = []
        daysAbbrs = [PRMP_DateTime.daysAbbr[-1]] + PRMP_DateTime.daysAbbr[:-1]
        w = 1/7
        for dayAbbr in daysAbbrs:
            x = col * w
            d = PRMP_Label(self, text=dayAbbr, relief='groove', background=self.header_bg, foreground=self.header_fg)
            d.place(relx=x, rely=.1, relw=w, relh=.15)
            self.headers.append(d)
            col += 1

        h = .75 / 6
        y = .25
        for d in range(42):
            m = d % 7
            x = m * w
            if (d != 0) and (m == 0): y += h
            btn = self.DayLabel(self, returnMethod=self.choosenDay, text=d, relief='groove')
            btn.place(relx=x, rely=y, relw=w, relh=h)
            self.daysButtons.append(btn)

        self.reset = self.daysButtons[-4]
        self.reset.config(command=self.resetDate, text='☂', background='red', foreground='white', notPart=1, relief='ridge')

        self.updateDays()

    def afterPaint(self):
        dic = dict(background=PRMP_Theme.DEFAULT_BUTTON_COLOR[0], foreground=PRMP_Theme.DEFAULT_BUTTON_COLOR[1])

        background = PRMP_Theme.DEFAULT_BUTTON_COLOR[1]
        foreground = PRMP_Theme.DEFAULT_BUTTON_COLOR[0]

        for btn in [self._back, self._for, self._prev, self._nxt, *self.headers]: btn.config(background=background, foreground=foreground)

        self.monthNameLbl.config(**dic)
        self.yearLbl.config(**dic)

    def resetDate(self, e=0):
        self.month = PRMP_DateTime.now()
        self.updateDays()

    def nextYear(self):
        new = self.month + 12
        if self.max and (new.ymdToOrd > self.max.ymdToOrd): return
        self.month = new
        self.updateDays()

    def nextMonth(self, e=0):
        new = self.month + 1
        if self.max and (new.ymdToOrd > self.max.ymdToOrd): return
        self.month = new
        self.updateDays()

    def previousYear(self):
        new = self.month - 12
        if self.min and (new.ymdToOrd < self.min.ymdToOrd): return
        self.month = new
        self.updateDays()

    def previousMonth(self):
        new = self.month - 1
        if self.min and (new.ymdToOrd < self.min.ymdToOrd): return
        self.month = new
        self.updateDays()

    def updateDays(self):

        self.monthNameLbl.config(text=self.month.monthName)
        self.yearLbl.config(text=self.month.year)
        monthDates = self.month.monthDates
        totalDays = len(monthDates)

        remainingBtns = self.daysButtons[totalDays:]
        for day in monthDates:
            index = monthDates.index(day)
            DayLabel = self.daysButtons[index]
            if DayLabel == self.reset: continue

            if self.month.isSameMonthYear(day):
                DayLabel.config(day=day)
                if self.month.isSameDate(day): DayLabel.clicked()
            else: DayLabel.empty()

        for btn in remainingBtns:
            if btn == self.reset: continue
            btn.empty()

    @property
    def date(self): return self.__date

    def choosenDay(self, date):
        self.__date = date
        if self.callback: self.callback(date)

class PRMP_Entry_Label(Label):

    def __init__(self, master, font='DEFAULT_FONT', **kwargs): super().__init__(master, asEntry=True, font=font, **kwargs)
Entry_Label = PRMP_Entry_Label

class PRMP_Camera(PRMP_Style_Frame):

    def __init__(self, master, source=0, frameUpdateRate=10, callback=None, **kwargs):
        import cv2
        self.cv2 = cv2
        self.cam = None
        self.source = source
        self.image = None
        self._image = None
        self._set = None
        self.callback = callback
        self.pause = False
        self.opened = False

        self.frameUpdateRate = frameUpdateRate

        super().__init__(master, **kwargs)

        self.screen = Label(self, place=dict(relx=.006, rely=.01, relh=.85, relw=.985))
        self.screen.bind('<Double-1>', self.screenPause, '+')

        self.save = Button(self, config=dict(text='Save', command=self.saveImage))
        self.bind('<Map>', self.checkVisibility)
        self.bind('<Unmap>', self.checkVisibility)
        self.bind('<Return>', self.saveImage)

    def y(self): return

    def placeSave(self): self.save.place(relx=.375, rely=.87, relh=.1, relw=.25)

    def screenPause(self, e=0):
        if self.pause or self._set:
            self.pause = False
            self.openCam()
            self._set = None
            self.save.place_forget()
        else:
            self.pause = True
            self.closeCam()
            self.placeSave()

    def saveImage(self):
        self.imageFile = PRMP_ImageFile(image=self._image)
        if self.callback: return self.callback(self.imageFile)

    @staticmethod
    def _saveImage(image):
        file = asksaveasfilename(filetypes=picTypes)

        if file: image.save(file)

    def get(self): return self.saveImage()

    def openCam(self):
        if self._set: return
        self.cam = self.cv2.VideoCapture(self.source)
        self.updateScreen()
        self.opened = True

    def closeCam(self):
        if self.cam and self.cam.isOpened():
            self.cam.release()
            self.opened = False

    def snapshot(self):
        # Get a frame from the video source
        success, frame = self.getFrame()
        # if frame: self.cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", self.cv2.cvtColor(frame, self.cv2.COLOR_RGB2BGR))

    def _updateScreen(self, image=None):
        self.image = PhotoImage(image=image) if image else self.image
        self.screen.config(image=self.image)

    def updateScreen(self):
        if self.image: self._updateScreen()
        # if self.image: self.screen['image'] = self.image
        del self.image
        self.image = None
        self.setImage()
        if not self.pause: self.after(self.frameUpdateRate, self.updateScreen)

    def checkVisibility(self, event):
        if event.type == tk.EventType.Map:
            if not self.pause:
                self.after(100, self.openCam)
                pass
        elif event.type == tk.EventType.Unmap: self.closeCam()

    def setImage(self, image=None):
        self._set = image
        success, frame = self.getFrame()
        if success or self._set:
            dif = 20
            w_h = self.width-dif, self.height-dif
            if w_h[0] < 0 and w_h[1] < 0: return

            self._image = PRMP_Image(self._set) if self._set else Image.fromarray(frame)

            image = self._image.copy()
            image.thumbnail(w_h)

            self._updateScreen(image)

    def getFrame(self):
        if self.cam and self.cam.isOpened():
            success, frame = self.cam.read()
            if success: return (success, self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB))
            else: return (success, None)
        else: return (False, None)

    def __del__(self): self.closeCam()

class Hierachy(PRMP_TreeView):

    def __init__(self, master=None, columns=[], toggleOpen=True, binds=[], **kwargs):
        self._toggleOpen = False
        self.toop = toggleOpen
        self.last = []
        self.binds = binds
        super().__init__(master=master, columns=columns, **kwargs)

        self.bindings()

    @property
    def openDialog(self):
        from .dialogs import dialogFunc
        return dialogFunc

    def toggleOpen(self, e=0):
        if self._toggleOpen: self._toggleOpen = False
        else: self._toggleOpen = True

        if self.last: self.viewObjs(*self.last)

    def bindings(self):
        self.treeview.bind('<Control-Return>', self.viewSelected, '+')
        if self.toop:
            self.treeview.bind('<Control-o>', self.toggleOpen, '+')
            self.treeview.bind('<Control-O>', self.toggleOpen, '+')

        self.treeview.bind('<Control-r>', self.reload, '+')
        self.treeview.bind('<Control-R>', self.reload, '+')

        for event, func, sign in self.binds: self.treeview.bind(event, func, sign)

    def reload(self, e=0):
        if self.last: self.viewObjs(*self.last)

    def viewSelected(self, e=0):
        current = self.selected()
        if current: self.openDialog(master=self, obj=current)

    def getSubs(self, obj, item=''):
        return obj.subs


    def _viewObjs(self, obj, parent=''):
        if not obj: return

        if isinstance(obj, list):
            subs = obj
            item = parent
        else:
            raw = self.columns.getFromObj(obj)
            first, *columns = raw
            # print(raw)

            item = self.insert(parent, text=first, values=columns, open=self._toggleOpen, value=obj)

            subs = self.getSubs(obj, item)

        if isinstance(subs, list):
            for sub in subs:
                # print(subs)
                if sub: self._viewObjs(sub, item)

    def viewObjs(self, obj, parent=''):
        if not parent: self.clear()
        self._viewObjs(obj, parent)
        self.last = obj, parent

    def viewSubs(self, obj): self.viewObjs(obj[:])
H = Hierachy

class AttributesViewer(LabelFrame):

    def __init__(self, master, attr='', obj=None, dialog=None, **kwargs):
        super().__init__(master, **kwargs)
        from .two_widgets import LabelLabel, LabelEntry, LabelText, TwoWidgets

        self.dialog = dialog
        if not self.dialog:
            from .dialogs import dialogFunc
            self.dialog = dialogFunc

        self.obj = obj
        self.attr = attr

        self._value = self.obj[self.attr]
        self._type = type(self._value)

        self.name = LabelEntry(self, place=dict(relx=0, rely=0, relh=.15, relw=1), topKwargs=dict(text='attr Name'), bottomKwargs=dict(state='readonly'), orient='h', longent=.3)

        self.name.set(self.attr)

        self.value = LabelText(self, place=dict(relx=0, rely=.15, relh=.45, relw=1), topKwargs=dict(text='attr Value'), bottomKwargs=dict(state='disabled'), orient='h', longent=.3)

        self.value.set(self._value)

        self.valueType = LabelEntry(self, place=dict(relx=0, rely=.6, relh=.15, relw=1), topKwargs=dict(text='value Type'), bottomKwargs=dict(state='readonly'), orient='h', longent=.23)

        self.valueType.set(self._type)

        self.mastertype = TwoWidgets(self, place=dict(relx=0, rely=.76, relh=.14, relw=1), topKwargs=dict(text='master Type', command=self.openMaster), bottomKwargs=dict(state='readonly'), orient='h', longent=.22, top=Button, bottom='entry')

        self.mastertype.set(type(self.obj))

        self.details = Button(self, text='Further Details', place=dict(relx=0, rely=.9, relh=.1, relw=1), command=self.open)

    def openMaster(self): self.dialog(obj=self.obj)

    def open(self):
        if isinstance(self._value, (int, str, list, tuple, dict)): AttributesExplorer(values=self._value, dialog=self.dialog, grab=0)
        else: self.dialog(obj=self._value, grab=0, tm=1)

class AttributesExplorer(LabelFrame):
    def __init__(self, master, listboxConfig={}, callback=None, obj=None, values={}, dialog=None, **kwargs):
        super().__init__(master, **kwargs)
        from .two_widgets import LabelLabel, LabelEntry, LabelText, TwoWidgets

        self.dialog = dialog
        self.callback = callback
        self.obj = obj

        frame1 = Frame(self, place=dict(relx=0, rely=0, relw=.44, relh=1))

        Label(frame1, text='Top Attrs', place=dict(relx=0, rely=0, relw=1, relh=.07))

        self.listbox = ListBox(frame1, place=dict(relx=0, rely=.08, relh=.84, relw=1), listboxConfig=dict(config=dict(selectmode='multiple'), values=values), bindings=[('<Return>', self.clicked, '')])

        self.total = LabelLabel(frame1, place=dict(relx=0, rely=.93, relh=.07, relw=.6), orient='h', bottomKwargs=dict(font='DEFAULT_FONT'), longent=.4, topKwargs=dict(text='Total'))

        Button(frame1, text='Open', place=dict(relx=.65, rely=.93, relh=.07, relw=.25), command=self.openAttribute)

        PRMP_Separator(self, place=dict(relx=.445, rely=0, relh=1, relw=.05), config=dict(orient='vertical'))

        frame2 = Frame(self, place=dict(relx=.455, rely=0, relw=.545, relh=1))

        self.treeview = PRMP_Treeview(frame2, place=dict(relx=0, rely=0, relh=.8, relw=1))
        self.treeview.heading('#0', text='Attributes')
        self.ivd = self.treeview.ivd
        self.treeview.bind('<Delete>', self.deleteAttribute, '+')

        self.entry = LabelEntry(frame2, place=dict(relx=0, rely=.81, relw=.65, relh=.085), orient='h', longent=.25, topKwargs=dict(text='New'), bottomKwwargs=dict(placeholder=''))
        self.entry.B.bind('<Return>', self.addAtrribute, '+')

        self.top = Checkbutton(frame2, text='Top?', place=dict(relx=.7, rely=.815, relh=.07, relw=.25))

        Button(frame2, text='Delete', place=dict(relx=.1, rely=.915, relh=.07, relw=.25), command=self.deleteAttribute)
        Button(frame2, text='Get', place=dict(relx=.65, rely=.915, relh=.07, relw=.25), command=self.getAttributes)

        self._foc = None

        if obj and not values:
            keys = list(obj.__dict__.keys())
            values = [key.strip('_') for key in keys if '__' not in key]
            values.sort()

        self.values = values
        self.set(values)

    def openAttribute(self):
        from .dialogs import PRMP_MsgBox, AttributesViewerDialog

        if not self.obj: PRMP_MsgBox(self, title='Object Error', message='No object is given!')

        attrs = self.getAttributes()
        if attrs:
            leng = len(attrs)

            if not leng: PRMP_MsgBox(self, title='Attribute Error', message='Choose an attribute from the listbox!')
            elif leng > 1: PRMP_MsgBox(self, title='Attribute Error', message='Choose only one attribute from the listbox!')
            else:
                attr = attrs[0]
                # value = self.obj[attr]
                # openCores(obj=value)
                AttributesViewerDialog(attr=attr, obj=self.obj, dialog=self.dialog, tm=0, grab=0)

    def addAtrribute(self, e=0):
        get = self.entry.get()
        if not get: return
        item = '' if self.top.get() else self.treeview.focus()
        self.treeview.insert(item, text=get)
        # self.treeview.focus('')
        self.setListBox()
        self.entry.B.clear()

    def deleteAttribute(self, e=0):
        self._foc = focus = self.treeview.focus()

        _all = 'all attributes' if not focus else f'this attribute --> {self.ivd[focus]}'

        from .dialogs import PRMP_MsgBox

        PRMP_MsgBox(self, title='Delete Attribute', message=f'Are you sure to delete {_all}', ask=1, callback=self._delete)

    def _delete(self, w):
        if w:
            if not self._foc: self.treeview.deleteAll()
            else: self.treeview.delete(self._foc)
        self.setListBox()

    def setListBox(self):
        self.listbox.clear()
        tops = self.treeview.get_children()
        for top in tops: self.listbox.insert(self.ivd[top])
        self.total.set(self.listbox.last)

    def clicked(self, event=None, selected=None):
        selected = self.listbox.selected
        self.treeview.see

    def set(self, values):
        if not values: return
        self.values = values
        self.setTreeview(values)
        self.setListBox()

    def getAttributes(self):
        tops = self.treeview.getChildren()
        listbox = self.listbox.curselection()
        if not listbox: listbox = range(self.listbox.last)
        result = [tops[num] for num in listbox] if isinstance(tops, (tuple, list)) else [tops]

        if self.callback: self.callback(result)
        else: return result


    def setTreeview(self, values, parent=''):
        if isinstance(values, list):
            for value in values: self.setTreeview(value, parent)

        elif isinstance(values, dict):
            for key, value in values.items():
                item = self.treeview.insert(parent, text=key)
                self.setTreeview(value, item)

        elif isinstance(values, (str, bytes)):
            self.treeview.insert(parent, text=values)
            pass

class ColumnViewer(LabelFrame):

    def __init__(self, master, column=None, **kwargs):
        super().__init__(master, **kwargs)
        from .two_widgets import LabelEntry

        self.text = LabelEntry(self, place=dict(relx=0, rely=0, relh=.2, relw=1), topKwargs=dict(text='text'), orient='h', longent=.3)

        self.attr = LabelEntry(self, place=dict(relx=0, rely=.2, relh=.2, relw=1), topKwargs=dict(text='attr'), orient='h', longent=.3)

        self.value = LabelEntry(self, place=dict(relx=0, rely=.4, relh=.2, relw=1), topKwargs=dict(text='value'), orient='h', longent=.3)

        self._width = LabelEntry(self, place=dict(relx=0, rely=.6, relh=.2, relw=1), topKwargs=dict(text='width'), orient='h', longent=.3)

        if column:
            self.text.set(column.text)
            self.attr.set(column.attr)
            self.value.set(column.value)
            self._width.set(column.width)

    def openMaster(self):
        from .dialogs import dialogFunc
        dialogFunc(master=self, obj=self.obj)

    def open(self):
        from .dialogs import dialogFunc, ColumnsExplorerDialog
        if isinstance(self._value, (int, str, list, tuple, dict)): ColumnsExplorerDialog(self, values=self._value)
        else: dialogFunc(master=self, obj=self._value)

class ColumnsExplorer(PRMP_FillWidgets, LabelFrame):
    def __init__(self, master, listboxConfig={}, callback=None, columns=None, masterWid=None, **kwargs):

        LabelFrame.__init__(self, master, **kwargs)
        PRMP_FillWidgets.__init__(self)
        from .two_widgets import LabelLabel, LabelEntry

        self.callback = callback
        self.columns = columns
        self.masterWid = masterWid

        _cols = ['text', 'attr', 'width', 'value']

        frame1 = Frame(self, place=dict(relx=0, rely=0, relw=.3, relh=1))

        Label(frame1, text='Columns', place=dict(relx=0, rely=0, relw=1, relh=.07))

        self.listbox = ListBox(frame1, place=dict(relx=0, rely=.08, relh=.84, relw=1), listboxConfig=dict(config=dict(selectmode='multiple')), bindings=[('<Return>', self.clicked, '')])

        self.total = LabelLabel(frame1, place=dict(relx=0, rely=.93, relh=.07, relw=.6), orient='h', bottomKwargs=dict(font='DEFAULT_FONT'), longent=.4, topKwargs=dict(text='Total'))

        PRMP_Separator(self, place=dict(relx=.305, rely=0, relh=1, relw=.05), config=dict(orient='vertical'))

        frame2 = Frame(self, place=dict(relx=.315, rely=0, relw=.685, relh=1))

        self.treeview = Hierachy(frame2, place=dict(relx=0, rely=0, relh=.7, relw=1), columns=_cols)
        self.treeview.treeview.bind('<Delete>', self.deleteColumn, '+')

        self.text = LabelEntry(frame2, place=dict(relx=.0, rely=.71, relw=.5, relh=.085), orient='h', longent=.23, topKwargs=dict(text='text'), bottomKwargs=dict(_type='text', required=True))
        self.attr = Button(frame2, place=dict(relx=.55, rely=.71, relw=.1, relh=.085), text='attr', command=self.getAttr)
        self._width = LabelEntry(frame2, place=dict(relx=0, rely=.8, relw=.3, relh=.085), orient='h', topKwargs=dict(text='width'), bottomKwargs=dict(_type='number'))
        self.value = LabelEntry(frame2, place=dict(relx=.35, rely=.8, relw=.3, relh=.085), orient='h', longent=.4,  topKwargs=dict(text='value'), bottomKwargs=dict(_type='text'))

        Button(frame2, text='Get', place=dict(relx=.8, rely=.75, relh=.15, relw=.15), command=self.getColumns)

        Button(frame2, text='Delete', place=dict(relx=.1, rely=.915, relh=.07, relw=.25), command=self.deleteColumn)
        Button(frame2, text='Add', place=dict(relx=.45, rely=.915, relh=.07, relw=.25), command=self.addColumn)

        self._foc = None
        self._focObj = None
        self._attr = ''

        self.set(columns)
        self._cols = _cols

        self.addResultsWidgets(_cols)

    def width(self): return self._width

    def addColumn(self, e=0):
        gets = self.get(['text', '_width', 'value'])
        gets['attr'] = self._attr
        width = gets['_width'] or 20
        gets['width'] = int(width)
        try: j = self.columns.addColumn(gets)
        except:
            from .dialogs import PRMP_MsgBox
            PRMP_MsgBox(self, title='Error', _type='error', message='Try to add the "attr" value.')
        self._attr = ''

        self.set(self.columns)

    def getAttr(self):
        from .dialogs import AttributesExplorerDialog
        AttributesExplorerDialog(callback=self.setAttr)

    def setAttr(self, attr):
        if attr: self._attr = attr[0]

    def deleteColumn(self, e=0):
        from .dialogs import PRMP_MsgBox

        self._foc = focus = self.treeview.treeview.focus()
        if not focus: PRMP_MsgBox(self, title='No Selection.n', message='Pick a row to delete.')

        self._focObj = self.treeview.treeview.ivd[focus]

        _all = 'all Columns' if not focus else f'this Column --> {self._focObj.index}'

        PRMP_MsgBox(self, title='Delete Column', message=f'Are you sure to delete {_all}', ask=1, callback=self._delete)

    def _delete(self, w):
        if w:
            if not self._foc: return
            else:
                self.treeview.treeview.delete(self._foc)
                # self.columns.remove(self._focObj)
                self.updateCol()

        self.setListBox()


    def setListBox(self):
        self.listbox.clear()
        tops = self.columns

        if tops:
            for top in tops:
                text = top.text
                self.listbox.insert(text)
            last = self.listbox.last
        else: last = 0

        self.total.set(last)

    def clicked(self, event=None, selected=None):
        selected = self.listbox.selected
        self.treeview.see

    def set(self, columns):
        if not columns: return

        self.columns = columns if isinstance(columns, Columns) else Columns(columns)

        self.treeview.treeview.deleteAll()
        self.treeview.viewSubs(self.columns)

        self.setListBox()

    def updateCol(self, listbox=[]):
        tops = self.treeview.treeview.getChildren()
        listbox = listbox or range(len(tops))

        result = [tops[num] for num in listbox] if isinstance(tops, (tuple, list)) else [tops]

        results = [dict(text=res.text, attr=res.attr, width=res.width, value=res.value) for res in result]

        self.columns.process(results)



    def getColumns(self, e=0):
        listbox = self.listbox.curselection()
        self.updateCol(listbox)

        if self.callback: self.callback(self.columns, e)



    # def setTreeview(self, values, parent=''):
    #     if isinstance(values, list):
    #         for value in values: self.setTreeview(value, parent)

    #     elif isinstance(values, dict):
    #         for key, value in values.items():
    #             item = self.treeview.insert(parent, text=key)
    #             self.setTreeview(value, item)

    #     elif isinstance(values, (str, bytes)):
    #         self.treeview.insert(parent, text=values, value=values)
    #         pass

class PRMP_DropDownCalendarWidget(PRMP_DropDownWidget):
    def __init__(self, *args, **kwargs):
        from .dialogs import PRMP_CalendarDialog

        super().__init__(*args, ddwc=PRMP_CalendarDialog, ddwk=dict(gaw=0, geo=(300, 250)), **kwargs)


class PRMP_DropDownCalendarEntry(PRMP_DropDownEntry):
    def __init__(self, *args, **kwargs):
        from .dialogs import PRMP_CalendarDialog

        super().__init__(*args, ddwc=PRMP_CalendarDialog, ddwk=dict(gaw=0, geo=(300, 250)), **kwargs)


# two_widgets.py

class TwoWidgets(PRMP_Frame):
    top_widgets = {'label': PRMP_Label, 'checkbutton': PRMP_Checkbutton, 'radiobutton': PRMP_Radiobutton}
    stop_widgets = {'label': PRMP_Style_Label, 'checkbutton': PRMP_Style_Checkbutton, 'radiobutton': PRMP_Style_Radiobutton}
    bottom_widgets = {'label': PRMP_Label, 'datebutton': PRMP_DateButton, 'entry': PRMP_Entry, 'text': PRMP_Text, 'stext': PRMP_SText, 'combobox': PRMP_Combobox, 'spinbox': PRMP_Spinbox, 'button': PRMP_Button, 'monthbutton': PRMP_MonthButton, 'monthyearbutton': PRMP_MonthYearButton}
    sbottom_widgets = {'label': PRMP_Style_Label, 'datebutton': PRMP_DateButton, 'entry': PRMP_Style_Entry, 'text': PRMP_Text, 'stext': PRMP_SText, 'combobox': PRMP_Combobox, 'spinbox': PRMP_Style_Spinbox, 'button': PRMP_Button, 'dropdownentry': PRMP_DropDownEntry}
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

        self.val, self.var = self.value, self.variable = self.T.val, self.T.var

        self.rt = None

        if self.value and self.variable: self.checked()

        self.place_widgs()

    def clicked(self, e=0): return self.B.get()

    @property
    def value(self): return self.Top.value
    @property
    def variable(self): return self.Top.variable
    @value.setter
    def value(self, v): return
    @variable.setter
    def variable(self, v): return

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






# plot_canvas.py

import random


class PlotDatas:
    def __init__(self, xticks=[], ys=[], labels=[], xlabel='', ylabel='', plot=0):
        self.xticks = xticks
        self.ys = ys
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.labels = labels
        self._x_axis(plot)

    def float_it(self, num):
        re = float('%.2f' % num)
        return re

    def _x_axis(self, plot=0):
        try:
            assert len(self.labels) == len(self.ys), f'Length of "labels-> {len(self.labels)}" must be equal to the length of "ys-> {len(self.ys)}"'

            assert len(self.xticks) == len(self.ys[0]), f'Length of "xticks-> {len(self.xticks)}" must be equal to the length of "ys[0]-> {len(self.ys[0])}"'

            self.x_points = len(self.ys[0])
            self.d_1_point = len(self.ys)
            self.width = self.float_it(1. / (self.d_1_point + 1))
            self.space = self.float_it(1. / (self.d_1_point))

        except Exception as e:
            # print(e)
            self.x_points = len(self.ys)
            self.d_1_point = 1
            self.width = .6
            self.space = self.width

        finally:
            self.ranges = range(self.x_points)
            self.d_ranges = range(self.d_1_point)
            self._plot_points()

    def _plot_points(self):
        point = 0
        self.plot_points = []
        try:
            assert len(self.xticks) == len(self.ys[0]), f'Length of "xticks-> {len(self.xticks)}" must be equal to the length of "ys[0]-> {len(self.ys[0])}"'

            for _ in self.ys:
                e_tick_points = [self.float_it(p + point) for p in range(self.x_points)]
                self.plot_points.append(e_tick_points)
                point += self.width
        except: self.plot_points = self.ranges

    def switch(self):
        if self.d_1_point != 1:
            self.xticks, self.labels = self.labels, self.xticks
            self.xlabel, self.ylabel = self.ylabel, self.xlabel


            rly = range(len(self.ys[0]))
            _ys = []

            for yn in rly:
                y = []
                for _y in self.ys:
                    x = _y[yn]
                    y.append(x)
                _ys.append(y)

            self.ys = _ys
            self._x_axis()

            return 1
        else: print('d_1_point=1', __file__)

Bar = PlotDatas

class Plots(PRMP_Mixins):
    bkcol = 'white'
    def __init__(self, bkcol=''):
        self.big = 1

        from matplotlib import pyplot

        self.figure = pyplot.figure(facecolor=bkcol or self.bkcol)
        self.subplot = self.figure.add_subplot(self.big,1,1)

        self._pie = None
        self._grid = None

        self.chart = 'plot'
        self.annotation = {}

    def annotate(self, xlabel='', ylabel='', title='', xticks=0, yticks=0, set_xticks=0, set_yticks=0, axisrotate=(0, 0), lblrotate=(0, 90)):

        if xlabel: self.subplot.set_xlabel(xlabel, rotation=lblrotate[0])
        if ylabel: self.subplot.set_ylabel(ylabel, rotation=lblrotate[1])

        if set_xticks: self.subplot.set_xticks(set_xticks)
        if set_yticks: self.subplot.set_yticks(set_yticks)

        if xticks: self.subplot.set_xticklabels(xticks)
        if xticks: self.subplot.set_xticklabels(xticks, rotation=axisrotate[0])

        if yticks: self.subplot.set_yticklabels(yticks, rotation=axisrotate[1])

        if title: self.subplot.set_title(title)
        if self.chart != 'pie': self.subplot.set_title(title)

    def genAnnot(self, xlabel='', ylabel='', title='', xticks=0, yticks=0, set_xticks=0, set_yticks=0, axisrotate=(0, 0), lblrotate=(0, 90)): return dict(xlabel=xlabel, ylabel=ylabel, title=title, xticks=xticks, yticks=yticks, set_xticks=set_xticks, set_yticks=set_yticks, axisrotate=axisrotate, lblrotate=lblrotate)

    def doAnnotation(self):
        if self.annotation: self.annotate(**self.genAnnot(**self.annotation))

    def doPlotting(self, chart='plot', grid=None, adjust={}, draw=True, autoAdjust=False, **kwargs):
        self.clear()
        self.chart = chart.lower()

        func = self.getFromSelf(self.chart)
        # print()
        if self.chart == 'pie': kwargs = {k: v for k, v in kwargs.items() if k in ['ys', 'labels', 'explode', 'shadow', 'title']}
        func(**kwargs)
        # func(self, **kwargs)

        self.doAnnotation()
        self.legend()
        self.set_grid(grid)

        if autoAdjust:
            adjust = {}
            self.adjust()
        elif adjust: self.adjust(**adjust)

        if draw: self.draw()

    def adjust(self, left=.2, bottom=.5, right=.94, top=.88, wspace=.2, hspace=0): self.figure.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

    def draw(self): self.figure.canvas.draw()

    def legend(self):
        self.subplot.legend()
        # return
        # try: self.subplot.legend()
        # except Exception as e: print(e)

    def set_grid(self, grid):
        if not grid: return
        self._grid = grid
        lw, ls, c = grid['lw'], grid['ls'], grid['c']
        self.subplot.grid(lw=lw, ls=ls, c=c)

    def clear(self):
        self.subplot.cla()
        self.draw()
        self.chart_datas = {}

    def plot(self, xticks=[], ys=[], labels=[], markers=[], lss=[], linestyle=[], lw=0, linewidth=0, alpha=0, switch=0):
        if linestyle: lss = linestyle
        if linewidth: lw = linewidth
        if not lw: lw = 2
        if not alpha:  alpha = 1

        plotDatas = PlotDatas(xticks=xticks, ys=ys, labels=labels, xlabel=self.chart_datas.get('xlabel', ''), ylabel=self.chart_datas.get('ylabel', ''), plot=1)

        if switch: plotDatas.switch()

        self.annotation.update(dict(xticks=plotDatas.xticks, xlabel=plotDatas.xlabel, ylabel=plotDatas.ylabel))

        try:
            indexes = range(len(plotDatas.labels))
            for index in indexes:
                y = plotDatas.ys[index]
                label = plotDatas.labels[index]

                if markers:
                    marker = markers[index]
                    markersize = 10
                else:
                    marker = None
                    markersize = None
                if lss: ls = lss[index]
                else: ls = None

                self.subplot.plot(plotDatas.xticks, y, label=label, marker=marker, ls=ls, lw=lw, markersize=markersize, alpha=alpha)

        except Exception as e:
            # print(e, 'error first')
            if markers:
                markers = markers[0]
                markersize = 10
            else:
                markers = None
                markersize = None

            if lss: lss = lss[0]
            else: lss = None

            try: self.subplot.plot(plotDatas.xticks, plotDatas.ys, label=plotDatas.labels, marker=markers, ls=lss, lw=lw, markersize=markersize, alpha=alpha)
            except Exception as e:
                # print(e)
                pass

    def bar(self, xticks=[], ys=[], labels=[], xlabel='', title='', switch='', ylabel='', axisrotate=(20, 0)):

        barObj = PlotDatas(xticks=xticks, ys=ys, labels=labels, xlabel=xlabel, ylabel=ylabel)
        if switch: barObj.switch()

        self.annotation = dict(xlabel=barObj.xlabel, axisrotate=axisrotate, title=title, ylabel=barObj.ylabel)
        if self.chart == 'bar':
            bar_h = self.subplot.bar
            self.annotation.update(dict(set_xticks=barObj.ranges, xticks=barObj.xticks))
        else:
            bar_h = self.subplot.barh
            self.annotation.update(dict(set_yticks=barObj.ranges, yticks=barObj.xticks))

        if barObj.d_1_point != 1:
            for ind in barObj.d_ranges:
                x = barObj.plot_points[ind]
                y = barObj.ys[ind]
                label = barObj.labels[ind]

                bar_h(x, y, barObj.width,  label=label)

        else: bar_h(barObj.plot_points, barObj.ys, label=barObj.labels)

    barh = bar

    def hist(self, *args): pass

    def pie(self,  ys=[], labels=[], explode=[], shadow=None, title=''):
        self.annotation = dict(title=title)

        if not self.pie: return

        self._pie(ys, labels=labels, explode=explode, autopct='%1.1f%%', shadow=shadow, labeldistance=1.1)
        self.adjust(left=0, bottom=.4, right=1, top=.88, wspace=.2, hspace=0)


class Render(Plots):
    def __init__(self, bkcol='white', annotation={}):
        super().__init__(bkcol)
        self.figure.canvas.set_window_title('Goodness and Mercy')
        self._pie = pyplot.pie
        self.annotation = annotation

    def draw(self): self.figure.show()

    def pie(self,  **kwargs):
        super().pie(**kwargs)
        self.adjust(left=0, bottom=.1, right=1, top=.88, wspace=.2, hspace=0)


class PRMP_PlotCanvas(Plots, PRMP_Frame):
    charts = ['plot', 'bar', 'barh', 'hist', 'pie']
    lss = ['dashed', 'dashdot', 'solid', 'dotted']

    def __init__(self, master=None, relief='solid', **kwargs):
        PRMP_Frame.__init__(self, master, relief=relief, **kwargs)
        Plots.__init__(self)

        self.expand = False

        self.chart_datas = {}
        self._pie = self.subplot.pie

        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        self.canvas = FigureCanvasTkAgg(self.figure, master=self).get_tk_widget()
        self.canvas.bind('<1>', self.show)

        self.canvas.place(relx=-.05, rely=-.03, relh=1.7, relw=1.05)

        self.adjust()

    def ls_choser(self, num=1):
        ls = []
        while len(ls) <= num:
            l = random.choice(self.lss)
            ls.append(l)
        if num == 1: return ls[0]
        else: return ls

    def marker_choser(self, num):
        markers = {'point':'.', 'circle':'o', 'triangle_down ':'v', 'triangle_up':'^', 'triangle_left':'<', 'triangle_right':'>', 'octagon':'8', 'square':'s', 'pentagon':'p', 'plus': 'P', 'star' :'*', 'hexagon1':'h', 'hexagon2':'H', 'cancel':'X', 'diamond':'D', 'thin_diamond':'d', 'underscore':'_'}
        markers = list(markers.values())
        markers_give = []
        while len(markers_give) <= num:
            mark = random.choice(markers)
            if mark in markers_give: pass
            else: markers_give.append(mark)
        return markers_give

    def doPlotting(self, expand=False, inApp=1, adjust={}, **kwargs):
        pie = kwargs.get('pie', False)
        draw = True

        if pie:
            if not adjust: adjust = dict(left=0, bottom=.3, right=1, top=.88, wspace=.2, hspace=0)
            if not inApp: draw = False

        dic = dict(draw=draw, **kwargs)

        if adjust: dic['adjust'] = adjust

        super().doPlotting(**dic)
        if expand: self.show()

    def plot(self, xticks=[], labels=[], xlabel='', ylabel='', title='', marker=None, lss=None, annot={}, axisrotate=(20, 0), **kwargs):

        if marker: markers = self.marker_choser(len(labels))
        else: markers = None

        if lss: lss = self.ls_choser(len(labels))

        self.annotation = dict(xticks=xticks, axisrotate=axisrotate, xlabel=xlabel, title=title, ylabel=ylabel, **annot)

        self.chart_datas = dict(xticks=xticks, labels=labels, markers=markers, lss=lss, **kwargs)

        super().plot(**self.chart_datas)

    def bar(self, **kwargs):
        self.chart_datas = kwargs
        super().bar(**self.chart_datas)

    def pie(self, labels=[], explode=None, **kwargs):

        if explode: explode = [.1 for _ in labels]
        else: explode = [0 for _ in labels]

        self.chart_datas = dict(explode=explode, labels=labels, **kwargs)
        super().pie(**self.chart_datas)

    def set_grid(self, grid): super().set_grid(grid)

    def show(self, o=0): Render(bkcol=self.bkcol, annotation=self.annotation).doPlotting(chart=self.chart, grid=self._grid, **self.chart_datas)






# dialogs.py

import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
from tkinter.simpledialog import askstring, askfloat, askinteger


class PRMP_Dialog(PRMP_MainWindow, PRMP_FillWidgets):

    def __init__(self, master=None, _return=True, values={}, ntb=1, nrz=0, tm=1, gaw=1, tw=1, editable=True, callback=None, show=1, grab=1, bell=False, delay=0, tt=False, tooltype=False, wait=False, **kwargs):

        self.tooltype = tt or tooltype
        if self.tooltype: grab = 0

        PRMP_MainWindow.__init__(self, master, ntb=ntb, nrz=nrz, tm=tm, gaw=gaw, tw=tw, grab=grab, tooltype=self.tooltype, **kwargs)

        PRMP_FillWidgets.__init__(self, values=values)

        self.__result = None
        self.callback = callback
        self._return = _return

        self.submitBtn = None
        self.editBtn = None

        self._setupDialog()
        self.set()

        if editable:
            if values: self.editInput(0)
            else: self.editInput(1)

        self.defaults()

        self.paint()
        if bell: self.bell()

        self.focus()
        if delay: self.after(delay, self.destroy)

        # if self.tooltype: self.withdraw()
        if 2: pass
        elif wait: self.wait_window()
        elif show: self.mainloop()


    def _setupDialog(self):
        'This is to be overrided in subclasses of PRMPDialog to setup the widgets into the dialog.'

    def defaults(self):
        # self.grab_set()
        # self.wait_window()
        pass

    @property
    def result(self): return self.__result

    def _setResult(self, result): self.__result = result

    def addSubmitButton(self):
        self.submitBtn = PRMP_Button(self.container, config=dict(text='Submit', command=self.processInput))

    def bindCR(self): self.bind('<Control-Return>', self.processInput)
    def unbindCR(self): self.unbind('<Control-Return>')

    def _placeSubmitButton(self):
        x, y = self.containerGeo
        self.submitBtn.place(x=(x/2)-30 , y=y-40, h=30, w=60)

    def placeSubmitBtn(self, wh=0):
        if wh:
            self.bindCR()
            self.container.paint()
            geo = self.kwargs.get('geo')
            self._placeSubmitButton()
        else:
            self.unbindCR()
            self.submitBtn.place_forget()

    def addEditButton(self):
        if self.submitBtn == None: self.addSubmitButton()
        x, y = self.containerGeo
        self.editBtn = PRMP_Style_Checkbutton(self.container, config=dict(text='Edit', command=self.editInput))
        self.editBtn.place(x=10 , y=y-40, h=30, w=60)

    def processInput(self, e=0):
        result = self.get()
        # result = {'address': 'lklk', 'email': 'awa.@asd.asa', 'gender': 'Male', 'name': 'Aderemi Goodness', 'phone': '2121', 'regDate': PRMP_DateTime(2020, 12, 30, 0, 54, 19)}
        if result:
            self._setResult(result)
            self.action()
            self.save()

        else: PRMP_MsgBox(self, title='No Input Error', message='No input whatsoever is given.', _type='error', ask=0)

    def action(self): print('redefine this method for functionality')

    def save(self): print('redefine this method for functionality')

    def editInput(self, e=0):
        if self.editBtn == None: return
        if e: self.editBtn.set('1')
        if self.editBtn.get(): self.placeSubmitBtn(1)
        else: self.placeSubmitBtn()
        for widgetName in self.resultsWidgets:
            wid = self[widgetName]
            if self.editBtn.get(): wid.normal()
            else: wid.disabled()

    def destroyDialog(self):
        if self.tooltype: self.withdraw()
        elif self._return: self.destroy()

        if self.callback: self.callback(self.result)

PD = PRMP_Dialog

class PRMP_CalendarDialog(PRMP_Dialog):

    def __init__(self, master=None, month=None, title='PRMP_Calendar Dialog', geo=(300, 300), min_=None, max_=None, date=None, **kwargs):
        self.min = min_
        self.max = max_
        self.month = date or month

        super().__init__(master, title=title, geo=geo, editable=False, **kwargs)

    def _setupDialog(self): self.calendar = self.addWidget(PRMP_Calendar, config=dict(callback=self.getDate, max_=self.max, min_=self.min, month=self.month), place=dict(relx=0, rely=0, relh=1, relw=1))

    def afterPaint(self): self.calendar.afterPaint()

    def getDate(self, date):
        self._setResult(date)
        if self._return:
            PRMP_Calendar.choosen = None
            self.destroyDialog()

    def validate_cmd(self, date): return PRMP_DateTime.getDMYFromDate(date)

    def set(self, date=None):
        date = super().getDate(date)
        if date:
            self.calendar.month = date
            self.calendar.updateDays()

CD = PRMP_CalendarDialog

class PRMP_MsgBox(PRMP_Dialog):
    _bitmaps = ['info', 'question', 'error', 'warning']
    def __init__(self, master=None, geo=(350, 160), title='Message Dialog', message='Put your message here.', _type='info', cancel=0, ask=0, okText='', msgFont='DEFAULT_FONT', plenty=0, bell=True, msg='', delay=3000, **kwargs):

        message = msg or message

        self.plenty = plenty
        self.message = message
        self.msgFont = msgFont
        self._type = _type
        self.okText = okText
        self._cancel = cancel

        if kwargs.get('callback'): ask = 1
        if okText: ask = 0

        if ask: delay = 0
        # print(ask, delay)
        self.ask = ask

        super().__init__(master, title=title, geo=geo, tm=1, asb=0, editable=False, grab=1, bell=bell, delay=delay, **kwargs)

    def _setupDialog(self):
        self.placeContainer(h=self.geo[1]-50)
        if self.plenty: self.label = PRMP_Text(self.container, state='disabled')
        else: self.label = PRMP_Label(self.container, config=dict(bitmap='', wraplength=250), font='PRMP_FONT')

        self.label.set(self.message)
        self.label.place(x=0, y=0, relh=.75, relw=.85)

        self.bitmap = PRMP_Label(self.container, config=dict(bitmap=self.getType(self._type)))
        self.bitmap.place(relx=.85, y=0, relh=1, relw=.15)

        self.yes = PRMP_Button(self, config=dict(text='Yes' if self.ask else self.okText or 'Ok', command=self.yesCom))

        if not self.ask:
            self.yes.place(relx=.3, rely=.83, relh=.15, relw=.37)
            self.bind('<Return>', lambda e: self.yes.invoke())
        else:
            self.yes.place(relx=.06, rely=.83, relh=.15, relw=.17)
            self.bind('<Y>', lambda e: self.yes.invoke())
            self.bind('<y>', lambda e: self.yes.invoke())

            self.no = PRMP_Button(self, config=dict(text='No', command=self.noCom), place=dict(relx=.63, rely=.83, relh=.15, relw=.17))
            self.bind('<N>', lambda e: self.no.invoke())
            self.bind('<n>', lambda e: self.no.invoke())

        if self._cancel:
            self.cancel = PRMP_Button(self, config=dict(text='Cancel', command=self.cancelCom))
            self.cancel.place(relx=.33, rely=.83, height=28, relw=.2)
        self.yes.focus()

    def getType(self, _type):
        if _type in self._bitmaps: return _type
        elif _type in self._xbms: return f'@{self._xbms[_type]}'

    @property
    def _xbms(self): return PRMP_Xbms.filesDict()

    def yesCom(self):
        if self.ask: self._setResult(True)
        self.destroyDialog()

    def cancelCom(self):
        self._setResult(None)
        self.destroyDialog()

    def noCom(self):
        self._setResult(False)
        self.destroyDialog()

PMB = PRMP_MsgBox

class PRMP_CameraDialog(PRMP_Dialog):

    def __init__(self, master=None, title='PRMP_Camera Dialog', cameraKwargs={}, **kwargs):
        self.cameraKwargs = cameraKwargs
        super().__init__(master, title=title, **kwargs)

    def isMaximized(self): return self.getWid_H_W(self)

    def _setupDialog(self):
        self.camera = PRMP_Camera(self.container, place=dict(relx=.01, rely=.01, relh=.98, relw=.98), callback=self.getImage, config=dict(relief='flat'), **self.cameraKwargs)
        self.set = self.camera.setImage

    def getImage(self, imageFile):
        self._setResult(imageFile)
        if not self.callback: return PRMP_Camera._saveImage(imageFile)
        self.destroyDialog()

    # def

    def __del__(self): del self.camera
CamD = PRMP_CameraDialog

class PRMP_ImageDialog(PRMP_Dialog):

    def __init__(self, master=None, image=None, title='Image Dialog', **kwargs):
        self.image = image
        # print(kwargs)
        super().__init__(master, title=title, show=0, **kwargs)

    # def isMaximized(self): return self.getWid_H_W(self)

    def _setupDialog(self):
        self.imageLabel = PRMP_ImageLabel(self.container, prmpImage=self.image, place=dict(relx=.01, rely=.01, relh=.98, relw=.98), callback=self.getImage, config=dict(relief='flat'))
        self.set = self.imageLabel.set
        # self.bind('<Return>', self.imageLabel.saveImage)

    def getImage(self, imageFile):
        self._setResult(imageFile)
        self.destroyDialog()

class Splash(PRMP_Dialog):
    def __init__(self, master=None, prmpImage='', ntb=1, atb=0, asb=0, geo=(800, 500), callback=None, title='Goodness and Mercy', imageKwargs={}, delay=2000, **kwargs):

        self.prmpImage = prmpImage
        self.delay = delay
        self.imageKwargs = imageKwargs

        super().__init__(master, atb=atb, asb=asb, ntb=ntb, geo=geo, title=title, editable=0, callback=callback, **kwargs)

    def _setupDialog(self):
        asb = self.addStatusBar
        if asb: cont = self.container
        else:
            cont = self
            self.container.place_forget()

        self.image = PRMP_ImageLabel(cont, prmpImage=self.prmpImage, place=dict(relx=0, rely=0, relw=1, relh=.9), resize=self.geo, imageKwargs=self.imageKwargs, normal=1)

        self.load = PRMP_ImageLabel(cont, prmpImage='line_boxes', place=dict(relx=0, rely=.9, relw=1, relh=.1), imageKwargs=dict(inbuilt=1, inExt='gif'), resize=(280, 50), normal=1)

        # self.after(self.delay, self.destroy)
        self.after(self.delay, self.processCallback)

    def processCallback(self):
        if self.callback: self.callback(self.destroy)
        else: self.after(10, self.processCallback)

    def set(self): pass



class ColumnViewerDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Columns Viewer Dialog', geo=(300, 300), column=None, **kwargs):
        self.column = column
        super().__init__(master, title=title, geo=geo, **kwargs)

    def _setupDialog(self):
        self._column = ColumnViewer(self.container, place=dict(relx=.02, rely=.02, relh=.96, relw=.96), column=self.column)
        self.addEditButton()

        self.text = self._column.text
        self.attr = self._column.attr
        self.value = self._column.value
        self._width = self._column._width

        self.addResultsWidgets(['text', 'attr', '_width', 'value'])
        self.set()

    def processInput(self):
        result = self.get()

        print(result)

class ColumnsExplorerDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Columns Explorer Dialog', geo=(800, 500), columns=None, **kwargs):
        self.columns = columns
        super().__init__(master, title=title, geo=geo, **kwargs)

    def _setupDialog(self):

        self.cols = ColumnsExplorer(self.container, place=dict(relx=.02, rely=.02, relh=.96, relw=.96), columns=self.columns, callback=self._callback)

        self.bind('<Return>', self.cols.getColumns)

    def _callback(self, w, e=0):
        if self.callback:
            self.callback(w)
            if not e: self.destroy()






class AttributesExplorerDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Attributes Explorer Dialog', geo=(600, 500), obj=None, dialog=None, **kwargs):
        self.obj = obj
        self.dialog = dialog
        super().__init__(master, title=title, geo=geo, **kwargs)

    def _setupDialog(self): AttributesExplorer(self.container, place=dict(relx=.02, rely=.02, relh=.96, relw=.96), values=self.values, obj=self.obj,  dialog=self.dialog, callback=self._callback)

    def _callback(self, w):
        if self.callback:
            self.callback(w)
            self.destroy()



class AttributesViewerDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Attributes Viewer Dialog', geo=(700, 300), obj=None, attr=None, dialog=None, **kwargs):
        self.attr = attr
        self.obj = obj
        self.dialog = dialog
        super().__init__(master, title=title, geo=geo, **kwargs)

    def _setupDialog(self): AttributesViewer(self.container, place=dict(relx=.02, rely=.02, relh=.96, relw=.96), attr=self.attr, obj=self.obj, dialog=self.dialog)











def showDialog(title=None, msg=None, which=None):
    if which == 'error': messagebox.showerror(title, msg)
    elif which == 'info': messagebox.showinfo('Information', msg)
    elif which == 'warn': messagebox.showwarning('Warning', msg)

def confirmDialog(title=None, msg=None, which=None):
    if which == 1: return messagebox.askyesno(title, msg)
    if which == 2: return messagebox.askquestion(title, msg)
    if which == 3: return messagebox.askokcancel(title, msg)
    if which == 4: return messagebox.askretrycancel(title, msg)
    if which == 5: return messagebox.askyesnocancel(title, msg)

def askPath(opened=False, folder=False, many=False, save=False, **kwargs):
    if folder == False:
        if opened == False:
            if many == False:
                if save == False: return filedialog.askopenfilename(**kwargs)
                else: return filedialog.asksaveasfilename(**kwargs)
            else: return filedialog.askopenfilenames(**kwargs)
        else:
            if many == False:
                if save == False: return filedialog.askopenfile(**kwargs)
                else: return filedialog.asksaveasfile(**kwargs)
            else: return filedialog.askopenfiles(**kwargs)
    else: return filedialog.askdirectory(**kwargs)

def dialogFunc(*args, ask=0, path=0, obj=None, int_=0, float_=0, string=0, **kwargs):
    if obj:
        if isinstance(obj, PRMP_DateTime): PRMP_CalendarDialog(month=obj, **kwargs)
        elif isinstance(obj, (PRMP_Image, PRMP_ImageFile)): PRMP_ImageDialog(image=obj, **kwargs)
        elif isinstance(obj, Columns): ColumnsExplorerDialog(columns=obj, **kwargs)
        elif isinstance(obj, Column): ColumnViewerDialog(column=obj, **kwargs)
    elif path: return askPath(**kwargs)
    elif ask: return confirmDialog(**kwargs)
    elif string: return askstring(*args, **kwargs)
    elif float_: return askfloat(*args, **kwargs)
    elif int_: return askinteger(*args, **kwargs)
    else: return showDialog(**kwargs)



def getPixs(folder):
    if not path.isdir(folder): raise f'{folder} is not a valid directory/folder.'

    cwd = getcwd()
    chdir(folder)
    pixs = []

    for file in listdir(folder):
        if path.isfile(file):
            if PRMP_ImageType.get(file):
                p = path.join(folder, file)
                pixs.append(p)
    chdir(cwd)
    return pixs

class PhotoViewer(PRMP_MainWindow):

    def __init__(self, title='PRMP Photo Viewer', folder='', file='', **kwargs):
        super().__init__(title=title, **kwargs)
        self._folder = folder
        self._pixs = []
        self._total = 0
        self._current = ''
        self._index = 0

        self.frame = Frame(self.container)

        self.folder = LabelButton(self.frame, place=dict(relx=.005, rely=.005, relw=.99, relh=.09), orient='h', topKwargs=dict(text='Folder'), longent=.13, bottomKwargs=dict(command=self.chooseDir))
        self.bind('<Control-O>', self.chooseDir)
        self.bind('<Control-o>', self.chooseDir)

        self.imageLabel = PRMP_ImageLabel(self.frame, place=dict(relx=.005, rely=.1, relw=.99, relh=.7), prmpImage=file)

        self.previous = Button(self.imageLabel, text=self._previous, place=dict(relx=.005, rely=.42, relw=.1, relh=.16), command=self.previousPic, relief='flat', tipKwargs=dict(text='Previous Picture'))

        self.next = Button(self.imageLabel, text=self._next, place=dict(relx=.89, rely=.42, relw=.1, relh=.16), command=self.nextPic, relief='flat', tipKwargs=dict(text='Next Picture'))

        self.total = LabelLabel(self.frame, place=dict(relx=.005, rely=.8, relw=.5, relh=.09), orient='h', topKwargs=dict(text='Total Pictures: '), longent=.55)
        self.index = LabelEntry(self.frame, place=dict(relx=.65, rely=.8, relw=.35, relh=.09), orient='h', topKwargs=dict(text='Index'), longent=.45, bottomKwargs=dict(_type='number'))
        self.index.B.bind('<Return>', self.byIndex)

        self.current = LabelEntry(self.frame, place=dict(relx=.005, rely=.9, relw=.7, relh=.09), orient='h', topKwargs=dict(text='Current: '), longent=.24, bottomKwargs=dict(state='readonly'))

        self.listBtn = Checkbutton(self.frame, place=dict(relx=.75, rely=.9, relw=.2, relh=.07), text='List?', command=self.toggleList, var=1, value=1, tipKwargs=dict(text='Toggle list of pictures in the current folder.'))

        self.listFrame = Frame(self.container)
        self.list = ListBox(self.listFrame, place=dict(relx=.005, rely=.005, relw=.99, relh=.99), callback=self.listSelection)

        self.defaults()
        self.placeFrame()
        if file:
            d = path.dirname(file)
            if d: self.chooseDir(folder=d)
            self.setCurrent(file)
            # self.current.set(file)
        self.paint()

    def defaults(self):
        self.bind('<Left>', self.previousPic)
        self.bind('<Right>', self.nextPic)
        if self._folder: self.chooseDir(folder=self._folder)
        else: self.updateDatas()

    def byIndex(self, e=0):
        index = self.index.get()
        try:
            print(index)
            index = int(index)
            assert 0 <= index <= self._total, f'Index {index} is not in range 0 ... {self._total}.'
            self._index = index
            self.setCurrent()
        except Exception as e:
            PRMP_MsgBox(self, title=e.__class__.__name__, message=e, ask=0, _type='error')
            return

    def updateDatas(self):
        self.folder.set(self._folder)
        self.total.set(self._total)
        self.index.set(self._index+1)
        self.setCurrent()

    def setCurrent(self, current_=''):
        if not current_:
            if not self._pixs: return
            self.index.set(self._index)
            self._current = self._pixs[self._index]
            if not path.exists(self._current):
                PRMP_MsgBox(self, title='Not Exist', message=f'{self._current} does not exist, try to reload the folder.', ask=0)
                return

        current = path.basename(self._current)
        self.current.set(current)
        self.imageLabel.loadImage(current_ or self._current)

    def chooseDir(self, e=0, folder=''):
        if not folder: folder = dialogFunc(path=1, folder=1, initialdir=self._folder, title='PRMP Photoviewer')

        if not folder: return

        self._folder = folder
        self._pixs = getPixs(folder)

        self._current = ''
        if self._pixs: self._current = self._pixs[0]

        self._total = len(self._pixs)
        self.updateDatas()
        self.list.set(self._pixs)

    def listSelection(self, selected, event=0):
        if selected:
            selected = selected[0]
            self._index = self._pixs.index(selected)
            self.setCurrent()

    def previousPic(self, e=0):
        if self._pixs:
            self._index -= 1
            if self._index <= 0: self._index = self._total - 1
            self.setCurrent()

    def nextPic(self, e=0):
        if self._pixs:
            self._index += 1
            if self._index >= self._total: self._index = 0
            self.setCurrent()

    def toggleList(self):
        if self.listBtn.get():
            x, y = self.geo[:2]
            self.changeGeometry((x*2, y))
            self.placeList()
            self.placeFrame(1)
        else:
            self.changeGeometry(self.geo[:2])
            self.placeFrame()
            self.listFrame.place_forget()

    def placeFrame(self, w=0):
        if w: relw = .5
        else: relw = .99
        self.frame.place(relx=.005, rely=.005, relw=relw, relh=.96)

    def placeList(self): self.listFrame.place(relx=.5, rely=.005, relw=.49, relh=.96)



