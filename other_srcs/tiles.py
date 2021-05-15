import os

import itertools, threading

from prmp_lib.prmp_gui import *

class Tile(Checkbutton):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.on = False
        self.bind('<1>', self.tiled)

        # self.deselect()
        # self.select()
        # self.toggle()
        # self.flash()
        # self.invoke()
    
    def tiled(self, wid=None):
        if self.on:
            self['bg'] = PRMP_Theme.DEFAULT_BACKGROUND_COLOR
            self['fg'] = PRMP_Theme.DEFAULT_FOREGROUND_COLOR
            self.on = False
        else:
            # self.flash()
            self['fg'] = PRMP_Theme.DEFAULT_BACKGROUND_COLOR
            self['bg'] = PRMP_Theme.DEFAULT_FOREGROUND_COLOR
            self.on = True
        # self.toggle()


class Tiles(PRMP_MainWindow):
    
    def __init__(self, master=None, geo=(1300, 840), themeIndex=37, tiles=9, **kwargs):
        super().__init__(master, geo=geo, themeIndex=themeIndex, asb=0, tipping=1, title='Tiles By PRMPSmart', resize=(0, 0), **kwargs)

        self.canvas = self.addWidget(Canvas, place=dict(relx=0, rely=0, relw=1, relh=1))
        self.bind('<B1-Motion>', self.moving)
        if tiles > 50: tiles = 50
        # self.bind('<Motion>', self.flash)
        
        self._img = PRMP_Image('purple_lux', inbuilt=1, inExt='jpeg', resize=geo)
        # self.change_color(self._img.image)

        self.img = self._img.createTkImage()
        self.tiles = tiles
        
        self.old = self.canvas.create_image(0, 0, image=self.img, anchor='nw')
        
        self.after(100, self.afterload)
        # self.after(100, lambda: threading.Thread(target=self.afterload).start())
        self.last = None
        self.start()
    
    def flash(self, event):
        x, y = event.x_root, event.y_root
        wid = self.winfo_containing(x, y)
        try: wid.flash()
        except Exception as e: pass
    
    def moving(self, event):
        # print(event.__dict__)
        x, y = event.x_root, event.y_root
        wid = self.winfo_containing(x, y)

        if wid != self.last:
            try:
                wid.tiled()
                self.last = wid
            except Exception as e: pass

        
        # print(wid)
    
    def afterload(self):
        w, h = self.canvas.width, self.canvas.height
        w //= self.tiles
        h //= self.tiles
        r = c = v = 0
        for co in range(self.tiles**2):
            c = co%self.tiles
            r = co//self.tiles
            if co != 0 and c == 0: c = 0
            x = r * (w)
            y = c * (h)
            self.canvas.create_window(x, y, window=Tile(self.canvas, width=w, height=h), anchor='nw')
        self.paint()


Tiles(tiles=40, tm=1, be=1, b4t=1)


