# -*- coding: utf-8 -*-
"""Compact representation of raw csv import and transformation controlled by yaml config files"""

def docstring_to_file(docstring, filename):
    with open(filename,"w") as f:
        f.write(docstring)

###############################################################################
# 1. INITIAL_DATA
doc = """line 1
line 2 something
line 3
line 4 more of something
line 5
line 101
line 102
line 103"""

DOC_investment = """1.7. Инвестиции в основной капитал1), млрд. рублей  / Fixed capital investments1), bln rubles																	
2014	13527,7	1863,8	2942,0	3447,6	5274,3	492,2	643,2	728,4	770,4	991,1	1180,5	1075,1	1168,5	1204,0	1468,5	1372,5	2433,3
в % к соответствующему периоду предыдущего года / percent of corresponding period of previous year																	
2014	97,3	94,7	98,1	98,5	97,2	92,7	95,5	95,3	97,4	97,3	99,3	99,1	98,4	98,1	99,2	92,2	98,9
в % к предыдущему периоду  / percent of previous period																	
2014		35,7	158,2	114,9	149,9	21,1	129,6	114,5	106,6	127,0	119,0	90,5	107,1	103,3	121,6	92,7	173,8"""
RAW_CSV_FILENAME = "_raw.csv"      
docstring_to_file(DOC_investment, RAW_CSV_FILENAME)


# 2.1. MAIN CONFIGURATION FILE
# Proxy for configuration file content
DOC_segment_info_yaml_filename = """spec0.txt
------
line 2 so
4 more
spec1.txt
------
line 101
line 103
spec2.txt
------"""
# Result of configuration file import
some_part_of_starter_line1 = "line 2 so"
some_part_of_finish_line1 =  "4 more"
DEFAULT_SPEC_FILE = "spec0.txt"
SEGMENTS = [[some_part_of_starter_line1, some_part_of_finish_line1, "spec1.txt"],
            ["line 101",                 "line 103",                "spec2.txt"]]
# 2.2. SEGMENT CONFIGURATION FILES
# spec0.txt
spec0_txt = """
"""

# spec1.txt
spec1_txt = """
"""
# 3. OUTPUT RESULTS
    
labelled_rows = [['VARNAME1', 'unit1', 101, 100.5, 100.2, 98.5],
                 ['VARNAME2', 'unit2',  50,    55,  45.3, 25.7]]
        
outside_lines = ['line 1', 'line 4 more of something', 'line 5', '...', 'line 103']

###############################################################################

def get_labelled_rows (raw_csv_filename, segment_info_yaml_filename):
    raw_rows = read_raw_csv(raw_csv_filename)
    segment_specs = get_segment_specs(segment_info_yaml_filename)
    default_spec  = get_default_spec(segment_info_yaml_filename)
    labelled_rows = label_raw_raws_by_spec(raw_rows, default_spec, segment_specs)    
    return labelled_rows 
    
def read_raw_csv(raw_csv_filename):
    pass    
    
# -----------------------------------------------
# Issue:...
def get_segment_spec(yaml_filename):
    # todo - add import from yaml file + make test function for this import
    return SEGMENTS 
    
def get_default_spec(yaml_filename):
    # todo - add import from yaml file + make test function for this import
    pass # DEFAULT_SPEC_FILE    
# -----------------------------------------------

read_raw_csv(RAW_CSV_FILENAME)





def label_raw_raws_by_spec(raw_rows, default_spec, segment_specs)


def stream_doc(doc):
    for y in doc.split("\n"):      
       yield y
   
def emit_segment(stream, starter_text, end_text):
    must_emit = False
    for current_row in stream:
        # accept entry of starter_text or end_text at any position
        if starter_text in current_row:
            must_emit = True
        if end_text in current_row:
            must_emit = False
        if must_emit:
            yield current_row


gen = stream_doc(doc)
seg = emit_segment(gen, some_part_of_starter_line1, some_part_of_finish_line1)
assert next(seg) == "line 2 something"
assert next(seg) == "line 3"

def emit_list(L):
    for y in L:
        yield y
    
def emit_outside_segments(gen, segments):
    as_list = [x for x in gen]
    for seg in segs:
        r = [x for x in emit_segment(as_list, seg[0], seg[1])]
        for g in r:
            as_list.remove(g)
    return emit_list(as_list)
for ol in outside_lines:
    assert next(out) == ol

# file, segmentation
# emit default segment with default config dictinaries
# emit other segments with their config dictinaries

accepts - stream, two dictionaries 
emits - rows with labels



def _yield_segment_from_stream(source_stream, start_line, end_line):
    pass

def _label_stream(stream, headline_dict, support_dict):
    return yield_row_with_labels(stream, headline_dict, support_dict)

def _label_segment(raw_stream, list_of_boundary_lines, list_of_specification_dicts):
    headline_dict = specification['headline']
    support_dict  = specification['support']
    # obtain filename
    f = get_raw_csv_filename(p)
    # open csv
    gen_in = yield_csv_rows(f)
    # read specification
    headline_dict, support_dict = load_spec(p)    
    # produce rows with labels
    return yield_row_with_labels(gen_in, headline_dict, support_dict)

                 
segs = [[s[0], s[1]] for s in S[1:]]
gen = stream_doc(doc)
out = emit_outside_segments(gen, segs)
