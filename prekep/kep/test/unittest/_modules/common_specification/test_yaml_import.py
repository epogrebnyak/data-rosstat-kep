# -*- coding: utf-8 -*-

import yaml
from unittest import TestCase
from kep.file_io.common import docstring_to_file, yield_csv_rows, delete_file
from kep.file_io.specification import load_spec, get_yaml

class TestYamlImport(TestCase):
    #------------------------------------------------------------------------------
    # General testing of docstring_to_file() and _get_yaml()
    #------------------------------------------------------------------------------

    DOC_1 = """- Something looking like a yaml
- Но обязательно с русским текстом
---
key1 : with two documents
key2 : который будет глючить с кодировкой."""

    def test_io(self):
        p = docstring_to_file(self.DOC_1, "test_yaml_doc.txt")
        self.assertEqual(self.DOC_1, "\n".join([x[0] for x in yield_csv_rows(p)]))
        y = get_yaml(p)
        self.assertEqual(y[0][0], 'Something looking like a yaml')
        self.assertEqual(y[1]["key1"], 'with two documents')
        #delete_file(p)

    #------------------------------------------------------------------------------
    # YAML document structure testing
    #------------------------------------------------------------------------------

    doc_header = """1.7. Инвестиции в основной капитал :
  - I
  - bln_rub
1.14. Объем платных услуг населению :
  - Uslugi
  - bln_rub"""

    header_dict = {
    "1.7. Инвестиции в основной капитал":  ['I','bln_rub'],
    "1.14. Объем платных услуг населению": ['Uslugi','bln_rub']
     }

    # Unit labels
    doc_unit  = """в % к соответствующему периоду предыдущего года : yoy
в % к предыдущему периоду : rog"""
    unit_dict =    {
    "в % к соответствующему периоду предыдущего года": 'yoy',
    "в % к предыдущему периоду": 'rog'
    }

    # Special readers for some variables
    doc_reader = "CPI : read12"
    reader_dict = {'CPI' : 'read12'}

    ########### Test 1 - reading docs individually
    docs = [doc_reader, doc_unit, doc_header]
    dicts = [reader_dict, unit_dict, header_dict]

    def test_individial_docs_and_dicts(self):
        for _doc, _dict in zip(self.docs, self.dicts):
            self.assertEqual(yaml.load(_doc), _dict)

    ########### Test 2 - reading docs together

    comments = ["\n# Configuration file\n# 1. Names of special reader functions for some variables. Used for uncoventional tables."
               , "\n# 2. Unit headers <-> unit names"
               , "\n# 3. Main headers <-> variable names + default unit names"]
    comments_and_docs = ["\n".join([c,d]) for c, d in zip(comments, docs)]
    yaml_doc = "\n---\n".join(comments_and_docs)

    def test_in_one_doc(self):
        spec = list(yaml.load_all(self.yaml_doc))
        self.assertEqual(spec[0], self.reader_dict)
        self.assertEqual(spec[1], self.unit_dict)
        self.assertEqual(spec[2], self.header_dict)

    ########### Test 3 - reading docs as a file
    def test_with_file(self):
        filename = "_test_yaml_spec_sample.txt"
        p = docstring_to_file(self.yaml_doc, filename)

        d1, d2 = load_spec(p)
        self.assertEqual(d1, self.header_dict)
        self.assertEqual(d2, self.unit_dict)
        #delete_file(p)

if __name__ == "__main__":
    pass