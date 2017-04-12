# -*- coding: utf-8 -*-
"""Variable label handling."""


def make_label(var, unit):
    """Costruct a dictionary based on *var* and *unit*."""
    return {'var': var, 'unit': unit}

EMPTY_LABEL = make_label("", "")

def concat_label(label: dict)-> str:
    """Return string repesenting *label* dictionary.
    
    >>> concat_label({'var': 'GDP', 'unit': 'yoy'})
    'GDP_yoy'"""
    if not isinstance(label, dict):
        raise ValueError(label)
    return label['var'] + "_" + label['unit']

# TODO LOW: bring back splitting of label to head and unit from 