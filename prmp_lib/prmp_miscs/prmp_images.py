

__all__ = ['PRMP_PNGS', 'PRMP_JPEGS', 'PRMP_GIFS', 'PRMP_XBMS', 'PRMP_Images', 'PRMP_ImageFile', 'PRMP_Image', 'PRMP_File', 'io', 'os', 'base64', 'zlib', 'pickle', 'PRMP_ImageType', 'Image', 'PhotoImage', 'BitmapImage', 'ImageSequence', 'PRMP_IMAGES']

from .pyized_images import *

try:
    from PIL.ImageTk import Image, PhotoImage, BitmapImage
    from PIL import Image, ImageDraw, ImageSequence
    from PIL import ImageGrab
    _PIL_ = True
except Exception as e:
    _PIL_ = False
    print('PIL <pillow> image library is not installed.')
    print(e)

try:
    import cv2
    _CV2_ = True
except Exception as e:
    _CV2_ = False
    print('cv2 <opencv-python> computer vision library is not installed.')
    print(e)

try:
    import cv2
    _CV2_ = True
except Exception as e:
    _CV2_ = False
    print('cv2 <opencv-python> computer vision library is not installed.')
    print(e)

from .prmp_exts import *
from .prmp_mixins import PRMP_AdvMixins


class PRMP_ImageType:

    tests = []

    def test_jpeg(data):
        """JPEG data in JFIF or Exif format"""
        if data[6:10] in (b'JFIF', b'Exif'):
            return 'jpeg'

    tests.append(test_jpeg)

    def test_png(data):
        if data.startswith(b'\211PNG\r\n\032\n'):
            return 'png'

    tests.append(test_png)

    def test_gif(data):
        """GIF ('87 and '89 variants)"""
        if data[:6] in (b'GIF87a', b'GIF89a'):
            return 'gif'

    tests.append(test_gif)

    def test_tiff(data):
        """TIFF (can be in Motorola or Intel byte order)"""
        if data[:2] in (b'MM', b'II'):
            return 'tiff'

    tests.append(test_tiff)

    def test_rgb(data):
        """SGI image library"""
        if data.startswith(b'\001\332'):
            return 'rgb'

    tests.append(test_rgb)

    def test_pbm(data):
        """PBM (portable bitmap)"""
        if len(data) >= 3 and \
            data[0] == ord(b'P') and data[1] in b'14' and data[2] in b' \t\n\r':
            return 'pbm'

    tests.append(test_pbm)

    def test_pgm(data):
        """PGM (portable graymap)"""
        if len(data) >= 3 and \
            data[0] == ord(b'P') and data[1] in b'25' and data[2] in b' \t\n\r':
            return 'pgm'

    tests.append(test_pgm)

    def test_ppm(data):
        """PPM (portable pixmap)"""
        if len(data) >= 3 and \
            data[0] == ord(b'P') and data[1] in b'36' and data[2] in b' \t\n\r':
            return 'ppm'

    tests.append(test_ppm)

    def test_rast(data):
        """Sun raster file"""
        if data.startswith(b'\x59\xA6\x6A\x95'):
            return 'rast'

    tests.append(test_rast)

    def test_xbm(data):
        """X bitmap (X10 or X11)"""
        if data.startswith(b'#define '):
            return 'xbm'

    tests.append(test_xbm)

    def test_bmp(data):
        if data.startswith(b'BM'):
            return 'bmp'

    tests.append(test_bmp)

    def test_webp(data):
        if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
            return 'webp'

    tests.append(test_webp)

    def test_exr(data):
        if data.startswith(b'\x76\x2f\x31\x01'):
            return 'exr'

    tests.append(test_exr)

    @classmethod
    def get(cls, file=None, data=b'', b64=b'', image=None):
        if file:
            if isinstance(file, (str, bytes)): file = open(file, 'rb')
            data = file.read(32)
        elif b64: data = base64.b64decode(b64)
        elif image:
            file = io.BytesIO()
            image.save(file)
            data = file.getvalue()

        if data:
            _needed = data[:32]
            return cls._get(_needed)

    @classmethod
    def _get(cls, data):
        for test in cls.tests:
            ext = test(data)
            if ext: return ext

