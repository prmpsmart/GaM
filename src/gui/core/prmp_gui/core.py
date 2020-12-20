import os
import platform
import time
import tkinter as tk
from tkinter.font import Font, families
import tkinter.ttk as ttk
from random import randint
from tkinter.filedialog import askopenfilename
from .pics import PRMP_Image
from .miscs import Mixins, partial, copyClassMethods, DateTime, bound_to_mousewheel, Columns
from ctypes import windll

# superclasses

'PRMP_GUI by PRMPSmart prmpsmart@gmail.com'


class PRMP_Theme(Mixins):
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
    
    DEFAULT_FONT = {'family': 'Segoe Marker', 'size': 13, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    
    DEFAULT_MINUTE_FONT = {'family': 'Segoe Marker', 'size': 10, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    BIG_FONT = {'family': 'Segoe Marker', 'size': 31, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    
    DEFAULT_MENU_FONT = {'family': 'Adobe Garamond Pro Bold', 'size': 10, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    
    DEFAULT_BUTTON_FONT = {'family': 'Buxton Sketch', 'size': 14, 'weight': 'bold', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    DEFAULT_BUTTONS_FONT = {'family': 'Buxton Sketch', 'size': 10, 'weight': 'bold', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    DEFAULT_SMALL_BUTTON_FONT = {'family': 'Buxton Sketch', 'size': 12, 'weight': 'bold', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    
    DEFAULT_TITLE_FONT = {'family': 'Lucida Calligraphy', 'size': 13, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}

    DEFAULT_STATUS_FONT = DEFAULT_TITLE_FONT

    
    DEFAULT_LABEL_FONT = {'family': 'Viner Hand ITC', 'size': 13, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    
    DEFAULT_LABELFRAME_FONT = {'family': 'Script MT Bold', 'size': 15, 'weight': 'normal', 'slant': 'roman', 'underline': 0, 'overstrike': 0}
    
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

        if button_color != None: cls.DEFAULT_BUTTON_COLOR = button_color

        if progress_meter_color != None: cls.DEFAULT_PROGRESS_BAR_COLOR = progress_meter_color

        if background_color != None: cls.DEFAULT_BACKGROUND_COLOR = background_color

        if input_elements_background_color != None: cls.DEFAULT_INPUT_ELEMENTS_COLOR = input_elements_background_color

        if text_color != None: cls.DEFAULT_FOREGROUND_COLOR = text_color

        if scrollbar_color != None: cls.DEFAULT_SCROLLBAR_COLOR = scrollbar_color

        if input_text_color is not None: cls.DEFAULT_INPUT_TEXT_COLOR = input_text_color
        
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
            fo = Font(name=df, **font)
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
            kwargs = {k: v for k, v in self.kwargs.items() if k not in ['font', 'very', 'placeholder', '_type']}
            
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
                _dict.update(dict(activebackground=activebackground, activeforeground=activeforeground, highlightbackground=background))
            
            oneColor = True
            col = PRMP_Theme.DEFAULT_BUTTON_COLOR
            if isinstance(col, tuple): oneColor = False
            else: background, foreground = 'white', 'black'
                
            if wt in ['Button', 'Label', 'Radiobutton', 'Checkbutton']:
                
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
                
            elif wt in ['Entry', 'Text', 'Listbox']:
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
    
    def _paintAll(self, e=0):
        self._paint()
        self._paintChildren()
    
    def paint(self, e=0):
        # print(e)
        self._paintAll()
    
    @classmethod
    def currentThemeDict(cls): return cls.THEMES_DICTS[cls.CURRENT_THEME]

PTh = PRMP_Theme

class PRMP_Widget(PRMP_Theme):
    _top = 'top'
    _left = 'left'
    _right = 'right'
    _bottom = 'bottom'
    _center = 'center'
    _sides = [_top, _left, _right, _bottom, _center]
    
    upArrow = chr(11014)
    downArrow = chr(11015)
    x_btn1 = chr(10060)
    x_btn2 = chr(10062)
    
    max_ = chr(9645)
    min_ = chr(10134)

    TIPPING = False
    
    @property
    def topest(self): return PRMP_Window.TOPEST
    
    @property
    def _children(self): return self.winfo_children()
    @property
    def toplevel(self):
        prmp_master = self.prmp_master
        while True:
            master = prmp_master.prmp_master
            if master == None: return prmp_master
            prmp_master = master



    def __init__(self, _ttk_=False, tip=None, status='', relief='groove', nonText=False, asEntry=False, highlightable=True, place={}, grid={}, pack={}, **kwargs):

        self.kwargs = kwargs.copy()
        if asEntry:
            relief = 'sunken'
            self.kwargs['asEntry'] = asEntry
        self.kwargs['relief'] = relief

        if self.kwargs.get('prmp_master'):
            self.prmp_master = self.kwargs.pop('prmp_master')
        else: self.prmp_master = None
        self._status = status
        self.font = None
        self.highlightable = highlightable
        self.nonText = nonText

        self.toggleGroup = []
        
        self.val = self.value = self.kwargs.get('value', '1')
        self.var = self.variable = self.kwargs.get('variable')
    
        self._ttk_ = _ttk_
        
        try:
            font = self.kwargs.get('font', 'DEFAULT_FONT')
            # font = self.kwargs.get('font', 'PRMP_FONT')
            self.useFont(font)
        except: pass
        
        if tip: self.addTip(tip)
        
        self.bind('<Enter>', self.entered, '+')
        self.bind('<Leave>', self.left, '+')

        self.positionWidget(place=place, pack=pack, grid=grid)
        
    def entered(self, e=0):
        if not self.nonText: self.statusShow()
        if self.highlightable:
            try: self.configure(relief='solid')
            except: pass
    
    def left(self, e=0):
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
        try: return self['text']
        except: pass
        
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
    
    def positionWidget(self, widget=None, place={}, grid={}, pack={}):
        if widget == None: widget = self
        trues = [bool(pos) for pos in [place, pack, grid]].count(True)
        if trues > 1: raise ValueError('only one is required between [place, pack, grid]')
        else:
            if place: widget.place(**place)
            elif pack: widget.pack(**pack)
            elif grid: widget.grid(**grid)
    
    def switchOne(self, e=0):
        val = self.var.get()
        if self.onFg == False:
            self.light()
            self.var.set('0')
            self.onFg = True
        elif self.PRMP_WIDGET == 'Radiobutton' and val == self.value: self.light()
        elif val != self.value: self.unlight()
        else:
            self.unlight()
            self.onFg = False
    
    def checked(self, e=0):
        if self.variable:
            if self.variable.get() == self.value: self.light()
            else: self.unlight()
    
    def switchGroup(self, e):
        self.var.set(self.val)
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

        def setRelief(e=0): wid.configure(relief=relief, **kwargs)
        def resetRelief(e=0): wid.paint()
        
        wid.bind('<Enter>', setRelief, '+')
        wid.bind('<Leave>', resetRelief, '+')
    
    def bindEntryHighlight(self, **kwargs): self.bindOverrelief(self, **kwargs)
    
    def readonly(self, wh=''):
        try: self.state('readonly')
        except: self.disabled()
    
    def disabled(self): self.state('disabled')
    
    def active(self): self.state('active')
    
    def normal(self): self.state('normal')
    
    def state(self, s):
        try: self.configure(state=s)
        except: super().state(s)

    def config(self, **kwargs):
        self.kwargs.update(kwargs)
        self.configure(**kwargs)
    
    @property
    def PRMP_WIDGET(self): return self.className.replace('PRMP_', '')
       
    def addTip(self, tip='Tip', delay=0, follow=True):
        if PRMP_Widget.TIPPING: from .extensions import ToolTip; ToolTip(self, msg=tip, delay=delay, follow=follow)
    
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
        self.bind("<ButtonPress-1>", partial(PRMP_Widget._move, root), '+')
        self.bind("<ButtonRelease-1>", partial(PRMP_Widget._move, root), '+')
        self.bind("<B1-Motion>", partial(PRMP_Widget._onMotion, root), '+')
        
        self.bind("<ButtonPress-3>", partial(PRMP_Widget._move, root), '+')
        self.bind("<ButtonRelease-3>", partial(PRMP_Widget._move, root), '+')
        self.bind("<B3-Motion>", partial(PRMP_Widget._onMotion, root), '+')
    
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
PWd = PRMP_Widget

class PRMP_(PRMP_Widget):

    def __init__(self, **kwargs):
        super().__init__( _ttk_=False, **kwargs)
P_ = PRMP_

class PRMP_Style_(PRMP_Widget):

    def __init__(self, highlightable=False, **kwargs):
        super().__init__(_ttk_=True, highlightable=highlightable, **kwargs)
    
    @property
    def style(self): return PRMP_Window.STYLE
PS_ = PRMP_Style_

class PRMP_Input:
    
    def __init__(self, placeholder='', _type='text', values=[], very=False, **kwargs):
        _type = _type.lower()

        self.placeholder = placeholder
        self.values = values
        
        self.bind("<FocusIn>", self._clear_placeholder, '+')
        self.bind("<FocusOut>", self._add_placeholder, '+')

        types = ['email', 'number', 'money']
        
        if _type == 'email':
            self.bind('<KeyRelease>', self.checkingEmail, '+')
            self.verify = self.checkingEmail
        elif _type == 'number':
            self.set = self.setNumber
            self.get = self.getNumber
            self.bind('<KeyRelease>', self.checkingNumber, '+')
            self.verify = self.checkingNumber
        elif _type == 'money':
            self.placeholder = self._moneySign
            self.set = self.setMoney
            self.get = self.getMoney
            self.bind('<KeyRelease>', self.checkingMoney, '+')
            self.verify = self.checkingMoney
        else:
            self.bind('<KeyRelease>', self.normVery, '+')
            self.verify = self.normVery
        
        if self.values or (_type in types): self.very = True
        else: self.very = False or very

        self.set(self.placeholder)
    
    def normVery(self, e=0):
        if not self.very: return
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
        self.insert(0, number)
        
    def getNumber(self):
        number = self._get()
        if self.checkNumber(number): return number

    def setMoney(self, money=None):
        self.clear()
        if money == self.placeholder or not money: money = self.placeholder
        elif not self.checkMoney(money): money = self.numberToMoney(money)
        self.insert(0, money)
        
    def getMoney(self):
        money = self._get()
        if self.checkMoney(money): return self.moneyToNumber(money)
        return money
        
    def entered(self, e=0):
        super().entered()
        self._clear_placeholder()
        
    def left(self, e=0):
        super().left()
        self.focus()
        self._add_placeholder()
    
    def green(self):
        self.configure(foreground='green')
        return True
    
    def red(self):
        self.configure(foreground='red')
        return False
    
    def checkingEmail(self, e=0):
        email = self._get()
        if email:
            if self.checkEmail(email): return self.green()
            else: return self.red()
    
    def checkingNumber(self, e=0):
        number = self._get()
        if number:
            if self.checkNumber(number): return self.green()
            else: return self.red()
    
    def checkingMoney(self, e=0):
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
    
    def normal(self):
        super().normal()
        self.verify()
        
    def disabled(self):
        self._add_placeholder()
        super().disabled()
        self.verify()
        
    def paint(self):
        super().paint()
        self.verify()

    def set(self, values):
        self.clear()
        self.insert(0, values)
        self.verify()
    
    def _clear_placeholder(self, e=0):
        if self._get() == self.placeholder: self.clear()

    def _add_placeholder(self, e=0):
        if self._get() == '': self.set(self.placeholder)
        pass
    
    def clear(self): self.delete('0', 'end')
    
    def _get(self): return super().get()
    
    def get(self):
        get = self._get()
        if get == self.placeholder: get = ''
        return get
PI = PRMP_Input

class PRMP_InputButtons:
    
    def set(self, val):
        if val: self.var.set(val)
        else: self.var.set('0')
    
    def get(self):
        val = self.var.get()
        if val == self.val: return True
        else: return False
    
PIB = PRMP_InputButtons

# based on tk only

class PRMP_Canvas(PRMP_, tk.Canvas):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Canvas.__init__(self, master, **config)
        PRMP_.__init__(self, prmp_master=master,**config, **kwargs)
Canvas = PCv = PRMP_Canvas

class PRMP_Message(PRMP_, PRMP_Input, tk.Message):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Message.__init__(self, master=master, **config)
        PRMP_.__init__(self, prmp_master=master,**config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)
Message = PM = PRMP_Message

class PRMP_Text(PRMP_Input, PRMP_, tk.Text):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Text.__init__(self, master=master, **config)
        PRMP_.__init__(self, prmp_master=master, **config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)
        
    def _get(self): return tk.Text.get(self, '1.0', 'end').strip('\n')
    
    def set(self, values): self.clear(); self.insert('0.0', values)
    
    def clear(self): self.delete('0.0', 'end')

    @property
    def PRMP_WIDGET(self): return 'Text'
Text = PTx = PRMP_Text

class PRMP_Listbox(PRMP_, tk.Listbox):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Listbox.__init__(self, master=master, **config)
        PRMP_.__init__(self, prmp_master=master, **config, **kwargs)
    
Listbox = PLb = PRMP_Listbox


# based on ttk only

class PRMP_Combobox(PRMP_Input, PRMP_Style_, ttk.Combobox):
    
    def __init__(self, master=None, type_='', config={}, values=[], **kwargs):

        if type_.lower() == 'gender': values = ['Male', 'Female']

        ttk.Combobox.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
        PRMP_Input.__init__(self, values=values, **kwargs)
        
        self.changeValues(values)

    
    @property
    def PRMP_WIDGET(self): return 'Combobox'
    
    def changeValues(self, values):
        self.values = values
        self['values'] = values
    
    def getValues(self): return self['values']
Combobox = PCb = PRMP_Combobox

class PRMP_LabeledScale(PRMP_Style_, ttk.LabeledScale):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.LabeledScale.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
LabeledScale = PLS = PRMP_LabeledScale

class PRMP_Notebook(PRMP_Style_, ttk.Notebook):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Notebook.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
    
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
        # print(widget)
        if "close" in element:
            widget.state(['alternate'])
        else:
            widget.state(['!alternate'])

Notebook = PN = PRMP_Notebook

class PRMP_Panedwindow(PRMP_Style_, ttk.Panedwindow):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Panedwindow.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
Panedwindow = PPw = PRMP_Panedwindow

class PRMP_Progressbar(PRMP_Style_, ttk.Progressbar):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Progressbar.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
Progressbar = PPb = PRMP_Progressbar

class PRMP_Separator(PRMP_Style_, ttk.Separator):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Spinbox.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
Separator = PS = PRMP_Separator

class PRMP_Sizegrip(PRMP_Style_, ttk.Sizegrip):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Sizegrip.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
Sizegrip = PSg = PRMP_Sizegrip

class PRMP_Style(ttk.Style, Mixins):
    loaded = False
    ttkthemes = ("black", "blue", 'prmp')
    ttkstyles = ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

    def __init__(self, master=None):
        super().__init__(master)
        if not PRMP_Style.loaded: self.createPrmp()
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
        if PRMP_Style.loaded: return
        
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
        PRMP_Style.loaded = True
    
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
                    'fieldbackground': text_background,
                    # 'arrowsize': 15,
                    # 'selectborderwidth': 2,
                    # 'padding': 2,
                    # 'insertwidth': 2,
                    'arrowcolor': foreground,
                },
                'layout': [('Spinbox.border', {'children': [('Spinbox.field', {'side': 'top', 'sticky': 'we', 'children': [('null', {'side': 'right', 'sticky': '', 'children': [('Spinbox.uparrow', {'side': 'right', 'sticky': 'e'}), ('Spinbox.downarrow', {'side': 'right', 'sticky': 'e'})]}), ('Spinbox.padding', {'sticky': 'nswe', 'children': [('Spinbox.textarea', {'sticky': 'nswe'})]})]})]})]
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
                    'background': [('selected', text_background)],#, ('hover', button_background)],
                    'foreground': [('selected', text_foreground)]#, ('hover', button_foreground)],
                    # 'relief': [('hover', 'ridge')]
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
                    'relief': 'ridge'
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

    def update(self, e=0):
        if not PRMP_Style.loaded: self.createPrmp()
        self.theme_settings('prmp', self.settings)
Style = PSt = PRMP_Style

class PRMP_Treeview(PRMP_Style_, ttk.Treeview):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Treeview.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)    
Treeview = PTv = PRMP_Treeview

#   common to tk and ttk

#   from tk widgets --> PRMP_

class PRMP_Button(PRMP_, tk.Button):
    
    def __init__(self, master=None, font='DEFAULT_BUTTON_FONT', asEntry=False, asLabel=False, config={}, **kwargs):
        tk.Button.__init__(self, master, **config)
        PRMP_.__init__(self, prmp_master=master,font=font, asEntry=asEntry, **config, **kwargs)
    
    @property
    def PRMP_WIDGET(self): return 'Button'
Button = PB = PRMP_Button

class PRMP_Checkbutton(PRMP_InputButtons, PRMP_, tk.Checkbutton):
    
    def __init__(self, master=None, asLabel=False, config={}, **kwargs):
        self.var = tk.StringVar()
        tk.Checkbutton.__init__(self, master, variable=self.var, **config)
        PRMP_.__init__(self, prmp_master=master,variable=self.var, asLabel=asLabel, **config, **kwargs)
        
        self.var.set('0')
        self.toggleSwitch()

    @property
    def PRMP_WIDGET(self): return 'Checkbutton'
    def disabled(self):
        
        self['fg'] = PRMP_Theme.DEFAULT_BACKGROUND_COLOR
        self.state('disabled')
Checkbutton = PC = PRMP_Checkbutton

class PRMP_Entry(PRMP_Input, PRMP_, tk.Entry):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Entry.__init__(self, master, **config)
        PRMP_.__init__(self, prmp_master=master, **config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)
    
    @property
    def PRMP_WIDGET(self): return 'Entry'
Entry = PE = PRMP_Entry

class PRMP_Frame(PRMP_, tk.Frame):
    
    def __init__(self, master=None, bd=2, relief='flat', highlightable=False, config={}, **kwargs):
        tk.Frame.__init__(self, master, relief=relief, bd=bd, **config)
        PRMP_.__init__(self, prmp_master=master,relief=relief, highlightable=highlightable, nonText=True, **config, **kwargs)

    @property
    def PRMP_WIDGET(self): return 'Frame'
Frame = PF = PRMP_Frame

class PRMP_Label(PRMP_, tk.Label):
    
    def __init__(self, master=None, font='DEFAULT_LABEL_FONT', config={}, **kwargs):
        tk.Label.__init__(self, master, **config)
        PRMP_.__init__(self, prmp_master=master,font=font, **config, **kwargs)

    @property
    def PRMP_WIDGET(self): return 'Label'
Label = PL = PRMP_Label

class PRMP_LabelFrame(PRMP_, tk.LabelFrame):
    
    def __init__(self, master=None, font='DEFAULT_LABELFRAME_FONT', config={}, **kwargs):
        tk.LabelFrame.__init__(self, master,  **config)
        PRMP_.__init__(self, prmp_master=master,font=font, **config, **kwargs)
    
    @property
    def PRMP_WIDGET(self): return 'LabelFrame'
LabelFrame = PLF = PRMP_LabelFrame

class PRMP_Menubutton(PRMP_, tk.Scrollbar):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Scrollbar.__init__(self, master, **config)
        PRMP_.__init__(self, prmp_master=master,**config, **kwargs)
Scrollbar = PM = PRMP_Menubutton

class PRMP_OptionMenu(PRMP_, tk.OptionMenu):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.OptionMenu.__init__(self, master, **config)
        PRMP_.__init__(self, prmp_master=master,**config, **kwargs)
OptionMenu = PO = PRMP_OptionMenu

class PRMP_PanedWindow(PRMP_, tk.PanedWindow):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.PanedWindow.__init__(self, master, **config)
        PRMP_.__init__(self, prmp_master=master,**config, **kwargs)
PanedWindow = PP = PRMP_PanedWindow

class PRMP_Radiobutton(PRMP_InputButtons, PRMP_, tk.Radiobutton):
    
    def __init__(self, master=None, asLabel=False, config={}, **kwargs):
        tk.Radiobutton.__init__(self, master, **config)
        PRMP_.__init__(self, prmp_master=master,asLabel=asLabel, **config, **kwargs)
    
    @property
    def PRMP_WIDGET(self): return 'Radiobutton'
Radiobutton = PR = PRMP_Radiobutton

class PRMP_Scale(PRMP_, tk.Scale):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Scale.__init__(self, master, **config)
        PRMP_.__init__(self, prmp_master=master,**config, **kwargs)
Scale = PS = PRMP_Scale

class PRMP_Scrollbar(PRMP_, tk.Scrollbar):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Scrollbar.__init__(self, master, **config)
        PRMP_.__init__(self, prmp_master=master,**config, **kwargs)
    
    def set(self, first, last): return ttk.Scrollbar.set(self, first, last)
Scrollbar = PSc = PRMP_Scrollbar

class PRMP_Spinbox(PRMP_, tk.Spinbox):
    
    def __init__(self, master=None, config={}, **kwargs):
        tk.Spinbox.__init__(self, master, **config)
        PRMP_.__init__(self, prmp_master=master,**config, **kwargs)
Spinbox = PSp = PRMP_Spinbox

#   from ttk widgets --> PRMP_Style_

class PRMP_Style_Button(PRMP_Style_, ttk.Button):
    
    def __init__(self, master=None, font='DEFAULT_BUTTON_FONT', asEntry=False, asLabel=False, config={}, **kwargs):
        ttk.Button.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,font=font, asEntry=asEntry, **config, **kwargs)
SButton = PSB = PRMP_Style_Button

class PRMP_Style_Checkbutton(PRMP_InputButtons, PRMP_Style_, ttk.Checkbutton):
    
    def __init__(self, master=None, asLabel=False, config={}, **kwargs):
        self.var = tk.StringVar()
        ttk.Checkbutton.__init__(self, master, variable=self.var, **config)
        PRMP_Style_.__init__(self, prmp_master=master,variable=self.var, asLabel=asLabel, **config, **kwargs)
        
        self.var.set('0')
        self.toggleSwitch()
SCheckbutton = PSC = PRMP_Style_Checkbutton

class PRMP_Style_Entry(PRMP_Input, PRMP_Style_, ttk.Entry):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Entry.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master, **config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)
SEntry = PSE = PRMP_Style_Entry

class PRMP_Style_Frame(PRMP_Style_, ttk.Frame):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Frame.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, nonText=True, **kwargs)
SFrame = PSF = PRMP_Style_Frame

class PRMP_Style_Label(PRMP_Style_, ttk.Label):
    
    def __init__(self, master=None, font='DEFAULT_LABEL_FONT', config={}, **kwargs):
        ttk.Label.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,font=font, **config, **kwargs)
SLabel = PSL = PRMP_Style_Label

class PRMP_Style_LabelFrame(PRMP_Style_, ttk.LabelFrame):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.LabelFrame.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master, **config, **kwargs)
SLabelFrame = PSLF = PRMP_Style_LabelFrame

class PRMP_Style_Menubutton(PRMP_Style_, ttk.Scrollbar):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Scrollbar.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
SScrollbar = PSM = PRMP_Style_Menubutton

class PRMP_Style_OptionMenu(PRMP_Style_, ttk.OptionMenu):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.OptionMenu.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
SOptionMenu = PSO = PRMP_Style_OptionMenu

class PRMP_Style_PanedWindow(PRMP_Style_, ttk.PanedWindow):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.PanedWindow.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
SPanedWindow = PSP = PRMP_Style_PanedWindow

class PRMP_Style_Radiobutton(PRMP_InputButtons, PRMP_Style_, ttk.Radiobutton):
    
    def __init__(self, master=None, asLabel=False, config={}, **kwargs):
        ttk.Radiobutton.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,asLabel=asLabel, **config, **kwargs)
