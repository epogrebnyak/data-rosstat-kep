# -*- coding: utf-8 -*-

from rowsystem.preclasses import DataWithDefiniton
from rowsystem.db import DefaultDatabase, DataframeEmitter
from rowsystem.stream import dicts_as_stream
from rowsystem.label import adjust_labels, Label, UnknownLabel

class RowSystem(DataWithDefiniton):

    def __init__(self, *arg):       
        
        # read raw rows and definition
        super().__init__(*arg)
        
        # label rows
        self.label()
        
        # allow call like rs.data.annual_df() - supplementary
        # self.data = DataframeEmitter(self.dicts())

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