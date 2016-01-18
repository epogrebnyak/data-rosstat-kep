from rowsystem.rowsystem import KEP
a = KEP()
a.__update__()
assert a.len() > 0 

from rowsystem.classes import CurrentMonthRowSystem 
c = CurrentMonthRowSystem()
assert c.__len__()['datapoints'] > 0 