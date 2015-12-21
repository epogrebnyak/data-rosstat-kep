# -*- coding: utf-8 -*-
"""Write stream of data to sqlite database.
   Read from sqlite database into pandas DataFrame. 
"""

import functools
import sqlite3
import pandas as pd

# path only relative to 'kep'
# DB_FILE = 'kep//database//kep.sqlite'
from kep.paths import DB_FILE 

def _create_table(file = DB_FILE):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute('''CREATE TABLE if not exists "data" 
    ("freq" CHAR NOT NULL, 
    "label" VARCHAR NOT NULL, 
    "year" INTEGER NOT NULL, 
    "qtr" INTEGER, 
    "month" INTEGER, 
    "val" FLOAT NOT NULL , 
    PRIMARY KEY ("freq", "label", "year", "qtr", "month", "val"))''')
    conn.commit()
    conn.close()

def wipe_db_tables(file = DB_FILE):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.executescript(""" DELETE FROM "main"."data" """)
    conn.commit()
    conn.close()

def stream_to_database(stream, db_file = DB_FILE):
    """
    Incoming *stream* of tuples (freq, year, qtr, month, label, val) written to db_file
    """
    conn = sqlite3.connect(db_file)
    conn.executemany("INSERT OR REPLACE INTO data VALUES (?, ?, ?, ?, ?, ?)", stream)
    conn.commit() 
    conn.close() 

# Read sqlite query results into pandas DataFrame
def get_freq(con, lit):
    if lit in ('q','m','a'):  # fixed unexpected behavior e.g. "qm" or "ma" returned True
        return pd.read_sql_query("SELECT * from data where freq =?", con,params=(lit,)) # assembling query with Python's string operations is insecure; DB-API parameter substitution used instead
    else:
        raise ValueError

def get_annual(con):
    return get_freq(con, "a")

def get_quarterly(con):
    return get_freq(con, "q")

def get_monthly(con):
    return get_freq(con, "m")
    
def select_unique_labels(con):
    return pd.read_sql_query("SELECT DISTINCT label from data", con)   


#@functools.lru_cache()
def read_dfs(db_file = DB_FILE):
    """Get all of DB_FILE as annual, quarterly and monthly dataframes."""
    con = sqlite3.connect(db_file)
    dfa = get_annual(con)
    dfq = get_quarterly(con)
    dfm = get_monthly(con)
    con.close()
    return dfa, dfq, dfm

def get_unique_labels(db_file = DB_FILE):
    con = sqlite3.connect(db_file)
    df = select_unique_labels(con)
    con.close()
    return sorted(df['label'].tolist())        
    
def get_period_value(df, label, year, quarter=None, month=None):
    indexer = (df.label == label) & (df.year == year)
    if quarter is not None:
        indexer &= (df.qtr == quarter)
    if month is not None:
        indexer &= (df.month == month)
    filtered = df[indexer]
    assert len(filtered.index) == 1
    return filtered.iloc[0].val



if __name__ == "__main__":
    #test_database()
    pass
    #print (get_unique_labels())
