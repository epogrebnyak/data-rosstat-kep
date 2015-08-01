# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 21:15:01 2015

@author: Евгений
"""

def is_year(s):
    try:
        int(s)
        return True        
    except:
        return False
        