# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 02:36:45 2015

@author: Евгений
"""

def delete_double_space(line):
    return " ".join(line.split())
       
print(delete_double_space("a  2          3b")) 
assert delete_double_space("a  2          3b") == "a 2 3b"