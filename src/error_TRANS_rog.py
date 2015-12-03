# -*- coding: utf-8 -*-

from save import get_dfm
from csv2db import import_csv


import_csv("../data/ind09/")
df = get_dfm()
print(df.TRANS_rog.head())

"""
в % к предыдущему периоду / percent of previous period																	
1999			101,3	100,6	106,0	…	91,3	115,6	94,8	101,9	96,8	101,6	101,9	98,0	106,1	98,3	105,6
2000		99,8	98,0	100,7	105,5	96,9	96,9	106,1	94,6	102,1	97,9	102,2	99,5	98,7	107,3	97,8	102,8
"""