class PRMP_Images:
    @classmethod
    def grabscreen(cls, bbox=None):
        if not _PIL_: return
        return ImageGrab.grab(bbox)
    @classmethod
    def grabclipboard(cls):
        if not _PIL_: return
        return ImageGrab.grabclipboard()
    @classmethod
    def rgb2hex(cls, color):
        ''' To get the hex value of a color in rgb format

        :param color: a list containing the values of the rgb
        :type color: list
        '''
        color = [int(a) for a in color]
        f, s, t = color
        return "#{:02x}{:02x}{:02x}".format(f, s, t)
    
    @classmethod
    def get_colors_percent(cls, freq, colors):
        ''' To get the dict containing colors and their percentages.

        :param freq: a list containing the frequencies of each color in colors
        :type image: list

        :param colors: a list containing the colors
        :type colors: list
        '''
        total = sum(freq)
        percent = [int(val/total*100) for val in freq]
        hex_pers = dict(zip(colors, percent))

        return hex_pers

    @classmethod
    def get_most_common(cls, colors):
        ''' To get the color with the max percentage.

        :param colors: a dict containing the colors and their percentages of occurrence
        :type colors: dict
        '''

        _max = max(list(colors.values()))
        for k in colors:
            if colors[k] == _max: return k

    @classmethod
    def get_colors(cls, image, numcolors=10, resize=150, inhex=0, most_common=0, percent=0):
        ''' To get the colors in an image.

        :param image: an image or a str or bytes to an image file
        :type image: [str, bytes, Image]

        :param numcolors: number of colors to return
        :type numcolors: int

        :param resize: an int to resize the image to speed up the process
        :type resize: int
        
        :param inhex: bool whether to return the colors in hex
        :type inhex: bool
        
        :param most_common: bool whether to return only the most common color
        :type most_common: bool
        
        :param percent: bool whether to return colors with the frequency (percentages)
        :type percent: bool
        '''
        if not _PIL_: return
        # Resize image to speed up processing
        img = Image.open(image) if isinstance(image, (str, bytes)) else image
        if resize: img.thumbnail((resize, resize))

        # Reduce to palette
        paletted = img.convert('P', palette=Image.ADAPTIVE, colors=numcolors)

        # Find colors
        palette = paletted.getpalette()
        color_counts = sorted(paletted.getcolors(), reverse=True)

        frequency = [a[0] for a in color_counts]

        colors = []
        for i in range(numcolors):
            palette_index = color_counts[i][1]
            start = palette_index*3
            dominant_color = palette[start:start+3]
            colors.append(tuple(dominant_color))
        
        if inhex: colors = [cls.rgb2hex(c) for c in colors]
        
        colors_percent = cls.get_colors_percent(frequency, colors)

        if most_common: colors = cls.get_most_common(colors_percent)
        
        if percent: colors = colors_percent

        return colors
    
    @classmethod
    def save_palette(colors, swatchsize=20, outfile="palette.png" ):
        ''' To write the dict or list colors into an image.
        :param colors: list of colors or dict of colors with the colors as the keys.
        :type colors: list, tuple, dict

        :param swatchsize: the size of each rectangle of the colors.
        :type swatchsize: int

        :param outfile: path to save the image to.
        :type outfile: str, bytes
        '''
        if not _PIL_: return
        num_colors = len(colors)
        palette = Image.new('RGB', (swatchsize*num_colors, swatchsize))
        draw = ImageDraw.Draw(palette)

        posx = 0
        for color in colors:
            draw.rectangle([posx, 0, posx+swatchsize, swatchsize], fill=color) 
            posx = posx + swatchsize

        del draw
        palette.save(outfile, "PNG")

    @classmethod
    def images_into_py(cls, folder='.', pyfile='pyized_images.py', merge={}, prefix='PRMP', space=10, add_all=0):
        '''
        _author_ = PRMPSmart

        :param folder: a str path to a folder.
        :param pyfile: a str path to a python file to host the images.
        :param merge: a dict as follows ->
            {'png':
                {'image_1': image_1_data, 'image_2': image_2_data}, 
            'jpg':
                {'image_3': image_3_data, 'image_4': image_4_data}
            }
        :param prefix: name use as prefix of the ensuing dicts.
        :param space: space to leave before the next variable.
        '''
        # to avoid error in the first instance of working with merge
        space = '\n' * space

        if not merge: merge = {}

        pixs = {}
        for fd in os.listdir(folder):
            # joining to make full path
            pp = os.path.join(folder, fd)
            if os.path.isfile(pp):
                # get image type
                ext = PRMP_ImageType.get(pp)
                # get usable name
                name = PRMP_Exts.getname(os.path.basename(pp))

                if ext:
                    # if it exists already
                    if ext in pixs:
                        ext_dict = pixs[ext]
                        ext_dict[name] = pp
                    # if not
                    else:
                        ext_dict = {name: pp}
                        pixs[ext] = ext_dict
        
        # merging
        for ext, value_dicts in merge.items():
            # if some image type of merge exists in then pixs
            if ext in pixs:
                pixs_own = pixs[ext]
                # this will overwrite the image with same name as those in merge
                merge_own = value_dicts.copy()
                merge_own.update(pixs_own)
                pixs[ext] = merge_own
            # if not
            else: pixs[ext] = value_dicts

        pyfile = open(pyfile, 'w')
        
        if add_all:
            keys = [prefix + '_' + k.upper() + 'S' for k in pixs.keys()]
            _all_ = '__all__ = {}{}'.format(keys, space)
            pyfile.write(_all_)

        exts = {}
        for k, v in pixs.items():
            exts[k] = []

            for name, file_data in v.items():
                _dict = {'name': ''}
                if (k in merge) and (name in merge[k]) and (file_data == merge[k][name]):
                    _dict['name'] = name
                    _dict['data'] = 1

                splits = PRMP_Exts.getsplits(file_data, **_dict)

                exts[k].append(name)
                keys = splits.keys()

                more = len(keys) > 1

                sp = '\n\n' if more else space

                for key, val in splits.items(): pyfile.write("{} = {}{}".format(key, val, sp))

                if len(keys) > 1: pyfile.write("{} = {}{}".format(name, ' + '.join(keys), space))


        for ext, names in exts.items():
            EXTS = prefix + '_' + ext.upper() + 'S = {'
            for name in names: EXTS += "'{}': {}, ".format(name, name)
            EXTS = EXTS[:-2]
            EXTS += '}' + space
            pyfile.write(EXTS)
        
        pyfile.close()

    @classmethod
    def get(cls, inbuilt, ext, decode=0):
        _base64 = cls.getBase64(inbuilt, ext)
        if _base64:
            if decode: return base64.b64decode(_base64)
            return _base64

    @classmethod
    def getBase64(cls,  inbuilt, ext):
        exts = f'PRMP_{ext.upper()}S'
        glob = globals()
        if exts in glob:
            exts_all = glob[exts]
            if inbuilt in exts_all: return exts_all[inbuilt]

