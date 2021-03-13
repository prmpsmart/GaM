from ..gam.gam_dialogs import *
from .dc_extensions import *

class ClientDialog(PersonDialog):

    def __init__(self, master=None, title='New Client Dialog', manager=None, client=None, geo=(550, 500), **kwargs):
        self.client = client
        self.manager = manager
        if not self.manager:
            if self.client:
                kwargs['person'] = client
                self.manager = self.client.manager
        super().__init__(master=master, title=title, geo=geo, manager=self.manager, **kwargs)

    def _setupDialog(self):
        super()._setupDialog()

        clientDetails = PRMP_LabelFrame(self, config=dict(text='Client Details'))
        clientDetails.place(x=2, y=290, h=100, relw=.35)

        self.rate = LabelEntry(clientDetails, topKwargs=dict(config=dict(text='Rate')), bottomKwargs=dict(_type='number'),orient='h', place=dict(relx=.02, rely=0, relh=.45, relw=.8), longent=.45)

        self.cardDue = PRMP_Checkbutton(clientDetails, text='Card Due', place=dict(relx=.02, rely=.5, relh=.45, relw=.8))

        self.addResultsWidgets(['rate', 'cardDue'])

    def action(self, e=0):
        # print(self.result)
        if self.result:
            if self.client: PRMP_MsgBox(self, title='Edit Client Details', message='Are you sure to edit the details of this client?', _type='question', callback=self.updateClient)
            elif self.manager: PRMP_MsgBox(self, title='Client Creation', message='Are you sure to create a new client?', _type='question', callback=self.newClient)

    def updateClient(self, w):
        if w:
            self.client.person.update(**self.result)
            self.client.changeRate(self.result['rate'])
            self._setResult(self.client)
        self.destroyDialog()

    def newClient(self, w):
        if w:
            client = self.manager.createClient(**self.result)
            self._setResult(client)
        self.destroyDialog()


class AreaDialog(GaM_Dialog):
    def __init__(self, master=None, area=None, manager=None, title='Area Dialog', **kwargs):
        self.area = area
        self.manager = manager

        super().__init__(master, geo=(350, 300), values=area, title=title, **kwargs)

    def _setupDialog(self):
        self.addEditButton()
        # name readonly
        self.name = LabelEntry(self.container, place=dict(relx=.005, rely=.05, relw=.5, relh=.15), orient='h', topKwargs=dict(text='Name'), bottomKwargs=dict(state='readonly'))
        # date
        self.date = LabelDateButton(self.container, topKwargs=dict(text='Date'), place=dict(relx=.005, rely=.25, relw=.45, relh=.15),  longent=.4, orient='h')
        # co
        self.co = Button(self.container, text='Cash Officers', place=dict(relx=.05, rely=.5, relw=.35, relh=.12))

        # unique_id
        UniqueID(self.container, place=dict(relx=.5, rely=.5, relw=.35, relh=.12), obj=self.area)
        self.addResultsWidgets(['name', 'date'])

    def action(self):
        if self.result:
            if self.area: PRMP_MsgBox(self, title='Edit Area Details', message='Are you sure to edit the details of this area?', _type='question', callback=self.updateArea)

            elif self.manager: PRMP_MsgBox(self, title='area Creation', message='Are you sure to create a new area?', _type='question', callback=self.newArea)

            else: PRMP_MsgBox(self, title='Area Dialog Error', message='No Area or Manager is given.', _type='error', ask=0)

    def updateArea(self, w):
        if w:
            self.area.update(self.result['date'])
            self._setResult(self.area)
        self.destroyDialog()

    def newArea(self, w):
        if w:
            area = self.manager.createArea(date=self.result['date'])
            self._setResult(area)
        self.destroyDialog()


class ClientAccountDialog(AccountDialog):

    def _setupDialog(self):
        super()._setupDialog()
        self.addEditButton()

        self.rate = LabelEntry(self.container, topKwargs=dict(config=dict(text='Rate')), bottomKwargs=dict(_type='money'),orient='h', place=dict(relx=.005, y=100, h=40, relw=.8), longent=.4)

        self.addResultsWidgets('rate')


