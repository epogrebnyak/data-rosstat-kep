from kep.inspection.var_check import get_varnames_not_in_db, get_complete_dicts

DATA_FOLDER = "data/2015/ind10"

def test_get_complete_dicts(data_folder = DATA_FOLDER):
    hdr, unit = get_complete_dicts(data_folder)
    assert 'CPI_FOOD' in [z[0] for z in hdr.values()]    

def test_import_complete(data_folder = DATA_FOLDER):
    # TODO: add config file to import 'PROFIT' 
    assert len(get_varnames_not_in_db(data_folder)) == 1
    assert get_varnames_not_in_db(data_folder) == ["PROFIT"]