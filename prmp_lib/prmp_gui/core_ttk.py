from .core import *

__all__ = ['PRMP_Style', 'PRMP_Style_Button', 'PRMP_Style_Checkbutton', 'PRMP_Style_Entry', 'PRMP_Style_Frame', 'PRMP_Style_Label', 'PRMP_Style_LabelFrame', 'PRMP_Menubutton', 'PRMP_Style_OptionMenu', 'PRMP_Style_PanedWindow', 'PRMP_Style_Radiobutton', 'PRMP_Style_Scale', 'PRMP_Style_Scrollbar', 'PRMP_Style_Spinbox', 'PRMP_Combobox', 'PRMP_LabeledScale', 'PRMP_Notebook', 'PRMP_Progressbar', 'PRMP_Separator', 'PRMP_Sizegrip', 'PRMP_Treeview', 'SButton', 'SCheckbutton', 'SEntry', 'SFrame', 'SLabel', 'SLabelFrame', 'SOptionMenu', 'SPanedWindow', 'SRadiobutton', 'SScale', 'SScrollbar', 'SSpinbox', 'Combobox', 'LabeledScale', 'Notebook', 'Progressbar', 'Separator', 'Sizegrip', 'Treeview', 'Menubutton', 'ttk']

class PRMP_Style_(PRMP_Widget):

    def __init__(self, highlightable=False, **kwargs):
        super().__init__(_ttk_=True, highlightable=highlightable, **kwargs)

    @property
    def style(self): return PRMP_Window.STYLE
PS_ = PRMP_Style_

#   from ttk widgets --> PRMP_Style_

class PRMP_Style(ttk.Style, PRMP_Mixins):
    LOADED = False
    PRMP_Window = None

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
            'buttons.TButton': {
                'map': {
                    'relief': [('hover', 'solid')],
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
        
        if not PRMP_Style.PRMP_Window:
            from .windows import PRMP_Window
            PRMP_Style.PRMP_Window = PRMP_Window

        if PRMP_Style.PRMP_Window: PRMP_Style.PRMP_Window.TOPEST.event_generate('<<PRMP_STYLE_CHANGED>>')
        return _settings

    def update(self, event=None):
        if not PRMP_Style.LOADED: self.createPrmp()
        self.theme_settings('prmp', self.settings)
Style = PSt = PRMP_Style

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
        PRMP_Style_.__init__(self, master=master, config=config, nonText=True, **kwargs)
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

class PRMP_Menubutton(PRMP_Style_, ttk.Menubutton):
    TkClass = ttk.Menubutton

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master, config=config, **kwargs)
Menubutton = PM = PRMP_Menubutton

class PRMP_Style_OptionMenu(PRMP_Style_, ttk.OptionMenu):
    TkClass = ttk.OptionMenu

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master, config=config, **kwargs)
SOptionMenu = PSO = PRMP_Style_OptionMenu

class PRMP_Style_PanedWindow(PRMP_Style_, ttk.PanedWindow):
    TkClass = ttk.PanedWindow

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master, config=config, **kwargs)
SPanedWindow = PSP = PRMP_Style_PanedWindow

class PRMP_Style_Radiobutton(PRMP_InputButtons, PRMP_Style_, ttk.Radiobutton):
    TkClass = ttk.Radiobutton

    def __init__(self, master=None, asLabel=False, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master,asLabel=asLabel, config=config, **kwargs)
SRadiobutton = PSR = PRMP_Style_Radiobutton

class PRMP_Style_Scale(PRMP_Style_, ttk.Scale):
    TkClass = ttk.Scale

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master, config=config, **kwargs)
SScale = PSS = PRMP_Style_Scale

class PRMP_Style_Scrollbar(PRMP_Style_, ttk.Scrollbar):
    TkClass = ttk.Scrollbar

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master, config=config, **kwargs)

    def set(self, first, last): return ttk.Scrollbar.set(self, first, last)
SScrollbar = PSSc = PRMP_Style_Scrollbar

class PRMP_Style_Spinbox(PRMP_Input, PRMP_Style_, ttk.Spinbox):
    TkClass = ttk.Spinbox

    def __init__(self, master=None, config={}, **kwargs):
        PRMP_Style_.__init__(self, master=master, config=config, **kwargs)
        PRMP_Input.__init__(self, **kwargs)


SSpinbox = PSSp = PRMP_Style_Spinbox

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
