import re

class ProfileParser:
    patterns = {
        'bench_xput': 'Throughput: ([0-9\.]*) txns/sec',
        'time': 'real time: ([0-9\.]*)',
        'commits': ', ([0-9]*) commits',
        'aborts': '[0-9]* \(([0-9\.]*)%\) aborts',
        'hcos': '\$ ([0-9]*) HCO',
        'hco_filter_rate': 'out of [0-9]* check attempts \(([0-9\.]*)%\)',
        'commit_time_aborts' : '[0-9]* \(([0-9\.]*)%\) of aborts at commit time',
        'lock_aborts' : '[0-9]* \(([0-9\.]*)%\) of aborts due to lock time-outs',
        'observe_lock_aborts' : '[0-9]* \(([0-9\.]*)%\) of aborts due to observing write-locked versions',
        'commit_attempts' : '([0-9]*) commit attempts',
        'nonopaque' :  '[0-9]* \(([0-9\.]*)%\) nonopaque'
    }

    types = {
        'time': 'float',
        'aborts': 'int',
        'hcos': 'int',
        'hco_filter_rate': 'float'
    }

    @classmethod
    def extract(cls, metric, text):
        m = re.search(cls.patterns[metric], text)
        if m is not None:
            s = m.group(1)
            return float(s)
        else:
            return 0.0
