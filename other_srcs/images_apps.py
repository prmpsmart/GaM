import os
os.environ['PRMP_DB'] = ''

import itertools, threading, shutil

from prmp_lib.prmp_gui import *
from prmp_lib.prmp_gui.image_widgets import *
from prmp_lib.prmp_gui.tushed_widgets import *



class Background:
    img_count = 0
    def load(self):
        if not PRMP_DB: return

        i = 'red'
        size = self.cont.width, self.cont.height
        img = PRMP_DB.getImage('prmp_jpgs', '%s_lux'%i)[0]
        self.cont.loadImage(img, resize=size, name='Background_%d'%self.img_count)

        img = self.cont.image
        self.change2Imgcolor(img)
        self.img_count += 1
        if self.img_count > 20: self.img_count = 0

class MPVImage(PRMP_ImageCheckbutton):
    f = 0
    imageKwargs = dict(prmpImage='user_preppy_blue',inbuilt=1, inExt='png', resize=(80, 80))
    def __init__(self, master, mm=None, imageKwargs={}, resize=(80, 80), **kwargs):

        if not imageKwargs.get('prmpImage', None):
            imageKwargs = self.imageKwargs

        self.filename = imageKwargs.get('prmpImage')
        self.mm = mm
        super().__init__(master, tipKwargs=dict(text=self.filename), imageKwargs=imageKwargs, **kwargs)
        self.bind('<Double-1>', self.open)
    
    def open(self, event):
        geo=(500, 500)
        if self.mm.full_preview.get(): geo = self.prmpImage.image.size

        self.mm.preview.setSize((*geo, event.widget.winfo_rootx(), event.widget.winfo_rooty()))
        self.mm.preview.set(self.prmpImage)

        self.mm.preview.deiconify()
        
    def set(self, file=''):
        self.filename = str(file)
        self.set_tooltip_text(dict(text=os.path.basename(self.filename or '')))
        if not file: self.loadImage(**self.imageKwargs, name='blue_admin%d'%MPVImage.f)
        else: self.loadImage(prmpImage=file, resize=(80, 80), name=f'{file}_{MPVImage.f}')
        MPVImage.f += 1
        if MPVImage.f == 200: MPVImage.f = 0
        self.paint()

class Database_Images(PRMP_MainWindow, Background):

    def __init__(self, master=None, callback=None, db_file='', **kwargs):
        super().__init__(master, containerClass=PRMP_ImageSLabel, geo=(450, 650), title='Database Images', **kwargs)

        self.callback = callback
        self.prmpDB = None
        self.currentTable = ''
        self.currentImage = None
        self.images = {}
        db_file = r'C:/Users/Administrator/Coding_Projects/Python/Dev_Workspace/GaM/images_db.prmp_db'

        Label(self.cont, text='Tables', place=dict(relx=0, rely=0, relh=.08, relw=.43), font='BIG_PRMP_FONT')
        self.table_names = ListBox(self.cont, place=dict(relx=0, rely=.08, relh=.72, relw=.43), callback=self.loadTable)

        PRMP_Separator(self.cont, place=dict(relx=.44, rely=0, relh=.8, relw=.008))
        PRMP_Separator(self.cont, place=dict(relx=.451, rely=0, relh=.8, relw=.008))

        self.current_table = Label(self.cont, text='Images in Table', place=dict(relx=.47, rely=0, relh=.08, relw=.53), font='BIG_PRMP_FONT')
        self.table_images = ListBox(self.cont, place=dict(relx=.47, rely=.08, relh=.72, relw=.53), callback=self.preview_image)

        self.db_path = ChoosePath(self.cont, text='DB File', bottomKwargs=dict(_type='file', very=1, foreground='white'), place=dict(relx=.02, rely=.82, relh=.17, relw=.7), orient='h', longent=.25, folder=0)

        self.db_path.set(db_file)

        self.preview = PRMP_ImageDialog(self, withdraw=1, ntb=0, asb=0, atb=0)
        self.preview.imageLabel.bind('<1>', lambda e: self.preview.withdraw())

        custom = lambda e: self.db_path.set(dialogFunc(path=1, folder=0))

        self.db_path.B.bind('<Double-1>', custom)
        self.db_path.B.bind('<Return>', self.loadFile)

        self.preview_chk = Checkbutton(self.cont, place=dict(relx=.8, rely=.83, relh=.05, relw=.18), text='Preview?')

        self.fullsize = Checkbutton(self.cont, place=dict(relx=.8, rely=.89, relh=.05, relw=.18), text='Fullsize?')

        if self.callback: Button(self.cont, text='Return', place=dict(relx=.05, rely=.9, relh=.05, relw=.13), command=self.returnImages)
        
        if not master: self.after(10, self.load)
        if db_file: self.loadDB(db_file)

        self.loadFile()
        self.start()

    def loadFile(self, event=None):
        db_file = self.db_path.get()
        if db_file: self.loadDB(db_file)
    
    def loadDB(self, db_file):
        self.prmpDB = PRMP_ImagesDB(db_file)
        self.table_names.set(self.prmpDB.tableNames)
    
    def loadTable(self, event=None, selected=None):
        table = selected[-1]
        if table == self.currentTable: return

        self.currentTable = table
        self.images = self.prmpDB.getTable(table)
        
        self.table_images.set(self.images)
    
    def preview_image(self, event=None, selected=None):
        if not self.preview_chk.get(): return
        image = selected[-1]
        if image == self.currentImage: return
        self.currentImage = image

        self.preview.setTitle(f'{self.currentTable} --> {image}')
        self.preview.set(image, )
        
        if not self.preview.winfo_ismapped(): self.preview.deiconify()
    
    def isMaximized(self):
        self.load()
    
    def returnImages(self):
        if self.callback: self.callback(self.images)

