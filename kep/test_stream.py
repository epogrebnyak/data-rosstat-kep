from rs import CurrentMonthRowSystem

def test_var_stream():
   cmrs = CurrentMonthRowSystem()
   assert 0 != sum(abs(x['value']) for x in cmrs.named_dicts('GOV_CONSOLIDATED_DEFICIT_gdp_percent'))   
