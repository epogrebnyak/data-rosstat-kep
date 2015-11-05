# -*- coding: utf-8 -*-
"""
"""
#------------- todo api-1 - написать get_time_series() + get_datafame()

def get_time_series(label, freq, start_date, end_date = None):
    pass

def get_datafame(labels, freq, start_date, end_date = None):
    pass

# пример вызова
get_time_series("I_yoy", "a", 2000)
get_time_series("I_yoy", "m", "2000-07", "2015-01")
get_time_series("I_yoy", "q", "2000-1", "2015-2")
get_dataframe(["I_yoy", ], "m", "2000-07", "2015-01")

# если end_date не задан - берется до самых свежих данных
# даты типа "2000-07" должны преобразовываться в (2000, 7) и дальше использоваться для запроса
# за основу можно взять код в query.py, но можно и что-то новое, он там не очень нравится

#------------- todo api-2 - отрисовывать all_monthly_df 
from query import get_var_list

vars = get_var_list()
all_monthly_df = get_datafame(vars, "m", "1999-01") 

# нужно подумать над способом рисовать многочисленную группу графиков all_monthly_df 
# например по 2*3 = 6 штук на страницу в окно, а потом нескоько страниц скливать в pdf или html
# идея в том, чтобы примерно видеть наполнение базы данных + затем группировать показатели по разделам
# мжно сначала что-то корявое типа all_monthly_df.plot() но там из-за большлго количества графиков не будет видно подписей 
 

