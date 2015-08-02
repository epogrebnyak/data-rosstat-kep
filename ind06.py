# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 15:53:59 2015

@author: Евгений
"""

from word import make_raw_csv_and_headers
import os

files = ["tab" + str(x) + ".doc" for x in range(0,5)] 
files[0] = "tab.doc"
folder = "data/ind06/"
for p in [os.path.abspath(folder + fn) for fn in files]:
    make_raw_csv_and_headers (p)
    
