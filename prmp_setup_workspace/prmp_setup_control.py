from prmp.prmp_miscs.prmp_setup import PRMP_Setup, path, chdir, system
chdir(path.dirname(__file__))

root = path.dirname(path.dirname(__file__))


prmp_miscs = 'prmp\prmp_miscs\compiled\prmp_miscs.py'
prmp_gui = 'prmp\prmp_gui\compiled\prmp_gui.py'
photoviewer = 'prmp\prmp_photoviewer\compiled\photoviewer.py'
scripts = [path.join(root, a) for a in [prmp_miscs, prmp_gui, photoviewer]][0:1]
scripts = []

# filename = root = ''
filename = prmp_gui
file = path.join(root, filename)
# print(file)
# print(path.isfile(file))

ps = PRMP_Setup('build_ext', folder=file, scripts=scripts, version='1.5', dest='pyd')

ps.build()


