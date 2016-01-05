# -*- coding: utf-8 -*-
"""Примеры получения данных в виде временных рядов. Используются функции:
   - get_ts, get_df, 
   - get_dfa, get_dfq, get_dfm."""

from kep import get_ts, get_df
from kep import get_dfa, get_dfq, get_dfm
from kep import update_db

# refresh db
update_db()

# query by variable name - obtain pandas time series
ts1 = get_ts('SOC_WAGE_rub','a', 1999)
assert ts1.loc[2014] == 32495

ts2 = get_ts('CPI_rog','a', 1999)
assert ts2.loc[2014] == 111.4

# query by variable names - obtain pandas dataframe
df1 = get_df(['SOC_WAGE_rub', 'CPI_rog'], 'm', '2010-01', '2015-10')
assert df1.loc['2015-10-31','SOC_WAGE_rub'] == 33357.0 # note: data revision, was 33240.0
assert df1.loc['2015-10-31','CPI_rog'] ==  100.7

# get all dataframes at annual, qtr and monthly frequencies
dfa = get_dfa()
dfq = get_dfq()
dfm = get_dfm()

   
