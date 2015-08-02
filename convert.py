# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:22:13 2015

@author: Евгений
"""

from word import doc_to_database, make_readable_csv, csv_to_database
import os

# Trial 1
p = os.path.abspath("data/1-07/1-07.doc")
doc_to_database(p)    

# Trial 2
#p = os.path.abspath("data/minitab/minitab.doc")
#c = os.path.abspath("data/minitab/minitab.csv")
#r = make_readable_csv(c)
#csv_to_database(r) 

    