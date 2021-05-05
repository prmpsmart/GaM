
# Rates
# Contributions
# Paids
# Debits
# Upfronts

from src.utils.gam_config import GaM_Settings
from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime as PD

gam = GaM_Settings
# gam.loadAll()
# print(gam.GaM)

from src.backend.office.office_regions import DCOffice

dcoffice = DCOffice(manager='Mrs. Oloruntobi Beatrice', location='35b Esho street, Akure Ondo State.', date=PD(2017, 4, 7))
dcoffice[0]._date = PD(2021, 5, 1)
gam.GaM = dcoffice

areasM = dcoffice.areasManager

for _ in range(6): areasM.createArea()
from dc_datas import clients

pp = lambda obj: print(obj['name'])

month = PD.now()
for area_num, clients_datas in clients.items():
    area = areasM.getSub(number=area_num)
    areaAcc = area.accountsManager[0]
    clientsM = area.clientsManager
    multis = []
    
    for data in clients_datas:
        client = clientsM.createClient(**data)

        if accs:= data.get('accs'):
            name = data['name']
            lednum = list(accs.keys())[0]
            rate = list(accs.values())[0]
            multis.append([name, lednum, rate])
    
        if multis:
            current = areaAcc.ledgerNumbers + 1
            for name, lednum, rate in multis:
                if current == lednum:
                    client = clientsM.getSub(name=name)
                    client['accountsManager'].createAccount(rate=rate)

ar2 = areasM.getSub(number=2)


gla = ar2.clientsManager.getSub(name='Mum Ayo')


print(gla[:])
gam.saveAll()

