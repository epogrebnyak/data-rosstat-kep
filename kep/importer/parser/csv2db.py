# -----------------------------------------------------------------------
# wrapping 'parser' contents
from kep.importer.parser.label_csv import get_labelled_rows
from kep.importer.parser.stream import stream_flat_data

from kep.database.db import stream_to_database
from kep.file_io.common import get_filenames
from kep.database.db import wipe_db_tables

def to_database(raw_data_file, spec_file, cfg_file = None):
    lab_rows = get_labelled_rows(raw_data_file, spec_file, cfg_file)
    db_rows = stream_flat_data(lab_rows)
    stream_to_database(db_rows)

# -----------------------------------------------------------------------
# adding contents from other packages

def import_csv(data_folder, kill_existing_data = True):
    csv, spec, cfg = get_filenames(data_folder)
    if kill_existing_data:
        wipe_db_tables()
    to_database(csv, spec, cfg) 
    
 