SRadiobutton = PSR = PRMP_Style_Radiobutton

class PRMP_Style_Scale(PRMP_Style_, ttk.Scale):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Scale.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
SScale = PSS = PRMP_Style_Scale

class PRMP_Style_Scrollbar(PRMP_Style_, ttk.Scrollbar):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Scrollbar.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
    
    def set(self, first, last): return ttk.Scrollbar.set(self, first, last)
SScrollbar = PSSc = PRMP_Style_Scrollbar

class PRMP_Style_Spinbox(PRMP_Style_, ttk.Spinbox):
    
    def __init__(self, master=None, config={}, **kwargs):
        ttk.Spinbox.__init__(self, master, **config)
        PRMP_Style_.__init__(self, prmp_master=master,**config, **kwargs)
SSpinbox = PSSp = PRMP_Style_Spinbox

#  windows

class PRMP_Window(PRMP_Widget):
    TOPEST = None
    STYLE = None

    TKICON = ''
    PRMPICON = ''

    def __init__(self, container=True, containerConfig={},  gaw=None, ntb=None, tm=None, tw=None, grabAnyWhere=True, geo=(300, 300), geometry=(), noTitleBar=True, topMost=True, alpha=1, toolWindow=False, side='center', title='Window', bindExit=True, nrz=None, notResizable=True, atb=None, asb=None, be=None, resize=(0, 0), addStatusBar=True, addTitleBar=True, tkIcon='', prmpIcon='', **kwargs):
        
        if PRMP_Window.TOPEST == None:
            self.bind('<<PRMP_STYLE_CHANGED>>', self.paint)
            PRMP_Window.TOPEST = self
            self.createDefaultFonts()
            PRMP_Window.STYLE = PRMP_Style(self)
        
        PRMP_Widget.__init__(self, geo=geo, nonText=True, **kwargs)

        self.container = None
        self.zoomed = False
        self.iconed = False
        self.titleBar = None
        self.statusBar = None
        self.side = side
        self.titleText = title
        
        self.title(title)
        self.co = 0

        if container:
            self.container = PRMP_Style_Frame(self)
            self.container.configure(relief='groove')
        
        if geo != None: geometry = geo
        if gaw != None: grabAnyWhere = gaw
        if ntb != None: noTitleBar = ntb
        if tm != None: topMost = tm
        if nrz != None: notResizable = nrz
        if tw != None: toolWindow = tw
        if be != None: bindExit = be
        if atb != None: addTitleBar = atb
        if asb != None: addStatusBar = asb
        
        if notResizable: resize = (0, 0)
        
        if bindExit: self.bindExit()

        self.windowAttributes(topMost=topMost, toolWindow=toolWindow, alpha=alpha, noTitleBar=noTitleBar, addTitleBar=addTitleBar, addStatusBar=addStatusBar, prmpIcon=prmpIcon, tkIcon=tkIcon, resize=resize)
        
        if grabAnyWhere: self._grab_anywhere_on()
        else: self._grab_anywhere_off()
        
        self.bindToWidget(('<Configure>', self.placeContainer), ('<FocusIn>', self.placeContainer), ('<Map>', self.deiconed), ('<Control-M>', self.minimize), ('<Control-m>', self.minimize))
        
        self.placeOnScreen(side, geometry)

        if noTitleBar: self.after(10, self.addWindowToTaskBar)
    
    def windowAttributes(self, topMost=0, toolWindow=0, alpha=1, noTitleBar=1,  addTitleBar=1, addStatusBar=1, tkIcon='', prmpIcon='', resize=(1, 1)):
        self.resize = resize
        
        self.resizable(*self.resize)
        
        self.noTitleBar = noTitleBar
        self._addStatusBar = addStatusBar
        self._addTitleBar = addTitleBar

        if noTitleBar: self.overrideredirect(True)
        
        if addTitleBar:
            if toolWindow: self.__r = 1
            else: self.__r = 0
            self.addTitleBar()
            self.setPRMPIcon(prmpIcon or PRMP_Window.PRMPICON)
        
        if addStatusBar: self.addStatusBar()
        
        self.toolWindow = toolWindow
        self.topMost = topMost
        self.alpha = alpha

        self.setTkIcon(tkIcon or PRMP_Window.TKICON)

        self.attributes('-topmost', topMost, '-toolwindow', toolWindow, '-alpha', alpha)
    
    def topmost(self): self.attributes('-topmost', True)

    def addWindowToTaskBar(self, e=0):
        self.withdraw()
        winfo_id = self.winfo_id()
        parent = windll.user32.GetParent(winfo_id)
        res = windll.user32.SetWindowLongW(parent, -20, 0)
        self.deiconify()
        if not res: self.after(10, self.addWindowToTaskBar)
 
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
            if geometry: self.setGeometry(self._geometry)
        
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
        
    def getWhichSide(self): return randint(1, 15) % 3
    
    @property
    def getXY(self):
        if self._geometry: return self._geometry[:3]
        return (400, 300)
    
    def _pointsToCenterOfScreen(self, x, y, *a):
        screen_x, screen_y = self.screen_xy
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

    def _isDialog(self, g=1):
        self.attributes('-toolwindow', 1)
        self.resizable(0, 0)
        if g: self.grab_set()
        self.focus()
        self.wait_window()
    
    
    def placeContainer(self, e=0, h=0):
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
    
    def minimize(self, e=0):
        self.withdraw()
        self.overrideredirect(False)
        self.iconify()
        self.iconed = True
    
    def deiconed(self, e=0):
        if self.iconed:
            self.co += 1
            self.iconed = False
            v = self.winfo_viewable()
            if v:
                if self.noTitleBar: self.overrideredirect(True)
                self.normal()
                self.addWindowToTaskBar()
        
    def maximize(self, e=0):
        if self.__r: return
        if self.resize.count(True) < 2: return
        
        if self.zoomed:
            self.zoomed = False
            self.state('normal')
            self.isNormal()
        else:
            self.zoomed = True
            self.state('zoomed')
            self.isMaximized()
    
    def isMaximized(self): pass

    def isMinimized(self): pass
    
    def isNormal(self): pass
    
    def addTitleBar(self, title=''):
        if self.titleBar:
            self.title(title)
            self.titleBar.set(title or self.titleText)
            self.placeTitlebar()
            return
        F, L, B = PRMP_Style_Frame, PRMP_Style_Label, PRMP_Style_Button

        w, y = self.geo[:2]


        fr = F(self)

        if not self.__r:
            self.imgMin = PRMP_Image('green', resize=(20, 20))
            self._min = B(fr, config=dict(command=self.minimize, text=self.min_, image=self.imgMin, style='green.TButton'), tip='Minimize', font='DEFAULT_SMALL_BUTTON_FONT')

            self.imgMax = PRMP_Image('yellow', resize=(20, 20))
            self._max = B(fr, config=dict(command=self.maximize, text=self.max_, image=self.imgMax, style='yellow.TButton'), tip='Maximize', font='DEFAULT_SMALL_BUTTON_FONT')

        self.imgExit = PRMP_Image('red', resize=(20, 20))
        self._exit = B(fr, config=dict(text=self.x_btn2, command=self.destroy, image=self.imgExit, style='exit.TButton'), tip='Exit', font='DEFAULT_SMALL_BUTTON_FONT')

        self._icon = L(fr)

        self.titleBar = L(fr, config=dict( text=title or self.titleText), font='DEFAULT_TITLE_FONT', relief='groove')
        self.titleBar.bind('<Double-1>', self.maximize, '+')
        self.titleBar._moveroot()

        self.placeTitlebar()
    
    def setTkIcon(self, icon): self.iconbitmap(icon)

    def setPRMPIcon(self, icon):
        self.imgIcon = PRMP_Image(icon, resize=(20, 20))
        self._icon['image'] = self.imgIcon
    
    def placeTitlebar(self):
        if self.titleBar:
            x = self.titleBar.master.winfo_width()
            xw = self.titleBar.master.master.winfo_width()
            self.titleBar.master.place(x=0, rely=0, h=30, w=xw)
            if x < 0: return
            w = 30
            if not self.__r:
                self._min.place(x=x-90, rely=0, relh=1, w=30)
                self._max.place(x=x-60, rely=0, relh=1, w=30)
                w = 90
            self._icon.place(x=0, rely=0, relh=1, w=30)
            self.titleBar.place(x=30, rely=0, relh=1, w=x-w-30)
            self._exit.place(x=x-30, rely=0, relh=1, w=30)

    def editStatus(self, text):
        if self.statusBar: self.statusBar.set(text)
    
    def addStatusBar(self):
        if self.statusBar:
            self.placeStatusBar()
            return
    
        F, L, B = PRMP_Style_Frame, PRMP_Style_Label, PRMP_Style_Button

        fr = F(self)
        self.statusBar = L(fr, config=dict(text='Status' or self.statusText, ), font='DEFAULT_STATUS_FONT')
        self.statusBar._moveroot()
        self._up = B(fr, config=dict(text=self.upArrow, command=self.prevTheme), font='DEFAULT_SMALL_BUTTON_FONT', tip='Previous Theme')
        self._down = B(fr, config=dict(text=self.downArrow, command=self.nextTheme), font='DEFAULT_SMALL_BUTTON_FONT', tip='Next Theme')
        
        self.placeStatusBar()
        
    def placeStatusBar(self, e=0):
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

    def prevTheme(self):
        theme, index = self._prevTheme()
        self.editStatus(f'Theme({theme}) | Index({index})')
        self._colorize()
        
    def nextTheme(self):
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
    
    def paint(self, e=0):
        self._paintAll()
        self.afterPaint()
    
    def afterPaint(self): pass

    @property
    def toplevel(self): return self
    
    def bindExit(self):
        def ex(e=0): os.sys.exit()
        self.bind_all('<Control-/>', ex)
