# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 14:00:41 2015

@author: Евгений
"""

from label_csv import dump_labelled_rows_to_csv, inspect_labelled_output, check_vars_not_in_labelled_csv
import os

c = os.path.abspath("../data/ind06/tab.csv")
inspect_labelled_output(c)


#t = dump_labelled_rows_to_csv(c)
#check_vars_not_in_labelled_csv(c)

print("“Mining and quarrying”") 