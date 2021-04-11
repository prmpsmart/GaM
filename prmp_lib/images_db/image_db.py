import os
cwd = os.getcwd()


def save_PRMP_Images():
    from prmp_lib.prmp_miscs.prmp_images import PRMP_ImageFile, PRMP_ImageType, PRMP_Images, PRMP_IMAGES
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



### dones

# logo
# frames
# prmps




format_dir_pix_names()




