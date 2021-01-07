from os import *

cat = 'png'
dir_ = f'prmp_{cat}s'

file = f'{dir_}.py'


names = {path.splitext(v)[0]: v for v in listdir(dir_)}
files = [path.join(dir_, f) for f in listdir(dir_)]



print(names)








