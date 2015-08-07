# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 04:53:52 2015

@author: EP
"""

import sqlite3
conn = sqlite3.connect('kep.sqlite')
c = conn.cursor()

# Insert a row of data
c.execute("SELECT * FROM annual WHERE label = 'RETAIL_SALES_rog' ")

for p in c:
    print (p)

# Save (commit) the changes
conn.commit()