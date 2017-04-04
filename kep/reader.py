from common import File
from config import CSV_PATH
from parsing_definitions import get_definitions
from label import adjust_labels, Label, UnknownLabel
from stream import dicts_as_stream

def get_rows():
    return [row.split('\t') for row in File(CSV_PATH).read_text().split('\n')]  


rows = get_rows()
definitions = get_definitions()


#    def __yield_head_labels__(self):
#       for spec in self.segments:
#            for hlab in spec.head_labels:
#               yield hlab
#               
#    def get_definition_head_labels(self):
#        """Which unique headlabels are defined in specification?"""   
#        unique = set(self.__yield_head_labels__())
#        return sorted(list(unique))

def is_year(s):    
    # case for "20141)"    
    s = s.replace(")", "")
    try:
       int(s)
       return True        
    except ValueError:
       return False  

DEFAULT = 1
ALTERNATIVE = 0

class SegmentState():

    def __init__(self, default_spec, other_specs):
    
        self.default_spec = default_spec    
        self.specs = other_specs  
        self.reset_to_default_state()   
      
    @staticmethod    
    def is_matched(head, line):
        if line:
            return head.startswith(line)
        else:
            return False  
            
    def update_if_entered_custom_segment(self, head):
        for segment_spec in self.specs:
           if self.is_matched(head, segment_spec['scope']['start_line']):
                self.enter_segment(segment_spec)
                
    def update_if_leaving_custom_segment(self, head):    
        if self.is_matched(head, self.current_end_line):
                self.reset_to_default_state()
    
    def reset_to_default_state(self):
        # Exit from segment
        self.segment_state = DEFAULT
        self.current_spec = self.default_spec
        self.current_end_line = None
       
    def enter_segment(self, segment_spec):
        self.segment_state = ALTERNATIVE
        self.current_spec = segment_spec
        self.current_end_line = segment_spec['scope']['end_line']       

    def assign_segments(self, head_sequence):       
        spec_sequence = []
        for head in head_sequence:
           # are we in the default spec?
           if self.segment_state == ALTERNATIVE:
                # we are in custom spec  
                # do we have to switch to the default spec? 
                self.update_if_leaving_custom_segment(head)  
           self.update_if_entered_custom_segment(head)
           #finished adjusting specification for i-th row 
           spec_sequence = spec_sequence + [self.current_spec]
        return spec_sequence 
    
heads = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9']

default_def = {'scope': {'end_line': None, 'start_line': None}, 'def': 0}   
alt_defs = [
        {'scope': {'start_line': 'h1', 'end_line': 'h4'}, 'def': "seg 1 h1-h3"}
      , {'scope': {'start_line': 'h4', 'end_line': 'h6'}, 'def': "seg 2 h4-h5"}
      , {'scope': {'start_line': 'h8', 'end_line': 'h9'}, 'def': "seg 3 h8"}]

a = SegmentState(default_def, alt_defs).assign_segments(heads)
hs = [(h, s['def']) for h, s in zip(heads, a)]
assert hs == [('h0', 0),
 ('h1', 'seg 1 h1-h3'),
 ('h2', 'seg 1 h1-h3'),
 ('h3', 'seg 1 h1-h3'),
 ('h4', 'seg 2 h4-h5'),
 ('h5', 'seg 2 h4-h5'),
 ('h6', 0),
 ('h7', 0),
 ('h8', 'seg 3 h8'),
 ('h9', 0)]
    

b = SegmentState(default_def, []).assign_segments(heads)
hs2 = [(h, s['def']) for h, s in zip(heads, b)]
assert hs2 == [('h0', 0),
 ('h1', 0),
 ('h2', 0),
 ('h3', 0),
 ('h4', 0),
 ('h5', 0),
 ('h6', 0),
 ('h7', 0),
 ('h8', 0),
 ('h9', 0)]


def get_row_head(row):
    if row and row[0]:                
        if row[0].startswith("_"):
             pass
        else:                 
             yield row[0]

class Rows():   

    @property            
    def enum_row_heads(self):
        for i, row in enumerate(self.rows):
            if row and row[0]:
                yield i, row[0]
            else:
                yield i, ""
    
    def __init__(self):
        self.rows = get_rows()
        self.default_spec = get_definitions()['default']        
        self.segment_specs = get_definitions()['additional']
        _ss = SegmentState(self.default_spec, self.segment_specs)
        heads = [head for i, head in self.enum_row_heads]
        self.specs = _ss.assign_segments(heads)         

        """Label rows using markup information from self.specs[i].header_dict
           and .unit_dict. Stores labels in self.labels[i]. 
        """
        self.labels = [UnknownLabel() for _ in self.rows]
        cur_label = UnknownLabel() 
        for i, head in self.enum_row_heads:
           if not is_year(head):  
               cur_label = adjust_labels(textline=head, incoming_label=cur_label, 
                                          dict_headline=self.specs[i]['table_headers'], 
                                          dict_unit=self.specs[i]['units'])
           self.labels[i] = Label(cur_label.head, cur_label.unit)     
              
    
    @property   
    def labelled_data_rows(self):    
        for i, row in enumerate(self.rows):
            if row and row[0] and is_year(row[0]) \
               and not self.labels[i].is_unknown():
                  yield i, row, self.labels[i], self.specs[i]['reader_func']                 

    def dicts(self):
        return dicts_as_stream(self)    

#    def get_labelled_rows_by_component(self):    
#       for i, row, label, reader in self.labelled_data_rows:
#            var_name = label.labeltext
#            filtered_list = [filter_value(x) for x in row]             
#            reader_func = get_reader_func_by_row_length_and_special_dict(row, reader)            
#            year, annual_value, qtr_values, monthly_values = reader_func(filtered_list)
#            yield var_name, year, annual_value, qtr_values, monthly_values       