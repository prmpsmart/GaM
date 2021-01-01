from ._gui import *
from prmp_gui.core import *


class Details(LabelFrame):
    def __init__(self, master, which='s', main=None, **kw):
        
        root = master.master

        super().__init__(master, **kw)
        
        self.main = main
        self.which = which
        self.destPath = ''
        
        self.indicatorLbl = Label(self, place=dict(relx=.61, rely=0, relh=.1, relw=.1))
        
        self.actionBtn = Button(self,  text='Send' if which == 's' else 'Receive', command=self.send if which == 's' else self.receive, place=dict(relx=.781, rely=0, relh=.1, relw=.154))
        
        self.browseBtn = Button(self, text='Browse' if which == 's' else 'Remote Load', command=self.main.browse if which == 's' else self.remoteLoad, place=dict(relx=.015, rely=0, relh=.1, relw=.154 if which == 's' else .26))
        
        if which == 'r':
            self.destDir = Checkbutton(self, text=f'{compStr} Destination?',  command=self.setDest, place=dict(relx=.313, rely=0, relw=.255, relh=.082))
        
        self.detConts = Frame(self, border="2", place=dict(relx=.01, rely=.114, relh=.868, relw=.981))
        
        self.which = which
        self.pathStat = None
        
        self.nameL = Button(self.detConts, text='Name', command=self.reload, place=dict(relx=.01, rely=.01, relh=.12, relw=.164))
        self.nameS = Label(self.detConts, text='File Name', place=dict(relx=.175, rely=.01, relh=.12, relw=.82))
        self.nameTip = Tip(self.nameS, root=root)

        self.sizeL = Label(self.detConts, text='Size', place=dict(relx=.01, rely=.14, relh=.12, relw=.164))
        self.sizeS = Label(self.detConts, anchor='ne', place=dict(relx=.175, rely=.14, relh=.12, relw=.274))
        self.sizeTip = Tip(self.sizeS, root=root)

        self.typeL = Label(self.detConts, text='Type', place=dict(relx=.01, rely=.27, relh=.12, relw=.164))
        self.typeS = Label(self.detConts, anchor='ne', justify='right', place=dict(relx=.175, rely=.27, relh=.12, relw=.274))
        self.typeTip = Tip(self.typeS, root=root)

        self.ctimeL = Label(self.detConts, text='CTime', place=dict(relx=.01, rely=.4, relh=.12, relw=.164))
        self.ctimeS = Label(self.detConts, foreground="#000000", font=font0,  anchor='nw', justify='right', place=dict(relx=.175, rely=.4, relh=.12, relw=.274))
        self.ctimeTip = Tip(self.ctimeS, root=root)

        self.atimeL = Label(self.detConts, text='ATime', place=dict(relx=.01, rely=.53, relh=.12, relw=.164))
        self.atimeS = Label(self.detConts, foreground="#000000", font=font0,  anchor='nw', justify='right', place=dict(relx=.175, rely=.53, relh=.12, relw=.274))
        self.atimeTip = Tip(self.atimeS, root=root)

        self.mtimeL = Label(self.detConts, text='MTime', place=dict(relx=.01, rely=.66, relh=.12, relw=.164))
        self.mtimeS = Label(self.detConts, place=dict(relx=.175, rely=.66, relh=.12, relw=.274))
        self.mtimeTip = Tip(self.mtimeS, root=root)

        self.filesCountL = Label(self.detConts, text='Files Count', place=dict(relx=.47, rely=.14, relh=.12, relw=.329))
        self.filesCountS = Label(self.detConts, anchor='ne', place=dict(relx=.8, rely=.14, relh=.12, relw=.194))

        self.dirsCountL = Label(self.detConts, text='Dirs Count', place=dict(relx=.47, rely=.27, relh=.12, relw=.329))
        self.dirsCountS = Label(self.detConts, anchor='ne', place=dict(relx=.8, rely=.27, relh=.12, relw=.194))
        
        self.innerSizeL = Label(self.detConts, text='Inner Files Size', place=dict(relx=.47, rely=.4, relh=.12, relw=.329))
        self.innerSizeS = Label(self.detConts,  anchor='ne', place=dict(relx=.8, rely=.4, relh=.12, relw=.194))
        self.innerSizeTip = Tip(self.innerSizeS, root=root)
        
        
        
        text = 'Compress?' if which == 's' else 'Decompress?'
        compText = compStr + text
        tip = 'Compress before sending (Good for Directories).' if which == 's' else 'Decompress after receiving (Good for Directories).'
        
        
        self.detailsL = Label(self.detConts, text='Details', place=dict(relx=.493, rely=.53, relh=.12, relw=.268))
        self.detailsS = Label(self.detConts, background="red", foreground="white", font=font2,  text='No', place=dict(relx=.78, rely=.53, relh=.12, relw=.205))
        
        self.compress = Checkbutton(self, text=compText, activebackground="#ececec", activeforeground="#000000", disabledforeground="#a3a3a3", font=font1, foreground="#000000", highlightbackground="#d9d9d9", highlightcolor="black",  place=dict(relx=.493, rely=.69, relw=.268, relh=.1))
        self.compressTip = Tip(self.compress, msg=tip, root=root)

        self.previewBtn = Button(self, relief="ridge", text='Preview', command=self.preview, place=dict(relx=.77, rely=.69, relh=.1, relw=.205))

        self.level = Progressbar(self, value="30", place=dict(relx=.02, rely=.82, relh=.14, relw=.75))

        self.percent = Label(self.detConts, text='100%', place=dict(relx=.78, rely=.82, relh=.14, relw=.22))
        
        self.tranxFer = None
        self.pathStat = None
        
        self.after(100, self.update)
     
    def preview(self): Preview(self.main.root, self.pathStat)
    
    def setDest(self):
        self.destPath = ''
        if self.destDir == '1':
            p = dialogFunc(path=1, folder=1)
            if os.path.exists(p): self.destPath = p
            else: show('Path Error', 'The choosen directory does not exists', 'warn')
    
    def setDetails(self):
        def setRed(): self.detailsS.config(text='No', bg='red')
        def setGreen(text): self.detailsS.config(text=text, bg='green')
    
        if self.tranxFer and self.tranxFer.tranxFeredDetails:
            if self.which == 'r': setGreen('Received')
            else: setGreen('Sent')
            if self.tranxFer.finished: setRed()
        else: setRed()
    
    def update(self):
        self.setDetails()
        self.setOnGoing()
        self.setProgress()
        self.after(100, self.update)
    
    def load(self, pathStat=None):
        if pathStat: self.pathStat = pathStat
        if self.pathStat:
            self.nameS.config(text=self.pathStat.name)
            self.nameTip.update(self.pathStat.fullName)
            
            self.sizeS.config(text=self.pathStat.fSize)
            self.sizeTip.update(self.pathStat.fullSize)
            
            self.typeS.config(text=self.pathStat.type)
            self.typeTip.update(self.pathStat.fullType)
            
            self.ctimeS.config(text=self.pathStat.cTime)
            self.ctimeTip.update(self.pathStat.fullCTime)
            
            self.atimeS.config(text=self.pathStat.aTime)
            self.atimeTip.update(self.pathStat.fullATime)
            
            self.mtimeS.config(text=self.pathStat.mTime)
            self.mtimeTip.update(self.pathStat.fullMTime)
            
            self.filesCountS.config(text=self.pathStat.filesCount)
            
            self.dirsCountS.config(text=self.pathStat.dirsCount)
            
            self.innerSizeS.config(text=self.pathStat.fInnerSize)
            self.innerSizeTip.update(self.pathStat.fullInnerSize)
        self.after(1000, self.load)
    
    def localLoad(self, path):
        if isinstance(path, str): pass
        else: path = os.path.get()
        
        pathStat = LocalPathStat(path)
        if pathStat.exists: self.load(pathStat)
        else: show('Loading Error', 'Path is invalid', 'error')
    
    def reload(self):
        try: self.localLoad()
        except: pass
    
    def remoteLoad(self):
        if self.main.checkConnected:
            self.tranxFer = TranxFer(self.main.connection, which='download', dest=self.destPath)
            self.tranxFer.startThreadedTranxFer()
            
            first = time.time()
            
            while True:
                second = time.time()
                pathStat = self.tranxFer.remotePath
                
                if pathStat:
                    self.load(pathStat)
                    break
                elif (second - first) >= 3:
                    show('Parsing Error', 'Remote load error.', 'error')
                    break
    
    def setOnGoing(self):
        def setOff(): self.indicatorLbl.config(text='Off', bg='red')
        if self.tranxFer and self.tranxFer.onGoing: self.indicatorLbl.config(text='On', bg='green')
        else:
            setOff()
    
    def setProgress(self):
        if self.tranxFer and not self.tranxFer.finished:
            self.percent.config(text=self.tranxFer.tranxFeredPercent)
            self.level.config(value=self.tranxFer.tranxFered)
        else:
            self.level.config(value=0)
            self.percent.config(text='0.00 %')
        # self.level.update()
    
    def send(self):
        if self.main.checkConnected:
            if self.main.checkPath():
                self.tranxFer = TranxFer(self.main.connection, LocalPathStat(self.main.path.get()))
                self.tranxFer.startThreadedTranxFer()
    
    def receive(self):
        if self.main.checkConnected:
            if self.tranxFer and self.tranxFer.startedReceiving:
                show('Error', 'A tranxFer is still on', 'error')
                return
            if self.tranxFer: self.tranxFer.startThreadedReceiving()
            else: show('TranxFer Error', 'Load remotely first to get the path details', 'warn')


