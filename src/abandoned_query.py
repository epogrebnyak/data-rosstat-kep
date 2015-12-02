# -*- coding: utf-8 -*-
import pandas as pd
from datetime import date, datetime
from calendar import monthrange
import shutil

try:
   from .database import read_dfs
   from .common import dump_iter_to_csv
   from .var_names import get_var_list_as_dataframe
except (ImportError, SystemError):
   from database import read_dfs 
   from common import dump_iter_to_csv
   from var_names import get_var_list_as_dataframe

XLSX_FILE     = "output//kep.xlsx"
XLS_FILE      = "output//kep.xls"
ANNUAL_CSV    = "output//data_annual.txt"	
QUARTERLY_CSV = "output//data_qtr.txt"
MONTHLY_CSV   = "output//data_monthly.txt"

#--------------------------------------------------------------------------
def get_end_of_monthdate(y, m):
    return datetime(year=y, month=m, day=monthrange(y, m)[1])

def get_end_of_quarterdate(y, q):
    return datetime(year=y, month=q*3, day=monthrange(y, q*3)[1])
    
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
    if not dfa.empty:     
        return dfa.pivot(columns='label', values='val', index='year')
    else:
        return pd.DataFrame()
    
def reshape_q(dfq):
    if not dfq.empty:     
        dt = [get_end_of_quarterdate(y,q) for y, q in zip(dfq["year"], dfq["qtr"])]
        dfq["time_index"] = pd.DatetimeIndex(dt, freq = "Q")
        dfq = dfq.pivot(columns='label', values='val', index='time_index')
        dfq.insert(0, "year", dfq.index.year)
        dfq.insert(1, "qtr", dfq.index.quarter)
        return dfq
    else:
        return pd.DataFrame()

def reshape_m(dfm):
    if not dfm.empty:     
        dt = [get_end_of_monthdate(y,m) for y, m in zip(dfm["year"], dfm["month"])]
        dfm["time_index"] = pd.DatetimeIndex(dt, freq = "M")
        dfm = dfm.pivot(columns='label', values = 'val', index = 'time_index')
        dfm.insert(0, "year", dfm.index.year)
        dfm.insert(1, "month", dfm.index.month)
        return dfm
    else: 
        return pd.DataFrame()

#------------------------------------------------------------------------------
# Functions to slice dfm, dfa, dfq
# These are end-user API functions

def date_to_tuple(input_date):
    if isinstance(input_date, int):
        return (input_date, 1)
    elif "-" in input_date:
        return tuple(map(int, input_date.split('-')))
    else:
        return (int(input_date), 1)

assert date_to_tuple(2000)      ==  (2000, 1)
assert date_to_tuple("2000")    ==  (2000, 1)
assert date_to_tuple("2000-07") ==  (2000, 7)
assert date_to_tuple("2000-1")  ==  (2000, 1)

def slice_source_df_by_date_range(freq, start_date, end_date=None):

    dfa, dfq, dfm = get_reshaped_dfs()
    start_year, start_period = date_to_tuple(start_date)
    
    # define end date
    if end_date is not None:
        end_year, end_period = date_to_tuple(start_date)
    else:
        end_year = date.today().year + 1
        end_period = 1
        
    # select which dataframe to use and define indexer
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

def _get_ts_or_df(label, freq, start_date, end_date=None):
   df = slice_source_df_by_date_range(freq, start_date, end_date)
   return df[label]
   
# ----------------------------------------------------------------------
# wrappers for _get_ts_or_df 
# NOTE: must also make start_date optional

def get_TimeSeries(label, freq, start_date, end_date=None):
    return _get_ts_or_df(label, freq, start_date, end_date)

def get_DataFrame(labels, freq, start_date, end_date=None):
    return _get_ts_or_df(label, freq, start_date, end_date)
    
def get_ts(label, freq, start_date, end_date=None):
    return _get_ts_or_df(label, freq, start_date, end_date)

def get_df(labels, freq, start_date, end_date=None):
    return _get_ts_or_df(label, freq, start_date, end_date)

