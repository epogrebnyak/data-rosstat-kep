"""Examples to import annual, quarterly and monthly pandas dataframes:
   - from local files
   - from web
   - from 'kep' package   
   
   All examples result in annual, quarterly and monthly pandas dataframes in variables dfa, dfq, dfm
   
   May also manually download Excel files to explore data and double-check:
      https://github.com/epogrebnyak/rosstat-kep-data/raw/master/output/kep.xls
      https://github.com/epogrebnyak/rosstat-kep-data/raw/master/output/kep.xlsx    
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
# Requirement: 'kep' package saved to local machine via git or by downloading zip file 
#               URL: https://github.com/epogrebnyak/rosstat-kep-data/
#               You must bein directory from which 'kep' package is importable               
#

try:
   from kep import KEP
   dfa, dfq, dfm = KEP().dfs() 
except:
   print ("Cannot import from 'kep' package.")