class Massive_Photo_Viewer(PRMP_MainWindow):
    
    def __init__(self, master=None, geo=(1300, 840), themeIndex=37, **kwargs):
        super().__init__(master, geo=geo, themeIndex=themeIndex, asb=0, b4t=0, tipping=1, title='Massive Photo Viewer', resize=(0, 0), **kwargs)

        self.canvas = self.addWidget(Canvas, place=dict(relx=0, rely=0, relw=1, relh=1))
        
        self._img = PRMP_Image('purple_lux', inbuilt=1, inExt='jpeg', resize=geo)
        self.change_color(self._img.image)

        self.img = self._img.createTkImage()
        
        self.old = self.canvas.create_image(0, 0, image=self.img, anchor='nw')

        PRMP_Separator(self.canvas, orient='vertical', place=dict(relx=.765, rely=0, relw=.005, relh=1))
        PRMP_Separator(self.canvas, orient='vertical', place=dict(relx=.775, rely=0, relw=.005, relh=1))

        self.source_dir = ChoosePath(self.canvas, place=dict(relx=.79, rely=.008, relw=.2, relh=.15), text='Source Folder', callback=self.load_dir, folder=1)

        self.total = LabelLabel(self.canvas, topKwargs=dict(text='Total Pictures'), place=dict(relx=.79, rely=.17, relw=.2, relh=.04), longent=.65, orient='h', font='PRMP_FONT')
        
        rv = 20, 20

        self.pages = LabelLabel(self.canvas, topKwargs=dict(text='Pages', compound='left', image=PRMP_Image('file_open', resize=rv, inbuilt=1, for_tk=1)), place=dict(relx=.79, rely=.22, relw=.2, relh=.04), orient='h', font='PRMP_FONT')

        Button(self.canvas, text='Previous', place=dict(relx=.81, rely=.27, relw=.07, relh=.04), image=PRMP_Image('button_previous', resize=rv, inbuilt=1, for_tk=1), compound='left', command=self.prev_page)
        Button(self.canvas, text='Next', place=dict(relx=.9, rely=.27, relw=.07, relh=.04), image=PRMP_Image('button_next', resize=rv, inbuilt=1, for_tk=1), compound='left', command=self.next_page)

        self.full_preview = Checkbutton(self.canvas, text='Full size?', place=dict(relx=.81, rely=.34, relw=.1, relh=.04), image=PRMP_Image('zoom', resize=rv, inbuilt=1, for_tk=1), compound='left')

        Button(self.canvas, text='Use as Wallpaper?', place=dict(relx=.81, rely=.4, relw=.15, relh=.04), image=PRMP_Image('image_png', resize=rv, inbuilt=1, for_tk=1), compound='left', command=self.as_wall)
        

        Button(self.canvas, text='Load from Database?', place=dict(relx=.81, rely=.46, relw=.15, relh=.04), image=PRMP_Image('gtk_cdrom', resize=rv, inbuilt=1, for_tk=1), compound='left', command=self.from_database)

        self.varr = tk.StringVar(self)
        yy = .6
        self._copy = Radiobutton(self.canvas, text='Copy', place=dict(relx=.79, rely=yy, relw=.07, relh=.04), config=dict(value='copy', variable=self.varr, compound='left', image=PRMP_Image('gtk_copy', resize=rv, inbuilt=1, inExt='png', for_tk=1)))
        self._delete = Radiobutton(self.canvas, text='Delete', place=dict(relx=.86, rely=yy, relw=.07, relh=.04), config=dict(value='delete', variable=self.varr, compound='left', image=PRMP_Image('gtk_delete', resize=rv, inbuilt=1, inExt='png', for_tk=1)))
        self._move = Radiobutton(self.canvas, text='Move', place=dict(relx=.93, rely=yy, relw=.06, relh=.04), config=dict(value='move', variable=self.varr, compound='left', image=PRMP_Image('gtk_cut', resize=rv, inbuilt=1, inExt='png', for_tk=1)))

        self.setRadioGroups([self._copy, self._delete, self._move])

        self.dest_dir = ChoosePath(self.canvas, place=dict(relx=.79, rely=yy+.07, relw=.2, relh=.15), text='Destination Folder', folder=1)

        Button(self.canvas, text='Proceed', place=dict(relx=.85, rely=yy+.26, relw=.09, relh=.04), image=PRMP_Image('button_play', resize=(25, 25), inbuilt=1, inExt='png', for_tk=1), compound='left', command=self.proceed)

        self.image_labels = []
        self.pictures = []
        self.m = 9
        self.current = 1
        self.diff = self.m ** 2
        self.folder = ''
        
        self.after(100, lambda: threading.Thread(target=self.load).start())
        # pp = {}
        # # pp.update(PRMP_PNGS)
        # # pp.update(PRMP_JPEGS)
        # # pp.update(PRMP_XBMS)
        # pp.update(PRMP_GIFS)
        # # print(len(pp))
        # self.after(3000, lambda: threading.Thread(target=self._load_dict, args=[pp]).start())
        
        self.preview = PRMP_ImageDialog(self, geo=geo, imageWidConfig=dict(fullsize=1, bindMenu=0), asb=0, tooltype=1, atb=0, withdraw=1, ntb=1)
        self.preview.bind('<1>', lambda e: self.preview.withdraw())

        self.start()
    
    def as_wall(self):
        MPVImage.f += 1
        for img_lbl in self.image_labels:
            if img_lbl.variable.get() == '1':
                
                img = img_lbl.prmpImage.image

                self.img = PRMP_Image(image=img, resize=self.geo, name=f'PRMP_Test{MPVImage.f}', for_tk=1)
                # print(self.old)
                self.canvas.delete(self.old)
                self.old = self.canvas.create_image(0, 0, image=self.img, anchor='nw')
                self.change_color(img)
                return
        
    def load(self):
        r = c = v = 0
        hh = 80

        for co in range(self.diff):
            c = co%self.m
            r = co//self.m
            if co != 0 and c == 0: c = 0

            x = r * (hh+30)
            y = c * (hh+10)

            one = MPVImage(self.canvas, width=hh, height=hh, mm=self)
            self.canvas.create_window(x, y, window=one, anchor='nw')

            self.image_labels.append(one)

        self.paint()
    
    def load_dir(self, folder='', images=[]):
        images = images or  []
        self.folder = folder
        self.pictures = images.copy()

        if folder:
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path) and PRMP_ImageType.get(file_path): self.pictures.append(file_path)
    
        self.total.set(self.total_pictures)
        self.load_images(0)
    
    def load_images(self, index): threading.Thread(target=self._load_images, args=[index]).start()
    
    def _load_images(self, index):
        if self.pictures:
            pictures = self.pictures[self.diff*index: self.diff*(index+1)]
            self.pages.set(self.pages_format)
            
            labels = dict(itertools.zip_longest(self.image_labels, pictures, fillvalue=None))

            for wid, file in labels.items():
                if wid and file:
                    wid.set(file)
                    if wid.checkVar: wid.variable.set('0')
                elif wid: wid.set(None)

    def _load_dict(self, dic):
        labels = dict(itertools.zip_longest(self.image_labels, list(dic.items()), fillvalue=None))
        return
        co = 0
        for wid, tup in labels.items():
            # if co  == 10: return
            if wid and tup:
                name, b64 = tup
                # print(len(b64))
                file = PRMP_Image(name, b64=b64)
                wid.set(file)
                if wid.checkVar: wid.variable.set('0')
            co += 1

    @property
    def total_pictures(self): return len(self.pictures)

    @property
    def total_pages(self): return self.total_pictures//self.diff + 1

    @property
    def pages_format(self): return f'{self.current} of {self.total_pages}'
    
    @property
    def picked(self):
        _p = []
        for pp in self.image_labels:
            if pp.variable.get() == '1': _p.append(pp.filename)
        return _p

    def proceed(self):
        dest = self.dest_dir.get()

        if not self.picked: PRMP_MsgBox(self, _type='error', msg='Are you whyning me?\nPick atleast a picture!!!', title='Empty pictures')

        if not os.path.isdir(dest): PRMP_MsgBox(self, _type='error', msg='Destination folder is invalid!', title='Path Error')

        var = self.varr.get()

        if var in ['copy', 'delete', 'move']:
            func = self[var]
            PRMP_MsgBox(self, ask=1, callback=func, title='Confirmation', msg=f'Are you sure to {var} the marked pictures?')

        else: PRMP_MsgBox(self, _type='error', msg='Invalid options!\nChoose among:\n["Copy", "Delete", "Move"] !', title='Options Error')

    def copy(self, w):
        if not w: return
        picked = self.picked
        dest = self.dest_dir.get()
        for a in picked:
            if not a: return
            base = os.path.basename(a)
            new = os.path.join(dest, base)
            shutil.copy2(a, new)

    def delete(self, w):
        if not w: return

        picked = self.picked
        dest = self.dest_dir.get()
        # for a in picked: os.remove(a)

        self.load_dir(self.folder)

    def move(self, w):
        if not w: return
        picked = self.picked
        dest = self.dest_dir.get()
        for a in picked:
            if not a: return
            base = os.path.basename(a)
            new = os.path.join(dest, base)
            shutil.move(a, new)
        self.load_dir(self.folder)
    
    def next_page(self):
        self.current += 1
        if self.current > self.total_pages: self.current = 1
        self.load_images(self.current-1)

    def prev_page(self):
        self.current -= 1
        if self.current < 1: self.current = self.total_pages
        self.load_images(self.current-1)

    def from_database(self):
        file = dialogFunc(path=1)
        if file: Database_Images(self, db_file=file, callback=self.load_db, tooltype=0, tw=1, tm=0)
    
    def load_db(self, images): self.load_dir(images=images)

