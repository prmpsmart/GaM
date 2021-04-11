from prmp_lib.prmp_gui import *
from prmp_lib.prmp_gui.image_widgets import *
from prmp_lib.prmp_gui.tushed_widgets import *


class Image_Renamer(Tk):

    def __init__(self, **kwargs):
        super().__init__(containerClass=PRMP_ImageSLabel, containerConfig=dict(anchor='center'), geo=(700, 500), **kwargs)

        self.image = PRMP_ImageSLabel(self.cont, place=dict(relx=0, rely=0, relh=1, relw=.6))
        self.path = ChoosePath(self.cont, place=dict(relx=.65, rely=0, relh=.15, relw=.3))





        self.load()
        self.start()
    
    def load(self):
        size = self.cont.width, self.cont.height
        self.cont.loadImage(r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM\prmp_lib\images_db\images\prmp_jpegs\422138468_50112.jpg', resize=size)
        img = self.cont.image
        self.change2Imgcolor(img)













Image_Renamer(title='Image Renamer')








