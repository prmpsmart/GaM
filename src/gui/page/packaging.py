from .packed import *
sys = os.sys

class t: pass
ttk = tk = t()
gg = globals().copy()
for a in gg: setattr(t, a, gg[a])












