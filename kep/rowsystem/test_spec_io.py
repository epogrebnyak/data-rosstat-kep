from spec_io import write_file
from spec_io import load_cfg, load_spec


def fcomp(doc, var, loader_func, fname = None):
    if fname is None:
        fname = "temp.txt"
    path = write_file(fname, doc)
    assert loader_func(path) == var

spec_dict = ({'table headline B': ['var_B', 'main_unit_abbr_for_B'], 'table headline A': ['var_A', 'main_unit_abbr_for_A']} 
            ,{'unit of measurement 2': 'unit_abbr2', 'unit of measurement 1': 'unit_abbr1'} 
            ,{'special reader': None, 'end line': None, 'start line': None})

spec_txt = """
# segment information
start line : null
end line : null
special reader: null

---
# units (several)
unit of measurement 1: unit_abbr1
unit of measurement 2: unit_abbr2

---
# headlines (many lines)
table headline A:
   - var_A
   - main_unit_abbr_for_A
table headline B:
   - var_B
   - main_unit_abbr_for_B
"""

spec_filename = 'spec.txt'

cfg_txt ="""
- {0}
- {0}""".format(spec_filename)

cfg_list = [[None, None, ({'table headline B': ['var_B', 'main_unit_abbr_for_B'], 'table headline A': ['var_A', 'main_unit_abbr_for_A']}, {'unit of measurement 2': 'unit_abbr2', 'unit of measurement 1': 'unit_abbr1'}, {'special reader': None, 'end line': None, 'start line': None})],
            [None, None, ({'table headline B': ['var_B', 'main_unit_abbr_for_B'], 'table headline A': ['var_A', 'main_unit_abbr_for_A']}, {'unit of measurement 2': 'unit_abbr2', 'unit of measurement 1': 'unit_abbr1'}, {'special reader': None, 'end line': None, 'start line': None})]]

def test_spec():
    fcomp(spec_txt, spec_dict, load_spec, spec_filename)

def test_cfg():
    write_file(spec_filename, spec_txt)
    fcomp(cfg_txt, cfg_list, load_cfg, "cfg.txt")
    
test_spec()
test_cfg()




