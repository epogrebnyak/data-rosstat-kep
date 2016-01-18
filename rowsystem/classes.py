"""DataWithDefiniton(InputDefinition),  InputDefinition() classes and their precursor classes. 
  
  InputDefinition(data_folder) stores all inputs for parsing from 'datafolder'
  DataWithDefiniton(data_folder) also inits rowsystem data structure. 
      
  DataWithDefiniton() is a parent to RowSystem class in rowsystem.py 
  
"""

import os
import yaml
   
from rowsystem.config import RESERVED_FILENAMES, CURRENT_MONTH_DATA_FOLDER
from rowsystem.word   import make_csv
from rowsystem.stream import dicts_as_stream
from rowsystem.label  import adjust_labels, Label, UnknownLabel
from rowsystem.db     import DefaultDatabase, DataframeEmitter

class Folder():

     def __init__(self, folder_path, must_create = False):
        # TODO: check if folder_path exists
        #       make a folder if must_create == True
        self.folder = folder_path


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
            raise Exception("Wrong segment format for " + yaml_input) 
                
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
         
    #def __repr__(self):
    #    return self.content
     
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

class ConvertWord(Folder):
    def __init__(self, *arg):
    
        super().__init__(*arg)
        # results in self.folder
        
        self._convert_word_files_in_folder_to_seamless_csv()

    def _convert_word_files_in_folder_to_seamless_csv(self):
         make_csv(self.folder)
        
       
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
         ConvertWord(data_folder)
         csv  = os.path.join(data_folder, RESERVED_FILENAMES['csv'] )
         spec = os.path.join(data_folder, RESERVED_FILENAMES['spec'])
         cfg  = os.path.join(data_folder, RESERVED_FILENAMES['cfg'] )
         if os.path.exists(cfg):
             self.init_by_component(csv, spec, segment_input = cfg)
         else:         
             self.init_by_component(csv, spec, segment_input = None)
             
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
            self.folder = arg[0]            
            self.init_from_folder(self.folder)
            
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

class RowSystem(DataWithDefiniton):

    def __init__(self, *arg):       
        
        # read raw rows and definition
        super().__init__(*arg)
        
        # label rows
        self.label()
        
        # allow call like rs.data.annual_df() - supplementary
        self.data = DataframeEmitter(self.dicts())        
        
    def dicts(self):
        return dicts_as_stream(self)

    def save(self):
        DefaultDatabase().save_stream(gen = self.dicts())
    
    def label(self):
        self._assign_parsing_specification_by_row()
        self._run_label_adjuster()
        
    def _labels_not_imported(self):
        target_list = self.get_definition_head_labels()
        imported_list = self.data.get_saved_head_labels()
        not_imported_list = []
        for label in target_list:
            if label not in imported_list:
                not_imported_list.append(label)
        return not_imported_list

    def varnames(self):
         # MAYDO: assign by frequency
         return self.data.get_saved_full_labels()        

    def headnames(self):
         # MAYDO: assign by frequency
         return self.data.get_saved_head_labels()
         
    def print_varnames(self, n = 2):
         # MAYDO: integrate to __repr__()
         if n == 2:
             self.print_varlist_two_columns()
         else:
             print(self)

    def print_varlist_two_columns(self):
        """List of variables in two colums, similar to Windows 'dir /D'"""
        # MAYDO: generalise to n columns +  use max length of variable namet in print("%-40.40s ... 
        print()
        vn = self.varnames()
        N = len(vn)
        if round(N/2) != N/2:
           vn = vn + ['']
        z = iter(vn)
        i = 0
        while i < N:
           print ("%-40.40s %-40.40s" % (next(z), next(z)))
           i += 2
        print()         

    def __len__(self):
         nh = len(self.headnames())
         nv = len(self.varnames())
         nd = len(self.data.dicts)
         return {'headnames': nh, 'fullnames': nv, 'datapoints':nd} 
        
    def __repr__(self):
         nlab = len(self.headnames())
         nvar = len(self.varnames())
         ndatapoints = len(self.data.dicts)
         info_0 = "Current dataset has {} variables, {} timeseries and {} data points".format(nlab, nvar, ndatapoints)
         info_1 =  "\nVariables ({}):\n".format(nlab)  + ", ".join(self.headnames())      
         info_2 =  "\nTimeseries ({}):\n".format(nvar) + ", ".join(self.varnames())      
         return info_0 + info_1 + info_2      
         
    def check_import_complete(self):
        nolabs = self._labels_not_imported()
        if nolabs:
            print(nolabs)
            raise Exception("Following labels were not imported: " + ", ".join(nolabs))
    
    def _run_label_adjuster(self):
        """Label data rows in rowsystems *rs* using markup information from id*.
           Returns *rs* with labels added in 'head_label' and 'unit_label' keys. 
        """
  
        cur_label = UnknownLabel()    
        for i, row in enumerate(self.rowsystem):    
        
           if self.is_textinfo_row(row):   
                   
                  adj_label = adjust_labels(textline=row['string'],
                                            incoming_label=cur_label, 
                                            dict_headline = row['spec'].header_dict, 
                                            dict_unit = row['spec'].unit_dict)

                  self.rowsystem[i]['label'] = Label(adj_label.head, adj_label.unit)
                  cur_label = adj_label
           
           else:
                  self.rowsystem[i]['label'] = Label(cur_label.head, cur_label.unit) 

    def _assign_parsing_specification_by_row(self):
        """Write appropriate parsing specification from self.default_spec or self.segments
            to self.rowsystem[i]['spec'] based on segments[j].start_line and .end_line      
        """
    
        switch = _SegmentState(self.default_spec, self.segments)
        
        # no segment information - all rows have default_spec 
        if not self.segments:
            for i, head in self.row_heads:
                 self.rowsystem[i]['spec'] = self.default_spec
        
        # segment information is supplied, will check row_heads and compare it with 
        else:            
            for i, head in self.row_heads:
                # are we in the default spec?
                if switch.in_segment:
                    # we are in custom spec. do we have to switch to the default spec? 
                    switch.update_if_leaving_custom_segment(head)  
                    # maybe it is also a start of a new custom spec?
                    switch.update_if_entered_custom_segment(head)
                else:
                    # should we switch to custom spec?
                    switch.update_if_entered_custom_segment(head)
                #finished adjusting specification for i-th row 
                self.rowsystem[i]['spec'] = switch.current_spec
               
class _SegmentState():

    def __init__(self, default_spec, segments):
      
      self.in_segment = False
      self.current_end_line = None
      self.current_spec = default_spec
      self.default_spec = default_spec
      self.segments = segments      
      
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

class CurrentMonthRowSystem(RowSystem):        

    def __init__(self):       
        
        # read raw rows and definition
        super().__init__(CURRENT_MONTH_DATA_FOLDER)
        
def print_rs():
   for rs in [CurrentMonthRowSystem()]:
       rs.check_import_complete() 
       rs.print_varnames() 
       print(rs)       