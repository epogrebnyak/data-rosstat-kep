import kep.ini as ini
import kep.reader.access as reader
from kep.reader.parsing_definitions import ParsingDefinition

def test_spec_contains_main_and_additional_defintions():
    # main_def and more_def contain all parsing defintions 
    main_def = ParsingDefinition(path=ini.get_mainspec_filepath())
    more_def = [ParsingDefinition(path) for path in ini.get_additional_filepaths()]
    
    # *spec* replaces all definitions
    spec = reader.get_spec()
    assert spec.main == main_def
    assert spec.extras == more_def
    
# TODO (structurally importants): restore other tests for kep.reader from:
#    src\kep\reader\tests


if __name__ == "__main__":
    spec = reader.get_spec()