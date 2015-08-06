# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 02:09:37 2015

@author: EP
"""

from word import dump_labelled_rows_to_csv, check_vars_not_in_labelled_csv, csv_to_database
import os    

    
f = os.path.abspath("../data/ind06/all_tab.csv") #all_tab got.csv
r = dump_labelled_rows_to_csv(f)
print("Written to:   \n", r)
check_vars_not_in_labelled_csv(f)
csv_to_database(r)