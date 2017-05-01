import kep.config as config
from kep.reader.csv_data import csv_file_to_dicts
from kep.reader.parsing_definitions import ParsingDefinition
from kep.parser.emitter import Datapoints

def get_pdef():
    """Get main parsing definition"""
    spec_path = config.get_mainspec_filepath()
    return ParsingDefinition(path=spec_path)

def get_csv_dicts(year, month):
    """Get CSV data"""
    # TODO: make use of year, months
    if not is_valid_year(year) or is_valid_month(month):
        raise ValueError("Cannot accept date: {}.{}".format(month,year))
    csv_path = config.get_default_csv_path()
    return list(csv_file_to_dicts(csv_path))

# TODO: move this elsewhere
def get_mock_csv_dicts(version=0):
    """Get mock CSV data for testing"""
    if version == 0:
        csv_path = config.get_default_csv_path()
        return list(csv_file_to_dicts(csv_path))    
        
    
def is_valid_year(year):
    # TODO: stub, write code here 
    return True


def is_valid_month(month):
    # TODO: stub, write code here     
    return True   
    

if __name__ == "__main__":
    year = month = None
    # TODO: make failing test for year, month
    csv_dicts = get_csv_dicts(year, month)
    pdef = get_pdef()
    
    # dataset
    d = Datapoints(csv_dicts, pdef)
    output = list(x for x in d.emit('a') if x['year']==2016) 

    def show_2016():
        for z in output:
            print(z.__repr__() + ",") 

    show_2016()   

    # NEXT:
    # Kill this.py + check usage in kep.parser
    # Remove reader.py (leave todos/requirements + some code in 'main' in this module)
    # Compare pdef unique varname heads to Datapoints varname heads
    #     - Datapoints varname heads
    #     - pdef unique varname heads
    #     - print both
    #     - diff on list
    #     - find in file
    #     - decide why not imported +  fix specs? 
    #     - think of test
    # Pdef issues
    # More tabs issues
    # Guide to code review  