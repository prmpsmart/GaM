
from prmp_gui.dialogs import PRMP_ImageDialog

class Photos:
    pass

class PhotoViewer(PRMP_ImageDialog):

    def __init__(self, title='', **kwargs):
        super().__init__(title=title, **kwargs)




PV = PhotoViewer


PV()

