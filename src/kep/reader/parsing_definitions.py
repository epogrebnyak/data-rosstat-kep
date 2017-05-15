"""Read parsing specification from yaml file.

Usage:
    
    ParsingDefinition(path)
    
    Class attributes:
       .start
       .end
       .reader
       .units
       .headers
       .all_labels       
"""

from collections import OrderedDict, namedtuple
import yaml

from kep.reader.files import File


# Make yaml load dicts as OrderedDicts - start -------------
_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


def _dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


def _dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))


yaml.add_representer(OrderedDict, _dict_representer)
yaml.add_constructor(_mapping_tag, _dict_constructor)
# ----------------------------------------------------- end



Label = namedtuple("Label", ['varname', 'unit'])

def make_label_from_list(_list):
    if len(_list) >= 2:
        return Label(_list[0], _list[1])
    elif len(_list) == 1:
        return Label(_list[0], None)
    else:
        msg = "\n".join(_list)
        raise ValueError(msg) 

def label_to_str(label):    
    return label.varname + "_" + label.unit

assert make_label_from_list(["GDP", "rog"]) == Label("GDP", "rog")
assert make_label_from_list(["IND"]) == Label("IND", None)



class StringAsYAML():
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
        self.check_parsed_yaml(self.content) 
        # make parts of yaml accessible as class attributes
        labs = [v[0] for v in self.content[2].values()]
        self.attrs = {'start': self.content[0]['start line'],
                      'end': self.content[0]['end line'],
                      'reader': self.content[0]['special reader'],
                      'units': self.content[1],
                      'headers': OrderedDict((k, make_label_from_list(v)) 
                                              for k,v in self.content[2].items()),
                      'all_labels': labs,
                      'unique_labels': sorted(list(set(labs)))
                      }
    def has_same_scope(self, _pd):
        if self.start == _pd.start and self.end == _pd.end \
            and self.reader == _pd.reader:
            return True
        else:
            return False
        
    @staticmethod
    def check_parsed_yaml(content):
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

    def __eq__(self, obj):
        return self.content == obj.content

    def __repr__(self):
        msg1 = "between line <{0}> and <{1}> read with <{2}>"
        msg2 = "{0} variables ({1}...) "
        vars = self.unique_varheads()
        trunc = min(len(vars), 50)
        return (msg2.format(len(self.headers), vars[:trunc]) +               
                msg1.format(self.start, self.end, self.reader))        
    
    def unique_varheads(self):
        vh = [h.varname for h in self.headers.values()]
        return sorted(list(set(vh)))
    
    def __str__(self):
        msgs = ['start: {}'.format(self.start),
        'end: {}'.format(self.end),
        'reader: {}'.format(self.reader),
        'headers: {}'.format(len(self.headers)),
        'units: {}'.format(len(self.units)),
        'unique_labels: {}'.format(", ".join(self.unique_labels))]
        return "\n".join(msgs)
        
def unique(_list):
    return sorted(list(set(_list)))
        
class ParsingDefinition(StringAsYAML):
    
    def __init__(self, path):
        """Read and parse data from file at *path*."""
        yaml_string = File(path).read_text()        
        super().__init__(yaml_string) 

    
if __name__ == "__main__":
    import kep.ini as ini
    main_def = ParsingDefinition(path=ini.get_mainspec_filepath())
    pathlist = ini.get_additional_filepaths()
    more_def = [ParsingDefinition(path) for path in pathlist]
    
    groups = [main_def]
    print("Main parsing definition:\n", groups)
    
    print("""PROBLEM: must use additional parsing definitions in algorithm
 they are imported in *more_def* here but they are not 
 used in containers.py when parsing table headers."
""")
    while more_def:
        p = more_def.pop()
        cur_group = [p]
        for d in more_def:
            if d.has_same_scope(p):
                cur_group.append(d)
                more_def.remove(d)
        print()
        print (cur_group)               
        groups.append(cur_group)