class ThriftDialog(GaM_Dialog):
    def __init__(self, master=None, thrift=None, title='Thrift Dialog', values={}, manager=None, **kwargs):
        self.thrift = thrift
        self.values = values
        self.manager = manager
        super().__init__(master, geo=(350, 300), title=title, **kwargs)

    def _setupDialog(self):
        self.addEditButton()
        self.thrifts = ThriftInput(self.container, callback=self.set, place=dict(relx=.01, rely=.01, relh=.82, relw=.96), thrift=self.thrift, values=self.values, manager=self.manager)

        self.get = self.thrifts.get
        self.set = self.thrifts.set

        for k in self.thrifts.resultsWidgets: self.__dict__[k] = self.thrifts.__dict__[k]

        self.addResultsWidgets(self.thrifts.resultsWidgets)

    # def set(self, values={}):
    #     if values:
    #         if isinstance(values, Thrift):
    #             values.get('money')
    #             values['income'] = values
    #         elif isinstance(values, dict):
    #             if values.get('money'): values.


    def action(self):
        if self.result:
            if self.thrift: PRMP_MsgBox(self, title='Edit thrift Details', message='Are you sure to edit the details of this thrift?', _type='question', callback=self.updateThrift)

            elif self.manager: PRMP_MsgBox(self, title='Thrift Creation', message='Are you sure to create a new Thrift?', _type='question', callback=newThrift)
            else: PRMP_MsgBox(self, title='Thrift Dialog Error', message='No Thrift or Manager is given.', _type='error', ask=0)

    def updateThrift(self, w):
        if w:
            try:
                self.thrift.update(**self.result, reload_=1)
                self._setResult(self.thrift)

            except Exception as error: PRMP_MsgBox(self, title='Thrift Update Error', message=error, _type='error', ask=0)
        self.destroyDialog()

    def newThrift(self, w):
        if w:
            try:
                thrift = self.manager.createThrift(**self.result)
                self._setResult(thrift)
            except Exception as error: PRMP_MsgBox(self, title='Thrift Creation Error', message=error, _type='error', ask=0)
        self.destroyDialog()


class ThriftDetailsDialog(GaM_Dialog):
    def __init__(self, master=None, title='Thrift Details Dialog', thrift=None, geo=(450, 650), values={}, **kwargs):
        self.thrift = thrift
        self.values = values
        super().__init__(master, geo=geo, title=title, **kwargs)

    def _setupDialog(self):
        self.thriftDetail = ThriftDetail(self.container, place=dict(relx=.02, rely=.005, relh=.99, relw=.96), thrift=self.thrift, values=self.values)

        self.get = self.thriftDetail.get
        self.set = self.thriftDetail.set


class ClientsList(GaM_Dialog):
    def __init__(self, master=None, area=None, title='Clients List', **kwargs):
        self._area = area
        super().__init__(master, title=title, **kwargs)

    def _setupDialog(self):
        if self._area:
            name = self._area.name
            values = self._area.clientsManager
            valuesKwargs = dict(showAttr='name')
        else: name, values, valuesKwargs = '', [], {}

        self.area = LabelLabel(self.container, bottomKwargs=dict(text=self._area.name if self._area else 'Area'), place=dict(relx=0, rely=0, relh=.12, relw=1), orient='h', longent=.3, topKwargs=dict(text='Area'))

        self.clients = SubsList(self.container, callback=self.returnClient, place=dict(relx=0, rely=.12, relh=.88, relw=1), values=values, valuesKwargs=valuesKwargs)

    def returnClient(self, client):
        self.destroy()
        self.callback(client)


