from .dialogs import *
import cv2
from .pics import PRMP_Image, PhotoImage
from PIL.Image import fromarray

class Camera(PRMP_Dialog):
    def __init__(self, source=0, frameUpdateRate=10, title='Camera', **kwargs):
        self.cam = None
        self.source = source
        self.image = None
        self._image = None
        self.frameUpdateRate = frameUpdateRate


        super().__init__(title=title, **kwargs)
    
    def isMaximized(self): return self.getWid_H_W(self)
    
    def _setupDialog(self):
        self.x, self.y = self.geo

        self.screen = Label(self.container, place=dict(relx=.006, rely=.01, relh=.85, relw=.985))
        # self.screen = Label(self.container, place=dict(relx=.02, rely=.02, relh=.8, relw=.96))
        self.pause = SCheckbutton(self.container, place=dict(relx=.1, rely=.87, relh=.1, relw=.2), config=dict(text='Pause', command=self.pauseCam))
        self.pause.set('0')
        self.save = Button(self.container, config=dict(text='Save'))
        self.screen.bind('<Double-1>', self.pauseCam)

        # self.openCam()
    
    def placeSave(self): self.save.place(relx=.5, rely=.87, relh=.1, relw=.2)
    
    def pauseCam(self, o=0):
        if self.pause.get():
            self.pause.set('0')
            # self.updateScreen()
        else:
            self.pause.set('1')
            self.placeSave()
    
    def openCam(self):
        self.cam = cv2.VideoCapture(self.source)
        self.updateScreen()
    
    def closeCam(self):
        if self.cam and self.cam.isOpened(): self.cam.release()

    def snapshot(self):
        # Get a frame from the video source
        success, frame = self.getFrame()
        # if frame: cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    
    def updateScreen(self):
        if self.image: self.screen.config(image=self.image)
        # if self.image: self.screen['image'] = self.image
        del self.image
        self.image = None
        self.setImage()
        if not self.pause.get(): self.after(self.frameUpdateRate, self.updateScreen)

    def setImage(self):
        success, frame = self.getFrame()
        if success:
            self._image = fromarray(frame)
            # res = cv2.resize(img,(2*self.width, 2*self.height), interpolation = cv2.INTER_CUBIC)
            # self._image
            image = self._image.copy()
            # image.resize(self.isMaximized())
            image.thumbnail((self.x-30, self.y-60))
            self.image = PhotoImage(image=image)
        else: print('Read Error')

    def getFrame(self):
        if self.cam and self.cam.isOpened():
            success, frame = self.cam.read()
            if success: return (success, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else: return (success, None)
        else: return (False, None)

    def __del__(self): self.closeCam()








