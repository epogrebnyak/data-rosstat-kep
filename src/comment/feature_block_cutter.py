# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 11:39:08 2015

@author: Евгений
"""

from word import yield_csv_rows_between_labels as fcut
import os 

f = os.path.abspath("../data/ind06/all_tab.csv")
s1 = "2.2. Сальдированный финансовый результат"
e1 = "Убыточные организации"

s2 = e1
e2 = "2.3. Кредиты, депозиты и прочие размещенные средства"

for row in fcut(f, s1, e1):
    print(row)
    
    