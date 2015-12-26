import pandas as pd

from kep.query.end_user import get_ts, get_df
from kep.importer.csv2db import import_csv
from kep.paths import CURRENT_MONTH_DATA_FOLDER

# fixture: implicit - import_csv(CURRENT_MONTH_DATA_FOLDER), may be a function at start of module + split test to two functions
def test_get_df_and_ts():
    import_csv(CURRENT_MONTH_DATA_FOLDER)
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
    test_get_df_and_ts()