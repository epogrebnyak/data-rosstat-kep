# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 08:38:34 2015

@author: EP
"""

# ----------------

def label_raw_rows_by_spec(raw_rows, default_spec, segment_specs):
    labels = UNKNOWN_LABELS[:]

    in_segment = False
    current_spec = default_spec
    current_end_line = None

    labelled_rows = []

    for row in raw_rows:

        if not row[0]:
            # junk row
            continue

        # Are we in the default spec?
        if not in_segment:
            # Do we have to switch to a custom one?
            for start_line, end_line, spec in segment_specs:
                if row[0].startswith(start_line):
                    # Yes!
                    in_segment = True
                    current_spec = spec
                    current_end_line = end_line
                    break
        else:
            # We are in a custom spec. Do we have to switch to the default one?
            if row[0].startswith(current_end_line):
                in_segment = False
                current_spec = default_spec
                current_end_line = None

        # Spec has been possibly switched, now may have to adjust labels
        if not is_year(row[0]):
            # label-switching row
            labels = adjust_labels(row[0], labels, current_spec)
        else:
            # data row
            labelled_rows.append(labels + row)

    return labelled_rows


