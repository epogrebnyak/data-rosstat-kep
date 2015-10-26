# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 00:40:31 2015

@author: EP
"""

doc = """line 1
line 2 something
line 3
line 4 more of something
line 5
"""

some_part_of_starter_line = "line 2 so"
some_part_of_finish_line =  "4 more"

def stream_doc(doc):
    for y in doc.split("\n"):      
      yield y
      
gen = stream_doc(doc)

def emit_segment(stream, starter_text, end_text):
    for x in stream:
        yield x

seg = emit_segment(gen, some_part_of_starter_line, some_part_of_finish_line)
assert next(seg) == "line 2 something"
assert next(seg) == "line 3"