class DailyContributionDailog(GaM_Dialog):

    def __init__(self, master=None, title='Area 1 Daily Contribution', dcContrib=None, geo=(1500, 800), **kwargs):
        self.dcContrib = dcContrib
        super().__init__(master, title=title, geo=geo, **kwargs)

    def changeDate(self, date):
        if date: self.totals.date.set(date.date)

    def _placeSubmitButton(self):
        x, y = self.containerGeo
        self.submitBtn.place(x=120 , y=y-40, h=30, w=60)

    def _setupDialog(self):
        self.addEditButton()

        self.area = Button(self.container, command=self.openArea, text='Area', place=dict(relx=.007, rely=.005, relw=.17, relh=.05))

        self.date = LabelDateButton(self.container, topKwargs=dict(text='Date'), place=dict(relx=.18, rely=.005, relw=.11, relh=.05), orient='h', bottomKwargs=dict(callback=self.changeDate), longent=.37)

        self.account = LabelCombo(self.container, topKwargs=dict(text='Area\'s Account'), place=dict(relx=.005, rely=.06, relw=.2, relh=.1), longent=.4, func=self.setAreaAccountDependents)
        self.account.get = self.account.B.getObj

        self.month = LabelMonthYearButton(self.container, topKwargs=dict(text='Month'), place=dict(relx=.21, rely=.06, relw=.08, relh=.1), longent=.4)

        PRMP_Separator(self.container, place=dict(relx=.005, rely=.19, relh=.005, relw=.29))

        Button(self.container, text='New Client', place=dict(relx=.007, rely=.205, relw=.1, relh=.04), command=self.addNewClient)
        Button(self.container, text='New Client Account', place=dict(relx=.11, rely=.205, relw=.15, relh=.04), command=self.addNewClientAccount)

        self.ledgerNumber = LabelSpin(self.container, topKwargs=dict(text='Ledger Number'), place=dict(relx=.005, rely=.255, relw=.25, relh=.05), longent=.43, orient='h', func=self.clientNumberChanged, bttk=1)

        self.clientName = LabelLabel(self.container, topKwargs=dict(text='Client Name'), place=dict(relx=.005, rely=.31, relw=.27, relh=.05), longent=.32, orient='h')

        self.rate = LabelLabel(self.container, topKwargs=dict(text='Cl. Rate'), place=dict(relx=.005, rely=.361, relw=.1, relh=.05), orient='h')

        self.clientMonth = LabelLabel(self.container, topKwargs=dict(text='Cl. Month'), place=dict(relx=.13, rely=.361, relw=.15, relh=.05), orient='h')

        PRMP_Separator(self.container, place=dict(relx=.005, rely=.412, relh=.005, relw=.29))

        self.income = LabelEntry(self, topKwargs=dict(text='Income'), bottomKwargs=dict(_type='money'), place=dict(relx=.005, rely=.46, relh=.05, relw=.14), orient='h')
        self.money = Checkbutton(self, text='Money?', place=dict(relx=.18, rely=.467, relh=.03, relw=.065))

        self.transfer = LabelEntry(self, topKwargs=dict(text='Transfer'), place=dict(relx=.005, rely=.515, relh=.05, relw=.14), orient='h', bottomKwargs=dict(_type='money'))

        self.paidout = LabelEntry(self, topKwargs=dict(text='Paidout'), bottomKwargs=dict(_type='money'), orient='h', place=dict(relx=.005, rely=.57, relh=.05, relw=.14))

        self.ready = Checkbutton(self.container, text='Ready?', place=dict(relx=.2, rely=.525, relh=.04, relw=.07))
        Button(self.container, text='Add Thrift', place=dict(relx=.18, rely=.575, relh=.04, relw=.09), command=self.addThrift)

        PRMP_Separator(self.container, place=dict(relx=.005, rely=.663, relh=.005, relw=.29))

        self.contributed = LabelSpin(self.container, topKwargs=dict(text='Contributed'), place=dict(relx=.005, rely=.685, relw=.22, relh=.05), orient='h', longent=.4, bttk=1)

        Button(self.container, text='Delete', place=dict(relx=.23, rely=.685, relw=.06, relh=.04), command=self.deleteThrift)

        PRMP_Separator(self.container, place=dict(relx=.005, rely=.765, relh=.005, relw=.29))

        self.bto = LabelEntry(self.container, topKwargs=dict(text='Brought To Office'), place=dict(relx=.005, rely=.8, relw=.2, relh=.05), orient='h', longent=.6, bottomKwargs=dict(placeholder='Enter B-T-O', _type='money'))

        Button(self.container, text='Add B-T-O', place=dict(relx=.21, rely=.805, relw=.08, relh=.04), command=self.addBTO)

        PRMP_Separator(self.container, place=dict(relx=.005, rely=.882, relh=.005, relw=.29))

        Button(self.container, text='Update', place=dict(relx=.225, rely=.945, relw=.07, relh=.04), command=self.dcUpdate)


        self.view = Hierachy(self.container, place=dict(relx=.3, rely=.005, relw=.695, relh=.69))
        self.view.setColumns(TreeColumns.columns(self.dcContrib))

        self.totals = DailyContTotal(self.container, place=dict(relx=.3, rely=.7, relw=.692, relh=.29), relief='groove', dcContrib=self.dcContrib)

        self.addResultsWidgets(['date', 'ledgerNumber', 'clientName', 'month', 'account', 'income', 'money', 'paidout', 'transfer', 'contributed', 'bto'])
        self.thriftWidgets = ['income', 'paidout', 'money', 'transfer', 'ledgerNumber', 'account']

    def defaults(self):
        # self.bind('<Up>', lambda e: self.ledgerNumber.B.event_generate('<<Increment>>'), '+')
        # self.bind('<Down>', lambda e: self.ledgerNumber.B.event_generate('<<Decrement>>'), '+')

        self.bind('<Return>', self.addThrift, '+')

        self.container.bind('<1>', lambda e: self.focus())

        self._account = None
        self._clientAccount = None

        if self.dcContrib:
            self._area = self.dcContrib.manager.master
            self.account.B.setObjs(self._area, 'name')
            self.area.set(self._area.name)

        else: self._area = None

        self.update()

        # self.editBtn.set(False)
        # self.editInput()

    def getThriftDetails(self): return self.get(self.thriftWidgets)

    def dcUpdate(self): PRMP_MsgBox(self, title='Update Confirmation.', message='Are you sure to update this Daily Contribution?', ask=1, callback=self._dcUpdate)

    def _dcUpdate(self, w):
        if not w: return
        self.dcContrib.updateThrifts()
        self.update()

    def update(self, e=0):
        if not self.dcContrib: return
        if self._account: self.setClientNumbers()

        self.contributed.B.config(to=len(self.dcContrib), from_=1)
        self.date.set(self.dcContrib.date.date)
        self.view.viewSubs(self.dcContrib)
        self.bto.set(self.dcContrib.bto)
        self.totals._refresh()

    def openArea(self): openCores(self, obj=self._area)

    def processInput(self, e=0):
        pass

    def getDel(self):
        get = self.contributed.get() or 0
        try:
            get = int(float(get))
            return get
        except: pass

    def deleteThrift(self):
        get = self.getDel()

        if get and (get <= len(self.dcContrib)):
            title = 'Sure to delete?'
            message = f'Are you sure to delete thrift No. {get}.'
            ask = 1
            _type = 'question'
            callback = self._deleteThrift
        else:
            title = 'Error'
            message = 'The input is invalid.'
            ask = 0
            _type = 'error'
            callback = None

        PRMP_MsgBox(self, title=title, message=message, ask=ask, _type=_type, callback=callback)

    def _deleteThrift(self, w):
        if w:
            get = self.getDel()
            # print(get)
            self.dcContrib.removeSubByIndex(get - 1)

            self.update()
            PRMP_MsgBox(self, title='Removed Successful.', message=f'Thrift No. {get} has been successfully removed. ', ask=0, _type='info')

    def addThrift(self, e=0):
        # self.month.B.flash()
        # return
        if not self.editBtn.get(): return
        if e and (e.widget in [self.ledgerNumber.B, self.account.B, self.contributed.B]): return

        if self.ready.get(): self.isReady(1)
        else:
            PRMP_MsgBox(self, title='Ready to continue?', message='Are you sure to add this transaction?', _type='warn', callback=self.isReady)
            return

    def isReady(self, w):
        if w: self._addThrift()

    def _addThrift(self, e=0):
        thriftDetails = self.getThriftDetails()
        try:
            assert self._account is thriftDetails['account'], 'No area account is selected.'
        except AssertionError as e:
            PRMP_MsgBox(self, title='Account Error', message=e, ask=0, _type='error')
            return

        try: self.dcContrib.createThrift(**thriftDetails)
        except Exception as error: PRMP_MsgBox(self, title='Thrift Creation Error', message=error, ask=0, _type='error', delay=5000)

        self.update()
        self.emptyWidgets(self.thriftWidgets[:4])

    def getClientsAccounts(self):
        if self._account: return self._account.getClientsAccounts()
        return []

    def setAreaAccountDependents(self, e=None):
        self._account = self.account.get()
        self.setClientNumbers()

    def maxNum(self): return len(self.getClientsAccounts())

    def setClientNumbers(self):
        max_ = self.maxNum()

        self.ledgerNumber.B.configure(from_=1, to=max_ or 1, increment=1)

    def clientNumberChanged(self, e=0):  self.after(10, self._clientNumberChanged)

    def getSomething(self, area=0):
        if not area:
            if not self._account:
                # PRMP_MsgBox(self, title='No Area Account', message=f'An area account has not been choosen.', ask=0, _type='error')
                return
            return self._account
        else:
            if not self._area:
                # PRMP_MsgBox(self, title='No Area', message=f'An area has not been given.', ask=0, _type='error')
                return
            return self._area

    def _clientNumberChanged(self):
        get = self.ledgerNumber.get()
        num = int(float(get))

        account = self.getSomething()
        if not account: return

        clientAccount = account.getClientAccount(num)

        if clientAccount:
            self._clientAccount = clientAccount
            self.clientName.set(self._clientAccount.region.name)
            self.rate.set(self._clientAccount.rate)
            self.clientMonth.set(self._clientAccount.month.monthYear)
        else:
            self._clientAccount = None
            # PRMP_MsgBox(self, title='Not Found', message=f'No Client with account\'s ledger number = {num}.', ask=0, _type='error')

    def addBTO(self):
        bto = self.bto.get()
        try:
            assert bto > 0, 'Brought to office cannot be less than 0'
            self.dcContrib.addBTO(bto)
            self.totals._refresh()
        except AssertionError as error: PRMP_MsgBox(self, title=error.__class__.__name__, message=error, ask=0)

    def addNewClient(self):
        area = self.getSomething(1)
        if area: ClientDialog(self, manager=area.clientsManager, callback=self.update)

    def addNewClientAccount(self):
        area = self.getSomething(1)
        if area: ClientsList(self, area=area, callback=self._addNewClientAccount)

    def _addNewClientAccount(self, client):
        if client: ClientAccountDialog(self, manager=client.accountsManager, callback=self._finalNewClientAccount)

    def _finalNewClientAccount(self, account):
        self.update()
        if account:
            name = account.month.monthYear
            client = account.region.name
            ledgerNumber = account.ledgerNumber

            text= f'Account of month: {name}\nClient name: {client}\nLedger Number: {ledgerNumber}\nhas just been created.'

            PRMP_MsgBox(self, title='Account creation is successful.', message=text, ask=0, delay=0)


