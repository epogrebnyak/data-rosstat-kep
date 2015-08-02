# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 01:58:32 2015

@author: Евгений
"""

from datetime import date
from dateutil.relativedelta import relativedelta

def get_end_of_monthdate(y,m):
   retrun date(year=y, month=m, day=1) + relativedelta(months=+1) +  relativedelta(days = -1)


for i in range(0,12):
   print(i+1)
   dt = date(year=2015, month=i+1, day=1) + relativedelta(months=+1) +  relativedelta(days = -1)
   print(dt + relativedelta(days = -1))