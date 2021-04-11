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
    os.chdir('images')
    dirs = ['Backgrounds', 'Buttons', 'Currencies', 'Earthquakes', 'files_icons', 'gtk', 'Logos', 'prmp_gifs', 'prmp_pngs', 'prmp_xbms', 'socials', 'soft_scraps', 'sphinx']



format_dir_pix_names()




