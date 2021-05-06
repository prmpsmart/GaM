from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime

# Rates
# Contributions
# Paids
# Debits
# Upfronts

from src.utils.gam_config import GaM_Settings
from prmp_lib.prmp_miscs.prmp_datetime import PRMP_DateTime as PD

gam = GaM_Settings
# gam.loadAll()
print(gam.GaM)

from src.backend.office.office_regions import DCOffice

dcoffice = DCOffice(manager='Owode', location='35b Esho street, Akure Ondo State.', date=PD(2017, 4, 7))
dcoffice[0]._date = PD(2021, 5, 1)
gam.GaM = dcoffice

areasM = dcoffice.areasManager

for _ in range(6): areasM.createArea()
gam.saveAll()
exit()

def dt(day, month): return PRMP_DateTime(2021, month, day)

def d(**kwargs):
    ret = {}
    for k, v in kwargs.items():
        if k == 'c': name = 'current'
        elif k == 'l': name = 'last'
        elif k == 'u': name = 'upfrontLoan'
        elif k == 'r': name = 'upfrontRepay'
        elif k == 'w': name = 'withdraw'
        elif k == 't': name = 'transfer'
        elif k == 'b': name = 'bto'
        elif k == 'n': name = 'next'
        elif k == 'p': name = 'paidout'
        else: name = k
        ret[name] = v
    return ret


def c(n, r, d=(6, 5), accs={}):
    ret = dict(name=n, rate=r, date=dt(*d))
    if accs: ret['accs'] = accs
    return rett

