from ..core.agam_dialogs import *
from ..core.gui_core.two_widgets import *


class ThirdPartySuretyDialog(PersonDialog):
    
    def __init__(self, master=None, geo=(500, 570), title='Third Party Dialog', **kwargs):
        super().__init__(master=master, geo=geo, title=title, **kwargs)
    
    def _setupDialog(self):
        super()._setupDialog()
        
        other = LF(self, text='Other Details')
        other.place(relx=.02, y=230, h=290, relw=.96)
        
        self.dob = LDB(other, text='Date of Birth', orient='h', longent=.5, relx=.01, rely=0, relh=.1, relw=.5)
        self.religion = LE(other, text='Religion', orient='h', longent=.35, relx=.59, rely=0, relh=.1, relw=.4)
        self.maritalStatus = LE(other, text='Marital Status', orient='h', relx=.01, rely=.11, relh=.1, relw=.5)
        self.occupation = LE(other, text='Occupation', orient='h', relx=.01, rely=.22, relh=.1, relw=.6, longent=.35)
        self.officeAddress = LT(other, text='Office Address', orient='h', longent=.32, relx=.01, rely=.33, relh=.28, relw=.7)
        self.homeTown = LE(other, text='Home Town', orient='h', relx=.01, rely=.62, relh=.1, relw=.4)
        self.stateOfOrigin = LE(other, text='State of Origin', orient='h', relx=.51, rely=.62, relh=.1, relw=.5)
        self.relationshipWithMember = LE(other, text='Relationship with Member', orient='h', longent=.6, relx=.01, rely=.73, relh=.1, relw=.7)
        self.knowledgeOfMember = LE(other, text='Knowledge Of Member', orient='h', longent=.6, relx=.01, rely=.84, relh=.1, relw=.7)
        
        self.childWidgets += [other]
        self.resultsWidgets += ['dob', 'officeAddress', 'religion', 'homeTown', 'stateOfOrigin', 'occupation', 'knowledgeOfMember', 'relationshipWithMember', 'maritalStatus']














