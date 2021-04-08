from prmp_lib.prmp_miscs.prmp_setup import PRMP_Setup, system

binaries = {'photoviewer.cp39-win_amd64.pyd': '.', 'prmp_gui.cp39-win_amd64.pyd': '.', 'prmp_miscs.cp39-win_amd64.pyd': '.'}

a = PRMP_Setup('pyinstaller', name='PRMP_Photoviewer', console=1, binaries=binaries, onefile=False, icon='', noconfirm=0, extra_commands=[], scripts='main.py')
# a = PRMP_Setup('inno_setup', 'PRMP_Photoviewer.iss', gen_script=1, gui=1)

# a.build()

system(r'C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GaM\prmp\prmp_photoviewer\dist\PRMP_Photoviewer\PRMP_Photoviewer.exe C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GaM\src\gui\gam\imgs\nairabag.png -g800x600')

