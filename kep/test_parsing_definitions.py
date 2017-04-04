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

# todo - may need write the file 
_path = 'spec_sample.txt'

def test_yaml_structure():    
    assert list(yaml.load_all(SPEC_SAMPLE)) == \
    [{'end line': None, 'special reader': None, 'start line': None},
     {'в процентах': 'percent'},
     {'Another header': ['VAR2', 'rur', 5.2],
      'Varname header': ['VAR1', 'usd', 5.1],
      'Объем ВВП': ['GDP', 'bln_rub', 1.1]}]

def test_segment_definition():        
    assert get_parsing_definition(_path) == \
    {'scope': {'end_line': None, 'start_line': None},
     'reader_func': None,
     'units': {'в процентах': 'percent'},
     'table_headers': {
       'Another header': ['VAR2', 'rur', 5.2],
       'Varname header': ['VAR1', 'usd', 5.1],
       'Объем ВВП'     : ['GDP', 'bln_rub', 1.1]}     
    }