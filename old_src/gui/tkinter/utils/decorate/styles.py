from .colours import Colours, Fonts
# from ttkthemes import ThemedStyle
from ..widgets.admin_req import make_change
from tkinter.ttk import Style
ThemedStyle = Style

all_themes = ["alt", "aquativo", "arc", "black", "blue", "clam", "classic", "clearlooks", "default", "elegance","itft1", "keramik", "kroc", "plastik", "radiance", "scidblue", "scidgreen", "scidgrey", "scidmint", "scidpink", "scidpurple", "scidsand", "smog", "ubuntu", "vista", "winnative", "winxpblue", "xpnative", "equilux", "breeze"]

class Styles(ThemedStyle):
    geometry = "1500x780+45+40"
    short_geo = "600x700"
    password = "d3cd7fdbcfec731019d16678a16e6c83e70ba7952f32221ced7765bc"

    themes = ["black", "blue", "kroc", "smog", "ubuntu"]
    themes = all_themes

    style = "blue"

    chart                = "white"

    higbg                = "blue"
    higfg                = "white"
    background           = "#9a80bb"
    foreground           = "black"

    showbg              = "white"
    showfg              = "black"
    showred             = "red"

    font                = Fonts.font11b

    @classmethod
    def change(cls, theme):

        cls.style = theme

        if theme == "ubuntu":
            cls.higbg                = "blue"
            cls.higfg                = "white"
            cls.background           = "#c9c1bc"
            cls.foreground           = "black"

        elif theme == "black":
            cls.higbg                = "blue"
            cls.higfg                = "white"
            cls.background           = "#424242"
            cls.foreground           = "white"

        elif theme == "blue":
            cls.higbg                = "blue"
            cls.higfg                = "white"
            cls.background           = "#6699cc"
            cls.foreground           = "black"

        elif theme == "kroc":
            cls.higbg                = "blue"
            cls.higfg                = "white"
            cls.background           = "#fcb64f"
            cls.foreground           = "black"

        elif theme == "smog":
            cls.higbg                = "blue"
            cls.higfg                = "white"
            cls.background           = "#e7eaf0"
            cls.foreground           = "black"

    def __init__(self, master=None, theme='', chart=''):
        if theme: self.style = theme
        if chart: self.chart = chart

        if master:
            super().__init__(master)

            if theme: self.change_style(theme)


    def change_style(self, theme, func=None):
        Styles.change(theme)
        # self.theme_use(theme)
        self.map("TCheckbutton", foreground=[("pressed", "red"), ("active", "blue")], background=[("pressed", "!disabled", "black"), ("active", "white")])
        self.changeit_theme(theme)
        if func: make_change(func)

    def changeit_theme(self, theme):
        if theme == "clam":
            self.configure(".", background="#3c7333")

    @classmethod
    def get_state(cls): return cls(theme=cls.style, chart=cls.chart)
    @classmethod
    def load_state(cls, imageobj):
        if isinstance(imageobj, cls):

            cls.change(imageobj.style)
            cls.chart = imageobj.chart

    def set_default(self):
        return
        self.theme_use(self.style)





