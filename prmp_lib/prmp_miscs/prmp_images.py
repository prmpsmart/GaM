

__all__ = ['PRMP_PNGS', 'PRMP_JPEGS', 'PRMP_GIFS', 'PRMP_XBMS', 'PRMP_Images', 'PRMP_ImageFile', 'PRMP_Image', 'PRMP_File', 'io', 'os', 'base64', 'zlib', 'pickle', 'PRMP_ImageType', 'Image', 'PhotoImage', 'BitmapImage', 'ImageSequence', 'PRMP_IMAGES', 'PRMP_ImagesDB', 'PRMP_DB']

from ._prmp_images import *
import sqlite3, base64, os, tkinter as tk, numpy


try:
    from PIL.ImageTk import Image, PhotoImage, BitmapImage
    from PIL import Image, ImageDraw, ImageSequence
    from PIL import ImageGrab
    _PIL_ = True
except Exception as e:
    _PIL_ = False
    print('PIL <pillow> image library is not installed.')

try:
    import cv2
    _CV2_ = True
except Exception as e:
    _CV2_ = False
    print('cv2 <opencv-python> computer vision library is not installed.')

try:
    import cv2
    _CV2_ = True
except Exception as e:
    _CV2_ = False
    print('cv2 <opencv-python> computer vision library is not installed.')

from .prmp_exts import *
from .prmp_mixins import PRMP_AdvMixins, PRMP_StrMixins



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
    def images_into_py(cls, folder='', files=[], pyfile='pyized_images.py', merge={}, prefix='PRMP', space=10, add_all=0):
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
        if not prefix.endswith('_'): prefix += '_'
        prefix += '%sS'

        pixs = {}
        if folder or files:
            _files = files.copy()
            del files

            if folder:
                for file in os.listdir(folder):
                    file = os.path.join(folder, file)
                    if PRMP_ImageType.get(file): _files.append(file)
            
            for file in _files:
                # get image type
                ext = PRMP_ImageType.get(file)
                # get usable name
                name = PRMP_Exts.getname(file)

                if ext:
                    # if it exists already
                    if ext in pixs:
                        ext_dict = pixs[ext]
                        ext_dict[name] = file
                    # if not
                    else:
                        ext_dict = {name: file}
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
            keys = list(pixs.keys())
            keys.extend(['image', 'images_list'])
            keys = [prefix % k.upper() for k in keys]
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
            EXTS = prefix % ext.upper() + ' = {'
            for name in names: EXTS += "'{}': {}, ".format(name, name)
            EXTS = EXTS[:-2]
            EXTS += '}' + space
            pyfile.write(EXTS)
        
        IMAGES = prefix % 'IMAGE' + ' = {'
        for ext in exts:
            EXT = prefix % ext.upper()
            IMAGES += "'{}': {}, ".format(ext, EXT)
        IMAGES = IMAGES[:-2]
        IMAGES += '}' + space
        pyfile.write(IMAGES)

        IMAGES_LISTS = prefix % 'IMAGE' + '_LISTS = ['
        bb = [prefix % ext.upper() for ext in exts]
        for b in bb: IMAGES_LISTS += b + ', '
        IMAGES_LISTS = IMAGES_LISTS[:-2]
        IMAGES_LISTS += ']' + space
        pyfile.write(IMAGES_LISTS)

        # for ext in exts:

        
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


