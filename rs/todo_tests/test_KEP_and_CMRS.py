from rowsystem.rowsystem import KEP

a = KEP()
a.__update__()

def test_kep():
    assert a.len() > 0 
    dfm = a.monthly_df()
    dfa = a.annual_df()
    dfq = a.quarter_df()
    

def test_fiscal_inidciators_present():
    #WARNING: labels do not quarantee proper data in dataset  
    for lab in ['GOV_CONSOLIDATED_EXPENSE_ACCUM', 'GOV_CONSOLIDATED_REVENUE_ACCUM', 
                'GOV_FEDERAL_EXPENSE_ACCUM', 'GOV_FEDERAL_REVENUE_ACCUM', 'GOV_FEDERAL_SURPLUS_ACCUM', 
                'GOV_SUBFEDERAL_EXPENSE_ACCUM', 'GOV_SUBFEDERAL_REVENUE_ACCUM', 'GOV_SUBFEDERAL_SURPLUS_ACCUM']:
        assert lab in a.get_saved_head_labels()  
    
def test_CMRS():
    from rowsystem.classes import CurrentMonthRowSystem 
    c = CurrentMonthRowSystem()
    assert c.__len__()['datapoints'] > 0 