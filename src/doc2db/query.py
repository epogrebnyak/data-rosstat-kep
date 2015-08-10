# -*- coding: utf-8 -*-
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import shutil

try:
   from .database import read_dfs
   from .common import dump_iter_to_csv
except SystemError:
   from database import read_dfs 
   from common import dump_iter_to_csv


XLFILE = "kep.xls"

def get_end_of_monthdate(y,m):
   return date(year=y, month=m, day=1) + relativedelta(months=+1) + relativedelta(days = -1)

def get_end_of_quarterdate(y,q):
   return date(y,1,1) + relativedelta (months = q*3) + relativedelta (days = -1)
    
def duplicate_labels(df):
    r = df[df.duplicated(['label','year']) == True]
    return r['label'].unique()

def check_for_dups(df): 
    dups = duplicate_labels(df)
    if len(dups) > 0:
        raise Exception("Duplicate labels: " + " ".join(dups))

def reshape_all(dfa, dfq, dfm):
    return reshape_a(dfa), reshape_q(dfq), reshape_m(dfm)
    
def reshape_a(dfa):
    return dfa.pivot(columns='label', values = 'val', index = 'year')
    
def reshape_q(dfq):
    dt = [get_end_of_quarterdate(y,q) for y, q in zip(dfq["year"], dfq["qtr"])]
    dfq["time_index"] = pd.DatetimeIndex(dt, freq = "Q")
    dfq = dfq.pivot(columns='label', values = 'val', index = 'time_index')
    dfq.insert(0, "year", dfq.index.year)
    dfq.insert(1, "qtr", dfq.index.quarter)
    return dfq

def reshape_m(dfm):
    dt = [get_end_of_monthdate(y,m) for y, m in zip(dfm["year"], dfm["month"])]
    dfm["time_index"] = pd.DatetimeIndex(dt, freq = "M")
    dfm = dfm.pivot(columns='label', values = 'val', index = 'time_index')
    print("\nMonthly vars:")
    print(dfm.columns.values)
    dfm.insert(0, "year", dfm.index.year)
    dfm.insert(1, "month", dfm.index.month)
    return dfm

def write_to_xl(dfa, dfq, dfm):
    with pd.ExcelWriter(XLFILE) as writer:
        dfa.to_excel(writer, sheet_name='year')
        dfq.to_excel(writer, sheet_name='quarter')
        dfm.to_excel(writer, sheet_name='month')   
    shutil.copy(XLFILE, "..")


def get_additional_header(df):
    # TODO 1: make a query on spec dictionary
    return ["date"] + df.columns.values.tolist()
    
def get_csvrows(df):
    strings = df.to_csv(sep = "\t", decimal = ",")
    # note: below will not be needed in pandas 0.16
    #       undesired - will change . for , in headers too
    # TODO 2: get headers and datablock separately      
    strings = strings.replace(".", ",")
    return [x.split("\t") for x in strings.split("\n")]

def df_csv_iter(df):
    # TODO 3 restore original order of items as in spec dictionary + rebase df
    # TODO 4 this has to be stored in database, something with autoincrement
    yield get_additional_header(df) 
    for row in get_csvrows(df):
        yield row
        
def to_csv(df, filename):
    dump_iter_to_csv(df_csv_iter(df), filename)

def write_to_csv(dfa, dfq, dfm):
    to_csv(dfa, "annual.txt")
    to_csv(dfq, "qtr.txt")
    to_csv(dfm, "month.txt")   
    # TODO 5 - Also write this to Excel xls/xlsx too  as sheets
    # TODO 6 - Write a sheet with varnames
    # TODO 7 - Check its complete
    
def db2xl():
    dfa, dfq, dfm = read_dfs()
    check_for_dups(dfa)
    dfa = reshape_a(dfa)
    dfq = reshape_q(dfq)
    dfm = reshape_m(dfm)
    write_to_xl(dfa, dfq, dfm)
    write_to_csv(dfa, dfq, dfm)

if __name__ == "__main__":
    dfa, dfq, dfm = read_dfs()
    check_for_dups(dfa)
    dfa, dfq, dfm = reshape_all(dfa, dfq, dfm)
    write_to_xl(dfa, dfq, dfm)
    for y in df_csv_iter(dfa):
        print(y)
    
# note- order on columns i lost, a-betic

 
#TODO:
# may change formatting of the columns http://xlsxwriter.readthedocs.org/en/latest/example_pandas_column_formats.html#ex-pandas-column-formats
# http://stackoverflow.com/questions/17069694/writing-xlwt-dates-with-excel-date-format
# http://stackoverflow.com/questions/9920935/easily-write-formatted-excel-from-python-start-with-excel-formatted-use-it-in
# do not write second row - inherited from pivot.   
    