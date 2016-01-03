# -*- coding: utf-8 -*-
### Получение данных

# TODO:
# Issue: call not protecte if the variable is not in dataset, must end with friendly message + suggestion to import database + list of variables available.
#        can wipe database to replicate this error and run this file  

from kep import get_ts, get_df
from kep import get_dfa, get_dfq, get_dfm, get_all_dfs 
from kep import get_varnames 

# query by variable name - obtain pandas time series
ts1 = get_ts('SOC_WAGE_rub','a', 1999)
assert ts1.loc[2014] == 32495

ts2 = get_ts('CPI_rog','a', 1999)
assert ts2.loc[2014] == 111.4

# query by variable names - obtain pandas dataframe
df1 = get_df(['SOC_WAGE_rub', 'CPI_rog'], 'm', '2010-01', '2015-10')
# TODO: fix error get_df must return many rows from 2010 to 2015, returns just one row.
#       must be similar to dfm[['SOC_WAGE_rub','CPI_rog']]

# get all dataframes
dfa = get_dfa()
dfq = get_dfq()
dfm = get_dfm()

# or simply: 
# dfa, dfq, dfm = get_all_dfs()