from . import *
# from .dialogs import *
from .tushed_widgets import *


class PRMP_SolidScreen(PRMP_MainWindow):
    def __init__(self, side='top-center', gaw=1, bd=12, geo=(),**kwargs):
        super().__init__(tm=1, gaw=gaw, geo=geo or (500, 500), side=side, **kwargs)

        self.container.configure(borderwidth=bd)

        self.paint()

SS = PRMP_SolidScreen

