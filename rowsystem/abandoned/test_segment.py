#-------------------------------------------------------------------------------------

RS_SEG_TEST = [{'list':['string1 + more text'],      'spec': None}
             , {'list':[''],                         'spec': None}
             , {'list':[None],                       'spec': None}
             , {'list':None,                         'spec': None}
             , {'list':[],                           'spec': None}
             , {'list':['string2 + even more text'], 'spec': None}
             , {'list':['string3 with some text'],   'spec': None}
             , {'list':['string4 and that is it'],   'spec': None}
             ]

RS_SEG_TEST_OUTPUT = [{'list': ['string1 + more text'], 'spec': 1},
 {'list': [''], 'spec': None},
 {'list': [None], 'spec': None},
 {'list': None, 'spec': None},
 {'list': [], 'spec': None},
 {'list': ['string2 + even more text'], 'spec': 0},
 {'list': ['string3 with some text'], 'spec': 2},
 {'list': ['string4 and that is it'], 'spec': 3}]

SEG_SPEC_TEST = [('string1 + more text',   'string2 + even more text', 1)
                 ,('string3 with some text', 'string4 and that is it',  2)
                 ,('string4 and that is it', None,                      3)]

DEFAULT_DICTS = 0 

from rowsystem import assign_parsing_specification_by_row
def test_segment():
    assert RS_SEG_TEST_OUTPUT == assign_parsing_specification_by_row(RS_SEG_TEST, DEFAULT_DICTS, SEG_SPEC_TEST)

#-------------------------------------------------------------------------------------