class FullFileTranxFer(FileTranxFer):
    name = 'full'
    geo = (400, 800)

    def __init__(self, master=None, title='Full File TranxFer', **kwargs):
        super().__init__(master, title=title,  **kwargs)
        
    
    def defaults(self):

        self.serverSet = False
    
    def _setupApp(self):
        self.titleL = Label(self.root,  text='FileTranxFer by PRMPSmart', place=dict(relx=.01, rely=.01, relh=.029, relw=.98))
        
        self.clock = Label(self.titleL, place=dict(relx=.01, rely=.04, relh=.9, relw=.24))
        self.tick()
        
        self.miniBtn = Button(self.titleL, text='''Mini''', command=self.another, place=dict(relx=.8, rely=.04, relh=.9, relw=.2))
        
        self.localhostS = Checkbutton(self.root,  text='Localhost?', place=dict(relx=.02, rely=.045, relh=.04, relw=.3))
        
        self.osL = Label(self.root, text='OS', place=dict(relx=.69, rely=.045, relh=.04, relw=.1))
        self.osS = Label(self.root, text=get_os_name(), place=dict(relx=.79, rely=.045, relh=.04, relw=.2))
        

        self.network = LabelFrame(self.root, text='Network Details', place=dict(relx=.013, rely=.085, relh=.27, relw=.98))
        
        self.networkL = Label(self.network, text='Network?', place=dict(relx=.01, rely=.02, relh=.12, relw=.2))
        self.networkS = Label(self.network, place=dict(relx=.22, rely=.02, relh=.12, relw=.1))
        
        self.connectedL = Label(self.network, text='Connected?', place=dict(relx=.37, rely=.02, relh=.12, relw=.2))
        self.connectedS = Label(self.network, place=dict(relx=.58, rely=.02, relh=.12, relw=.1))
        
        self.servingL = Label(self.network, text='Serving?', place=dict(relx=.7, rely=.02, relh=.12, relw=.18))
        self.servingS = Label(self.network, place=dict(relx=.89, rely=.02, relh=.12, relw=.1))

        self.ipAddressL = Label(self.network,  text='IP4 Address', place=dict(relx=.01, rely=.15, relh=.12, relw=.25))

        self.ipAddressS = Label(self.network, place=dict(relx=.26, rely=.15, relh=.12, relw=.3))
        
        self.gatewayL = Label(self.network,  text='Gateway', place=dict(relx=.01, rely=.28, relh=.12, relw=.25))
        self.gatewayS = Label(self.network, place=dict(relx=.26, rely=.28, relh=.12, relw=.3))
        
        self.reloadNetworkBtn = Button(self.network, text='Reload', command=lambda: self.loadNetworkInfo(1), place=dict(relx=.01, rely=.43, relh=.12, relw=.18))
        
        # self.handShakeS = Checkbutton(self.network,  text='HS?', command=self.toServe, place=dict(relx=.2, rely=.43, relh=.12, relw=.15))
        # Tip(self.handShakeS, 'Do you want Hand Shake security?')
        
        self.isServerS = Checkbutton(self.network,  text='Server?', command=self.toServe, place=dict(relx=.36, rely=.43, relh=.12, relw=.2))
        
        self.serverL = Label(self.network,  text='Server', place=dict(relx=.01, rely=.56, relh=.12, relw=.18))
        self.serverS = Entry(self.network, place=dict(relx=.2, rely=.56, relh=.12, relw=.3))
        
        self.sameAsGatewayS = Checkbutton(self.network,  text='Gateway?', command=self.isGateway, place=dict(relx=.51, rely=.56, relh=.12, relw=.23))
        
        self.portL = Label(self.network,  text='Port', place=dict(relx=.01, rely=.69, relh=.12, relw=.18))
        self.portS = Entry(self.network, place=dict(relx=.2, rely=.69, relh=.12, relw=.3))

        self.transRateL = Label(self.network, text='Transmission Rates', place=dict(relx=.58, rely=.15, relh=.12, relw=.41))
        self.upRateL = Label(self.network, text='TX / UP', place=dict(relx=.58, rely=.28, relh=.12, relw=.15))
        self.upRateS = Label(self.network, place=dict(relx=.74, rely=.28, relh=.12, relw=.25))
        self.dnRateL = Label(self.network, text='RX / DN', place=dict(relx=.58, rely=.41, relh=.12, relw=.15))
        self.dnRateS = Label(self.network, place=dict(relx=.74, rely=.41, relh=.12, relw=.25))

        self.serverDetailL = Label(self.network,  text='Server IP : Port', place=dict(relx=.01, rely=.87, relh=.12, relw=.313))
        self.serverDetailS = Label(self.network, place=dict(relx=.33, rely=.87, relh=.12, relw=.42))
        
        self.setBtn = Button(self.network, text='Set', command=self.setServerDetails, place=dict(relx=.51, rely=.7, relh=.12, relw=.18))
        
        self.serveBtn = Button(self.network, text='Serve', command=self.serve, place=dict(relx=.77, rely=.56, relh=.12, relw=.18))

        self.stopBtn = Button(self.network, text='Stop', command=self.stop, place=dict(relx=.77, rely=.7, relh=.12, relw=.18))
        
        self.connectBtn = Button(self.network, text='Connect', command=self.connect, place=dict(relx=.77, rely=.87, relh=.12, relw=.18))



        self.sendDetails = Details(self.root,text='Send', main=self, place=dict(relx=.01, rely=.358, relh=.33, relw=.98))
        
        if self._path: self.sendDetails.localLoad(self._path)

        self.isDir = Checkbutton(self.sendDetails, text=f'{compStr} Directory?', place=dict(relx=.313, rely=0, relw=.255, relh=.082))

        self.receiveDetails = Details(self.root, text='Receive', main=self, which='r', place=dict(relx=.013, rely=.695, relh=.3, relw=.98))
        self.root.after(1000, self.loadNetworkInfo)
        self.root.after(10, self.update)
        self.root.mainloop()
        
    def update(self):
        super().update()
        self.setConnected()
        self.root.after(100, self.update)
    
    def mini(self): MiniFileTranxFer(self.root)
    
    def browse(self):
        super().browse()
        if self.path: self.sendDetails.localLoad(self.path)
    
    def setNetwork(self):
        super().setNetwork()
        if self.networkInfo: self.gatewayS.config(text=self.networkInfo.gateway)
        else:  self.gatewayS.config(text='No network.')
    
    def loadNetworkInfo(self, e=0):
        self.setNetwork()
        if self.networkInfo:
            self.ipAddressS.config(text=self.networkInfo.ip)
            self.gatewayS.config(text=self.networkInfo.gateway)
            if which_platform() != 'nt':
                self.upRateS.config(text=self.networkInfo.tx.fBytes)
                self.dnRateS.config(text=self.networkInfo.rx.fBytes)
        if e==0: self.root.after(1000, self.loadNetworkInfo)
    
    def isGateway(self):
        if self.connected: show('Connected', 'Already Connected, Stop to continue', 'warn')
        else:
            self.serverSet = False
            self.isServer.set('0')
            if self.sameAsGateway.get() == '1':
                self.serverEnt.set(self.networkInfo.gateway if self.networkInfo else self.lh)
                self.serverS.config(state='disabled')
            else: self.serverS.config(state='normal')
    
    def toServe(self):
        if super().toServe(): self.sameAsGateway.set('0')
        
    def setServerDetails(self):
        if self.localhost.get() == '1' and 8: 0
            # if
        self.serverDetailS.config(text='')
        if super().setServerDetails():
            self.serverDetailS.config(text=f'{self.serverEnt.get()} : {self.getPort()}')
            return True
    
    def serve(self):
        if super().serve():
            if self.setServerDetails():
                self.server = Server(self.port, True if self.handShake.get() == '1' else False)
                self.setServing()
                return True
            else: show('Not Set', 'Server and Port not set.', 'warn')





class GuiFileTranxFer:
    def __init__(self, full=True):
        TranxFerLogger.setLevel('critical')
        FullFileTranxFer() if full else MiniFileTranxFer()









