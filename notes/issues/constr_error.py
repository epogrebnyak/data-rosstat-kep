from rowsystem.maincall import datafolder_objects
from kep.importer.converter.word import make_csv

rs, kep = datafolder_objects()
print("Not imported:", rs.not_imported()) 
print("Problem 1.")
print("Line 1402 not imported, because it has extra \" at start of text:" )
print(rs.rowsystem[1402]['list'][0])
print("Source of problem: rowsystem/word.py behaviour. Modelled at data/fragments/constr_error.")
print("---")


print("Now replicating error of Word file conversion:")
print("printout below will have \"1.8. Объем работ...")

# must run on Windows machine 
import os
from rowsystem.config import PROJECT_ROOT_PATH
from rowsystem.classes import RowSystem
folder = os.path.join(PROJECT_ROOT_PATH, 'data', 'fragments', 'constr_error')
csv = os.path.join(folder, "tab.csv")
#os.remove(csv)

def show_sample(folder):
    z = RowSystem(folder)
    for i in range(6):
        print("Line ", i, ": ", z.rowsystem[i]['list'][0])
    print("...")
    return z.rowsystem[2]['list'][0]
s1 = show_sample(folder)    
    
print("---")
print("Different import function:")
print("printout below will not have \"  at start of line 1.8. Объем работ...")
#os.remove(csv)
make_csv(folder)
s2 = show_sample(folder)

PAT = "\x221.8. Объем работ по виду деятельности \x22\x22Строительство\x22\x22"
print(s1.startswith(PAT))
print(s2.startswith(PAT))