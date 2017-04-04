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