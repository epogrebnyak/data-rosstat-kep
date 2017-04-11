# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 12:18:03 2017

@author: PogrebnyakEV
"""

"""
Todo - General questions
  1. review algorithm, comment where code surprises you
  2. (optional) suggest alternatives for algorithm
  3. suggestions for better naming of vars, funcs
  4. where would you add tests?
  5. (optional) write doctests where appropriate
  6. use PEP 526 annotations
"""

# TODO CRITICAL: upp comments form Upwork

# Not todo below

"""
1. Use different *raw_data* and *parsing_instructions* from file or constants
--------------------------------------------------------------------------
  - csv must read from file, definitions must be read from file
  - csv and definitions may be used in tests as files or hardcoded strings
"""

"""
2. Multiple segments
-----------------
  - this is one segment of file, will have different instructions for different
    parts of CSV file
  - see SegmentState class https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/reader/reader.py#L29
"""

"""
3. Generate variable descriptions:
----------------------------------
describe_var("GDP_yoy") == "Валовый внутренний продукт"
describe_unit("GDP_yoy") == "изменение год к году"
split("GDP_yoy") == "GDP", "yoy"
# Implemented in Label class in reader.label
# https://github.com/epogrebnyak/data-rosstat-kep/blob/master/kep/reader/label.py
# Another strategy - saving text labels from file
#    def get_headlabel_description_dicts(self):
#        return dict([(x["_head"],x["_desc"]) for x in self.get_iter_from_table(self.DB_HEADLABELS)])
4. Possible checks
------------------
Need to prioritize the checks:
  - all variables from definitions are read
  - some datapoints are read and compared to hardcoded values
  - sums round up to priod data
  - rates of change are product of monthly/quarterly rates
  - other?
"""

"""
Not todo
========
New csv file representation
---------------------------
- now a flat list of lines
- may be a container-like group of tables (header + data) + sections and tables organised by section
- good for detecting missing variables, but complicates parser
"""
