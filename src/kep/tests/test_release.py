import unittest
from kep.ini import get_path_csv_sample
from kep.release import get_pdef
from kep.reader.csv_data import csv_file_to_dicts
from kep.parser.emitter import Datapoints

testpoints_valid = [
    {'year': 2016, 'value': 85881.0, 'freq': 'a', 'varname': 'GDP__bln_rub'},
    {'year': 2016, 'value': 99.8, 'freq': 'a', 'varname': 'GDP__rog'},
    {'year': 2016, 'value': 101.3, 'freq': 'a', 'varname': 'IND_PROD__yoy'},
    {'year': 2016, 'value': 104.8, 'freq': 'a', 'varname': 'AGRO_PRODUCTION__yoy'},
    {'year': 2016, 'value': 13939.0, 'freq': 'a', 'varname': 'PROD_AGRO_MEAT__th_t'},
    {'year': 2016, 'value': 103.4, 'freq': 'a', 'varname': 'PROD_AGRO_MEAT__yoy'},
    {'year': 2016, 'value': 30724.0, 'freq': 'a', 'varname': 'PROD_AGRO_MILK__th_t'},
    {'year': 2016, 'value': 99.8, 'freq': 'a', 'varname': 'PROD_AGRO_MILK__yoy'},
    {'year': 2016, 'value': 43527.0, 'freq': 'a', 'varname': 'PROD_AGRO_EGGS__mln'},
    {'year': 2016, 'value': 102.2, 'freq': 'a', 'varname': 'PROD_AGRO_EGGS__yoy'},
    {'year': 2016, 'value': 5182.0, 'freq': 'a', 'varname': 'TRANS__bln_t_km'},
    {'year': 2016, 'value': 101.8, 'freq': 'a', 'varname': 'TRANS__yoy'},
    {'year': 2016, 'value': 5070.0, 'freq': 'a', 'varname': 'TRANS_COM__bln_t_km'},
    {'year': 2016, 'value': 101.8, 'freq': 'a', 'varname': 'TRANS_COM__yoy'},
    {'year': 2016, 'value': 1227.0, 'freq': 'a', 'varname': 'TRANS_RAILLOAD__mln_t'},
    {'year': 2016, 'value': 100.7, 'freq': 'a', 'varname': 'TRANS_RAILLOAD__yoy'},
    {'year': 2016, 'value': 14639.8, 'freq': 'a', 'varname': 'I__bln_rub'},
    {'year': 2016, 'value': 99.1, 'freq': 'a', 'varname': 'I__yoy'},
    {'year': 2016, 'value': 5689.6, 'freq': 'a', 'varname': 'I__bln_rub'},
    {'year': 2016, 'value': 6184.4, 'freq': 'a', 'varname': 'CONSTR__bln_rub_fix'},
    {'year': 2016, 'value': 95.7, 'freq': 'a', 'varname': 'CONSTR__yoy'},
    {'year': 2016, 'value': 79.8, 'freq': 'a', 'varname': 'DWELL__mln_m2'},
    {'year': 2016, 'value': 93.5, 'freq': 'a', 'varname': 'DWELL__yoy'},
    {'year': 2016, 'value': 60.66, 'freq': 'a', 'varname': 'RUR_USD__eop'},
    {'year': 2016, 'value': 63.81, 'freq': 'a', 'varname': 'RUR_EUR__eop'},
    {'year': 2016, 'value': 28137.1, 'freq': 'a', 'varname': 'RETAIL_SALES__bln_rub'},
    {'year': 2016, 'value': 94.8, 'freq': 'a', 'varname': 'RETAIL_SALES__yoy'},
    {'year': 2016, 'value': 1333.7, 'freq': 'a', 'varname': 'TURNOVER_CATERING__bln_rub'},
    {'year': 2016, 'value': 96.2, 'freq': 'a', 'varname': 'TURNOVER_CATERING__yoy'},
    {'year': 2016, 'value': 8377.8, 'freq': 'a', 'varname': 'RETAIL_USLUGI__bln_rub'},
    {'year': 2016, 'value': 99.7, 'freq': 'a', 'varname': 'RETAIL_USLUGI__yoy'},
    {'year': 2016, 'value': 104.5, 'freq': 'a', 'varname': 'PRICE_INDEX_LIVESTOCK_PRODUCTS__rog'},
    {'year': 2016, 'value': 21814.0, 'freq': 'a', 'varname': 'PROD_AGRO_MILK__th_t'},
    {'year': 2016, 'value': 103.2, 'freq': 'a', 'varname': 'PRICE_INDEX_INVESTMENT__rog'},
    {'year': 2016, 'value': 106.6, 'freq': 'a', 'varname': 'PRICE_INDEX_CONSTRUCTION__rog'},
    {'year': 2016, 'value': 105.6, 'freq': 'a', 'varname': 'PRICE_INDEX_CARGO_TRANSPORT__rog'},
    {'year': 2016, 'value': 105.4, 'freq': 'a', 'varname': 'CPI__rog'},
    {'year': 2016, 'value': 104.3, 'freq': 'a', 'varname': 'CPI_FOOD__rog'},
    {'year': 2016, 'value': 106.4, 'freq': 'a', 'varname': 'CPI_ALCOHOL__rog'},
    {'year': 2016, 'value': 4.2, 'freq': 'a', 'varname': 'SOC_UNEMPLOYED__bln'},
    {'year': 2016, 'value': 5.5, 'freq': 'a', 'varname': 'SOC_UNEMPLOYMENT_RATE__percent'},
    {'year': 2016, 'value': 956.0, 'freq': 'a', 'varname': 'SOC_UNEMPLOYED_REGISTERED__th'},
    {'year': 2016, 'value': 793.0, 'freq': 'a', 'varname': 'SOC_UNEMPLOYED_REGISTERED_BENEFITS__th'},
    {'year': 2016, 'value': 36746.0, 'freq': 'a', 'varname': 'SOC_WAGE__rub'},
    {'year': 2016, 'value': 107.8, 'freq': 'a', 'varname': 'SOC_WAGE__yoy'},
    {'year': 2016, 'value': 12391.1, 'freq': 'a', 'varname': 'SOC_PENSION__rub'},
    {'year': 2016, 'value': 30763.8, 'freq': 'a', 'varname': 'SOC_MONEY_INCOME_PER_CAPITA__rub'},
    {'year': 2016, 'value': 101.0, 'freq': 'a', 'varname': 'SOC_MONEY_INCOME_PER_CAPITA__yoy'},
    {'year': 2016, 'value': 94.4, 'freq': 'a', 'varname': 'SOC_REAL_MONEY_INCOME__yoy'},
    {'year': 2016, 'value': 94.1, 'freq': 'a', 'varname': 'HH_REAL_DISPOSABLE_INCOME__yoy'}
]

