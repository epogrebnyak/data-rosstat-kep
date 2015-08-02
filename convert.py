# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:22:13 2015

@author: Евгений
"""

from word import make_raw_csv_and_headers, make_reabable_csv, csv_to_database
from word import load_spec
import os

#for fn in ["data/1-07/1-07.doc", "data/ind06/tab.doc", "data/minitab/minitab.doc"]:

#fn = "data/minitab/minitab.doc"
#p = os.path.abspath(fn)

# c, h = make_raw_csv_and_headers(p)
c = os.path.abspath("data/minitab/minitab.csv")
t = make_reabable_csv(c)
t = os.path.abspath("data/minitab/minitab.txt")
csv_to_database(t) 