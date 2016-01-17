# Test rowsystem end-to-end 

import os 

from rowsystem.classes import RowSystem
from rowsystem.db import KEP, TestKEP
from rowsystem.tests.testdata import TestRowSystem

from rowsystem.config import CURRENT_MONTH_DATA_FOLDER, TESTFILE_DIR
import rowsystem.tests.testdata as testdata

def test_folder_level_import_and_df_testing():
    testdata.get_testable_files() # MAYDO: return folder path
    folder = TESTFILE_DIR #os.path.dirname(os.path.realpath(__file__)) # MAYDO: incorporate as RowSystem()
    rs = RowSystem(folder)
    rs.save()    
    kep = KEP()
    dfa = kep.annual_df()
    dfq = kep.quarter_df()
    dfm = kep.monthly_df()
    assert testdata.REF_DFA_CSV == dfa.to_csv()
    assert testdata.REF_DFQ_CSV == dfq.to_csv()
    assert testdata.REF_DFM_CSV == dfm.to_csv()
    testdata.remove_testable_files()

def test_folder_level_import_and_df_testing():   
    labels_in_db = TestKEP().get_saved_head_labels() 
    labels_in_def = TestRowSystem().get_definition_head_labels()
    ref_label_list = ['CPI', 'CPI_NONFOOD', 'IND_PROD', 'INVESTMENT', 'SALES_FOOD', 'SALES_NONFOOD', 'TRANS']
    assert ref_label_list == labels_in_db
    assert ref_label_list == labels_in_def

