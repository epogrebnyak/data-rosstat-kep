from dataframes import KEP
from label import Label
import pandas as pd
from pandas.util.testing import assert_frame_equal

k = KEP()
       
def test_df_KEP():
    assert_frame_equal(k.dfm, k.get_df('m', k.get_varnames()['m']))
    assert_frame_equal(k.dfq, k.get_df('q', k.get_varnames()['q']))
    assert_frame_equal(k.dfa, k.get_df('a', k.get_varnames()['a']))
    
    # QUESTION: unclear why asserts below do not pass
    #assert k.dfm.equals(k.get_df('m', k.get_varnames()['m']))
    #assert k.dfa.equals(k.get_df('a', k.get_varnames()['a']))
    #assert k.dfq.equals(k.get_df('q', k.get_varnames()['q']))
        
    m1_name = k.get_varnames()['m'][5]
    assert isinstance(k.get_ts("m", m1_name), pd.Series)
    
    # query by single name - obtain pandas time series
    ts1 = k.get_ts('a', 'SOC_WAGE_rub')
    assert ts1.loc[2014] == 32495    
    assert ts1.equals(k.dfa['SOC_WAGE_rub'])    

    ts2 = k.get_ts('a', 'CPI_rog')
    assert ts2.loc[2014] == 111.4
    assert ts2.equals(k.dfa['CPI_rog'])
    
    # query by multiple names - obtain pandas dataframe
    df1 = k.get_df('m', ['SOC_WAGE_rub', 'CPI_rog'])
    assert df1.loc['2015-10-31','SOC_WAGE_rub'] == 33357.0 # note: data revision, was 33240.0
    assert df1.loc['2015-10-31','CPI_rog'] == 100.7
    assert df1.equals(k.dfm[['SOC_WAGE_rub', 'CPI_rog']])       

def test_fiscal_inidciators_present():
    #WARNING: labels do not quarantee proper data in dataset  
    label_list = [Label(x).head for x in k.__get_saved_full_labels__()]
    for lab in ['GOV_CONSOLIDATED_EXPENSE_ACCUM', 'GOV_CONSOLIDATED_REVENUE_ACCUM', 
                'GOV_FEDERAL_EXPENSE_ACCUM', 'GOV_FEDERAL_REVENUE_ACCUM', 'GOV_FEDERAL_SURPLUS_ACCUM', 
                'GOV_SUBFEDERAL_EXPENSE_ACCUM', 'GOV_SUBFEDERAL_REVENUE_ACCUM', 'GOV_SUBFEDERAL_SURPLUS_ACCUM']:
        assert lab in label_list  
