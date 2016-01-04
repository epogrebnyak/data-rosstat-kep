# -*- coding: utf-8 -*-
"""Примеры получения данных в виде временных рядов. Используются функции get_ts, get_df, 
   get_dfa, get_dfq, get_dfm, get_varnames."""

# TODO 1:
#        suggest laconic update of the database with current month here

# TODO 2:
# Issue: get_ts, get_df calls not protected if variable is not in dataset
#        if variable not in database must print a friendly message + list of variables available ", ".join(get_varnames()
#        + suggestion to import/update database with code example as in TODO 1.

# NOT TODO: can list of variables in todo be in several colums? same as Windows 'dir /D'

# TODO 3: need  wrappers to read csv files from URL + same in R.

from kep import get_ts, get_df
from kep import get_dfa, get_dfq, get_dfm #, get_all_dfs 
from kep import get_varnames 

# query by variable name - obtain pandas time series
ts1 = get_ts('SOC_WAGE_rub','a', 1999)
assert ts1.loc[2014] == 32495

ts2 = get_ts('CPI_rog','a', 1999)
assert ts2.loc[2014] == 111.4

# query by variable names - obtain pandas dataframe
df1 = get_df(['SOC_WAGE_rub', 'CPI_rog'], 'm', '2010-01', '2015-10')
assert df1.loc['2015-10-31','SOC_WAGE_rub'] = 33240.0
assert df1.loc['2015-10-31','CPI_rog'] =  100.7

# get all dataframes
dfa = get_dfa()
dfq = get_dfq()
dfm = get_dfm()

print("All available varnames: ", ", ".join(get_varnames())) 