class PRMP_ImageFile(PRMP_File):

    @property
    def image(self):
        if not _PIL_: return
        return Image.open(self)

    def __init__(self, imageFileName='', inbuilt=False, inExt='png', image=None, array=None, **kwargs):
        isArray = self.isArray(array)
        passed = [bool(a) for a in [imageFileName, image, isArray]].count(True)
        assert passed <= 1, 'Only one is required in [imageFileName, image]'

        if imageFileName and inbuilt: kwargs['b64'] = PRMP_Images.get(imageFileName, inExt)

        super().__init__(filename=imageFileName, **kwargs)

        if isArray and _PIL_: image = Image.fromarray(array)
        if image: image.save(self, inExt)

        PRMP_ImageFile.count += 1
    
    @property
    def ext(self): return PRMP_ImageType.get(self)

class PRMP_Image:
    count = 0
    def __init__(self, filename='', inbuilt=False, inExt='png', resize=(), thumb=(), image=None, b64=b'', name='', for_tk=False, array=None):

        pic = None
        self.imageFile = None

        self.resizedImage = None

        self._thumb = thumb
        self._resize = resize

        self.image = image
        self.for_tk = for_tk
        self.tkImage = None

        filename = filename or ''

        isArray = PRMP_AdvMixins.isArray(None, array)
        
        self.name = name or PRMP_Exts.getname(str(filename))

        self._animatedTkFrames = []
        self._animatedFrames = []

        if filename or image or b64 or isArray:
            if image: self.imageFile = PRMP_ImageFile(filename, image=image)
            
            elif b64: self.imageFile = PRMP_ImageFile(filename, b64=b64)
            
            elif isArray: self.imageFile = PRMP_ImageFile(filename, array=array)
            
            else: self.imageFile = PRMP_ImageFile(filename, inbuilt=inbuilt, inExt=inExt)
            
            # else: self.imageFile = PRMP_ImageFile(filename)

            if not isinstance(self.imageFile, (PRMP_ImageFile, str)): raise ValueError('{} or {} is not a valid value.'.format(filename, image))

            self.ext = self.imageFile.ext

            if _PIL_:
                if self.ext == 'xbm': self.tkImgClass = BitmapImage
                else: self.tkImgClass = PhotoImage
            else:
                import tkinter as tk
                self.tkImgClass = tk.PhotoImage
                if self.ext == 'xbm': self.tkImgClass = tk.BitmapImage

            img = self.image = self.image or Image.open(self.imageFile) if _PIL_ else None

            self.frames = getattr(img, 'n_frames', 1)
            
            if img: self.info = img.info

            if resize and len(resize) == 2 and resize[0] > 0 and resize[1] > 0: img = self.resizedImage = img.resize(resize)

            if thumb and len(thumb) == 2 and thumb[0] > 0 and thumb[1] > 0: img.thumbnail(thumb)

            self.img = img

            if self.for_tk: self.createTkImage(self.name)

            PRMP_Image.count += 1

        else: raise ValueError('imageFile is None')
    
    def createTkImage(self, name=''):
        self.tkImage = self.tkImgClass(self.img, name=name or self.name or self.name_n_ext)
        return self.tkImage

    def __str__(self):
        if self.for_tk: return str(self.tkImage)

        return self.name

    @property
    def animatedTkFrames(self):
        if not _PIL_: return

        if self._animatedTkFrames: return self._animatedTkFrames
        else:
            for frame in ImageSequence.Iterator(self.img):
                if self._resize: img = frame.resize(self._resize)
                if self._thumb:
                    frame.thumbnail(self._thumb)
                    img = frame
                else: img = frame
                tkimg = self.tkImgClass(img)
                self._animatedTkFrames.append(tkimg)

            # for img in self.animatedFrames:
            #     tkimg = self.tkImgClass(img)
            #     self._animatedTkFrames.append(tkimg)
        return self._animatedTkFrames

    @property
    def animatedFrames(self):
        if not _PIL_: return
        if self._animatedFrames: return self._animatedFrames
        else:
            for frame in ImageSequence.Iterator(self.img):
                if self._resize: img = frame.resize(self._resize)
                elif self._thumb:
                    frame.thumbnail(self._thumb)
                    img = frame
                else: img = frame
                self._animatedFrames.append(img)
        return self._animatedFrames

    @property
    def interframe_durations(self): return [anf.info.get('duration', 0) for anf in self.animatedFrames]

    @property
    def name_n_ext(self):
        if self.imageFile: return self.imageFile.name_n_ext
        else: return self.basename

    @property
    def basename(self):
        if self.imageFile: return self.imageFile.basename
        return 'PRMP_Image(%d)'%PRMP_Image.count

    def resize(self, rz): return self.image.resize(rz)

    def get(self): return self.imageFile

    def resizeTk(self, rz): return self.tkImgClass(self.resize(rz))

    def thumbnail(self, rz): self.image.thumbnail(rz)

    def thumbnailTk(self, rz):
        self.thumbnail(rz)
        return self.tkImgClass(self.image)

    def copy(self):
        if self.image: return self.image.copy()
    
    def fromarray(self, array, bgr2rgb=False):
        if _CV2_ and bgr2rgb: array = cv2.cvtColor(array, cv2.COLOR_BGR2RGB)
        self.image = Image.fromarray(array)


    def toarray(self, rgb2bgr=False):
        if not self.image: return

        import numpy
        array = numpy.asarray(self.image)
        if _CV2_ and rgb2bgr: array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        return array

    def _find_faces(self, **kwargs): return self.find_faces(image=self.image, **kwargs)
    
    @classmethod
    def find_faces(cls, cascPath='', image=None, array=None, as_image=False, prmp_image=False, **kwargs):
        if not _CV2_: return

        cascPath = cascPath or r"C:\Users\Administrator\Documents\My\Archives\libraries\python\cv2\data\haarcascade_frontalface_default.xml"

        faceCascade = cv2.CascadeClassifier(cascPath)

        if image: array = cls(image=image).toarray()
        
        gray = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            #flags = cv2.CV_HAAR_SCALE_IMAGE
        )
        # print("Found {0} faces!".format(len(faces)))

        for (x, y, w, h) in faces: cv2.rectangle(array, (x, y), (x+w, y+h), (0, 255, 0), 2)

        if as_image or prmp_image:
            cl = PRMP_Image if prmp_image else PRMP_ImageFile
            return cl(array=array, **kwargs)
        else: return array







# tranxfer_c2 -D -A192.168.43.1 -P7767