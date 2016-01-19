"""Access to inputs (files or text strings) to read raw data and parsing specification."""

#Use to access:
#from inputs import CurrentFolder, File, CSV, YAML

import os
import yaml

class CurrentFolder():
    """Manipulation with folder paths. Can be used to pioint to current or parent folders."""
    
    @staticmethod
    def get_cwd():        
        return os.getcwd()
        
    @staticmethod
    def current_folder():
        curpath = os.path.realpath(__file__)
        return os.path.dirname(curpath)
        
    @staticmethod
    def level_up(path, n = 1):
        for i in range(n):
            path = os.path.split(path)[0]
        return path
        
    def up(self, n = 1):
        self.path = self.level_up(self.path, n)   
        return self 
        
    def join(self, folder):
        self.path = os.path.join(self.path, folder)
        return self         
        
    def change(self, path):
        if not os.path.isdir(path):
             os.makedirs(path)
        self.path = path
        return self
        
    def __init__(self):      
        self.path = self.current_folder()
        
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
        
    def same_folder(self, template_path=None):
        if template_path:
            folder = os.path.split(template_path)[0]
            self.filename = os.path.join(folder, self.filename)        
        return self
        
    def remove(self):
        try:
           os.remove(self.filename)
        except:
           pass           

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
    
    self.filename = None
       if os.path.exists(input):
           filename = input       
           self.content = File(filename).read_text()
       elif isinstance(input, str):
           self.content = input
       else:
           raise ValueError

class CSV():
    """Read CSV from file or string, store in self.rows as list.
    
    >>> CSV('abc\\tdef\\nvar\\t123').rows
    [['abc', 'def'], ['var', '123']]
    
    >>> CSV(File('temp.txt').save_text('abc\\tdef\\nvar\\t123').filename).rows
    [['abc', 'def'], ['var', '123']]
    
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
    
    """  

    def __init__(self, yaml_input):
        """Parses *yaml_input* as string or filename, stores it in self.content."""    
        yaml_string = UserInput(yaml_input).content
        self.content = list(yaml.load_all(yaml_string))            
