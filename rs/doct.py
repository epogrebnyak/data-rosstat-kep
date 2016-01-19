import os
import yaml

import rs.tabulate as tab

class Folder():

    @staticmethod
    def current_folder():
        curpath = os.path.realpath(__file__)
        return os.path.dirname(curpath)
        
    @staticmethod
    def level_up(path, n = 1):
        for i in range(n):
            path = os.path.split(path)[0]
        return path

    def __init__(self, folder_input=None, must_create = False):
        # TODO: check if folder_input exists
        #       make a folder if must_create == True
        if folder_input:
            self.folder = folder_input
        else:
            self.folder = self.current_folder()
        
class File():
    """File input-output operations with special handling of encoding and line ends.
    
    >>> File('temp.txt').save_text("abc").read_text()
    'abc'
    
    >>> next(File('temp.txt').save_text('abc'+'\\n'+'def')._yield_lines())
    'abc'
    
    # Not support by nose/doctest 
    # assert File('temp.txt').swap_folder(Folder().folder) == os.path.join(Folder().folder, 'temp.txt')
    #True

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
        
    def swap_folder(self, template_path=None):
        if template_path is None:
            return filename
        else:
            folder = os.path.split(template_path)[0]
            path = os.path.join(folder, self.filename)
            if os.path.exists(path):
                self.filename = path
            else: 
                raise FileNotFoundError(path)
        
    def remove(self):
        try:
           os.remove(self.filename)
        except:
           pass           

class UserInput():
    """Allows pass-through of both strings with content or filenames.

    >>> UserInput('abc').content
    'abc'

    >>> UserInput(File('temp.txt').save_text('content123').filename).content 
    'content123'
   
    >>> File('temp.txt').remove()
    
    """
    
    def __init__(self, input):
       """Reads *input* as string or filename, stores it in self.content."""
       self.filename = None
       if os.path.exists(input):
           filename = input       
           self.content = File(filename).read_text()
       elif isinstance(input, str):
           self.content = input
       else:
           raise ValueError

class CSV():
    """Read CSV from file or string, store in self.rows.

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
        """Parses *yaml_input* as string or filename, stores it in  self.content """    
        yaml_string = UserInput(yaml_input).content
        self.content = list(yaml.load_all(yaml_string))        

class Segment(YAML):
    """Read parsing specification from yaml specfile or string."""  

    def __init__(self, yaml_input):
    
        # parses yaml to 'self.content'
        super().__init__(yaml_input)
         
        try: 
            # check specification data structure
            assert isinstance(self.content, list)
            assert len(self.content) == 3
            for part in self.content:
                assert isinstance(part, dict)
            for kw in ['start line', 'end line', 'special reader']:
                assert self.content[0].keys().__contains__(kw)
        except:
            raise Exception("Wrong format: " + yaml_input) 
                
        # assignment of attributes according to yaml structure
        self.attrs = {'start_line':   self.content[0]['start line'],
             'end_line':              self.content[0]['end line'],
             'reader_func':           self.content[0]['special reader'],
             'unit_dict':             self.content[1],
             'header_dict':           self.content[2]}
             
    def __getattr__(self, name):
        try:
            return self.attrs[name]        
        except KeyError:
            raise AttributeError(name)

    def __eq__(self, obj):
         return self.content == obj.content
         
    def __repr__(self):
        return self.content.__repr__()
         
class SegmentList(YAML):
    
    def __init__(self, yaml_input):
    
        super().__init__(yaml_input)
        
        try: 
            # 'self.content[0]' contains a list of 1+ entries
            assert isinstance(self.content, list)
            assert isinstance(self.content[0], list)
            assert len(self.content) = 1
            assert len(self.content[0]) >= 1
        except:
            raise Exception("Wrong format: " + yaml_input) 
        
        # if yaml_input is filepath - use it as template
        if os.path.exists(yaml_input):
            template_path = yaml_input
        else:
            template_path = None
            
        adjusted_file_list = [File(f).swap_folder(template_path).filename for f in self.content[0]]        

        try:
            self.segments = [Segment(f) for f in adjusted_file_list] 
            assert len(self.segments) >= 1
        except:
            print("Error in configuration:", self.content[0])            
            for f in adjusted_file_list:
                print(f)
                print(Segment(f))
                raise Exception 

                
def is_year(s):    
    # case for "20141)"    
    s = s.replace(")", "")
    try:
       int(s)
       return True        
    except ValueError:
       return False                
                
