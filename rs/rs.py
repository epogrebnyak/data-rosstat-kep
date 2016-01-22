"""Manipulate raw data and parsing specification to obtain stream of flat data in class Rowsystem."""

# from rs import RowSystem                  # CurrentRowSystem (todo)


import os
from inputs import CurrentFolder, File, CSV, YAML
from config import RESERVED_FILENAMES, CURRENT_MONTH_DATA_FOLDER

from word import make_csv
from label import adjust_labels, Label, UnknownLabel
from stream import dicts_as_stream
from db import DefaultDatabase, DataframeEmitter
import tabulate as tab

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
            raise Exception("Wrong format for spec file: " + yaml_input) 
                
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

def is_year(s):    
    # case for "20141)"    
    s = s.replace(")", "")
    try:
       int(s)
       return True        
    except ValueError:
       return False                
       
       
class SegmentsList():
    def __init__(self, cfg_input, folder=None):
    
        # Input options are:
        #    filename + folder
        #    string + folder
        #    path    
    
        if folder:        
           app_path = os.path.join(folder, cfg_input)
           #filename + folder
           if os.path.exists(app_path):
                 ui = app_path
           #string + folder
           else:
                 ui = cfg_input
        #path
        else:
            ui = cfg_input
            folder = File(cfg_input).folder
        
        spec_paths_list = [os.path.join(folder, f) for f in YAML(ui).content[0]]
        self.yaml_string_list = [File(p).read_text() for p in spec_paths_list]        
      
                
class InputDefinition():
    """Inputs for parsing. Supports following calls: 
    
    InputDefinition(data_folder)               
    InputDefinition(csv_path, cfg_path)
    InputDefinition(csv_content, cfg_content, folder)
    InputDefinition(csv_content, [spec_content1, spec_content2])
    
    Input:
       csv_content   - string with raw csv data
       csv_path      - path to file with content above   
       cfg_content   - YAML document with list of files containing parsing specification(s)
       cfg_path      - path to file with content above
       spec_content* - YAML document with parsing specification     
    """
    
    def init_by_strings_and_folder(self, csv_content, cfg_content, folder):        
         self.init_by_strings(csv_content, SegmentsList(cfg_content, folder).yaml_string_list)   

    def init_by_paths(self, csv_path, cfg_path):
        self.init_by_strings(csv_path, SegmentsList(cfg_path).yaml_string_list)

    def init_by_strings(self, csv_input, spec_yamls):    
        self.rows = CSV(csv_input).rows
        self.segments = [Segment(spec_yaml) for spec_yaml in spec_yamls]
        self.specs  = [None for x in self.rows] # placeholder for parsing specification
        self.labels = [None for x in self.rows] # placeholder for parsing result
    
    def init_from_folder(self, data_folder):
        make_csv(self.folder)
        csv_path = os.path.join(data_folder, RESERVED_FILENAMES['csv'])
        cfg_path = os.path.join(data_folder, RESERVED_FILENAMES['cfg']) 
        self.init_by_paths(csv_path, cfg_path)

    def __init__(self, *arg):
        # folder
        if len(arg) == 1:
            self.folder = arg[0]            
            self.init_from_folder(data_folder = self.folder)
        # csv_input + list of specs 
        elif len(arg) == 2:
            self.folder = None
            self.init_by_strings(csv_input = arg[0], spec_yamls = arg[1])
        # csv_input + list of filenames + spec folder    
        elif len(arg) == 3:
            self.folder = arg[2]
            apparent_csv_path = os.path.join(self.folder, arg[0])
            apparent_cfg_path = os.path.join(self.folder, arg[1])
            if os.path.exists(apparent_csv_path) and os.path.exists(apparent_cfg_path):
                self.init_by_paths(csv_path = apparent_csv_path, cfg_path = apparent_cfg_path)
            else:
                self.init_by_strings_and_folder(csv_content = arg[0], cfg_content = arg[1], folder = arg[2])            
        else:
            raise Exception("Wrong number of arguments for InputDefinition() given: " + str(len(arg)) )         
         
    def get_definition_head_labels(self):
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

    # Access methods for rows  
    def non_empty_rows(self):
        for i, row in enumerate(self.rows):
            if row and row[0]:
                yield i, row  

    @property   
    def labelled_data_rows(self):    
        for i, row in self.non_empty_rows():
            if is_year(row[0]) and not self.labels[i].is_unknown():
                yield i, row, self.labels[i], self.specs[i].reader_func                 

    @property            
    def row_heads(self):
        for i, row in self.non_empty_rows():
            yield i, row[0]
            
    @property  
    def full_rows(self):
        i = 0 
        for row, spec, lab in zip(self.rows, self.specs, self.labels):
            yield i, row, spec, lab        
            i += 1    
                
class DefaultRowSystem(InputDefinition):
    """Data structure and functions to manupulate raw data and pasring specification""" 

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
        return self
        
    def save_as_test(self):
        TestDatabase().save_stream(gen = self.dicts())     
        return self
        
    def label(self):
        self._assign_parsing_specification_by_row()
        self._run_label_adjuster()
    
    def _run_label_adjuster(self):
        """Label rows using markup information from self.specs[i].header_dict
           and .unit_dict. Stores labels in self.labels[i]. 
        """
  
        cur_label = UnknownLabel()    

        for i, head in self.row_heads:
        
           # change cur_label at text rows, not starting with year number
           if not is_year(head):  
                cur_label = adjust_labels(textline=head, incoming_label=cur_label, 
                                          dict_headline=self.specs[i].header_dict, 
                                          dict_unit=self.specs[i].unit_dict)

           self.labels[i] = Label(cur_label.head, cur_label.unit)  
            

    def _assign_parsing_specification_by_row(self):
        """Write appropriate parsing specification from selfsegments[0] or self.segments
            to self.specs[i] based on segments[i].start_line and .end_line      
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
        self.reset_to_default()   
      
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
        # Exit from segment
        self.in_segment = False
        self.current_spec = self.default_spec
        self.current_end_line = None
       
    def enter_segment(self, segment_spec):
        self.in_segment = True
        self.current_spec = segment_spec
        self.current_end_line = segment_spec.end_line       

class RowSystem(DefaultRowSystem):

    # not todo: assort by time series frequency
    def varnames(self):
         return self.data.get_saved_full_labels()        

    def headnames(self):
         return self.data.get_saved_head_labels()
         
    def definition_headnames(self):
        return self.get_definition_head_labels() 
        
    def not_imported(self):
        imported_list = self.headnames()
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
         return {'n_heads': nh, 'n_vars': nv, 'n_pts':nd} 
        
    def __repr__(self):
         i = self.__len__()
         info_0 = "\nDataset contains {} variables, ".format(i['n_heads']) + \
                                     "{} timeseries ".format(i['n_vars']) + \
                                "and {} data points.".format(i['n_pts'])                                 
         info_1 = "\nVariables ({}):\n    ".format(i['n_heads']) + tab.printable(self.headnames()) 
         info_2 = "\nTimeseries ({}):\n   ".format(i['n_vars']) + tab.printable(self.varnames())     
         # check: ends with many spaces
         info_3 = "\nSource folder:\n    " + str(self.folder)
         return info_0 + info_1 + info_2 + info_3
         
if __name__ == '__main__': 
    pass
