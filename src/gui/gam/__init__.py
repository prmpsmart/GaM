from prmp_lib.prmp_gui import PRMP_Window
import os

join = os.path.join
_dir = os.path.dirname(__file__)
imgs = join(_dir, 'imgs')
# PRMP_Window.PRMPICON = join(imgs, 'gam.png')
# PRMP_Window.TKICON = join(imgs, 'gam.ico')
PRMP_Window.PRMPICON = join(imgs, 'nairabag.png')
PRMP_Window.TKICON = join(imgs, 'nairabag.ico')