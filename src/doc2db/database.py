# -*- coding: utf-8 -*-
"""Write stream to database."""

import sqlite3
import pandas as pd

try:
    from .stream import emit_flat_data 
except ImportError:
    from stream import emit_flat_data 

DB_FILE = 'kep.sqlite'

def wipe_db_tables(file = DB_FILE):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.executescript("""
    DELETE FROM "main"."data";
    DELETE FROM "main"."quarterly";
    DELETE FROM "main"."monthly";
    DELETE FROM "main"."annual";
    """)
    conn.commit()
    conn.close()
    
def write_to_database(p):
    gen = emit_flat_data(p)
    stream_to_database(gen)

def stream_to_database(stream, db_file = DB_FILE):
    """
    Incoming *stream* is iterator of tuples (freq, year, qtr, month, label, val)
    """
    conn = sqlite3.connect(db_file)
    conn.executemany("INSERT OR REPLACE INTO data VALUES (?, ?, ?, ?, ?, ?)", stream)
    conn.commit() 
    conn.close() 
    

# Read sqlite query results into  pandas DataFrames

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

def read_dfs (db_file = DB_FILE):
    con = sqlite3.connect(db_file)
    dfa = get_annual(con)
    dfq = get_quarterly(con)
    dfm = get_monthly(con)
    con.close()
    return dfa, dfq, dfm

if __name__ == "__main__":
    import os
    from stream import emit_flat_data
    p = os.path.abspath("../data/1-07/1-07.txt")
    gen = emit_flat_data(p)
    write_to_database(gen)
    