import pytest
from kep.common.seq import Seq

def test_seq_with_duplicates ():
    test_seq_with_duplicates = ["a", "a", "a", "b"]
    t = Seq(test_seq_with_duplicates)
    assert t == test_seq_with_duplicates
    assert t.duplicates == ['a']
    assert t.unique == ['a', 'b']
    assert t.has_duplicates() is True   
                           
def test_seq_no_duplicates():                           
    test_seq_no_duplicates = ["a", "b", "c"]
    z = Seq(test_seq_no_duplicates)
    assert z.duplicates == []
    assert z.has_duplicates() is False

if __name__ == "__main__":
    pytest.main(__file__)