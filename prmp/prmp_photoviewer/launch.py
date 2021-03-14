from prmp.prmp_miscs.prmp_setup import PRMP_Setup, system

binaries = {'photoviewer.cp39-win_amd64.pyd': '.', 'prmp_gui.cp39-win_amd64.pyd': '.', 'prmp_miscs.cp39-win_amd64.pyd': '.'}

# a = PRMP_Setup('pyinstaller', name='PRMP_Photoviewer', console=True, binaries=binaries, onefile=False, icon='', noconfirm=True, extra_commands=[])
a = PRMP_Setup('pyinstaller', name='PRMP_Photoviewer', console=0, binaries=binaries, onefile=False, icon='', noconfirm=0, extra_commands=[], scripts='main.py')

# a.build()
system(r'C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GaM\prmp\prmp_photoviewer\dist\PRMP_Photoviewer\PRMP_Photoviewer_w.exe C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GaM\src\gui\gam\imgs\nairabag.png -g800x600')

