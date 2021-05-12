import os

root = r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM\prmp_lib'
libs = ['prmp_gui', 'prmp_miscs']
join = lambda p: os.path.join(root, p)
libs = [join(a) for a in libs]

prmp_gui = ['core.py', 'core_tk.py', 'core_ttk.py', 'date_widgets.py', 'dialogs.py', 'drop_downs.py', 'extensions.py', 'extensions_dialogs.py', 'image_widgets.py', 'miscs.py', 'object_widgets.py', 'plot_canvas.py', 'scrollables.py', 'tushed_widgets.py', 'tushed_windows.py', 'two_widgets.py', 'windows.py']
prmp_gui = ['miscs.py', 'core.py', 'core_tk.py', 'core_ttk.py', 'windows.py', 'tushed_windows.py', 'image_widgets.py', 'date_widgets.py', 'scrollables.py', 'drop_downs.py', 'plot_canvas.py', 'two_widgets.py', 'tushed_widgets.py', 'dialogs.py', 'extensions_dialogs.py']

prmp_miscs = ['prmp_adb.py', 'prmp_datetime.py', 'prmp_errors.py', 'prmp_exts.py', 'prmp_images.py', 'prmp_mixins.py', 'prmp_setup.py', 'prmp_unicodes.py', '_prmp_images.py']
prmp_miscs = ['_prmp_images.py', 'prmp_adb.py', 'prmp_errors.py', 'prmp_mixins.py', 'prmp_datetime.py', 'prmp_exts.py', 'prmp_images.py', 'prmp_setup.py']

prmp_gui_imports = b'''
# miscs.py
import platform
from prmp_lib.prmp_miscs.prmp_mixins import PRMP_StrMixins
import functools

# core.py
import os, time, random, tkinter as tk, sys, tkinter.ttk as ttk
from tkinter.font import Font, families
from prmp_lib.prmp_miscs.prmp_images import PRMP_Image, _PIL_, PRMP_Images, _CV2_
from .miscs import functools, platform
from prmp_lib.prmp_miscs.prmp_mixins import PRMP_GuiMixins, PRMP_Mixins

# windows.py
import ctypes, subprocess, functools, os
from prmp_lib.prmp_miscs.prmp_mixins import PRMP_ClassMixins
from prmp_lib.prmp_miscs.prmp_images import PRMP_Images

# image_widgets.py
from prmp_lib.prmp_miscs.prmp_images import *
from prmp_lib.prmp_miscs.prmp_images import _PIL_
import time

# date_widgets.py
from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime, datetime

# drop_downs.py
from prmp_lib.prmp_miscs.prmp_mixins import PRMP_AdvMixins

# plot_canvas.py
import random, math
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# dialogs.py
from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime
from prmp_lib.prmp_miscs.prmp_images import *
from prmp_lib.prmp_miscs.prmp_mixins import PRMP_ClassMixins, PRMP_AdvMixins
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import tkinter.simpledialog as simpledialog

# tushed_widgets.py
from prmp_lib.prmp_miscs.prmp_images import PRMP_DB


'''

prmp_miscs_imports = b'''

# prmp_mixins.py
import re, os, io

# prmp_datetime.py
import datetime, calendar

# prmp_exts.py
import base64, zlib, pickle, zipfile

# prmp_images.py
import sqlite3, base64, os, tkinter as tk, numpy

try:
    from PIL.ImageTk import Image, PhotoImage, BitmapImage
    from PIL import Image, ImageDraw, ImageSequence
    from PIL import ImageGrab
    _PIL_ = True
except Exception as e:
    _PIL_ = False
    print('PIL <pillow> image library is not installed.')

try:
    import cv2
    _CV2_ = True
except Exception as e:
    _CV2_ = False
    print('cv2 <opencv-python> computer vision library is not installed.')

try:
    import cv2
    _CV2_ = True
except Exception as e:
    _CV2_ = False
    print('cv2 <opencv-python> computer vision library is not installed.')

# prmp_setup.py
from distutils.core import setup
from Cython.Build import cythonize
import PyInstaller.__main__


'''

def getText(file):
    textlines = open(file, 'rb').readlines()

    text = b''
    for line in textlines:
        if b'from ' in line: continue
        elif b'import ' in line: continue
        elif b'__all__ ' in line:
            if not b'\'__all__ ' in line: continue
        text += line
    return text

def write_prmp_miscs():
    openfile = open('prmp_modules/prmp_miscs.py', 'wb')
    openfile.write(b'__author__ = "PRMP Smart"')
    openfile.write(prmp_miscs_imports)

    for file in prmp_miscs:
        f = os.path.join(libs[1], file)
        text = getText(f)
        openfile.write(text)





write_prmp_miscs()
