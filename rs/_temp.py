import os
fn1 = 'spec1.txt' 
fn2 = 'spec2.txt' 
tempfile ='temp.txt'

a1 = 'line1'
a2 = 'more text'
LINE_1 = a1 + '\t' + a2

CSV_TXT = """{}
2014\t123\t456
в процентах
2014\t200\t300""" .format(LINE_1) 

SPEC_TXT = """start line: {0}
end line: null  
special reader: null   
---
"в процентах" : rog
---
{0}: 
 - VARNAME
 - usd""".format(LINE_1)

CFG_TXT =  """- {0}
- {1}""".format(fn1, fn2)

print(CSV_TXT,SPEC_TXT,CFG_TXT)


# NCOL = 2

# def add_tail(lst, n = NCOL):
    # """Add extra elements at end of lst"""
    # extra_blanks = (len(lst) // n + 1) * n - len(lst)
    # return lst + [' ' for x in range(extra_blanks)]

# def chunks(lst, n = NCOL):
    # """Yield successive n-sized chunks from lst."""
    # for i in range(0, len(lst), n):
        # yield lst[i:i+n]

# def get_max_width_in_list(textlist):
    # return max([len(t) for t in textlist])

# def cell_format(max_width):
    # return "{:<" + str(max_width) + "}"
    
# def printable(textlist, sep = "   "):
    # max_width = get_max_width_in_list(textlist)
    # cell_pattern = cell_format(max_width)    
    # return '\n'.join([sep.join([cell_pattern.format(x) for x in line]) for line in chunks(add_tail(textlist))])

# textlist = ['35462356', 'wrt', 'wergwetrgwegwetg', 'qrgfwertgwqert', 'abc']
# print(printable(textlist))         
        
# import itertools
# TABLE_HEADER = ["Код", "Описание", "Ед.изм."]

# def get_max_widths(table):
    # """
    # For a table with N columns, returns list of N integers,
    # where each element is the maximum width of the corresponding column.

    # Supports incomplete rows with less than N elements.
    # """
    # max_widths = []
    # column_count = 0
    # for row in table:
        # if len(row) > column_count:
            # max_widths.extend([0 for i in range(len(row) - column_count)])
            # column_count = len(max_widths)
        # for i, value in enumerate(row):
            # max_widths[i] = max(max_widths[i], len(value))
    # return max_widths

# def pure_tabulate(iter, header=TABLE_HEADER):
    # """
    # Returns nicely formatted table as a string.
    # """
    # # Calculate column widths
    # table = list(iter)
    # widths = get_max_widths(itertools.chain([header], table))
    # # | Text      | Another text |
    # template =              '| ' + ' | '.join(cell_format(x) for x in widths) + ' |'
    # #                        |:------|:------------------------------------|
    # header_separator_line = '|:' + '-|:'.join('-' * x for x in widths) + '-|'
    # # Format and combine all rows into table
    # rows = itertools.chain([template.format(*header), header_separator_line],
                           # (template.format(*row) for row in table))
    # return '\n'.join(rows)
    
  
# print(pure_tabulate(chunks(add_tail(textlist, n = 3), n = 3), header=TABLE_HEADER))

        