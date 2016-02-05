"""Examples to import annual, quarterly and monthly pandas dataframes:
   - from local files
   - from web
   - from 'kep' package   
   
   All examples result in annual, quarterly and monthly pandas dataframes in variables dfa, dfq, dfm respectively.
   
   Excel files are also available for download to explore data and double-check pandas/R results:
      https://github.com/epogrebnyak/rosstat-kep-data/raw/master/output/kep.xls
      https://github.com/epogrebnyak/rosstat-kep-data/raw/master/output/kep.xlsx    
   
   Excercise:
      1. obtain dfa, dfq, dfm in any or all of these methods
      
      2. try plotting some variables, e.g. reproduce graphs at https://github.com/epogrebnyak/rosstat-kep-data/blob/master/README.md#Основные-показатели
         also at qtr and monthly frequencies
         
         Pandas plotting code used may be found at: 
         https://github.com/epogrebnyak/rosstat-kep-data/blob/master/kep/extract/plots.py#L130-L139
         
      3. Get similar indicators for US economy from FRED (https://research.stlouisfed.org/docs/api/fred/)
"""

import pandas as pd
import os


def add_index(dfq, dfm):
    # set time index
    dfq.index = pd.to_datetime(dfq.time_index)    
    dfm.index = pd.to_datetime(dfm.time_index)
    return dfq, dfm
    

#
# 1. Import csv files local files
# Requirement: data_annual.txt, data_quarter.txt, data_monthly.txt are saved to local machine 
#

# add path to where txt files are saved. in this project this is 'output' folder
LOCAL_DIR = "output"
DFA_PATH = os.path.join(LOCAL_DIR, "data_annual.txt")
DFQ_PATH = os.path.join(LOCAL_DIR, "data_quarter.txt")
DFM_PATH = os.path.join(LOCAL_DIR, "data_monthly.txt")

try:
    dfa = pd.read_csv(DFA_PATH, index_col = 0)
    dfq = pd.read_csv(DFQ_PATH)
    dfm = pd.read_csv(DFM_PATH)
    # set time index
    dfq, dfm = add_index(dfq, dfm)
    print("Import from local files successful")
       
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
    dfa = pd.read_csv(DFA_URL, index_col = 0)
    dfq = pd.read_csv(DFQ_URL)
    dfm = pd.read_csv(DFM_URL)
    # set time index
    dfq, dfm = add_index(dfq, dfm)
    print("Import from web successful")

except:
   print ("Cannot import from web.")
   
# -----------------------------------------------------------------------------
#
# do not replicate this code in R ---------------------------------------------  
#


#
# 3. Import csv files from 'kep' package
# Requirement: 'kep' package saved to local machine by git or by downloading zip file 
#               at https://github.com/epogrebnyak/rosstat-kep-data/
#               You must be in directory from which 'kep' package is importable 
#               (repository root folder) 

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
    print("Import from 'kep' package successful")
    
except AttributeError:
    print ('Check working dir and paths in Spyder or run script in console.')
    
except:
    print ("Cannot import 'kep' package.")

#
#
# do not replicate code above in R --------------------------------------------
#
# -----------------------------------------------------------------------------

try:
   print(dfa.head())
   print(dfq.head())
   print(dfm.head())
   print(dfa.describe())
   print(dfq.describe())
   print(dfm.describe())
except:
   print ("Variables not imported.")
