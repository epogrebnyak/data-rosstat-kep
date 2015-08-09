# -*- coding: utf-8 -*-
"""
"""
import os

from doc2db import raw_csv_to_database
from doc2db import check_vars_not_in_labelled_csv
from doc2db import wipe_db_tables

# suspend below - it will overwrite on machines with no Word installed
# p = os.path.abspath("../data/1-07/1-07.doc")
# doc_to_database(p)

def job1():
    p = os.path.abspath("../data/1-07/1-07.csv")
    raw_csv_to_database(p)
    check_vars_not_in_labelled_csv(p)

def job2():
    p = os.path.abspath("../data/minitab/minitab.csv")
    raw_csv_to_database(p)
    check_vars_not_in_labelled_csv(p)

def job3():    
    p = os.path.abspath("../data/ind06/tab.csv")
    raw_csv_to_database(p)
    check_vars_not_in_labelled_csv(p)

if __name__ == "__main__":
    wipe_db_tables()
    job3()
    import doc2db.query
