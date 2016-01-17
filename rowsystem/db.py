'''
Classes to store time series in a local database (sqlite) and access them as pandas dataframes. 

   DefaultDatabase()      Read/write wrapper around database. Accepts/emits streams 
                          of database rows as dictionaries.   
   DataframeEmitter()     Generic pandas interface to database, reshapes annual, quarterly 
                          and monthly  dataframes for convienient representation of data.
   KEP(DataframeEmitter)  End-user class to get time series as pandas objects.
   
'''

import os
import pandas as pd
from datetime import date, datetime
from calendar import monthrange

from rowsystem.label import Label
from rowsystem.config import PROJECT_SRC_FOLDER 

class Database():
    """(1) Save incoming datastream to database by .save_stream() 
       (2) Yield datastream from database by .get_stream()
       """    

    DB_MAIN_TABLE = 'flatdata'
    DB_FILES = {'test': os.path.join(PROJECT_SRC_FOLDER, "test.sqlite3")
        , 'default': os.path.join(PROJECT_SRC_FOLDER, "kep.sqlite3")
        }
        
    def _sqlite_backend(self):
        # to be overloaded
        # return 'sqlite:///' + DB_FILES['test']
        pass
        
    def __init__(self, gen = None):
        if gen:
            self.save_stream(gen)

    
    def __eq__(self, obj):
        return self.dicts == obj.dicts              
        
    def db_connect(self):
        # NOTE: may use old sqlite3 code instead
        import dataset
        sqlite_src = self._sqlite_backend()
        return dataset.connect(sqlite_src)

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
    
    @property 
    def dicts(self):
        return self.get_stream()

class DefaultDatabase(Database):

    def _sqlite_backend(self):
        # to be overloaded
        return 'sqlite:///' + self.DB_FILES['default']

class TestDatabase(Database):

    def _sqlite_backend(self):
        # to be overloaded
        return 'sqlite:///' + self.DB_FILES['test']
                
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
        
    @staticmethod
    def unique(x):
        return sorted(list(set(x)))

    def get_saved_full_labels(self):
        return self.unique([d['varname'] for d in self.dicts])       
        
    def get_saved_head_labels(self):
        return self.unique(Label(full_lab).head for full_lab in self.get_saved_full_labels())       
    
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

from publish import Publisher
        
class KEP(DataframeEmitter, Publisher):
    """Initalises connection to default KEP database."""      
    
     DB_STREAM = {'test': TestDatabase().get_stream(),
               'default': DefaultDatabase().get_stream() }
    
    def __init__(self, sourcetype = 'default'):
       self.dicts = list(DB_STREAM[sourcetype]) 

class CurrentKEP(KEP):
    """Writes latest month data to db and initalises connection to it."""      
    
    def update():
       from rowsystem.classes import CurrentMonthRowSystem 
       CurrentMonthRowSystem().save()    
    
    def __init__(self):
       self.update()
       self.dicts = list(self.DB_STREAM['default']) 
       
       
class TestKEP(KEP):
    """Initalises connection to test database."""     
    
    def __init__(self):
       self.dicts = list(self.DB_STREAM['test'])       
       