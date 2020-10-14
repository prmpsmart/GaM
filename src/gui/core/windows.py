from .prmp_tk import *



class RegionHierachy(PRMP_Tk):
    
    def __init__(self, region):
        super().__init__()
        self.nodes = {}
        frame = tk.Frame(self)
        self.tree = ttk.Treeview(frame)
        ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
        self.tree.heading('#0', text='Project tree', anchor='w')

        self.tree.grid(row=0, column=0, rowspan=10, columnspan=10)
        ysb.grid(row=0, column=11, rowspan=10, sticky='ns')
        xsb.grid(row=11, column=0, columnspan=10, sticky='ew')
        frame.grid()

        self.region = region
        self.processRegion(self.region)
    
    def processRegion(self, region):
        regionsManagers = region.regionsManagers
        if regionsManagers[0]:
            for rm in regionsManagers: self.processRegion(rm)

RH = RegionHierachy