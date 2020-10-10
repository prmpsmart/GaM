from random import randint
import tkinter as tk
import tkinter.ttk as ttk

TK_WIDGETS = ['Button', 'Canvas', 'Checkbutton', 'Entry', 'Frame', 'Label', 'LabelFrame', 'Listbox', 'Menu', 'Menubutton', 'Message', 'OptionMenu', 'PanedWindow', 'Radiobutton', 'Scale', 'Scrollbar', 'Spinbox', 'TKCalendar', 'TKOutput', 'Text', 'TkFixedFrame', 'TkScrollableFrame', 'Widget']

# Excerpt from PySimpleGUI theme implementation of his theme.
class Theme:
    
    BLUES = ("#082567", "#0A37A3", "#00345B")
    PURPLES = ("#480656", "#4F2398", "#380474")
    GREENS = ("#01826B", "#40A860", "#96D2AB", "#00A949", "#003532")
    YELLOWS = ("#F3FB62", "#F0F595")
    TANS = ("#FFF9D5", "#F4EFCF", "#DDD8BA")
    NICE_BUTTON_COLORS = ((GREENS[3], TANS[0]), ('#000000', '#FFFFFF'), ('#FFFFFF', '#000000'), (YELLOWS[0], PURPLES[1]), (YELLOWS[0], GREENS[3]), (YELLOWS[0], BLUES[2]))
    COLOR_SYSTEM_DEFAULT = '1234567890'
    DEFAULT_BUTTON_COLOR = ('white', BLUES[0])
    OFFICIAL_PYSIMPLEGUI_BUTTON_COLOR = ('white', BLUES[0])
    DEFAULT_ERROR_BUTTON_COLOR = ("#FFFFFF", "#FF0000")
    DEFAULT_BACKGROUND_COLOR = None
    DEFAULT_ELEMENT_BACKGROUND_COLOR = None
    DEFAULT_ELEMENT_TEXT_COLOR = COLOR_SYSTEM_DEFAULT
    DEFAULT_TEXT_ELEMENT_BACKGROUND_COLOR = None
    DEFAULT_TEXT_COLOR = COLOR_SYSTEM_DEFAULT
    DEFAULT_INPUT_ELEMENTS_COLOR = COLOR_SYSTEM_DEFAULT
    DEFAULT_INPUT_TEXT_COLOR = COLOR_SYSTEM_DEFAULT
    DEFAULT_SCROLLBAR_COLOR = None
    DEFAULT_PROGRESS_BAR_COLOR = (GREENS[0], '#D0D0D0')
    DEFAULT_PROGRESS_BAR_COMPUTE = ('#000000', '#000000')
    DEFAULT_PROGRESS_BAR_COLOR_OFFICIAL = (GREENS[0], '#D0D0D0')
    DEFAULT_HIGHLIGHT_BG = 'white'
    DEFAULT_HIGHLIGHT_BG = '#004080'
    
    THEMES_DICTS = {
        'SystemDefault': {'BACKGROUND': COLOR_SYSTEM_DEFAULT, 'TEXT': COLOR_SYSTEM_DEFAULT, 'INPUT': COLOR_SYSTEM_DEFAULT, 'TEXT_INPUT': COLOR_SYSTEM_DEFAULT, 'SCROLL': COLOR_SYSTEM_DEFAULT, 'BUTTON': OFFICIAL_PYSIMPLEGUI_BUTTON_COLOR, 'PROGRESS': COLOR_SYSTEM_DEFAULT},
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
        
        'Default':   {'BACKGROUND': COLOR_SYSTEM_DEFAULT, 'TEXT': COLOR_SYSTEM_DEFAULT, 'INPUT': COLOR_SYSTEM_DEFAULT, 'TEXT_INPUT': COLOR_SYSTEM_DEFAULT, 'SCROLL': COLOR_SYSTEM_DEFAULT, 'BUTTON': OFFICIAL_PYSIMPLEGUI_BUTTON_COLOR, 'PROGRESS': COLOR_SYSTEM_DEFAULT},
        'Default1':  {'BACKGROUND': COLOR_SYSTEM_DEFAULT, 'TEXT': COLOR_SYSTEM_DEFAULT, 'INPUT': COLOR_SYSTEM_DEFAULT, 'TEXT_INPUT': COLOR_SYSTEM_DEFAULT, 'SCROLL': COLOR_SYSTEM_DEFAULT, 'BUTTON': COLOR_SYSTEM_DEFAULT, 'PROGRESS': COLOR_SYSTEM_DEFAULT},
        'DefaultNoMoreNagging':  {'BACKGROUND': COLOR_SYSTEM_DEFAULT, 'TEXT': COLOR_SYSTEM_DEFAULT, 'INPUT': COLOR_SYSTEM_DEFAULT, 'TEXT_INPUT': COLOR_SYSTEM_DEFAULT, 'SCROLL': COLOR_SYSTEM_DEFAULT, 'BUTTON': OFFICIAL_PYSIMPLEGUI_BUTTON_COLOR, 'PROGRESS': COLOR_SYSTEM_DEFAULT},
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
    
    CURRENT_THEME = 'Dark Blue 3'
    
    
    @classmethod
    def setTheme(cls, theme, force=False):
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
        else: ix = randint(0, len(lf_values) - 1); print('** Warning - {} Theme is not a valid theme. Change your theme call. **'.format(theme))
        
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
                    text_element_background_color=colors['BACKGROUND'],
                    element_background_color=colors['BACKGROUND'],
                    text_color=colors['TEXT'],
                    input_elements_background_color=colors['INPUT'],
                    button_color=colors['BUTTON'],
                    progress_meter_color=colors['PROGRESS'],
                    scrollbar_color=(colors['SCROLL']),
                    element_text_color=colors['TEXT'],
                    input_text_color=colors['TEXT_INPUT'])
            return cls.CURRENT_THEME
        except Exception as er:
            print(f'Error: {er} ')
            print(f'** Warning - Theme value not valid. Change your theme ({theme}) call. **')
    
    @classmethod
    def setOptions(cls, button_color=None, progress_meter_color=None, background_color=None, element_background_color=None, text_element_background_color=None, input_elements_background_color=None, input_text_color=None, scrollbar_color=None, text_color=None, element_text_color=None, error_button_color=(None, None)):

        if button_color != None: cls.DEFAULT_BUTTON_COLOR = button_color

        if progress_meter_color != None: cls.DEFAULT_PROGRESS_BAR_COLOR = progress_meter_color

        if background_color != None: cls.DEFAULT_BACKGROUND_COLOR = background_color

        if text_element_background_color != None: cls.DEFAULT_TEXT_ELEMENT_BACKGROUND_COLOR = text_element_background_color

        if input_elements_background_color != None: cls.DEFAULT_INPUT_ELEMENTS_COLOR = input_elements_background_color

        if element_background_color != None: cls.DEFAULT_ELEMENT_BACKGROUND_COLOR = element_background_color

        if text_color != None: cls.DEFAULT_TEXT_COLOR = text_color

        if scrollbar_color != None: cls.DEFAULT_SCROLLBAR_COLOR = scrollbar_color

        if element_text_color != None: cls.DEFAULT_ELEMENT_TEXT_COLOR = element_text_color

        if input_text_color is not None: cls.DEFAULT_INPUT_TEXT_COLOR = input_text_color

        if error_button_color != (None, None): cls.DEFAULT_ERROR_BUTTON_COLOR = error_button_color

        return True

    
    @classmethod
    def themesList(cls): return sorted(list(cls.THEMES_DICTS.keys()))
    
    @classmethod
    def addTheme(cls, newThemeame, newThemeDict):
        pass
    
    def paint(self):
        theme = Theme.THEMES_DICTS[Theme.CURRENT_THEME]
        if self.PRMP_ELEMENT == 'BUTTON':
            pass

