# TODO: move testing away to a new file 

import itertools

SEP = "_"

class Label():
    def __init__(self, *arg):
        self._head = None
        self._unit = None
        
        if len(arg) == 1:
            if isinstance(arg[0], str):    
                self.labeltext = arg[0] 
        if len(arg) == 2:
            self._head = arg[0]
            self._unit = arg[1]
            
    @property
    def labeltext(self):        
        return self.combine(self._head, self._unit)

    @labeltext.setter
    def labeltext(self, value):
        if SEP in value:
           self._head = self._get_head(value)
           self._unit = self._get_unit(value)

    @property
    def head(self):        
        return self._head
        
    @head.setter
    def head(self, value):
        self._head = value        
        
    @property     
    def unit(self):        
        return self._unit
        
    @unit.setter
    def unit(self, value):
        self._unit = value         
        
    def __repr__(self):
        return str(self.labeltext) # "Label: " + str(self.full) + " (head: " + str(self._head) + ", unit: " + str(self._unit) + ")"
        
    @property    
    def dict(self):
        return {'label':self.label, 'head':self._head, 'unit':self._unit}
        
    @staticmethod    
    def _get_head(name):
        words = name.split('_')
        return '_'.join(itertools.takewhile(lambda word: word.isupper(), words))

    @staticmethod
    def _get_unit(name):
        words = name.split('_')
        return '_'.join(itertools.dropwhile(lambda word: word.isupper(), words))

    @staticmethod
    def combine(head, unit):
        if len(str(head)+str(unit)):
           return str(head) + SEP + str(unit)
        else:
           return ''
        
    def __eq__(self, obj):
        if self._head == obj.head and self._unit == obj.unit:
            return True      
        else:
            return False   

class UnknownLabel(Label):
     def __init__(self):
        self._head = "UNKNOWN"
        self._unit = "unknown"
            

def which_label_on_start(text, lab_dict):      
     for pat in lab_dict.keys():
           if text.strip().startswith(pat):
                return lab_dict[pat]
     
def which_label_in_text(text, lab_dict):
     for pat in lab_dict.keys():
           if pat in text:
               return lab_dict[pat]

def adjust_labels(textline, incoming_label, dict_headline, dict_unit):

     """Set new primary and secondary label based on *line* contents. *line* is first element of csv row.    

    line = 'Производство транспортных средств и оборудования  / Manufacture of  transport equipment                                                
            ... causes change in primary (header) label
    
    line = 'отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous mon
            ... causes change in secondary (unit) label
    
    ASSUMPTIONS:
      - primary label appears only once in csv file (may not be true, need to use segments then)
      - primary label followed by secondary label 
      - secondary label always at start of the line 
    """
    
    # *_sr stands for 'search result'
    headline_sr = which_label_in_text(textline, dict_headline)             
    unit_sr = which_label_on_start(textline, dict_unit)  

    if headline_sr:
       adjusted_label = Label(*headline_sr)
    elif unit_sr:
       adjusted_label = incoming_label
       adjusted_label.unit = unit_sr 
    else:
       adjusted_label = UnknownLabel()
       
    return adjusted_label

    
def label(rs, id):    

    rs = assign_parsing_specification_by_row(rs, id)
    return label_rowsystem(rs, id)
        

def label_rowsystem(rs, id):
    """Label data rows in rowsystems *rs* using markup information from id*.
       Returns *rs* with labels added in 'head_label' and 'unit_label' keys. 
    """

    # run label adjuster     
    cur_label = UnknownLabel()    
    for i, row in enumerate(rs):
       if is_textinfo_row(row):            
              adj_label = adjust_labels(line=row['string'],
                                        incoming_label=cur_label, 
                                        dict_headline = row['spec'].header_dict, 
                                        dict_unit = row['spec'].unit_dict)
              rs[i]['label'] = adj_label
              cur_label = adj_label
       else:
              rs[i]['label'] = cur_label
             
    return rs    

# -----------------------------------------------------------------------------
# assign_parsing_specification_by_row    

def emit_rowheads(rs):
    for i, row in enumerate(rs):
       try:
           head = row['list'][0]
           if head:
              yield i, head              
       except:
           pass   
   
class _SegmentInfo():

   def __init__(self, id):
   	self.id = id
   	self.in_segment = False
        self.current_end_line = None
        self.current_spec = id.default_spec
        self.default_spec = id.default_spec
        
    @staticmethod	
    def is_matched(head, line):
        if line:
	    return head.startswith(line)
	else:
	    return False  

   def update_if_entered_custom_segment(self, head):
	for segment_spec in self.id.segments:
	       if self.is_matched(head, segment_spec.start_line):
	            self.enter_segment(segment_spec)
	            
   def update_if_leaving_custom_segment(self, head):	
   	if self.is_matched(head,self.current_end_line):
                switch.reset_to_default(self)
	
   def reset_to_default(self):
        self.in_segment = False
        self.current_spec = id.default_spec
        self.current_end_line = None
       
   def enter_segment(self, segment_spec):
        self.in_segment = True
        self.current_spec = segment_spec
        self.current_end_line = segment_spec.end_line
   	

def assign_parsing_specification_by_row(rs, id):
    
    switch = _SegmentInfo(id)
    
    # no segment information
    if not id.segments:
    	for i, head in emit_rowheads(rs):
    	     rs[i]['spec'] = id.default_spec
        return rs
    
    for i, head in emit_rowheads(rs):
        # are we in the default spec?
        if switch.in_segment:
            # we are in custom spec. do we have to switch to the default spec? 
            switch.update_if_leaving_custom_segment(head)  
            # should we also now switch to custom spec?
            switch.update_if_entered_custom_segment(head)
        else:
            # should we switch to custom spec?
            switch.update_if_entered_custom_segment(head)
        #finished adjusting specification for i-th row 
        rs[i]['spec'] = current_spec
    return rs
    
    
text = "This is line 1 here"
lab_dict1 = {"This is": 1}
lab_dict2 = {"line": [2, 100]}

assert which_label_on_start(text, lab_dict1) == 1
assert which_label_on_start(text, lab_dict2) is None
assert which_label_in_text(text, lab_dict1) == 1
assert which_label_in_text(text, lab_dict2) == [2, 100]


test_curlabel = Label('SOMETHING_here')
testline1 = "This is line 1 here"
testline2 = "what unit is this?"
testline3 = "..."
dict_headline = {"line 1": ['I', 'rub']}
dict_support  = {"what": 'usd'}

assert "I_rub"         == adjust_labels(testline1, test_curlabel, dict_headline, dict_support).labeltext
assert "SOMETHING_usd" == adjust_labels(testline2, test_curlabel, dict_headline, dict_support).labeltext       
assert UnknownLabel()  == adjust_labels(testline3, test_curlabel, dict_headline, dict_support)

