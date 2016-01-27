"""Access to program inputs (files or text strings)."""

# --------------------------------------------------------------------------------
#
#  Classes:
#    Folder, CurrentFolder - navigating filesystem
#    File, TempfolderFile - occasionally used for writing data in tests 
#    UserInput, CSV, YAML - reading tabular raw data and specification for parsing.
#
#  Classes have docstring tests, runable by 'nosetests inputs.py --with-doctest' 
#
# --------------------------------------------------------------------------------

import os
import yaml
import csv

class Folder():
    """Manipulation of folder paths. Can be used to point to current or parent folders.
    
    >>> Folder('c:/root/project').path
    'c:/root/project'
    
    >>> Folder('c:/root/project').up(2)
    c:\\
    
    >>> Folder('c:/root/project').up(2).join('data').__repr__()
    'c:\\\\data'
    
    >>> Folder('c:/root/project').cd('/dev/null')
    \\dev\\null
    
    """

    
    @staticmethod
    def get_cwd():        
        return os.getcwd()
        
    @staticmethod
    def current__file__folder():
        curpath = os.path.realpath(__file__)
        return os.path.dirname(curpath)

    @staticmethod
    def exists(path):
        if os.path.isdir(path):
            return True
        else:
            raise FileNotFoundError(path)        
        
    def up(self, n = 1):
        for i in range(n):
            self.path = os.path.split(self.path)[0]
        return self 
        
    def join(self, *folders):
        self.path = os.path.join(self.path, *folders)
        return self         
        
    def cd(self, path, must_create = False):
        """Change directory and create it if does not exist"""
        if not os.path.isdir(path) and must_create:
             os.makedirs(path)
        self.path = path
        return self
    
    def __init__(self, folder): 
        self.cd(folder)
        
    def __repr__(self):
        return os.path.normpath(self.path)
        
class CurrentFolder(Folder):
    """Current folder class, storing path where this file is located."""
            
    def __init__(self):
        if __file__:    
            self.path = self.current__file__folder()
        else:
            # NOTE: must have __file__ property to work. 
            raise Exception ("Not a script, __file__ not found.")        
        
class File():
    """File input-output operations with special handling of encoding and line ends.
    
    >>> File('temp.txt').save_text("abc").read_text()
    'abc'
    
    >>> next(File('temp.txt').save_text('abc'+'\\n'+'def')._yield_lines())
    'abc'
    
    >>> File('temp.txt').same_folder("c:/r.txt").filename
    'c:/temp.txt'
    
    >>> File('temp.txt').remove()    
    
    """
    # NOTE: use File('temp.txt').save_text('string') to save 'string' to file. 

    ENCODING = 'utf8' 

    def __init__(self, filename):
        self.filename = filename
        
    def __repr__(self):
        return os.path.normpath(self.filename)  
            
    def write_open(self):
        return open(self.filename, 'w', encoding = self.ENCODING)
        
    def read_open(self):
        if os.path.exists(self.filename):
            return open(self.filename, 'r', encoding = self.ENCODING)
        else:
            raise FileNotFoundError(self.filename)  
        
    def save_text(self, docstring):
        """Save *docstring* to current file and retrun filename."""
        with self.write_open() as f:
            f.write(docstring) 
        return self
        
    def dump_iter(self, iterable):
        """Write generator *iterable* into file"""    
        with self.write_open() as csvfile:
            filewriter = csv.writer(csvfile,  delimiter='\t', lineterminator='\n')
            for row in iterable:        
                 filewriter.writerow(row)
        return self 
        
    def _yield_lines(self):
        with self.read_open() as f:
            for line in f:
                if line.endswith('\n'):
                     yield line[0:-1]
                else:
                     yield line            
        
    def read_text(self):
        """Read text from file."""
        return "\n".join(self._yield_lines())
    
    @property
    def folder(self):
        return os.path.split(self.filename)[0]
    
    def same_folder(self, template_path=None):
        """Changes *self.filename* directory to one of *template_path*"""
        if template_path:
            folder = os.path.split(template_path)[0]
            self.filename = os.path.join(folder, self.filename)        
        return self
        
    def remove(self):
        try:
           os.remove(self.filename)
        except:
           pass           

class TempfolderFile(File):

    def __init__(self, filename):
        from kep.config import TESTDATA_DIR 
        self.filename=os.path.join(TESTDATA_DIR, filename)  
        
class UserInput():
    """Reads from strings with content or from filenames.
    
    >>> UserInput('abc').content
    'abc'
    
    >>> UserInput(File('temp.txt').save_text('content123').filename).content 
    'content123'
    
    >>> File('temp.txt').remove()
    
    """
    
    def __init__(self, input):
       """Reads *input* as string or filename, stores it in self.content"""
       
       def is_file(input):
        
            # protect against error 'filname too long' on Windows
            try:
                if os.path.exists(input):
                    return True
                else:
                    return False
            except:
                return False
       
       if is_file(input):
           filename = input       
           self.content = File(filename).read_text()
       elif isinstance(input, str):
           self.content = input
       else:
           raise ValueError(input)

class CSV():
    """Read CSV from file or string, store in self.rows as list.
    
    >>> CSV('abc\\tdef\\nvar\\t123').rows
    [['abc', 'def'], ['var', '123']]
    
    >>> CSV(File('temp.txt').save_text('abc\\tdef\\nvar\\t123').filename).rows
    [['abc', 'def'], ['var', '123']]
    
    >>> File('temp.txt').remove()  
    
    """  
    def __init__(self, csv_input):
        self.rows = [row.split('\t') for row in UserInput(csv_input).content.split('\n')]            
          
class YAML():
    """Read and parse YAML from file or string.
    
    >>> YAML('abc').content
    ['abc']
    
    >>> YAML('- abc \\n- def\\n---\\n key_text : value_text').content
    [['abc', 'def'], {'key_text': 'value_text'}]
    
    >>> YAML(File('temp.txt').save_text('- abc \\n- def\\n---\\n key_text : value_text').filename).content
    [['abc', 'def'], {'key_text': 'value_text'}]
    
    >>> File('temp.txt').remove()  
    
    """  

    def __init__(self, yaml_input):
        """Parses *yaml_input* as string or filename, stores it in self.content."""    
        yaml_string = UserInput(yaml_input).content
        self.content = list(yaml.load_all(yaml_string))