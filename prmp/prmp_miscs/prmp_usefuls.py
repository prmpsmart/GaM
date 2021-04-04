import os, zipfile, subprocess

def zipPath(resource, destination='', latest=False, quiet=0):
    # Create name of new zip file, based on original folder or file name
    resource = resource.rstrip('\\').rstrip('/')
    # if resource in destination: TranxFerLogger.warning('Loop: Save somewhere else!')
    
    if not os.path.exists(resource): return
    
    if destination:
        if os.path.isdir(destination):
            baseFileName = os.path.basename(resource) + '.zip'
            zipFileName = os.path.join(destination, baseFileName)
        else: zipFileName = destination

    else: zipFileName = resource + '.zip'
    
    if os.path.isdir(resource): zipRootDir = os.path.basename(resource)
    
    if (os.path.isfile(zipFileName) == True) and (latest == False): return zipFileName
    
    # Create zip file
    with zipfile.ZipFile(zipFileName, "w", compression=zipfile.ZIP_DEFLATED) as zipFile:
        if os.path.isdir(resource):
            for root, dirs, files in os.walk(resource):
               for file in files:
                   filename = os.path.join(root, file)
                   arc = root.replace(resource, zipRootDir)
                   arcname = os.path.join(arc, file)
                   if not quiet: print('adding %s'%filename)
                   zipFile.write(filename, arcname, zipfile.ZIP_DEFLATED)
        else: zipFile.write(resource, zipFileName, zipfile.ZIP_DEFLATED)
    return zipFileName


class Reloader:
    def runner(self):
        args, env = [os.sys.executable] + os.sys.argv,  os.environ
        env["PRMP_TK"] = "RUNNING"
        while True:
            exit_code = subprocess.call(args, env=env, close_fds=False)
            if exit_code != 63: return exit_code
    def reloader(self, e=None):
        try: os.system("cls")
        except: os.system("clear")
        print("Reloading")
        os.sys.exit(63)
    def reload(self, func):
        try:
            if os.environ.get("PRMP_TK") == "RUNNING": func()
            else: os.sys.exit(self.runner())
        except Exception as E: pass


