from kep.file_io.common import get_var_abbr, get_unit_abbr
from kep.query.var_names import get_title, get_unit, FILLER, get_var_list_components

# from kep.test.pytest.test_setup import update_database_to_current_month_folder
# note: had unexpected error in conftest.py when trying to do this import below, cannot reproduce error now
from kep.database.db import update_database_to_current_month_folder


def test_get_var_abbr():
    assert get_var_abbr('PROD_E_TWh') == 'PROD_E'

def test_get_unit_abbr():
    assert get_unit_abbr('PROD_E_TWh') == 'TWh'

def test_get_title():
    assert get_title('CONSTR_yoy') == 'Объем работ по виду деятельности "Строительство"'
    assert get_title('I_bln_rub') == 'Инвестиции в основной капитал'
    assert get_title('I_yoy') == 'Инвестиции в основной капитал'

def test_get_unit():
    assert get_unit('CONSTR_yoy') == 'в % к аналог. периоду предыдущего года'

def test_get_var_list_components_no_filler():
    # warning: test depends on state on database, current folder must be imported
    update_database_to_current_month_folder()
    table = get_var_list_components()
    for row in table:
        assert row[0] != FILLER
        assert row[1] != FILLER
		

