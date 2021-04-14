from . import *
from .dialogs import *
from .tushed_widgets import *


class PRMP_SolidScreen(PRMP_MainWindow):
    def __init__(self, side='top-center', gaw=1, bd=12, geo=(),**kwargs):
        super().__init__(tm=1, gaw=gaw, geo=geo or (500, 500), side=side, **kwargs)

        self.container.configure(borderwidth=bd)

        self.paint()

SS = PRMP_SolidScreen


class ColumnViewerDialog(PRMP_Dialog):

    def __init__(self, master=None, title='Columns Viewer Dialog', geo=(300, 300), column=None, **kwargs):
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

    def processInput(self):
        result = self.get()

        # print(result)


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


