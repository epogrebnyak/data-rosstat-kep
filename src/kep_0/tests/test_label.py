# -*- coding: utf-8 -*-
from kep.reader.label import which_label_on_start, which_label_in_text, adjust_labels, UnknownLabel, Label

def test_labels():
    z = Label()
    r = z
    z.label = "THIS_VAR_some_unit"
    r.head = "THIS_VAR"
    r.unit = "some_unit"
    w = Label("THIS_VAR_some_unit")
    q = Label("THIS_VAR", "some_unit")  
    assert z == w
    assert w == q
    assert z == r
    assert Label()._get_head('PROD_E_TWh') == 'PROD_E' 
    assert Label()._get_unit('PROD_E_TWh') == 'TWh'

    
text = "This is line 1 here"
lab_dict1 = {"This is": 1}
lab_dict2 = {"line": [2, 100]}

def test_inclusion_funcs():
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

def test_adjust_labels():
    assert "I_rub"         == adjust_labels(testline1, test_curlabel, dict_headline, dict_support).labeltext
    assert "SOMETHING_usd" == adjust_labels(testline2, test_curlabel, dict_headline, dict_support).labeltext       
    assert UnknownLabel()  == adjust_labels(testline3, test_curlabel, dict_headline, dict_support)    