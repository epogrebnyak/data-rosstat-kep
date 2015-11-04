# -*- coding: utf-8 -*-
"""
Created on Wed Nov  4 18:13:48 2015

@author: EP
"""

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
# даты "2000-07" должны преобразовываться в (2000, 7) и дальше использоваться для запроса

