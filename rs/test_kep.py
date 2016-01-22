from kep import KEP

# tests interfere with default database, .save initiated somewhere  
kep = KEP()
kep.__update_from_current_month__()

def test_current_month_row_system():
    assert kep.len() > 0 

def test_kep():
    dfm = kep.monthly_df()
    dfa = kep.annual_df()
    dfq = kep.quarter_df()
    # somethign else here - maybe from final use examples?    

def test_fiscal_inidciators_present():
    #WARNING: labels do not quarantee proper data in dataset  
    for lab in ['GOV_CONSOLIDATED_EXPENSE_ACCUM', 'GOV_CONSOLIDATED_REVENUE_ACCUM', 
                'GOV_FEDERAL_EXPENSE_ACCUM', 'GOV_FEDERAL_REVENUE_ACCUM', 'GOV_FEDERAL_SURPLUS_ACCUM', 
                'GOV_SUBFEDERAL_EXPENSE_ACCUM', 'GOV_SUBFEDERAL_REVENUE_ACCUM', 'GOV_SUBFEDERAL_SURPLUS_ACCUM']:
        assert lab in kep.get_saved_head_labels() 
   
if '__main__' == __name__:   
   pass # kep.publish()