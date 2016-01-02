# -*- coding: utf-8 -*-
### Получение данных

from kep import get_ts, get_df
from kep import get_dfa, get_dfq, get_dfm, get_all_dfs 
from kep import get_varnames 

# query by variable name - obtain pandas time series
ts1 = get_ts('SOC_WAGE_rub','a', 1999)
assert ts1.loc[2014] == 32495

# query by variable names - obtain pandas dataframe
df1 = get_df(['SOC_WAGE_rub', 'CPI_rog'], 'm', '2010-01', '2015-10')
# TODO: assert

# get all 
dfa = get_dfa()
dfq = get_dfq()
dfm = get_dfm()

# or simply: 
dfa, dfq, dfm = get_all_dfs()