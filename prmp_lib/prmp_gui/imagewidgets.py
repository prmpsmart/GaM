from . import *
from prmp_lib.prmp_miscs.prmp_pics import *


class PRMP_ImageWidget:
    def __init__(self, prmpImage=None, thumb=None, resize=None, bindMenu=0, fullsize=False, loadDefault=0, imgDelay=100, face=False, **imageKwargs):
        if not _PIL_: print('PIL is not available for this program!')
        imageKwargs['for_tk'] = 1

        self.rt = None
        self.prmpImage = prmpImage
        self.thumb = thumb
        self.resize = resize
        self.fullsize = fullsize
        self.face = face

        self.frame_counter = 0
        self.frame = None
        self.frames = None
        self.durations = None
        self.isGif = False
        
        self.loadDefault = loadDefault

        self.default_dp = PRMP_Image('profile_pix', inbuilt=True, thumb=self.thumb)

        if bindMenu: self.bindMenu()

        # self.after(imgDelay, lambda: self.loadImage(self.prmpImage, **imageKwargs))
        self.loadImage(self.prmpImage, **imageKwargs)

        # self.bind('<Configure>', lambda e: self.loadImage(self.prmpImage, event=e, **imageKwargs))

    def disabled(self):
        self.unBindMenu()
        super().disabled()

    def normal(self):
        self.bindMenu()
        super().normal()

    def loadImage(self, prmpImage=None, event=None, **kwargs):
        self.delMenu()
        self.isGif = False

        self.frame_counter = 0
        # self.thumb = self.resize or self.thumb
        if not self.thumb: self.thumb = self.width, self.height

        if self.winfo_ismapped() and  not (self.resize and self.thumb):
            if self.thumb[0] < 0 and self.thumb[1] < 0:
                # self.thumb = (250, 200)
                self.after(50, lambda: self.loadImage(prmpImage, **kwargs))
                return

        try:
            if not isinstance(prmpImage, PRMP_Image): prmpImage = PRMP_Image(prmpImage, thumb=self.thumb, resize=self.resize, **kwargs)

            if isinstance(prmpImage, PRMP_Image): self.imageFile = prmpImage.imageFile
            else: raise ValueError('prmpImage must be an instance of PRMP_Image')

            self.prmpImage =  prmpImage

            if prmpImage.ext == 'xbm': self.frame = prmpImage.resizeTk(self.resize)

            self.image = self.prmpImage.image
            if self.fullsize: self.resize = (self.width, self.height)

            if self.resize: self.frame = self.prmpImage.resizeTk(self.resize)
            else: self.frame = self.prmpImage.thumbnailTk(self.thumb)

            if self.prmpImage.ext == 'gif':
                self.frames = []
                self.durations = []
                for frame in ImageSequence.Iterator(self.image):
                    if self.resize: frame = frame.resize(self.resize)
                    elif self.thumb: frame.thumbnail(self.thumb)
                    tkimg = PhotoImage(frame)
                    self.frames.append(tkimg)
                    self.durations.append(frame.info['duration'])
                if self.frames: self.frame = self.frames[self.frame_counter]

                self.isGif = True
                self.__renderGif()
            
            else:
                if self.face: self.frame = self.prmpImage._find_faces(prmp_image=1, for_tk=1)

            self.config(image=self.frame)
            self.paint()

        except Exception as e:
            raise e


            self['image'] = ''
            if self.loadDefault: self.loadImage(self.default_dp)

    def __renderGif(self):
        if not self.isGif: return
        if not self.frames: return
        if not self.winfo_exists(): return

        # Update Frame
        self.frame = self.frames[self.frame_counter]
        self.config(image=self.frames[self.frame_counter])

        # Loop Counter
        self.frame_counter += 1
        if self.frame_counter >= len(self.frames): self.frame_counter = 0
        # self.after(self.durations[self.frame_counter], self.__renderGif)
        self.after(100, self.__renderGif)

    def removeImage(self):
        self.delMenu()
        from .dialogs import PRMP_MsgBox

        PRMP_MsgBox(self, title='Profile Picture Removal', message='Are you sure you wanna remove the picture from this profile? ', callback=self._removeImage)

    def _removeImage(self, val):
        if val: self.loadImage()

    def set(self, imageFile=None):
        if imageFile: self.loadImage(imageFile)

    def changeImage(self, e=0):
        self.delMenu()
        file = askopenfilename(filetypes=picTypes)
        if file: self.loadImage(file)

    def bindMenu(self):
        self.bind('<1>', self.delMenu, '+')
        self.bind('<3>', self.showMenu, '+')
        self.bind('<Double-1>', self.camera, '+')

    def unBindMenu(self):
        self.unbind('<1>')
        self.unbind('<3>')
        self.unbind('<Double-1>')

    def get(self): return self.imageFile

    def delMenu(self, e=0):
        if self.rt:
            self.rt.destroy()
            del self.rt
            self.rt = None

    def camera(self, e=0):
        self.delMenu()
        from .dialogs import PRMP_CameraDialog

        PRMP_CameraDialog(self, title='Profile Photo', tw=1, tm=1, callback=self.set)

    def saveImage(self):
        self.delMenu()
        if self.imageFile:
            from .dialogs import dialogFunc
            file = dialogFunc(path=1, save=1,filetypes=picTypes)
            if file: self.imageFile.save(file)

    def showMenu(self, e=0):
        self.delMenu()
        x, y = e.x, e.y
        x, y = e.x_root, e.y_root
        self.rt = rt = PRMP_Toplevel(self, geo=(50, 75, x, y), tm=1, asb=0, atb=0)
        PRMP_Button(rt, text='Camera', command=self.camera, overrelief='sunken', font=PRMP_Theme.DEFAULT_MENU_FONT, place=dict(relx=0, rely=0, relh=.25, relw=1))
        PRMP_Button(rt, text='Change', command=self.changeImage, overrelief='sunken', font=PRMP_Theme.DEFAULT_MENU_FONT, place=dict(relx=0, rely=.25, relh=.25, relw=1))
        PRMP_Button(rt, config=dict(text='Save', command=self.saveImage, overrelief='sunken'), font=PRMP_Theme.DEFAULT_MENU_FONT, place=dict(relx=0, rely=.5, relh=.25, relw=1))
        PRMP_Button(rt, config=dict(text='Remove', command=self.removeImage, overrelief='sunken'), font=PRMP_Theme.DEFAULT_MENU_FONT, place=dict(relx=0, rely=.75, relh=.25, relw=1))
        rt.paint()

