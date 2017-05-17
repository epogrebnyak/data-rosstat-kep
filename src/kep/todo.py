# -*- coding: utf-8 -*-

import kep.reader.access as reader
pdef = reader.get_pdef()
csv_dicts = list(reader.get_csv_dicts())   

# problem 1 - must introduce additional parsing defintions 
#             to Block class, get_blocks and Datapoints 

print("""PROBLEM 1: 

    We have several additional parsing definitions which apply to
    segments of csv file (from start line to end line).
    
    We can import these defintions as in *more_def* , but they are never
    used in containers.py when parsing table headers.

    When dealing with segments of csv file, only a single parsing definition 
    aplies to a segment, it is either main spec or some additional spec.

    For previous implementatoin see SegmentState class in 
    https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/reader/reader.py#L29-L85
    
        SegmentState(default_spec, other_specs).assign_segments(heads)

    was used to assign parsing definition to each segment.
    
    Maybe in containers.py we can also walk by table headers and assing a parsing
    definition to each table. 
    
    Block().textrows
           .datarows
           .parsing_defintion
           
    Block().yield_datapoints()       
""")

import kep.ini as ini
from kep.reader.parsing_definitions import ParsingDefinition
# main_def and more_def contain all parsing defintions 
main_def = ParsingDefinition(path=ini.get_mainspec_filepath())
more_def = [ParsingDefinition(path) for path in ini.get_additional_filepaths()]
all_def = main_def + more_def 

# read blocks
import kep.parser.containers as containers  

blocks = containers.get_blocks(csv_dicts, pdef)
#for b in blocks:
#    containers.uprint(b)
#    print('\n')
containers.show_stats(blocks, pdef)

# TODO 1:
# - Block class must have .pdef property 
# - assign main pdef to all tables
# - make assign_parsing_definitions() to allocate additional pdefs
# - emitter.Datapoints(csv_dicts, pdef_main, pdef_additionals=None)
#   when Block has label it is defined






# NOT TODO: early detect duplicates 
#varnames = [(b.label, i) for i,b in enumerate(blocks) if b.label is not None]