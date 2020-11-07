from .bases import *



class PRMP_Style(ttk.Style):
    loaded = False
    ttkthemes = ("black", "blue", 'prmp')
    ttkstyles = ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')


    def __init__(self, master=None):
        super().__init__(master=master)
        if not PRMP_Style.loaded: self.createPrmp()
    
    def tupledFont(self, fontDict):
        options = []
        for k, v in fontDict.items():
            options.append("-"+k)
            options.append(str(v))
        return tuple(options)
    
    def theme_use(self, theme):
        if theme in self.ttkthemes:
            if theme not in self.loadedThemes: getattr(self, 'create' + theme.title())()
            pass

        PRMP_Style.CURRENTSTYLE = theme
        super().theme_use(theme)
    
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
    
    def createBlue(self):
        PRMP_Style.loadedThemes.append('blue')
        
        frame = "#6699cc"
        lighter = "#bcd2e8"
        window = "#e6f3ff"
        # window = "red"
        selectbg = "#2d2d66"
        # selectbg = "blue"
        selectfg = "#ffffff"
        selectfg = "yellow"
        disabledfg = "#666666"

        imagesDict = self.styleImages('blue')
        
        # return
        settings = {
            '.': {
                'configure': {
                    'borderwidth': 1,
                    'background': frame,
                    'fieldbackground': window,
                    'troughcolor': lighter,
                    'selectbackground': selectbg,
                    'selectforeground': selectfg
                },
                'map': {
                    'foreground': [
                        ('disabled', disabledfg)
                    ]
                }
            },
            'TButton': {
                'configure': {
                    'padding': (10, 0),
                },
                'layout': [
                    ('Button.button', {'children': [
                        ('Button.focus', {'children': [
                            ('Button.padding', {'children': [
                                ('Button.label', None)
                            ]})
                        ]})
                    ]})
                ],
            },
            'button': {
                'element create': ['image', imagesDict['button-n'], ('pressed', imagesDict['button-p']), ('active', imagesDict['button-h']), {'border': 4, 'sticky': 'ew'}]
            },
            'Checkbutton.indicator': {
                'element create': ['image', imagesDict['check-nu'], 
                    (('active', '!disabled', 'selected'), imagesDict['check-hc']), 
                    (('active', '!disabled'), imagesDict['check-hu']), 
                    (('selected', '!disabled'), imagesDict['check-nc']), {'width': 24, 'sticky': 'w'}]
            },
            'Radiobutton.indicator': {
                'element create': ['image', imagesDict['radio-nu'], 
                    (('active', '!disabled', 'selected'), imagesDict['radio-hc']), 
                    (('active', '!disabled'), imagesDict['radio-hu']), 
                    ('selected', imagesDict['radio-nc']), {'width': 24, 'sticky': 'w'}]
            },
            'TMenubutton': {
                'configure': {
                    'relief': 'raised',
                    'padding': (10, 2)
                },
            },
            'Toolbar': {
                'configure': {
                    'width': 0,
                    'relief': 'flat',
                    'borderwidth': 2,
                    'padding': 4,
                    'background': frame,
                    'foreground': '#000000'
                },
                'map': {
                    'background': [
                        ('active', selectbg)
                    ],
                    'foreground': [
                        ('active', selectfg)
                    ],
                    'relief': [
                        ('disabled', 'flat'), 
                        ('selected', 'sunken'), 
                        ('pressed', 'sunken'), 
                        ('active', 'raised')
                    ]
                }
            },
            'TEntry': {
                'configure': {
                    'selectborderwidth': 1,
                    'padding': 2,
                    'insertwidth': 2,
                    'font': 'TkTextFont'
                }
            },
            'TCombobox': {
                'configure': {
                    'selectborderwidth': 1,
                    'padding': 2,
                    'insertwidth': 2,
                    'font': 'TkTextFont'
                }
            },
            'TNotebook.Tab': {
                'configure': {
                    'padding': (4, 2, 4, 2)
                },
                'map': {
                    'background': [
                        ('selected', frame),
                        ('active', lighter)
                    ],
                    'padding': [
                        ('selected', (4, 4, 4, 2))
                    ]
                }
            },
            'TLabel': {
                'configure': {
                    'relief': 'solid',
                    'anchor': 'center',
                    'font': "-family {Times New Roman} -size 11 -weight bold"
                },
                'map': {
                    'relief': [('!active', 'solid'), ('disabled', 'ridge')],
                    'foreground': [('!disabled', 'black')],
                    # 'padding':
                }
            },
            'TLabelframe': {
                'configure': {
                    'borderwidth': 2,
                    'relief': 'groove'
                }
            },
            'Vertical.TScrollbar': {
                'layout': [
                    ('Scrollbar.trough', {'children': [
                        ('Scrollbar.uparrow', {'side': 'top'}),
                        ('Scrollbar.downarrow', {'side': 'bottom'}),
                        ('Scrollbar.uparrow', {'side': 'bottom'}),
                        ('Vertical.Scrollbar.thumb', {'side': 'left', 'expand': 'true', 'sticky': 'ns'})
                    ]})
                ]
            },
            'Horizontal.TScrollbar': {
                'layout': [
                    ('Scrollbar.trough', {'children': [
                        ('Scrollbar.leftarrow', {'side': 'left'}),
                        ('Scrollbar.rightarrow', {'side': 'right'}),
                        ('Scrollbar.leftarrow', {'side': 'right'}),
                        ('Horizontal.Scrollbar.thumb', {'side': 'left', 'expand': 'true', 'sticky': 'we'})
                    ]})
                ]
            },
            'Horizontal.Scrollbar.thumb': {
                'element create': ['image', imagesDict['sb-thumb'], (('pressed', '!disabled'), imagesDict['sb-thumb-p']), {'border': 3}]
            },
            'Vertical.Scrollbar.thumb': {
                'element create': ['image', imagesDict['sb-vthumb'], (('pressed', '!disabled'), imagesDict['sb-vthumb-p']), {'border': 3}]
            },
            # element create 133
            # last for loop
            # element create 138
            'Scale.slider': {
                'element create': ['image', imagesDict['slider'], (('pressed', '!disabled'), imagesDict['slider-p'])]
            },
            'Vertical.Scale.slider': {
                'element create': ['image', imagesDict['vslider'], (('pressed', '!disabled'), imagesDict['vslider-p'])]
            },
            'Horizontal.Progress.bar': {
                'element create': ['image', imagesDict['sb-thumb'], {'border': 2}]
            },
            
            'Vertical.Progress.bar': {
                'element create': ['image', imagesDict['sb-vthumb'], {'border': 2}]
            },
            'Treeview': {
                'map': {
                    'background': [
                        ('selected', selectbg)
                    ],
                    'foreground': [
                        ('selected', selectfg)
                    ]
                }
            }
        }
        
        for sd in ['up', 'down', 'left', 'right']:
            settings.update({f'{sd}arrow': {
                'element create': ['image', imagesDict[f'arrow{sd}'], ('disabled', imagesDict[f'arrow{sd}']), ('pressed', imagesDict[f'arrow{sd}-p']), ('active', imagesDict[f'arrow{sd}-h']), {'border': 1, 'sticky': ()}]}})
        
        # s = sfs(settings)
        
        self.theme_create('blue', settings=settings)
        return self

    def createPrmp(self):
        if PRMP_Style.loaded: return
        self.theme_create('prmp', settings=self.settings)
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

        default_font = self.tupledFont(PRMP_Theme.DEFAULT_FONT)
        big_font = self.tupledFont(PRMP_Theme.BIG_FONT)
        menu_font = self.tupledFont(PRMP_Theme.DEFAULT_MENU_FONT)
        button_font = self.tupledFont(PRMP_Theme.DEFAULT_BUTTON_FONT)
        small_button_font = self.tupledFont(PRMP_Theme.DEFAULT_SMALL_BUTTON_FONT)
        title_font = self.tupledFont(PRMP_Theme.DEFAULT_TITLE_FONT)
        status_font = self.tupledFont(PRMP_Theme.DEFAULT_STATUS_FONT)
        label_font = self.tupledFont(PRMP_Theme.DEFAULT_LABEL_FONT)
        labelframe_font = self.tupledFont(PRMP_Theme.DEFAULT_LABELFRAME_FONT)

        oneColor = True

        if isinstance(button_color, tuple): button_foreground, button_background = button_color
        else:
            background, foreground = 'white', 'black'
            button_foreground, button_background = foreground, background
        
        _settings = {
            '.': {
                'map': {
                    'anchor': [('hover', 'nw')]
                }

            },

            'TButton': {
                'configure': {
                    'relief': 'raised',
                    'anchor': 'center',
                    'font': button_font,
                    'foreground': button_foreground,
                    'background': button_background
                },
               'map': {
                    'relief': [('pressed', 'solid'), ('hover', 'ridge'), ('focus', 'solid')],
                    'foreground': [('disabled', 'black')],
                },
            },
            
            'TLabel': {
                'configure': {
                    'relief': 'groove',
                    'anchor': 'center',
                    'font': label_font,
                    'foreground': foreground,
                    'background': background,
                },
                'map': {
                    'relief': [('active', 'groove'), ('disabled', 'ridge'), ('hover', 'ridge'),],
                }
            },
            'entry.TLabel': {
                'configure': {
                    'relief': 'sunken',
                    'background': text_background,
                    'foreground': text_foreground,
                    'overrelief': 'solid',
                    'font': default_font
                },
                'map': {
                    'relief': [('hover', 'solid')],
                }
            },
        }

        return _settings

    def update(self, e=0):
        if not PRMP_Style.loaded: self.createPrmp()
        self.theme_settings('prmp', self.settings)
    theme_use = update

PSt = PRMP_Style



