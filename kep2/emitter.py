# -*- coding: utf-8 -*-

from .containers import get_blocks, get_year
from .utils import filter_value

def yield_datapoints(row_tuple: list, varname: str, year: int) -> iter:
    """Yield dictionaries containing individual datapoints based on *row_tuple* content.    
    
    :param row_tuple: tuple with annual value and lists of quarterly and monthly values
    :param varname: string like 'GDP_yoy'
    :param year: int
    :return: dictionaries ready to feed into pd.Dataframe
    """
    # a - annual value, just one number
    # qs - quarterly values, list of 4 elements
    # ms - monthly values, list of 12 elements
    a, qs, ms = row_tuple

    # annual value, yield if present
    if a:
        yield {'freq': 'a',
               'varname': varname,
               'year': year,
               'value': filter_value(a)}
    # quarterly values, yield if present
    if qs:
        for i, val in enumerate(qs):
            if val:
                yield {'freq': 'q',
                       'varname': varname,
                       'year': year,
                       'qtr': i + 1,
                       'value': filter_value(val)}
    # quarterly values, yield if present
    if ms:
        for j, val in enumerate(ms):
            if val:
                yield {'freq': 'm',
                       'varname': varname,
                       'year': year,
                       'month': j + 1,
                       'value': filter_value(val)}

               
def datablock_to_stream(label, datarows, splitter_func):
    if label:        
        for row in datarows:
            a, qs, ms = splitter_func(row['data']) 
            for dp in yield_datapoints(row_tuple=(a, qs, ms),
                               year=get_year(row['head']),
                               varname=label):
                yield dp


class Datapoints():
    """Emit a stream datapoints from *csv_dicts* according to *parse_def*."""

    def __init__(self, csv_dicts, parse_def):
        """
        csv_dicts: iterable of dictionaries with csv file content by row
                   each dictionary has 'head', 'data'
                   generated by CSV_Reader(path).yield_dicts()              
        parse_def: object containing header dict, units dict and splitter func name
                   generated by ParsingDefinition(path)
        """
        
        self.blocks = get_blocks(csv_dicts, parse_def)
        self.datapoints = list(self.walk_by_blocks())

    def walk_by_blocks(self):
        for block in self.blocks:
            for datapoint in datablock_to_stream(label=block.label
                                               , datarows=block.datarows
                                               , splitter_func=block.splitter_func):
                yield datapoint                
      
    def emit(self, freq):
        """Returns generator of dictionaries of datapoints as formatted 
           by yield_datapoints().
           
           param freq: 'a', 'q' or 'm' 
        """
        if freq in 'aqm':
            for p in self.datapoints:
                if p['freq'] == freq:
                    # Note: (1) 'freq' key will be redundant for later use in
                    #           dataframe, drop it
                    #       (2) without copy() pop() changes self.datapoints
                    z = p.copy()
                    z.pop('freq')
                    yield z
        else:
            raise ValueError(freq)

if __name__ == "__main__":
    # inputs
    import this
    csv_dicts, parse_def = this.get_csv_data_and_definition()

    # walk by blocks
    blocks = get_blocks(csv_dicts, parse_def)
    for b in blocks:
        if b.label:
            values = list(datablock_to_stream(label=b.label
                                            , datarows=b.datarows
                                            , splitter_func=b.splitter_func))
            #print(b.label, len(b.datarows))
            #print(values[0])
            
    # dataset
    d = Datapoints(csv_dicts, parse_def)
    output = list(d.emit('a'))
    
# TODO: need more information displayed about
#       place
#    """WARNING: unexpected row with length 3"""