from definitions import InputDefinition
    
class RowData(InputDefinition):

    def __init__():
        #input defintion __init__
        # make rows a rowsystem 
    

    def is_year(s):    
        # case for "20141)"    
        s = s.replace(")", "")
        try:
           int(s)
           return True        
        except ValueError:
           return False

    def is_textinfo_row(row):
        head = row['list'][0]
        if is_year(head):
           return False
        elif head == '':
           return False
        else:
           return True

    def is_data_row(row):
        if is_year(row['list'][0]):
           return True
        else:
           return False

    def doc_to_rowsystem(input_definition):
        """Import CSV file contents from *input_definition* and return corresponding rowsystem,
           where each line(row) from *input_definition,rows* is presented as a dictionary containing 
           raw data and supplementary information."""
           
        rowsystem = []
        for row in input_definition.rows:
           rs_item = {   'string': row,  # raw string
           #MAYDO: remove 'list'
                           'list': row.split('\t'),  # string separated coverted to list  
                          'label': None, # placeholder for parsing result
                           'spec': None} # placeholder parsing input (specification)
           rowsystem.append(rs_item)
        return rowsystem
