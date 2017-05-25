# -*- coding: utf-8 -*-
"""Test csv data import."""

import tempfile
from pathlib import Path
import types
import pytest

import kep.reader.csv_io as rio #(r)eader (io)

#  to_csv(rows, filepath)
#  from_csv(filepath)
#  csv_file_to_dicts(filepath)   

  
def __doc_to_rows__(doc):
    """Splits string by EOL and tabs, returns list of lists"""
    return [r.split('\t') for r in doc.split('\n')]

    
CSV_CONTENT = "2015\t99,2\t99,9\n2016\t101,3\t101,1"
ROWS = [['2015', '99,2', '99,9'], ['2016', '101,3', '101,1']] 
assert __doc_to_rows__(CSV_CONTENT) == ROWS
DICTS = [{'head': '2015', 'data': ['99,2', '99,9']},
         {'head': '2016', 'data': ['101,3', '101,1']}]
    
def __generate_temp_filename__():
    """Return valid local filepath. 
       Temp file is deleted, but filename remains valid."""
    with tempfile.NamedTemporaryFile("w") as tfile:
        fn = tfile.name
    return fn
    
@pytest.fixture
def csv_filename():
    filepath = __generate_temp_filename__()
    Path(filepath).write_text(CSV_CONTENT)
    yield filepath  
    Path(filepath).unlink()


@pytest.fixture
def temp_filename():
    filepath = __generate_temp_filename__()
    yield filepath  
    Path(filepath).unlink()
    
    
def test_from_csv_reads_reference_rows(csv_filename): 
    gen = rio.from_csv(csv_filename)
    assert isinstance(gen, types.GeneratorType)
    assert list(gen) == ROWS


def test_csv_as_dicts_reads_reference_dicts(csv_filename):
    gen = rio.csv_file_to_dicts(filepath=csv_filename)
    assert isinstance(gen, types.GeneratorType)
    assert list(gen)== DICTS 
               

_from = rio.from_csv
_to = rio.to_csv

    
def test_apply_from_and_to(csv_filename):                          
    gen = _from(_to(rows=ROWS, filepath=csv_filename))
    assert list(gen) == ROWS


def test_apply_to_and_from(csv_filename, temp_filename):
    gen = _from(csv_filename)
    _to(rows=gen, filepath=temp_filename)
    assert Path(temp_filename).read_text() == CSV_CONTENT + "\n"

        
@pytest.fixture
def real_csv_filename():
    from kep.ini import get_path_csv_sample
    return get_path_csv_sample(version=0).__str__()


def get_rows_and_dicts():
    fn = real_csv_filename()
    csv_rows = list(rio.from_csv(fn))
    csv_dicts = list(rio.csv_file_to_dicts(fn)) 
    return csv_rows, csv_dicts     

    
def test_real_data_reading_result_lengths_soft_check(real_csv_filename):
    csv_rows, csv_dicts = get_rows_and_dicts()
    assert len(csv_rows) > len(csv_dicts)


def test_real_data_reading_result_lengths_fixed_values_check(real_csv_filename):
    csv_rows, csv_dicts = get_rows_and_dicts()
    #  as get_path_csv_sample(version=0) points to a specific file, 
    #  we can keep len check fixed      
    assert len(csv_rows) == 4609
    assert len(csv_dicts) == 4386


if __name__ == "__main__":  
    pytest.main([__file__])
    
    csv_rows, csv_dicts = get_rows_and_dicts()
    assert len(csv_rows) == 4609
    assert len(csv_dicts) == 4386