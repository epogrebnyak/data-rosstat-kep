# kep.importer.parser.csv2db.import_csv() logic:
    # - reads specification files spec and cfg <- this is inspect_db().udf_vars 
    # - labels rows read from CSV file <- need check here
    # - flattens rows into stream <- need check here
    # - reads stream in database <- inspect_db() checks variables here

from kep.importer.parser.label_csv import get_labelled_rows
from kep.importer.parser.stream import stream_flat_data
from kep.database.db import stream_to_database
from kep.file_io.common import get_filenames

def slice_lab_rows(tag, lab_rows):
    for x in lab_rows:
        if x[0] == tag:
            yield x

def row_exists(tag, lab_rows):
    return len([x for x in slice_lab_rows('PROD_AUTO_TRUCKS_AND_CHASSIS', lab_rows)]) > 0 

def test_lab_rows():
    data_folder = "data/2015/ind10"
    csv, spec, cfg = get_filenames(data_folder)
    lab_rows = get_labelled_rows(csv, spec, cfg)
    assert row_exists('PROD_AUTO_TRUCKS_AND_CHASSIS', lab_rows)    