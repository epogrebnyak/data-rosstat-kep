import pandas as pd
from datetime import datetime
from calendar import monthrange

from kep.reader.label import Label
import kep.common.tabulate as tab
from kep.database.db import DefaultDatabase, TrialDatabase
from kep.config import DATABASE_CSV_FILENAMES, OUTPUTDIR_CSV_FILENAMES


def get_end_of_monthdate(y, m):
    return datetime(year=y, month=m, day=monthrange(y, m)[1])

    
def get_end_of_quarterdate(y, q):
    return datetime(year=y, month=q*3, day=monthrange(y, q*3)[1])   
    
    
class DictsAsDataframes():
    """Converts incoming stream of dictionaries from database to pandas dataframes."""
    
    def __init__(self, gen):
       self.dicts = list(gen)           

    def __eq__(self, obj):
        return self.dicts == obj.dicts  
        
    def len(self):
        return len(self.dicts) 

    # ---------------------------------------------------------------------------------
    #   
    # Variable names        
    #
    # ---------------------------------------------------------------------------------
    
    def get_varnames(self):
        return self.get_saved_full_labels()
          
    @staticmethod
    def unique(x):
        return sorted(list(set(x)))

    def get_saved_head_labels(self):
        return self.unique(Label(full_lab).head for full_lab in self.get_saved_full_labels())       

    def get_saved_full_labels(self):
        return self.unique([d['varname'] for d in self.dicts]) 
        
    # ---------------------------------------------------------------------------------
    #   
    #  Dataframes       
    #
    # ---------------------------------------------------------------------------------
     
    def data_stream(self, freq, keys):
        for d in self.dicts:
            if d['freq'] == freq:
                yield {k: d[k] for k in keys}        
           
    def _annual_duplicated(self):    
        annual_data_stream = self.data_stream('a', ['varname', 'year', 'value'])
        dfa = pd.DataFrame(annual_data_stream)    
        return dfa[dfa.duplicated(['varname','year'], False) == True]
    
    def annual_df(self):
        """Returns pandas dataframe with ANNUAL data from labelled rowsystem *rs*."""
        
        def duplicate_labels(df):
               r = df[df.duplicated(['varname','year']) == True]
               return r['varname'].unique()
           
        def check_for_dups(df): 
               dups = duplicate_labels(df)
               if len(dups) > 0:
                   raise Exception("Duplicate labels: " + " ".join(dups))

        annual_data_stream = self.data_stream('a', ['varname', 'year', 'value'])
        dfa = pd.DataFrame(annual_data_stream)
        check_for_dups(dfa)
        dfa = dfa.pivot(columns='varname', values='value', index='year')
        return dfa
        
    def quarter_df(self):
        """Returns pandas dataframe with QUARTERLY data from labelled rowsystem *rs*."""
    
        # get datastream 
        qtr_data_stream = self.data_stream('q', ['varname', 'year', 'qtr', 'value'])
        
        # get datastream     
        dfq = pd.DataFrame(qtr_data_stream)
        
        # add time index
        dt = [get_end_of_quarterdate(y,q) for y, q in zip(dfq["year"], dfq["qtr"])]
        dfq["time_index"] = pd.DatetimeIndex(dt, freq = "Q")

        # reshape
        dfq = dfq.pivot(columns='varname', values='value', index='time_index')
        
        # add extra columns
        dfq.insert(0, "year", dfq.index.year)    
        dfq.insert(1, "qtr", dfq.index.quarter)
        return dfq
        
    def monthly_df(self):
        """Returns pandas dataframe with MONTHLY data from labelled rowsystem *rs*."""
    
        # get datastream     
        monthly_data_stream = self.data_stream('m', ['varname', 'year', 'month', 'value'])    
                
        # obtain dataframe
        dfm = pd.DataFrame(monthly_data_stream)                        
        
        # add time index
        dt = [get_end_of_monthdate(y,m) for y, m in zip(dfm["year"], dfm["month"])]
        dfm["time_index"] = pd.DatetimeIndex(dt, freq = "M")

        # reshape
        dfm = dfm.pivot(columns='varname', values='value', index='time_index')
        
        # add extra columns
        dfm.insert(0, "year", dfm.index.year)
        dfm.insert(1, "month", dfm.index.month)
        return dfm 
        
    def save_dfs(self): 
        """Save dataframes to CSV"""
        self._save_dfs(DATABASE_CSV_FILENAMES)    
        self._save_dfs(OUTPUTDIR_CSV_FILENAMES)
        
    def _save_dfs(self, filenames):

        def to_csv(df, f):
           # as in DataFrame.to_csv(path_or_buf=None, sep=', ', na_rep='', float_format=None, columns=None, header=True, 
           #                        index=True, index_label=None, mode='w', encoding=None, quoting=None, quotechar='"', 
           #                        line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True, 
           #                        escapechar=None, decimal='.', **kwds)
           df.to_csv(f)

        to_csv(self.annual_df(),  filenames['a'])
        to_csv(self.quarter_df(), filenames['q'])
        to_csv(self.monthly_df(), filenames['m'])
        
        
