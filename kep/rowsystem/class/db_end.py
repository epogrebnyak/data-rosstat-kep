'''
from rowsystem import RowSystem
from kep import KEP

rs = RowSystem(folder)
    # reads input definition from standard files
    # labels rows

rs.save()
    # saves data to default database
        # streams flat dictionaries 
        # + saves to sqlite
        # + saves to csv (freeze)


'''

def test_iter():
    yield {'varname':'GDP_rub', 'year':2014, 'val':65000}
    yield {'varname':'GDP_rub', 'year':2014, 'val':62000}

#  -----------------------------------------------------------------------
#     
#DEV NOTES:
#1. DefaultDatabase() may use old sqlite3 code or pip install dataset
#
#2. RowSystem(folder).save() writes RowSystem(folder).get_dicts_stream() to database:
#      DefaultDatabase(gen = self.get_dicts_stream())

class RowSystem():

    def _get_dicts_stream(self):
        return test_iter()
    
    def save(self):
        self.data = DataframeEmitter(self._get_dicts_stream())
        DefaultDatabase(gen = self._get_dicts_stream())  

#3. Init emitter with dicts stream either in RowSystem or in KEP
#      - In folder class:
#      self.data = DataframeEmitter(self.get_dicts_stream())
#      self.data.dfa() 
#         OR
#      inherit DataframeEmitter in RowSystem
#
#      - Standalone in KEP - #DONE
#
#4. Reuse available code in DataframeEmitter()
#
#  -----------------------------------------------------------------------

import dataset
    
class DefaultDatabase():
    """Save incoming datastream to database. Yield datastream from database."""

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
                row.popitem(last=False)
                yield dict(row) #({k:row[k] for k in KEYS})   
        
test_db = DefaultDatabase(test_iter())
assert list(test_iter()) == list(test_db.get_stream())
        
        
class DataframeEmitter():
    """Converts stream of dictionaries from database to pandas dataframes."""
    
    def __init__(self, gen):
       self.dicts = list(gen)           
    
    def get_ts(self, varname):
        pass

    def get_df(self, varname_list):
        pass
        # check varname_list is list
    
    @property    
    def dfa():
        pass
        
    @property
    def dfq():
        pass
        
    @property
    def dfm():
        pass   
        
    # supplementary methods go here - from 
        
class KEP(DataframeEmitter):
    """Initalises connection to default KEP database."""      
    
    def __init__(self):
       self.dicts = list(DefaultDatabase().get_stream())
#       
#print(KEP.dfa.to_csv)
