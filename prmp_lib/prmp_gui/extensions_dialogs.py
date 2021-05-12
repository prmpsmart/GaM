from . import *
from .dialogs import *
from .tushed_widgets import *



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


class ColumnViewerDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Columns Viewer Dialog', geo=(300, 300), column=None, manager=None, **kwargs):
        self.manager = manager
        self.column = column
        super().__init__(master, title=title, geo=geo, **kwargs)

    def _setupDialog(self):
        self._column = ColumnViewer(self.container, place=dict(relx=.02, rely=.02, relh=.96, relw=.96), column=self.column)
        self.addEditButton()

        self.text = self._column.text
        self.attr = self._column.attr
        self.value = self._column.value
        self._width = self._column._width

        self.addResultsWidgets(['text', 'attr', '_width', 'value'])
        self.set()

    def processInput(self, e=0):
        self._result = self.get()

        if self._result.get('text'):

            if self.column: PRMP_MsgBox(self, title='Edit Column?', msg='Are you sure to edit this column object?', ask=1, callback=self.editColumn)

            elif self.manager: PRMP_MsgBox(self, title='Add Column?', msg='Are you sure to add this column object?', ask=1, callback=self.addColumn)

        else: PRMP_MsgBox(self, title='Error', msg='Atleast input text!')
        
    def addColumn(self, w):
        if w: self.manager.addColumn(self._result)
        self.destroyDialog()
        
    def editColumn(self, w):
        if w: self.column.__dict__.update(self._result)
        self.destroyDialog()


class ColumnsExplorerDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Columns Explorer Dialog', geo=(800, 500), columns=None, **kwargs):
        self.columns = columns
        super().__init__(master, title=title, geo=geo, **kwargs)

    def _setupDialog(self):

        self.cols = ColumnsExplorer(self.container, place=dict(relx=.02, rely=.02, relh=.96, relw=.96), columns=self.columns, callback=self._callback)

        self.bind('<Return>', self.cols.getColumns)

    def _callback(self, w, e=0):
        if self.callback:
            self.callback(w)
            if not e: self.destroy()