IW = PRMP_ImageWidget

class PRMP_ImageLabel(PRMP_ImageWidget, PRMP_Label):
    def __init__(self, master, prmpImage=None, resize=(), thumb=(), imageKwargs={}, config={}, **kwargs):
        PRMP_Label.__init__(self, master, config=dict(anchor='center', **config), **kwargs)
        PRMP_ImageWidget.__init__(self, prmpImage=prmpImage, thumb=thumb, resize=resize, **imageKwargs)

IL = PRMP_ImageLabel

class PRMP_ImageSLabel(PRMP_ImageWidget, PRMP_Style_Label):
    def __init__(self, master, prmpImage=None, resize=(), thumb=(), imageKwargs={}, config={}, **kwargs):
        PRMP_Style_Label.__init__(self, master, config=dict(anchor='center', **config), **kwargs)
        PRMP_ImageWidget.__init__(self, prmpImage=prmpImage, thumb=thumb, resize=resize, **imageKwargs)

SIL = PRMP_ImageSLabel

class PRMP_ImageButton(PRMP_ImageWidget, PRMP_Button):
    def __init__(self, master, prmpImage=None, resize=(), thumb=(), config={}, imageKwargs={}, **kwargs):
        PRMP_Button.__init__(self, master, config=dict(anchor='center', **config), **kwargs)
        PRMP_ImageWidget.__init__(self, prmpImage=prmpImage, thumb=thumb, resize=resize,  **imageKwargs)

IB = PRMP_ImageButton

class PRMP_ImageSButton(PRMP_ImageWidget, PRMP_Style_Button):
    def __init__(self, master, prmpImage=None, resize=(), thumb=(), config={}, imageKwargs={}, **kwargs):
        PRMP_Style_Button.__init__(self, master, config=dict(**config), **kwargs)
        PRMP_ImageWidget.__init__(self, prmpImage=prmpImage, thumb=thumb, resize=resize,  **imageKwargs)

ISB = PRMP_ImageSButton


class PRMP_ImageCheckbutton(PRMP_ImageWidget, PRMP_Checkbutton):
    def __init__(self, master, prmpImage=None, resize=(), thumb=(), config={}, imageKwargs={}, **kwargs):
        PRMP_Checkbutton.__init__(self, master, config=dict(anchor='center', **config), **kwargs)
        PRMP_ImageWidget.__init__(self, prmpImage=prmpImage, thumb=thumb, resize=resize,  **imageKwargs)

