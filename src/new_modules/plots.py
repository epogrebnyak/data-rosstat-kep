# -*- coding: utf-8 -*-
"""
"""

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

from query import get_var_list
from api2 import get_dataframe

vars_ = get_var_list()
all_monthly_df = get_dataframe(vars_, "m", "1999-01")

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


# todo-plot-7:49 06.11.2015:

# у нас из tab.csv в итоге будет считываться очень много (несколько деястков) переменных

# задача рисунков сейчас - вывести все эти переменные на экран
# комбинации по два рисунка на график будут очень полезны, но не сейчас

# требуется:
# - на одном рисунке один график + название переменной только в заголовке сверху
# - задавать размещение графиков на страницу M*N - 3 на 2 например
# - постранично вывести все граифики из get_var_list() 
# - каждое окно с таким граифом сохранить в графический файл (например .png)
# - объединить эти рисунки в pdf или html файл
# - можно сразу сливать рисунки в один PDF - http://matplotlib.org/api/backend_pdf_api.html#matplotlib.backends.backend_pdf.PdfPages

# цель этой задачи - иметь выдачу, на которой нарисованы все имеющиеся 
# на этот момент в базе данных графики

# - таких выдач должно быть в итоге три - месячная, квартальая, годовая.

# end - todo-plot-7:49 06.11.2015:
 







