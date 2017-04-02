# csv
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

class GoodRows():   

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


g = GoodRows()
assert type(g.specs[1000]) == dict
assert len(g.rows) == len(g.specs)
assert type(list(g.dicts())[1000]) == dict

  
class Rows():
    
    def __init__(self):
        self.rows = get_rows()
        self.segments = get_definitions()        

    def __eq__(self, obj):
        if self.rows == obj.rows and self.segments == obj.segments:
           return True
        else:
           return False

    @property                  
    def non_empty_rows(self):
        for i, row in enumerate(self.rows):
            if row and row[0]:
                yield i, row  

    @property            
    def row_heads(self):
        for i, row in self.non_empty_rows():
            if row[0].startswith("_"):
                pass
            else:                 
                yield i, row[0]

    @property
    def apparent_headers(self):
        for i, head in self.row_heads:
            if not is_year(head) and (head.strip()[0].isdigit() or head.strip()[1].isdigit()) \
                                 and "000," not in head:
               yield i, head


                
    @property   
    def labelled_data_rows(self):    
        for i, row in self.non_empty_rows():
            if is_year(row[0]) and not self.labels[i].is_unknown():
                yield i, row, self.labels[i], self.specs[i].reader_func                 


            
                
    @property  
    def full_rows(self):
        i = 0 
        for row, spec, lab in zip(self.rows, self.specs, self.labels):
            try:
                yield {'i':i, 'row':row, 'spec':spec, 'label':lab.labeltext}
            except:
                yield {'i':i, 'row':row, 'spec':spec, 'label':"___"}                
            i += 1             
    
#    @property     
#    def datablock_lines(self):    
#        for j, head in self.row_heads:
#            if head.startswith("2009"):
#                yield j
#        
#    def all_2014_count(self):
#        return len(list(self.datablock_lines))    
#        
        # add this statistics to __repr__()
        # not todо/make issue: number of variables by section.
        # May also assign time series in rs.toc() by reviewing rs.full_rows list of dict     

    def section_content(self):
    
        header_lines = [i for i, h in self.apparent_headers] + [100000 * 100000]  
        headers      = [h for i, h in self.apparent_headers]
        data_lines   = [j for j    in self.datablock_lines]

        def count_all_between(si, ei, seq = data_lines):
           k = 0 
           u = 0
           labs = []
           for s in seq:          
              if s >= si and s <= ei:
                 k += 1
                 if self.labels[s].is_unknown():
                    u += 1 
                 else:
                    labs.append(self.labels[s].labeltext)
           return k, u, labs

        def cnt_by_seg():
           for t, line in enumerate(header_lines[0:-1]):
               total, unknowns, labs = count_all_between(header_lines[t], header_lines[t+1])
               yield line, headers[t], total, unknowns, labs 

        return list(cnt_by_seg())

    def toc(self):
       """Write table of contents with additional information about raw csv file parsing.""" 
       
       from kep.reader.comments import PARSING_COMMENTS
       
       def comment(header):       
           for e in PARSING_COMMENTS:
               if header.startswith(e[1]):
                  return "\n    Комментарий: " + e[0]
           return ""
           
       def make_msg(line, header, total, unknowns, labs, full = True):
           msg = ""
           
           if full:
              # writing full information about all headers
              msg = header.join("\n" * 2)
              
           if total:
              # we are writing only headers with some data inside
              if unknowns == 0:
                  # everything specified  
                  if full:
                     # ... in full output lets mention it
                     msg += "\n".join("    " + lab for lab in labs) + \
                     "\n    Все переменные раздела внесены в базу данных."                  
              else:
                  # ahhhh! there are some undocumented varibales in the section! 
                  msg = header.join("\n" * 2)
                  msg += "\n".join("    " + lab for lab in labs) + \
                         "\n    {0} из {1} переменных внесено в базу данных".format(total - unknowns, total)
                  msg += comment(header)
                 
           return msg
           
       msg1 = "\n".join(make_msg(*arg, full = True) for arg in self.section_content())
       msg2 = "\n".join(make_msg(*arg, full = False) for arg in self.section_content())       
       File(TOC_FILE).save_text(msg1 + "\n"*5 + "-------------------------\n" + \
                                                "НЕ ВНЕСЕНО В БАЗУ ДАННЫХ:\n" + msg2)  
        
    def __yield_head_labels__(self):
       for spec in self.segments:
            for hlab in spec.head_labels:
               yield hlab
               
    def get_definition_head_labels(self):
        """Which unique headlabels are defined in specification?"""   
        unique = set(self.__yield_head_labels__())
        return sorted(list(unique))

               
class CoreRowSystem(Rows):
    """Data structure and functions to manupulate raw data and pasring specification.
       
       Main mthods are:
          dicts()
          label()
          save()         
    """ 

    def __init__(self, *arg):       
        
        # read raw rows and definition
        super().__init__(*arg)
        
        # label rows
        self.label()
        
        # allow call like rs.data.annual_df()
        self.data = DictsAsDataframes(self.dicts())

        #check for duplicates
        try_dfa = self.data.annual_df()        

    def dicts(self):
        return dicts_as_stream(self)

    def named_dicts(self, name):
        for d in self.dicts():
            if d['varname'] == name:
               yield d            
        
    def get_header_and_desc_dicts(self):
        for spec in self.segments:
            for k,v in spec.header_dict.items():
                yield {"_head":v[0], '_desc':k}
                
    def save(self):
        self.save_as_default()     
        
    def save_as_default(self):
        self.dump_dicts_to_db(db = DefaultDatabase())
        self.toc()
        return self
    
    def save_as_test(self):
        self.dump_dicts_to_db(db = TrialDatabase())
        return self
        
    def dump_dicts_to_db(self, db): 
        # WARNING: call order matters, cannot call db.save_data_dicts(), causes error   
        db.save_headlabel_description_dicts(gen = self.get_header_and_desc_dicts())
        db.save_data_dicts(gen = self.dicts())
        
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
    
        switch = SegmentState(self.segments)
        
        # no segment information - all rows have default parsing specification 
        if len(self.segments) == 1:
            for i, head in self.row_heads:
                 self.specs[i] = self.segments[0]
        
        # segment information is supplied, 
        # will check row_heads and compare it with 
        else:            
            for i, head in self.row_heads:
            
                # are we in the default spec?
                if switch.in_additional_segment:
                    # we are in custom spec. 
                    # do we have to switch to the default spec? 
                    switch.update_if_leaving_custom_segment(head)  
                    # maybe it is also a start of a new custom spec?
                    switch.update_if_entered_custom_segment(head)
                # should we switch to custom spec?
                else:                    
                    switch.update_if_entered_custom_segment(head)
                    
                #finished adjusting specification for i-th row 
                self.specs[i] = switch.current_spec          


#
#class RowSystem(CoreRowSystem):
#
#    def varnames(self):
#         return self.data.get_saved_full_labels()        
#
#    def headnames(self):
#         return self.data.get_saved_head_labels()
#         
#    def definition_headnames(self):
#        return self.get_definition_head_labels() 
#        
#    def not_imported(self):
#        imported_list = self.headnames()
#        not_imported_list = []
#        for label in self.definition_headnames():
#            if label not in imported_list:
#                not_imported_list.append(label)
#        return not_imported_list
#        
#    def import_msg(self):
#        nolabs = self.not_imported()
#        if nolabs:
#            return ("\nWARNING: following labels were not imported: " + ", ".join(nolabs))
#        else:
#            return ""
#    
#    def __len__(self):
#         h = len(self.headnames())
#         v = len(self.varnames())
#         d = len(self.data.dicts)
#         t = self.all_2014_count()
#         
#         return {'heads': h, 'vars': v, 'points':d, 'total_ts':t} 
#    
#    def __init__(self, *arg):
#         super().__init__(*arg)
#      
#    def __repr__(self):
#         len_dict = self.__len__()
#         t = len_dict['total_ts']
#         cvg = int(round(len_dict['vars']  / t * 100, 0))
#         info_0 = "\nTimeseries ({}):\n".format(len_dict['vars']) + tab.printable(self.varnames())     
#         info_1 = "\n\nDataset contains {} variables, ".format(len_dict['heads']) + \
#                                       "{} timeseries ".format(len_dict['vars']) + \
#                                  "and {} data points.".format(len_dict['points'])
#         info_2 = "\nApparent total timeseries in original source: {0}. Estimated coverage: {1}%".format(t, cvg)  
#         info_3 = "\nSource folder:\n    " + str(self.folder)
#         info_4 = self.import_msg()
#         return info_0 + info_1 + info_2 + info_3 +  info_4
#         
#
#class CurrentMonthRowSystem(RowSystem):
#    
#    def __init__(self):
#        super().__init__()
#        print(self)
#      
#    def update(self):
#        
#        #updates database
#        self.save()
#        print("\nDatabase updated from:\n    " + self.folder) 
#        
#        #updates csv dumps
#        self.data.save_dfs()
#        print("New CSV dumps created.") 
#         
#if __name__ == '__main__': 
#    m = CurrentMonthRowSystem()
#    m.toc()
#       
