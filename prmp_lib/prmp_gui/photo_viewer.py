from os import path, chdir, listdir, getcwd, sys
try:
    # this means that its the prmp_gui package that is being used
    from prmp_lib.prmp_gui.core import *
    from prmp_lib.prmp_gui.two_widgets import *
    from prmp_lib.prmp_gui.dialogs import *
except:
    # this means that its the prmp_gui extension module that is being used
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

    def __init__(self, title='PRMP Photo Viewer', folder='', file='', **kwargs):
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

        self.imageLabel = PRMP_ImageLabel(self.frame, place=dict(relx=.005, rely=.1, relw=.99, relh=.7), prmpImage=file)

        self.previous = Button(self.imageLabel, text=self._previous, place=dict(relx=.005, rely=.42, relw=.1, relh=.16), command=self.previousPic, relief='flat', tipKwargs=dict(text='Previous Picture'))

        self.next = Button(self.imageLabel, text=self._next, place=dict(relx=.89, rely=.42, relw=.1, relh=.16), command=self.nextPic, relief='flat', tipKwargs=dict(text='Next Picture'))

        self.total = LabelLabel(self.frame, place=dict(relx=.005, rely=.8, relw=.5, relh=.09), orient='h', topKwargs=dict(text='Total Pictures: '), longent=.55)
        self.index = LabelEntry(self.frame, place=dict(relx=.65, rely=.8, relw=.35, relh=.09), orient='h', topKwargs=dict(text='Index'), longent=.45, bottomKwargs=dict(_type='number'))
        self.index.B.bind('<Return>', self.byIndex)

        self.current = LabelEntry(self.frame, place=dict(relx=.005, rely=.9, relw=.7, relh=.09), orient='h', topKwargs=dict(text='Current: '), longent=.24, bottomKwargs=dict(state='readonly'))

        self.listBtn = Checkbutton(self.frame, place=dict(relx=.75, rely=.9, relw=.2, relh=.07), text='List?', command=self.toggleList, var=1, value=1, tipKwargs=dict(text='Toggle list of pictures in the current folder.'))

        self.listFrame = Frame(self.container)
        self.list = ListBox(self.listFrame, place=dict(relx=.005, rely=.005, relw=.99, relh=.99), callback=self.listSelection)

        self.defaults()
        self.placeFrame()
        if file:
            d = path.dirname(file)
            if d: self.chooseDir(folder=d)
            self.setCurrent(file)
            # self.current.set(file)
        self.paint()

    def defaults(self):
        self.bind('<Left>', self.previousPic)
        self.bind('<Right>', self.nextPic)
        if self._folder: self.chooseDir(folder=self._folder)
        else: self.updateDatas()

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

    def setCurrent(self, current_=''):
        if not current_:
            if not self._pixs: return
            self.index.set(self._index)
            self._current = self._pixs[self._index]
            if not path.exists(self._current):
                PRMP_MsgBox(self, title='Not Exist', message=f'{self._current} does not exist, try to reload the folder.', ask=0)
                return

        current = path.basename(self._current)
        self.current.set(current)
        self.imageLabel.loadImage(current_ or self._current)

    def chooseDir(self, e=0, folder=''):
        if not folder: folder = dialogFunc(path=1, folder=1, initialdir=self._folder, title='PRMP Photoviewer')

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

def main():
    import argparse

    arrd = sys.argv
    parser = argparse.ArgumentParser(prog='PRMP_PhotoViewer.exe', description="PRMP PhotoViewer", epilog="By PRMP Smart prmpsmart@gmail.com", exit_on_error=False)

    # if os.environ.get("PRMP_TK") == "RUNNING": parser.add_argument("prmp")

    parser.add_argument("path", nargs='?', type=str, help="path to view", default='')
    parser.add_argument("-g", "--geo", type=str, dest="geometry", help="geometry of the app")
    parser.add_argument("-s", "--side", type=str, dest="side", help="side to postion the app", default='center')
    parser.add_argument("-v", "--version", action="version", version="Version = 2.0.0")

    args = parser.parse_args()
    path_ = args.path
    geometry = args.geometry
    side = args.side

    if path.exists(path_):
        if path.isfile(path_): key = 'file'
        elif path.isdir(path_): key = 'folder'
        else: key = None

        if key: dicts = {key: path_}
        else: ValueError(f'The "path" provided -> "{path_}" is invalid!')

    elif path_: raise ValueError(f'The "path" provided -> "{path_}" does not exist!')
    else: dicts = {}

    if geometry: geo = PRMP_Mixins.getNumsInStrAsList(None, geometry, [1,3])

    else: geo = (500, 500)

    PhotoViewer(geo=geo, side=side, tipping=1, **dicts).mainloop()

if __name__ == '__main__': main()


