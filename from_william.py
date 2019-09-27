#!/usr/bin/env python3

import config
import json
import csv

from runner import BenchRunner as br

WILLIAM_TRIALS = 5

tpcc_sys_name_map = {
    'name': 'tpcc',
    'OCC (W0)': 'o/0',
    #'OCC (W0) + NOREG': 'onr/0',
    'OCC + CU (W0)': 'o.c/0',
    'OCC (W0) + SV': 'o.s/0',
    'OCC + CU (W0) + SV': 'o.c.s/0',
    'OCC (W1)': 'o/1',
    #'OCC (W1) + NOREG': 'onr/1',
    'OCC + CU (W1)': 'o.c/1',
    'OCC (W1) + SV': 'o.s/1',
    'OCC + CU (W1) + SV': 'o.c.s/1',
    'OCC (W4)': 'o/4',
    #'OCC (W4) + NOREG': 'onr/4',
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

tpcc_opacity_sys_name_map = {
    'name': 'tpcc',
    'OPQ (W0)': 'op/0',
    'OPQ + CU (W0)': 'op.c/0',
    'OPQ (W0) + SV': 'op.s/0',
    'OPQ + CU (W0) + SV': 'op.c.s/0',
    'OPQ (W1)': 'op/1',
    'OPQ + CU (W1)': 'op.c/1',
    'OPQ (W1) + SV': 'op.s/1',
    'OPQ + CU (W1) + SV': 'op.c.s/1',
    'OPQ (W4)': 'op/4',
    'OPQ + CU (W4)': 'op.c/4',
    'OPQ (W4) + SV': 'op.s/4',
    'OPQ + CU (W4) + SV': 'op.c.s/4'
}

tpcc_tictoc_sys_name_map = {
    'name': 'tpcc',
    'TicToc (W0)': 'tictoc/0',
    'TicToc (W1)': 'tictoc/1',
    'TicToc (W4)': 'tictoc/4',
    'TicToc + CU (W0)': 'tictoc.c/0',
    'TicToc + CU (W1)': 'tictoc.c/1',
    'TicToc + CU (W4)': 'tictoc.c/4',
    'TicToc (W0) + ST': 'tictoc.s/0',
    'TicToc (W1) + ST': 'tictoc.s/1',
    'TicToc (W4) + ST': 'tictoc.s/4',
    'TicToc + CU (W0) + ST': 'tictoc.c.s/0',
    'TicToc + CU (W1) + ST': 'tictoc.c.s/1',
    'TicToc + CU (W4) + ST': 'tictoc.c.s/4',
}

tpcc_gc_sys_name_map = {
    'name': 'tpcc',
    'MVCC (W{} R0)': 'm.r0',
    'MVCC (W{} R1000)': 'm.r1k',
    'MVCC (W{} R100000)': 'm.r100k',
}

tpcc_safe_flatten_sys_name_map = {
    'name': 'tpcc',
    'MVCC (W0)': 'mf/0',
    'MVCC (W0) + ST': 'mf.s/0',
    'MVCC + CU (W0)': 'mf.c/0',
    'MVCC + CU (W0) + ST': 'mf.c.s/0',
    'MVCC (W1)': 'mf/1',
    'MVCC (W1) + ST': 'mf.s/1',
    'MVCC + CU (W1)': 'mf.c/1',
    'MVCC + CU (W1) + ST': 'mf.c.s/1',
    'MVCC (W4)': 'mf/4',
    'MVCC (W4) + ST': 'mf.s/4',
    'MVCC + CU (W4)': 'mf.c/4',
    'MVCC + CU (W4) + ST': 'mf.c.s/4'
}

tpcc_factors_sys_name_map = {
    'name': 'tpcc_factors',
    'MVCC (W1)-HT': 'm.h/1',
    'MVCC (W1)-AL': 'm.a/1',
    'MVCC (W1)-NOEXP': 'm.e/1',
    'MVCC (W1)-BACKOFF': 'm.r/1',
    'MVCC (W1)-AL-BACKOFF-HT': 'm.a.r.h/1'
}

tpcc_stacked_factors_sys_name_map = {
    'name': 'tpcc_stacked_factors',
    'MVCC (W1)NAIVE': 'mn/1',
    'MVCC (W1)+AL': 'mn.a/1',
    'MVCC (W1)+AL+BACKOFF': 'mn.a.r/1',
    'MVCC (W1)+AL+BACKOFF+NOEXC': 'mn.a.r.e/1',
    'MVCC (W1)BASE': 'mn.a.r.e.h/1',
    'MVCC (W4)NAIVE': 'mn/4',
    'MVCC (W4)+AL': 'mn.a/4',
    'MVCC (W4)+AL+BACKOFF': 'mn.a.r/4',
    'MVCC (W4)+AL+BACKOFF+NOEXC': 'mn.a.r.e/4',
    'MVCC (W4)BASE': 'mn.a.r.e.h/4',
    'MVCC (W0)NAIVE': 'mn/0',
    'MVCC (W0)+AL': 'mn.a/0',
    'MVCC (W0)+AL+BACKOFF': 'mn.a.r/0',
    'MVCC (W0)+AL+BACKOFF+NOEXC': 'mn.a.r.e/0',
    'MVCC (W0)BASE': 'mn.a.r.e.h/0',
    'OCC (W1)NAIVE': 'on/1',
    'OCC (W1)+AL': 'on.a/1',
    'OCC (W1)+AL+BACKOFF': 'on.a.r/1',
    'OCC (W1)+AL+BACKOFF+NOEXC': 'on.a.r.e/1',
    'OCC (W1)BASE': 'on.a.r.e.h/1',
    'OCC (W4)NAIVE': 'on/4',
    'OCC (W4)+AL': 'on.a/4',
    'OCC (W4)+AL+BACKOFF': 'on.a.r/4',
    'OCC (W4)+AL+BACKOFF+NOEXC': 'on.a.r.e/4',
    'OCC (W4)BASE': 'on.a.r.e.h/4',
    'OCC (W0)NAIVE': 'on/0',
    'OCC (W0)+AL': 'on.a/0',
    'OCC (W0)+AL+BACKOFF': 'on.a.r/0',
    'OCC (W0)+AL+BACKOFF+NOEXC': 'on.a.r.e/0',
    'OCC (W0)BASE': 'on.a.r.e.h/0'
}

tpcc_index_contention_sys_name_map = {
	'name': 'tpcc_index_contention',
	'OCC (W1)-CONT-AWARE-IDX': 'on/1',
	'OCC (W4)-CONT-AWARE-IDX': 'on/4',
	'OCC (W0)-CONT-AWARE-IDX': 'on/0',
	'OCC (W1)BASE': 'o/1',
	'OCC (W4)BASE': 'o/4',
	'OCC (W0)BASE': 'o/0'
}

ycsb_sys_name_map = {
    'name': 'ycsb',
    'OCC ({})': 'o',
    'OCC ({}) + CU': 'o.c',
    'OCC ({}) + SV': 'o.s',
    'OCC ({}) + CU + SV': 'o.c.s',
    'MVCC ({})': 'm',
    'MVCC ({}) + ST': 'm.s',
    'MVCC ({}) + CU': 'm.c',
    'MVCC ({}) + CU + ST': 'm.c.s',
}

ycsb_tictoc_comp_sys_name_map = {
    'name': 'ycsb_tictoc_comp',
    'OCC (A)': 'o/a',
    'OCC (B)': 'o/b',
    'MVCC (A)': 'm/a',
    'MVCC (B)': 'm/b',
    'TicToc (A)': 'tictoc/a',
    'TicToc (B)': 'tictoc/b',

    'OCC + CU (A)': 'o.c/a',
    'OCC + CU (B)': 'o.c/b',
    'MVCC + CU (A)': 'm.c/a',
    'MVCC + CU (B)': 'm.c/b',
    'TicToc + CU (A)': 'tictoc.c/a',
    'TicToc + CU (B)': 'tictoc.c/b',

    'OCC (A) + SV': 'o.s/a',
    'OCC (B) + SV': 'o.s/b',
    'MVCC (A) + ST': 'm.s/a',
    'MVCC (B) + ST': 'm.s/b',
    'TicToc (A) + SV': 'tictoc.s/a',
    'TicToc (B) + SV': 'tictoc.s/b',

    'OCC + CU (A) + SV': 'o.c.s/a',
    'OCC + CU (B) + SV': 'o.c.s/b',
    'MVCC + CU (A) + ST': 'm.c.s/a',
    'MVCC + CU (B) + ST': 'm.c.s/b',
    'TicToc + CU (A) + SV': 'tictoc.c.s/a',
    'TicToc + CU (B) + SV': 'tictoc.c.s/b',
}

wiki_sys_name_map = {
    'name': 'wiki',
    'OCC': 'o/1',
    'OCC + CU': 'o.c/1',
    'OCC + SV': 'o.s/1',
    'OCC + CU + SV': 'o.c.s/1',
    'TicToc': 'tictoc/1',
    'TicToc + CU': 'tictoc.c/1',
    'TicToc + SV': 'tictoc.s/1',
    'TicToc + CU + SV': 'tictoc.c.s/1',
    'MVCC': 'm/1',
    'MVCC + ST': 'm.s/1',
    'MVCC + CU': 'm.c/1',
    'MVCC + CU + ST': 'm.c.s/1',
}

rubis_sys_name_map = {
    'name': 'rubis',
    'OCC': 'o/1',
    'OCC + CU': 'o.c/1',
    'OCC + SV': 'o.s/1',
    'OCC + CU + SV': 'o.c.s/1',
    'TicToc': 'tictoc/1',
    'TicToc + CU': 'tictoc.c/1',
    'TicToc + SV': 'tictoc.s/1',
    'TicToc + CU + SV': 'tictoc.c.s/1',
    'MVCC': 'm/1',
    'MVCC + ST': 'm.s/1',
    'MVCC + CU': 'm.c/1',
    'MVCC + CU + ST': 'm.c.s/1',
}

tpcc_out_file = config.get_result_file(config.MVSTOConfig.NAME)
tpcc_result_file = 'tpcc_results.txt'
tpcc_opacity_file = 'tpcc_opacity_results.txt'
tpcc_tictoc_file = 'tpcc_tictoc_results.txt'
tpcc_safe_flatten_file = 'tpcc_safe_flatten_results.txt'
ycsb_out_file = config.get_result_file(config.MVSTOYCSBConfig.NAME)
ycsb_result_file = 'ycsb_results.txt'

# YCSB baseline CC comparisons (convert using the generic convert() function)
ycsb_tictoc_comp_out_file = config.get_result_file(config.YCSBTicTocCompConfig.NAME)
ycsb_tictoc_comp_result_file = 'ycsb_tictoc_results.txt'

wiki_out_file = config.get_result_file(config.MVSTOWikiConfig.NAME)
wiki_result_file = 'wiki_results.txt'
rubis_out_file = config.get_result_file(config.MVSTORubisConfig.NAME)
rubis_result_file = 'rubis_results.txt'
tpcc_stacked_factors_out_file = config.get_result_file(config.MVSTOTPCCStackedFactorsConfig.NAME)
tpcc_stacked_factors_result_file = 'tpcc_stacked_factors_results.txt'
tpcc_index_contention_out_file = config.get_result_file(config.MVSTOTPCCIndexContentionConfig.NAME)
tpcc_index_contention_result_file = 'tpcc_index_contention_results.txt'
tpcc_factors_out_file = config.get_result_file(config.MVSTOTPCCFactorsConfig.NAME)
tpcc_factors_result_file = 'tpcc_factors_results.txt'


def convert(infile, sys_name_map, compatible_results):
    sys_name_reverse_map = {}
    sys_short_names = []

    for k,v in sys_name_map.items():
        if k == 'name':
            continue
        sys_name_reverse_map[v] = k
        sys_short_names.append(v)

    num_trials = WILLIAM_TRIALS
    if sys_name_map['name'] == 'rubis':
        num_trials = 10

    try:
        with open(infile, 'r') as rf:
            reader = csv.DictReader(rf)
            for row in reader:
                d1 = row['# Threads']
                for v in sys_short_names:
                    long_name = sys_name_reverse_map[v]
                    for i in range(num_trials):
                        (d2, d3) = v.split('/')
                        runner_key = br.key(d1, d2, d3, i)
                        col_key = long_name
                        col_key += ' [T{}]'.format(i+1)
                        try:
                            xput = float(row[col_key])
                        except KeyError:
                            print('key {} not found.'.format(runner_key))
                            continue
                        if runner_key in compatible_results:
                            print('WARNING: Overriding result runner key {}'.format(runner_key))
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
                                col_key = col_key.format('A')
                            elif d3 == 'b':
                                col_key = col_key.format('B')
                            else:
                                col_key = col_key.format('C')
                            col_key += ' [T{}]'.format(i+1)
                            xput = float(row[col_key])
                            compatible_results[runner_key] = (xput, 0.0, 0.0)
        except (FileNotFoundError, IOError):
            print('File {} not found, not processed.'.format(filename))
    return compatible_results


def convert_tpcc_gc_all(sys_name_map, compatible_results):
    sys_name_reverse_map = {}
    sys_short_names = []

    for k,v in sys_name_map.items():
        if k == 'name':
            continue
        sys_name_reverse_map[v] = k
        sys_short_names.append(v)

    num_whs = ('1', '0')
    for wh in num_whs:
        try:
            filename = 'tpcc_gc_results.txt'
            with open(filename, 'r') as rf:
                reader = csv.DictReader(rf)
                for row in reader:
                    d1 = row['# Threads']
                    d3 = wh
                    for v in sys_short_names:
                        d2 = v
                        long_name = sys_name_reverse_map[v]
                        for i in range(WILLIAM_TRIALS):
                            runner_key = br.key(d1, d2, d3, i)
                            col_key = long_name
                            col_key = col_key.format(d3)
                            col_key += ' [T{}]'.format(i+1)
                            xput = float(row[col_key])
                            compatible_results[runner_key] = (xput, 0.0, 0.0)
        except (FileNotFoundError, IOError):
            print('File {} not found, not processed.'.format(filename))
    return compatible_results

if __name__ == '__main__':
    results = {}
    results = convert(tpcc_result_file, tpcc_sys_name_map, results)
    results = convert(tpcc_opacity_file, tpcc_opacity_sys_name_map, results)
    results = convert(tpcc_tictoc_file, tpcc_tictoc_sys_name_map, results)
    results = convert_tpcc_gc_all(tpcc_gc_sys_name_map, results)
    results = convert(tpcc_safe_flatten_file, tpcc_safe_flatten_sys_name_map, results)
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
    results = convert(ycsb_tictoc_comp_result_file, ycsb_tictoc_comp_sys_name_map, results)
    if results:
        with open(ycsb_tictoc_comp_out_file, 'w') as wf:
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
    results = convert(tpcc_result_file, tpcc_sys_name_map, results)
    results = convert(tpcc_factors_result_file, tpcc_factors_sys_name_map, results)
    results = convert_cicada(results)
    if results:
        with open(tpcc_factors_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)

    results = {}
    results = convert(tpcc_stacked_factors_result_file, tpcc_stacked_factors_sys_name_map, results)
    if results:
        with open(tpcc_stacked_factors_out_file, 'w') as wf:
            json.dump(results, wf, indent=4, sort_keys=True)
    results = {}
    results = convert(tpcc_index_contention_result_file, tpcc_index_contention_sys_name_map, results)
    if results:
    	with open(tpcc_index_contention_out_file, 'w') as wf:
    		json.dump(results, wf, indent=4, sort_keys=True)

