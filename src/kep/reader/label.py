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
    
#TODO: label varname text to head, unit   
#todo: old tests for label

if __name__== "__main__":
    assert from_list(["GDP", "rog"]) == Label("GDP", "rog")
    assert from_list(["IND"]) == Label("IND", None)