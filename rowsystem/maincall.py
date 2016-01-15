from rowsystem.config import CURRENT_MONTH_DATA_FOLDER, TESTFILE_DIR
import rowsystem.tests.testdata as testdata

from rowsystem.rowsystem import RowSystem 
from rowsystem.db import KEP

def testfolder_objects():
    testdata.get_testable_files()  
    rs = RowSystem(TESTFILE_DIR)
    rs.save()    
    kep = KEP()
    #dfa = kep.annual_df()
    #dfq = kep.quarter_df()
    #dfm = kep.monthly_df()
    return rs, kep

def testfolder_teardown():
    testdata.remove_testable_files()
    
def datafolder_objects():
    rs = RowSystem(CURRENT_MONTH_DATA_FOLDER)
    rs.save()    
    kep = KEP()
    return rs, kep

def get_dfa():
    rs, kep = datafolder_objects()
    return kep.annual_df()   

if __name__ == '__main__':
    dfa = get_dfa()