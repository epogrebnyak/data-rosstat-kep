# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:22:13 2015

@author: Евгений
"""

from word import doc_to_database, make_reabable_csv
import os


# Trial 1
p = os.path.abspath("data/1-07/1-07.doc")
doc_to_database(p)
    

# Trial 2
p = os.path.abspath("data/minitab/minitab.doc")
doc_to_database(p)

#from word import load_spec, change_extension, make_labelled_csv
#r = os.path.abspath("data/minitab/minitab2.csv")
#src_csv = r
#label_dict, sec_label_dict = load_spec(src_csv)
#
#out_csv = change_extension(src_csv,"txt")
#make_labelled_csv(src_csv, out_csv, label_dict, sec_label_dict)
#
##t = os.path.abspath("data/minitab/minitab.txt")
#csv_to_database(t) 
    