#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.25.1
#  in conjunction with Tcl version 8.6
#    Dec 01, 2020 03:30:42 AM WAT  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import sort_search_support

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = Toplevel1 (root)
    sort_search_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    top = Toplevel1 (w)
    sort_search_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#800080'  # Closest X11 color: 'magenta4'
        _fgcolor = '#ffffff'  # X11 color: 'white'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

        top.geometry("600x450")
        top.title("New Toplevel")
        top.configure(background="#800080")

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.033, rely=0.067, relheight=0.9
                , relwidth=0.933)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(font="-family {Times New Roman} -size 11 -weight bold")
        self.Labelframe1.configure(foreground="black")
        self.Labelframe1.configure(text='''Sort and Search''')
        self.Labelframe1.configure(background="#800080")

if __name__ == '__main__':
    vp_start_gui()




