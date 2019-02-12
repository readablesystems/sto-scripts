#/usr/bin/env python3

import config
import json
import csv

from runner import BenchRunner as br
from plotter import BenchPlotter as bp

WILLIAM_TRIALS = 5

sys_name_map = {
    'OCC (W1)': 'o/1',
    'OCC + CU (W1)': 'o.c/1',
    'OCC (W4)': 'o/4',
    'OCC + CU (W4)': 'o.c/4',
    'OCC (W1) + SV': 'o.s/1',
    'OCC + CU (W1) + SV': 'o.c.s/1',
    'OCC (W4) + SV': 'o.s/4',
    'OCC + CU (W4) + SV': 'o.c.s/4',
    'MVCC (W1)': 'm/1',
    'MVCC (W1) + ST + IV': 'm.s.i/1',
    'MVCC + CU (W1)': 'm.c/1',
    'MVCC (W4)': 'm/4',
    'MVCC (W4) + ST + IV': 'm.s.i/4',
    'MVCC + CU (W4)': 'm.c/4',
    'MVCC + CU (W1) + ST + IV': 'm.c.s.i/1',
    'MVCC + CU (W4) + ST + IV': 'm.c.s.i/4'
}

outfile = config.get_result_file(config.MVSTOConfig.NAME)
infile = 'results.txt'

sys_name_reverse_map = {}
sys_short_names = []

compatible_results = {}

for k,v in sys_name_map.items():
    sys_name_reverse_map[v] = k;
    sys_short_names.append(v)

with open(infile, 'r') as rf:
    reader = csv.DictReader(rf)
    for row in reader:
        d1 = row['# Threads']
        for v in sys_short_names:
            long_name = sys_name_reverse_map[v]
            for i in range(WILLIAM_TRIALS):
                (d2, d3) = v.split('/')
                runner_key = br.key(d1, d2, d3, i)
                xput = float(row[long_name + ' + OB [T{}]'.format(i+1)])
                compatible_results[runner_key] = (xput, 0.0, 0.0)

with open('c-1w-results.txt', 'r') as rf:
    reader = csv.DictReader(rf)
    for row in reader:
        d1 = row['# Threads']
        d2 = 'c'
        d3 = '1'
        for i in range(WILLIAM_TRIALS):
            runner_key = br.key(d1,d2,d3,i)
            xput = float(row['Cicada (W1)' + ' [T{}]'.format(i+1)]) * 1000000.0
            compatible_results[runner_key] = (xput, 0.0, 0.0)

with open('c-4w-results.txt', 'r') as rf:
    reader = csv.DictReader(rf)
    for row in reader:
        d1 = row['# Threads']
        d2 = 'c'
        d3 = '4'
        for i in range(WILLIAM_TRIALS):
            runner_key = br.key(d1,d2,d3,i)
            xput = float(row['Cicada (W4)' + ' [T{}]'.format(i+1)]) * 1000000.0
            compatible_results[runner_key] = (xput, 0.0, 0.0)

with open(outfile, 'w') as wf:
    json.dump(compatible_results, wf, indent=4, sort_keys=True)
