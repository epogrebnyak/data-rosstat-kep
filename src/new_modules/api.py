# -*- coding: utf-8 -*-

import database, query

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

dfa, dfq, dfm = database.read_dfs()

def get_rows_by_date_range(freq, start_date, end_date=None):
    if freq == 'a':
        df = dfa
        if isinstance(start_date, str):
            start_date = int(start_date)
        indexer = df.year >= start_date
        if end_date is not None:
            if isinstance(end_date, str):
                end_date = int(end_date)
            indexer &= df.year <= end_date
    elif freq == 'q':
        df = dfq
        start_year, start_qtr = map(int, start_date.split('-'))
        indexer = (df.year > start_year) | ((df.year == start_year) & (df.qtr >= start_qtr))
        if end_date is not None:
            end_year, end_qtr = map(int, end_date.split('-'))
            indexer &= (df.year < end_year) | ((df.year == end_year) & (df.qtr <= end_qtr))
    elif freq == 'm':
        df = dfm
        start_year, start_month = map(int, start_date.split('-'))
        indexer = (df.year > start_year) | ((df.year == start_year) & (df.month >= start_month))
        if end_date is not None:
            end_year, end_month = map(int, end_date.split('-'))
            indexer &= (df.year < end_year) | ((df.year == end_year) & (df.month <= end_month))
    else:
        raise ValueError("Unrecognized frequency: %s" % freq)
    return df[indexer]

def get_time_series(label, freq, start_date, end_date=None):
    df = get_rows_by_date_range(freq, start_date, end_date)
    return df[df.label == label]['val']

def get_dataframe(labels, freq, start_date, end_date=None):
    df = get_rows_by_date_range(freq, start_date, end_date)
    filtered = df[df.label.isin(labels)]
    if freq == 'a':
        return query.reshape_a(filtered)
    elif freq == 'q':
        return query.reshape_q(filtered)
    else:
        return query.reshape_m(filtered)

a = get_time_series("I_yoy", "a", 2000)
b = get_time_series("I_yoy", "q", "2000-1", "2015-2")
c = get_time_series("I_yoy", "m", "2000-07", "2015-01")
d = get_dataframe(["I_yoy", ], "m", "2000-07", "2015-01")

#print(a)
#print(b)
#print(c)
#print(d)

# EP: непонято, что this? то что снизу, или то что сверху?
# TODO: clarify exactly how this should look

from query import get_var_list

vars = get_var_list()
all_monthly_df = get_dataframe(vars, "m", "1999-01")

fig, axes = plt.subplots(nrows=3, ncols=3)

# Does not necessarily have to be of length 9
col_sets = [
    ['Uslugi_bln_rub', 'Uslugi_yoy'],
    ['USLUGI_bln_rub', 'USLUGI_yoy'],
    ['I_bln_rub', 'RETAIL_SALES_bln_rub'],
    ['IND_PROD_yoy', 'I_yoy', 'RETAIL_SALES_yoy'],
    ['TRANS_RAILLOAD_mln_t', 'TRANS_RAILLOAD_yoy'],
    ['WAGE_rub'],
    ['RUR_EUR_eop', 'RUR_USD_eop'],
    ['WAGE_yoy'],
    ['CPI_rog', 'PROD_E_TWh']
]

coords = [(i, j) for i in range(3) for j in range(3)]

for (i, j), cols in zip(coords, col_sets):
    all_monthly_df[cols].plot(ax=axes[i][j])
    axes[i][j].set_xlabel('')

plt.show()

# нужно подумать над способом рисовать многочисленную группу графиков all_monthly_df 
# например по 2*3 = 6 штук на страницу в окно, а потом нескоько страниц скливать в pdf или html
# идея в том, чтобы примерно видеть наполнение базы данных + затем группировать показатели по разделам
# можно сначала что-то корявое типа all_monthly_df.plot() но там из-за большого количества графиков не будет видно подписей
