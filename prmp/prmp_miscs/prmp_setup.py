from distutils.core import setup
from Cython.Build import cythonize
from os import mkdir, path, listdir, sys, chdir
from platform import python_version

py_ver = python_version()[:3].replace('.', '')
python = r'C:/Users/Administrator/AppData/Local/Programs/Python/Python%s/python.exe'%py_ver

classifiers = [
    'Development Status :: 1 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Python Software Foundation License',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
    'Programming Language :: C/C++',
    'Topic :: Software Development :: Bug Tracking',
]
platforms = ['Windows']
keywords = []
license_ = ''




class PRMP_Setup:
    def __init__(self, folder='', scripts=[], description='', meta_datas={}, classifiers=classifiers, platforms=platforms, keywords=[], license=''):

        pac = folder[:-3] if folder.endswith('.py') else folder

        self.meta_datas = meta_datas or dict(
            name=pac,
            version='1.0',
            author='PRMPSmart',
            author_email='prmpsmart@gmail.com',
            maintainer='PRMPSmart',
            maintainer_email='prmpsmart@gmail.com',
            url=f'github.com/prmpsmart/{pac}',
            description=description or f'an extension module for {folder}',
            long_description='an example to test the creation of python extension modules et all.',
            download_url=f'github.com/prmpsmart/{pac}.git',
            classifiers=classifiers,
            platforms=platforms,
            keywords=keywords,
            license=license_,
        )
        self.scripts, self.dest = scripts or self.get_scripts(folder)

    def get_scripts(self, folder):
        files = []
        if path.isdir(folder):
            for fi in listdir(folder):
                p = path.join(folder, fi)
                if path.isfile(p): files.append(p)
            return files, f'/{folder}'
        else: return [folder], ''

    def build_ext(self):
        for d in ['c', 'pyd']:
            try: mkdir(d)
            except: pass
        ext_modules = cythonize(self.scripts, language_level=3, build_dir='c')
        sys.argv.extend(['build_ext', f'-bpyd{self.dest}'])
        setup(ext_modules=ext_modules, **self.meta_datas)



if __name__ == '__main__':
    argv = sys.argv
    if len(argv) > 1:
        folder = argv[1]
        del argv[1]
    else: folder = 'test'
    PRMP_Setup(folder).build_ext()