PW = PRMP_Window

class PRMP_Tk(tk.Tk, PRMP_Window):
    def __init__(self, _ttk_=False, **kwargs):
        tk.Tk.__init__(self)
        PRMP_Window.__init__(self, _ttk_=_ttk_, **kwargs)
Tk = PT = PRMP_Tk

class PRMP_Toplevel(tk.Toplevel, PRMP_Window):
    def __init__(self, master=None, _ttk_=False, **kwargs):
        tk.Toplevel.__init__(self, master)
        PRMP_Window.__init__(self, _ttk_=_ttk_, **kwargs)
Toplevel = PTl = PRMP_Toplevel

class PRMP_MainWindow(Mixins):
    
    def __init__(self, master=None, _ttk_=False, atb=1, asb=1, **kwargs):
        if master: self.root = PRMP_Toplevel(master, _ttk_=_ttk_, atb=atb, asb=asb, **kwargs)
        else: self.root = PRMP_Tk(_ttk_=_ttk_, atb=atb, asb=asb, **kwargs)
        self.root.root = self.root

        for k, v in self.class_.__dict__.items():
            if k.startswith('__') or k == 'root': continue
            if callable(v): self.root.__dict__[k] = partial(v, self)

    
    def __str__(self): return str(self.root)
    
    def __getitem__(self, name):
        attr = self.__dict__.get(name, '_prmp_')
        if attr != '_prmp_': return attr
        else: return getattr(self.root, name)

    
    def __getattr__(self, name): return getattr(self.root, name)
