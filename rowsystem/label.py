# TODO: move testing away to a new file 

import itertools

SEP = "_"

FILLER = "<...>"

UNITS_ABBR = {
# --- part from default_dicts [0]
    'rog':'в % к предыдущему периоду',
    'rub':'рублей',
    'yoy':'в % к аналог. периоду предыдущего года' ,
# --- part from default_dicts [1],
    'bln_t_km': 'млрд. т-км',
    'percent': '%',
    'bln_rub': 'млрд. руб.',
    'bln_rub_fix': 'млрд. руб. (в фикс. ценах)',
    'mln': 'млн. человек',
    'mln_t': 'млн. т',
    'TWh': 'млрд. кВт·ч',
    'eop': 'на конец периода',
    'bln': 'млрд.',
    'units': 'штук',
    'th': 'тыс.',
}


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

    @property    
    def unit_description(self):
        if self.unit in UNITS_ABBR.keys():
            return UNITS_ABBR[self.unit]
        else:
            return FILLER 

    @property    
    def head_description(self):
        return self.head + " " + FILLER         
        
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

    def is_unknown(self): 
        return self._head == UnknownLabel()._head                    






def get_unit(name):
    unit_abbr = get_unit_abbr(name)
    if unit_abbr in UNITS_ABBR.keys():
        return UNITS_ABBR[unit_abbr]
    else:
        return FILLER 


        
            
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
       adjusted_label = Label(incoming_label.head, incoming_label.unit)
       adjusted_label.unit = unit_sr 
    else:
       adjusted_label = UnknownLabel()
       
    return adjusted_label

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# testing
    
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
