"""Import csv files from web and convert to dataframes"""

import pandas as pd

def add_index(dfq, dfm):
    # set time index
    dfq.index = pd.to_datetime(dfq.time_index)    
    dfm.index = pd.to_datetime(dfm.time_index)
    return dfq, dfm
    
URL_DIR = "https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/"
DFA_URL = URL_DIR  + "data_annual.txt"
DFQ_URL = URL_DIR  + "data_quarter.txt"
DFM_URL = URL_DIR  + "data_monthly.txt"

dfa = pd.read_csv(DFA_URL, index_col = 0)
dfq = pd.read_csv(DFQ_URL)
dfm = pd.read_csv(DFM_URL)
# set time index
dfq, dfm = add_index(dfq, dfm)

