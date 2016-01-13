'''
Classes to store time series in a local database (sqlite) and access them as pandas dataframes. 

   DefaultDatabase()      Read/write wrapper around database. Accepts/emits streams 
                          of database rows as dictionaries.   
   DataframeEmitter()     Generic pandas interface to database, reshapes annual, quarterly 
                          and monthly  dataframes for convienient representation of data.
   KEP(DataframeEmitter)  End-user class to get time series as pandas objects.
   
'''

import pandas as pd
import dataset # NOTE: may use old sqlite3 code instead
from datetime import date, datetime
from calendar import monthrange

class DefaultDatabase():
    """(1) Save incoming datastream to database by .save_stream() 
       (2) Yield datastream from database by .get_stream()
       """
    # NOTE: may use old sqlite3 code instead
    
    DB_MAIN_TABLE = 'flatdata'
    
    def __init__(self, gen = None):
        if gen:
            self.save_stream(gen)
    
    def db_connect(self):
        sqlite_file = "kep.sqlite3"
        return dataset.connect('sqlite:///' + sqlite_file)

    def reset(self):
        with self.db_connect() as con:
            con[self.DB_MAIN_TABLE].delete()

    # MAYDO: use dataset.freeze() for csv
    def save_stream(self, gen):
        """Save *gen* datastream to database. *gen* must be a list or stream of dictionaries."""
        self.reset()
        with self.db_connect() as con:
            con[self.DB_MAIN_TABLE].insert_many(gen)    
    
    def get_stream(self):
        """Yield stream of dictionaries from database."""
        with self.db_connect() as con:
            for row in con[self.DB_MAIN_TABLE]:
                row.popitem(last=False) # kill first 'id' column
                yield dict(row)
   
def get_end_of_monthdate(y, m):
    return datetime(year=y, month=m, day=monthrange(y, m)[1])

def get_end_of_quarterdate(y, q):
    return datetime(year=y, month=q*3, day=monthrange(y, q*3)[1])   
    
        
class DataframeEmitter():
    """Converts incoming stream of dictionaries from database to pandas dataframes."""
    
    def __init__(self, gen):
       self.dicts = list(gen)           
    
    def get_ts(self, freq, varname):
        # use self.dicts
        pass
        #TODO

    def get_df(self, freq, varname_list):
        # use self.dicts
        pass
        #TODO
        # check varname_list is list
    
    def get_varnames(self, varname_list):
        # use self.dicts
        #TODO
        pass
    
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
        # MAYDO: raise excetion if not labelled        
        for d in self.dicts:
            if d['freq'] == freq:
                yield {k: d[k] for k in keys}        
        
    def dfs(rs):
        dfa = annual_df(rs)
        dfq = quarter_df(rs)
        dfm = monthly_df(rs)
        return dfa, dfq, dfm        
        
        
class KEP(DataframeEmitter):
    """Initalises connection to default KEP database."""      
    
    def __init__(self):
       self.dicts = list(DefaultDatabase().get_stream())
