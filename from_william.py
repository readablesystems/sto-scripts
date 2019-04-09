#!/usr/bin/env python3

import config
import json
import csv

from runner import BenchRunner as br

WILLIAM_TRIALS = 5

tpcc_sys_name_map = {
    'name': 'tpcc',
    'OCC (W0)': 'o/0',
    'OCC + CU (W0)': 'o.c/0',
    'OCC (W0) + SV': 'o.s/0',
    'OCC + CU (W0) + SV': 'o.c.s/0',
    'OCC (W1)': 'o/1',
    'OCC + CU (W1)': 'o.c/1',
    'OCC (W1) + SV': 'o.s/1',
    'OCC + CU (W1) + SV': 'o.c.s/1',
    'OCC (W4)': 'o/4',
    'OCC + CU (W4)': 'o.c/4',
    'OCC (W4) + SV': 'o.s/4',
    'OCC + CU (W4) + SV': 'o.c.s/4',
    'MVCC (W0)': 'm/0',
    'MVCC (W0) + ST': 'm.s/0',
    'MVCC + CU (W0)': 'm.c/0',
    'MVCC + CU (W0) + ST': 'm.c.s/0',
    'MVCC (W1)': 'm/1',
    'MVCC (W1) + ST': 'm.s/1',
    'MVCC + CU (W1)': 'm.c/1',
    'MVCC + CU (W1) + ST': 'm.c.s/1',
    'MVCC (W4)': 'm/4',
    'MVCC (W4) + ST': 'm.s/4',
    'MVCC + CU (W4)': 'm.c/4',
    'MVCC + CU (W4) + ST': 'm.c.s/4'
}

tpcc_factors_sys_name_map = {
    'name': 'tpcc_factors',
    'MVCC (W1)': 'm/1',
    'MVCC (W1) + HT': 'm.h/1',
    'MVCC (W1) + RP': 'm.a/1',
    'MVCC (W1) + HT + RP': 'm.h.a/1',
    'MVCC (W1) + CU + HT + ST + RP': 'm.h.a.c.s/1'
}

ycsb_sys_name_map = {
    'name': 'ycsb',
    'OCC': 'o',
    'OCC + CU': 'o.c',
    'OCC + SV': 'o.s',
    'OCC + CU + SV': 'o.c.s',
    'MVCC': 'm',
    'MVCC + ST': 'm.s',
    'MVCC + CU': 'm.c',
    'MVCC + CU + ST': 'm.c.s',
}

wiki_sys_name_map = {
    'name': 'wiki',
    'OCC (W1)': 'o/1',
    'OCC + CU (W1)': 'o.c/1',
    'OCC (W1) + SV': 'o.s/1',
    'OCC + CU (W1) + SV': 'o.c.s/1',
    'MVCC (W1)': 'm/1',
    'MVCC (W1) + ST': 'm.s/1',
    'MVCC + CU (W1)': 'm.c/1',
    'MVCC + CU (W1) + ST': 'm.c.s/1',
}

rubis_sys_name_map = {
    'name': 'rubis',
    'OCC (W1)': 'o/1',
    'OCC + CU (W1)': 'o.c/1',
    'OCC (W1) + SV': 'o.s/1',
    'OCC + CU (W1) + SV': 'o.c.s/1',
    'MVCC (W1)': 'm/1',
    'MVCC (W1) + ST': 'm.s/1',
    'MVCC + CU (W1)': 'm.c/1',
    'MVCC + CU (W1) + ST': 'm.c.s/1',
}

