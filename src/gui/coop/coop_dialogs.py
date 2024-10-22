from ..gam.gam_dialogs import *


class ThirdPartySuretyDialog(PersonDialog):

    def __init__(self, master=None, geo=(550, 700), title='Third Party Dialog', **kwargs):
        super().__init__(master=master, geo=geo, title=title, **kwargs)

    def _setupDialog(self):
        super()._setupDialog()

        self.phone.master.place_forget()
        self.image.place_forget()
        self.phone.master.place(x=2, y=2, relh=.4, relw=.55)
        self.image.place(relx=.58, y=14, relh=.335, relw=.41)

        other = PRMP_LabelFrame(self.container, config=dict(text='Other Details'))
        other.place(x=2, rely=.42, relh=.5, relw=.96)

        self.dob = LabelDateButton(other, topKwargs=dict(config=dict(text='Date of Birth')), orient='h', longent=.5, relx=.01, rely=0, relh=.1, relw=.5)
        self.religion = LabelEntry(other, topKwargs=dict(config=dict(text='Religion')), orient='h', longent=.35, relx=.59, rely=0, relh=.1, relw=.4)
        self.maritalStatus = LabelEntry(other, topKwargs=dict(config=dict(text='Marital Status')), orient='h', relx=.01, rely=.11, relh=.1, relw=.5)
        self.occupation = LabelEntry(other, topKwargs=dict(config=dict(text='Occupation')), orient='h', relx=.01, rely=.22, relh=.1, relw=.6, longent=.35)
        self.officeAddress = LabelText(other, topKwargs=dict(config=dict(text='Office Address')), orient='h', longent=.32, relx=.01, rely=.33, relh=.28, relw=.7)
        self.homeTown = LabelEntry(other, topKwargs=dict(config=dict(text='Home Town')), orient='h', relx=.01, rely=.62, relh=.1, relw=.4)
        self.stateOfOrigin = LabelEntry(other, topKwargs=dict(config=dict(text='State of Origin')), orient='h', relx=.48, rely=.62, relh=.1, relw=.5)
        self.relationshipWithMember = LabelEntry(other, topKwargs=dict(config=dict(text='Relationship with Member')), orient='h', longent=.6, relx=.01, rely=.73, relh=.1, relw=.7)
        self.knowledgeOfMember = LabelEntry(other, topKwargs=dict(config=dict(text='Knowledge Of Member')), orient='h', longent=.6, relx=.01, rely=.84, relh=.1, relw=.7)

        self.addResultsWidgets(['dob', 'officeAddress', 'religion', 'homeTown', 'stateOfOrigin', 'occupation', 'knowledgeOfMember', 'relationshipWithMember', 'maritalStatus'])














