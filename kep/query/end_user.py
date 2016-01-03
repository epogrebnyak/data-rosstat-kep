# -*- coding: utf-8 -*-
""" Functions to slices of full monthly, quarterly and annual dataframes (dfm, dfa, dfq). 
    These are end-user API functions."""
from datetime import date
import pandas as pd
    
from kep.query.save import get_reshaped_dfs
from kep.database.db import get_unique_labels
# NOTE: maybe use some different data habdling
from kep.query.save import get_end_of_monthdate, get_end_of_quarterdate

# ----------------------------------------------------------------------
# End-use wrappers for _get_ts_or_df 

# TODO: need more work on errors

def get_all_dfs():
    return get_reshaped_dfs()

def get_ts(label, freq, start_date=None, end_date=None):
    df = _get_ts_or_df(label, freq, start_date, end_date)
    return df[label] 

def get_df(labels, freq, start_date=None, end_date=None):
    df = _get_ts_or_df(labels, freq, start_date, end_date)
    slicing_labels = in_index(labels, df)
    return df[slicing_labels]

# WARNING: labels may be outside df.columns
def in_index(labels, df):
   return [lab for lab in labels if lab in df.columns]   

# WARNING: hardcoded floor for date: start_date=1999
def _get_ts_or_df(label, freq, start_date, end_date):
   if start_date is None: 
       start_date = 1999
   return slice_source_df_by_date_range(freq, start_date, end_date)


# ----------------------------------------------------------------------

def date_to_tuple(input_date):
    if isinstance(input_date, int):
        return (input_date, 1)
    elif "-" in input_date:
        return tuple(map(int, input_date.split('-')))
    else:
        return (int(input_date), 1)

#>assert date_to_tuple(2000)      ==  (2000, 1)
#>True
#>assert date_to_tuple("2000")    ==  (2000, 1)
#>True
#>assert date_to_tuple("2000-07") ==  (2000, 7)
#>True
#>assert date_to_tuple("2000-1")  ==  (2000, 1)
#>True

def slice_source_df_by_date_range(freq, start_date, end_date=None):
    """Main function to produce selections of dataframes"""
    
    dfa, dfq, dfm = get_reshaped_dfs()
    start_year, start_period = date_to_tuple(start_date)
    
    # define end date
    if end_date is not None:
        end_year, end_period = date_to_tuple(end_date)
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



# NOTE: may execute get_reshaped_dfs once and store it in memory