IB = PRMP_ImageCheckbutton

class PRMP_ImageSCheckbutton(PRMP_ImageWidget, PRMP_Style_Checkbutton):
    def __init__(self, master, prmpImage=None, resize=(), thumb=(), config={}, imageKwargs={}, **kwargs):
        PRMP_Style_Checkbutton.__init__(self, master, config=dict(**config), **kwargs)
        PRMP_ImageWidget.__init__(self, prmpImage=prmpImage, thumb=thumb, resize=resize,  **imageKwargs)

ISB = PRMP_ImageSCheckbutton


class PRMP_Camera(PRMP_Style_Frame):

    def __init__(self, master, source=0, frameUpdateRate=10, callback=None, face=False, **kwargs):
        import cv2
        self.cv2 = cv2
        self.cam = None
        self.source = source
        self.image = None
        self._image = None
        self._set = None
        self.callback = callback
        self.face = face
        self.pause = False
        self.opened = False

        self.frameUpdateRate = frameUpdateRate

        super().__init__(master, **kwargs)

        self.screen = PRMP_Style_Label(self, place=dict(relx=0, rely=0, relh=1, relw=1), anchor='center')
        self.screen.bind('<Double-1>', self.screenPause, '+')
        self.screen.bind('<Configure>', self.onConfig, '+')

        self.save = Button(self, config=dict(text='Save', command=self.saveImage))
        self.bind('<Map>', self.checkVisibility)
        self.bind('<Unmap>', self.checkVisibility)
        self.bind('<Return>', self.saveImage)

    def y(self): return

    def placeSave(self):
        self.screen.place(relx=.006, rely=.01, relh=.85, relw=.985)
        self.save.place(relx=.375, rely=.87, relh=.1, relw=.25)

    def screenPause(self, e=0):
        if self.pause or self._set:
            self.pause = False
            self.openCam()
            self._set = None
            self.screen.place(relx=0, rely=0, relh=1, relw=1)
            self.save.place_forget()
        else:
            self.pause = True
            self.closeCam()
            self.placeSave()

    def saveImage(self):
        self.imageFile = PRMP_ImageFile(image=self._image)
        if self.callback: return self.callback(self.imageFile)

    @staticmethod
    def _saveImage(image):
        from .dialogs import dialogFunc
        file = dialogFunc(path=1, save=1, filetypes=picTypes)

        if file: image.save(file)

    def get(self): return self.saveImage()

    def onConfig(self, event=None):
        if not self._image: return
        w_h = self.screen.width, self.screen.height
        
        image = self._image
        # image.thumbnail(w_h)
        image = image.resize(w_h)
        self._updateScreen(image)
        
    def openCam(self):
        if self._set: return

        self.cam = self.cv2.VideoCapture(self.source)
        self.updateScreen()
        self.opened = True

    def closeCam(self):
        if self.cam and self.cam.isOpened():
            self.cam.release()
            self.opened = False

    def snapshot(self):
        # Get a frame from the video source
        success, frame = self.getFrame()
        # if frame: self.cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", self.cv2.cvtColor(frame, self.cv2.COLOR_RGB2BGR))

    def _updateScreen(self, image=None):
        self.image = PhotoImage(image=image) if image else self.image
        self.screen.config(image=self.image)

    def updateScreen(self):
        if self.image: self._updateScreen()
        # if self.image: self.screen['image'] = self.image
        del self.image
        self.image = None
        self.setImage()
        if not self.pause: self.after(self.frameUpdateRate, self.updateScreen)

    def checkVisibility(self, event):
        if event.type == tk.EventType.Map:
            if not self.pause:
                self.after(100, self.openCam)
                pass
        elif event.type == tk.EventType.Unmap: self.closeCam()

    def setImage(self, image=None):
        self._set = image
        success, frame = self.getFrame()
        if success or self._set:
            if self.width <= 0 and self.height <= 0: return

            if self.face: frame = PRMP_Image.find_faces(array=frame)

            # self._image = PRMP_Image(self._set) if self._set else PRMP_Image(array=frame, for_tk=1)
            self._image = Image.fromarray(frame)

            self.onConfig()

            self._updateScreen(image)

    def getFrame(self):
        if self.cam and self.cam.isOpened():
            success, frame = self.cam.read()
            if success: return (success, self.cv2.cvtColor(frame, self.cv2.COLOR_BGR2RGB))
            else: return (success, None)
        else: return (False, None)

    def __del__(self): self.closeCam()