MainWindow = PMW = PRMP_MainWindow


#   scrollable widgets

class PRMP_ListBox(PRMP_Frame):
    selection_modes = ['single', 'browse', 'multiple', 'extended']
    
    def __getattr__(self, attr):
        ret = self.getFromSelf(attr, self._unget)
        if ret != self._unget: return ret
        else: return getattr(self.listbox, attr)

    def __init__(self, master=None, columns=[], callback=None, listboxConfig={}, **kwargs):
        super().__init__(master=master, **kwargs)

        self.values = []
        self.last = None
        self.callback = callback

        self.listbox = PRMP_Listbox(self, config=listboxConfig)
        self.listbox.bind('<<ListboxSelect>>', self.clicked)

        self.xscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="horizontal", command=self.listbox.xview))
        self.yscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="vertical", command=self.listbox.yview))
        self.listbox.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)
        
        self.xscrollbar.pack(side="bottom", fill="x")
        self.listbox.pack(side='left', fill='both', expand=1)
        self.yscrollbar.pack(side="right", fill="y")

        bound_to_mousewheel(0, self)
    
    def clear(self): self.delete(0, self.last)
    
    def set(self, values, showAttr=''):
        self.clear()
        self.last = len(values)
        for val in values:
            st = getattr(val, showAttr, None) or str(val)
            self.listbox.insert('end', st)
        self.values = values
    
    def clicked(self, e=0):
        if self.callback:
            selected = self.selected
            if selected: self.callback(selected=self.selected, event=e)

    @property
    def selected(self):
        sels = self.listbox.curselection()
        if sels:
            select = []
            for sel in sels: select.append(self.values[sel])
            return select


