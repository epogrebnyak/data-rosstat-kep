import os
import pandas as pd
from pprint import pprint
from spec_io import write_file, fcomp

from spec_io import load_spec, load_cfg, param_import_from_files
from rowsystem import doc_to_rowsystem, label_rowsystem, init_rowsystem_from_folder, get_annual_df

# --- hardcoded constrants for testing ---
# 1. csv input
CSV_DOC = "\n".join(["1. Gross domestic product at current prices",
          "billion ruble",          
          "\tYEAR\tVALUE",
          "2013\t61500",
          "2014\t64000",
          "percent change from previous year - annual basis",
          "2013\t1.013",
          "2014\t1.028"])

# 2. specification = header/unit dictionaries + reader function and segment information
header_dict = {"Gross domestic product": ["GDP", "bln_rub"]}

unit_dict   = {'billion ruble':'bln_rub',
               'percent change from previous year':'yoy'}

segment1    = {'start line' : None,
               'end line' : None,
               'special reader': None}

segment2    = {'start line' : 'percent change',
               'end line' : None,
               'special reader': 'read_special'}

SPEC1 = (header_dict , unit_dict,  segment1)
SPEC2 = (header_dict , unit_dict,  segment2)

spec1_txt = """
# segment information
start line : null
end line : null
special reader: null

---
billion ruble : bln_rub
percent change from previous year : yoy

---
Gross domestic product:
  - GDP
  - bln_rub
"""

spec2_txt = """
# segment information
start line : percent change
end line : null
special reader: read_special

---
billion ruble : bln_rub
percent change from previous year : yoy

---
Gross domestic product:
  - GDP
  - bln_rub
"""

# ----------------------------

def get_testable_files_rs():        
    csvfile = write_file("tab.csv", CSV_DOC)
    spec_filename = write_file ("tab_spec.txt", spec1_txt)
    tmp_spec2 = write_file ("spec2.txt", spec2_txt)
    cfg_filename = write_file("tab_cfg.txt", """- spec2.txt""")
    return {'csv':csvfile, 'spec':spec_filename, 'cfg':cfg_filename, 'more':[tmp_spec2]}
    
def remove_testable_files():
    fdict = get_testable_files_rs()
    filelist = [fdict[k] for k in ['csv','spec','cfg']] + fdict['more']
    for fn in filelist:  
        os.remove(fn)

# ----------------------------
        
# 3. labelled rowsystem
from rs_constants import LABELLED_WITH_SEGMENTS, LABELLED_RS

# 4. resulting dataframe
DFA = pd.DataFrame.from_items([
                                 ('GDP_bln_rub', [61500.0, 64000.0])
                                ,('GDP_yoy', [1.013, 1.028])
                                 ])             
DFA.index = [2013,2014]                             

        
# --- testing ---

def test_specs():
    fcomp (spec1_txt, SPEC1, load_spec)
    fcomp (spec2_txt, SPEC2, load_spec)

def test_file_csv_import():    
    csvfile = write_file("tab_csv.txt", CSV_DOC) 
    rs = doc_to_rowsystem(csvfile)
    rs = label_rowsystem(rs, SPEC1)
    ref = LABELLED_RS
    #import pdb; pdb.set_trace()
    _comp(rs, ref)
    os.remove(csvfile)

def test_main():
    rs1 = doc_to_rowsystem(CSV_DOC)
    rs2 = label_rowsystem(rs1, SPEC1)    
    ref = LABELLED_RS
    _comp(rs2, ref)
    df = get_annual_df(rs2)
    # MAYDO: fix lousy comparison below
    assert 'year' + DFA.to_csv() == df.to_csv()
    
def test_with_segments_by_var():
    SEG = [('percent change', None, SPEC2)]
    rs1 = doc_to_rowsystem(CSV_DOC)
    rs2 = label_rowsystem(rs1, SPEC1, SEG)
    ref = LABELLED_WITH_SEGMENTS
    _comp(rs2, ref) 

def test_with_segments_by_file():
    fdict = get_testable_files_rs()    
    spec_filename = fdict['spec']
    cfg_filename =  fdict['cfg']
    
    default_spec = load_spec(spec_filename)
    segments = load_cfg(cfg_filename)

    rs1 = doc_to_rowsystem(CSV_DOC)
    rs2 = label_rowsystem(rs1, default_spec, segments)
    ref = LABELLED_WITH_SEGMENTS
    _comp(rs2, ref)
    remove_testable_files()

def test_folder_level_import():
    get_testable_files_rs()
    folder = os.path.dirname(os.path.realpath(__file__))
    rs = init_rowsystem_from_folder(folder)
    ref = LABELLED_WITH_SEGMENTS
    #import pdb; pdb.set_trace()
    _comp(rs, ref)
    remove_testable_files()

def test_folder_level_import_and_df_testing():
    get_testable_files_rs()
    folder = os.path.dirname(os.path.realpath(__file__))
    rs = init_rowsystem_from_folder(folder)
    df = get_annual_df(rs)
    # import pdb; pdb.set_trace()
    # MAYDO: fix lousy comparison below
    assert 'year' + DFA.to_csv() == df.to_csv()
    
    
# ----------------------------------------------------------------------
  
def _comp(rs, ref_rs):
    try:
        assert rs == ref_rs
    except:
        for i in range(len(rs)):
           print(i, rs[i] == ref_rs[i])
           print("Actual:")
           pprint(rs[i])
           print("Reference:")
           pprint(ref_rs[i])

# ----------------------------------------------------------------------
    
if __name__ == "__main__":
    #print("Main test:")
    test_main()
    #print("CSV import:")
    test_file_csv_import()
    #print("Segments by variables:")
    test_with_segments_by_var()
    #print("Segments by spec/cfg files:")
    test_with_segments_by_file()
    #
    test_folder_level_import()