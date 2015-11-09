# -*- coding: utf-8 -*-
"""Write stream of data to sqlite database.
   Read from sqlite database into pandas DataFrame. 
"""

import sqlite3
import pandas as pd

DB_FILE = 'db//kep.sqlite'

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
    c.executescript("""
    DELETE FROM "main"."data";
    """)    
    # /* DELETE FROM "main"."quarterly";
    #    DELETE FROM "main"."monthly";
    #    DELETE FROM "main"."annual"; */
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
    if lit in "qma":  
        return pd.read_sql_query("SELECT * from data where freq = \'{}\' ".format(lit), con)
    else:
        raise ValueError

def get_annual(con):
    return get_freq(con, "a")

def get_quarterly(con):
    return get_freq(con, "q")

def get_monthly(con):
    return get_freq(con, "m")

def read_dfs(db_file = DB_FILE):
    """Get all of DB_FILE as annual, quarterly and monthly dataframes."""
    con = sqlite3.connect(db_file)
    dfa = get_annual(con)
    dfq = get_quarterly(con)
    dfm = get_monthly(con)
    con.close()
    return dfa, dfq, dfm

def get_period_value(df, label, year, quarter=None, month=None):
    indexer = (df.label == label) & (df.year == year)
    if quarter is not None:
        indexer &= (df.qtr == quarter)
    if month is not None:
        indexer &= (df.month == month)
    filtered = df[indexer]
    assert len(filtered.index) == 1
    return filtered.iloc[0].val

def test_database():
    from stream import get_test_flat_db_rows
    gen = get_test_flat_db_rows()
    #_create_table()
    # wipe_db_tables()
    stream_to_database(gen)
    dfa, dfq, dfm = read_dfs(db_file = DB_FILE)
    assert get_period_value(dfa, 'I_yoy', 2014) == 97.3    

if __name__ == "__main__":
    #test_database()
    pass