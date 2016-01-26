"""Update default database to current month and save dataframes as CSVs"""
# Must be in separate file to prevent import confilct with RowSystem

from dataframes import DictsAsDataframesLinkedToDatabase
from rs import CurrentMonthRowSystem

class Admin(DictsAsDataframesLinkedToDatabase):
    """Administrative class to update default database to current month and save dataframes as CSVs"""
           
    def __init__(self):
        super().__init__('default')  

    def update(self):
        # update default database to current month 
        self.__update_from_current_month__()
        # save dataframes as CSV
        self.save_dfs()
        
    def __update_from_current_month__(self):        
        self.rs = CurrentMonthRowSystem()        
        # .save() pushes new data to DefaultDatabase()        
        self.rs.save()
        # __init__() below reads new data from DefaultDatabase() 
        self.__init__() 
        print(self.rs)
        print("\nDataset updated from " + self.rs.folder) 
        
if __name__ == "__main__":
    a = Admin()
    a.update()