from prmp_gifs import *
from prmp_pngs import *
from prmp_xbms import *

glo = globals().copy()
keys = list(a for a in glo.keys() if '__' not in a)
keys.sort()

file = 'prmp_images.py'

opn = open(file, 'w')


for g in keys:
    v = glo[g]
    if isinstance(v, bytes):
        strf = f"{g} = {v} \n\n"
        opn.write(strf)

for g in keys:
    v = glo[g]
    if isinstance(v, dict):
        dic_str = '{'
        for k in v: dic_str += f"'{k}': {k}, "

        dic_str = dic_str[:-2]
        dic_str += '}'
        
        fin = f"{g} = {dic_str}\n\n"
        opn.write(fin)







opn.close()


