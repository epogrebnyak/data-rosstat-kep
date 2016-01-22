from db import DataframeEmitter, DefaultDatabase, TestDatabase
from rs import RowSystem
from publish import Publisher

class DataframeEmitterInitialised(DataframeEmitter):
    """Stores copy of default or test database in *self.dicts*. """ 
       
    def __init__(self, sourcetype = 'default'):
       if sourcetype == 'default':
           self.db = DefaultDatabase()
       elif sourcetype == 'test':
           self.db = TestDatabase()
       else:
           raise Exception
       import pdb; pdb.set_trace()
       self.dicts = list(self.db.get_stream())   
       self.sourcetype = sourcetype
       
    def __update_from_current_month__(self):
       if self.sourcetype == 'default':
           from config import CURRENT_MONTH_DATA_FOLDER
           self.__rs__ = RowSystem(CURRENT_MONTH_DATA_FOLDER).save()
           # .save() above  pushed new data to DefaultDatabase(), __init__() below will read it from there
           self.__init__() 
           print(self.__rs__)
           print("\nDataset updated from " + self.__rs__.folder)       
           
        
class KEP(DataframeEmitterInitialised, Publisher):
    """Alias for DataframeEmitterInitialised - stores copy of DEFAULT database in 'self.dicts' and allows
       - retrieving datafames (via DatabaseWrapper + DataframeEmitter)
       - updating from current month folder with __update_from_current_month__()
       - writing graphs and xls/csv output to output folder (via Publisher)."""  
       
    def __init__(self):
        super().__init__('default')  
        
    # NOTE: some wisdom about multiple inheritance below
    # http://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance   