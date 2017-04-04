import yaml
import os
from pprint import pprint

from kep.config import PARSING_DEFINITIONS_FOLDER, DEFAULT_SPEC_FILE, SPEC_FILENAME_MUST_CONTAIN 
from kep.common import File

# -----------------------------------------------------------------------------
#
# Reminder about how YAML works
#
#assert yaml.load("""
#в % к соответствующему периоду предыдущего года : yoy
#""") == {"в % к соответствующему периоду предыдущего года" : "yoy"}
#           
#
#assert list(yaml.load_all("""
#a: 2
#---
#b: 3""")) == [{'a': 2}, {'b': 3}]
#
# -----------------------------------------------------------------------------


# Read parsing specification from yaml specfile or string.


def parse_spec_text(yaml_string):  
    
    content = list(yaml.load_all(yaml_string))
    return { 'scope': { 'start_line':  content[0]['start line'],
                          'end_line':  content[0]['end line']},
             'reader_func': content[0]['special reader'],
             'units':   content[1],
             'table_headers': content[2]
             }


SPEC_FILENAME_MUST_CONTAIN

    
def get_parsing_definition(yaml_filepath):
    yaml_string = File(yaml_filepath).read_text()
    return parse_spec_text(yaml_string)  
 

def get_default_definition():
    _f = os.path.join(PARSING_DEFINITIONS_FOLDER, DEFAULT_SPEC_FILE)
    return get_parsing_definition(_f) 
           
def get_specfiles_paths():    
    _dir = PARSING_DEFINITIONS_FOLDER    
    paths = [os.path.join(_dir,f) 
             for f in os.listdir(_dir)             
             if SPEC_FILENAME_MUST_CONTAIN in f
             and f != DEFAULT_SPEC_FILE]    
    return [p for p in paths if os.path.isfile(p)]


def get_definitions():
    return {'default': get_default_definition(),
            'additional': [get_parsing_definition(f) for f in get_specfiles_paths()]
            }

if __name__ == "__main__":
    pprint(get_definitions())




#
##------------------------------------------------------------------------------
#
#class File():
#    """File input-output operations with special handling of encoding and line ends.
#    
#    >>> File('temp.txt').save_text("abc").read_text()
#    'abc'
#    
#    >>> next(File('temp.txt').save_text('abc'+'\\n'+'def')._yield_lines())
#    'abc'
#    
#    >>> File('temp.txt').same_folder("c:/r.txt").filename
#    'c:/temp.txt'
#    
#    >>> File('temp.txt').remove()    
#    
#    """
#    # NOTE: use File('temp.txt').save_text('string') to save 'string' to file. 
#
#    ENCODING = 'utf8' 
#
#    def __init__(self, filename):
#        self.filename = filename
#        
#    def __repr__(self):
#        return os.path.normpath(self.filename)  
#            
#    def write_open(self):
#        return open(self.filename, 'w', encoding = self.ENCODING)
#        
#    def read_open(self):
#        if os.path.exists(self.filename):
#            return open(self.filename, 'r', encoding = self.ENCODING)
#        else:
#            raise FileNotFoundError(self.filename)  
#        
#    def save_text(self, docstring):
#        """Save *docstring* to current file and retrun filename."""
#        with self.write_open() as f:
#            f.write(docstring) 
#        return self
#        
#    def dump_iter(self, iterable):
#        """Write generator *iterable* into file"""    
#        with self.write_open() as csvfile:
#            filewriter = csv.writer(csvfile,  delimiter='\t', lineterminator='\n')
#            for row in iterable:        
#                 filewriter.writerow(row)
#        return self 
#        
#    def _yield_lines(self):
#        with self.read_open() as f:
#            for line in f:
#                if line.endswith('\n'):
#                     yield line[0:-1]
#                else:
#                     yield line            
#        
#    def read_text(self):
#        """Read text from file."""
#        return "\n".join(self._yield_lines())
#
#class UserInput():
#    """Reads from strings with content or from filenames.
#    
#    >>> UserInput('abc').content
#    'abc'
#    
#    >>> UserInput(File('temp.txt').save_text('content123').filename).content 
#    'content123'
#    
#    >>> File('temp.txt').remove()
#    
#    """
#    
#    def __init__(self, input):
#       """Reads *input* as string or filename, stores it in self.content"""
#       
#       def is_file(input):
#        
#            # protect against error 'filname too long' on Windows
#            try:
#                if os.path.exists(input):
#                    return True
#                else:
#                    return False
#            except:
#                return False
#       
#       if is_file(input):
#           filename = input       
#           self.content = File(filename).read_text()
#       elif isinstance(input, str):
#           self.content = input
#       else:
#           raise ValueError(input)
#
#class YAML():
#    """Read and parse YAML from file or string.
#    
#    >>> YAML('abc').content
#    ['abc']
#    
#    >>> YAML('- abc \\n- def\\n---\\n key_text : value_text').content
#    [['abc', 'def'], {'key_text': 'value_text'}]
#    
#    >>> YAML(File('temp.txt').save_text('- abc \\n- def\\n---\\n key_text : value_text').filename).content
#    [['abc', 'def'], {'key_text': 'value_text'}]
#    
#    >>> File('temp.txt').remove()  
#    
#    """  
#
#    def __init__(self, yaml_input):
#        """Parses *yaml_input* as string or filename, stores it in self.content."""    
#        yaml_string = UserInput(yaml_input).content
#        self.content = list(yaml.load_all(yaml_string))
#
#
#class Segment(YAML):
#    """Read parsing specification from yaml specfile or string.
#    
#Valid specification yaml looks like:
#    
#start line: null       # 'start_line'
#end line: null         # 'end_line'
#special reader: null   # 'reader_func'
#---
## 'unit_dict' section 
#"в процентах" : percent
#---
## 'header_dict' section 
#Varname header: 
# - VAR1
# - usd
# - 1.1 # section number
#Another header:
# - VAR2
# - rur
# - 1.2 # section number
#
#"""  
#
#    def self_check(self, yaml_input):
#        """Check specification data structure"""
#        try: 
#            # yaml was read as a list         
#            assert isinstance(self.content, list)
#            # yaml has 3 docs
#            assert len(self.content) == 3
#            # every doc is a dict
#            for part in self.content:
#                assert isinstance(part, dict)
#            # first doc has reserved keys 
#            for kw in ['start line', 'end line', 'special reader']:
#                assert self.content[0].keys().__contains__(kw)
#        except:
#            raise Exception("Wrong format for parsing specification.\nGiven: " + yaml_input[0:200] + "..." \
#                            + "\nParsed: " + self.content.__repr__()[0:200] + "...") 
#
#    def __init__(self, yaml_input):
#    
#        # parses yaml to 'self.content'
#        super().__init__(yaml_input)
#        
#        # checks input structrure
#        self.self_check(yaml_input)
#         
#        # assignment of attributes according to yaml structure
#        self.attrs = {'start_line':   self.content[0]['start line'],
#             'end_line':              self.content[0]['end line'],
#             'reader_func':           self.content[0]['special reader'],
#             'unit_dict':             self.content[1],
#             'header_dict':           self.content[2],
#             'head_labels':          [v[0] for v in self.content[2].values()]
#             }
#             
#    def __getattr__(self, name):
#        try:
#            return self.attrs[name]        
#        except KeyError:
#            raise AttributeError(name)
#
#    def __eq__(self, obj):
#         return self.content == obj.content
#         
#    def __repr__(self):
#        return self.content.__repr__()