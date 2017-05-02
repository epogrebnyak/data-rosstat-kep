import unittest
from kep.release import get_actual_csv_dicts_for_testing, get_pdef
from kep.parser.emitter import Datapoints

testpoints_valid = [
{'varname': 'GDP_bln_rub', 'year': 2016, 'value': 85881.0},
{'varname': 'GDP_rog', 'year': 2016, 'value': 99.8},
{'varname': 'IND_PROD_yoy', 'year': 2016, 'value': 101.3},
{'varname': 'AGRO_PRODUCTION_yoy', 'year': 2016, 'value': 104.8},
{'varname': 'PROD_AGRO_MEAT_th_t', 'year': 2016, 'value': 13939.0},
{'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 103.4},
{'varname': 'PROD_AGRO_MILK_th_t', 'year': 2016, 'value': 30724.0},
{'varname': 'PROD_AGRO_MILK_yoy', 'year': 2016, 'value': 99.8},
{'varname': 'PROD_AGRO_EGGS_mln', 'year': 2016, 'value': 43527.0},
{'varname': 'PROD_AGRO_EGGS_yoy', 'year': 2016, 'value': 102.2},
{'varname': 'TRANS_bln_t_km', 'year': 2016, 'value': 5182.0},
{'varname': 'TRANS_yoy', 'year': 2016, 'value': 101.8},
{'varname': 'TRANS_COM_bln_t_km', 'year': 2016, 'value': 5070.0},
{'varname': 'TRANS_COM_yoy', 'year': 2016, 'value': 101.8},
{'varname': 'TRANS_RAILLOAD_mln_t', 'year': 2016, 'value': 1227.0},
{'varname': 'TRANS_RAILLOAD_yoy', 'year': 2016, 'value': 100.7},
{'varname': 'I_bln_rub', 'year': 2016, 'value': 14639.8},
{'varname': 'I_yoy', 'year': 2016, 'value': 99.1},
{'varname': 'I_bln_rub', 'year': 2016, 'value': 5689.6},
{'varname': 'CONSTR_bln_rub_fix', 'year': 2016, 'value': 6184.4},
{'varname': 'CONSTR_yoy', 'year': 2016, 'value': 95.7},
{'varname': 'DWELL_mln_m2', 'year': 2016, 'value': 79.8},
{'varname': 'DWELL_yoy', 'year': 2016, 'value': 93.5},
{'varname': 'RUR_USD_eop', 'year': 2016, 'value': 60.66},
{'varname': 'RUR_EUR_eop', 'year': 2016, 'value': 63.81},
{'varname': 'RETAIL_SALES_bln_rub', 'year': 2016, 'value': 28137.1},
{'varname': 'RETAIL_SALES_yoy', 'year': 2016, 'value': 94.8},
{'varname': 'TURNOVER_CATERING_bln_rub', 'year': 2016, 'value': 1333.7},
{'varname': 'TURNOVER_CATERING_yoy', 'year': 2016, 'value': 96.2},
{'varname': 'RETAIL_USLUGI_bln_rub', 'year': 2016, 'value': 8377.8},
{'varname': 'RETAIL_USLUGI_yoy', 'year': 2016, 'value': 99.7},
{'varname': 'PRICE_INDEX_LIVESTOCK_PRODUCTS_rog', 'year': 2016, 'value': 104.5},
{'varname': 'PROD_AGRO_MILK_th_t', 'year': 2016, 'value': 21814.0},
{'varname': 'PRICE_INDEX_INVESTMENT_rog', 'year': 2016, 'value': 103.2},
{'varname': 'PRICE_INDEX_CONSTRUCTION_rog', 'year': 2016, 'value': 106.6},
{'varname': 'PRICE_INDEX_CARGO_TRANSPORT_rog', 'year': 2016, 'value': 105.6},
{'varname': 'CPI_rog', 'year': 2016, 'value': 105.4},
{'varname': 'CPI_FOOD_rog', 'year': 2016, 'value': 104.3},
{'varname': 'CPI_ALCOHOL_rog', 'year': 2016, 'value': 106.4},
{'varname': 'SOC_UNEMPLOYED_bln', 'year': 2016, 'value': 4.2},
{'varname': 'SOC_UNEMPLOYMENT_RATE_percent', 'year': 2016, 'value': 5.5},
{'varname': 'SOC_UNEMPLOYED_REGISTERED_th', 'year': 2016, 'value': 956.0},
{'varname': 'SOC_UNEMPLOYED_REGISTERED_BENEFITS_th', 'year': 2016, 'value': 793.0},
{'varname': 'SOC_WAGE_rub', 'year': 2016, 'value': 36746.0},
{'varname': 'SOC_WAGE_yoy', 'year': 2016, 'value': 107.8},
{'varname': 'SOC_PENSION_rub', 'year': 2016, 'value': 12391.1},
{'varname': 'SOC_MONEY_INCOME_PER_CAPITA_rub', 'year': 2016, 'value': 30763.8},
{'varname': 'SOC_MONEY_INCOME_PER_CAPITA_yoy', 'year': 2016, 'value': 101.0},
{'varname': 'SOC_REAL_MONEY_INCOME_yoy', 'year': 2016, 'value': 94.4},
{'varname': 'HH_REAL_DISPOSABLE_INCOME_yoy', 'year': 2016, 'value': 94.1}
]

testpoints_invalid = [
    {'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 30724.0},
    {'varname': 'PROD_AGRO_MEAT_yoy', 'year': 2016, 'value': 99.8},
]

class DatapointsFromActualDataset(unittest.TestCase):

    def setUp(self):
        csv_dicts = get_actual_csv_dicts_for_testing()
        pdef = get_pdef()
        self.d = Datapoints(csv_dicts, pdef)
        self.output = list(x for x in self.d.emit('a') if x['year']==2016) 

class TestDatapoints_Array_Length_Long_Enough(DatapointsFromActualDataset):
    def test_positive(self):
        assert len(self.d.datapoints) > 21000

class TestDatapoints_Includes_FirstDatapoint(DatapointsFromActualDataset):
    def test_positive(self):
        _dict = {'freq': 'a', 'value': 4823.0, 'varname': 'GDP_bln_rub', 'year': 1999}
        assert self.d.is_included(_dict)
        assert self.d.datapoints[0] == _dict

class TestDatapoints_Include_ManyDatapoints_for_2016_Annual_Data(DatapointsFromActualDataset):
    def test_positive(self):
        for t in testpoints_valid:
            assert t in self.output

    def test_negative(self):
        for t in testpoints_invalid:
            assert t not in self.output

if __name__ == '__main__':  
    unittest.main()