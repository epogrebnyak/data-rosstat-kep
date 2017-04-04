from kep.reader.stream import split_row_fiscal

def test_split():
    test_row = "1999	653,8	22,7	49,2	91,5	138,7	185,0	240,0	288,5	345,5	400,6	454,0	528,0".split('\t')
    assert split_row_fiscal(test_row) == (1999, '653,8', ['49,2', '185,0', '345,5', '653,8'], ['22,7', '49,2', '91,5', '138,7', '185,0', '240,0', '288,5', '345,5', '400,6', '454,0', '528,0', '653,8'])

    
    
    
from kep.reader.rs import CurrentMonthRowSystem

def test_var_stream():
   rs = CurrentMonthRowSystem()
   assert 0 != sum(abs(x['value']) for x in rs.named_dicts('GOV_CONSOLIDATED_DEFICIT_gdp_percent'))   


if __name__ == "__main__":
    test_var_stream()
    rs = CurrentMonthRowSystem()