from ..core.prmp_gui.extensions import *
from ..dc.dc_extensions import *
from ..core.agam_extensions import *


class PersonalDetails(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        Label(self, text='Name', place=dict(relx=.02, rely=0, relh=.15, relw=.25))
        self.name = Entry(self, place=dict(relx=.3, rely=0, relh=.15, relw=.68))

        Label(self, text='Number', place=dict(relx=.02, rely=.16, relh=.15, relw=.25))
        self.number = Entry(self, place=dict(relx=.3, rely=.16, relh=.15, relw=.68))

        Label(self, text='Phone', place=dict(relx=.02, rely=.32, relh=.15, relw=.25))
        self.phone = Entry(self, place=dict(relx=.3, rely=.32, relh=.15, relw=.68))

        Label(self, text='ID', place=dict(relx=.02, rely=.48, relh=.15, relw=.25))
        self.id = Entry(self, place=dict(relx=.3, rely=.48, relh=.15, relw=.68))

        Label(self, text='Gender', place=dict(relx=.02, rely=.64, relh=.15, relw=.25))
        self.gender = Combobox(self, type_='gender', place=dict(relx=.3, rely=.64, relh=.15 , relw=.68))

        Label(self, text='Address', place=dict(relx=.02, rely=.8, relh=.15, relw=.25))
        self.address = Entry(self, place=dict(relx=.3, rely=.8, relh=.15, relw=.68))


class RecordDetails(LabelFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        Label(self, text='Date', place=dict(relx=.02, rely=0, relh=.25, relw=.2))
        self.date = Button(self, text='06/12/2020', place=dict(relx=.24, rely=0, relh=.25, relw=.25))

        Label(self, text='Range', place=dict(relx=.02, rely=.27, relh=.25, relw=.2))

        self.range1 = Entry(self, place=dict(relx=.24, rely=.27, relh=.25, relw=.25))

        Label(self, text='- to -', relief='flat', place=dict(relx=.51, rely=.27, relh=.25, relw=.2))

        self.range2 = Entry(self, place=dict(relx=.73, rely=.27, relh=.25, relw=.25))

        Label(self, text='Note', place=dict(relx=.02, rely=.54, relh=.25, relw=.2 ))
        self.note = Text(self, wrap='word', place=dict(relx=.24, rely=.54, relh=.42, relw=.74), very=True)


class DateSearch(LabelFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.date = Button(self, text='06/12/2020', place=dict(relx=.02, rely=0, relh=.2, relw=.3))

        self.year = Radiobutton(self, text='Year', value='year', place=dict(relx=.02, rely=.22, relh=.25 , relw=.22))

        self.month = Radiobutton(self, text='Month', value='month', place=dict(relx=.25, rely=.22, relh=.25 , relw=.22))

        self.week = Radiobutton(self, text='Week', value='week', place=dict(relx=.48, rely=.22, relh=.25 , relw=.24))

        self.day = Radiobutton(self, text='Day', value='day', place=dict(relx=.73, rely=.22, relh=.25 , relw=.24))

        self.dayName = RadioEntry(self, topKwargs=dict(config=dict(text='Day Name', value='dayName')), orient='h', place=dict(relx=.02, rely=.48, relh=.25 , relw=.45))

        self.monthName = RadioEntry(self, topKwargs=dict(config=dict(text='Month Name', value='monthName')), orient='h', place=dict(relx=.5, rely=.48, relh=.25 , relw=.45))

        self.weekNumber = RadioEntry(self, topKwargs=dict(config=dict(text='Week Number', value='weekNumber')), orient='h', place=dict(relx=.02, rely=.75, relh=.25 , relw=.45))

        self.yearNumber = RadioEntry(self, topKwargs=dict(config=dict(text='Year Number', value='yearNumber')), orient='h', place=dict(relx=.5, rely=.75, relh=.25 , relw=.456))



