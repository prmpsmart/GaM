
import os
from distutils.core import setup
from Cython.Build import cythonize
import PyInstaller.__main__


inno_script_example = '''
    ; Script generated by the PRMP Smart SETUP WIZARD.
    ; SEE THE DOCUMENTATION FOR DETAILS ON CREATING PRMP Smart SETUP SCRIPT FILES!

    #define MyAppName "TranxFer"
    #define MyAppVersion "1.5"
    #define MyAppPublisher "PRMPSmart Inc."
    #define MyAppURL "http://www.tranxFer.com/"
    #define MyAppExeName "TranxFer.exe"

    [Setup]
    ; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
    ; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
    AppId={{C280E116-9281-4691-B2FE-E53773049917}
    AppName={#MyAppName}
    AppVersion={#MyAppVersion}
    ;AppVerName={#MyAppName} {#MyAppVersion}
    AppPublisher={#MyAppPublisher}
    AppPublisherURL={#MyAppURL}
    AppSupportURL={#MyAppURL}
    AppUpdatesURL={#MyAppURL}
    DefaultDirName={autopf}\{#MyAppName}
    DefaultGroupName={#MyAppName}
    AllowNoIcons=yes
    ; The [Icons] "quicklaunchicon" entry uses {userappdata} but its [Tasks] entry has a proper IsAdminInstallMode Check.
    UsedUserAreasWarning=no
    ; Remove the following line to run in administrative install mode (install for all users.)
    PrivilegesRequired=lowest
    PrivilegesRequiredOverridesAllowed=dialog
    OutputDir={output directory here}
    OutputBaseFilename=TranxFer-setup
    Password=mimi
    Compression=lzma
    SolidCompression=yes
    WizardStyle=modern

    [Languages]
    Name: "english"; MessagesFile: "compiler:Default.isl"

    [Tasks]
    Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
    Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

    [Files]
    Source: {put the main exe here};
    DestDir: "{app}"; Flags: ignoreversion
    Source: "{put the path to folder needed here} \*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
    ; NOTE: Don't use "Flags: ignoreversion" on any shared system files

    [Icons]
    Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
    Name: "{group}\{cm:ProgramOnTheWeb,{#MyAppName}}"; Filename: "{#MyAppURL}"
    Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
    Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
    Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

    [Run]
    Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

'''

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

class Holder: pass


