from rowsystem.maincall import datafolder_objects

rs, kep = datafolder_objects()
print("Not imported:", rs.not_imported()) 
print("Problem 1.")
print("Line 1402 not imported, because it has extra \" at start of text:" )
print(rs.rowsystem[1402]['list'][0])
print("Source of problem: rowsystem/word.py behaviour. Modelled at data/fragments/constr_error.")

# must run on Windows machine 
import os
from rowsystem.config import PROJECT_ROOT_PATH
from rowsystem.rowsystem import RowSystem
folder = os.path.join(PROJECT_ROOT_PATH, 'data', 'fragments', 'constr_error')
#z = RowSystem(folder)
#for x in z.rowsystem:
#    print(x['list'][0])
