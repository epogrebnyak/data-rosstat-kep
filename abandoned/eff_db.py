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
    
def iter_person():
    for r in persons:
        yield r

con = sqlite3.connect(":memory:")

# Create the table
con.execute("create table person(firstname, lastname)")

gen = iter_person()
# Fill the table
con.executemany("insert into person(firstname, lastname) values (?, ?)", gen)

# Print the table contents
for row in con.execute("select firstname, lastname from person"):
    print(row)

print("I just deleted", con.execute("delete from person").rowcount, "rows")


#    # Print the table contents
#    print("Inside database:")     
#    for row in conn.execute("select label, year, val from annual"):
#        print(row)
#    for row in conn.execute("select label, year, month, val from monthly"):
#        print(row)
#    for row in conn.execute("select label, year, qtr, val from quarterly"):
#        print(row)