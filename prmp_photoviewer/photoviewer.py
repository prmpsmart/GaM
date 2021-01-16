from os import path, chdir, listdir, getcwd
from prmp_gui.dialogs import PRMP_MainWindow, PRMP_ImageType, PRMP_ImageLabel
from prmp_gui.two_widgets import *
PRMP_Theme.setThemeIndex(38)

class Photos:
    
    @classmethod
    def getPixs(cls, dir_):
        if not path.isdir(dir_): raise f'{dir_} is not a valid directory/folder.'

        cwd = getcwd()
        chdir(dir_)
        pixs = []
        
        for file in listdir(dir_):
            if PRMP_ImageType.get(file):
                p = path.join(dir_, file)
                pixs.append(p)
        chdir(cwd)
        return pixs




class PhotoViewer(PRMP_MainWindow):

    def __init__(self, title='PRMP Photo Viewer', **kwargs):
        super().__init__(title=title, **kwargs)

        self.frame = Frame(self.container)

        self.folder = LabelButton(self.frame, place=dict(relx=.005, rely=.005, relw=.99, relh=.09), orient='h', topKwargs=dict(text='Folder'), longent=.13)
        self.imageLabel = PRMP_ImageLabel(self.frame, place=dict(relx=.005, rely=.1, relw=.99, relh=.7))
        self.left = Button(self.imageLabel, text=self._left, place=dict(relx=.005, rely=.42, relw=.1, relh=.16), command=self.leftPic, relief='flat')
        self.right = Button(self.imageLabel, text=self._right, place=dict(relx=.9, rely=.42, relw=.1, relh=.16), command=self.rightPic, relief='flat')
        self.total = LabelLabel(self.frame, place=dict(relx=.005, rely=.8, relw=.5, relh=.09), orient='h', topKwargs=dict(text='Total Pictures: '), longent=.55)
        self.currentName = LabelLabel(self.frame, place=dict(relx=.005, rely=.9, relw=.7, relh=.09), orient='h', topKwargs=dict(text='Current: '), longent=.24)
        self.index = LabelEntry(self.frame, place=dict(relx=.65, rely=.8, relw=.35, relh=.09), orient='h', topKwargs=dict(text='Index'), longent=.45)
        # self.listBtn = Checkbutton(self.frame, place=dict(relx=.005, rely=.005, relw=.99, relh=.09), text='Folder', command=self.toggleList)
        
        # self.listFrame = Frame(self.container, place=dict(relx=.005, rely=.005, relw=.99, relh=.09))
        # self.list = ListBox(self.frame, place=dict(relx=.005, rely=.005, relw=.99, relh=.09))

        self.defaults()
        self.placeFrame()
        self.paint()
    
    def toggleList(self): pass
    
    def placeFrame(self, w=0):
        if w: relw = .5
        else: relw = .99
        self.frame.place(relx=.005, rely=.005, relw=relw, relh=.96)

    def placeList(self): self.frame.place(relx=.5, rely=.005, relw=.49, relh=.96)

    
    def defaults(self):
        
        self.bind('<Left>', self.leftPic)
        self.bind('<Right>', self.rightPic)

    
    def leftPic(self, e=0):

        print(e)
    
    def rightPic(self, e=0):


        print(e)




PV = PhotoViewer

d = r'C:\Users\Administrator\Pictures\Valentina'
PV(geo=(500, 500)).mainloop()

