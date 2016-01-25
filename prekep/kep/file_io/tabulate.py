import itertools

TABLE_HEADER = ["Код", "Описание", "Ед.изм."]

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

def pure_tabulate(table, header=TABLE_HEADER):
    """
    Returns nicely formatted table as a string.
    """
    # Calculate column widths
    widths = get_max_widths(itertools.chain([header], table))
    # Template for header and rows.
    # | Text      | Another text |
    template = '| ' + ' | '.join(('{:<%s}' % x) for x in widths) + ' |'
    # Special string for the separator line below header.
    # |:----------|:-------------|
    header_separator_line = '|:' + '-|:'.join('-' * x for x in widths) + '-|'
    # Format and combine all rows into table
    rows = itertools.chain([template.format(*header), header_separator_line],
                           (template.format(*row) for row in table))
    return '\n'.join(rows)
