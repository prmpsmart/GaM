import os
os.sys.path.append(r'C:\Users\Administrator\Coding_Projects\Python\Dev_Workspace\GaM\prmp')
from prmp_gui.extensions import *

d = r'C:\Users\Administrator\Pictures\PRMPSmart Wallpapers'
pics = [os.path.join(d, a) for a in os.listdir(d)]
sp = pics[0]


user = 'Rocky Miracy Peter'


class Login(MainWindow):

    def __init__(self, geo, atb=0, asb=0, title='', ntb=1, pf=0, bn=0, **kwargs):
        '''
        Login screen of an application.
        '''
        self.co = 44

        super().__init__(geo=geo, atb=atb, asb=asb, title=title, ntb=ntb, b4t=0, tm=1, themeIndex=38, cac=1, **kwargs)
        
        self.canvas = self.container
        
        self.canvas.bind('<Configure>', lambda e: self.afterload(0))
        
        self.profile_frame = pf

        self.head_pix = 'blue_admin'
        # self.head_pix = 'profile_pix'

        if pf: self.pix = PRMP_ImageLabel(self.canvas, width=200, height=200, prmpImage=self.head_pix, resize=(200, 200), highlightable=1, imageKwargs=dict(bindMenu=0, name='llovee', inbuilt=1, inExt='png'))

        self.password = PasswordEntry(self.canvas, config=dict(relief='flat'),  place=dict(relx=.25, rely=.6, relh=.05, relw=.5))

        self.username_font = self.PRMP_FONT.copy()
        self.username_font['size'] = 30
        self.username_font = self.parseFont(self.username_font)
        
        if bn:
            self.canvas.bind('<1>', lambda e: self.afterload(1))
            self.canvas.bind('<3>', lambda e: self.afterload(-1))
        
        self.anime = PRMP_ImageSLabel(self.canvas, 'line_bubbles', imageKwargs=dict(bindMenu=0, name='llovee', inExt='gif', inbuilt=1), place=dict(relx=(1-.3)/2, rely=.9, relw=.3, relh=.05), config=dict(relief='flat'))

    
    def afterload(self, s):
        '''
        updates the canvas objects
        '''
        x, y = geo = self.width, self.height
        
        self.co += s
        p = pics[self.co]
        # print(self.co)

        bgs = self.change_color(p)
        self.anime['background'] = bgs[2]

        self.img = PRMP_Image(p, resize=geo, for_tk=1)
        self.canvas.create_image(0, 0, image=self.img, anchor='nw')

        if not self.profile_frame:
            p = self.head_pix
            self.admin = PRMP_Image(p, resize=(200, 200), name=f'{p}{self.co}', inExt='png', inbuilt=1, for_tk=1)
            self.canvas.create_image(x/2, 220, image=self.admin)

        else: self.canvas.create_window(x/2, 200, window=self.pix)

        self.canvas.create_text(x/2, 360, text=user, fill='white', font=self.username_font)

        if self.co >= len(pics)-1: self.co = 0

        PRMP_Window.STYLE.update()

Login((700, 700), title=user, tipping=1, pf=0, bn=0).start()



