import os

for r, t, f in os.walk('.'):
    for o in f:
        if o.endswith('pyc'):
            p = os.path.join(r, o)
            print(p)
            os.remove(p)