from kep.inspection.var_check import get_varnames_not_in_db, get_complete_dicts
from kep.importer.csv2db import import_csv
from kep.paths import CURRENT_MONTH_DATA_FOLDER

# NOTE: get_complete_dicts() may be a part of file_io.specification
def test_get_complete_dicts(data_folder = CURRENT_MONTH_DATA_FOLDER):
    hdr, unit = get_complete_dicts(data_folder)
    assert 'CPI_FOOD' in [z[0] for z in hdr.values()] 
    # TODO: MUST CHANGE!
        

def test_import_complete(data_folder = CURRENT_MONTH_DATA_FOLDER):
    import_csv(data_folder, kill_existing_data = True)
    assert len(get_varnames_not_in_db(data_folder)) == 0
    # assert get_varnames_not_in_db(data_folder) == ["PROFIT"]
    # TODO: MUST CHANGE!