
from PIL.ImageTk import Image, PhotoImage, BitmapImage
from PIL import ImageSequence
from .prmp_images import PRMP_PNGS, PRMP_GIFS, PRMP_XBMS
from .prmp_exts import *


class PRMP_Pics:
    _dir = 'prmp_pics'
    subDir = ''

    @classmethod
    def picsExt(cls):
        ext = cls.subDir[:-1]
        return ext.replace('prmp_', '')

    @classmethod
    def picsHome(cls): return os.path.join(os.path.dirname(__file__), cls._dir)

    @classmethod
    def picName(cls, pic): return os.path.splitext(os.path.basename(pic))[0]

    @classmethod
    def files(cls):
        _dir = os.path.join(cls.picsHome(), cls.subDir)
        _files = []

        for r, d, ff in os.walk(_dir):
            for f in ff:
                if f.endswith(cls.picsExt()):
                    _files.append(os.path.join(r, f))

        return _files

    @classmethod
    def filesDict(cls):
        files = cls.files()
        _filesDict = {cls.picName(file): file for file in files}
        return _filesDict

    @classmethod
    def get(cls, bitmap):
        filesL = cls.files()

        if isinstance(bitmap, int):
            try: return filesL[bitmap]
            except: filesL[0]
        elif isinstance(bitmap, str):
            files = cls.filesDict()
            try: return files[bitmap]
            except: filesL[0]

    @classmethod
    def get(cls, bitmap):
        filesL = cls.files()

        if isinstance(bitmap, int):
            try: return filesL[bitmap]
            except: filesL[0]
        elif isinstance(bitmap, str):
            files = cls.filesDict()
            try: return files[bitmap]
            except: filesL[0]

class PRMP_Xbms(PRMP_Pics): subDir = 'prmp_xbms'

class PRMP_Pngs(PRMP_Pics): subDir = 'prmp_pngs'

class PRMP_Gifs(PRMP_Pics): subDir = 'prmp_gifs'

class PRMP_Images:

    @classmethod
    def get(cls, inbuilt, ext):
        base64 = cls.getBase64(inbuilt, ext)
        return b64decode(base64)

    @classmethod
    def getBase64(cls,  inbuilt, ext):
        if ext == 'png': return PRMP_PNGS[inbuilt]
        elif ext == 'gif': return PRMP_GIFS[inbuilt]
        elif ext == 'xbm': return PRMP_XBMS[inbuilt]

class PRMP_ImageFile(PRMP_File):

    def getImageFile(self, pix, ext='.png', db=0):
        if isinstance(pix, str):
            e = os.path.splitext(pix)[-1]

            if e in ['.png', '.xbm', '.gif', '.jpg', '.jpeg']: self.ext = e[1:]
            else: self.ext = ext

            if db:
                if self.ext == 'png': pic = PRMP_Pngs.get(pix)
                elif self.ext == 'gif': pic = PRMP_Gifs.get(pix)
                elif self.ext == 'xbm': pic = PRMP_Xbms.get(pix)
            else: pic = pix
            self.name = pix
            self.basename = os.path.basename(pic)
            return pic

    def __init__(self, imageFileName='', inbuilt=False, inExt='png', image=None, **kwargs):

        passed = [bool(a) for a in [imageFileName, image]].count(True)
        assert passed <= 1, 'Only one is required in [imageFileName, image]'

        if imageFileName and inbuilt: kwargs['data'] = PRMP_Images.get(imageFileName, inExt)

        super().__init__(imageFileName, **kwargs)

        if image: image.save(self, inExt)

        PRMP_ImageFile.count += 1

class PRMP_Image:
    count = 0
    def __init__(self, filename='', inbuilt=False, inExt='png', resize=(), thumb=(), image=None, base64=b''):

        pic = None
        self.imageFile = None
        self.imgClass = PhotoImage
        self.resizedImage = None

        self._thumb = thumb
        self._resize = resize
        # print(base64)

        self.image = None
        self.tkImage = None
        self.name = ''
        self._animatedTkFrames = []
        self._animatedFrames = []

        if filename or image or base64:
            if filename:
                self.imageFile = filename if isinstance(filename, PRMP_ImageFile) else PRMP_ImageFile(filename, inbuilt=inbuilt, inExt=inExt)
            elif image: self.imageFile = PRMP_ImageFile(image=image)
            elif base64: self.imageFile = PRMP_ImageFile(base64=base64)
            else: self.imageFile = filename or image

            if not isinstance(self.imageFile, PRMP_ImageFile): raise ValueError('{} or {} is not a valid value.'.format(filename, image))

            self.name = self.imageFile.name
            self.ext = self.imageFile.ext

            if self.ext == 'xbm': self.imgClass = BitmapImage

            img = self.image = Image.open(self.imageFile)
            self.info = img.info

            if resize and len(resize) == 2 and resize[0] > 0 and resize[1] > 0: img = self.resizedImage = self.image.resize(resize)

            if thumb and len(thumb) == 2 and thumb[0] > 0 and thumb[1] > 0: img.thumbnail(thumb)

            self.img = img

            self.tkImage = self.imgClass(img, name=self.basename)

            PRMP_Image.count += 1

        else: raise ValueError('imageFile is None')

    def __str__(self): return str(self.tkImage)

    @property
    def animatedTkFrames(self):
        if self._animatedTkFrames: return self._animatedTkFrames
        else:
            for frame in ImageSequence.Iterator(self.img):
                if self._resize: img = frame.resize(self._resize)
                if self._thumb:
                    frame.thumbnail(self._thumb)
                    img = frame
                else: img = frame
                tkimg = self.imgClass(img)
                self._animatedTkFrames.append(tkimg)

            # for img in self.animatedFrames:
            #     tkimg = self.imgClass(img)
            #     self._animatedTkFrames.append(tkimg)
        return self._animatedTkFrames

    @property
    def animatedFrames(self):
        if self._animatedFrames: return self._animatedFrames
        else:
            for frame in ImageSequence.Iterator(self.img):
                print(99)
                if self._resize: img = frame.resize(self._resize)
                elif self._thumb:
                    frame.thumbnail(self._thumb)
                    img = frame
                else: img = frame
                self._animatedFrames.append(img)
            print(self._animatedFrames)
        return self._animatedFrames

    @property
    def interframe_durations(self): return [anf.info.get('duration', 0) for anf in self.animatedFrames]

    @property
    def basename(self):
        if self.imageFile: return self.imageFile.name
        return 'PRMP_Image(%d)'%dPRMP_Image.count

    def resize(self, rz): return self.image.resize(rz)

    def get(self): return self.imageFile

    def resizeTk(self, rz): return self.imgClass(self.resize(rz))

    def thumbnail(self, rz): self.image.thumbnail(rz)

    def thumbnailTk(self, rz):
        self.thumbnail(rz)
        return self.imgClass(self.image)






# tranxfer_c2 -D -A192.168.43.1 -P7767