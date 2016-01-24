"""Aliases for DataframeEmitter class allowing access to default and test databases.
 
   AdminKEP().update() updates default database to current month data folder.

   """
# 
# NOTE (1): code cannot be placed in db.py because it causes circular reference and cannot be imported.
#
# NOTE (2): some wisdom about multiple inheritance below
# http://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
#

from dataframes import DataframeEmitterInitialised
from rs import CurrentMonthRowSystem
from publish import Publisher
      
        
class AdminKEP(DataframeEmitterInitialised, Publisher):
    """Alias for DataframeEmitterInitialised - stores copy of DEFAULT database in 'self.dicts' 
       and allows following:
       - retrieving datafames (via DatabaseWrapper + DataframeEmitter)
       - updating from current month folder with __update_from_current_month__()
       - writing graphs and xls/csv output to output folder (via Publisher).
    """
    
    def __init__(self):
        super().__init__('default')  

    def update(self):
        self.__update_from_current_month__()
        self.save_dfs()
        
    def __update_from_current_month__(self):
        self.rs = CurrentMonthRowSystem()        
       
        # .save() pushes new data to DefaultDatabase()        
        self.rs.save()

        # __init__() below reads new data from DefaultDatabase() 
        self.__init__() 

        print(self.rs)
        print("\nDataset updated from " + self.rs.folder)
        return self 
        

if __name__ == "__main__":
    a = AdminKEP()
    a.update()
    a.publish()