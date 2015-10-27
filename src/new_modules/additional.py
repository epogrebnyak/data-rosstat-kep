# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 00:40:31 2015

@author: EP
"""

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

doc = """line 1
line 2 something
line 3
line 4 more of something
line 5
...
line 101
line 102
line 103"""

some_part_of_starter_line1 = "line 2 so"
some_part_of_finish_line1 =  "4 more"

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
     
S = [[None,                       None,                      "spec0.txt"], 
     [some_part_of_starter_line1, some_part_of_finish_line1, "spec1.txt"],
     ["line 101",                 "line 103",                "spec2.txt"]]
    
    
segs = [[s[0], s[1]] for s in S[1:]]
gen = stream_doc(doc)
out = emit_outside_segments(gen, segs)
outside_lines = ['line 1', 'line 4 more of something', 'line 5', '...', 'line 103']
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

                 
