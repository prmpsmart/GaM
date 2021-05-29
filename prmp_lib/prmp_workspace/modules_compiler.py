import os

root = r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM\prmp_lib'
libs = ['prmp_gui', 'prmp_miscs']
join = lambda p: os.path.join(root, p)
libs = [join(a) for a in libs]

prmp_gui = ['core.py', 'core_tk.py', 'core_ttk.py', 'date_widgets.py', 'dialogs.py', 'drop_downs.py', 'extensions.py', 'extensions_dialogs.py', 'image_widgets.py', 'miscs.py', 'object_widgets.py', 'plot_canvas.py', 'scrollables.py', 'tushed_widgets.py', 'tushed_windows.py', 'two_widgets.py', 'windows.py']
prmp_gui = ['miscs.py', 'core.py', 'core_tk.py', 'core_ttk.py', 'windows.py', 'tushed_windows.py', 'image_widgets.py', 'date_widgets.py', 'scrollables.py', 'drop_downs.py', 'plot_canvas.py', 'two_widgets.py', 'tushed_widgets.py', 'dialogs.py', 'extensions_dialogs.py']

prmp_miscs = ['prmp_adb.py', 'prmp_datetime.py', 'prmp_errors.py', 'prmp_exts.py', 'prmp_images.py', 'prmp_mixins.py', 'prmp_setup.py', 'prmp_unicodes.py', '_prmp_images.py']
prmp_miscs = ['_prmp_images.py', 'prmp_adb.py', 'prmp_errors.py', 'prmp_mixins.py', 'prmp_datetime.py', 'prmp_exts.py', 'prmp_images.py', 'prmp_setup.py']




prmp_miscs_imports = b'''

try: import re
except: ...

try: import os
except: ...

try: import io
except: ...

try: import datetime
except: ...

try: import calendar
except: ...

try: import base64
except: ...

try: import zlib
except: ...

try: import pickle
except: ...

try: import zipfile
except: ...

try: import sqlite3
except: ...

try: import tkinter as tk
except: ...

try: import numpy
except: ...

try:
    from PIL.ImageTk import Image, PhotoImage, BitmapImage
    from PIL import Image, ImageDraw, ImageSequence, ImageGrab
    _PIL_ = True
except Exception as e:
    _PIL_ = False
    # print('PIL <pillow> image library is not installed.')

try:
    import cv2
    _CV2_ = True
except Exception as e:
    _CV2_ = False
    # print('cv2 <opencv-python> computer vision library is not installed.')

# prmp_setup.py
try:
    from distutils.core import setup
    from Cython.Build import cythonize
    import PyInstaller.__main__
except: ...


'''
prmp_gui_imports = b'''

try: import platform
except: ...

from prmp_miscs import *
from prmp_miscs import _PIL_, _CV2_

try: import functools
except: ...

try: import time
except: ...

try: import random
except: ...

try: import sys
except: ...

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter.font import Font, families
    import tkinter.messagebox as messagebox
    import tkinter.filedialog as filedialog
    import tkinter.simpledialog as simpledialog
except: ...


# windows.py
try: import ctypes
except: ...

try: import subprocess
except: ...

try:
    import math
    from matplotlib import pyplot
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
except: ...


'''


def getText(file):
    textlines = open(file, 'rb').readlines()

    text = b''
    for line in textlines:
        if line.strip().startswith(b'from '): continue
        elif b'import ' in line: continue
        elif b'__all__ ' in line:
            if not b'\'__all__ ' in line: continue
        text += line
    return text

def write_prmp_gui():
    openfile = open('prmp_modules/prmp_gui.py', 'wb')
    openfile.write(b'__author__ = "PRMP Smart"')
    openfile.write(prmp_gui_imports)

    for file in prmp_gui:
        f = os.path.join(libs[0], file)
        text = getText(f)
        openfile.write(text)

def write_prmp_miscs():
    openfile = open('prmp_modules/prmp_miscs.py', 'wb')
    openfile.write(b'__author__ = "PRMP Smart"')
    openfile.write(prmp_miscs_imports)

    for file in prmp_miscs:
        f = os.path.join(libs[1], file)
        text = getText(f)
        openfile.write(text)

def build():
    imgs = r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM\prmp_lib\prmp_miscs\_prmp_images.py'
    gui = 'prmp_modules/prmp_gui.py'
    miscs = 'prmp_modules/prmp_miscs.py'
    
    from prmp_lib.prmp_miscs.prmp_setup import PRMP_Setup
    files = [miscs]
    files = [gui]
    files = [gui, miscs]
    PRMP_Setup('build_ext', scripts=files).build()



write_prmp_miscs()
write_prmp_gui()
build()
