# from Cython.Build import cythonize
from py_libs import py27_dll, py27_include, py37_dll, py37_include, py38_dll, py38_include, py_dir
from os import system, path, chdir, getcwd
from shutil import copy2, move

py = 37
if py == 27:
    py_inc = py27_include
    py_dll = py27_dll
elif py == 37:
    py_inc = py37_include
    py_dll = py37_dll
elif py == 38:
    py_inc = py38_include
    py_dll = py38_dll


py='contrib_app.py'
out='compiled/contrib_app.c'
obj='compiled/contrib_app.o'
pyd='compiled/contrib_app.pyd'
exe='compiled/Contrib_App.exe'


def cmd_cy():
    # system(r'python C:\Users\Administrator\Coding_Projects\PYTHON\Networking\collate.py')
    cmd = f"python -m cython -3 -f --embed=main {py} -o {out}"
    print(cmd)
    system(cmd)

def compile_dll():
    cmd_cy()
    # return
    cmd1 = f"gcc -Wall -g -I{py_inc} -c {out} -o {obj}"
    cmd2 = f"g++ -shared -Wl,--dll {obj} -o {pyd} {py_dll}"
    print(cmd1)
    system(cmd1)
    print(cmd2)
    system(cmd2)

def compile_exe(win=0):
    _exe = r'C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GaM\other_srcs\%s'%exe

    mode = "-mwindows" if win else "-mconsole"

    cmd =  f"g++ -Wall -g -I{py_inc} {mode} {out} {py_dll} -municode -o {_exe}"

    print(cmd)
    system(cmd)

def run(): system(exe)

def exec_exe():
    base = path.basename(exe)
    dest = path.join(py_dir, base)
    try: copy2(exe, dest)
    except Exception as e: print(e)
    chdir(py_dir)
    system(base)
    return
    try: move(dest, path.dirname(exe))
    except Exception as e: print(e)

def pyinstaller(c=0):
    chdir('test')
    ico = ''
    con, win = "--console", "--windowed"
    wh = con if c else win
    levels = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]
    level = f"--log-level {levels[2]}"
    g = '_c' if c else ''
    name = f'--name TranxFer{g}'
    script = 'main.py'
    data = '--add-data prmp_pics;prmp_pics'
    bins = ['contrib_app']
    pyds = ''
    for a in bins: pyds += r' --add-binary C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GaM\other_srcs\%s.pyd;.'%a

    cmd = f"python -m PyInstaller --clean {wh} {level} -D {name} -y {pyds} {data} {script}"
    # cmd = f"python -m PyInstaller -h"

    print(cmd)
    print()
    system(cmd)

def nuitka(win=0):
    dep = "--windows-dependency-tool=pefile"
    wind = "--windows-disable-console"
    o = '-o FileTranxFer.exe'
    cmd = f'python -m nuitka --remove-output --mingw64 --standalone --no-pyi-file --follow-imports {py}'#--plugin-enable=tk-inter
    cmd = 'python -m nuitka -h'
    print(cmd)
    system(cmd)

# compile_dll()
compile_exe(1)

# pyinstaller()

k = r'C:\ProgramData\Anaconda3\PRMP_Apps\Contrib_App.exe'
# k = 'activate'
# system(k)







