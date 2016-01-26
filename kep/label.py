# -*- coding: utf-8 -*-
"""Class Label to store variable labels and adjust_labels() procedure to go through labels for rows in csv file."""

import itertools
from db import DefaultDatabase

SEP = "_"
FILLER = "<...>"


def yield_var_name_components(self):        
    """Yields a list containing variable name, text description and unit of measurement."""        
    for var_name in self.get_saved_full_labels():
        lab = Label(var_name)
        yield [lab.labeltext, lab.head, lab.unit_description]

UNITS_ABBR = {
# --- part from unit dicts
    'rog': 'в % к предыдущему периоду',
    'rub': 'рублей',
    'yoy': 'в % к аналог. периоду предыдущего года' ,
    'ytd': 'с начала года',
# --- part from header dicts
    'bln_t_km':    'млрд. т-км',
    'percent':     '%',
    'bln_rub':     'млрд. руб.',
    'bln_rub_fix': 'млрд. руб. (в фикс. ценах)',
    'mln':   'млн. человек',
    'mln_t': 'млн. т',
    'TWh':   'млрд. кВт·ч',
    'eop':   'на конец периода',
    'bln':   'млрд.',
    'units': 'штук',
    'th':    'тыс.'
}

def get_unit(name):
    unit_abbr = get_unit_abbr(name)
    if unit_abbr in UNITS_ABBR.keys():
        return UNITS_ABBR[unit_abbr]
    else:
        return FILLER 

class Label():

    headlabel_reverse_desc_dict = DefaultDatabase().headlabel_desc_dicts

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
        try:
           return self.headlabel_reverse_desc_dict[self._head]
        except:
           return FILLER 
            
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
    
    line = 'Производство транспортных средств и оборудования  / Manufacture of  transport equipment'                                                
            ... causes change in primary (header) label
    
    line = 'отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous mon'
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