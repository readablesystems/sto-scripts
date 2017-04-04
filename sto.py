#!/usr/bin/env python

import re

class profile_parser:
    patterns = {
        'time': 'real time: ([0-9\.]*)',
        'aborts': '([0-9]*) \(([0-9\.]*)%\) aborts',
        'hcos': '\$ ([0-9]*) HCO',
        'hco_filter_rate': 'out of [0-9]* check attempts \(([0-9\.]*)%\)'
    }

    types = {
        'time': 'float',
        'aborts': 'int',
        'hcos': 'int',
        'hco_filter_rate': 'float'
    }

    @classmethod
    def extract(cls, metric, text):
        s = re.search(cls.patterns[metric], text).group(1)
        return float(s)
