'''
Classes to store time series in database and access them as pandas dataframes. 

   DefaultDatabase()      Read/write wrapper around database. Accepts/emits streams 
                          of database rows as dictionaries.   
   DataframeEmitter()     Pandas interface to database. 
   KEP(DataframeEmitter)  End-user class to get time series.
   
'''

# TODO: available df access methods go to DataframeEmitter()
# TODO: move methods to RowSystem
# TODO: separate tests from this file 
# MAYDO: use dataset.freeze() for csv

import dataset # NOTE: may use old sqlite3 code instead

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

    def dicts_as_iter(self):
        return test_iter()

    def dicts_as_list(self):
        return list(test_iter())
    
    def save(self):
        DefaultDatabase().save_stream(gen = self.dicts_as_iter())

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
    
        
class KEP(DataframeEmitter):
    """Initalises connection to default KEP database."""      
    
    def __init__(self):
       self.dicts = list(DefaultDatabase().get_stream())
