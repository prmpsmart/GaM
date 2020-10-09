
from PIL import Image, ImageTk
from ......backend.utils.data.images.images import Images
from .img_tk import Img_Tk

class Images_Tk:
    
    @classmethod
    def convert2photo(cls, image):
        img = Image.open(image)
        size = img.size
        ph_img = ImageTk.PhotoImage(img)
        img_tk = Img_Tk(ph_img, size)
        return img_tk
    
    @classmethod
    def agam(cls):
        ag = Images.agam()
        co_ag = cls.convert2photo(ag)
        return co_ag
    @classmethod
    def login(cls):
        lo = Images.login()
        co_lo = cls.convert2photo(lo)
        return co_lo
    @classmethod
    def app(cls):
        ap = Images.app()
        co_ap = cls.convert2photo(ap)
        return co_ap
    @classmethod
    def ico(cls): return Images.ico()

    @classmethod
    def get_agam(cls, char):
        ag = Images.get_agam(char)
        co_ag = cls.convert2photo(ag)
        return co_ag
    @classmethod
    def get_login(cls, char):
        lo = Images.get_login(char)
        co_lo = cls.convert2photo(lo)
        return co_lo
    @classmethod
    def get_app(cls, char):
        ap = Images.get_app(char)
        co_ap = cls.convert2photo(ap)
        return co_ap
    @classmethod
    def get_ico(cls, char): return Images.get_ico(char)
    


