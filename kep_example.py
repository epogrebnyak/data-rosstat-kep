### Получение данных

# query by variable name(s) 
z = kep.get_ts('SOC_WAGE_rub','a', 2014)
#assert isinstance(z, pd.core.series.Series)
#assert z.iloc[0] == 32495

e = get_df(['SOC_WAGE_rub', 'CPI_rog'], 'm', '2015-06', '2015-06')

# complete database:
annual_varnames = kep.get_varnames("a")
qtr_varnames    = kep.get_varnames("q")
month_varnames  = kep.get_varnames("m")
all_varnames    = kep.get_varnames(all = True)

dfa = get_df(annual_varnames)
dfq = get_df(qtr_varnames)
dfm = get_df(month_varnames)

### Импорт в базу данных

import kep 
data_folder = "data/2015/ind10"
# TODO:
# must stop if (1) no Word installed, (2) CSV already exists 
kep.make_csv()
#
kep.import_csv()
# save data and variable list to Excel, CSV files, write plots to PDF and *.png 
kep.dump_db()
