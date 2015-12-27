# -*- coding: utf-8 -*-
import os
from unittest import TestCase

from kep.file_io.common import docstring_to_file, delete_file
from kep.file_io.specification import load_spec, load_cfg

MUST_CLEANUP = False


class TestLoadSpecAndCfg(TestCase):

    DOC_SPEC = """# Configuration file
# 1. Names of special reader functions for some variables. Used for uncoventional tables. TO BE DEPRECIATED.
CPI : read12
---
# 2. Unit headers <-> unit names
в % к предыдущему периоду : rog
---
# 3. Main headers <-> variable names + default unit names
Инвестиции в основной капитал :
  - I
  - bln_rub"""

    CFG_SPEC = """- 3.5. Индекс потребительских цен
- 4. Социальная сфера
- spec_cpi.txt
---

- Производство транспортных средств и оборудования
- 1.7. Инвестиции в основной капитал
- spec_cpi.txt"""

    def test_spec(self):
        p = docstring_to_file(self.DOC_SPEC, "test_spec2.txt")
        print(p)
        header_dict, unit_dict = load_spec(p)
        self.assertEqual(header_dict, {"Инвестиции в основной капитал" : ["I", "bln_rub"]})
        self.assertEqual(unit_dict, {"в % к предыдущему периоду" : "rog"})
        if MUST_CLEANUP:
            delete_file(p)

    def test_cfg1(self):
        p = docstring_to_file(self.CFG_SPEC, "test_cfg2.txt")
        cfgs = load_cfg(p)
        print (cfgs)
        #assert cfgs[0][0] == "3.5. Индекс потребительских цен"
        #assert cfgs[1][2] == "_spec_1.txt"
        if MUST_CLEANUP:
            delete_file(p)


    def test_cfg2(self):
        p = docstring_to_file(self.DOC_SPEC, "test_spec3.txt")
        header_dict, unit_dict = load_spec(p)
        self.assertEqual(header_dict, {"Инвестиции в основной капитал" : ["I", "bln_rub"]})
        self.assertEqual(unit_dict,  {"в % к предыдущему периоду" : "rog"})
        if MUST_CLEANUP:
            delete_file(p)

if __name__ == "__main__":
   pass