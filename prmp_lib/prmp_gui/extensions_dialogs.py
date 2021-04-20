from .dialogs import *


class AttributesExplorerDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Attributes Explorer Dialog', geo=(600, 500), obj=None, dialog=None, **kwargs):
        self.obj = obj
        self.dialog = dialog
        super().__init__(master, title=title, geo=geo, **kwargs)

    def _setupDialog(self): AttributesExplorer(self.container, place=dict(relx=.02, rely=.02, relh=.96, relw=.96), values=self.values, obj=self.obj,  dialog=self.dialog, callback=self._callback)

    def _callback(self, w):
        if self.callback:
            self.callback(w)
            self.destroy()

class AttributesViewerDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Attributes Viewer Dialog', geo=(700, 300), obj=None, attr=None, dialog=None, **kwargs):
        self.attr = attr
        self.obj = obj
        self.dialog = dialog
        super().__init__(master, title=title, geo=geo, **kwargs)

    def _setupDialog(self): AttributesViewer(self.container, place=dict(relx=.02, rely=.02, relh=.96, relw=.96), attr=self.attr, obj=self.obj, dialog=self.dialog)




