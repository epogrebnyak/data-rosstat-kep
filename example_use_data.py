# -*- coding: utf-8 -*-
### Получение данных

from kep import get_ts, get_df, get_varnames, get_all_dfs 

# query by variable name(s) 
z = get_ts('SOC_WAGE_rub','a', 2014)
assert z.loc[2014] == 32495

e = get_df(['SOC_WAGE_rub', 'CPI_rog'], 'm', '2015-06', '2015-06')

# complete database:
annual_varnames = get_varnames("a")
qtr_varnames    = get_varnames("q")
month_varnames  = get_varnames("m")
all_varnames    = get_varnames()

dfa = get_df(annual_varnames, "a")
dfq = get_df(qtr_varnames, "q")
dfm = get_df(month_varnames, "m")

# TODO: maybe:
# import ...
# dfa = get_dfa()
# dfq = get_dfq()
# dfm = get_dfm()

# or simply: 
dfa, dfq, dfm = get_all_dfs()