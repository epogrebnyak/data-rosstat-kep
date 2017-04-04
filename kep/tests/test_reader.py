# -*- coding: utf-8 -*-
from kep.reader.reader import SegmentState, Rows

heads = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9']
default_def = {'scope': {'end_line': None, 'start_line': None}, 'def': 0}   
alt_defs = [
        {'scope': {'start_line': 'h1', 'end_line': 'h4'}, 'def': "seg 1 h1-h3"}
      , {'scope': {'start_line': 'h4', 'end_line': 'h6'}, 'def': "seg 2 h4-h5"}
      , {'scope': {'start_line': 'h8', 'end_line': 'h9'}, 'def': "seg 3 h8"}]

a = SegmentState(default_def, alt_defs).assign_segments(heads)
hs = [(h, s['def']) for h, s in zip(heads, a)]

def test_segment_assignment():
    assert hs == [('h0', 0),
     ('h1', 'seg 1 h1-h3'),
     ('h2', 'seg 1 h1-h3'),
     ('h3', 'seg 1 h1-h3'),
     ('h4', 'seg 2 h4-h5'),
     ('h5', 'seg 2 h4-h5'),
     ('h6', 0),
     ('h7', 0),
     ('h8', 'seg 3 h8'),
     ('h9', 0)]    

b = SegmentState(default_def, []).assign_segments(heads)
hs2 = [(h, s['def']) for h, s in zip(heads, b)]

def test_no_additional_segments():
    assert hs2 == [('h0', 0),
     ('h1', 0),
     ('h2', 0),
     ('h3', 0),
     ('h4', 0),
     ('h5', 0),
     ('h6', 0),
     ('h7', 0),
     ('h8', 0),
     ('h9', 0)]
    
    
g = Rows()
         
def test_Rows():           
    assert type(g.specs[1000]) == dict
    assert len(g.rows) == len(g.specs)
    assert type(list(g.dicts())[1000]) == dict