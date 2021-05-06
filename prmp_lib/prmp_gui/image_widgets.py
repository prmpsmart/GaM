from . import *
from .core_ttk import PRMP_Style_
from prmp_lib.prmp_miscs.prmp_images import *
from prmp_lib.prmp_miscs.prmp_images import _PIL_
import time


class PRMP_ImageWidget:
    WidgetClass = None
    count = 0

    def __init__(self, master, bindMenu=0,  loadDefault=0, imgDelay=150, face=False, imageKwargs={}, config={}, **kwargs):

        self.WidgetClass.__init__(self, master, config=config, **kwargs)
        if not _PIL_: print('PIL is not available for this program!')

        self.rt = None
        self.face = face
        self.lastRender = 0
        self.frame_counter = 0
        self.frame = None
        self.frames = None
        self.durations = None
        self.isGif = False
        self.prmpImage = None
        self.imageFile = None
        self.loadDefault = loadDefault

        self.default_dp = PRMP_Image('profile_pix', inbuilt=True, for_tk=1)

        if bindMenu: self.bindMenu()

        if imageKwargs:
            imageKwargs['for_tk'] = 1
            self.after(imgDelay, lambda: self.loadImage(**imageKwargs))
            # self.loadImage(**imageKwargs)
        elif loadDefault: self.after(imgDelay, lambda: self.loadImage(self.default_dp))

        self.bind('<Configure>', lambda e: self.loadImage(event=e, **imageKwargs))

    def disabled(self):
        self.unBindMenu()
        super().disabled()

    def normal(self):
        self.bindMenu()
        super().normal()

    def loadImage(self, prmpImage=None, event=None, **kwargs):
        self.delMenu()
        self.isGif = False
        self.lastRender = time.time()
        
        self.frame_counter = 0
        _resize = (self.width, self.height)

        resize = kwargs.get('resize', _resize)
        kwargs['resize'] = _resize
        
        thumb = kwargs.get('thumb')

        name = kwargs.get('name')
        if not name: kwargs['name'] = f'{prmpImage}_{self.className}_{PRMP_ImageWidget.count}'

        # if not self.winfo_ismapped():
        #     self.after(50, lambda: self.loadImage(prmpImage, **kwargs))
        #     return

        try:
            if not isinstance(prmpImage, PRMP_Image):
                kwargs['for_tk'] = 1
                prmpImage = PRMP_Image(prmpImage, thumb=thumb, **kwargs)

            if isinstance(prmpImage, PRMP_Image):
                if not prmpImage.image: return
                
                if resize: self.imageFile = PRMP_Image(image=(prmpImage.resize(resize)), for_tk=1)
                else: self.imageFile = prmpImage.imageFile
            else: raise ValueError('prmpImage must be an instance of PRMP_Image')

            self.frame = self.prmpImage = prmpImage

            if prmpImage.ext == 'xbm':
                if resize: self.frame = prmpImage.resizeTk(resize)

            self.image = self.prmpImage.image

            if self.prmpImage.ext == 'gif':
                self.frames = []
                self.durations = []
                for frame in ImageSequence.Iterator(self.image):
                    if resize: frame = frame.resize(resize)
                    elif thumb: frame.thumbnail(thumb)
                    tkimg = PhotoImage(frame)
                    self.frames.append(tkimg)
                    self.durations.append(frame.info['duration'])
                if self.frames: self.frame = self.frames[self.frame_counter]

                self.isGif = True
                self.cancel_current_gif = True

                self.__renderGif(self.lastRender)

            
            elif resize: self.frame = self.prmpImage.resizeTk(resize)

            elif thumb: self.frame = self.prmpImage.thumbnailTk(thumb)

            else:
                if self.face: self.frame = self.prmpImage._find_faces(prmp_image=1, for_tk=1)

            self.config(image=self.frame)
            # self.paint()
        except ValueError as e:
            # print(e)
            self['image'] = None
            if self.loadDefault: self.loadImage(self.default_dp)
        except Exception as e:
            raise e
            pass
        
        if PRMP_ImageWidget.count > 1000: PRMP_ImageWidget.count = 0

        PRMP_ImageWidget.count += 1

    def __renderGif(self, magic=''):
        if not (self.isGif or self.frames or self.winfo_exists()): return

        if magic != self.lastRender: return
        
        # Update Frame
        self.frame = self.frames[self.frame_counter]
        self.config(image=self.frames[self.frame_counter])

        # Loop Counter
        self.frame_counter += 1
        if self.frame_counter >= len(self.frames): self.frame_counter = 0
        # self.after(self.durations[self.frame_counter], self.__renderGif)
        self.after(120, lambda: self.__renderGif(magic))

    def removeImage(self):
        self.delMenu()
        from .dialogs import PRMP_MsgBox

        PRMP_MsgBox(self, title='Profile Picture Removal', message='Are you sure you wanna remove the picture from this profile? ', callback=self._removeImage)

    def _removeImage(self, val):
        if val: self.loadImage()

    def set(self, imageFile=None, **kwargs):
        if imageFile: self.loadImage(imageFile, **kwargs)

    def changeImage(self, e=0):
        self.delMenu()
        from .dialogs import dialogFunc
        from .core_tk import picTypes
        file = dialogFunc(path=True, filetypes=picTypes)
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
    WidgetClass = PRMP_Label
    def __init__(self, master, **kwargs):
        # PRMP_Label.__init__(self, master, config=dict(anchor='center', **config), **kwargs)
        PRMP_ImageWidget.__init__(self, master, **kwargs)

IL = PRMP_ImageLabel

class PRMP_ImageSLabel(PRMP_ImageWidget, PRMP_Style_Label):
    WidgetClass = PRMP_Style_Label
    def __init__(self, master, **kwargs):
        # PRMP_Style_Label.__init__(self, master, config=dict(anchor='center', **config), **kwargs)
        PRMP_ImageWidget.__init__(self, master, **kwargs)

SIL = PRMP_ImageSLabel

class PRMP_ImageButton(PRMP_ImageWidget, PRMP_Button):
    WidgetClass = PRMP_Button
    def __init__(self, master, **kwargs):
        # PRMP_Button.__init__(self, master, config=dict(anchor='center', **config), **kwargs)
        PRMP_ImageWidget.__init__(self, master, **kwargs)

IB = PRMP_ImageButton

class PRMP_ImageSButton(PRMP_ImageWidget, PRMP_Style_Button):
    WidgetClass = PRMP_Style_Button
    def __init__(self, master, **kwargs):
        # PRMP_Style_Button.__init__(self, master, config=dict(**config), **kwargs)
        PRMP_ImageWidget.__init__(self, master, **kwargs)

ISB = PRMP_ImageSButton


class PRMP_ImageCheckbutton(PRMP_ImageWidget, PRMP_Checkbutton):
    WidgetClass = PRMP_Checkbutton
    def __init__(self, master, **kwargs):
        # PRMP_Checkbutton.__init__(self, master, config=dict(anchor='center', **config), **kwargs)
        PRMP_ImageWidget.__init__(self, master, **kwargs)

IB = PRMP_ImageCheckbutton

class PRMP_ImageSCheckbutton(PRMP_ImageWidget, PRMP_Style_Checkbutton):
    WidgetClass = PRMP_Style_Checkbutton
    def __init__(self, master, **kwargs):
        # PRMP_Style_Checkbutton.__init__(self, master, config=dict(**config), **kwargs)
        PRMP_ImageWidget.__init__(self, master, **kwargs)

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
        from .core_tk import picTypes
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
