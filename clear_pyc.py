
import argparse, os, zipfile
def clear_pyc(path=''):
    path = os.path.abspath(path)
    print(f'Deleting ".pyc" files in --> "{path}"')
    # return
    for r, t, f in os.walk(path):
        for o in f:
            if o.endswith('pyc'):
                p = os.path.join(r, o)
                print(p)
                os.remove(p)


def main():

    parser = argparse.ArgumentParser(prog='clear_pyc.exe', description="Clearing of all .pyc files in this folder.", epilog="By PRMP Smart prmpsmart@gmail.com", exit_on_error=False)

    parser.add_argument("path", nargs='?', type=str, help="path to delete .pyc files", default='.')
    parser.add_argument("-v", "--version", action="version", version="Version = 1.0.0")

    args = parser.parse_args()
    path = args.path
    clear_pyc(path)

# if __name__ == '__main__': main()

# os.system(r'C:\Users\Administrator\Desktop\Clear_pyc C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM')
# 
# g = ['1', '2', '3', '4', 5]

# g.remove(5)
# print(g)
clear_pyc()

