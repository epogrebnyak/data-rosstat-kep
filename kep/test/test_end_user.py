import pandas as pd

from kep.selector.end_user import date_to_tuple, get_ts, get_df

def test_date_to_tuple():
    assert date_to_tuple(2000)      ==  (2000, 1)
    assert date_to_tuple("2000")    ==  (2000, 1)
    assert date_to_tuple("2000-07") ==  (2000, 7)
    assert date_to_tuple("2000-1")  ==  (2000, 1)

def test_get_df_and_ts():
    z = get_ts('SOC_WAGE_rub','a', 2014)
    assert isinstance(z, pd.core.series.Series)
    assert z.iloc[0] == 32495

    e = get_df(['SOC_WAGE_rub', 'CPI_rog'], 'm', '2015-06', '2015-06')
    assert isinstance(e, pd.DataFrame)
    # WARNING: this is data revision - in ind06 this was 
    # assert e.iloc[0,0] == 35930.0
    # now in ind09 it is:
    assert e.iloc[0,0] == 35395
    assert e.iloc[0,1] == 100.2

if __name__ == "__main__":
    test_date_to_tuple()
    test_get_df_and_ts()