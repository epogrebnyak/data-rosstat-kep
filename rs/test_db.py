from db import TrialDatabase

def sample_iter():
    yield {'value': None, 'freq': None, 'month': None, 'val': 65000, 'year': 2014, 'varname': 'GDP_rub', 'qtr': None}
    yield {'value': None, 'freq': None, 'month': None, 'val': 62000, 'year': 2013, 'varname': 'GDP_rub', 'qtr': None}

def test_DefaultDatabase():        
    test_db = TrialDatabase(sample_iter())
    assert list(sample_iter()) == list(test_db.get_stream())

