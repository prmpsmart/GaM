from prmp_lib.prmp_miscs.prmp_images import *
import os
cwd = os.getcwd()

def rename_prmp_jpegs():
    dd = r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\Images\prmp_jpgs'
    for file in os.listdir(dd):
        new = 'wall_' + file
        file = os.path.join(dd, file)
        new = os.path.join(dd, new)
        os.rename(file, new)


def zippiin():
    from prmp_lib.prmp_miscs.prmp_exts import zipPath

    s = 'prmp_gui'
    f = r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM\prmp_lib\%s'%s
    # f = r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM\other_srcs'

    zipPath(f, 'zips', excludes=['prmp_db', '.pyc'], quiet=1, latest=1)


def save_PRMP_Images():
    for img_ext in PRMP_IMAGES:
        for name, data in img_ext.items():
            file = PRMP_ImageFile(name, b64=data)
            ext = file.ext
            os.chdir(ext+'s')
            file.save(f'{name}.{ext}')
            os.chdir(cwd)


def format_dir_pix_names():
    os.chdir('images/soft_scraps')
    dirs = os.listdir()

    # dirs = [p for p in dirs if not  os.path.splitext(p)[0].isalpha()]
    print(len(dirs))
    
    dis = [p.replace('-01', '').replace('-', '_').replace(' ', '_').lower() for p in dirs]
    gg = {}
    for a in dis:
        if a in gg: gg[a] += 1
        else: gg[a] = 1
    dis = [(p, p.replace('-01', '').replace('-', '_').replace(' ', '_').lower()) for p in dirs]
    
    # for a, b in dis: os.rename(a, b)
    
    print(len(list(gg.values())))


def run(size, files):
    res = [PRMP_Image(a, thumb=size) for a in files]
    for f in res: PRMP_ImageFile(f'{f.name}.{f.ext}', image=f.image).save()


def changeImageSizes():
    from threading import Thread
    os.chdir('images/prmp_jpegs')
    files = [f'raw/{a}' for a in os.listdir('raw')]
    print(len(files))
    size = 256, 256
    fol = '%dx%d'%size
    size = 1024, 1024
    try: os.mkdir(fol)
    except: print(fol,'already exists.')

    files = [PRMP_ImageFile(a) for a in files]
    f1 = files[:19], files[19:38], files[38:57]
    os.chdir(fol)

    for a in f1: Thread(target=run, args=[size, a]).start()

    # d = [(a.ext, a.image.size, a.ext) for a in f1[0]]
    # print(d)

    # j = files[0]
    # print(j.ext)
    # print(j.data[:10])
    # print(j.ext)
    # print(j.ext)
    # print(j.ext)
    # print(j.ext)


zippiin()


# img = PRMP_DB.getImage('prmp_jpgs', 'orange_lux')[0]


# print(type(img))





