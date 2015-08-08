# -*- coding: utf-8 -*-
"""Write stream to database."""

import sqlite3

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
    
def write_to_database(stream, db_file = DB_FILE):
    """
    Incoming *stream* is iterator of tuples (freq, year, qtr, month, label, val)
    """
    conn = sqlite3.connect(db_file)
    conn.executemany("INSERT OR REPLACE INTO data VALUES (?, ?, ?, ?, ?, ?)", stream)
    conn.commit() 
    conn.close() 

if __name__ == "__main__":
    import os
    from stream_from_labelled_csv import emit_flat_data
    p = os.path.abspath("../data/1-07/1-07.txt")
    gen = emit_flat_data(p)
    write_to_database(gen)
    