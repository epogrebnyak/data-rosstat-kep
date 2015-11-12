# -*- coding: utf-8 -*-
import pandas as pd
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import shutil

try:
   from .database import read_dfs
   from .common import dump_iter_to_csv
except (ImportError, SystemError):
   from database import read_dfs 
   from common import dump_iter_to_csv

XLFILE = "output//kep.xlsx"
ANNUAL_CSV = "output//data_annual.txt"	
QUARTERLY_CSV = "output//data_qtr.txt"
MONTHLY_CSV = "output//data_monthly.txt"

def get_end_of_monthdate(y,m):
   return datetime(year=y, month=m, day=1) + relativedelta(months=+1) + relativedelta(days = -1)

def get_end_of_quarterdate(y,q):
   return datetime(y,1,1) + relativedelta (months = q*3) + relativedelta (days = -1)
    
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
    return dfa.pivot(columns='label', values='val', index='year')
    
def reshape_q(dfq):
    dt = [get_end_of_quarterdate(y,q) for y, q in zip(dfq["year"], dfq["qtr"])]
    dfq["time_index"] = pd.DatetimeIndex(dt, freq = "Q")
    dfq = dfq.pivot(columns='label', values='val', index='time_index')
    dfq.insert(0, "year", dfq.index.year)
    dfq.insert(1, "qtr", dfq.index.quarter)
    return dfq

def reshape_m(dfm):
    dt = [get_end_of_monthdate(y,m) for y, m in zip(dfm["year"], dfm["month"])]
    dfm["time_index"] = pd.DatetimeIndex(dt, freq = "M")
    dfm = dfm.pivot(columns='label', values = 'val', index = 'time_index')
    #print("\nMonthly vars:")
    #print(dfm.columns.values)
    dfm.insert(0, "year", dfm.index.year)
    dfm.insert(1, "month", dfm.index.month)
    return dfm

def write_to_xl(dfa, dfq, dfm):
    with pd.ExcelWriter(XLFILE) as writer:
        dfa.to_excel(writer, sheet_name='year')
        dfq.to_excel(writer, sheet_name='quarter')
        dfm.to_excel(writer, sheet_name='month')   
    shutil.copy(XLFILE, "..")

def get_var_list():
    dfa, dfq, dfm = read_dfs()
    dfa = reshape_a(dfa)
    return dfa.columns.values.tolist()    

def get_additional_header(df):
    # TODO 1: make a query on spec dictionary
    return ["date"] + df.columns.values.tolist()
    
def get_csvrows(df):
    strings = df.to_csv(sep = "\t", decimal = ",", header = False)
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
    to_csv(dfa, ANNUAL_CSV)
    to_csv(dfq, QUARTERLY_CSV)
    to_csv(dfm, MONTHLY_CSV)   
    # TODO 5 - Also write this to Excel xls/xlsx too  as sheets
    # TODO 6 - Write a sheet with varnames
    # TODO 7 - Check its complete
    
def get_reshaped_dfs():
    # todo later: maybe use *unpacking
    dfa, dfq, dfm = read_dfs()
    check_for_dups(dfa)
    dfa = reshape_a(dfa)
    dfq = reshape_q(dfq)
    dfm = reshape_m(dfm)
    return dfa, dfq, dfm

def db_dump():
    dfa, dfq, dfm = read_dfs()
    check_for_dups(dfa)
    dfa = reshape_a(dfa)
    dfq = reshape_q(dfq)
    dfm = reshape_m(dfm)
    # write_to_xl(dfa, dfq, dfm)
    write_to_csv(dfa, dfq, dfm)

def date_to_tuple(input_date):
    if isinstance(input_date, int):
        return (input_date, 1)
    elif "-" in input_date:
        return tuple(map(int, input_date.split('-')))
    else:
        return (int(input_date), 1)

def slice_source_df_by_date_range(freq, start_date, end_date=None):

    dfa, dfq, dfm = get_reshaped_dfs()

    start_year, start_period = date_to_tuple(start_date)

    if end_date is not None:
        end_year, end_period = date_to_tuple(start_date)
    else:
        end_year = date.today().year + 1
        end_period = 1

    if freq == 'a':
        df = dfa
        indexer = (df.index >= start_year) & (df.index <= end_year)
    elif freq == 'q':
        df = dfq
        d1 = get_end_of_quarterdate(start_year, start_period)
        d2 = get_end_of_quarterdate(end_year, end_period)
        indexer = (df.index >= d1) & (df.index <= d2)
    elif freq == 'm':
        df = dfm
        d1 = get_end_of_monthdate(start_year, start_period)
        d2 = get_end_of_monthdate(end_year, end_period)
        indexer = (df.index >= d1) & (df.index <= d2)
    else:
        raise ValueError("Frequency must be 'a', 'q' or 'm'. Provided: %s" % freq)

    return df[indexer]

def get_dfm():
    var_names = get_var_list()
    return get_time_series(var_names, "m", "1999-01")

def get_time_series(label, freq, start_date, end_date=None):
    df = slice_source_df_by_date_range(freq, start_date, end_date)
    return df[label]

def get_dataframe(labels, freq, start_date, end_date=None):
    df = slice_source_df_by_date_range(freq, start_date, end_date)
    return df[labels]

def test_get_df_and_ts():
    z = get_time_series('WAGE_rub','a', 2014)
    assert isinstance(z, pd.core.series.Series)
    assert z.iloc[0] == 32495

    e = get_dataframe(['WAGE_rub', 'CPI_rog'], 'm', '2015-06', '2015-06')
    assert isinstance(e, pd.DataFrame)
    assert e.iloc[0,0] == 35930.0
    assert e.iloc[0,1] == 100.2

if __name__ == "__main__":
    dfa, dfq, dfm = read_dfs()
    check_for_dups(dfa)
    dfa, dfq, dfm = reshape_all(dfa, dfq, dfm)
    write_to_xl(dfa, dfq, dfm)
    for y in df_csv_iter(dfa):
        print(y)

    assert date_to_tuple(2000)      ==  (2000, 1)
    assert date_to_tuple("2000")    ==  (2000, 1)
    assert date_to_tuple("2000-07") ==  (2000, 7)
    assert date_to_tuple("2000-1")  ==  (2000, 1)

    test_get_df_and_ts()
    
# note- order on columns i lost, a-betic

 
#TODO:
# may change formatting of the columns http://xlsxwriter.readthedocs.org/en/latest/example_pandas_column_formats.html#ex-pandas-column-formats
# http://stackoverflow.com/questions/17069694/writing-xlwt-dates-with-excel-date-format
# http://stackoverflow.com/questions/9920935/easily-write-formatted-excel-from-python-start-with-excel-formatted-use-it-in
# do not write second row - inherited from pivot.   
