# -*- coding: utf-8 -*-
"""Read CSV file as stream of rows.

   Usage:
       gen =  CSV_Reader(path).yield_dicts()

"""

from kep.reader.files import File


def doc_to_lists(doc: str) -> list:
    """Splits string by EOL and tabs, returns list of lists."""
    return [r.split('\t') for r in doc.split('\n')]


def row_as_dict(row: list) -> dict:
    """Represents csv *row* content as a dictionary with 'head' and 'data' keys:
       'head' - string, first element in list *row* (year, table header or comment)
       'data' - list, next elements in list *row*,
                ususally data elements like ['15892', '17015', '18543', '19567']
    """
    return dict(head=row[0],
                data=row[1:])


def yield_rows_as_dicts(rows: list) -> iter:
    """Yield non-empty csv rows as dictionaries. """
    for r in rows:
        # check if list is not empty and first element is not empty
        if r and r[0]:
            yield row_as_dict(r)


def yield_dicts_from_file(path):
    doc = File(path).read_text()
    rows = doc_to_lists(doc)
    return yield_rows_as_dicts(rows)


def yield_dicts_from_string(doc):
    rows = doc_to_lists(doc)
    return yield_rows_as_dicts(rows)

# TODO: replace CSV_reader with below:

def csv_doc_to_dicts(doc):
    rows = doc_to_lists(doc)
    return yield_rows_as_dicts(rows)


def csv_file_to_dicts(path):
    doc = File(path).read_text()
    return csv_doc_to_dicts(doc)

# end todo


class StringReader():
    def __init__(self, doc: str):
        """Read tabular data from *doc* string."""
        self.rows = doc_to_lists(doc)

    def yield_dicts(self):
        """Use iterator to expose file contents."""
        return yield_rows_as_dicts(self.rows)


class CSV_Reader(StringReader):
    def __init__(self, path: str):
        """Read tabular data from *path* file"""
        doc = File(path).read_text()
        super().__init__(doc)