from unittest import TestCase
from kep.file_io.common import get_var_abbr, get_unit_abbr
from kep.query.var_names import get_title, get_unit, FILLER, get_var_list_components
from kep.test.unittest.test_setup import update_database_to_current_month_folder

# using fixtures: implicitly - by get_var_list_components()
# warning: test depends on state on database, if current folder is imported


class TestQueryVarNames(TestCase):

    def test_get_var_abbr(self):
        self.assertEqual(get_var_abbr('PROD_E_TWh'),'PROD_E')

    def test_get_unit_abbr(self):
        self.assertEqual(get_unit_abbr('PROD_E_TWh'), 'TWh')

    def test_get_title(self):
        self.assertEqual(get_title('CONSTR_yoy'), 'Объем работ по виду деятельности "Строительство"')
        self.assertEqual(get_title('I_bln_rub'), 'Инвестиции в основной капитал')
        self.assertEqual(get_title('I_yoy'), 'Инвестиции в основной капитал')

    def test_get_unit(self):
        self.assertEqual(get_unit('CONSTR_yoy'), 'в % к аналог. периоду предыдущего года')

    def test_get_var_list_components_no_filler(self):
        update_database_to_current_month_folder()
        table = get_var_list_components()
        for row in table:
            self.assertNotEqual(row[0], FILLER)
            self.assertNotEqual(row[1], FILLER)