class PRMP_Widget(Theme):
    PRMP_WIDGET = 'Widget'
    _top = 'top'
    _left = 'left'
    _right = 'right'
    _bottom = 'bottom'
    _center = 'center'
    _sides = [_top, _left, _right, _bottom, _center]
        
    def bind_exit(self): print(89); self.bind_all('<Control-u>', exit)
    
    def setupOfWidget(self, gaw=False, ntb=False, tm=False, tw=False, alp=1, grabAnyWhere=False, geo=(), geometry=(), noTitleBar=False, topMost=False, alpha=1, toolWindow=False, side='center', title='Window', bg='SystemButtonFace', bind_exit=False):
        
        if geo: geometry = geo
        if gaw: grabAnyWhere = gaw
        if ntb: noTitleBar = ntb
        if tm: topMost = tm
        if alp: alpha = alp
        if tw: toolWindow = tw
        
        self.title(title)
        self.config(bg=bg)
        self.side = side
        
        if bind_exit: self.bind_exit()
        
        self.attributes('-topmost', topMost, '-toolwindow', toolWindow, '-alpha', alpha)
        
        if grabAnyWhere: self._grab_anywhere_on()
        else: self._grab_anywhere_off()
        
        if noTitleBar:
            self.state('withdrawn')
            self.overrideredirect(1)
            self.state('normal')
        
        self.lastPoints = [0, 0, 0, 0]
        self._geometry = geometry
        
        error_string = f'side must be of {self._sides} or combination of "center-{self._sides[:-1]}" delimited by "-". e.g center-right. but the two must not be the same.'
        
        if side:
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
    setupOfWindow = setupOfWidget

    def _move(self, event):
        try: self.x, self.y = event.x, event.y
        except: pass
    
    def _grab_anywhere_on(self):
        self.bind("<ButtonPress-1>", self._move)
        self.bind("<ButtonRelease-1>", self._move)
        self.bind("<B1-Motion>", self._onMotion)
    def _grab_anywhere_off(self):
        self.unbind("<ButtonPress-1>")
        self.unbind("<ButtonRelease-1>")
        self.unbind("<B1-Motion>")
    def _onMotion(self, event):
        try:
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.winfo_x() + deltax
            y = self.winfo_y() + deltay
            self.geometry("+%s+%s" % (x, y))
        except Exception as e:
            print('on motion error', e)
    def screenwidth(self): return self.winfo_screenwidth() - 70
    def screenheight(self): return self.winfo_screenheight() - 70
    def getWhichSide(self): return randint(1, 15) % 3
    @property
    def getXY(self):
        if self._geometry: return self._geometry[:3]
        return (0, 0)
    
    def _pointsToCenterOfScreen(self, x, y):
        screen_x, screen_y = self.screenwidth(), self.screenheight()
        show_x = (screen_x - x) // 2
        show_y = (screen_y - y) // 2
        return [x, y, show_x, show_y]
   
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
    
    def centerOfTopOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-1] = 50
        self.setGeometry(points)
        
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
        self.setGeometry(points)
        
    def topLeftOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2:] = 50, 50
        self.setGeometry(points)
        
    def topRightOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-1] = 50
        points[2] *= 2
        self.setGeometry(points)
        
    def bottomLeftOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[2] = 50
        points[-1] *= 2
        self.setGeometry(points)
        
    def bottomRightOfScreen(self):
        points = self.pointsToCenterOfScreen
        points[-2] *= 2
        points[-1] *= 2
        self.setGeometry(points)
    
    def topOfScreen(self): [self.topLeftOfScreen, self.topRightOfScreen, self.centerOfTopOfScreen][self.getWhichSide()]()
    def bottomOfScreen(self): [self.bottomLeftOfScreen, self.bottomRightOfScreen, self.centerOfBotomOfScreen][self.getWhichSide()]()
    def rightOfScreen(self): [self.bottomRightOfScreen, self.topRightOfScreen, self.centerOfRightOfScreen][self.getWhichSide()]()
    def leftOfScreen(self): [self.bottomLeftOfScreen, self.topLeftOfScreen, self.centerOfLeftOfScreen][self.getWhichSide()]()
    
    def _isDialog(self):
        self.grab_set()
        self.wait_window()
PRMP_Window = PRMP_Widget
class PRMP_Tk(tk.Tk, PRMP_Widget):
    def __init__(self): super().__init__()

class PRMP_Toplevel(tk.Toplevel, PRMP_Widget):
    def __init__(self, master=None): super().__init__(master)

class PRMP_Button(tk.Button, PRMP_Widget):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

class PRMP_Checkbutton(tk.Checkbutton, PRMP_Widget):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

class PRMP_Entry(tk.Entry, PRMP_Widget):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

class PRMP_Frame(tk.Frame, PRMP_Widget):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

class PRMP_LabelFrame(tk.LabelFrame, PRMP_Widget):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

class PRMP_Message(tk.Message, PRMP_Widget):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

class PRMP_Radiobutton(tk.Radiobutton, PRMP_Widget):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

class PRMP_Text(tk.Text, PRMP_Widget):
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)




