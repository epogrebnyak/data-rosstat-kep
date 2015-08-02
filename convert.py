# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:22:13 2015

@author: Евгений
"""

from word import doc_to_database
import os

# Trial 2
p = os.path.abspath("data/minitab/minitab.doc")
#doc_to_database(p)
t = os.path.abspath("data/minitab/minitab.txt")
csv_to_database(t) 
    