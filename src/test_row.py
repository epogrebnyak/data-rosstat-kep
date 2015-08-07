# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 04:08:30 2015

@author: EP
"""

from word import reader12_with_annual
row = ["1999", '27,00', '22,60', '22,86', '24,18', '24,23', '24,44', '24,22', '24,19', '24,75', '25,08', '26,05', '26,42', '27,00']
y, a, q, m = reader12_with_annual(row)
assert y == '1999'
assert q == None
assert a == '27,00'    
assert len (m) == 12 
assert a == m[-1]