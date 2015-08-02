# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 00:36:13 2015

@author: Евгений
"""

def push_annual(cursor, var_name, year, val):
    cursor.execute("INSERT OR REPLACE INTO annual VALUES (?, ?,  ?)", (var_name, year, val))

def push_quarter(cursor, var_name, year, quarter, val):
    cursor.execute("INSERT OR REPLACE INTO quarter VALUES (?, ?, ?, ?)", (var_name, year, quarter, val))

def push_monthly(cursor, var_name, year, month, val):
    cursor.execute("INSERT OR REPLACE INTO monthly VALUES (?, ?, ?, ?)", (var_name, year, month, val))


import sqlite3
conn = sqlite3.connect('kep.sqlite')
c = conn.cursor()

# Insert a row of data
c.execute("INSERT OR REPLACE INTO annual VALUES (?, ?,  ?)", ('153', 1000, 0))

c.executescript("""
DELETE FROM "main"."quarterly";
DELETE FROM "main"."monthly";
DELETE FROM "main"."annual";
""")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.




import sqlite3

def wipe_db_tables():
    conn = sqlite3.connect('kep.sqlite')
    c = conn.cursor()
    c.executescript("""
    DELETE FROM "main"."quarterly";
    DELETE FROM "main"."monthly";
    DELETE FROM "main"."annual";
    """)
    conn.commit()
    conn.close()