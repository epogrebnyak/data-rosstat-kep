# -*- coding: utf-8 -*-
import pandas as pd
import sqlite3

from datetime import date
from dateutil.relativedelta import relativedelta

def get_end_of_monthdate(y,m):
   return date(year=y, month=m, day=1) + relativedelta(months=+1) + relativedelta(days = -1)

def get_end_of_quarterdate(y,q):
   return date(y,1,1) + relativedelta (months = q*3) + relativedelta (days = -1)
    
    

# Read sqlite query results into  pandas DataFrames

def read_dfs(file = "kep.sqlite"):
    con = sqlite3.connect(file)
    dfa = pd.read_sql_query("SELECT * from annual", con)
    dfq = pd.read_sql_query("SELECT * from quarterly", con)
    dfm = pd.read_sql_query("SELECT * from monthly", con)
    con.close()
    return dfa, dfq, dfm
    
dfa, dfq, dfm = read_dfs()
dfa = dfa.pivot(columns='label', values = 'val', index = 'year')


dt = [get_end_of_quarterdate(y,q) for y, q in zip(dfq["year"], dfq["qtr"])]
dfq["time_index"] = pd.DatetimeIndex(dt, freq = "Q")
dfq = dfq.pivot(columns='label', values = 'val', index = 'time_index')
dfq.insert(0, "year", dfq.index.year)
dfq.insert(1, "qtr", dfq.index.quarter)

dt = [get_end_of_monthdate(y,m) for y, m in zip(dfm["year"], dfm["month"])]
dfm["time_index"] = pd.DatetimeIndex(dt, freq = "M")
dfm = dfm.pivot(columns='label', values = 'val', index = 'time_index')
dfm.insert(0, "year", dfm.index.year)
dfm.insert(1, "month", dfm.index.month)

with pd.ExcelWriter("kep.xls") as writer:
    dfa.to_excel(writer, sheet_name='year')
    dfq.to_excel(writer, sheet_name='quarter')
    dfm.to_excel(writer, sheet_name='month')   
    
#TODO:
# may change formatting of the columns http://xlsxwriter.readthedocs.org/en/latest/example_pandas_column_formats.html#ex-pandas-column-formats
# http://stackoverflow.com/questions/17069694/writing-xlwt-dates-with-excel-date-format
# http://stackoverflow.com/questions/9920935/easily-write-formatted-excel-from-python-start-with-excel-formatted-use-it-in
# do not write second row - inherited from pivot.   
    