class PRMP_ImagesDB(PRMP_AdvMixins, PRMP_StrMixins):
    defaultDB = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'images_db.prmp_db')

    @classmethod
    def PRMP_DB(cls): return cls(cls.defaultDB)

    @classmethod
    def _open(cls, db_file, cursor=False):
        '''opens a connection
        db_file: path for the file or :memory:
        cursor: bool whether to return cursor or connection
        '''

        connection = sqlite3.connect(db_file)
        if cursor: return connection.cursor()
        else: return connection

    @classmethod
    def _getConnection(cls, db_file='', cursor=None):
        '''returns a connection
        db_file: path for the file or :memory:
        cursor:  cursor object
        '''
        if cursor: connection = cursor.connection
        elif db_file: connection = cls._open(db_file)
        return connection

    @classmethod
    def _getCursor(cls, db_file='', connection=None):
        '''returns a cursor
        db_file: path for the file or :memory:
        connection: connection object
        '''
        if connection: cursor = connection.cursor()
        elif db_file: cursor = cls._open(db_file, 1)

        return cursor

    @classmethod
    def _getName(cls, name):
        'strips the name to something modest'
        name = os.path.basename(name)
        name = os.path.splitext(name)[0]
        return name

    @classmethod
    def _getImagesDict(cls, images_folder, sub_folders=0):
        'returns dict of folders of images in a folder using their folder as their collective keys'
        
        images_folders = [images_folder]
        if sub_folders:
            for folder in os.listdir(images_folder):
                folder = os.path.join(images_folder, folder)
                if os.path.isdir(folder): images_folders.append(folder)

        dicts = {}
        for folder in images_folders:
            files = []
            for file in os.listdir(folder):
                file = os.path.join(folder, file) 
                if os.path.isfile(file) and PRMP_ImageType.get(file): files.append(file)
            dicts[folder] = files
        return dicts
    
    @classmethod
    def _createDB(cls, db_file, images_dict):
        'initialize the database with the folders(keys) in the images_dict'
        # creating the tables
        _tbs = images_dict.keys()
        tables = [cls._getName(table)for table in _tbs]
        
        cursor = cls._open(db_file, 1)
        for table in tables: cursor.execute(f'CREATE TABLE {table} (name TEXT, ext TEXT, data BLOB)')

        cls._fillDB(cursor, images_dict)
        return cursor
    
    @classmethod
    def _getData(cls, file): return open(file, 'rb').read()
    
    @classmethod
    def _fillDB(cls, cursor, images_dict):
        'fills the database with the images.'
        _tbs = images_dict.keys()
        _tabs = [cls._getName(table) for table in _tbs]
        tables = dict(zip(_tabs, _tbs))

        for table, table_path in tables.items():
            images_paths = images_dict[table_path]
            # formatting the files
            _filed = [cls._getName(file) for file in images_paths]
            images_named = tuple(zip(_filed, images_paths))
            
            values = []
            for name, image_path in images_named:
                value = (name, PRMP_ImageType.get(image_path), cls._getData(image_path))
                values.append(value)
            
            cursor.executemany(f'INSERT INTO {table} VALUES (?,?,?)', values)

        cursor.connection.commit()
        cursor.connection.close()
    

    @classmethod
    def _createImageDB(cls, db_file, images_folder, sub_folders=False, obj=False):
        '''
        db_file: database path or :memory:
        images_folder: folder path to create database for
        sub_folders: bool, whether to recurse into the folders in the images_folder
        obj: bool, whether to return an instance of PRMP_IMageDB
        '''
        images_dict = cls._getImagesDict(images_folder, sub_folders)

        cursor = cls._createDB(db_file, images_dict)
        
        if not obj: return cls(db_file)

        return cursor

    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = self._open(db_file)
        self.cursor = self.connection.cursor()
    
    def addImages(self, images_folder, sub_folders=False): self._createImageDB(self.db_file, images_folder, sub_folders, 1)

    @classmethod
    def _getPRMPImage(cls, name, ext, data):
        'returns an instance of PRMP_ImageFile from the database data'
        return PRMP_ImageFile(f'{name}.{ext}', data=data)

    @classmethod
    def _getPRMPImages(cls, images):
        'returns instances of PRMP_ImageFile from the database datas'
        prmpImages = []
        for tups in images:
            if tups:
                img = cls._getPRMPImage(*tups)
                prmpImages.append(img)
        return prmpImages
    
    @classmethod
    def _getImage(cls, table, name, raw=0, cursor=None, **kwargs):
        if not cursor: cursor = cls._getCursor(**kwargs)
        t = (name,)

        cursor.execute(f'SELECT * FROM {table} WHERE name=?', t)
        images = list(cursor)
        
        if not raw: images = cls._getPRMPImages(images)
        return images
    
    def getImage(self, table, name, raw=0):
        return self._getImage(table, name, raw, cursor=self.cursor)
    
    @classmethod
    def _getImages(cls, images_dict, **kwargs):
        '''
        images_dict: {table: [images]}
        '''

        tables_images = {}
        for table, images in images_dict.items():
            table_images = []
            
            if images:
                for image in images: table_images.extend(cls._getImage(table, image, **kwargs))
            else: table_images.extend(cls._getTable(table, **kwargs))

            tables_images[table] = table_images
        
        return tables_images

    def getImages(self, images_dict, **kwargs):
        return  self._getImages(images_dict, cursor=self.cursor)
    
    @classmethod
    def _getTable(cls, table, cursor=None, raw=0, **kwargs):
        if not cursor: cls.getCursor(**kwargs)
        cursor.execute(f'SELECT * FROM {table}')
        images = list(cursor)

        if not raw: images =  cls._getPRMPImages(images)
        return images

    def getTable(self, table, raw=0): return self._getTable(table, raw=raw, cursor=self.cursor)
    
    def saveImage(self, table, name, file_path=None):
        image = self.getImage(table, name)
        if image: image = image[0]
        image.save(file_path)

    def saveTable(self, table, folder=''):
        folder = folder or table
        if folder:
            try: os.mkdir(folder)
            except: pass
        os.chdir(folder)
        
        images = self.getTable(table)
        for image in images: image.save()
    
    def saveAll(self, folder=''):
        if folder:
            try: os.mkdir(folder)
            except: pass
        os.chdir(folder)

    def addImage(self, table, file):
        pass

    def addTable(self, images_folder): self.addImages(images_folder, 0, 1)
    
    def addTables(self, images_folder): self.addImages(images_folder, 1, 1)

    @classmethod
    def _tableNames(cls, connection=None, **kwargs):
        if not connection: connection = cls._getConnection(**kwargs)
        table_names = list(connection.execute("SELECT NAME FROM SQLITE_MASTER WHERE TYPE='table' ORDER BY NAME"))
        names = [name[0] for name in table_names]
        return names

    @classmethod
    def _tableImages(cls, table, connection=None, **kwargs):
        if not connection: connection = cls._getConnection(**kwargs)
        table_images = list(connection.execute(f"SELECT name FROM {table} ORDER BY name"))
        images = [images[0] for images in table_images]
        return images
    
    @property
    def tableNames(self): return self._tableNames(connection=self.connection)
    
    def tableImages(self, table): return self._tableImages(table, connection=self.connection)

    @classmethod
    def _debugDB(cls, db_file='', connection=None, **kwargs):

        if not connection: connection = cls._getConnection(db_file=db_file, **kwargs)

        dir_ = db_file + '_datas'
        try: os.mkdir(dir_)
        except: pass

        schema = open(os.path.join(dir_, 'schema.txt'), 'w')
        tableNames = cls._tableNames(connection=connection)
        
        for tableName in tableNames:
            # '''
            schema.write("\n{}:\n".format(tableName))
            for (columnID, columnName, columnType,  columnNotNull, columnDefault, columnPK) in connection.execute("PRAGMA table_info('{}');".format(tableName)):
                
                schema.write("    id={id}, name={name}, type={type}, null={null}, default={default}, pk={pk}\n\n".format(
                    id=columnID,
                    name=columnName,
                    type=columnType if columnType else "''",
                    null=" not null" if columnNotNull else "''",
                    default=" [{}]".format(columnDefault) if columnDefault else "''",
                    pk=" *{}".format(columnPK) if columnPK else "''",
                ))
                fi = open(os.path.join(dir_, tableName + '.txt'), 'w')
                for columns in connection.execute('SELECT * FROM '+ tableName):
                    # IMAGEDB hack
                    name, ext, data = columns

                    size = len(data)
                    _ext = 'Bs'
                    byte = 1024.0

                    if size > byte-1:
                        size /= byte
                        _ext = 'Kbs'

                    if size > byte-1:
                        size /=  byte
                        _ext = 'Mbs'

                    if size > byte-1:
                        size /=  byte
                        _ext = 'Gbs'
                    
                    size = cls.decimalPlace(None, size, 2)
                    
                    columns = name, ext, f'{size} {_ext}'
                    # IMAGEDB hack
                    
                    fi.write(str(columns) + '\n')
                
            if 'segdir' in tableName:
                for columns in connection.execute('SELECT * FROM '+ tableName):
                    if 'segdir' in tableName:
                        print(str(columns[-1]), '\n'*3)
                # break

    def debugDB(self): self._debugDB(self.db_file, connection=self.connection)

    @classmethod
    def _createPyizedImage(cls, images_dict, pyfile='pyized_from_db.py', pyizedKwargs={}, **kwargs):
        
        tables_images = cls._getImages(images_dict, **kwargs)
        images = []

        for i in tables_images.values(): images.extend(i)

        PRMP_Images.images_into_py(files=images, pyfile=pyfile, **pyizedKwargs)

    def createPyizedImage(self, images_dict, py_file='pyized_from_db.py', **kwargs): return self._createPyizedImage(images_dict, py_file=py_file, cursor=self.cursor, **kwargs)


