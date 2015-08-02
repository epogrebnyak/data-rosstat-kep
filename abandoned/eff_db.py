# -*- coding: utf-8 -*-
import sqlite3

con = sqlite3.connect(":memory:")

# Create the table
con.execute("create table person(firstname, lastname)")


import sqlite3

persons = [
    ("Hugo", "Boss"),
    ("Calvin", "Klein")
    ]

con = sqlite3.connect(":memory:")

# Create the table
con.execute("create table person(firstname, lastname)")

# Fill the table
con.executemany("insert into person(firstname, lastname) values (?, ?)", persons)