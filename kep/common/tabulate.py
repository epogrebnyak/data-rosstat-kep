"""Formatting of output by column and for markdown."""

# -----------------------------------------------------------------
# Functions:
#    pure_tabulate(iter, header=TABLE_HEADER)
#    printable(textlist, sep = " "):
# -----------------------------------------------------------------

NCOL = 2

def add_tail(lst, n = NCOL):
    """Add extra elements at end of lst"""
    extra_blanks = (len(lst) // n + 1) * n - len(lst)
    return lst + [' ' for x in range(extra_blanks)]

def chunks(lst, n = NCOL):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def get_max_width_in_list(textlist):
    return max([len(t) for t in textlist])

def cell_format(max_width):
    return "{:<" + str(max_width) + "}"
    
def printable(textlist, sep = " "):
    """Returns a string with elements of *testlist* printied by NCOL columns."""
    max_width = get_max_width_in_list(textlist)
    cell_pattern = cell_format(max_width)    
    return '\n'.join([sep.join([cell_pattern.format(x) for x in line]) for line in chunks(add_tail(textlist))])

#----------------------------------------------------------------------------------------------------------------
        
import itertools
TABLE_HEADER = ["Код", "Описание", "Ед.изм.", "Частота"]

def get_max_widths(table):
    """
    For a table with N columns, returns list of N integers,
    where each element is the maximum width of the corresponding column.

    Supports incomplete rows with less than N elements.
    """
    max_widths = []
    column_count = 0
    for row in table:
        if len(row) > column_count:
            max_widths.extend([0 for i in range(len(row) - column_count)])
            column_count = len(max_widths)
        for i, value in enumerate(row):
            max_widths[i] = max(max_widths[i], len(value))
    return max_widths

def pure_tabulate(iter, header=TABLE_HEADER):
    """Returns markdown-formatted table as a string.
    
    TABLE_HEADER = ["Код", "Описание", "Ед.изм.", "Частота"]
    textlist = ['35462356', 'wrt', 'wergwetrgwegwetg', 'qrgfwertgwqert', 'abc']
    
    result should be like below
    
    | Код            | Описание | Ед.изм.          | Частота |
    |:---------------|:---------|:-----------------|:--------|
    | 35462356       | wrt      | wergwetrgwegwetg |         |
    |:---------------|:---------|:-----------------|:--------|
    | qrgfwertgwqert | abc      |                  |         |
    |:---------------|:---------|:-----------------|:--------|
    
    """
    # Calculate column widths
    table = list(iter)
    widths = get_max_widths(itertools.chain([header], table))
    # | Text      | Another text |
    template =              '| ' + ' | '.join(cell_format(x) for x in widths) + ' |'
    #                        |:------|:------------------------------------|
    header_separator_line = '|:' + '-|:'.join('-' * x for x in widths) + '-|'

    # Format and combine all rows into table
    # If tablo row has less elements than widths, new elements must be added to the row.
    # Otherwise template.format(*row) will fail due to the missing elements.
    rows = [template.format(*header), header_separator_line]
    column_count = len(widths)
    for row in table:
        if column_count > len(row):
            col = column_count - len(row)
            row += [''] * col
        rows.extend((template.format(*row), header_separator_line))

    return '\n'.join(rows)

if __name__ == '__main__':
    textlist = ['35462356', 'wrt', 'wergwetrgwegwetg', 'qrgfwertgwqert', 'abc']
    print(printable(textlist))     
    print(pure_tabulate(chunks(add_tail(textlist, n = 3), n = 3), header=TABLE_HEADER))
