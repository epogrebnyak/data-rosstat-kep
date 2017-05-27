import os
from pathlib import Path

import kep.ini as ini

def test_get_path_csv_file_exists():
    assert os.path.exists(ini.get_path_csv_sample(version=0).__str__())
    assert os.path.exists(ini.get_path_csv_data(year=2017, month=2).__str__())

    
def test_get_path_csv_same_file_returned():    
    csv1 = ini.get_path_csv_sample(version=0).open(encoding='utf-8').readlines()
    csv2 = ini.get_path_csv_data(year=2017, month=2).open(encoding='utf-8').readlines()
    assert csv1 == csv2
    
    
def test_get_mainspec_file_exists():
    assert os.path.exists(ini.get_mainspec_filepath().__str__())
    
    
def test_locate_additional_specs_file_exists():
    additional_specfiles = ['__spec_budget_expense.txt', '__spec_budget_revenue.txt', '__spec_budget_surplus.txt',
                            '__spec_cpi.txt', '__spec_foreign_trade.txt', '__spec_invest_src.txt', '__spec_overdue.txt',
                            '__spec_profit.txt', '__spec_receivable.txt', '__spec_retail.txt']
    for f in ini.get_additional_filepaths():
        name = Path(f).name
        assert name in additional_specfiles
        additional_specfiles.remove(name)
    assert additional_specfiles == []
    
def test_max_year_returns_2017_or_greater():
    assert ini.RawDataLocations(ini.rosstat_folder).max_year() >= 2017

def test_max_month_is_in_1_12_range():
    m = ini.RawDataLocations(ini.rosstat_folder).max_month()
    assert m >= 1 and m <=12