import os
import csv

from kep.config import CSV_PATH
from kep.reader.parsing_definitions import get_definitions
from kep.reader.label import adjust_labels, Label, UnknownLabel
from kep.reader.stream import dicts_as_stream

ENCODING = 'utf8'

class File():
    def __init__(self, path):
        if os.path.exists(path):
            self.path = path
        else:
            raise FileNotFoundError(path)

    def __repr__(self):
        return os.path.normpath(self.path)

    def __yield_lines__(self):
        with open(self.path, 'r', encoding=ENCODING) as f:
            for line in f:
                if line.endswith('\n'):
                    yield line[0:-1]
                else:
                    yield line

    def read_text(self):
        """Read text from file."""
        return "\n".join(self.__yield_lines__())


def get_rows():
    return [row.split('\t') for row in File(CSV_PATH).read_text().split('\n')]  

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

#for r, l in zip(Rows().rows[455:500], Rows().labels[455:500]):
#    print(r, l)
#    print()