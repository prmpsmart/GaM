
__author__ = 'PRMP Smart'
__email1__ = "prmpsmart@gmail.com"
__email2__ = "rockymiracy@gmail.com"

# Essential modules
import string, random, os, glob, sys, platform, threading, subprocess
__file__ = os.path.join(os.getcwd(), 'agam_thrift_all')
sys.argv += [__file__]
# Sorting modules
import time
from datetime import datetime, timedelta
from calendar import day_abbr as DAYS_ABBRS, day_name as DAYS_NAMES, month_abbr as MONTHS_ABBRS, month_name as MONTHS_NAMES, Calendar
# Compressing modules
import hashlib, zlib, base64

# Storage modules
import sqlite3
from xml.etree.ElementTree import ElementTree as ET, ElementPath as EP, Element as E, SubElement as SE
import pickle
from xlsxwriter import Workbook as WORKBOOK

# Dereferencing modules
from weakref import ref
import gc

# GUI modules
from tkinter import Label, Button, Frame, LabelFrame, Radiobutton, Entry, Checkbutton, StringVar, Message, filedialog, messagebox, Tk, Toplevel, Menu, Canvas, colorchooser, Pack, Grid, Place, IntVar
from tkinter.ttk import Combobox, Notebook, Menubutton, Scrollbar, Treeview, Spinbox
from ttkthemes import ThemedStyle
from win32com.client import Dispatch

# Visualisation modules
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot

# Command line tool module 
from argparse import ArgumentParser