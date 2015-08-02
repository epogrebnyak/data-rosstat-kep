# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:22:13 2015

@author: Евгений
"""

from word import doc_to_database, make_readable_csv, write_to_database
from word import wipe_db_tables, load_spec
from pprint import pprint
import os

src_doc = ["data/1-07/1-07.doc", "data/ind06/tab.doc", "data/minitab/minitab.doc"] 

wipe_db_tables()   

## Trial 1
#p = os.path.abspath("data/1-07/1-07.doc")
#doc_to_database(p)    

## Trial 2
##p = os.path.abspath("data/minitab/minitab.doc")
#c = os.path.abspath("data/minitab/minitab.csv")
#r = make_readable_csv(c)
#r = os.path.abspath("data/minitab/minitab.txt")
#write_to_database(r)

# Trial 3
c = os.path.abspath("data/ind06/all_tab.csv")
a,b,e = load_spec(c)
r = make_readable_csv(c)
write_to_database(r)

