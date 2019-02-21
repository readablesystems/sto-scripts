#!/usr/bin/env python3

import config
import json
import csv

from runner import BenchRunner as br

WILLIAM_TRIALS = 5

tpcc_sys_name_map = {
    'name': 'tpcc',
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

wiki_sys_name_map = {
    'name': 'wiki',
    'OCC (W1)': 'o/1',
    'OCC + CU (W1)': 'o.c/1',
    'OCC (W1) + SV': 'o.s/1',
    'OCC + CU (W1) + SV': 'o.c.s/1',
    'MVCC (W1)': 'm/1',
    'MVCC (W1) + ST + IV': 'm.s.i/1',
    'MVCC + CU (W1)': 'm.c/1',
    'MVCC + CU (W1) + ST + IV': 'm.c.s.i/1',
}

rubis_sys_name_map = {
    'name': 'rubis',
    'OCC (W1)': 'o/1',
    'OCC + CU (W1)': 'o.c/1',
    'OCC (W1) + SV': 'o.s/1',
    'OCC + CU (W1) + SV': 'o.c.s/1',
    'MVCC (W1)': 'm/1',
    'MVCC (W1) + ST + IV': 'm.s.i/1',
    'MVCC + CU (W1)': 'm.c/1',
    'MVCC + CU (W1) + ST + IV': 'm.c.s.i/1',
}

tpcc_out_file = config.get_result_file(config.MVSTOConfig.NAME)
tpcc_result_file = 'tpcc_results.txt'
wiki_out_file = config.get_result_file(config.MVSTOWikiConfig.NAME)
wiki_result_file = 'wiki_results.txt'
rubis_out_file = config.get_result_file(config.MVSTORubisConfig.NAME)
rubis_result_file = 'rubis_results.txt'


def convert(infile, sys_name_map, compatible_results):
    is_tpcc = sys_name_map['name'] == 'tpcc'

    sys_name_reverse_map = {}
    sys_short_names = []

    for k,v in sys_name_map.items():
        if k == 'name':
            continue
        sys_name_reverse_map[v] = k
        sys_short_names.append(v)

    try:
        with open(infile, 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                for v in sys_short_names:
                    long_name = sys_name_reverse_map[v]
                    for i in range(WILLIAM_TRIALS):
                        (d2, d3) = v.split('/')
                        runner_key = br.key(d1, d2, d3, i)
                        col_key = long_name
                        if is_tpcc:
                            col_key += ' + OB'
                        col_key += ' [T{}]'.format(i+1)
                        xput = float(row[col_key])
                        compatible_results[runner_key] = (xput, 0.0, 0.0)
    except (FileNotFoundError, IOError):
        return {}
    return compatible_results


def convert_cicada(compatible_results):
    try:
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
    except (FileNotFoundError, IOError):
        return {}
    return compatible_results


if __name__ == '__main__':
    results = {}
    results = convert(tpcc_result_file, tpcc_sys_name_map, results)
    results = convert_cicada(results)
    if results:
        with open(tpcc_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert(wiki_result_file, wiki_sys_name_map, results)
    if results:
        with open(wiki_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert(rubis_result_file, rubis_sys_name_map, results)
    if results:
        with open(rubis_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)

