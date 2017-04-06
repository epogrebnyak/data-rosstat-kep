import os
import csv

from kep.config import CSV_PATH
from kep.reader.parsing_definitions import get_definitions
from kep.reader.label import adjust_labels, Label, UnknownLabel
from kep.reader.stream import dicts_as_stream
from kep.reader.file import File


def get_rows():
    return [row.split('\t') for row in File(CSV_PATH).read_text().split('\n')]


def is_year(s):
    # case for "20141)"    
    s = s.replace(")", "")
    try:
        int(s)
        return True
    except ValueError:
        return False


DEFAULT = 1
ALTERNATIVE = 0


class SegmentState():
    """
    SegmentState is used in parsing of sequence of headers. It holds information 
    about what parsing specification (segment) applies to current row. The specification 
    switches between current and alternative segments, depending on headers. 
    
    Method .assign_segments(heads) yeilds a sequence of parsing specifications for 
    each element in heads.
    
    SegmentState(default_spec, other_specs).assign_segments(heads)   
    """

    def __init__(self, default_spec, other_specs):

        self.default_spec = default_spec
        self.specs = other_specs
        self.reset_to_default_state()

    @staticmethod
    def is_matched(head, line):
        if line:
            return head.startswith(line)
        else:
            return False

    def update_if_entered_custom_segment(self, head):
        for segment_spec in self.specs:
            if self.is_matched(head, segment_spec['scope']['start_line']):
                self.enter_segment(segment_spec)

    def update_if_leaving_custom_segment(self, head):
        if self.is_matched(head, self.current_end_line):
            self.reset_to_default_state()

    def reset_to_default_state(self):
        # Exit from segment
        self.segment_state = DEFAULT
        self.current_spec = self.default_spec
        self.current_end_line = None

    def enter_segment(self, segment_spec):
        self.segment_state = ALTERNATIVE
        self.current_spec = segment_spec
        self.current_end_line = segment_spec['scope']['end_line']

    def assign_segments(self, head_sequence):
        spec_sequence = []
        for head in head_sequence:
            # are we in the default spec?
            if self.segment_state == ALTERNATIVE:
                # we are in custom spec  
                # do we have to switch to the default spec? 
                self.update_if_leaving_custom_segment(head)
            self.update_if_entered_custom_segment(head)
            # finished adjusting specification for i-th row
            spec_sequence = spec_sequence + [self.current_spec]
        return spec_sequence


def get_row_head(row):
    if row and row[0]:
        if row[0].startswith("_"):
            pass
        else:
            yield row[0]


class Rows():
    @property
    def enum_row_heads(self):
        for i, row in enumerate(self.rows):
            if row and row[0]:
                yield i, row[0]
            else:
                yield i, ""

    def __init__(self):
        self.rows = get_rows()
        self.default_spec = get_definitions()['default']
        self.segment_specs = get_definitions()['additional']
        _ss = SegmentState(self.default_spec, self.segment_specs)
        heads = [head for i, head in self.enum_row_heads]
        self.specs = _ss.assign_segments(heads)

        """Label rows using markup information from self.specs[i].header_dict
           and .unit_dict. Stores labels in self.labels[i]. 
        """
        self.labels = [UnknownLabel() for _ in self.rows]
        cur_label = UnknownLabel()
        for i, head in self.enum_row_heads:
            if not is_year(head):
                cur_label = adjust_labels(textline=head, incoming_label=cur_label,
                                          dict_headline=self.specs[i]['table_headers'],
                                          dict_unit=self.specs[i]['units'])
            self.labels[i] = Label(cur_label.head, cur_label.unit)

    @property
    def labelled_data_rows(self):
        for i, row in enumerate(self.rows):
            if row and row[0] and is_year(row[0]) \
                    and not self.labels[i].is_unknown():
                yield i, row, self.labels[i], self.specs[i]['reader_func']

    def dicts(self):
        return dicts_as_stream(self)

    # -------------------------------------------------------------------------------
    #
    # Inspection
    #
    # -------------------------------------------------------------------------------

    @property
    def datablock_lines(self):
        SAFE_YEAR = "2009"
        for j, head in self.enum_row_heads:
            if head.startswith(SAFE_YEAR):
                yield j

    @property
    def apparent_headers(self):
        for i, head in self.enum_row_heads:
            if head:
                flag1 = True  #not is_year(head)
                flag2 = "." in head  #"000," not in head
                flag3 = head.strip()[0].isdigit() or head.strip()[1].isdigit()
                if flag1 and flag2 and flag3:
                    yield i, head

    def section_content(self):

        header_lines_numbers = [i for i, h in self.apparent_headers]
        headers = [h for i, h in self.apparent_headers]

        # all line numbers with SAFE_YEAR
        SAFE_YEAR = "2009"
        data_line_numbers = [i for i, head in self.enum_row_heads if head.startswith(SAFE_YEAR)]

        def count_all_between(si, ei, seq=data_line_numbers):
            k = 0
            u = 0
            labs = []
            for s in seq:
                if s >= si and s <= ei:
                    k += 1
                    if self.labels[s].is_unknown():
                        u += 1
                    else:
                        labs.append(self.labels[s].labeltext)
            return k, u, labs

        def cnt_by_seg():
            for t, line in enumerate(header_lines_numbers[0:-1]):
                total, unknowns, labs = count_all_between(header_lines_numbers[t], header_lines_numbers[t + 1])
                yield dict(line_number=line, header=headers[t],
                           total_vars_count=total, unknown_vars_count=unknowns,
                           varibales_read=labs)

        return list(cnt_by_seg())

        def diagnose():
            for z in self.section_content():
                print(make_msg(**z))


def make_msg(line_number, header, total_vars_count, unknown_vars_count,
             varibales_read):
    full = True
    msg = ""

    if full:
        # writing full information about all headers
        msg = header.join("\n" * 2)

    if total_vars_count:
        # we are writing only headers with some data inside
        if unknown_vars_count == 0:
            # everything specified
            if full:
                # ... in full output lets mention it
                msg += "\n".join("    " + lab for lab in varibales_read) + \
                       "\n    Все переменные раздела внесены в базу данных."
        else:
            # ahhhh! there are some undocumented varibales in the section!
            msg = header.join("\n" * 2)
            msg += "\n".join("    " + lab for lab in varibales_read) + \
                   "\n    {0} из {1} переменных внесено в базу данных".format(total_vars_count - unknown_vars_count,
                                                                              total_vars_count)

    return msg


if __name__ == '__main__':
    pass