class FillTable:

    def getDatas(self, columns=[], plot=0, heads=[],season='', which='', **kwargs):

        datas = self.obj.objectSort.fillColumns(_type=int, columns=columns, heads=heads, season=season, which=which, **kwargs)
        ticks = []

        if plot and datas:
            num = len(heads)
            _num = 0
            if season == 'month' and  which == 'days': _num = 1

            ticks = [data[_num] for data in datas]
            datas = [data[num:] for data in datas]

        title = self.obj.objectSort.getTitle(**kwargs)

        return datas, title, ticks

    def fillPlot(self, columns=[], heads=[], **kwargs):
        datas, title, ticks = self.getDatas(plot=1, columns=columns, heads=heads, **kwargs)

        self.plotDatas = dict(xticks=columns, ys=datas, labels=ticks, title=title)

    def fillTable(self, columns=[], heads=[], **kwargs):
        datas, title, _ = self.getDatas(columns=columns, heads=heads, **kwargs)

        self.table.setTitle(title)

        self.tree = self.table.hnce.tree

        headies = DCColumn.getShorts(heads + columns)
        self.tree.setColumns(headies)
        self.tree.clear()

        self.treeview = self.tree.treeview

        if not datas: return

        for data in datas:
            text, *values = data
            self.treeview.insert('', text=text, values=values)


