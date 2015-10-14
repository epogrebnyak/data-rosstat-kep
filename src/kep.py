# -*- coding: utf-8 -*-
"""
Extract, store and export economic indicator times series from Rosstat 'KEP' publication.

KEP publication URL:
    http://www.gks.ru/wps/wcm/connect/rosstat_main/rosstat/ru/statistics/publications/catalog/doc_1140080765391

Workflow:
    (1) Convert from Word to raw CSV
        word -> csv1        
        doc_to_csv(p)
    
    (2) Label CSV using yaml config file 
        csv1 + yaml -> csv2        
        labelize_csv(p)
    
    (3) Store CSV in flat database
        csv2 -> db          
        csv_to_database(p)
    
    (4) Export data to CSV and Excel files
        db -> csv + xls   
        database_to_xl()
        
    Supplementary jobs:
    (5)  csv1 -> headers -> yaml file     Create headers and yaml config file

Command line syntax (not implemented):
    kep.py convert  <FILE>
    kep.py labelize <FILE>
    kep.py read     <FILE> 
    kep.py dump  
    
"""
import os

from doc2db import wipe_db_tables
from doc2db import doc_to_csv, folder_to_csv
from doc2db import labelize_csv, csv_to_database, database_to_xl
from doc2db import check_vars_not_in_labelled_csv

def csv_job(f):    
    labelize_csv(f)
    csv_to_database(f)
    check_vars_not_in_labelled_csv(f)
   
if __name__ == "__main__":
    
    #### Convert DOC files
    #### COMMENT: will overwrite exisitng raw CSV files on machines with no Word installed    
    
    #### Task 1.1 : make single large CSV file form KEP publication
    folder = os.path.abspath("../data/ind06/")
    # folder_to_csv(folder)
    
    #### Task 1.2 : make CSV file form single doc file
    d = os.path.abspath("../data/1-07/1-07.doc")
    # doc_to_csv(d)
    
    #### Task 2: reset database, import CSV and dump to Excel from database
    wipe_db_tables()    
    p = list(range(3))
    p[0] = os.path.abspath("../data/1-07/1-07.csv")
    p[1] = os.path.abspath("../data/minitab/minitab.csv")
    p[2] = os.path.abspath("../data/ind06/tab.csv") 
    csv_job(p[0])    
    database_to_xl()    