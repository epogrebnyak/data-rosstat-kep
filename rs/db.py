'''
Classes to store time series in a local database (sqlite) and access them as pandas dataframes. 

   DefaultDatabase()      Read/write wrapper around database. Accepts/emits streams 
                          of database rows as dictionaries.   
                          
   DataframeEmitter()     Generic pandas interface to database dicts stream, produces annual, quarterly 
                          and monthly dataframes for convienient representation of data.
'''

from config import TEST_SQLITE_FILE, DEFAULT_SQLITE_FILE

class Database():
    """(1) Save incoming datastream to database by .save_stream() 
       (2) Yield datastream from database by .get_stream()
       """    

    DB_MAIN_TABLE = 'flatdata'
    DB_HEADLABELS = 'headlabels'
    DB_FILES = {'test': TEST_SQLITE_FILE
           , 'default': DEFAULT_SQLITE_FILE }
        
    def _sqlite_backend(self):
        # to be overloaded in child classes
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
            con[self.DB_HEADLABELS].delete()

    def save_iter_to_table(self, gen, table):
        """Save *gen* datastream to database. *gen* must be a list or stream of dictionaries."""
        # MAYDO: use dataset.freeze() for csv export/import    
        with self.db_connect() as con:
            con[table].delete()
        with self.db_connect() as con:
            con[table].insert_many(gen)     
            
    def save_stream(self, gen):
        self.save_iter_to_table(gen, self.DB_MAIN_TABLE) 
    
    def save_headlabel_description_dicts(self, gen):
        self.save_iter_to_table(gen, self.DB_HEADLABELS)        
        
    def get_iter_from_table(self, table):
        """Yield stream of dictionaries from database."""
        with self.db_connect() as con:
            for row in con[table]:
                row.popitem(last=False) # kill first 'id' column
                yield dict(row)
        
    def get_stream(self):
        return self.get_iter_from_table(self.DB_MAIN_TABLE) 
    
    @property 
    def dicts(self):
        return self.get_stream()
        
    def get_headlabel_description_dicts(self):
        return dict([(x["_head"],x["_desc"]) for x in self.get_iter_from_table(self.DB_HEADLABELS)])

    @property 
    def headlabel_desc_dicts(self):
        return self.get_headlabel_description_dicts()        
        
class DefaultDatabase(Database):

    def _sqlite_backend(self):
        # overloading 
        return 'sqlite:///' + self.DB_FILES['default']

class TestDatabase(Database):

    def _sqlite_backend(self):
        # overloading
        return 'sqlite:///' + self.DB_FILES['test']
                