class InputDefinition():
     """Inputs for parsing. Supports following calls: 
     
     InputDefinition(data_folder)               # will look for two RESERVED_FILENAMES in 'data_folder'
     InputDefinition(csv_input, segment_input)  # 
     
     Input:
         csv_input     - data file name or string with data content
         segment_input - YAML filename or string with list of files containing parsing specification(s)
     
     """

     def init_by_component(self, csv_input, segment_input):
         self.segments = SegmentList(segment_input).segments
         self.rows = CSV(csv_input).rows
         self.labels = [None for x in self.rows] # placeholder parsing input (specification)
         self.specs =  [None for x in self.rows] # placeholder for parsing result
             
     def init_from_folder(self, data_folder):
         make_csv(self.folder)
         csv  = os.path.join(data_folder, RESERVED_FILENAMES['csv'] )
         cfg  = os.path.join(data_folder, RESERVED_FILENAMES['cfg'] )
         self.init_by_component(csv, cfg)
 
     def __init__(self, *arg):
        
         if len(arg) == 1:
            self.folder = arg[0]            
            self.init_from_folder(data_folder = self.folder)
         elif len(arg) == 2:
            self.init_by_component(csv_input = arg[0], segment_input = arg[1)
         else:
            raise Exception("Wrong number of arguments for InputDefinition(), accepts 1 or 2.")         
             
     def _definition_head_labels(self):
        s = set()
        for spec in self.segments:
            for hd_items in spec.header_dict.values():
                s.add(hd_items[0])             
        return sorted(list(s))
         
     def __eq__(self, obj):
        if self.rows == obj.rows and self.segments == obj.segments:
           return True
        else:
           return False
    
    # Access methods    
    def non_empty_enumerated_rows(self):
       for i, row in enumerate(self.rows):
            if row and row[0]:
                yield i, row  
    
    @property   
    def data_rows(self):    
        for i, row in non_empty_enumerated_rows():
            if is_year(row[0]):
                yield i, row                

    @property            
    def row_heads(self):
        for i, row in non_empty_enumerated_rows():
            yield i, row[0]

    @property      
    def text_row_heads(self):
        for i, row in non_empty_enumerated_rows():
            if not is_year(row[0]):
                yield i, row[0]          

class DefaultRowSystem(InputDefinition):

    def __init__(self, *arg):       
        
        # read raw rows and definition
        super().__init__(*arg)
        
        # label rows
        self.label()
        
        # allow call like rs.data.annual_df()
        self.data = DataframeEmitter(self.dicts())        
        
    def dicts(self):
        return dicts_as_stream(self)

    def save(self):
        DefaultDatabase().save_stream(gen = self.dicts())
    
    def label(self):
        self._assign_parsing_specification_by_row()
        self._run_label_adjuster()
    
    def _run_label_adjuster(self):
        """Label data rows in rowsystems *rs* using markup information from id*.
           Returns *rs* with labels added in 'head_label' and 'unit_label' keys. 
        """
  
        cur_label = UnknownLabel()    

        for i, head in row_heads:
        
            if not is_year(head):  
                cur_label = adjust_labels(textline=head, incoming_label=cur_label, 
                                          dict_headline=self.specs[i].header_dict, 
                                          dict_unit=self.specs[i].unit_dict)

            self.labels[i] = Label(cur_label.head, cur_label.unit)  
            

    def _assign_parsing_specification_by_row(self):
        """Write appropriate parsing specification from self.default_spec or self.segments
            to self.rowsystem[i]['spec'] based on segments[j].start_line and .end_line      
        """
    
        switch = _SegmentState(self.segments)
        
        # no segment information - all rows have default parsing specification 
        if len(self.segments) == 1:
            for i, head in self.row_heads:
                 self.specs[i] = self.segments[0]
        
        # segment information is supplied, will check row_heads and compare it with 
        else:            
            for i, head in self.row_heads:
            
                # are we in the default spec?
                if switch.in_segment:
                    # we are in custom spec. do we have to switch to the default spec? 
                    switch.update_if_leaving_custom_segment(head)  
                    # maybe it is also a start of a new custom spec?
                    switch.update_if_entered_custom_segment(head)
                # should we switch to custom spec?
                else:                    
                    switch.update_if_entered_custom_segment(head)
                    
                #finished adjusting specification for i-th row 
                self.specs[i] = switch.current_spec          

class _SegmentState():

    def __init__(self, segments):

        self.segments = segments       
        self.default_spec = segments[0]      
        self.reset_to_default(self)   
      
    @staticmethod    
    def is_matched(head, line):
        if line:
            return head.startswith(line)
        else:
            return False  
            
    def update_if_entered_custom_segment(self, head):
        for segment_spec in self.segments:
           if self.is_matched(head, segment_spec.start_line):
                self.enter_segment(segment_spec)
                
    def update_if_leaving_custom_segment(self, head):    
        if self.is_matched(head,self.current_end_line):
                self.reset_to_default()
    
    def reset_to_default(self):
        self.in_segment = False
        self.current_spec = self.default_spec
        self.current_end_line = None
       
    def enter_segment(self, segment_spec):
        self.in_segment = True
        self.current_spec = segment_spec
        self.current_end_line = segment_spec.end_line       

class RowSystem(DefaultRowSystem):

    def varnames(self):
         # MAYDO: assort by time series frequency
         return self.data.get_saved_full_labels()        

    def headnames(self):
         # MAYDO: assort by time series frequency
         return self.data.get_saved_head_labels()
         
    def definition_headnames(self):
        return self._definition_head_labels() 
        
    def not_imported(self):
        imported_list = self.headnames(self)
        not_imported_list = []
        for label in self.definition_headnames():
            if label not in imported_list:
                not_imported_list.append(label)
        return not_imported_list
        
    def check_import(self):
        nolabs = self.not_imported()
        if nolabs:
            raise Exception("Following labels were not imported: " + ", ".join(nolabs))
        
    def __len__(self):
         nh = len(self.headnames())
         nv = len(self.varnames())
         nd = len(self.data.dicts)
         return {'headnames': nh, 'varnames': nv, 'datapoints':nd} 
        
    def __repr__(self):
         info = self.__len__()
         info_0 = "Current dataset has {} variables, {} timeseries and {} data points".format(info['headnames'],
                                                                                              info['varnames'], 
                                                                                              info['datapoints'])
         info_1 =  "\nVariables ({}):\n".format(nlab)  + tab.printable(self.headnames()) 
         info_2 =  "\nTimeseries ({}):\n".format(nvar) + tab.printable(self.varnames())     
         return info_0 + info_1 + info_2
         
         