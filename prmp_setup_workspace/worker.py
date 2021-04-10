from prmp_lib.prmp_miscs.prmp_images import *
# print(dir())

dd = [PRMP_JPEGS, PRMP_PNGS, PRMP_XBMS, PRMP_GIFS]
m = [a.replace('PRMP_', '').replace('S', '').lower() for a in ['PRMP_JPEGS', 'PRMP_PNGS', 'PRMP_XBMS', 'PRMP_GIFS']]

dic = dict(zip(m, dd))

PRMP_Images.images_into_py(merge=dic, space=3, add_all=1)
# print(m)