tpcc_out_file = config.get_result_file(config.MVSTOConfig.NAME)
tpcc_result_file = 'tpcc_results.txt'
ycsb_out_file = config.get_result_file(config.MVSTOYCSBConfig.NAME)
ycsb_result_file = 'ycsb_results.txt'
wiki_out_file = config.get_result_file(config.MVSTOWikiConfig.NAME)
wiki_result_file = 'wiki_results.txt'
rubis_out_file = config.get_result_file(config.MVSTORubisConfig.NAME)
rubis_result_file = 'rubis_results.txt'
tpcc_factors_out_file = config.get_result_file(config.MVSTOTPCCFactorsConfig.NAME)
tpcc_factors_result_file = 'tpcc_factors_results.txt'


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
        print('Input file {} not found, not processed.'.format(infile))
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

        with open('c-0w-results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'c'
                d3 = '0'
                for i in range(WILLIAM_TRIALS):
                    runner_key = br.key(d1,d2,d3,i)
                    cell_val = row['Cicada (W0)' + ' [T{}]'.format(i+1)]
                    if cell_val == "":
                        cell_val = '0.0'
                    xput = float(cell_val) * 1000000.0
                    compatible_results[runner_key] = (xput, 0.0, 0.0)
    except (FileNotFoundError, IOError):
        print('Cicada results files not found, not processed.')
        return {}
    return compatible_results

def convert_ermia(compatible_results):
    try:
        with open('e-1w-results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'e'
                d3 = '1'
                for i in range(WILLIAM_TRIALS):
                    runner_key = br.key(d1,d2,d3,i)
                    cell_val = row['ERMIA (W1)' + ' [T{}]'.format(i+1)]
                    if cell_val == "":
                        cell_val = '0.0'
                    xput = float(cell_val)
                    compatible_results[runner_key] = (xput, 0.0, 0.0)

        with open('e-4w-results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'e'
                d3 = '4'
                for i in range(WILLIAM_TRIALS):
                    runner_key = br.key(d1,d2,d3,i)
                    cell_val = row['ERMIA (W4)' + ' [T{}]'.format(i+1)]
                    if cell_val == "":
                        cell_val = '0.0'
                    xput = float(cell_val)
                    compatible_results[runner_key] = (xput, 0.0, 0.0)

        with open('e-0w-results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'e'
                d3 = '0'
                for i in range(WILLIAM_TRIALS):
                    runner_key = br.key(d1,d2,d3,i)
                    cell_val = row['ERMIA (W0)' + ' [T{}]'.format(i+1)]
                    if cell_val == "":
                        cell_val = '0.0'
                    xput = float(cell_val)
                    compatible_results[runner_key] = (xput, 0.0, 0.0)
    except (FileNotFoundError, IOError):
        print('ERMIA results files not found, not processed.')
        return {}
    return compatible_results

def convert_mocc(compatible_results):
    try:
        with open('mocc_results.txt', 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                d2 = 'mocc'
                for d3 in ['1', '4', '0']:
                    for i in range(WILLIAM_TRIALS):
                        runner_key = br.key(d1,d2,d3,i)
                        cell_val = row['MOCC (W{}) [T{}]'.format(d3, i+1)]
                        if cell_val == "":
                            cell_val = '0.0'
                        xput = float(cell_val) * 1000000.0
                        compatible_results[runner_key] = (xput, 0.0, 0.0)
    except (FileNotFoundError, IOError):
        print('MOCC results files not found, not processed.')
        return {}
    return compatible_results

def convert_ycsb_all(sys_name_map, compatible_results):
    sys_name_reverse_map = {}
    sys_short_names = []

    for k,v in sys_name_map.items():
        if k == 'name':
            continue
        sys_name_reverse_map[v] = k
        sys_short_names.append(v)

    ycsb_types = ('a', 'b')
    for yt in ycsb_types:
        try:
            filename = 'ycsb_{}_results.txt'.format(yt)
            with open(filename, 'r') as rf:
                reader = csv.DictReader(rf)
                for row in reader:
                    d1 = row['# Threads']
                    d3 = yt
                    for v in sys_short_names:
                        d2 = v
                        long_name = sys_name_reverse_map[v]
                        for i in range(WILLIAM_TRIALS):
                            runner_key = br.key(d1, d2, d3, i)
                            col_key = long_name
                            if d3 == 'a':
                                col_key += ' (A)'
                            else:
                                col_key += ' (B)'
                            col_key += ' [T{}]'.format(i+1)
                            xput = float(row[col_key])
                            compatible_results[runner_key] = (xput, 0.0, 0.0)
        except (FileNotFoundError, IOError):
            print('File {} not found, not processed.'.format(filename))
    return compatible_results

if __name__ == '__main__':
    results = {}
    results = convert(tpcc_result_file, tpcc_sys_name_map, results)
    results = convert_cicada(results)
    results = convert_ermia(results)
    results = convert_mocc(results)
    if results:
        with open(tpcc_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert_ycsb_all(ycsb_sys_name_map, results)
    if results:
        with open(ycsb_out_file, 'w') as wf:
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
    results = {}
    results = convert(tpcc_factors_result_file, tpcc_factors_sys_name_map, results)
    results = convert_cicada(results)
    if results:
        with open(tpcc_factors_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)

