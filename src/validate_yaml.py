# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 02:15:13 2015

@author: Евгений
"""
import yaml as ya
import os

with open(os.path.abspath("../data/ind06/all_tab_spec.txt")) as d:
    z3 = ya.load_all(d)
    for z in z3:
        print (z) 
