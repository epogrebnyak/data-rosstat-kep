# FIXME: rename or relocate this.py

import kep.config as config
from kep.reader.csv_data import csv_file_to_dicts
from kep.reader.parsing_definitions import ParsingDefinition

def get_csv_data_and_definition():
    # csv data
    csv_path = config.get_default_csv_path()
    csv_dicts = list(csv_file_to_dicts(csv_path))
    # parsing definition
    spec_path = config.get_mainspec_filepath()
    parse_def = ParsingDefinition(path=spec_path)
    return csv_dicts, parse_def

# TODO: import several specs
# ----------------------------------------------------------------------
# import config
# from inputs.parsing_definitions import ParsingDefinition
#
# def get_definitions(folder=config.get_default_spec_folder()):
#     _path = config.get_main_spec_filepath(folder)
#     _path_list = config.get_additional_specs_filepaths(folder)
#     return {'default': ParsingDefinition(path=_path),
#            'additional': [ParsingDefinition(path) for path in _path_list]
#            }
# ----------------------------------------------------------------------