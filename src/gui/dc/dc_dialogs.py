from ..core.agam_dialogs import *
from ...backend.dc.dc_regions import *

class ClientDialog(PersonDialog):
    
    def __init__(self, master=None, title='New Client Dialog', manager=None, client=None, geo=(550, 500), **kwargs):
        self.client = client
        if not manager:
            if client: self.manager = client.manager
        self.manager = manager
        super().__init__(master=master, title=title, geo=geo, **kwargs)
    
    def _setupDialog(self):
        super()._setupDialog()

        clientDetails = PRMP_LabelFrame(self, config=dict(text='Client Details'))
        clientDetails.place(x=2, y=290, h=100, relw=.35)
        
        self.rate = LabelEntry(clientDetails, topKwargs=dict(config=dict(text='Rate')), orient='h', relx=.02, rely=0, relh=.45, relw=.8, longent=.45)
        
        self.cardDue = PRMP_Checkbutton(clientDetails, text='Card Due')
        self.cardDue.place(relx=.02, rely=.5, relh=.45, relw=.8)

        self.addResultsWidgets(['rate', 'cardDue'])

    
    def processInput(self):
        result = super().processInput()

        if self.client:
            # confirm editing of the client details
            # edit the client details
            pass
        
        elif self.manager:
            client = self.manager.createClient(**result)
            print(client)

        if self._return: self.destroy()

        print(result, self.manager)








