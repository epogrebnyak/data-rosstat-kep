# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 14:16:06 2015

@author: Евгений
"""

s = "“Mining and quarrying”"

# symbol \u201c and  \u201d raise error when printing in console
# print(s)

print(s.encode("utf-8"))
print(s.encode("cp1251"))
s = s.replace("\u201c", '"')
s = s.replace("\u201d", '"')
print(s)