# ----------------------------------------------------------------------
    
def get_dfm():
    var_names = get_var_list()
    return get_DataFrame(var_names, "m", "1999-01")

# ----------------------------------------------------------------------

def test_get_df_and_ts():
    z = get_ts('WAGE_rub','a', 2014)
    assert isinstance(z, pd.core.series.Series)
    assert z.iloc[0] == 32495

    e = get_df(['WAGE_rub', 'CPI_rog'], 'm', '2015-06', '2015-06')
    assert isinstance(e, pd.DataFrame)
    # WARNING: this is data revision - in ind06 this was 
    # assert e.iloc[0,0] == 35930.0
    # now in ind09 it is:
    assert e.iloc[0,0] == 35395
    assert e.iloc[0,1] == 100.2

#-----------------------------------------------------------------------------------

def get_var_list():
    dfa, dfq, dfm = read_dfs()
    dfa = reshape_a(dfa)
    return dfa.columns.values.tolist()  
    
#-----------------------------------------------------------------------------------
# Excel output

def write_to_xl(dfa, dfq, dfm):
   # Not run/not tested. For issue #28
   df_var_names = get_var_list_as_dataframe()
   for file in [XLSX_FILE, XLS_FILE]:
      _write_to_xl(dfa, dfq, dfm, df_var_names, file)

def _write_to_xl(dfa, dfq, dfm, df_var_names, file):
    with pd.ExcelWriter(file) as writer:
        dfa.to_excel(writer, sheet_name='year')
        dfq.to_excel(writer, sheet_name='quarter')
        dfm.to_excel(writer, sheet_name='month')
        df_var_names.to_excel(writer, sheet_name='variables')
    # copy file to root directory     
    shutil.copy(file, "..")

# ---------------------------------------------------------------------------------
# CSV output

# ---------------------------------------------------------------------------------
# Legacy code, for deletion

def get_additional_header(df):
    return ["date"] + df.columns.values.tolist()
    
def get_csvrows(df):
    strings = df.to_csv(sep = "\t", decimal = ",", header = False)
    # note: below will not be needed in pandas 0.16
    #       undesired - will change . for , in headers too
    strings = strings.replace(".", ",")
    return [x.split("\t") for x in strings.split("\n")]

def df_csv_iter(df):
    # MUST ADD: restore original order of items as in spec dictionary + rebase df
    yield get_additional_header(df) 
    for row in get_csvrows(df):
        yield row
        
# End of deletion 
# ---------------------------------------------------------------------------------


def to_csv(df, filename):
   # Previous version: 
   # dump_iter_to_csv(df_csv_iter(df), filename)

   # We simplify it with following:
   df.to_csv(filename)
   # Reference call:
   # DataFrame.to_csv(path_or_buf=None, sep=', ', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, mode='w', encoding=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True, escapechar=None, decimal='.', **kwds)

def write_to_csv(dfa, dfq, dfm):
    to_csv(dfa, ANNUAL_CSV)
    to_csv(dfq, QUARTERLY_CSV)
    to_csv(dfm, MONTHLY_CSV)   

def get_reshaped_dfs():
    dfa, dfq, dfm = read_dfs()
    check_for_dups(dfa)
    dfa = reshape_a(dfa)
    dfq = reshape_q(dfq)
    dfm = reshape_m(dfm)
    return dfa, dfq, dfm

def db_dump():
    dfa, dfq, dfm = get_reshaped_dfs()
    write_to_xl(dfa, dfq, dfm)
    write_to_csv(dfa, dfq, dfm)

if __name__ == "__main__":
    dfa, dfq, dfm = read_dfs()
    check_for_dups(dfa)
    dfa, dfq, dfm = reshape_all(dfa, dfq, dfm)
    write_to_xl(dfa, dfq, dfm)

    #test_get_df_and_ts()
    
# NOTE: file contains both output functions dump_db() and query functions get_ts(), get_df()
#       also in this file: 
#       - get_dfm()
#       - from var_names import get_var_list_as_dataframe may be a circular reference with var_names.py as it uses get_var_list()