class Image_Renamer(Tk, Background):

    def __init__(self, folder='', **kwargs):
        super().__init__(containerClass=PRMP_ImageSLabel, containerConfig=dict(anchor='center'), geo=(800, 500), tipping=0, **kwargs)
        self.count = 0

        self.image_paths = []
        self.folder = folder
        self.current = 0
        self.current_file = ''
        self.total_images = 0

        self.image = PRMP_ImageSLabel(self.cont, place=dict(relx=.02, rely=.02, relh=.96, relw=.56))
        self.path = ChoosePath(self.cont, text='Choose Folder', place=dict(relx=.65, rely=0, relh=.25, relw=.3), callback=self.loadFolder, folder=1)

        self.total = LabelEntry(self.cont, topKwargs=dict(text='Total'), place=dict(relx=.65, rely=.28, relh=.08, relw=.3), orient='h', bottomKwargs=dict(state='readonly', foreground='black'))
        self.index = LabelSpin(self.cont, topKwargs=dict(text='Index'), place=dict(relx=.65, rely=.37, relh=.08, relw=.3), orient='h', bottomKwargs=dict(_type='number', very=1, background='white'), func=self.loadIndex, bttk=0)

        # self.index.B.bind('<FocusIn>', lambda e: self.focus())

        Button(self.cont, place=dict(relx=.7, rely=.55, relh=.08, relw=.2), command=self.refresh, text='Refresh')

        self.name = LabelEntry(self.cont, topKwargs=dict(text='Name'), place=dict(relx=.6, rely=.7, relh=.08, relw=.4), orient='h', longent=.2, bottomKwargs=dict(state='readonly', foreground='black'))

        self.rename = LabelEntry(self.cont, topKwargs=dict(text='Rename'), place=dict(relx=.6, rely=.79, relh=.08, relw=.4), orient='h', longent=.26)
        self.rename.B.bind('<Return>', self.renameFile, '+')

        self.bind('<Up>', self.rootLoadIndex, '+')
        self.bind('<Down>', self.rootLoadIndex, '+')
        self.refresh()
        self.first = 0 # hack for Down event
        self.after(50, self.load)
        self.start()

    def loadFolder(self, path):
        if not path: return
        self.folder = path
        self.image_paths = []
        
        for a in os.listdir(self.folder):
            f = os.path.join(path, a)
            if os.path.isfile(f) and PRMP_ImageType.get(f): self.image_paths.append(f)
        self.current = 0
        self.total_images = len(self.image_paths)
        
        self.total.set(self.total_images)
        self.index.B.setRange(1, self.total_images, 1)
        self.index.set(1)

        self.loadIndex()
    
    def getIndex(self, event):
        index = self.index.get()
        try: index = int(index)
        except: return 0

        if event:
            if event.keysym == 'Up': index += 1
            elif event.keysym == 'Down':
                if self.first: index -= 1
                else: index = 1
            elif event.keysym == 'Return':
                pass
            self.first = 1
        return index

    def rootLoadIndex(self, event=None):
        index = self.getIndex(event)
        self.index.set(index)
        self.loadIndex()
        
    def loadIndex(self, event=None):
        index = self.getIndex(event)
        
        if not index: return

        if (self.current == index) and not event==0: return

        if 0<index<=self.total_images:
            self.current = index
            self.current_file = self.image_paths[self.current-1]
            self.name.set(os.path.basename(self.current_file))
            
            if event == 0: return
            
            self.loadImage()
            self.count += 1

        if self.count == 40: self.count = 0
    
    def loadImage(self):
        if not self.current_file: return
        name = os.path.splitext(os.path.basename(self.current_file))[0]
        size = self.image.width, self.image.height

        self.image.loadImage(self.current_file, name=f'{name}_{self.count+1}', resize=size)

    def refresh(self):
        self.loadFolder(self.folder)
        self.path.set(self.folder)

    def renameFile(self, event=None):
        rename = self.rename.get()
        if not rename: return

        ext = os.path.splitext(self.current_file)[1]
        if not os.path.splitext(rename)[1]: rename += ext

        rename = os.path.join(self.folder, rename)

        try:
            os.rename(self.current_file, rename)
            self.image_paths[self.current-1] = rename
            self.rename.set('')
            self.loadIndex(0)
        except Exception as error: PRMP_MsgBox(self, title=error.__class__.__name__, msg=error, _type='error', geo=(400, 200), plenty=1)


app = Image_Renamer
app = Massive_Photo_Viewer
# app = Database_Images
# app = PRMP_ImageDialog

side = 'center'
app(side=side, callback=9, themeIndex=38)


