import pandas as pd
from datetime import datetime
from calendar import monthrange

from label import Label
import tabulate as tab
import plots as plots

from inputs import File
from config import XLSX_FILE, XLS_FILE, ANNUAL_CSV, QUARTER_CSV, MONTHLY_CSV
from config import PDF_FILE, MD_FILE, PNG_FOLDER, VARNAMES_FILE, OUTPUT_DIR 

from db import DefaultDatabase, TrialDatabase

def get_end_of_monthdate(y, m):
    return datetime(year=y, month=m, day=monthrange(y, m)[1])

def get_end_of_quarterdate(y, q):
    return datetime(year=y, month=q*3, day=monthrange(y, q*3)[1])   
        
class DataframeEmitter():
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
    # Varnames table acces functions - used in publish.Publisher() class       
    #
    # ---------------------------------------------------------------------------------
    
    # def yield_var_name_components(self):        
        # """Yields a list containing variable name, text description and unit of measurement."""        
        # for var_name in self.get_saved_full_labels():
            # lab = Label(var_name)
            # yield [lab.labeltext, lab.head_description, lab.unit_description]
            
    # def df_vars(self):
       # iter = self.yield_var_name_components()
       # return pd.DataFrame(iter, columns = tab.TABLE_HEADER)
    
    # def txt_vars_table(self): 
       # iter = self.yield_var_name_components() 
       # return tab.pure_tabulate(iter)
       
    
    # ---------------------------------------------------------------------------------
    #   
    #  Dataframes       
    #
    # ---------------------------------------------------------------------------------
     
    
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
            
    def data_stream(self, freq, keys):
        for d in self.dicts:
            if d['freq'] == freq:
                yield {k: d[k] for k in keys}        
        
    def save_dfs(self):
        """Saves Dataframes to CSV"""

        def to_csv(df, filename):
           # as in DataFrame.to_csv(path_or_buf=None, sep=', ', na_rep='', float_format=None, columns=None, header=True, index=True, index_label=None, mode='w', encoding=None, quoting=None, quotechar='"', line_terminator='\n', chunksize=None, tupleize_cols=False, date_format=None, doublequote=True, escapechar=None, decimal='.', **kwds)
           df.to_csv(filename)

        to_csv(self.annual_df(), ANNUAL_CSV)
        to_csv(self.quarter_df(), QUARTER_CSV)
        to_csv(self.monthly_df(), MONTHLY_CSV)

class DataframeEmitterLinkedToDatabase(DataframeEmitter):
    """Stores copy of default or test database in *self.dicts*. """ 
       
    def __init__(self, db_type = 'default'):
       self.db_type = db_type
       if db_type == 'default':
           self.db = DefaultDatabase()
       elif db_type == 'test':
           self.db = TrialDatabase()
       else:
           raise Exception("Unrecongised database type:" + db_type)
       # initilise emitter with database data stream
       self.dicts = list(self.db.get_stream())       

class KEP():

    # everything from database will be in CSVs
    dfei = DataframeEmitterLinkedToDatabase()
    dfei.save_dfs()

    def __init__(self):
        """Read stored CSVs as dataframes."""
    
        def from_csv(f):
           return pd.read_csv(f, index_col=0)        
    
        self.dfa = from_csv(ANNUAL_CSV)
        self.dfq = from_csv(QUARTER_CSV)
        self.dfm = from_csv(MONTHLY_CSV)
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
        varnames = dict((freq, df.columns.tolist()) for df, freq in zip([self.dfa,self.dfq, self.dfm], 'aqm')) 
        if freq:
            return varnames[freq]
        else:
            return varnames 
            
    def __get_saved_full_labels__(self):
        return list(set(self.get_varnames('a') + self.get_varnames('q') + self.get_varnames('m')))

class Varnames(KEP):   
       
    def __yield_var_name_components__(self):        
        """Yields a list containing variable name, text description and unit of measurement."""        
        for var_name in self.__get_saved_full_labels__():
            lab = Label(var_name)
            yield [lab.labeltext, lab.head_description, lab.unit_description]
            
    def df_vars(self):
       iter = self.__yield_var_name_components__()
       return pd.DataFrame(iter, columns = tab.TABLE_HEADER)
    
    def txt_vars_table(self): 
       iter = self.__yield_var_name_components__() 
       return tab.pure_tabulate(iter)        
        