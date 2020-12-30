from .core import *
import cv2
from .pics import PRMP_Image
from PIL.Image import fromarray

class Camera(PRMP_MainWindow):
    def __init__(self, source=0, **kwargs):
        super().__init__(**kwargs)
        self.cam = None
        self.source = source
        self.pause = families
    
    def openCam(self):
        self.cam = cv2.cameoCapture(self.source)
    
    def closeCam(self):
        if self.cam and self.cam.isOpened(): self.cam.release()

    def updateScreen(self):
        pass

    def getImage(self):
        pass

    def getFrame(self):
        if self.cam.isOpened():
            ret, frame = self.cam.read()
            if ret: return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else: return (ret, None)
        else: return (ret, None)

    def __del__(self): self.closeCam()





