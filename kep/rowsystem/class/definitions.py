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
    """Reads *input* as string or filename, stores input in  .content """
    
    def __init__(self, input):
       self.filename = None
       if os.path.exists(input):
           filename = input       
           self.content = File(filename).read_text()
       elif isinstance(input, str):
           self.content = input
       else:
           raise ValueError
    
class YAML():
    def __init__(self, yaml_input):
        yaml_string = UserInput(yaml_input).content
        self.content = list(yaml.load_all(yaml_string))
        
class Segment(YAML):

    def __init__(self, yaml_input):
    
        # parses yaml to 'self.content'
        super().__init__(yaml_input)
        
        # assignment according to yaml structure
        self.attrs = {'start_line':   self.content[0]['start line'],
             'end_line':              self.content[0]['end line'],
             'header_dict':           self.content[2], 
             'unit_dict':             self.content[1],
             'reader':                self.content[0]['special reader'],
             # for compatibility
             '_as_load_spec':         (self.content[2], self.content[1], self.content[0])}
    
    def __getattr__(self, name):
        try:
            return self.attrs[name]        
        except KeyError:
            raise AttributeError

    def __eq__(self, obj):
         return self.content == obj.content
     
class SegmentList(YAML):

    def __init__(self, yaml_input, template_path = None):
        # WARNING: in fodler import better provide full path as 'yaml_input' 
    
        super().__init__(yaml_input)
        
        # if yaml_input is path - use it as template
        if os.path.exists(yaml_input):
            template_path = yaml_input
            
        adjusted_file_list = [self._adjust_path(f, template_path) for f in self.content[0]]        
        self.segments = [Segment(f) for f in adjusted_file_list] 
            
    def _adjust_path(self, filename, template_path=None):
        # Import spec files from the same folder 
        # WARNING: possible weakness
        if template_path is None:
            return filename
        else:
            folder = os.path.split(template_path)[0]
            return os.path.join(folder, filename)       

class CSV():
    def __init__(self, csv_input):
        self.rows = UserInput(csv_input).content.split('\n')
        
       
class InputDefinition():
     """Supports following calls: 
     
     InputDefinition(data_folder) # looks for RESERVED_FILENAMES
     InputDefinition(csv_input, default_spec_input) # one segment    
     InputDefinition(csv_input, default_spec_input, segment_input) # many segments     
     
     csv_input - data file name or string with file content
     default_spec_input, segment_input - YAML filenames or strings with file content
     
     """

     def init_by_component(self, csv_input, default_spec_input, segment_input):
         self.rows = CSV(csv_input).rows
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