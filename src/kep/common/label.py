"""Handle variable label, consists of head and unit"""

from collections import namedtuple

Label = namedtuple("Label", ['varname', 'unit'])

def from_list(_list):
    head = _list[0]
    try:
        unit = _list[1]
    except IndexError:
        unit = None
    return Label(head, unit)
    
#TODO: label varname text to head, unit using isupper 
#MAYDO: old tests for label

HEAD_UNIT_SEPARATOR = "__"

def to_text(varname, unit):
    if varname and unit:
         return varname + HEAD_UNIT_SEPARATOR + unit 
    else:
         return None

if __name__== "__main__":
    assert from_list(["GDP", "rog"]) == Label("GDP", "rog")
    assert from_list(["IND"]) == Label("IND", None)
    assert to_text("GDP", "rog") == "GDP__rog"