class PlotDialog(FillTable, GaM_Dialog):

    def __init__(self, master=None, title='Plot Dialog', geo=(1500, 800), obj=None, **kwargs):
        self.obj = obj
        self.plotDatas = {}
        super().__init__(master, title=title, geo=geo, tm=0, **kwargs)

    def _setupDialog(self):

        note = Notebook(self.container, place=dict(relx=.005, rely=.005, relw=.28, relh=.64))

        self.frame2 = ProperDetails(note, obj=self.obj, callback=self.fillPlot)
        note.add(self.frame2, padding=3)
        note.tab(0, text='Proper Details', compound='left', underline='-1')

        self.chartOptions = ChartOptions(self.container, place=dict(relx=.005, rely=.65, relw=.28, relh=.3))

        fr = Frame(self.container, place=dict(relx=.285, rely=.005, relw=.711, relh=.99))

        from prmp.prmp_gui.plot_canvas import PRMP_PlotCanvas
        self.fig1 = PRMP_PlotCanvas(fr, place=dict(relx=.002, rely=.002, relw=.496, relh=.496))
        self.fig2 = PRMP_PlotCanvas(fr, place=dict(relx=.502, rely=.002, relw=.496, relh=.496))
        self.fig3 = PRMP_PlotCanvas(fr, place=dict(relx=.002, rely=.502, relw=.496, relh=.496))
        self.fig4 = PRMP_PlotCanvas(fr, place=dict(relx=.502, rely=.502, relw=.496, relh=.496))

        self.plots_figures = [self.fig1, self.fig2, self.fig3, self.fig4]

      ############ Plot and Clear

        self.plot_btn = Button(self.container, command=self.plotIt, text='Plot', place=dict(relx=.02, rely=.952, relh=.044, relw=.1))
        self.bind('<Control-P>', self.plotIt)
        self.bind('<Control-p>', self.plotIt)

        self.clear_btn = Button(self.container, command=self.clear_plot, text='Clear', place=dict(relx=.16, rely=.952, relh=.044, relw=.1))
        self.bind('<Control-C>', self.clear_plot)
        self.bind('<Control-c>', self.clear_plot)


    def plotIt(self, e=0):
        plotDetails = self.chartOptions.get()
        figNum = plotDetails.pop('figNum')

        if figNum > 4: figNum = 4
        elif figNum < 0: figNum = 1

        plot = self.plots_figures[figNum-1]
        if plot and self.plotDatas:
            plot.doPlotting(**self.plotDatas, **plotDetails)
            plot.draw()


    def clear_plot(self, e=0):
        num = self.chartOptions.fig.get()
        if num:
            num = int(num)

            if num > 4: num = 4
            elif num < 0: num = 1

            fig = self.plots_figures[num - 1]
            fig.clear()
        else: PRMP_MsgBox(self, message='Pick a chart number', title='Required Chart Number', _type='error')