# ---------------------------------------------------------------------------------
#   
#  Dicts copied from database
#
# ---------------------------------------------------------------------------------        
    
class DatabaseDictsAsDataframes(DictsAsDataframes):
    """Stores copy of DEFAULT database in *self.dicts*."""
       
    def __init__(self):
       self.db = DefaultDatabase()
       self.dicts = list(self.db.get_stream()) 
	   
class TrailDatabaseDictsAsDataframes(DictsAsDataframes):
    """Stores copy of TRAIL database in *self.dicts*."""
       
    def __init__(self):
       self.db = TrialDatabase()
       self.dicts = list(self.db.get_stream())   

# ---------------------------------------------------------------------------------
#   
#  End-user dataframes
#
# --------------------------------------------------------------------------------- 


class KEP():
    """Read stored CSVs as dataframes."""

    def __init__(self):
        self.read_dfs()
        
    
    def read_dfs(self):
        
        # WARNING: effectively we do not know the state of the database or csv dumps at this point
        #          deep update is CurrentMonthRowSystem().update()
        #          shallow update is DatabaseDictsAsDataframes().save_dfs()
        #          in practice we hope CurrentMonthRowSystem().update() was run some time before by administrator, eg by invoking update.py
        #          uncomment below to force start parsing routines
        #
        # CurrentMonthRowSystem().update()
        
        filenames = DATABASE_CSV_FILENAMES
        
        def from_csv(f):
            return pd.read_csv(f, index_col=0)
        
        # read dataframe CSV dumps
        self.dfa = from_csv(filenames['a'])
        self.dfq = from_csv(filenames['q'])
        self.dfm = from_csv(filenames['m'])
        self.dfq.index = pd.to_datetime(self.dfq.index)    
        self.dfm.index = pd.to_datetime(self.dfm.index)
    
    # ---------------------------------------------------------------------------------
    #   
    #  Time series and dataframe by label       
    #
    # ---------------------------------------------------------------------------------
    
    def get_ts(self, freq, varname):
        df = self.get_df(freq, [varname])
        return df[varname]

    def get_df(self, freq, labels):        
        df_dict = {'a': self.dfa, 'q': self.dfq, 'm': self.dfm}
        df = df_dict[freq]
        slicing_labels = [lab for lab in labels if lab in df.columns]       
        return df[slicing_labels]
        
    def get_varnames(self, freq = None):
        varnames = dict((ltr, df.columns.tolist()) for df, ltr in zip([self.dfa,self.dfq, self.dfm], 'aqm')) 
        if freq:
            return varnames[freq]
        else:
            return varnames 
    
    def dfs(self):
    	"""Shorthand for obtaining three resulting dataframes."""
    	return self.dfa, self.dfq, self.dfm
            
    def __get_saved_full_labels__(self):
        return list(set(self.get_varnames('a') + self.get_varnames('q') + self.get_varnames('m')))

# ---------------------------------------------------------------------------------
#   
#  Varname info holder class (used in Publisher class)
#
# --------------------------------------------------------------------------------- 

class Varnames(KEP):   
       
    def _yield_varname_components(self):        
        """Yields a list containing variable name, text description and unit of measurement.""" 
        
        varnames_by_freq = dict((ltr,self.get_varnames(ltr)) for ltr in list("aqm"))
        
        def freq_code(varname):
           code = ""
           for ltr in "aqm": 
               if varname in varnames_by_freq[ltr]:
                   code += ltr
           return code.upper()                    
        
        varnames = self.__get_saved_full_labels__()
        varnames.remove('year')
        varnames.remove('qtr')
        varnames.remove('month')
        
        for varname in varnames:
            yield [varname, Label(varname).head_description, Label(varname).unit_description, freq_code(varname)]
            
    def _list_varname_components(self):
       return sorted(self._yield_varname_components()) 
    
    def df_vars(self):
       iter_ = self._list_varname_components()
       return pd.DataFrame(iter_, columns = tab.TABLE_HEADER)
    
    def txt_vars_table(self): 
       iter_ = self._list_varname_components() 
       return tab.pure_tabulate(iter_)
