"""Handle variable label, consists of head and unit"""

import kep.common.label as label

def test_from_list_with_None_argument():
    assert label.from_list(["GDP", "rog"]) == label.Label("GDP", "rog")
    assert label.from_list(["IND"]) == label.Label("IND", None)