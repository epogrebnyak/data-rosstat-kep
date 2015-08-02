# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:22:13 2015

@author: Евгений
"""

from word import  make_reabable_csv
src_doc = ["1-07.doc", "ind06/tab.doc", "minitab/minitab.doc"] 
p = os.path.abspath(src_doc[2])
c = make_reabable_csv(p)
