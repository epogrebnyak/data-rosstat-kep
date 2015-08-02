# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 13:22:13 2015

@author: Евгений
"""

from word import make_reabable_csv_and_headers as preconvert
import os

for fn in ["data/1-07/1-07.doc", "ind06/tab.doc", "minitab/minitab.doc"]:
    p = os.path.abspath(fn)
    s = preconvert(p)
