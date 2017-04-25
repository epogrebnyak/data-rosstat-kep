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

from collections import OrderedDict
import yaml

import config
from files import File


def get_definitions(folder=config.get_default_spec_folder()):
    _path = config.get_main_spec_filepath(folder)
    _path_list = config.get_additional_specs_filepaths(folder)    
    return {'default': ParsingDefinition(path=_path),
            'additional': [ParsingDefinition(path) for path in _path_list]
            }

# Make yaml load dicts as OrderedDicts - start -------------
_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG


def _dict_representer(dumper, data):
    return dumper.represent_dict(data.items())


def _dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))


yaml.add_representer(OrderedDict, _dict_representer)
yaml.add_constructor(_mapping_tag, _dict_constructor)
# ----------------------------------------------------- end

class StringAsYAML():
    """Read parsing instruction from string. String format is similar to YAML_1."""
    
    def __init__(self, yaml_string):
        """Read and parse data from *yaml_string*."""
        self.content = self.from_yaml(yaml_string)
        self.check_parsed_yaml(self.content) 
        # make parts of yaml accessible as class attributes
        self.attrs = {'start': self.content[0]['start line'],
                      'end': self.content[0]['end line'],
                      'reader': self.content[0]['special reader'],
                      'units': self.content[1],
                      # WONTFIX variable names are a list now, but can be a label dict for easier handling later
                      'headers': self.content[2],
                      'all_labels': [v[0] for v in self.content[2].values()]
                      }

    @staticmethod
    def check_parsed_yaml(content):
        """Check data structure after reading yaml."""
        # yaml was read as a list
        if not isinstance(content, list) or len(content) != 3:
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

    def __eq__(self, obj):
        return self.content == obj.content

    def __repr__(self):
        return self.content.__repr__()


class ParsingDefinition(StringAsYAML):

    def __init__(self, path):
        """Read and parse data from file at *path*."""
        yaml_string = File(path).read_text()        
        super().__init__(yaml_string)
