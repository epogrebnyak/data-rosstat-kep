# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 01:30:56 2015

@author: Евгений
"""


from word import split_row_by_periods, reader12 

def test_row_split1():   
    row = [2007, 6716.2, 897.6, 1414.4, 1744.1, 2660.1, 255.3, 298.0, 344.3, 364.5, 
       472.2, 577.7, 543.1, 584.2, 616.8, 684.7, 740.4, 1235.0]
    y, a, q, m = split_row_by_periods(row)
    assert y == 2007
    assert len (q) == 4
    assert len (m) == 12    
    assert sum (q) == a
    assert sum (m) == a

def test_row_split2():   
    row = ['1999', '196.9', '203.3', '207.6', '213.1', '216.7', '220.7', '226.5',
                   '221.0', '162.0', '157.1', '150.5', '136.5']
    y, a, q, m = reader12(row)
    assert y == '1999'
    assert q == None
    assert a == None    
    assert len (m) == 12  