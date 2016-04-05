"""Examples to import annual, quarterly and monthly pandas dataframes:
   - from local files
   - from web
   - from 'kep' package   
   
   All examples result in annual, quarterly and monthly pandas dataframes in variables dfa, dfq, dfm respectively.
   
   Excel files are also available for download to explore data and double-check pandas/R results:
      https://github.com/epogrebnyak/rosstat-kep-data/raw/master/output/kep.xls
      https://github.com/epogrebnyak/rosstat-kep-data/raw/master/output/kep.xlsx    
   

Excecise:

      1. Оbtain dfa, dfq, dfm dataframes from https://github.com/epogrebnyak/rosstat-kep-data/ 
      
      2. Try plotting some variables, e.g. reproduce graphs at 
         https://github.com/epogrebnyak/rosstat-kep-data/blob/master/README.md#Основные-показатели
         
         also at quarterly and annual frequencies
         
         Pandas plotting code used may be found at: 
         https://github.com/epogrebnyak/rosstat-kep-data/blob/master/kep/extract/plots.py#L130-L139
		   
		 Note: plot formats not important here, main task is to generate some plots. 
         
      3. Get and plot similar indicators for US economy from FRED database
         https://research.stlouisfed.org/docs/api/fred/)

"""

import pandas as pd
import os


# 1. Import csv files local files
# Requirement: data_annual.txt, data_quarter.txt, data_monthly.txt are saved to local machine 

# add path to where txt files are saved
LOCAL_DIR = "output"
DFA_PATH = os.path.join(LOCAL_DIR, "data_annual.txt")
DFQ_PATH = os.path.join(LOCAL_DIR, "data_quarter.txt")
DFM_PATH = os.path.join(LOCAL_DIR, "data_monthly.txt")

try:
    dfa = pd.read_csv(DFA_PATH, index_col = 0)
    dfq = pd.read_csv(DFQ_PATH, converters = {'time_index':pd.to_datetime}, index_col = 'time_index')
    dfm = pd.read_csv(DFM_PATH, converters = {'time_index':pd.to_datetime}, index_col = 'time_index')       
except:
   print ("Cannot import from local files.")

# 2. Import csv files from web
# Requirement: internet access

URL_DIR = "https://raw.githubusercontent.com/epogrebnyak/rosstat-kep-data/master/output/"
DFA_URL = URL_DIR  + "data_annual.txt"
DFQ_URL = URL_DIR  + "data_quarter.txt"
DFM_URL = URL_DIR  + "data_monthly.txt"

try:
    dfa = pd.read_csv(DFA_URL, index_col = 0)
    dfq = pd.read_csv(DFQ_URL, converters = {'time_index':pd.to_datetime}, index_col = 'time_index')
    dfm = pd.read_csv(DFM_URL, converters = {'time_index':pd.to_datetime}, index_col = 'time_index')
except:
   print ("Cannot import from web.")
   
# 3. Import csv files from 'kep' package
# Requirement: 'kep' package saved to local machine by git or by downloading zip file 
#               from https://github.com/epogrebnyak/rosstat-kep-data/
#               You must be in directory from which 'kep' package is importable 

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
    
# check import results     
try:
   print(dfa.head())
   print(dfq.head())
   print(dfm.head())
   print(dfa.describe())
   print(dfq.describe())
   print(dfm.describe())
except:
   print ("Variables not imported.")
