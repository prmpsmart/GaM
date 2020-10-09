from .thrift_tabs.details_note import Thrift_Details, Frame, Notebook, Styles
from .thrift_tabs.home import Thrift_Home
from ...backend.utils.debug.debug import Debug



class Thrift(Notebook):
    name = "Thrift"
    def __init__(self, master):
        super().__init__(master, takefocus="")
        
        self.enable_traversal()

       ######## Thrift Home
        self.thrift_home = Thrift_Home(self)
        self.add(self.thrift_home, padding=1)
        self.tab(0, text="Thrift Home",compound="left",underline="0")

       ######## Details Note
        self.details_note = Thrift_Details(self)
        self.add(self.details_note, padding=1)
        self.tab(1, text="Thrift Details",compound="none",underline="0")
        
        
    def style(self):
        self.thrift_home.style()
        self.details_note.style()

    def draw_charts(self):
        self.thrift_home.draw_charts()
        self.details_note.draw_charts()

    def place_widgs(self):
        self.place(relx=0, rely=0, relh=1, relw=1)
        self.details_note.place_widgs()
        self.thrift_home.place_widgs()





