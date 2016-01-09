import os
import yaml

class File():
    #File('temp.txt').save_text("")

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
        return self.filename
    
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
        
    def remove(self):
        try:
           os.remove(self.filename)
        except:
           pass

class UserInput():
    """Reads *input* as string or filename, returns string or file content."""
    
    def __init__(self, input):
       self.filename = None
       if os.path.exists(input):
           filename = input       
           self.content = File(filename).read_text()
       elif isinstance(input, str):
           self.content = input
       else:
           raise ValueError
    
class InputYAML():
    def __init__(self, yaml_input):
        yaml_string = UserInput(yaml_input).content
        self.content = list(yaml.load_all(yaml_string))
        
class SegmentSpec(InputYAML):

    def __init__(self, yaml_input):
        super().__init__(yaml_input) # in Python 2 use super(D, self).__init__()
        self.attrs = {'start_line':   self.content[0]['start line'],
             'end_line':              self.content[0]['end line'],
             'header_dict':           self.content[2], 
             'unit_dict':             self.content[1],
             'reader':                self.content[0]['reader']}
    
    def __getattr__(self, name):
        try:
            return self.attrs[name]        
        except KeyError:
            raise AttributeError
            
    #def __setattr__(self, name, val):
    #    try:
    #        self.attrs[name] = val       
    #    except KeyError:
    #        raise AttributeError       
                 
z = SegmentSpec("""start line: 123
end line: 456
reader: null

---
a : 1
---
b : 2 
""")
print(z)   
        
        
class InputCSV():
    def __init__(self, csv_input):
        self.content = UserInput(csv_input).content.split('\n')

        
        
def test_File():
    # NOTE: works unless last line is \n 
    testline = """123\n\n456"""      
    assert testline == File(File('temp.txt').save_text(testline)).read_text()

def test_InputYAML():        
    txt = """a: 1\nb: 2\n---\n ddd"""
    file = File("noname.txt").save_text(txt)
    assert InputYAML(txt).content == InputYAML(file).content
        
def test_InputCSV():        
    test_list = ["123","---"] # NOTE: fails when \n inside list 
    test_string = "\n".join(test_list)
    assert test_list == InputCSV(test_string).content
        
        
        
