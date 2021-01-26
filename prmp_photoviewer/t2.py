from prmp_gui.extensions import *
from prmp_miscs.prmp_pics import *
from os import path, chdir, listdir, getcwd

rootDir = r'C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GAM\GAM\prmp_miscs\prmp_pics\prmp_xbms'
rootDir = r'C:\Users\Administrator\pictures\valentina'
rootDir = r'C:\Users\Administrator\Documents\GaM OFFICE\logos'

# PWd.TIPPING = 9

root = Tk(title='XBM viewer', side='center', geo=(600, 600), gaw=1, tm=1)
cont = Frame(root.container)
cont.place(relx=0, y=0, relw=1, relh=1)


lbls = []
count = 0
c = 0

for xbm in listdir(rootDir):
    fxbm = path.join(rootDir, xbm)
    if not PRMP_ImageType.get(fxbm): continue
    r = count % 2
    if r == 0 and count != 0: c += 1
    # lbl = L(cont, text=xbm, tip=xbm)
    # lbl = F(cont, tip=xbm)
    lbl = PRMP_ImageLabel(cont, prmpImage=fxbm, inbuiltKwargs=dict(inbuilt=0, inExt='xbm'), resize=(100, 100))#.place(relx=.2, rely=.2, relh=.6, relw=.6)
    lbl.grid(row=r, column=c)
    count += 1
    lbls.append(lbl)
    
# B(cont, text='tesst', tip='iepie kiuaw \niua oaiw acioe opopwefno aifu').grid(column=c, row=r+2)
# B(cont, text='tesst', tip='iepie kiuaw \niua oaiw acioe opopwefno aifu').grid()


root.paint()
cont.paint()
root.mainloop()
