
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

dcoffice = DCOffice(manager='Mrs. Oloruntobi Beatrice', location='35b Esho street, Akure Ondo State.', date=PD(2017, 4, 7))
dcoffice[0]._date = PD(2021, 5, 1)
gam.GaM = dcoffice

for _ in range(6): dcoffice.areasManager.createArea()










obj = dcoffice#.areasManager
print(obj[:])
print(obj.date)
print(obj[0].date)



# GaM_Settings.saveAll()

# through the areasManager
    # through the accountsManager
        # create accounts
    # create area
        # through the clientsmanager
            # create clients (date, name, rate)
        # through the accountsManager
            # create accounts (date, month)
        # through the dailycontributionsManager
            # create daily contribution and add thrift
            # update the dailycontribution
        

















# print(gam.GaM)











