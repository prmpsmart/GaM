from .dialogs import *
import cv2
from .pics import *
from PIL.Image import fromarray

class Camera(PRMP_Dialog):
    

    def __init__(self, source=0, frameUpdateRate=10, title='Camera', **kwargs):
        self.cam = None
        self.source = source
        self.image = None
        self._image = None
        self.pause = False

        self.frameUpdateRate = frameUpdateRate

        super().__init__(title=title, **kwargs)
    
    def isMaximized(self): return self.getWid_H_W(self)

    def _setupDialog(self):
        self.x, self.y = self.geo

        self.screen = Label(self.container, place=dict(relx=.006, rely=.01, relh=.85, relw=.985))
        self.screen.bind('<Double-1>', self.screenPause)

        self.save = Button(self.container, config=dict(text='Save', command=self.saveImage))

        self.openCam()
    
    def placeSave(self): self.save.place(relx=.375, rely=.87, relh=.1, relw=.25)

    def screenPause(self, e=0):
        if self.pause:
            self.pause = False
            self.openCam()
            self.save.place_forget()
        else:
            self.pause = True
            self.closeCam()
            self.placeSave()
    
    def saveImage(self):
        data = self.getImageData(self._image)
        self._setResult(data)
        if self._return: self.destroy()

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
        if not self.pause: self.after(self.frameUpdateRate, self.updateScreen)

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
        
        # else: print('Read Error')

    def getFrame(self):
        if self.cam and self.cam.isOpened():
            success, frame = self.cam.read()
            if success: return (success, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else: return (success, None)
        else: return (False, None)

    def __del__(self): self.closeCam()








