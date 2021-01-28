from os import listdir, path, chdir, getcwd
from base64 import b64encode, b64decode
from prmp_miscs.prmp_pics import PRMP_ImageType

cwd = getcwd()


def makeImage(cat):
    _dir_ = dir_ = '.'
    

    file = 'gam_images.py'
    
    opn = open(file, 'w')
    # return

    names = {path.splitext(v)[0].replace('-', '_'): v for v in listdir(dir_) if PRMP_ImageType.get(v)}
    lnames = list(names.keys())
    files = [path.join(dir_, f) for f in listdir(dir_)]

    # chdir(dir_)

    for name, file in names.items():
        data = open(file, 'rb').read()
        enc  = b64encode(data)
        strf = f"{name} = {enc} \n\n"
        opn.write(strf)
    
    chdir(cwd)

    img = ', '.join(lnames)


    dic_str = '{'
    for k in lnames:
        dic_str += f"'{k}': {k}, "

    dic_str = dic_str[:-2]
    dic_str += '}'


    dir_ = 'gam_pngs'
    # dir_ = 'gam_icos'
    fin = f"{dir_.upper()} = {dic_str}\n\n"
    opn.write(fin)



    opn.close()


cats = 'ico', 'png'
# cats = 'xbm', 'png'

makeImage(cats[1])



