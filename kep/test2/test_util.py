from kep.util import Seq

def test_seq_with_duplicates ():
    test_seq_with_duplicates = ["a", "a", "a", "b"]
    t = Seq(test_seq_with_duplicates)
    assert t == test_seq_with_duplicates
    #assert t.__occurences__ == {'a': 3, 'b': 1}
    assert t.duplicates == ['a']
    assert t.unique == ['a', 'b']
    assert t.has_duplicates() is True   
                           
def ttest_seq_no_duplicates():                           
    test_seq_no_duplicates = ["a", "b", "c"]
    z = Seq(test_seq_no_duplicates)
    assert z.duplicates == []
    assert z.has_duplicates() is False