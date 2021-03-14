from prmp.prmp_miscs.prmp_setup import PRMP_Setup, path, chdir, system
chdir(path.dirname(__file__))

root = path.dirname(path.dirname(__file__))


filename = 'prmp\prmp_miscs\compiled\prmp_miscs.py'
# filename = 'prmp\prmp_gui\compiled\prmp_gui.py'
# filename = 'prmp\prmp_photoviewer\compiled\photoviewer.py'



file = path.join(root, filename)

ps = PRMP_Setup('build_ext', folder=file, version='')

# ps.build()


