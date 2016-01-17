from rowsystem.classes import RowSystem, CurrentMonthRowSystem 
from rowsystem.tests.testdata import TestRowSystem
from rowsystem.config import CURRENT_MONTH_DATA_FOLDER, TESTFILE_DIR
from rowsystem.db import KEP, TestKEP, CurrentKEP
import rowsystem.tests.testdata as testdata

def get_testfolder_objects():
    testdata.get_testable_files()  
    rs = RowSystem(TESTFILE_DIR)
    rs.save()    
    kep = TestKEP()
    return rs, kep

def testfolder_teardown():
    testdata.remove_testable_files()
    
def test_testfolder_objects():
    t_rs, t_kep = get_testfolder_objects()
    assert t_rs == TestRowSystem()
    assert t_kep == TestKEP()   
    testfolder_teardown()
    
def datafolder_objects():
    rs = RowSystem(CURRENT_MONTH_DATA_FOLDER)
    rs.save()    
    kep = KEP()
    return rs, kep

def test_datafolder_objects():
    rs, kep = datafolder_objects()
    assert rs == CurrentMonthRowSystem()
    assert kep.dicts == CurrentKEP().dicts    
    
def get_dfa():
    rs, kep = datafolder_objects()
    return kep.annual_df()   
   
if __name__ == '__main__':
    dfa = get_dfa()
    assert dfa == CurrentMonthRowSystem().data.annual_df()
    dfq = kep.quarter_df()
    dfm = kep.monthly_df()