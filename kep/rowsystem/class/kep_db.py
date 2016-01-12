'''
Classes to store time series in a local database (sqlite) and access them as pandas dataframes. 

   DefaultDatabase()      Read/write wrapper around database. Accepts/emits streams 
                          of database rows as dictionaries.   
   DataframeEmitter()     Generic pandas interface to database, reshapes annual, quarterly 
                          and monthly  dataframes for convienient representation of data.
   KEP(DataframeEmitter)  End-user class to get time series as pandas objects.
   
'''

# TODO: available df access methods go to DataframeEmitter()
# TODO: move methods to RowSystem
# TODO: separate tests from this file 
# MAYDO: use dataset.freeze() for csv

import dataset # NOTE: may use old sqlite3 code instead
from datetime import date, datetime
from calendar import monthrange

def test_iter():
    yield {'varname':'GDP_rub', 'year':2014, 'val':65000}
    yield {'varname':'GDP_rub', 'year':2014, 'val':62000}

class RowSystem():
    
    def __init__(*arg):
        # read definition
        self.read_definition(*arg)
        # init rowsystem with empty values
        self.build_rs()
        # label rows
        self.label()
        # allow call like rs.data.dfa. NOTE: may have DataframeEmitter as parent for RowSystem() for call like rs.dfa
        self.data = DataframeEmitter(self.dicts())



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

def test_DefaultDatabase():        
    test_db = DefaultDatabase(test_iter())
    assert list(test_iter()) == list(test_db.get_stream())

        
class DataframeEmitter():
    """Converts incoming stream of dictionaries from database to pandas dataframes."""
    
    def __init__(self, gen):
       self.dicts = list(gen)           
    
    def get_ts(self, varname):
        # use self.dicts
        pass

    def get_df(self, varname_list):
        # use self.dicts
        pass
        # check varname_list is list
    
    def get_varnames(self, varname_list):
        # use self.dicts
        pass
    
    def df_annual():
        # use self.dicts
        pass
        
    def df_quarterly():
        # use self.dicts
        pass
        
    def df_monthly():
        # use self.dicts
        pass   
        
#-------------------------------------------


def data_stream(rs, freq, keys):
   # MAY DO: raise excetion if not labelled
   for db_row in stream_flat_data(rs):
          d = db_tuple_to_dict(db_row)
          if d['freq'] == freq:
              yield {k: d[k] for k in keys}

def annual_data_stream(rs):
     return data_stream(rs, 'a', ['varname', 'year', 'value'])

def qtr_data_stream(rs):
     return data_stream(rs, 'q', ['varname', 'year', 'qtr', 'value'])

def monthly_data_stream(rs):
     return data_stream(rs, 'm', ['varname', 'year', 'month', 'value'])
   
def get_annual_df(rs):
    """Returns pandas dataframe with annual data from labelled rowsystem *rs*."""
    
    def duplicate_labels(df):
           r = df[df.duplicated(['varname','year']) == True]
           return r['varname'].unique()
       
    def check_for_dups(df): 
           dups = duplicate_labels(df)
           if len(dups) > 0:
               raise Exception("Duplicate labels: " + " ".join(dups))

    dfa = pd.DataFrame(annual_data_stream(rs))
    dfa = dfa.pivot(columns='varname', values='value', index='year')
    #TODO: 
    #check_for_dups(dfa)
    return dfa

def get_end_of_monthdate(y, m):
    return datetime(year=y, month=m, day=monthrange(y, m)[1])

def get_end_of_quarterdate(y, q):
    return datetime(year=y, month=q*3, day=monthrange(y, q*3)[1])
    
def get_qtr_df(rs):
    """Returns pandas dataframe with QUARTERLY data from labelled rowsystem *rs*."""
    
    # get datastream     
    dfq = pd.DataFrame(qtr_data_stream(rs))
    
    # add time index
    dt = [get_end_of_quarterdate(y,q) for y, q in zip(dfq["year"], dfq["qtr"])]
    dfq["time_index"] = pd.DatetimeIndex(dt, freq = "Q")

    # reshape
    dfq = dfq.pivot(columns='varname', values='value', index='time_index')
    
    # add extra columns
    dfq.insert(0, "year", dfq.index.year)    
    dfq.insert(1, "qtr", dfq.index.quarter)
    return dfq

def get_monthly_df(rs):
    """Returns pandas dataframe with MONTHLY data from labelled rowsystem *rs*."""
    # get datastream     
    dfm = pd.DataFrame(monthly_data_stream(rs))
    
    # add time index
    dt = [get_end_of_monthdate(y,m) for y, m in zip(dfm["year"], dfm["month"])]
    dfm["time_index"] = pd.DatetimeIndex(dt, freq = "M")

    # reshape
    dfm = dfm.pivot(columns='varname', values='value', index='time_index')
    
    # add extra columns
    dfm.insert(0, "year", dfm.index.year)
    dfm.insert(1, "month", dfm.index.month)
    return dfm
    
def dfs(rs):
    dfa = get_annual_df(rs)
    dfq = get_qtr_df(rs)
    dfm = get_monthly_df(rs)
    return dfa, dfq, dfm


        
#-------------------------------------------        
        
        
        
class KEP(DataframeEmitter):
    """Initalises connection to default KEP database."""      
    
    def __init__(self):
       self.dicts = list(DefaultDatabase().get_stream())
