# -*- coding: utf-8 -*-
"""
Created on Mon May 22 17:11:48 2017

@author: PogrebnyakEV
"""

def extract_duplicates(items):
    dup_dict = {x:items.count(x) for x in items}
    dups = [k for k,v in dup_dict.items() if v>1]
    return dups

def unique(items):
    sorted(list(set(items)))    
    
class Seq():
    def __init__(items):
        self.items = items
        self.duplicates = extract_duplicates(items)
        self.count = {x:items.count(x) for x in items} 
        self.unique = unique(items)
        
