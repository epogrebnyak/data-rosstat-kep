"""DataWithDefiniton(InputDefinition),  InputDefinition() classes and their precursor classes. 
  
  InputDefinition(data_folder) stores all inputs for parsing from 'datafolder'
  DataWithDefiniton(data_folder) also inits rowsystem data structure. 
      
  DataWithDefiniton() is a parent to RowSystem class in rowsystem.py 
  
"""

import os
import yaml
   
from rowsystem.config import RESERVED_FILENAMES
from rowsystem.word import make_csv

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
         
        try: 
            assert isinstance(self.content, list)
            assert len(self.content) == 3
        except:
            print(self.content)
            raise Exception 
                
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
         
    def __repr__(self):
         return 
     
class SegmentList(YAML):

    def __init__(self, yaml_input, template_path = None):
        # WARNING: in fodler import better provide full path as 'yaml_input' 
    
        super().__init__(yaml_input)
        
        # if yaml_input is path - use it as template
        if os.path.exists(yaml_input):
            template_path = yaml_input
            
        adjusted_file_list = [self._adjust_path(f, template_path) for f in self.content[0]]        

        try:
            self.segments = [Segment(f) for f in adjusted_file_list] 
        except:
            print("Specfile error:")            
            for f in adjusted_file_list:
                print(f)
                print(Segment(f))
                raise Exception 

         
    def _adjust_path(self, filename, template_path=None):
        # Import spec files from the same folder 
        # WARNING: possible weakness
        if template_path is None:
            return filename
        else:
            folder = os.path.split(template_path)[0]
            path = os.path.join(folder, filename)
            if os.path.exists(path):
                return path
            else: 
                raise FileNotFoundError(path)

class CSV():
    def __init__(self, csv_input):
        self.rows = UserInput(csv_input).content.split('\n')
        
       
class InputDefinition():
     """Supports following calls: 
     
     InputDefinition(data_folder) # will look for RESERVED_FILENAMES in 'data_folder'
     InputDefinition(csv_input, default_spec_input) # one segment for all 'csv_input'    
     InputDefinition(csv_input, default_spec_input, segment_input) # many segments     
     
     csv_input - data file name or string with file content
     default_spec_input, segment_input - YAML filenames or strings with file content
     
     Usage variables:
        self.rows
        self.default_spec
        self.segments
     """

     def init_by_component(self, csv_input, default_spec_input, segment_input):
         self.rows = CSV(csv_input).rows
         self.default_spec = Segment(default_spec_input)
         if segment_input is None:
             self.segments = None             
         else:
             self.segments = SegmentList(segment_input).segments
             
     def init_from_folder(self, data_folder):
         self._convert_word_files_to_seamless_csv(data_folder)
         csv  = os.path.join(data_folder, RESERVED_FILENAMES['csv'] )
         spec = os.path.join(data_folder, RESERVED_FILENAMES['spec'])
         cfg =  os.path.join(data_folder, RESERVED_FILENAMES['cfg'] )
         self.init_by_component(csv, spec, cfg)
                  
     def _convert_word_files_to_seamless_csv(self, folder):
         make_csv(folder)
          
     def get_definition_head_labels(self):         
         if self.segments:
             full_spec_list = [self.default_spec] + self.segments
         else:
             full_spec_list = [self.default_spec]
        
         def unpack():
             for spec in full_spec_list:
                 for hd in spec.header_dict.values():
                     yield hd[0]
             
         return sorted(list(set(unpack())))
     
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
            
         elif len(arg) in [2, 3]:
            csv_input = arg[0]
            default_spec_input = arg[1]
            if len(arg) == 3:
                 segment_input = arg[2]        
            else:
                 segment_input = None
            self.init_by_component(csv_input, default_spec_input, segment_input)
            
         else:
            raise Exception # wrong number of arguments

class DataWithDefiniton(InputDefinition):
    
    def __init__(self, *arg):
    
        super().__init__(*arg)
        # Results in:
        #   self.rows
        #   self.default_spec
        #   self.segments
        
        self.string_rows_to_rowsystem()
        # Adds:
        #   self.rowsystem
    
    def string_rows_to_rowsystem(self):
        """Return rowsystem, where each line/row from self.rows is presented as 
           a dictionary containing raw data and supplementary information."""
           
        self.rowsystem = []
        
        #MAYDO: convert to class
        for row in self.rows:
           rs_item = {   'string': row,  # raw string
                                   #MAYDO: remove 'list'
                                   #WARNING: raw rows stored trice
                           'list': row.split('\t'),  # string separated coverted to list  
                          'label': None, # placeholder for parsing result
                           'spec': None} # placeholder parsing input (specification)
           self.rowsystem.append(rs_item)
           
    @property      
    def text_rows(self):
        for row in self.rowsystem:
            if self.is_textinfo_row(row):
                yield row            
                
    @property   
    def data_rows(self):
        for row in self.rowsystem:
            if self.is_data_row(row):
                yield row            

    @property            
    def row_heads(self):
        for i, row in enumerate(self.rowsystem):
           try:
               head = row['list'][0]
               if head:
                  yield i, head              
           except:
               pass   
   
    #@staticmethod
    def is_textinfo_row(self, row):
        head = row['list'][0]
        if self.is_year(head):
           return False
        elif head == '':
           return False
        else:
           return True

    #@staticmethod
    def is_data_row(self, row):
        if self.is_year(row['list'][0]):
           return True
        else:
           return False 
           
    @staticmethod
    def is_year(s):    
        # case for "20141)"    
        s = s.replace(")", "")
        try:
           int(s)
           return True        
        except ValueError:
           return False

if __name__ == "__main__":
    import testdata
    testdata.get_testable_files()
    folder = testdata.current_folder() 
    rd = DataWithDefiniton(folder)
    testdata.remove_files()