# -*- coding: utf-8 -*-
"""
Created on Sun May 28 02:07:16 2017

@author: EP
"""
import string
string.ascii_lowercase



def is_matched(pat, textline):
    if pat:
        return textline.startswith(pat)
    else:
        return False

def get_segment(stream, start, end):
    """Returns elements between [start, end) and remaining parts of *stream*.
    Recognises only first occurences."""
    remaining_stream = stream.copy()
    we_are_in_segment = False
    segment_lines = []
    for line in stream:
        if is_matched(start, line):
            we_are_in_segment = True
        if is_matched(end, line):
            we_are_in_segment = False
            break
        if we_are_in_segment:
            segment_lines.append(line)
            remaining_stream.pop(remaining_stream.index(line)) 
    return segment_lines, remaining_stream
            
stream = list("ab-123-c-456-def-000") #list(string.ascii_lowercase)

start = "b"
end = "c"
seg, remaining_stream = get_segment(stream, start, end) 
assert "".join(seg) == "b-123-"

start = "f"
end = None
seg, remaining_stream = get_segment(remaining_stream, start, end) 
assert "".join(seg) == "f-000"

seg, rs = get_segment(stream, None, None)
assert rs == stream
              