clients = {
    2: [c('Ileri', 500, (16, 4)),
        c('Owolabi', 300, (19, 4)),
        c('Anuoluwapo', 200, (20, 4)),
        c('Similoluwa', 200, (21, 4)),
        c('Pelu', 200, (22, 4)),
        c('Akindebo', 1000, (23, 4)),
        c('Toyin', 200, (23, 4)),
        c('Esther', 200, (26, 4)),
        c('Mum Faheed', 300, (27, 4)),
        c('Monsuru', 100, (29, 4)),
        c('Iya Laje', 700, (29, 4)),
        c('Glamour', 1000, (30, 4), accs={21: 500, 'date': dt(3, 5)}),
        c('N/D', 400, (30, 4)),
        c('Wuraola', 200, (30, 4)),
        c('Mum Bose', 200, (30, 4)),
        c('Moni', 300, (30, 4)),
        c('Pemisire', 500, (30, 4)),
        c('Grandma', 100, (30, 4)),
        c('Segun', 100, (3, 5)),
        c('Lizzy', 500, (3, 5)),
        c('Lolade', 200, (3, 5)),
        c('Kudirat', 200, (3, 5)),
        c('Daddy Blessing', 200, (3, 5)),
        c('Ismail', 500, (3, 5)),
        c('Bidex', 200, (3, 5)),
        c('Mum Feranmi', 300, (3, 5)),
        c('Tailor', 200, (3, 5)),
        c('Mum Ayo', 600, (3, 5), accs={30: 200, 'date': dt(3, 5)}),
        c('Car Wash', 300, (3, 5)),
        c('Mum Onisu', 200, (3, 5)),
        c('Mum Dunsin', 200, (4, 5)),
        c('Anyashu', 500, (4, 5)),
        c('Bisola', 200, (5, 5)),
        c('Ope Child', 100, (5, 5)),
        c('Ope', 200, (5, 5)),
        c('Mummy David', 300, (5, 5)),
        c('Thank God', 200, (5, 5)),
        c('Arowojolu', 300, (5, 5)),
        c('Akinola', 200),
        c('Oluwaseun', 100),
        c('Mum Mope', 200),
        c('Kenny', 100),
        c('Dupe', 200)
        
        
        ],
    
    4: [
        c('Iya Eko', 500),
        c('Alaja', 500),
        c('Kadijat', 500),
        c('Mum Mercy', 200),
        c('Mummy Esther', 500),
        c('Aduragbemi', 200),
        c('Gift', 200),
        c('Chimoa', 100),
        c('Engr RSK', 1000),
        c('Olaoluwa', 200),
        c('David Moses', 500),
        c('Alaule', 500),
        c('Iya Pelu', 500),
        c('Gift Asewo', 500),
        c('Eko', 500),
        c('Tunde', 500),
        c('Oluchi', 200),
        c('Oyindamola', 200),
        c('Ayuba', 500),
        c('Mum Amarachi', 100),
        c('Alarapon Opeyemi', 200),
        c('Mummy Dolapo', 300, accs={83: 200}),
        c('Mummy Bose', 300),
        c('Segun', 500),
        c('Mosun POS', 200),
        c('Iya Seun', 400),
        c('Funmilayo', 300),
        c('Daddy Samson', 500),
        c('Mummy Damilare', 1000),
        c('Miss Tosin', 200),
        c('Blessing', 300),
        c('Esther', 300),
        c('Vera', 500, accs={34: 200}),
        c('Sandral', 200),
        c('Taiwo Ijebu', 500),
        c('Alfa Oil', 500),
        c('Blessing Ijebu', 500),
        c('Moyo', 500),
        c('Sunday', 500),
        c('Tola', 500),
        c('Mummy Posi', 500),
        c('Doyin', 100),
        c('Adetutu', 100),
        c('Mummy Tunde', 200),
        c('Kemisola', 500),
        c('Iya Ife', 400),
        c('Umaru', 300),
        c('Emeka Kingsly', 500),
        c('Ezema', 200),
        c('Mummy Shola', 300),
        c('Olusola', 200),
        c('Endurance', 200, accs={55: 100}),
        c('Timex', 300),
        c('Titilayo', 300, accs={58: 200}),
        c('Oluwaseun', 200),
        c('Bassey', 500),
        c('Mr Patrick', 1500),
        c('Iyabo', 100),
        c('Iya Envelope', 200),
        c('Emaka PO', 700),
        c('Mummy Richard', 500),
        c('Muhammed Goni', 1000),
        c('Mummy Iyanu', 300),
        c('Cecillia', 100),
        c('Victoria Nathaniel', 300),
        c('Orobo Asewo', 500),
        c('Mercy Isaac', 1000),
        c('J. One', 500),
        c('Omowunmi', 1000),
        c('Hannah', 100),
        c('Glory', 400),
        c('Chairman', 1000),
        c('Rotimi', 500),
        c('Precious 3', 500),
        c('Mercy Odosai', 100),
        c('Azubuike', 200),
        c('Banjex', 300),
        c('Mum Semilore', 300),
        c('Mama', 300),
        c('Mum Victor', 200),
        c('Mercy P. Office', 500),
        c('Mum Kemi', 300),
        c('Ewe', 500),
        c('Deborah', 200),
        c('Gladys', 300),
        c('Mum Kinsley', 200),
        c('Deborah Hairdresser', 200),
        c('Adesida', 200),
        c('Omolara Ibunkun', 200)
        
        
        ],

    5: [c('Basira', 500),
        c('Iya Teni', 200),
        c('Blessing', 200),
        c('Toland', 200, accs={10: 200}),
        c('Mum Samuel', 500),
        c('Yemi 2', 400),
        c('Oluwaseun', 200, accs={8: 300}),
        c('Olarenwaju Peter', 200),
        c('Iya Simbi', 500),
        c('Mummy Pamilerin', 200),
        c('Blessing Owode', 700),
        c('Mum Tope', 200),
        c('Sis Bukky', 250),
        c('Aunty Yinka', 1000),
        c('Mum Aanu', 1000),
        c('Mum Odun', 400),
        c('Mum Ayo', 300),
        c('Demilade', 200),
        c('Iya Ope', 300),
        c('Iya Arewa', 300),
        c('Fatai', 300),
        c('Aishatu', 200),
        c('Rukayatu', 300),
        c('Oluwatosin', 200),
        c('Mummy Ope', 500, accs={28: 200}),
        c('Iya Eleko', 200),
        c('Deyade Toyin', 200),
        c('Mum Bukky', 200),
        c('Mummy Yetunde', 150),
        c('Mum Marvel', 200),
        c('Mutiu', 200),
        c('Mrs Owolanke', 500),
        c('Iya Gbolahan', 200),
        c('Temi', 3000),
        c('Mrs Aboluaye', 200),
        c('Mum Clinton', 200),
        c('Ijaboyede', 1000),
        c('Semilore', 200),
        c('Adejori', 200),
        c('Merit', 1000),
        c('Adelua', 200),
        c('Mum Samuel, Ondo Road', 500),
        c('Mum Sam', 200),
        c('Mum Marvel', 500),
        c('Suraju', 500),
        c('Oga Welder', 500),
        c('Mum Tosin', 200)
        
        ],

    6: [c('Daddy Alia', 300),
        c('Nifemi', 100),
        c('Adekunle Oluwabusuyi', 100),
        c('Abiola', 200),
        c('Mummy Ayo', 200),
        c('Olawole Adegoke', 200),
        c('Oreofe', 500),
        c('Slew', 100),
        c('Gafaru', 500),
        c('Ajibola', 500),
        c('Hikimat', 300),
        c('Elizabeth', 200),
        c('Bro Segun', 200),
        c('Mary', 300),
        c('Mummy Progress', 1000),
        c('Mama', 200),
        c('Iya Gbolahan', 100),
        c('Adesikemi', 300, accs={19: 300}),
        c('Mummy Love', 500),
        c('Mummy Bright', 200),
        c('Omotosho', 300),
        c('Iyanu Settar', 300),
        c('Marvelous', 100),
        c('Olajuwon', 200),
        c('Mummy Damilola', 250),
        c('Mummy Akorede', 200),
        c('Kenny', 200),
        c('Tailor', 100),
        c('Akara 1', 200),
        c('Hefkey', 200),
        c('Miss Tominiyi', 200),
        c('Blessing', 200),
        c('Mrs Omage', 200),
        c('Barakadu', 100),
        c('Anty Yemi', 2500),
        c('Sis Fajoke', 100),
        c('Boluwatife', 100),
        c('Sunday Joy', 500),
        c('Iya Sakiratu', 500),
        c('Sis Bidemi', 100),
        c('R.B Owoyemi', 200),
        c('Bro Monday', 500),
        c('Bro Eniola', 300),
        c('Mrs Olayemi', 200),
        c('Bro Tolu', 200),
        c('Sis Princess', 100),
        c('Mrs Julex', 300),
        c('Mr Adebayo', 200),
        c('Sis Tailor', 200),
        c('Francis Janet', 200)
        
        
        ]}


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
clac = ar2[0].clientsAccounts
# gla = ar2.clientsManager.getSub(name='Mum Ayo')

# print(clac[:])
gam.saveAll()




