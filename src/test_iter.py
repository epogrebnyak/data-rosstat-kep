# -*- coding: utf-8 -*-
"""
"""

doc = """1.10. Внешнеторговый оборот – всего1),  млрд.долларов США / Foreign trade turnover – total1),  bln US dollars																	
1999	115,1	24,4	27,2	28,4	35,1	7,2	7,9	9,3	9,8	8,0	9,3	9,5	9,3	9,6	10,4	11,1	13,7"""

def test_iter():
    for row in [x.split("\t") for x in doc.split("\n")]:
        yield row
        
doc