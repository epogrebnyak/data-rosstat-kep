# -*- coding: utf-8 -*-
"""
Created on Fri May 26 11:15:38 2017

@author: PogrebnyakEV
"""

import re

line1 = "2.1.5. Объем торговли"
line2 = "\"Объем торговли"
# \"* 
# \"*[\d.]*\s*(.*)\"*[\d.]*\s*(.*)
regex = r'\"?'  +   r'[\d.]*' + r'\s*' + r'(.*)' 
#regex = r"\"*[\d.]*\s*(.*)"
for l in (line1, line2):
    matches = re.findall(regex, l)
    print("found:", matches[0])
    
def supress_section(line):
    regex = r'\"?'  +   r'[\d.]*' + r'\s*' + r'(.*)' 
    matches = re.findall(regex, line)
    return matches[0]
                          
    
