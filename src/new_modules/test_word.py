# -*- coding: utf-8 -*-
"""
Test row reader functions
"""

from ..stream import split_row_by_periods
from ..stream import split_row_by_months, split_row_by_months_and_annual 
from ..label_csv import get_label_on_start,  get_label_in_text
from ..stream import kill_comment, filter_value

# *****************************************************************************

YEAR = 2000
MOS = [x + 1 for x in range(0,12)]
A = [sum(MOS)]

def qtr_range(z): 
    return list(range(z*3, z*3 + 3))    
    
assert qtr_range(0) == list(range(0,3))
assert qtr_range(1) == list(range(3,6))
assert qtr_range(2) == list(range(6,9))
assert qtr_range(3) == list(range(9,12))

def sum_of_months_by_quarter(mos, qn): 
    return sum(x for i, x in enumerate(mos) if i in qtr_range(qn))

QTRS = [sum_of_months_by_quarter(MOS, qn) for qn in [0,1,2,3]]


# *****************************************************************************

def test_row_split1():   
    row = [2007, 6716.2, 897.6, 1414.4, 1744.1, 2660.1, 255.3, 298.0, 344.3, 364.5, 
       472.2, 577.7, 543.1, 584.2, 616.8, 684.7, 740.4, 1235.0]
    y, a, q, m = split_row_by_periods(row)
    assert y == 2007
    assert len (q) == 4
    assert len (m) == 12 
    assert sum (q) == a
    assert sum (m) == a
    
    row = [YEAR] + A + QTRS + MOS 
    y, a, q, m = split_row_by_periods(row)
    assert y == YEAR
    assert q == QTRS
    assert m == MOS
    assert sum (q) == a 
    assert sum (m) == a    
    
def test_row_split2():   
    row = ['1999', '196.9', '203.3', '207.6', '213.1', '216.7', '220.7', '226.5',
                   '221.0', '162.0', '157.1', '150.5', '136.5']
    y, a, q, m = split_row_by_months(row)
    assert y == '1999'
    assert q == None
    assert a == None    
    assert len (m) == 12  

    row = [YEAR] + MOS 
    y, a, q, m = split_row_by_months(row)
    assert y == YEAR
    assert q == None
    assert a == None    
    assert m == MOS
    
def test_row_split3():   
    row = ["1999", '27,00', '22,60', '22,86', '24,18', '24,23', '24,44', '24,22', 
                   '24,19', '24,75', '25,08', '26,05', '26,42', '27,00']
    y, a, q, m = split_row_by_months_and_annual(row)
    assert y == '1999'
    assert q == None
    assert a == '27,00'    
    assert len (m) == 12 
    assert a == m[-1]

    
# *****************************************************************************

def test_labels():
    text = 'отчетный месяц в % к предыдущему месяцу  / reporting month as percent of previous mon'
    lab_dict = {"отчетный месяц в % к предыдущему месяцу" : "prev"}
    assert 'prev' == get_label_on_start(text, lab_dict)
    
    text = 'Производство транспортных средств и оборудования  / Manufacture of  transport equipment'
    lab_dict = {"транспортных средств и оборудования" : "TRANS_EQ"}
    assert 'TRANS_EQ' == get_label_in_text(text, lab_dict)
    
    
# *****************************************************************************
  
    

def test_filter_comment():
    assert kill_comment("20.5 3)") == "20.5"
    
def test_filter_value():
    assert filter_value("20.5 3)") == 20.5    
    assert filter_value ('6512.3 6762.31)') == 6512.3
    
