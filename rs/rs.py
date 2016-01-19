"""Manipulate raw data and parsing specification to obtain stream of flat data in class Rowsystem."""

#Entry:
#from rs import Segment, SegmentList, InputDefinition, RowSystem

from inputs import CurrentFolder, File, CSV, YAML
RESERVED_FILENAMES = {'csv': 'rs_tab.csv', 'cfg':'rs_cfg.txt'} 

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
         
class SegmentList(YAML):
    """Read several parsing specification files listed in a yaml specfile or string."""  
    
    def __init__(self, yaml_input):
    
        super().__init__(yaml_input)
        
        try: 
            # 'self.content[0]' contains a list of 1+ entries                          
            assert isinstance(self.content, list)
            assert isinstance(self.content[0], list)
            assert len(self.content) == 1
            assert len(self.content[0]) >= 1
        except:
            raise Exception("Wrong format for config file: " + yaml_input) 
        
        # if yaml_input is filepath - use it as template
        if os.path.exists(yaml_input):
            template_path = yaml_input
        else:
            template_path = None       
              
        adjusted_file_list = [File(f).same_folder(template_path).filename for f in self.content[0]]        

        for f in adjusted_file_list:
            assert os.path.exists(f)  
            
        try:            
            self.segments = [Segment(f) for f in adjusted_file_list] 
            assert len(self.segments) >= 1
        except:
            print("Error in configuration:", self.content[0])
            for f in adjusted_file_list:
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
    InputDefinition(csv_input, segment_input)  
    Input:
     csv_input     - data file name or string with data content
     segment_input - YAML filename or string with list of files containing parsing specification(s)
    """

    def init_by_component(self, csv_input, segment_input):
        self.segments = SegmentList(segment_input).segments
        self.rows = CSV(csv_input).rows
        self.specs = [None for x in self.rows]  # placeholder parsing specification
        self.labels = [None for x in self.rows] # placeholder for parsing result
         
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
            self.init_by_component(csv_input = arg[0], segment_input = arg[1])
        else:
            raise Exception("Wrong number of arguments for InputDefinition(), accepts 1 or 2, given: " + str(len(arg)) )         
         
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

    # Access methods for rows  
    def non_empty_enumerated_rows(self):
        for i, row in enumerate(self.rows):
            if row and row[0]:
                yield i, row  
    
    #@property   
    #def data_rows(self):    
    #    for i, row in self.non_empty_enumerated_rows():
    #        if is_year(row[0]):
    #            yield i, row                

    @property   
    def labelled_data_rows(self):    
        for i, row in self.non_empty_enumerated_rows():
            if is_year(row[0]) and not self.labels[i].is_unknown():
                yield i, row, self.labels[i], self.specs[i].reader_func                 

    @property            
    def row_heads(self):
        for i, row in self.non_empty_enumerated_rows():
            yield i, row[0]

    #@property      
    #def text_row_heads(self):
    #    for i, row in self.non_empty_enumerated_rows():
    #        if not is_year(row[0]):
    #            yield i, row[0]          

    @property  
    def full_rows(self):
        for i, row, spec, lab in enumerate(zip(self.rows, self.specs, self.labels)):
            yield i, row, spec, lab        
                
                
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
    
    def label(self):
        self._assign_parsing_specification_by_row()
        self._run_label_adjuster()
    
    def _run_label_adjuster(self):
        """Label data rows in rowsystems *rs* using markup information from id*.
           Returns *rs* with labels added in 'head_label' and 'unit_label' keys. 
        """
  
        cur_label = UnknownLabel()    

        for i, head in self.row_heads:
        
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
         return {'n_heads': nh, 'n_vars': nv, 'n_pts':nd} 
        
    def __repr__(self):
         i = self.__len__()
         info_0 = "Current dataset has {} variables, ".format(i['n_heads']) + 
                                      "{} timeseries ".format(i['n_vars']) + 
                                 "and {} data points.".format(i['n_pts'])                                 
         info_1 =  "\nVariables ({}):\n".format(info['n_heads'])  + tab.printable(self.headnames()) 
         info_2 =  "\nTimeseries ({}):\n".format(info['n_heads']) + tab.printable(self.varnames())     
         return info_0 + info_1 + info_2
    

if __name__ == '__main__': 
    from test_inputs_and_rs import write_temp_files, remove_temp_files
    import pprint     
    
    write_temp_files() # todo - better should return a folder
    r = RowSystem(CurrentFolder().path)
    r.check_import()
    print("\nRowsystem content")
    for frow in r.full_rows:
        pprint.pprint(frow)
    print("\nFlat dicts")
    pprint.pprint(r.dicts)    
    remove_temp_files()
