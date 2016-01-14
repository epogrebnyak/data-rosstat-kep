# Test rowsystem end-to-end 

import os 

from rowsystem.rowsystem import RowSystem
from rowsystem.db import KEP

#from rowsystem.config import CURRENT_MONTH_DATA_FOLDER, current_folder
import rowsystem.tests.testdata

assert current_folder() == os.path.dirname(os.path.realpath(__file__))

def test_folder_level_import_and_df_testing():
    testdata.get_testable_files() # MAYDO: return folder path
    folder = testdata.current_folder() #os.path.dirname(os.path.realpath(__file__)) # MAYDO: incorporate as RowSystem()
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
    return dfa, rs 

dfa, rs = test_folder_level_import_and_df_testing()
z = rs.get_definition_head_labels()
   
#    
# TODO: add new methods rs.validate() - it must: 
# - get head labels list from a definition
# - get head labels from rs.dicts_as_iter()
# - compare these

# from rowsystem import rowsystem_head_labels as collect_head_labels
#    
#def test_full_import():

   #TODO: get labels from spec, used in import check =  all must be imported 
   #labels_in_spec,  = get_target_and_actual_varnames_by_file(spec_path, cfg_path)
   #assert labels_in_spec ==

#
#   get_testable_files()
#   folder = os.path.dirname(os.path.realpath(__file__))
#   rs = init_rowsystem_from_folder(folder)
#   #import pdb; pdb.set_trace()   
#   labels_in_db = collect_head_labels(rs)
#   assert labels_in_db == ['CPI', 'CPI_NONFOOD', 'IND_PROD', 'INVESTMENT', 'SALES_FOOD', 'SALES_NONFOOD', 'TRANS']
