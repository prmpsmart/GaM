import os
os.sys.path.append(r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM\prmp')
os.sys.path.append(os.path.dirname(__file__))

import itertools, threading, shutil

from prmp_gui.dialogs import *
from prmp_gui.two_widgets import *


class MPVImage(PRMP_ImageCheckbutton):
    f = 0
    def __init__(self, master, prmpImage='', mm=None, **kwargs):
        self.filename = prmpImage or 'default_dp'
        self.mm = mm
        super().__init__(master, prmpImage=prmpImage, tipKwargs=dict(text=self.filename), **kwargs)
        self.bind('<Double-1>', self.open)
    
    def open(self, event):
        geo=(500, 500)

        if self.mm.full_preview.get(): geo = self.prmpImage.image.size
        self.mm.preview.setImage(self.prmpImage)

        self.mm.preview.size((*geo, event.widget.winfo_rootx(), event.widget.winfo_rooty()))
        self.mm.preview.deiconify()
        
    def set(self, file):
        self.filename = str(file)
        self.set_tooltip_text(dict(text=os.path.basename(self.filename or '')))
        self.loadImage(file)


class ChoosePath(LabelText):
    def __init__(self, master, text='', callback=None, **kwargs):
        FONT = self.PRMP_FONT
        FONT['size'] = 20
        super().__init__(master, longent=.3, topKwargs=dict(text=text, font=FONT, image=PRMP_Image('add_folder', resize=(25, 25), inbuilt=1, inExt='png', for_tk=1), compound='left'), tipKwargs=dict(text='Double-click to choose folder!'), **kwargs)
        self.T.bind('<Double-1>', self.load_dir)
        self.T.bind('<1>', self.read_dir)
        self.B.bind('<Double-1>', self.load_dir)
        self.folder = ''
        self.callback = callback

    def read_dir(self, event):
        folder = self.B.get()
        if os.path.isdir(folder):
            self.folder = folder
            self.B.set(folder)
            if self.callback: self.callback(folder)

    def load_dir(self, event):
        folder = dialogFunc(path=1, folder=1)
        if folder:
            self.folder = folder
            self.B.set(folder)
            if self.callback: self.callback(folder)


class MassivePhotoViewer(MainWindow):
    
    def __init__(self, master=None, geo=(1300, 840), themeIndex=37, **kwargs):
        super().__init__(master, geo=geo, themeIndex=themeIndex, asb=0, b4t=0, tipping=1, title='Massive Photo Viewer', resize=(0, 0), **kwargs)

        self.canvas = self.addWidget(Canvas, place=dict(relx=0, rely=0, relw=1, relh=1))
        
        self._img = PRMP_Image('purple_beau', inbuilt=1, inExt='jpeg', resize=geo)
        self.change_color(self._img.image)

        self.img = self._img.createTkImage()
        
        self.old = self.canvas.create_image(0, 0, image=self.img, anchor='nw')

        PRMP_Separator(self.canvas, orient='vertical', place=dict(relx=.765, rely=0, relw=.005, relh=1))
        PRMP_Separator(self.canvas, orient='vertical', place=dict(relx=.775, rely=0, relw=.005, relh=1))

        self.source_dir = ChoosePath(self.canvas, place=dict(relx=.79, rely=0, relw=.2, relh=.15), text='Source Folder', callback=self.load_dir)

        self.total = LabelLabel(self.canvas, topKwargs=dict(text='Total Pictures'), place=dict(relx=.79, rely=.17, relw=.2, relh=.04), longent=.65, orient='h', font='PRMP_FONT')
        
        rv = 20, 20

        self.pages = LabelLabel(self.canvas, topKwargs=dict(text='Pages', compound='left', image=PRMP_Image('pages', resize=rv, inbuilt=1, inExt='png', for_tk=1)), place=dict(relx=.79, rely=.22, relw=.2, relh=.04), orient='h', font='PRMP_FONT')

        Button(self.canvas, text='Previous', place=dict(relx=.81, rely=.27, relw=.07, relh=.04), image=PRMP_Image('backward', resize=rv, inbuilt=1, inExt='png', for_tk=1), compound='left', command=self.prev_page)
        Button(self.canvas, text='Next', place=dict(relx=.9, rely=.27, relw=.07, relh=.04), image=PRMP_Image('forward', resize=rv, inbuilt=1, inExt='png', for_tk=1), compound='left', command=self.next_page)

        self.full_preview = Checkbutton(self.canvas, text='Full size?', place=dict(relx=.81, rely=.34, relw=.1, relh=.04), image=PRMP_Image('zoom', resize=rv, inbuilt=1, inExt='png', for_tk=1), compound='left')

        Button(self.canvas, text='Use as Wallpaper?', place=dict(relx=.81, rely=.4, relw=.15, relh=.04), image=PRMP_Image('as_wall', resize=rv, inbuilt=1, inExt='png', for_tk=1), compound='left', command=self.as_wall)

        self.varr = tk.StringVar(self)
        yy = .6
        self._copy = Radiobutton(self.canvas, text='Copy', place=dict(relx=.79, rely=yy, relw=.07, relh=.04), config=dict(value='copy', variable=self.varr, compound='left', image=PRMP_Image('copy', resize=rv, inbuilt=1, inExt='png', for_tk=1)))
        self._delete = Radiobutton(self.canvas, text='Delete', place=dict(relx=.86, rely=yy, relw=.07, relh=.04), config=dict(value='delete', variable=self.varr, compound='left', image=PRMP_Image('delete', resize=rv, inbuilt=1, inExt='png', for_tk=1)))
        self._move = Radiobutton(self.canvas, text='Move', place=dict(relx=.93, rely=yy, relw=.06, relh=.04), config=dict(value='move', variable=self.varr, compound='left', image=PRMP_Image('move', resize=rv, inbuilt=1, inExt='png', for_tk=1)))

        self.setRadioGroups([self._copy, self._delete, self._move])

        self.dest_dir = ChoosePath(self.canvas, place=dict(relx=.79, rely=yy+.07, relw=.2, relh=.15), text='Destination Folder')

        Button(self.canvas, text='Proceed', place=dict(relx=.85, rely=yy+.26, relw=.09, relh=.04), image=PRMP_Image('play', resize=(25, 25), inbuilt=1, inExt='png', for_tk=1), compound='left', command=self.proceed)

        self.image_labels = []
        self.pictures = []
        self.m = 9
        self.current = 1
        self.diff = self.m ** 2
        self.folder = ''
        
        self.after(100, lambda: threading.Thread(target=self.afterload).start())
        pp = {}
        # pp.update(PRMP_PNGS)
        # pp.update(PRMP_JPEGS)
        # pp.update(PRMP_XBMS)
        pp.update(PRMP_GIFS)
        print(len(pp))
        self.after(3000, lambda: threading.Thread(target=self._load_dict, args=[pp]).start())
        
        self.preview = PRMP_ImageDialog(self, geo=geo, imageKwargs=dict(bindMenu=0, fullsize=1), asb=0, tooltype=1, atb=0)
        self.preview.bind('<1>', lambda e: self.preview.withdraw())

        self.start()
    
    def as_wall(self):
        MPVImage.f += 1
        for img_lbl in self.image_labels:
            if img_lbl.var.get() == '1':
                
                img = img_lbl.prmpImage.image

                self.img = PRMP_Image(image=img, resize=self.geo, name=f'{os.path.basename(img_lbl.filename or "PRMP_Test")}{MPVImage.f}', for_tk=1)
                # print(self.old)
                self.canvas.delete(self.old)
                self.old = self.canvas.create_image(0, 0, image=self.img, anchor='nw')
                self.change_color(img)
                return
        
    def afterload(self):
        r = c = v = 0
        hh = 80

        for co in range(self.diff):
            c = co%self.m
            r = co//self.m
            if co != 0 and c == 0: c = 0

            x = r * (hh+30)
            y = c * (hh+10)

            one = MPVImage(self.canvas, width=hh, height=hh, imageKwargs=dict(bindMenu=0, fullsize=0, inbuilt=1, inExt='png'), resize=(80, 80), prmpImage='blue_admin', mm=self)
            self.canvas.create_window(x, y, window=one, anchor='nw')

            self.image_labels.append(one)
        for a in self.image_labels: a.paint()
    
    def load_dir(self, folder):
        self.folder = folder
        self.pictures = []
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
                if wid:
                    wid.set(file)
                    wid.var.set('0')

    def _load_dict(self, dic):
        labels = dict(itertools.zip_longest(self.image_labels, list(dic.items()), fillvalue=None))
        # return
        co = 0
        for wid, tup in labels.items():
            # if co  == 10: return
            if wid and tup:
                name, b64 = tup
                # print(len(b64))
                file = PRMP_Image(name, b64=b64)
                wid.set(file)
                wid.var.set('0')
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
            if pp.var.get() == '1': _p.append(pp.filename)
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
        if self.current == self.total_pages+1: self.current = 1
        self.load_images(self.current-1)

    def prev_page(self):
        self.current -= 1
        if self.current == 0: self.current = 5
        self.load_images(self.current-1)



MassivePhotoViewer(tm=1)

