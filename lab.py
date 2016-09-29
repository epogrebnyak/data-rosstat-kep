# -*- coding: utf-8 -*-
# 9:58 29.09.2016	10:28 29.09.2016

import pandas as pd

#
# 1. Страница 4 рисунка
# =====================
#
# Нарисовать 4 графика на страницу, в каждом по одному временному ряду. 
#
#

#p = Page(["GDP", "CPI", "PPI", ""], header="", freq="m", start=None, end=None)


#
# 2. Один риснок
# ==============
#
# Нарисовать рисунок с одним временным рядом. 
#
# May use plotting archives
# https://github.com/epogrebnyak/plotting
# https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/getter/plots.py
#

# ts = Indicator("CPI", freq="m", start=None, end=None, add_sa=False)
# ts.save_graph()

DFA_PATH = "data_annual.txt"
DFQ_PATH = "data_quarter.txt"
DFM_PATH = "data_monthly.txt"

DEFAULT_FREQUENCY = "m"
VALID_FREQUENCIES = "aqm"

dfa = pd.read_csv(DFA_PATH, index_col = 0)
dfq = pd.read_csv(DFQ_PATH, converters = {'time_index':pd.to_datetime}, index_col = 'time_index')
dfm = pd.read_csv(DFM_PATH, converters = {'time_index':pd.to_datetime}, index_col = 'time_index')
DATAFRAMES = {'a': dfa, 'q': dfq, 'm': dfm}

class Indicator():

    def set_frequency(self, freq):    
        freq = freq.lower()
        if freq not in VALID_FREQUENCIES :
            raise Exeption("Invalid frequency: " + freq + "\Accepted: " + ", ".join(VALID_FREQUENCIES))        
        return DATAFRAMES[freq]    
        
    def filter_labels(self, labels):
        # convert to list if one label is given
        if isinstance(labels, str):
            labels = [labels]
        # filter labels            
        return [x for x in labels if x in self.dataframe.columns]        
    
    def __init__(self, label_values, freq=DEFAULT_FREQUENCY, start=None, end=None):
        self.dataframe = self.set_frequency(freq)        
        self.labels = self.filter_labels(label_values)
        self.df = self.dataframe.loc[start:end,self.labels] 
        self.basename = "@".join(self.labels) 
        
    def to_png(self):
        filename = self.basename + ".png"
        ax = self.df.plot()
        fig = ax.get_figure()
        fig.savefig(filename)                              
        
    def to_excel(self):
        filename = self.basename + ".xls"
        self.df.to_excel(filename)

cpi = Indicator(["CPI_rog", "CPI_NONFOOD_rog"], start='2005-01')
print(cpi.df)
cpi.to_png()
cpi.to_excel()

    