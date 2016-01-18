from rowsystem.rowsystem import KEP

def test_kep():
    a = KEP()
    a.__update__()
    assert a.len() > 0 

def test_CMRS():
    from rowsystem.classes import CurrentMonthRowSystem 
    c = CurrentMonthRowSystem()
    assert c.__len__()['datapoints'] > 0 