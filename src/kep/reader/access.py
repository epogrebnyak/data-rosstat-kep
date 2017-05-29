"""Read parsing definition and csv file."""

import kep.ini as ini
from kep.reader.csv_io import csv_file_to_dicts
from kep.reader.parsing_definitions import SegmentDefinition, Definition

# todo: integrate word2csv with kep.ini file location. Aim - generate many csv files for different days.
# todo: unzip/unrar word files 
# todo: move Tempfile to tests

def get_pdef():
    """Return parsing definition."""
    spec_path = ini.get_mainspec_filepath().__str__()
    return SegmentDefinition(path=spec_path)

def get_spec():
    """Return extended parsing definition."""
    return Definition(path=ini.get_mainspec_filepath(), 
                      pathlist=ini.get_additional_filepaths())       

def __get_csv_path__(year=None, month=None):
    if not year or not month:
        year, month = ini.get_latest()
    return ini.get_path_csv_data(year, month).__str__()    
    
def get_csv_dicts(year=None, month=None):
    """Get CSV data. Defaults to most recent locally saved dataset."""
    csv_path = __get_csv_path__(year, month)
    return csv_file_to_dicts(csv_path)

if __name__ == "__main__":
    csv_dicts = get_csv_dicts()
    spec = get_spec()  
    
    for pdef in spec.extras:
        for s,e in pdef.start_and_end_lines():
            print (s,e)