# -*- coding: utf-8 -*-
"""
Created on Thu May 25 17:49:25 2017

@author: PogrebnyakEV
"""

def parse_section_name(s: str)->bool:
    """Check if string is section name.
    """
    # Regex: number, than (dot followed by number) repeated 1-3 times
    # that maybe dot
    # than space than one or more symbols
    match = re.match(r'^(\d+(\.\d+){0,3})\.? .+$', s)
    if match:
        return match.group(1)
    else:
        return None
    
    
    
        def __parse_sections__(self):
        # get section number
        # there can be more than one section number in block, keep all for now
        self.sections = []
        for row in self.headers:
            # update section number
            new_section_number = parse_section_name(row['head'])
            if new_section_number:
                self.sections.append(new_section_number)