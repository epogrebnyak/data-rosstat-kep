import yaml
from parsing_definitions import get_parsing_definition

SPEC_SAMPLE = """
# 1. Место действия (начальная и конечная строка) и функция для прочтения таблиц
#
start line: null       # 'start_line'
end line: null         # 'end_line'
special reader: null   # 'reader_func'

---
# 2. Единицы измерения (читается в 'unit_dict') 

"в процентах" : percent
---
# 3. Названия и единицы измерения переменных в увязке с 
#    заголовками таблиц ('header_dict')

#1. Сводные показатели / Aggregated indicators
#1.1. Валовой внутренний продукт1) / Gross domestic product1)
#1.1.1. Объем ВВП, млрд.рублей /GDP, bln rubles

Объем ВВП : 
 - GDP
 - bln_rub 
 - 1.1 # section number

Varname header: 
 - VAR1
 - usd
 - 5.1 # section number
 
Another header:
 - VAR2
 - rur
 - 5.2 # section number
""" 

def test_yaml_structure():    
    assert list(yaml.load_all(SPEC_SAMPLE)) == \
    [{'end line': None, 'special reader': None, 'start line': None},
     {'в процентах': 'percent'},
     {'Another header': ['VAR2', 'rur', 5.2],
      'Varname header': ['VAR1', 'usd', 5.1],
      'Объем ВВП': ['GDP', 'bln_rub', 1.1]}]

def test_segment_definition(tmpdir):   
    # tmpdir is defined internally in pytest
    # described here: https://docs.pytest.org/en/latest/tmpdir.html#the-tmpdir-fixture
    # see also: http://stackoverflow.com/questions/36070031/creating-a-temporary-directory-in-pytest
    p = tmpdir.join("sample.txt")
    p.write_text(SPEC_SAMPLE, 'utf-8')
    assert p.read_text('utf-8') == SPEC_SAMPLE
    assert get_parsing_definition(p) == \
    {'scope': {'end_line': None, 'start_line': None},
     'reader_func': None,
     'units': {'в процентах': 'percent'},
     'table_headers': {
       'Another header': ['VAR2', 'rur', 5.2],
       'Varname header': ['VAR1', 'usd', 5.1],
       'Объем ВВП'     : ['GDP', 'bln_rub', 1.1]}     
    }