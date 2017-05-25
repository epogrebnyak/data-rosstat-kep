"""Read parsing specification from yaml file.

Usage:
    
    ParsingDefinition(path)
    
    Class attributes:
       .start
       .end
       .reader
       .units
       .headers
       .varnames       
"""

from collections import OrderedDict
import yaml
from pathlib import Path

from kep.ini import ENCODING
import kep.reader.label as label

# Make yaml load dicts as OrderedDicts - start -------------
_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


def _dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


def _dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))


yaml.add_representer(OrderedDict, _dict_representer)
yaml.add_constructor(_mapping_tag, _dict_constructor)
# ----------------------------------------------------- end

class BaseYAML():
    """Read parsing instruction from string. String format is below:   

    # scope 
    start line: null       # 'start_line'
    end line: null         # 'end_line'
    special reader: null   # 'reader_func'
    ---
    # 'units' section 
    в % к предыдущему периоду: rog
    период с начала отчетного года в % к соответствующему периоду предыдущего года: ytd
    в % к соответствующему периоду предыдущего года: yoy
    ---
    # 'headers' section 
    Объем ВВП: 
     - GDP
     - bln_rub
    Индекс промышленного производства:
     - IND_PROD
"""
       
    def __init__(self, yaml_string):
        """Read and parse data from *yaml_string*."""
        self.content = self.from_yaml(yaml_string)
        self.validate(self.content) 
        
        raw_headers_dict = self.content[2]        
        # dictionary of Label instances
        headers = OrderedDict((k, label.from_list(v)) for k,v in raw_headers_dict .items())        
        # list like [GDP, IND_PROD] with .unique property and .has_duplicates() method 
        varnames = [v[0] for v in raw_headers_dict.values()]
        
        # make parts of yaml accessible as class attributes
        self.attrs = {'start': self.content[0]['start line'],
                      'end': self.content[0]['end line'],
                      'reader': self.content[0]['special reader'],
                      'units': self.content[1],
                      'headers': headers,
                      'varnames': varnames}
        
    @staticmethod
    def validate(content):
        """Check data structure after reading yaml."""
        # yaml was read as a list
        if not isinstance(content, list): 
            raise ValueError("YAML was not read as list")
        # yaml has 3 documents    
        if len(content) != 3:
            raise ValueError("YAML is expected to contain 3 sections")    
        # every doc is an ordered dict
        for part in content:
            if not isinstance(part, OrderedDict):
                raise ValueError("Every section must be read as OrderedDict")
        # first doc has reserved keys 
        for kw in ['start line', 'end line', 'special reader']:
            if not content[0].keys().__contains__(kw):
                msg = "Missing reserved keyword: {}".format(kw)
                raise ValueError(msg)
                
    @staticmethod
    def from_yaml(yaml_string):
        content = list(yaml.load_all(yaml_string))
        # replace every occurence of None with empty OrderedDict
        content = [x if x is not None else OrderedDict() for x in content]
        return content

    def __getattr__(self, name):
        try:
            return self.attrs[name]
        except KeyError:
            raise AttributeError(name)
            
    def __setattr__(self, name, value):
        try:
            self.__dict__[name] = value
        except KeyError:
            raise AttributeError(name)
            
    def __varnames_str__(self, n=10):        
        if len(self.varnames) > n:            
            return ", ".join(self.varnames[:n]) + ", etc."        
        else:
            return ", ".join(self.varnames) 

    def __str__(self):
        txt1 = "{0} variables between line <{1}> and <{2}> read with <{3}>: \n"
        msg1 = txt1.format(len(self.headers), self.start, self.end, self.reader)
        msg2 = self.__varnames_str__()
        return msg1 + msg2

    def __repr__(self):
        msgs = ['start: {}'.format(self.start),
        'end: {}'.format(self.end),
        'reader: {}'.format(self.reader),
        'headers: {}'.format(len(self.headers)),
        'units: {}'.format(len(self.units)),
        'varnames (not unique): {}'.format(", ".join(self.varnames))]
        return "\n".join(msgs)

    def __eq__(self, obj):
        return self.content == obj.content

class ParsingDefinition(BaseYAML):
    
    def __init__(self, path):
        """Read and parse data from file at *path*."""
        yaml_string = Path(path).read_text(encoding=ENCODING)        
        super().__init__(yaml_string) 


class Specification():
    def __init__(self, path, pathlist):
        self.main = ParsingDefinition(path)
        self.extras = [ParsingDefinition(path) for path in pathlist]
        self.__collect_varnames__() 
    
    def __collect_varnames__(self):
        self.varnames = self.main.varnames
        for d in self.extras:
            self.varnames.extend(d.varnames)
            
if __name__ == "__main__":
    import kep.ini as ini
    main_def = ParsingDefinition(path=ini.get_mainspec_filepath())
    more_def = [ParsingDefinition(path) for path in ini.get_additional_filepaths()]
    spec = Specification(path=ini.get_mainspec_filepath(), pathlist=ini.get_additional_filepaths())