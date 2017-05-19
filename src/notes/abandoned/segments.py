import kep.parser.containers as containers 


class SegmentState():
    """
    SegmentState is used in parsing of sequence of headers. It holds information 
    about what parsing specification (segment) applies to current row. The specification 
    switches between current and alternative segments, depending on headers. 
    
    Method .assign_segments(heads) yeilds a sequence of parsing specifications for 
    each element in heads.
    
    SegmentState(default_spec, other_specs).assign_segments(heads)   
    """
    
    DEFAULT_STATE = 1
    ALT_STATE = 0

    def __init__(self, default_spec, other_specs):
        
        self.default_spec = default_spec
        self.specs = other_specs
        self.__reset_to_default_state__()

    @staticmethod
    def is_matched(head, line):
        if line:
            return head.startswith(line)
        else:
            return False

    def update_on_entering_custom_segment(self, head):
        for spec in self.specs:
            if self.is_matched(head, spec.start):
                self.__enter_segment__(spec)

    def update_on_leaving_custom_segment(self, head):
        if self.is_matched(head, self.current_end_line):
            self.__reset_to_default_state__()

    def __reset_to_default_state__(self): 
        # Exit from segment
        self.segment_state = self.DEFAULT_STATE
        self.current_spec = self.default_spec
        self.current_end_line = None

    def __enter_segment__(self, segment_spec):
        self.segment_state = self.ALT_STATE
        self.current_spec = segment_spec
        self.current_end_line = segment_spec.end

    def assign_parsing_definitions(self, csv_dicts):
        for row in csv_dicts:
            if containers.is_data_row(row):
                row.update({'pdef':None})
            else:
                head = row['head']
                if self.segment_state == self.ALT_STATE:
                    self.update_on_leaving_custom_segment(head)
                self.update_on_entering_custom_segment(head)
                row.update({'pdef':self.current_spec})
            yield row
        
import kep.reader.access as reader
csv_dicts = list(reader.get_csv_dicts())   

import kep.ini as ini
main_def = reader.ParsingDefinition(path=ini.get_mainspec_filepath())
more_def = [reader.ParsingDefinition(path) for path in ini.get_additional_filepaths()]

s = SegmentState(main_def, more_def)

for r in s.assign_parsing_definitions(csv_dicts):
    if not containers.is_data_row(r):
        if r['pdef'] != main_def:
            containers.uprint("\n", r['head'])
            containers.uprint(r['pdef'])
            