ListBox = PLB = PRMP_ListBox

class PRMP_TreeView(PRMP_Frame):
    __shows = ['tree', 'headings']
    __slots__ = ['tree']
    
    # def __getattr__(self, attr):
        # ret = self.getFromSelf(attr, self._unget)
        # if ret != self._unget: return ret
        # else: return getattr(self.treeview, attr)
    
    def __init__(self, master=None, columns=[], **kwargs):
        super().__init__(master=master, **kwargs)
        self.treeview = None
        self.xscrollbar = None
        self.yscrollbar = None

        self.columns = Columns(columns)
        # print(self.columns)
        self.setColumns(columns)
        self.create()
        
    def create(self):
        if self.treeview:
            self.treeview.destroy()
            del self.treeview
            
            self.xscrollbar.destroy()
            del self.xscrollbar

            self.yscrollbar.destroy()
            del self.yscrollbar


        self.t = self.tree = self.treeview = PRMP_Treeview(self)
        self.xscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="horizontal", command=self.treeview.xview))
        self.yscrollbar = PRMP_Style_Scrollbar(self, config=dict(orient="vertical", command=self.treeview.yview))
        self.treeview.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)
        
        self.xscrollbar.pack(side="bottom", fill="x")
        self.treeview.pack(side='left', fill='both', expand=1)
        self.yscrollbar.pack(side="right", fill="y")
        bound_to_mousewheel(0, self)
        
        self.ivd = self.itemsValuesDict = {}
        self.firstItem = None
        self.current = None
        self.attributes = []
        
        self.bindings()
    
    def bindings(self):
        self.tree.bind('<<TreeviewSelect>>', self.selected)

    def selected(self, e=0):
        item = self.tree.focus()
        self.current = self.ivd.get(item)
        return self.current

    def insert(self, item, position='end',  **kwargs): return self.treeview.insert(item, position, **kwargs)
    
    def tag_config(self, tagName, font=PRMP_Theme.DEFAULT_FONT, **kwargs):
        font = Font(**font)
        # return self.tree.tag_configure(tagName, font=font, **kwargs)
        return self.tree.tag_configure(tagName, **kwargs)
    
    def heading(self, item, **kwargs): return self.treeview.heading(item, **kwargs)
    
    def column(self, item, **kwargs): return self.treeview.column(item, **kwargs)
    
    def treeviewConfig(self, **kwargs): self.treeview.configure(**kwargs)
    
    tvc = Config = treeviewConfig

    def setColumns(self, columns=[]):
        self.create()

        if columns: self.columns.process(columns)
            
        if len(self.columns) > 1: self.tvc(columns=self.columns[1:])
        self.updateHeading()
            
    def updateHeading(self):
        for column in self.columns:
            self.heading(column.index, text=column.text, anchor='center')
            # print(column.width, time.time.time())
            self.column(column.index, width=column.width, minwidth=80, stretch=1,  anchor="center")
    
    def _set(self, obj=None, parent='', op=False):
        
        cols = self.columns.get(obj)
        
        name, *columns = self.columns.get(obj)
        tag = 'prmp'
        
        # the fourth value of this [text, attr, width, value] can be used in sorting, it wont insert the region and its columns both into self.tree and self.ivd if not equal to value
        
        item = self.insert(parent, text=name, values=columns, tag=tag, open=op)
        self.tag_config(tag)

        self.ivd[item] = obj
        
        if self.firstItem == None:
            self.firstItem = item
            self.treeview.focus(self.firstItem)
        
        subs = obj.subs
        if subs:
            for sub in subs: self._set(sub, item, op)
    
    def set(self, obj, op=0):
        self.setColumns()
        if self.firstItem:
            self.tree.delete(self.firstItem)
            self.firstItem = None
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


