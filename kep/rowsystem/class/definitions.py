import os
import yaml

"""To init input parameters use:
  
  InputDefinition(data_folder)
  
"""
      
RESERVED_FILENAMES = {'csv':"tab.csv", 'spec':"__tab_spec.txt", 'cfg':"__tab_cfg.txt"}    



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
        
class Segment(InputYAML):

    def __init__(self, yaml_input):
    
        # parses yaml to 'self.content'
        super().__init__(yaml_input)
        
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

    def __eq__(self, obj):
         return self.content == obj.content
     
class SegmentList(InputYAML):

    def __init__(self, yaml_input, template_path = None):
    
        super().__init__(yaml_input)
        
        # if yaml_input is path - use it as template
        if os.path.exists(yaml_input):
            template_path = yaml_input
            
        adjusted_file_list = [self._adjust_path(f, template_path) for f in self.content[0]]        
        self.segments = [Segment(f) for f in adjusted_file_list] 
            
    def _adjust_path(self, filename, template_path=None):
        if template_path is None:
            return filename
        else:
            folder = os.path.split(template_path)[0]
            return os.path.join(folder, filename)       

            
class InputCSV():
    def __init__(self, csv_input):
        self.content = UserInput(csv_input).content.split('\n')
       
class InputDefinition():

     def init_by_component(self, csv_input, default_spec_input, segment_input):
         self.rows = InputCSV(csv_input).content
         self.default_spec = Segment(default_spec_input)
         if segment_input is None:
             self.segments = None             
         else:
             self.segments = SegmentList(segment_input).segments
             
     def init_from_folder(self, data_folder):
         csv  = os.path.join(data_folder, RESERVED_FILENAMES['csv'] )
         spec = os.path.join(data_folder, RESERVED_FILENAMES['spec'])
         cfg =  os.path.join(data_folder, RESERVED_FILENAMES['cfg'] )
         self.init_by_component(csv, spec, cfg)
         
     def __eq__(self, obj):
        if self.rows == obj.rows \
           and self.default_spec == obj.default_spec \
           and self.segments == obj.segments:
           return True
        else:
           return False
     
     def __init__(self, *arg):
         if len(arg) == 1:
            data_folder = arg[0]
            self.init_from_folder(data_folder)
         elif len(arg) == 2 or len(arg) == 3:
            csv_input = arg[0]
            default_spec_input = arg[1]
            if len(arg) == 3:
                 segment_input = arg[2]        
            else:
                 segment_input = None
            self.init_by_component(csv_input, default_spec_input, segment_input)     
         else:
            raise Exception # wrong number of arguments

def test_definitions():
    LINE_1 = 'line1'
    BASE_CSV_TXT =  """{}\nline2""".format(LINE_1) 
    BASE_SPEC_TXT = """start line: {}    \nend line: 5. line2  \nreader: null   \n---\n  u : 1  \n---\n  h : 2""".format(LINE_1)
    BASE_CFG_TXT =  """- add_spec1.txt\n- add_spec2.txt"""
    File(RESERVED_FILENAMES['csv'] ).save_text(BASE_CSV_TXT )
    File(RESERVED_FILENAMES['spec']).save_text(BASE_SPEC_TXT)
    File(RESERVED_FILENAMES['cfg'] ).save_text(BASE_CFG_TXT)
    File('add_spec1.txt'           ).save_text(BASE_SPEC_TXT)
    File('add_spec2.txt'           ).save_text(BASE_SPEC_TXT)   
    assert LINE_1 == InputCSV(BASE_CSV_TXT).content[0]
    assert LINE_1 == Segment(BASE_SPEC_TXT).start_line          
    assert 2 == len(SegmentList(BASE_CFG_TXT).content[0])
    assert LINE_1 == InputDefinition(BASE_CSV_TXT, BASE_SPEC_TXT).default_spec.start_line    
    assert LINE_1 == InputDefinition(BASE_CSV_TXT, BASE_SPEC_TXT,BASE_CFG_TXT).segments[0].start_line 
    def1 = InputDefinition(BASE_CSV_TXT, BASE_SPEC_TXT,BASE_CFG_TXT)
    def2 = InputDefinition(os.path.dirname(os.path.realpath(__file__)))
    assert def1 == def2
  
def test_File():
    # NOTE: works unless last line is \n 
    testline = """123\n\n456"""      
    assert testline == File(File('temp.txt').save_text(testline)).read_text()

def test_InputYAML():        
    txt = """a: 1\nb: 2\n---\n ddd"""
    file = File("temp.txt").save_text(txt)
    assert InputYAML(txt).content == InputYAML(file).content
        
def test_InputCSV():        
    test_list = ["123","456"] # NOTE: fails when \n inside list 
    test_string = "\n".join(test_list)
    assert test_list == InputCSV(test_string).content