class PRMP_Setup:

    def __init__(self, type_='NaN', *args, **kwargs):
        self.type = type_
        if hasattr(self, self.type): getattr(self, self.type)(*args, **kwargs)
        else: raise ValueError(f'{self.type} is not a valid build type!')

    def build(self):
        func = f'_{self.type}'
        getattr(self, func)()

    def get_scripts(self, folder):
        files = []
        if os.path.isdir(folder):
            for fi in os.listdir(folder):
                p = os.path.join(folder, fi)
                if os.path.isfile(p): files.append(p)
            return files, f'/{folder}'
        else: return [folder], ''

    def build_ext(self, folder='', scripts=[], description='', meta_datas={}, classifiers=classifiers, platforms=platforms, keywords=[], license='', name='', inplace=False, dest='', version='1.0', include_dirs=[]):
        self.holder = Holder()
        name = name or os.path.basename(folder[:-3]) if folder.endswith('.py') else folder

        self.holder.meta_datas = dict(
            name=name,
            version=version,
            author='PRMPSmart',
            author_email='prmpsmart@gmail.com',
            maintainer='PRMPSmart',
            maintainer_email='prmpsmart@gmail.com',
            url=f'github.com/prmpsmart/{name}',
            description=description or f'an extension module for {folder}',
            long_description='an example to test the creation of python extension modules et all.',
            download_url=f'github.com/prmpsmart/{name}.git',
            classifiers=classifiers,
            platforms=platforms,
            keywords=keywords,
            license=license_,
        )
        self.holder.meta_datas.update(meta_datas)

        self.holder.scripts, self.holder.dest = (scripts, dest) if scripts else self.get_scripts(folder)
        if not self.holder.dest: self.holder.dest = dest or 'pyd'

        self.holder.directory = '--inplace' if inplace else f'-b{self.holder.dest}'
        self.holder.include_dirs = include_dirs
        if include_dirs: self.holder.include_dirs = [f'-I{incl_d}' for incl_d in include_dirs]
        # print(self.holder.include_dirs)

    def _build_ext(self):
        for d in ['c', 'pyd']:
            try: os.mkdir(d)
            except: pass
        ext_modules = cythonize(self.holder.scripts, language_level=3, build_dir='c', output_dir='c')

        os.sys.argv.extend(['build_ext', self.holder.directory, *self.holder.include_dirs])
        setup(ext_modules=ext_modules, **self.holder.meta_datas)

    def pyinstaller(self, scripts=[], console=True, extra_commands=[], log_level='info', datas={}, binaries={}, name='', onefile=False, icon='', clean=False, noconfirm=False):
        '''
        :param console: a boolean whether to enable consoled executable or not
        :param extra_commands: commands to pass to PyInstaller
        '''

        # assert scripts, 'Provide script(s) to compile!'

        if isinstance(scripts, str): scripts = [scripts]


        log_level = log_level.upper()
        log_levels = ["TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]
        assert log_level in log_levels, f'{log_level} not in {log_levels}.'

        self.holder = Holder()

        self.holder.scripts = scripts
        self.holder.name = f'-n{name}'

        self.holder.console = '-c' if console else '-w'
        self.holder.onefile = '-F' if onefile else '-D'
        self.holder.icon = f'-i{icon}' if icon else ''

        self.holder.datas = []

        for data in datas:
            dat = [f'--add-data', os.pathsep.join([data, datas[data]])]
            self.holder.datas.extend(dat)

        self.holder.binaries = []

        for binary in binaries:
            dat = [f'--add-binary', os.pathsep.join([binary, binaries[binary]])]
            self.holder.binaries.extend(dat)

        self.holder.extra_commands = extra_commands
        self.holder.clean = '--clean' if clean else ''
        self.holder.noconfirm = '-y' if noconfirm else ''

        self.holder.log_level = ['--log-level', log_level]

        self.holder.run_parameter = [self.holder.name, self.holder.console, self.holder.onefile, self.holder.icon, *self.holder.extra_commands, *self.holder.datas, *self.holder.binaries, self.holder.clean, self.holder.noconfirm, *self.holder.log_level, *self.holder.scripts]

        while '' in self.holder.run_parameter: self.holder.run_parameter.remove('')

        # print(self.holder.run_parameter)

    def _pyinstaller(self): PyInstaller.__main__.run(self.holder.run_parameter)

    def inno_setup(self, script='', old_ver='', new_ver='', gen_script=False, gui=False, customize=False, author='PRMP Smart'):
        self.holder = Holder()
        self.holder.script = script
        self.holder.new_ver = new_ver
        self.holder.old_ver = old_ver
        self.holder.author = author
        self.holder.gui = gui
        self.holder.customize = customize

        self.holder.script = script
        self.holder.gen_script = f'compil32 /wizard "{author} SETUP WIZARD" "{script}"' if gen_script else False


        program = 'iscc' if not gui else 'compil32 /cc'
        self.holder.program = f'{program} {script}'

    def customize_script(self, script, old_ver='', new_ver='', author=''):
        with open(script) as old: text = old.read()
        text = text.replace("INNO", author)
        if old_ver and new_ver: text = text.replace(old_ver, new_ver)
        with open(script, 'w') as new: new.write(text)

    def _inno_setup(self):
        inno_installed = "Inno Setup".upper() in ''.join(os.get_exec_path()).upper()
        if not inno_installed: raise ValueError('Inno Setup Compiler is not installed. You can get it on https://jrsoftware.org')

        if self.holder.gen_script: os.system(self.holder.gen_script)
        if self.holder.customize: self.customize_script(self.holder.script, old_var=self.holder.old_ver, new_var=self.holder.new_ver, author=self.holder.author)
        os.system(self.holder.program)

    def change_ext(self, file, ext):
        splits = file.split('.')
        splits[-1] = f'.{ext}'
        _outfile = ''.join(splits)
        return _outfile

    def py2c(self, file, quiet=False, embed=False, outfile='', pyver=2, dry_run=False):
        '''
        :param pyver: python version of the file
        '''
        _outfile = outfile or self.change_ext(file, 'c')

        embed = '--embed=main' if embed else ''
        outfile = f'-o {_outfile}' if _outfile else ''
        pyver = '-3' if pyver == 3 else ''
        cmd = f"python -m cython {pyver} -f {embed} {file} {outfile}"
        if dry_run or not quiet: print(cmd)
        if not dry_run: os.system(cmd)
        return _outfile

    def create_dll(self, file, include_dir='', as_pyd=False, python_dll='', cython_it=False, outext='dll', quiet=False, dry_run=False, **kwargs):
        self.holder = Holder()
        self.holder.dry_run = dry_run
        self.holder.quiet = quiet
        self.holder.python_dll = python_dll
        self.holder.file = file

        if cython_it: self.holder.file = self.py2c(file, dry_run=dry_run, **kwargs)
        self.holder.include_dir = f'-I{include_dir}' if include_dir else ''
        self.holder.objfile = self.change_ext(file, 'o')
        self.holder.outext = 'pyd' if as_pyd else outext

        self.holder.outfile = self.change_ext(file, outext)
        # print(self.holder.include_dir)

    def _create_dll(self):

        cmd1 = f"gcc -Wall -g {self.holder.include_dir} -c {self.holder.file} -o {self.holder.objfile}"
        if self.holder.dry_run or not self.holder.quiet: print(cmd1)
        if not self.holder.dry_run: os.system(cmd1)

        cmd2 = f"g++ -shared -Wl,--dll {self.holder.objfile} -o {self.holder.outfile} {self.holder.python_dll}"
        if self.holder.dry_run or not self.holder.quiet: print(cmd2)
        if not self.holder.dry_run: os.system(cmd2)

    def _create_exe(self, file, include_dir='', win=0, python_dll='', quiet=False, dry_run=False):
        outfile = self.change_ext(file, 'exe')
        include_dir = f'-I{include_dir}' if include_dir else ''

        mode = "-mwindows" if win else "-mconsole"

        cmd =  f"g++ -Wall -g {include_dir} {mode} {file} {python_dll} -municode -o {outfile}"

        if dry_run or not quiet: print(cmd)
        if not dry_run: os.system(cmd)




