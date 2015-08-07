# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 17:10:39 2015

@author: EP
"""

def get_labels_from_iter(gen):
    return set(row[0] in gen)
        