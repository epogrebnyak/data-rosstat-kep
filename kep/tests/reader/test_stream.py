from kep.reader.rs import CurrentMonthRowSystem

def test_var_stream():
   rs = CurrentMonthRowSystem()
   assert 0 != sum(abs(x['value']) for x in rs.named_dicts('GOV_CONSOLIDATED_DEFICIT_gdp_percent'))   


if __name__ == "__main__":
    test_var_stream()
    rs = CurrentMonthRowSystem()