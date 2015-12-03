# -*- coding: utf-8 -*-

from database import wipe_db_tables as wipe
from save import get_dfm
from csv2db import import_csv

# This should clear the database
wipe()
df = get_dfm()
assert df.size == 0 

# This should populate the database
import_csv("../data/ind09/")
df = get_dfm()
# this assert fails. get_dfm() still retruns empty dataframe
assert df.size > 0

#However if I restart the console, the follwoing will return populated dataframe 
# from save import get_dfm
# get_dfm()

# Somehow inside one session, sqlite does not update. 
# Note: we have conn.commit() and conn.close() after each call. 

# Expected result: assert on line 16 (df.size > 0) must pass.