"""Aliases for DataframeEmitter class allowsing access to default and test databases.
 
   KEP().__update_from_current_month__() updates default database for current month data folder.

   """

# NOTE: code cannot be placed in db.py because it then causes circular reference and cannot be imported.

from db import DefaultDatabase, TestDatabase
from df_emitter import DataframeEmitter
from rs import RowSystem
from publish import Publisher

class DataframeEmitterInitialised(DataframeEmitter):
    """Stores copy of default or test database in *self.dicts*. """ 
       
    def __init__(self, db_type = 'default'):
       if db_type == 'default':
           self.db = DefaultDatabase()
       elif db_type == 'test':
           self.db = TestDatabase()
       else:
           raise Exception
       self.dicts = list(self.db.get_stream())   
       self.db_type = db_type
       
    def update(self):
       self.__update_from_current_month__() 
           
    def __update_from_current_month__(self):
       if self.db_type == 'default':
           from config import CURRENT_MONTH_DATA_FOLDER
           self.__rs__ = RowSystem(CURRENT_MONTH_DATA_FOLDER).save()
           # NOTE (important):
           # .save() above pushed new data to DefaultDatabase(), __init__() below will read it from there
           self.__init__() 
           print(self.__rs__)
           print("\nDataset updated from " + self.__rs__.folder)
           return self           
           
        
class KEP(DataframeEmitterInitialised, Publisher):
    """Alias for DataframeEmitterInitialised - stores copy of DEFAULT database in 'self.dicts' 
       and allows following:
       - retrieving datafames (via DatabaseWrapper + DataframeEmitter)
       - updating from current month folder with __update_from_current_month__()
       - writing graphs and xls/csv output to output folder (via Publisher).
    """
    
    def __init__(self):
        super().__init__('default')  
        
    # NOTE: some wisdom about multiple inheritance below
    # http://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance