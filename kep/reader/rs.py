# -*- coding: utf-8 -*-
"""Manipulate raw data using parsing specification to obtain stream of clean flat data in Rowsystem class."""

import os

from kep.common.inputs import File, CSV, YAML
import kep.common.tabulate as tab
from kep.config import RESERVED_FILENAMES, CURRENT_MONTH_DATA_FOLDER, TOC_FILE
from kep.reader.word import make_csv
from kep.reader.label import adjust_labels, Label, UnknownLabel
from kep.reader.stream import dicts_as_stream
from kep.database.db import DefaultDatabase
from kep.extract.dataframes import DictsAsDataframes

class Segment(YAML):
    """Read parsing specification from yaml specfile or string.
    
Valid specification yaml looks like:
    
start line: null       # 'start_line'
end line: null         # 'end_line'
special reader: null   # 'reader_func'
---
# 'unit_dict' section 
"в процентах" : percent
---
# 'header_dict' section 
Varname header: 
 - VAR1
 - usd
 - 1.1 # section number
Another header:
 - VAR2
 - rur
 - 1.2 # section number

"""  

    def self_check(self, yaml_input):
        """Check specification data structure"""
        try: 
            # yaml was read as a list         
            assert isinstance(self.content, list)
            # yaml has 3 docs
            assert len(self.content) == 3
            # every doc is a dict
            for part in self.content:
                assert isinstance(part, dict)
            # first doc has reserved keys 
            for kw in ['start line', 'end line', 'special reader']:
                assert self.content[0].keys().__contains__(kw)
        except:
            raise Exception("Wrong format for parsing specification.\nGiven: " + yaml_input[0:200] + "..." \
                            + "\nParsed: " + self.content.__repr__()[0:200] + "...") 

    def __init__(self, yaml_input):
    
        # parses yaml to 'self.content'
        super().__init__(yaml_input)
        
        # checks input structrure
        self.self_check(yaml_input)
         
        # assignment of attributes according to yaml structure
        self.attrs = {'start_line':   self.content[0]['start line'],
             'end_line':              self.content[0]['end line'],
             'reader_func':           self.content[0]['special reader'],
             'unit_dict':             self.content[1],
             'header_dict':           self.content[2],
             'head_labels':          [v[0] for v in self.content[2].values()]
             }
             
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
            if os.path.exists(cfg_input):
                ui = cfg_input
                folder = File(cfg_input).folder
            else:
                raise FileNotFoundError(cfg_input) 
        
        assert isinstance(YAML(ui).content, list)
        first_yaml_doc = YAML(ui).content[0]
        spec_paths_list = [os.path.join(folder, f) for f in first_yaml_doc]
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
    
    def init_from_folder(self, data_folder):
        make_csv(self.folder)
        csv_path = os.path.join(data_folder, RESERVED_FILENAMES['csv'])
        cfg_path = os.path.join(data_folder, RESERVED_FILENAMES['cfg']) 
        self.init_by_paths(csv_path, cfg_path)

    def init_by_paths(self, csv_path, cfg_path):
        self.init_by_strings(csv_path, SegmentsList(cfg_path).yaml_string_list)
        
    def init_by_strings_and_folder(self, csv_content, cfg_content, folder):        
         self.init_by_strings(csv_content, SegmentsList(cfg_content, folder).yaml_string_list)   

    def init_by_strings(self, csv_input, spec_yamls):    
        self.rows = CSV(csv_input).rows
        self.segments = [Segment(spec_yaml) for spec_yaml in spec_yamls]
        self.specs  = [None for x in self.rows] # placeholder for parsing specification
        self.labels = [None for x in self.rows] # placeholder for parsing result

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

    def __eq__(self, obj):
        if self.rows == obj.rows and self.segments == obj.segments:
           return True
        else:
           return False
           
    #
    #
    # Access methods for rows  
    #
    #
    
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
    def full_rows(self):
        i = 0 
        for row, spec, lab in zip(self.rows, self.specs, self.labels):
            try:
                yield {'i':i, 'row':row, 'spec':spec, 'label':lab.labeltext}
            except:
                yield {'i':i, 'row':row, 'spec':spec, 'label':"___"}                
            i += 1             
    
    @property     
    def datablock_lines(self):    
        for j, head in self.row_heads:
            if head.startswith("2009"):
                yield j
        
    def all_2014_count(self):
        return len(list(self.datablock_lines))    
        
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

               
class CoreRowSystem(InputDefinition):
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

class RowSystem(CoreRowSystem):

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
        
    def import_msg(self):
        nolabs = self.not_imported()
        if nolabs:
            return ("\nWARNING: following labels were not imported: " + ", ".join(nolabs))
        else:
            return ""
    
    def __len__(self):
         h = len(self.headnames())
         v = len(self.varnames())
         d = len(self.data.dicts)
         t = self.all_2014_count()
         
         return {'heads': h, 'vars': v, 'points':d, 'total_ts':t} 
    
    def __init__(self, *arg):
         super().__init__(*arg)
      
    def __repr__(self):
         len_dict = self.__len__()
         t = len_dict['total_ts']
         cvg = int(round(len_dict['vars']  / t * 100, 0))
         info_0 = "\nTimeseries ({}):\n".format(len_dict['vars']) + tab.printable(self.varnames())     
         info_1 = "\n\nDataset contains {} variables, ".format(len_dict['heads']) + \
                                       "{} timeseries ".format(len_dict['vars']) + \
                                  "and {} data points.".format(len_dict['points'])
         info_2 = "\nApparent total timeseries in original source: {0}. Estimated coverage: {1}%".format(t, cvg)  
         info_3 = "\nSource folder:\n    " + str(self.folder)
         info_4 = self.import_msg()
         return info_0 + info_1 + info_2 + info_3 +  info_4
         

class CurrentMonthRowSystem(RowSystem):
    
    def __init__(self):
        super().__init__(CURRENT_MONTH_DATA_FOLDER)
        print(self)
      
    def update(self):
        
        #updates database
        self.save()
        print("\nDatabase updated from:\n    " + self.folder) 
        
        #updates csv dumps
        self.data.save_dfs()
        print("New CSV dumps created.") 
         
if __name__ == '__main__': 
    m = CurrentMonthRowSystem()
    m.toc()
       
