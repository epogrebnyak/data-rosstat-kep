# NOTE: may use old sqlite3 code instead
import dataset

'''
from rowsystem import RowSystem

rs = RowSystem(folder)
    # reads input definition from standard files
    # labels rows
    # starts pandas interface

rs.save()
    # saves data to default database or freeze files 

from kep import KEP
print(KEP().dfa.to_csv())
   
'''

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

    def dicts(self):
        return test_iter()
    
    def save(self):
        DefaultDatabase().save_stream(gen = self.dicts())

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
        pass

    def get_df(self, varname_list):
        pass
        # check varname_list is list
    
    def get_varnames(self, varname_list):
        pass
    
    @property    
    def dfa():
        pass
        
    @property
    def dfq():
        pass
        
    @property
    def dfm():
        pass   
        
    # TODO: available df access methods go here 
        
class KEP(DataframeEmitter):
    """Initalises connection to default KEP database."""      
    
    def __init__(self):
       self.dicts = list(DefaultDatabase().get_stream())