testpoints_invalid = [
    {'varname': 'PROD_AGRO_MEAT_yoy', 'freq': 'a', 'year': 2016, 'value': 30724.0},
    {'varname': 'PROD_AGRO_MEAT_yoy', 'freq': 'a', 'year': 2016, 'value': 99.8},
]

testpoint_1999 = {'freq': 'a', 'year': 1999, 'value': 4823.0, 'varname': 'GDP__bln_rub'}


class ActualDatapoints(unittest.TestCase):
    def setUp(self):
        csv_path = get_path_csv_sample(version=0).__str__()
        csv_dicts = csv_file_to_dicts(csv_path)
        pdef = get_pdef()
        self.d = Datapoints(csv_dicts, pdef)
        self.output = list(x for x in self.d.emit('a') if x['year'] == 2016)


class Test_ActualDatapoints_Array_Is_Long_Enough(ActualDatapoints):
    def test_positive(self):
        assert len(self.d.datapoints) > 21000


class Test_ActualDatapoints_Includes_First_Datapoint_1999_GDP(ActualDatapoints):
    def test_positive(self):
        assert self.d.is_included(testpoint_1999)
        assert self.d.datapoints[0] == testpoint_1999


class Test_Datapoints_Include_Many_Testpoints_for_2016(ActualDatapoints):
    def test_positive(self):
        for t in testpoints_valid:
            assert t in self.output

    def test_negative(self):
        for t in testpoints_invalid:
            assert t not in self.output


if __name__ == '__main__':
    unittest.main()
