from rowsystem.classes import RowSystem, CurrentMonthRowSystem 
from rowsystem.tests.testdata import TrialRowSystem, TrialAdminKEP
from rowsystem.config import CURRENT_MONTH_DATA_FOLDER, TESTFILE_DIR
from rowsystem.rowsystem import AdminKEP 
import rowsystem.tests.testdata as testdata

def get_testfolder_objects():
    testdata.get_testable_files()  
    rs = RowSystem(TESTFILE_DIR)
    rs.save()    
    kep = TrialAdminKEP()
    return rs, kep

def testfolder_teardown():
    testdata.remove_testable_files()
    
def test_testfolder_objects():
    t_rs, t_kep = get_testfolder_objects()
    assert t_rs == TrialRowSystem()
    assert t_kep == TrialAdminKEP()   
    testfolder_teardown()
    
def datafolder_objects():
    rs = RowSystem(CURRENT_MONTH_DATA_FOLDER)
    rs.save()    
    kep = AdminKEP()
    return rs, kep

#def test_datafolder_objects():
#    rs, kep = datafolder_objects()
#    assert rs == CurrentMonthRowSystem()
#    assert kep.dicts == AdminKEP().dicts    