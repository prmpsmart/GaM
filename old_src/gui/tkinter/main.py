from argparse import ArgumentParser
from src.backend.utils.data.tdata import Authorisation, Path
import os, zlib, sys
from src.gui.tkinter.thrift_note import Thrift
from src.gui.tkinter.utils.start_gui import Gui

def main():
    arrd = sys.argv
    # sys.argv = arrd[1:]
    parser = ArgumentParser(description="AGAM ANALYSIS SOFTWARE", epilog="By PRMP Smart prmpsmart@gmail.com")
    if os.environ.get("PRMP_TK") == "RUNNING":  parser.add_argument("prmp")
    # parser.add_argument("turna")
    # parser.add_argument("--turnaround")
    parser.add_argument("-u", "--username", type=str, dest="username", help="Username")
    parser.add_argument("-p", "--password", type=str, dest="password", help="Password")
    parser.add_argument("-d", "--debug", action="store_true", help="Show Debug")
    parser.add_argument("-v", "--version", action="version", version="Version = 2.0.2")


    args = parser.parse_args()
    username = args.username
    password = args.password
    
    sys.argv = arrd

    err = "Both Username and Password is neaded.\nTry the -h/--help for more details."
    if username and password:
        result = Authorisation.login_cmd(username, password)
        args.password = zlib.compress(Authorisation._Auths_Vars__hashit(Path.tempfile().encode()).encode())
        if args.debug: print(result)
        sys.exit(Gui(Thrift, 1))
    elif username and not password:
        if args.debug: print(err)
    elif not username and password:
        args.password = zlib.compress(Authorisation._Auths_Vars__hashit(Path.tempfile().encode()).encode())
        if args.debug: print(err)
    else:
        if args.debug: print(args)
        sys.exit(Gui(Thrift, 1))
    print(args)

if __name__ == "__main__": main()
#