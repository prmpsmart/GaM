from prmp.prmp_miscs.prmp_setup import PRMP_Setup, path, chdir, system
chdir(path.dirname(__file__))

root = path.dirname(path.dirname(__file__))


prmp_miscs = 'prmp\prmp_workspace\prmp_modules\prmp_miscs.py'
prmp_gui = 'prmp\prmp_workspace\prmp_modules\prmp_gui.py'
scripts = [path.join(root, a) for a in [prmp_miscs, prmp_gui]][0:1]
scripts = []

# filename = root = ''
filename = prmp_gui
# filename = prmp_miscs
file = path.join(root, filename)
# file = r'C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GaM\prmp\prmp_miscs\prmp_images.py'
# print(file)
# print(path.isfile(file))

ps = PRMP_Setup('build_ext', folder=file, scripts=scripts, version='1.5', dest='pyd')

ps.build()