class PRMP_ImageFile(PRMP_File):

    @property
    def image(self):
        if not _PIL_: return
        d = self.class_(data=self.data)
        
        return Image.open(d)

    def __init__(self, imageFileName='', inbuilt=False, inExt='png', image=None, array=None, **kwargs):
        isArray = self.isArray(array)
        passed = [bool(a) for a in [imageFileName, image, isArray]].count(True)
        assert passed <= 2, 'Only one is required in [array, image]'

        if imageFileName and inbuilt: kwargs['b64'] = PRMP_Images.get(imageFileName, inExt)
        self._ext = ''

        super().__init__(filename=imageFileName, **kwargs)

        if isArray and _PIL_: image = Image.fromarray(array)
        if image: image.save(self, inExt)

    @property
    def ext(self):
        if not self._ext: self._ext = PRMP_ImageType.get(self)
        return self._ext
    
    def save(self, file=None):
        if not file: file = self.name
        if not os.path.splitext(file)[1]: file += '.'+self.ext
        super().save(file)


class PRMP_Image:
    count = 0
    def __init__(self, filename='', inbuilt=False, inExt='png', resize=(), thumb=(), image=None, b64=b'', name='', for_tk=False, array=None):

        pic = None
        self.imageFile = None
        self.tkImgClass = None

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
            if not isinstance(filename, (PRMP_ImageFile)):
                if image: self.imageFile = PRMP_ImageFile(filename, image=image)
                
                elif b64: self.imageFile = PRMP_ImageFile(filename, b64=b64)
                
                elif isArray: self.imageFile = PRMP_ImageFile(filename, array=array)
                
                else: self.imageFile = PRMP_ImageFile(filename, inbuilt=inbuilt, inExt=inExt)
            else: self.imageFile = filename
                
            self.ext = self.imageFile.ext

            try: img = self.image = self.image or Image.open(self.imageFile) if _PIL_ else None
            except Exception as e: print(e); return None

            self.frames = getattr(img, 'n_frames', 1)
            
            if img: self.info = img.info

            if resize and len(resize) == 2 and resize[0] > 0 and resize[1] > 0: img = self.resizedImage = img.resize(resize)

            if thumb and len(thumb) == 2 and thumb[0] > 0 and thumb[1] > 0: img.thumbnail(thumb)

            self.img = img

            self.setTkImgClass()
            if self.for_tk: self.createTkImage(self.name)

            PRMP_Image.count += 1

        else: raise ValueError('imageFile is None')
    
    def setTkImgClass(self):
        if _PIL_:
            if self.ext == 'xbm': self.tkImgClass = BitmapImage
            else: self.tkImgClass = PhotoImage
        else:
            self.tkImgClass = tk.PhotoImage
            if self.ext == 'xbm': self.tkImgClass = tk.BitmapImage

    def createTkImage(self, name=''):
        self.setTkImgClass()
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

    def resizeTk(self, rz): return self.tkImgClass(self.resize(rz)) if self.tkImgClass else None

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

        array = numpy.asarray(self.image)
        if _CV2_ and rgb2bgr: array = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
        return array

    def _find_faces(self, **kwargs): return self.find_faces(image=self.image, **kwargs)
    
    @classmethod
    def find_faces(cls, cascPath='', image=None, array=None, as_image=False, prmp_image=False, **kwargs):
        if not _CV2_: return

        cascPath = cascPath or r"C:\Users\Administrator\Documents\My\Programming\Third Party Applications\libraries\python\cv2\data\haarcascades\haarcascade_frontalface_default.xml"

        faceCascade = cv2.CascadeClassifier(cascPath)

        if image: array = cls(image=age).toarray()
        
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

PRMP_DB = None

if 'PRMP_DB' in os.environ:
    try: PRMP_DB = PRMP_ImagesDB.PRMP_DB()
    except: pass





