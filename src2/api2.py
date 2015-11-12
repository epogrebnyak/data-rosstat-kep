# -*- coding: utf-8 -*-

import datetime
import query
import pandas as pd


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

    dfa, dfq, dfm = query.get_reshaped_dfs()
    
    start_year, start_period = date_to_tuple(start_date)

    if end_date is not None:
        end_year, end_period = date_to_tuple(start_date)
    else:
        end_year = datetime.date.today().year + 1
        end_period = 1
    
    if freq == 'a':
        df = dfa
        indexer = (df.index >= start_year) & (df.index <= end_year)
    elif freq == 'q':
        df = dfq
        d1 = query.get_end_of_quarterdate(start_year, start_period)
        d2 = query.get_end_of_quarterdate(end_year, end_period)
        indexer = (df.index >= d1) & (df.index <= d2)
    elif freq == 'm':
        df = dfm
        d1 = query.get_end_of_monthdate(start_year, start_period)
        d2 = query.get_end_of_monthdate(end_year, end_period)
        indexer = (df.index >= d1) & (df.index <= d2)
    else:
        raise ValueError("Frequency must be 'a', 'q' or 'm'. Provided: %s" % freq)
        
    return df[indexer]

def get_dfm():
    from query import get_var_list
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

# NOTE: api2.py to be merged with query.py

if __name__ == "__main__":
    test_get_df_and_ts()
