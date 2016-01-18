#from rowsystem.classes import CurrentMonthRowSystem
#from rowsystem.rowsystem import KEP
#from rowsystem.tests.testdata import TrialRowSystem, TrialKEP

# placing this code in separate file to avoid curcular reference in DatabaseWrapper.__update__():
from rowsystem.db import DataframeEmitter, TestDatabase,  DefaultDatabase
from rowsystem.publish import Publisher 
from rowsystem.classes import CurrentMonthRowSystem 
       
class DatabaseWrapper(DataframeEmitter):
    """Stores copy of default or test database in 'self.dicts' 
       and allows getting dataframes""" 
       
    DB_STREAM = {'test': TestDatabase(),
              'default': DefaultDatabase()}
       
    def __init_by_source__(self, sourcetype):
       self.dicts = list(self.DB_STREAM[sourcetype].get_stream())
    
    def __init__(self, sourcetype = 'default'):
       self.sourcetype = sourcetype
       self.__init_by_source__(self.sourcetype)
       
    def __eq__(self, obj):
       return self.dicts == obj.dicts  

    def __update__(self):
       cmrs = CurrentMonthRowSystem()
       cmrs.save()
       self.__init_by_source__(self.sourcetype) 
       print("Dataset updated from " + cmrs.folder)       
       print(cmrs)
      
class KEP(DatabaseWrapper, Publisher):
    """Alias for DatabaseWrapper  - stores copy of DEFAULT database in 'self.dicts' and allows
       - retrieving datafames (via DatabaseWrapper/DataframeEmitter)
       - updating from current month folder with __update__()
       - writing graphs and xls/csv output to output folder (via Publisher)."""  
       
    def __init__(self):
        super().__init__('default')  
        
    # NOTE: some wisdom about multiple inheritance here
    #       url - http://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance    
       
