from ..core.prmp_gui.core import *


class FramedCanvas(tk.Frame):
    def __init__(self, master, canvasConfig={}, **kwargs):
        super().__init__(master, **kwargs)

        self.canvas = tk.Canvas(self, **canvasConfig)
        self.canvas.place(relx=0.012, rely=0.017, relh=0.966, relw=0.976)

class DC_Digits(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        











