import os, sys, subprocess

class Reloader:
    def runner(self):
        args, env = [sys.executable] + sys.argv,  os.environ
        env["PRMP_TK"] = "RUNNING"
        while True:
            exit_code = subprocess.call(args, env=env, close_fds=False)
            if exit_code != 63: return exit_code
    def reloader(self, e=None):
        try: os.system("cls")
        except: os.system("clear")
        print("Reloading")
        sys.exit(63)
    def reload(self, func):
        try:
            if os.environ.get("PRMP_TK") == "RUNNING": func()
            else: sys.exit(self.runner())
        except Exception as E: pass


