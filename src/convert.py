# -*- coding: utf-8 -*-
"""
"""

from batch import doc_to_database
from batch import make_raw_csv_and_headers, make_csv_with_labels, csv_to_database
from batch import make_csv_in_stei_folder
from database import wipe_db_tables
from label_csv_by_specification import check_vars_not_in_labelled_csv, inspect_labelled_output 
import os

src_doc = ["../data/1-07/1-07.doc", "../data/minitab/minitab.doc"] 


# make csv files
def batch01():
    for p in src_doc:
        p = os.path.abspath(p)
        make_raw_csv_and_headers(p)

def batch02():
    folder = "../data/ind06/"
    make_csv_in_stei_folder(folder)


def batch1():
    print("\n### Trial 1")
    p = os.path.abspath("../data/1-07/1-07.doc")
    wipe_db_tables()       
    doc_to_database(p)    
    check_vars_not_in_labelled_csv(p)
    inspect_labelled_output(p)
    
def batch2():
    print("\n### Trial 2")
    # omit making raw csv - as it is long 
    c = os.path.abspath("../data/minitab/minitab.csv")
    t = make_csv_with_labels(c)
    wipe_db_tables()       
    csv_to_database(t) 
    check_vars_not_in_labelled_csv(c)
    inspect_labelled_output(c)
    
def batch3():
    print("\n### Trial 3")
    # omit making raw csv - as it is long 
    c = os.path.abspath("../data/ind06/all_tab.csv") #all_tab got.csv
    t = make_csv_with_labels(c)
    wipe_db_tables()       
    csv_to_database(t) 
    check_vars_not_in_labelled_csv(c)
    inspect_labelled_output(c)
    
if __name__ == "__main__":
    p = os.path.abspath("../data/minitab/minitab.csv")
    inspect_labelled_output(p)
    # p = os.path.abspath("../data/1-07/1-07.csv")
    # inspect_labelled_output(p)
    # TODO - import from single table
    # import query   