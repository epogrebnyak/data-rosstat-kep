# MAYDO: write fixture here with some importable files
# TODO: add new specification to current month folder 

import os 
from rowsystem import RowSystem
from db_interface import KEP
from path_config import CURRENT_MONTH_DATA_FOLDER, current_folder

folder =  CURRENT_MONTH_DATA_FOLDER

rs = RowSystem(folder)
    # reads input definition from standard files
    # labels rows
    # starts pandas interface

rs.save()
    # saves data to default database or freeze files 

kep = KEP()
dfa = kep.get_annual()
print(dfa.to_csv())
