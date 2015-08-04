# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 12:05:01 2015

@author: PogrebnyakEV
"""

def iter1 ():
    yield 1
    yield 2
    yield 3
    
    
def iter2 ():
    for y in [1,2,3]:
      yield y
     
     
gen1 = iter1()
gen2 = iter2()    
 
def compare_iterables(gen1, gen2):
   for a, b in zip(gen1, gen2):
       assert a == b
