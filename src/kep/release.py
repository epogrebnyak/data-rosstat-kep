"""
Locate directories:
    config.get_mainspec_filepath()

Get inputs:
    get parsing definition: get_pdef()
    get csv data:

Emit datapoints:


"""
import os

import kep.ini as ini
from kep.reader.csv_data import csv_file_to_dicts
from kep.reader.parsing_definitions import ParsingDefinition
from kep.parser.emitter import Datapoints


def get_pdef():
    """Get main parsing definition."""
    spec_path = ini.get_mainspec_filepath().__str__()
    return ParsingDefinition(path=spec_path)

    
def get_csv_dicts(year=None, month=None):
    """Get CSV data, defaults to latest locally available dataset."""
    if not year or not month:
        year, month = ini.get_latest()
    csv_path = ini.get_path_csv_data(year, month).__str__()
    return csv_file_to_dicts(csv_path)


if __name__ == "__main__":
    pdef = get_pdef()
    csv_dicts = get_csv_dicts()    
    
    # dataset
    d = Datapoints(csv_dicts, pdef)
    output = list(x for x in d.emit('a') if x['year']==2016) 

    def show_2016():
        for z in output:
            print(z.__repr__() + ",") 

    show_2016()