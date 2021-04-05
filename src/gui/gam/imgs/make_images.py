from prmp.prmp_miscs.prmp_pics import PRMP_Images
import os

d = os.path.dirname(__file__)
p = os.path.join(d, 'gam_images.py')

PRMP_Images.images_into_py(os.path.dirname(__file__), p, add_all=1, prefix='GaM')





