# -*- coding: utf-8 -*-
""" Functions to slices of full monthly, quarterly and annual dataframes (dfm, dfa, dfq). 
    These are end-user API functions."""

from save import get_reshaped_dfs
from var_names import get_var_list
from datetime import date

# NOTE: may execute get_reshaped_dfs once.

# ----------------------------------------------------------------------
# End-use wrappers for _get_ts_or_df 
# NOTE: must also make start_date optional

def get_TimeSeries(label, freq, start_date, end_date=None):
    return _get_ts_or_df(label, freq, start_date, end_date)

def get_DataFrame(labels, freq, start_date, end_date=None):
    return _get_ts_or_df(label, freq, start_date, end_date)
    
def get_ts(label, freq, start_date, end_date=None):
    return _get_ts_or_df(label, freq, start_date, end_date)

def get_df(labels, freq, start_date, end_date=None):
    return _get_ts_or_df(label, freq, start_date, end_date)

def get_dfm():
    var_names = get_var_list()
    return get_DataFrame(var_names, "m", "1999-01")

# ----------------------------------------------------------------------

def _get_ts_or_df(label, freq, start_date, end_date=None):
   df = slice_source_df_by_date_range(freq, start_date, end_date)
   return df[label]

# ----------------------------------------------------------------------

def date_to_tuple(input_date):
    if isinstance(input_date, int):
        return (input_date, 1)
    elif "-" in input_date:
        return tuple(map(int, input_date.split('-')))
    else:
        return (int(input_date), 1)

def test_date_to_tuple():
  assert date_to_tuple(2000)      ==  (2000, 1)
  assert date_to_tuple("2000")    ==  (2000, 1)
  assert date_to_tuple("2000-07") ==  (2000, 7)
  assert date_to_tuple("2000-1")  ==  (2000, 1)

def slice_source_df_by_date_range(freq, start_date, end_date=None):
    """Main function to produce selections of dataframes"""
    
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

if __name__ == "__main__":
    test_date_to_tuple()
    test_get_df_and_ts()
