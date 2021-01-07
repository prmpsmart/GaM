from os import listdir, path, chdir
from base64 import b64encode, b64decode

def makeImage(cat):
    _dir_ = dir_ = f'prmp_{cat}s'
    print(listdir(dir_))

    file = f'{_dir_}.py'
    di = r'C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\Test_GUI\Test_Gui\PySimpleGUI-master\GIFs'
    if cat == 'gif': dir_ = di
    
    opn = open(file, 'w')
    # return

    names = {path.splitext(v)[0].replace('-', '_'): v for v in listdir(dir_)}
    lnames = list(names.keys())
    files = [path.join(dir_, f) for f in listdir(dir_)]

    chdir(dir_)


    for name, file in names.items():
        data = open(file, 'rb').read()
        enc  = b64encode(data)
        strf = f"{name} = {enc} \n\n"
        opn.write(strf)

    img = ', '.join(lnames)


    dic_str = '{'
    for k in lnames:
        dic_str += f"'{k}': {k}, "

    dic_str = dic_str[:-2]
    dic_str += '}'


    dir_ = _dir_
    fin = f"{dir_.upper()} = {dic_str}\n\n"
    opn.write(fin)



    opn.close()


cats = 'xbm', 'gif', 'png'
cats = 'xbm', 'png'

for cat in cats: makeImage(cat)



