"""Examples to import annual, quarterly and monthly pandas dataframes:
   - from local files
   - from web
   - from 'kep' package   
   
   All examples result in annual, quarterly and monthly pandas dataframes in variables dfa, dfq, dfm respectively.
   
   Excel files are also available for download to explore data and double-check pandas/R results:
      https://github.com/epogrebnyak/rosstat-kep-data/raw/master/output/kep.xls
      https://github.com/epogrebnyak/rosstat-kep-data/raw/master/output/kep.xlsx    
   
   Excecise:
      1. obtain dfa, dfq, dfm in any or all of these methods
      2. try plotting some variables, e.g. reproduce graphs at https://github.com/epogrebnyak/rosstat-kep-data/blob/master/README.md#Основные-показатели
         also at qtr and monthly frequencies
      
      Plotting code used may be found at: 
      https://github.com/epogrebnyak/rosstat-kep-data/blob/master/kep/extract/plots.py#L130-L139
"""

import pandas as pd
import os

#
# 1. Import csv files local files
# Requirement: data_annual.txt, data_quarter.txt, data_monthly.txt are saved to local machine 
#

# add path to where txt files are saved
LOCAL_DIR = ""
DFA_PATH = os.path.join(LOCAL_DIR, "data_annual.txt")
DFQ_PATH = os.path.join(LOCAL_DIR, "data_quarter.txt")
DFM_PATH = os.path.join(LOCAL_DIR, "data_monthly.txt")

try:
    dfa = pd.read_csv(DFA_PATH)
    dfq = pd.read_csv(DFQ_PATH)
    dfm = pd.read_csv(DFM_PATH)
    # set time index
    self.dfq.index = pd.to_datetime(self.dfq.index)    
    self.dfm.index = pd.to_datetime(self.dfm.index)
except:
   print ("Cannot import from local files.")


#
# 2. Import csv files from web
# Requirement: internet access
#

URL_DIR = "https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/"
DFA_URL = URL_DIR  + "data_annual.txt"
DFQ_URL = URL_DIR  + "data_quarter.txt"
DFM_URL = URL_DIR  + "data_monthly.txt"

try:
    dfa = pd.read_csv(DFA_URL)
    dfq = pd.read_csv(DFQ_URL)
    dfm = pd.read_csv(DFM_URL)
    # set time index
    self.dfq.index = pd.to_datetime(self.dfq.index)    
    self.dfm.index = pd.to_datetime(self.dfm.index)
except:
   print ("Cannot import from web.")
    
#
# 3. Import csv files from 'kep' package
# Requirement: 'kep' package saved to local machine by git or by downloading zip file 
#               https://github.com/epogrebnyak/rosstat-kep-data/
#               You must be in directory from which 'kep' package is importable               
#

try:
   from kep import KEP, get_ts, get_df
   dfa, dfq, dfm = KEP().dfs()
   
   # get_ts() - query to obtain timeseries
   ts1 = get_ts('a', 'SOC_WAGE_rub')
   assert ts1.loc[2014] == 32495

   ts2 = get_ts('a', 'CPI_rog')
   assert ts2.loc[2014] == 111.4

   # get_df() - query to obtain pandas dataframe
   df1 = get_df("m", ['SOC_WAGE_rub', 'CPI_rog'])
   assert df1.loc['2015-10-31','SOC_WAGE_rub'] == 33357.0    # note: data revision, was 33240.0
   assert df1.loc['2015-10-31','CPI_rog'] == 100.7
   
except:
   print ("Cannot import from 'kep' package.")
   
try:
   print(dfa.head())
   print(dfq.head())
   print(dfm.head())
   #may also use .describe()
except:
   print ("Variables not imported.")