class ContribApp(GaM_Dialog):

    def __init__(self, contributions=None, geo=(900, 600), **kwargs):
        self.contributions = contributions

        super().__init__(tw=0, geo=geo, **kwargs)

    def _setupDialog(self):
        cont = self.container

        fr1 = Frame(cont, place=dict(relx=0, rely=0, relw=.4, relh=1), relief='groove')

        area1 = LabelFrame(fr1, place=dict(relx=0, rely=0, relw=1, relh=.4), relief='groove', text='Area Details')
        self.areaDatas = ['area', 'month', 'date', 'commission']

        self.area = LabelEntry(area1, topKwargs=dict(text='Area'), place=dict(relx=0, rely=0, relw=1, relh=.24), orient='h', bottomKwargs=dict(_type='number'))

        self.month = LabelMonthYearButton(area1, topKwargs=dict(text='Month'), place=dict(relx=0, rely=.25, relw=1, relh=.24), orient='h', longent=.35)

        self.date = LabelDateButton(area1, topKwargs=dict(text='Date'), place=dict(relx=0, rely=.5, relw=1, relh=.24), orient='h', longent=.35)

        self.commission = Checkbutton(area1, text='Commission', place=dict(relx=0, rely=.79, relw=.4, relh=.15))


        Button(area1, text='Create', place=dict(relx=.5, rely=.79, relw=.4, relh=.15), command=lambda: PRMP_MsgBox(self, title='Create a Contribution?', message='Are you sure to create contribution?', ask=1, callback=self.create, _type='question'))



        cont1 = LabelFrame(fr1, place=dict(relx=0, rely=.45, relw=1, relh=.4), relief='groove', text='Contribution Details')
        self.contDatas = ['number', 'rate', 'amount']

        self.number = LabelEntry(cont1, topKwargs=dict(text='Number'), place=dict(relx=0, rely=0, relw=1, relh=.24), orient='h', bottomKwargs=dict(_type='number'))

        self.rate = LabelEntry(cont1, topKwargs=dict(text='Rate'), place=dict(relx=0, rely=.25, relw=1, relh=.24), orient='h', bottomKwargs=dict(_type='number'))

        self.amount = LabelEntry(cont1, topKwargs=dict(text='Amount'), place=dict(relx=0, rely=.5, relw=1, relh=.24), orient='h', bottomKwargs=dict(_type='number'))

        Button(cont1, text='Add', place=dict(relx=.77, rely=.77, relw=.2, relh=.17), command=self.add)


        settings = LabelFrame(fr1, place=dict(relx=0, rely=.86, relw=1, relh=.12), text='Settings')
        Button(settings, text='Clear', place=dict(relx=0, rely=0, relw=.24, relh=.9), command=self.clearIt)
        Button(settings, text='Load', place=dict(relx=.25, rely=0, relw=.24, relh=.9), command=self.load)
        Button(settings, text='Save', place=dict(relx=.5, rely=0, relw=.24, relh=.9), command=lambda: PRMP_MsgBox(self, title='Save?', message=f'Are you sure to save to {self.contributions.path if self.contributions else ""}', callback=self.save_, geo=(400, 300)))

        Button(settings, text='Update', place=dict(relx=.75, rely=0, relw=.24, relh=.9), command=self.updateCont)

        fr2 = Frame(cont, place=dict(relx=.4, rely=0, relw=.6, relh=1), relief='groove')

        self.tree = Hierachy(fr2, place=dict(relx=0, rely=0, relw=1, relh=.8), columns=columns)
        self.tree.tree.bind('<Delete>', self.delete)

        totals = LabelFrame(fr2, text='Totals', place=dict(relx=0, rely=.8, relw=1, relh=.2))
        self.totalsDatas = ['money', 'total']

        self.money = LabelLabel(totals, place=dict(relx=0, rely=0, relw=.5, relh=.4), topKwargs=dict(text='Money'), orient='h')
        self.total = LabelLabel(totals, place=dict(relx=0, rely=.5, relw=.5, relh=.5), topKwargs=dict(text='Contributions'), orient='h', longent=.6)

    def update(self):
        self.clear()
        if self.contributions:
            self.setTitle(self.contributions.name)
            self.set(self.contributions, widgets=[*self.totalsDatas, *self.areaDatas])

            self.tree.viewSubs(self.contributions)

    def clear(self, w=1):
        if not w: return
        self.setTitle('Contribution App')

        self.tree.clear()
        self.emptyWidgets([*self.areaDatas, *self.contDatas])

        for wid in [*self.areaDatas, *self.totalsDatas]: self[wid].set('')

    def clearIt(self):
        PRMP_MsgBox(self, title='Clear?', message='Are you sure to clear this current contribution?', ask=1, callback=self.clear, _type='question')


    def defaults(self):

        self.bind('<Control-L>', self.load)
        self.bind('<Control-l>', self.load)
        self.bind('<Control-O>', self.load)
        self.bind('<Control-o>', self.load)
        self.bind('<Control-S>', self.save_)
        self.bind('<Control-s>', self.save_)
        self.bind('<Control-N>', self.create)
        self.bind('<Control-n>', self.create)
        self.bind('<Control-u>', self.updateCont)
        self.bind('<Control-U>', self.updateCont)

        self.update()


    def add(self, e=0):
        if not self.contributions: return

        datas = self.get(self.contDatas)

        try:
            self.contributions.add(**datas)
            self.emptyWidgets(self.contDatas)
        except Exception as e: PRMP_MsgBox(self, title=e.__class__.__name__, message=e, _type='error')

        self.update()

    def delete(self, e=0):
        if not self.contributions: return
        sel = self.tree.selected()
        self.contributions.remove(sel)
        self.update()

    def getAreaData(self):
        contData = self.get(self.areaDatas)
        contData['area'] = int(contData['area'])
        return contData

    def updateCont(self, e=0):
        if not self.contributions: return

        contData = self.getAreaData()
        self.contributions.__dict__.update(contData)
        self.update()

    def create(self, w=0):
        if not w: return
        if self.contributions:
            PRMP_MsgBox(self, title='A Contribution in progress!', message='Are you sure to clear contribution to start a new?', ask=1, callback=self.clear, _type='question')
            return

        contData = self.getAreaData()
        self.contributions = Contributions(**contData)
        self.update()


    def load(self, e=0):
        file = dialogFunc(path=1, filetypes=['Contributions {.cont}'])
        if not file: return

        conts = Contributions.load(file)
        self.contributions = conts
        self.update()

    def save_(self, e=0):
        if not self.contributions: return
        self.updateCont()

        path = self.contributions.path
        if os.path.exists(path): PRMP_MsgBox(self, title='Already Exists', message=f'The path {path} for this contribution already exists, do you wish to overwrite?', ask=1, callback=self._save, geo=(400, 300), _type='error')
        else: self._save(e)

    def _save(self, w=0):
        if w: self.contributions.save()




