import os

root = r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM\src\backend'
_libs = ['core', 'dc', 'office']
join = lambda p: os.path.join(root, p)
libs = [join(a) for a in _libs]

d_libs = dict(zip(_libs, libs))

core = ['errors.py', 'mixins.py', 'bases.py', 'records.py', 'records_managers.py', 'accounts.py', 'regions.py', 'regions_managers.py']

dc = ['dc_errors.py', 'dc_sorts.py', 'dc_records.py', 'dc_records_managers.py', 'dc_accounts.py', 'dc_specials.py']

office = ['office_accounts.py', 'office_regions.py']



core_imports = b'''
from prmp_miscs import *
import time, hashlib, datetime

'''

dc_imports = b'''
from core import *

'''

office_imports = b'''
from core import RegionsManager, Region, Person, PersonsManager, AccountsManager
from dc import AreasManager, AreaAccount, AreaAccountsManager
from prmp_miscs import PRMP_StrMixins

'''

def getText(file):
    textlines = open(file, 'rb').readlines()

    text = b''
    for line in textlines:
        if b'from ' in line: continue
        elif b'import ' in line: continue
        elif b'__all__ ' in line:
            if not b'\'__all__ ' in line: continue
        text += line
    return text

def write_backend(folder):
    glob = globals()

    openfile = open(f'modules/{folder}.py', 'wb')
    openfile.write(b'__author__ = "PRMP Smart"')
    openfile.write(glob[f'{folder}_imports'])

    for file in glob[folder]:
        f = os.path.join(d_libs[folder], file)
        text = getText(f)
        openfile.write(text)





# for l in _libs: write_backend(l)
# write_backend(_libs[-1])

from modules.prmp_miscs import PRMP_Setup as ps
p = ps('build_ext', scripts=[f'modules/{l}.py' for l in _libs])

p.build()
