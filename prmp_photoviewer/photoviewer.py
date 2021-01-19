from os import path, chdir, listdir, getcwd
from prmp_gui import *
PRMP_Theme.setThemeIndex(38)

def getPixs(folder):
    if not path.isdir(folder): raise f'{folder} is not a valid directory/folder.'

    cwd = getcwd()
    chdir(folder)
    pixs = []
    
    for file in listdir(folder):
        if path.isfile(file):
            if PRMP_ImageType.get(file):
                p = path.join(folder, file)
                pixs.append(p)
    chdir(cwd)
    return pixs

class PhotoViewer(PRMP_MainWindow):

    def __init__(self, title='PRMP Photo Viewer', folder='', **kwargs):
        super().__init__(title=title, **kwargs)
        self._folder = folder
        self._pixs = []
        self._total = 0
        self._current = ''
        self._index = 0

        self.frame = Frame(self.container)

        self.folder = LabelButton(self.frame, place=dict(relx=.005, rely=.005, relw=.99, relh=.09), orient='h', topKwargs=dict(text='Folder'), longent=.13, bottomKwargs=dict(command=self.chooseDir))
        self.bind('<Control-O>', self.chooseDir)
        self.bind('<Control-o>', self.chooseDir)

        self.imageLabel = PRMP_ImageLabel(self.frame, place=dict(relx=.005, rely=.1, relw=.99, relh=.7))
        self.previous = Button(self.imageLabel, text=self._previous, place=dict(relx=.005, rely=.42, relw=.1, relh=.16), command=self.previousPic, relief='flat')
        self.next = Button(self.imageLabel, text=self._next, place=dict(relx=.89, rely=.42, relw=.1, relh=.16), command=self.nextPic, relief='flat')

        self.total = LabelLabel(self.frame, place=dict(relx=.005, rely=.8, relw=.5, relh=.09), orient='h', topKwargs=dict(text='Total Pictures: '), longent=.55)
        self.index = LabelEntry(self.frame, place=dict(relx=.65, rely=.8, relw=.35, relh=.09), orient='h', topKwargs=dict(text='Index'), longent=.45, bottomKwargs=dict(_type='number'))
        self.index.B.bind('<Return>', self.byIndex)
        self.current = LabelLabel(self.frame, place=dict(relx=.005, rely=.9, relw=.7, relh=.09), orient='h', topKwargs=dict(text='Current: '), longent=.24)

        self.listBtn = Checkbutton(self.frame, place=dict(relx=.75, rely=.9, relw=.2, relh=.07), text='List?', command=self.toggleList)
        
        self.listFrame = Frame(self.container)
        self.list = ListBox(self.listFrame, place=dict(relx=.005, rely=.005, relw=.99, relh=.99), callback=self.listSelection)

        self.defaults()
        self.placeFrame()
        self.paint()
    
    def defaults(self):
        self.bind('<Left>', self.previousPic)
        self.bind('<Right>', self.nextPic)
        self.updateDatas()
    
    def byIndex(self, e=0):
        index = self.index.get()
        try:
            index = int(index)
            assert 0 <= index <= self._total, f'Index {index} is not in range 0 ... {self._total}.'
            self._index = index
            self.setCurrent()
        except Exception as e:
            PRMP_MsgBox(self, title=e.__class__.__name__, message=e, ask=0, _type='error')
            return
    
    def updateDatas(self):
        self.folder.set(self._folder)
        self.total.set(self._total)
        self.index.set(self._index+1)
        self.setCurrent()
    
    def setCurrent(self):
        if not self._pixs: return
        self.index.set(self._index)
        self._current = self._pixs[self._index]
        if not path.exists(self._current):
            PRMP_MsgBox(self, title='Not Exist', message=f'{self._current} does not exist, try to reload the folder.', ask=0)
            return
        current = path.basename(self._current)
        self.current.set(current)
        self.imageLabel.loadImage(self._current)
    
    def chooseDir(self, e=0):
        folder = dialogFunc(path=1, folder=1)
        if not folder: return
        self._folder = folder
        self._pixs = getPixs(folder)
        self._current = ''
        if self._pixs: self._current = self._pixs[0]
        self._total = len(self._pixs)
        self.updateDatas()
        self.list.set(self._pixs)
    
    def listSelection(self, selected, event=0):
        if selected:
            selected = selected[0]
            self._index = self._pixs.index(selected)
            self.setCurrent()
    
    def previousPic(self, e=0):
        if self._pixs:
            self._index -= 1
            if self._index <= 0: self._index = self._total - 1
            self.setCurrent()

    def nextPic(self, e=0):
        if self._pixs:
            self._index += 1
            if self._index >= self._total: self._index = 0
            self.setCurrent()
    
    def toggleList(self):
        if self.listBtn.get():
            x, y = self.geo[:2]
            self.changeGeometry((x*2, y))
            self.placeList()
            self.placeFrame(1)
        else:
            self.changeGeometry(self.geo[:2])
            self.placeFrame()
            self.listFrame.place_forget()
    
    def placeFrame(self, w=0):
        if w: relw = .5
        else: relw = .99
        self.frame.place(relx=.005, rely=.005, relw=relw, relh=.96)

    def placeList(self): self.listFrame.place(relx=.5, rely=.005, relw=.49, relh=.96)

PV = PhotoViewer

PV(geo=(500, 500), tm=1).mainloop()
exit()

rootDir = r'C:\Users\Administrator\Coding_Projects\PYTHON\Dev_Workspace\GAM\GAM\prmp_miscs\prmp_pics\prmp_xbms'
rootDir = r'C:\Users\Administrator\pictures\valentina'

# PWd.TIPPING = 9
root = Tk(title='XBM viewer', side='center', geo=(2100, 900), gaw=1, tm=1)
cont = Frame(root.container)
cont.place(relx=0, y=0, relw=1, relh=1)


lbls = []
count = 0
c = 0

for xbm in listdir(rootDir):
    r = count % 8
    if r == 0 and count != 0: c += 1
    fxbm = path.join(rootDir, xbm)
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
