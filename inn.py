# -*- coding: utf-8 -*-
import pandas as pd
from openpyxl import load_workbook

XL_FILE = dict(filename="clients.xlsx", sheet=1)

def yield_xlsx_rows(filename, sheet):
    wb = load_workbook(filename)
    ws = wb.worksheets[sheet]
    for row in ws.rows:
        yield [cell.value for cell in row]

rows = list(yield_xlsx_rows(**XL_FILE))
COLUMNS = ['id', 'title', 'desc', 'tag', 'fi', 'fo', 'fb', 'f4', 'inn']
PIVOT_ROW = rows[3]

def yield_dicts():
    for row in rows[6:]:
        large_dict = dict(zip(PIVOT_ROW, row))
        yield {k:large_dict[k] for k in COLUMNS}
        
z = [x for x in yield_dicts()] 
assert z[0]['inn']==7735128151 #"Ангстрем-Т, ОАО"
df = pd.DataFrame(z)
ix = df[['inn']].notnull()
inn_df= df[ix][['id', 'inn', 'title', 'tag', 'fi', 'fo', 'fb', 'f4', ]]
