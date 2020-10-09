from os import walk, path
from base64 import b64encode

def get_name(fil):
    base = path.basename(fil)
    name, ext = path.splitext(base)
    return name

pa = r"C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\AGAM_Thrift\AGAM\src\pixs"
op = open("image_list.py", 'w')

agams = []
apps = []
icos = []
logins = []

op.write("prmpsmart = None\n")
for r,t,f in walk(pa):
    for ff in f:
        pap = path.join(r, ff)
        name = get_name(pap)
        enco = b64encode(open(pap, "rb").read())
        
        text = f"{name} = {enco} \n\n"

        op.write(text)
        
        if "agam" in name: agams.append(name)
        if "app" in name: apps.append(name)
        if "ico" in name: icos.append(name)
        if "login" in name: logins.append(name)
        



agams.sort()
apps.sort()
icos.sort()
logins.sort()

op.write('''agams = [agam_A, agam_B] 

apps = [app_A, app_B, app_C, app_D] 

icos = [ico_A, ico_B, ico_C, ico_D] 

logins = [login_A, login_B, login_C, login_D, login_E, login_F, login_G, login_H, login_I, login_J, login_K, login_L, login_M, login_N] ''')

op.close()
