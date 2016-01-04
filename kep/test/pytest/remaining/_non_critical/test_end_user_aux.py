import pandas as pd

from kep.query.end_user import date_to_tuple

def test_date_to_tuple():
    assert date_to_tuple(2000)      ==  (2000, 1)
    assert date_to_tuple("2000")    ==  (2000, 1)
    assert date_to_tuple("2000-07") ==  (2000, 7)
    assert date_to_tuple("2000-1")  ==  (2000, 1)

if __name__ == "__main__":
    test_date_to_tuple()
