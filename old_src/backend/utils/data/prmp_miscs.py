
import sys, os, zlib, argparse

def not_exist(file): print("%s doesn't exist"%file)

def exist(file):
    if os.path.isfile(file): return True
    else:
        file_path = os.path.join(os.getcwd(), file)
        print(file_path)
        return os.path.isfile(file_path)

def com(file, out=None):
    try:
        if exist(file):
            if not out: out = file+".comp"
            real = open(file, "rb").read()
            com_ed = zlib.compress(real)
            open(out, "wb").write(com_ed)
            return out
        else: not_exist(file)
    except: print("Cannot be Compressed")

def decom(file, out=None):
    try:
        if exist(file):
            if not out:
                if file.endswith(".comp"): out = file[:-5]
                else: out = file+".decomp"
            real = open(file, "rb").read()
            decom_ed =  zlib.decompress(real)
            open(out, "wb").write(decom_ed)
            return out
        else: not_exist(file)
    except: print("Cannot be Decompressed")

def start():
    parser = argparse.ArgumentParser(description="Compressing and Decompressing file, default is compressing file", epilog="By PRMP Smart prmpsmart@gmail.com")
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument("-d", "--decompress", action="store_true", help="To decompress file")
    group1.add_argument("-c", "--compress", action="store_true", help="To compress file")
    group1.add_argument("-r", "--remove", action="store_true", help="Remove file")
    
    group2 = parser.add_mutually_exclusive_group()
    group2.add_argument("-o", "--outfile", type=str, dest="outfile", help="Output File")
    group2.add_argument("-u", "--use", action="store_true", help="To overwrite the old file")
    
    parser.add_argument("-v", "--version", action="version", version="Version = 0.1")
    parser.add_argument("-f", "--file", type=str, dest="file", help="File to be worked on", required=True)

    args = parser.parse_args()
    file = args.file.strip()
    if args.os.remove:
        if exist(file): os.remove(file)
        else: not_exist(file)

    elif args.decompress or args.compress:
        if args.decompress: func = decom
        elif args.compress: func = com
        
        if args.use: out = file
        else: out = args.outfile
        args.outfile = func(file, out)

    print(args)

